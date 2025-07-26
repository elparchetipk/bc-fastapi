# Ejercicios de Práctica - Semana 4

## 🎯 Objetivo General

Reforzar los conceptos de base de datos aprendidos en las prácticas mediante ejercicios simples y directos.

**⏱️ Tiempo total:** 45 minutos  
**📊 Nivel:** Básico-Intermedio

---

## 📋 Ejercicio 1: Tienda de Libros (25 min)

### Descripción

Crear una API simple para una tienda de libros con autores y libros relacionados.

### Objetivos

1. **Crear modelos básicos**:

```python
# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    nacionalidad = Column(String)

    # Relación: un autor tiene muchos libros
    libros = relationship("Libro", back_populates="autor")

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    precio = Column(Float)
    paginas = Column(Integer)

    # Relación con autor
    autor_id = Column(Integer, ForeignKey("autores.id"))
    autor = relationship("Autor", back_populates="libros")
```

1. **Crear schemas**:

```python
# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class AutorBase(BaseModel):
    nombre: str
    nacionalidad: str

class AutorCreate(AutorBase):
    pass

class Autor(AutorBase):
    id: int

    class Config:
        from_attributes = True

class LibroBase(BaseModel):
    titulo: str
    precio: float
    paginas: int
    autor_id: Optional[int] = None

class LibroCreate(LibroBase):
    pass

class LibroConAutor(LibroBase):
    id: int
    autor: Optional[Autor] = None

    class Config:
        from_attributes = True

class AutorConLibros(Autor):
    libros: List[LibroBase] = []

    class Config:
        from_attributes = True
```

1. **Implementar endpoints básicos**:

```python
# main.py (añadir a tu archivo existente)

# AUTORES
@app.post("/autores/", response_model=schemas.Autor)
def crear_autor(autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    db_autor = models.Autor(**autor.dict())
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor

@app.get("/autores/")
def listar_autores(db: Session = Depends(get_db)):
    return db.query(models.Autor).all()

@app.get("/autores/{autor_id}", response_model=schemas.AutorConLibros)
def obtener_autor_con_libros(autor_id: int, db: Session = Depends(get_db)):
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

# LIBROS
@app.post("/libros/", response_model=schemas.LibroConAutor)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    db_libro = models.Libro(**libro.dict())
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

@app.get("/libros/", response_model=List[schemas.LibroConAutor])
def listar_libros_con_autor(db: Session = Depends(get_db)):
    return db.query(models.Libro).all()
```

### Checklist de Verificación

- [ ] Modelos Autor y Libro creados
- [ ] Relación One-to-Many configurada
- [ ] Schemas con y sin relaciones anidadas
- [ ] Endpoints CRUD básicos funcionando
- [ ] Puedes crear autores y libros
- [ ] Puedes ver libros con información del autor
- [ ] Puedes ver autores con sus libros

---

## 📋 Ejercicio 2: Validaciones y Búsquedas (20 min)

### Contexto

Mejorar la API de libros con validaciones básicas y funciones de búsqueda.

### Tareas

1. **Añadir validaciones simples**:

```python
# Actualizar schemas.py
from pydantic import BaseModel, validator

class LibroBase(BaseModel):
    titulo: str
    precio: float
    paginas: int
    autor_id: Optional[int] = None

    @validator('precio')
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v

    @validator('paginas')
    def validar_paginas(cls, v):
        if v <= 0:
            raise ValueError('El número de páginas debe ser mayor a 0')
        return v

    @validator('titulo')
    def validar_titulo(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('El título no puede estar vacío')
        return v.strip()
```

1. **Añadir funciones de búsqueda**:

```python
# Añadir a crud.py (crear el archivo si no existe)
from sqlalchemy.orm import Session
from sqlalchemy import or_
import models

def buscar_libros_por_titulo(db: Session, busqueda: str):
    """Buscar libros por título"""
    return db.query(models.Libro).filter(
        models.Libro.titulo.contains(busqueda)
    ).all()

def buscar_libros_por_autor(db: Session, nombre_autor: str):
    """Buscar libros por nombre del autor"""
    return db.query(models.Libro).join(models.Autor).filter(
        models.Autor.nombre.contains(nombre_autor)
    ).all()

def obtener_libros_por_precio(db: Session, precio_min: float, precio_max: float):
    """Obtener libros en rango de precio"""
    return db.query(models.Libro).filter(
        models.Libro.precio >= precio_min,
        models.Libro.precio <= precio_max
    ).all()
```

1. **Añadir endpoints de búsqueda**:

```python
# Añadir a main.py
import crud

@app.get("/libros/buscar/")
def buscar_libros(
    titulo: str = Query(None, description="Buscar por título"),
    autor: str = Query(None, description="Buscar por autor"),
    precio_min: float = Query(None, description="Precio mínimo"),
    precio_max: float = Query(None, description="Precio máximo"),
    db: Session = Depends(get_db)
):
    if titulo:
        libros = crud.buscar_libros_por_titulo(db, titulo)
    elif autor:
        libros = crud.buscar_libros_por_autor(db, autor)
    elif precio_min and precio_max:
        libros = crud.obtener_libros_por_precio(db, precio_min, precio_max)
    else:
        libros = db.query(models.Libro).all()

    return {
        "libros": libros,
        "total": len(libros)
    }

@app.get("/estadisticas/")
def estadisticas_libros(db: Session = Depends(get_db)):
    """Estadísticas básicas de la librería"""
    total_libros = db.query(models.Libro).count()
    total_autores = db.query(models.Autor).count()

    if total_libros > 0:
        precios = [libro.precio for libro in db.query(models.Libro).all()]
        precio_promedio = sum(precios) / len(precios)
        precio_max = max(precios)
        precio_min = min(precios)
    else:
        precio_promedio = precio_max = precio_min = 0

    return {
        "total_libros": total_libros,
        "total_autores": total_autores,
        "precio_promedio": precio_promedio,
        "precio_mas_alto": precio_max,
        "precio_mas_bajo": precio_min
    }
```

### Lista de Verificación Final

- [ ] Validaciones funcionando (precio, páginas, título)
- [ ] Búsqueda por título funciona
- [ ] Búsqueda por autor funciona
- [ ] Filtro por rango de precio funciona
- [ ] Endpoint de estadísticas funciona
- [ ] Errores de validación se muestran correctamente

---

## 🧪 Ejercicio Bonus: Tests Básicos (Opcional)

Si tienes tiempo extra, crea algunos tests simples:

```python
# test_libros.py
import pytest
from fastapi.testclient import TestClient

def test_crear_autor(client: TestClient):
    response = client.post(
        "/autores/",
        json={"nombre": "Gabriel García Márquez", "nacionalidad": "Colombiana"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Gabriel García Márquez"

def test_crear_libro_con_autor(client: TestClient):
    # Crear autor primero
    autor_response = client.post(
        "/autores/",
        json={"nombre": "Isabel Allende", "nacionalidad": "Chilena"}
    )
    autor_id = autor_response.json()["id"]

    # Crear libro
    response = client.post(
        "/libros/",
        json={
            "titulo": "La Casa de los Espíritus",
            "precio": 25.99,
            "paginas": 450,
            "autor_id": autor_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["titulo"] == "La Casa de los Espíritus"
    assert data["autor"]["nombre"] == "Isabel Allende"

def test_validacion_precio_negativo(client: TestClient):
    response = client.post(
        "/libros/",
        json={
            "titulo": "Libro Inválido",
            "precio": -10.99,
            "paginas": 100
        }
    )
    assert response.status_code == 422  # Error de validación
```

---

## 🎯 Entregables

### Estructura Final del Proyecto

```text
semana-04-ejercicios/
├── main.py          # API con endpoints de autores y libros
├── models.py        # Modelos Autor y Libro con relaciones
├── schemas.py       # Schemas con validaciones
├── crud.py          # Funciones de búsqueda
├── database.py      # Configuración de BD
├── test_libros.py   # Tests básicos (opcional)
├── requirements.txt # Dependencias
└── libros.db       # Base de datos SQLite
```

### Funcionalidades Implementadas

- ✅ **Modelos relacionados** - Autor y Libro con One-to-Many
- ✅ **CRUD completo** - Crear, leer para ambas entidades
- ✅ **Validaciones** - Precio, páginas, título
- ✅ **Búsquedas** - Por título, autor, rango de precio
- ✅ **Estadísticas** - Resumen de datos básicos
- ✅ **Tests básicos** - Verificación de funcionamiento (opcional)

---

## 🚀 Desafío Extra (Para los Más Avanzados)

Si completaste todo y quieres más desafío:

1. **Añadir categorías** - Crear modelo Categoria y relacionarlo con Libro
2. **Paginación** - Implementar `skip` y `limit` en endpoints de listado
3. **Filtros combinados** - Buscar por título Y autor simultáneamente
4. **Ordenamiento** - Ordenar por precio, título, número de páginas

---

## 📚 Recursos de Apoyo

- [SQLAlchemy Relationships](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html)
- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [FastAPI Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)

¡Buena suerte con los ejercicios! 🎉
