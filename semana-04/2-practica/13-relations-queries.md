# Práctica 13: Relaciones Básicas entre Tablas

## 🎯 Objetivo

Aprender a crear relaciones simples entre tablas usando SQLAlchemy. Implementarás una relación básica **One-to-Many** (uno a muchos) entre categorías y productos.

- Crear una tabla de categorías
- Relacionar productos con categorías
- Realizar consultas básicas con relaciones

## ⏱️ Tiempo: 40 minutos

## 📋 Pre-requisitos

- ✅ Práctica 12 completada (CRUD Mejorado)
- ✅ API de productos funcionando
- ✅ Base de datos con tabla productos

---

## 🚀 Paso 1: Crear Modelo de Categoría (15 min)

### Añadir a models.py

```python
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# Modelo existente de Producto (actualizar)
class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
    descripcion = Column(String)

    # NUEVO: Relación con categoría
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    categoria = relationship("Categoria", back_populates="productos")

# NUEVO: Modelo de Categoría
class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    descripcion = Column(String)

    # Relación: una categoría tiene muchos productos
    productos = relationship("Producto", back_populates="categoria")
```

---

## 📨 Paso 2: Actualizar Schemas (10 min)

### Actualizar schemas.py

```python
from pydantic import BaseModel
from typing import List, Optional

# Schemas para Categoría
class CategoriaBase(BaseModel):
    nombre: str
    descripcion: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True

# Schemas actualizados para Producto
class ProductoBase(BaseModel):
    nombre: str
    precio: float
    descripcion: str
    categoria_id: Optional[int] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: str = None
    precio: float = None
    descripcion: str = None
    categoria_id: int = None

# Producto con información de categoría incluida
class ProductoConCategoria(ProductoBase):
    id: int
    categoria: Optional[Categoria] = None

    class Config:
        from_attributes = True

# Categoría con lista de productos
class CategoriaConProductos(Categoria):
    productos: List[ProductoBase] = []

    class Config:
        from_attributes = True
```

---

## 🔧 Paso 3: Actualizar Funciones CRUD (10 min)

### Añadir a crud.py

```python
from sqlalchemy.orm import Session, joinedload
import models, schemas

# Funciones CRUD para Categorías
def crear_categoria(db: Session, categoria: schemas.CategoriaCreate):
    """Crear una nueva categoría"""
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def obtener_categorias(db: Session):
    """Obtener todas las categorías"""
    return db.query(models.Categoria).all()

def obtener_categoria(db: Session, categoria_id: int):
    """Obtener categoría por ID"""
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()

def obtener_categoria_con_productos(db: Session, categoria_id: int):
    """Obtener categoría con sus productos"""
    return db.query(models.Categoria).options(
        joinedload(models.Categoria.productos)
    ).filter(models.Categoria.id == categoria_id).first()

# Funciones actualizadas para Productos
def obtener_productos_con_categoria(db: Session, skip: int = 0, limit: int = 10):
    """Obtener productos con información de categoría"""
    return db.query(models.Producto).options(
        joinedload(models.Producto.categoria)
    ).offset(skip).limit(limit).all()

def obtener_productos_por_categoria(db: Session, categoria_id: int):
    """Obtener productos de una categoría específica"""
    return db.query(models.Producto).filter(
        models.Producto.categoria_id == categoria_id
    ).all()
```

---

## 🌐 Paso 4: Actualizar API (5 min)

### Añadir endpoints a main.py

```python
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, get_db

# Crear tablas (incluye las nuevas)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Productos con Categorías")

# ENDPOINTS PARA CATEGORÍAS

@app.post("/categorias/", response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.crear_categoria(db=db, categoria=categoria)

@app.get("/categorias/")
def listar_categorias(db: Session = Depends(get_db)):
    return crud.obtener_categorias(db)

@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaConProductos)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.obtener_categoria_con_productos(db, categoria_id=categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

# ENDPOINTS ACTUALIZADOS PARA PRODUCTOS

@app.get("/productos/", response_model=List[schemas.ProductoConCategoria])
def listar_productos_con_categoria(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.obtener_productos_con_categoria(db, skip=skip, limit=limit)

@app.get("/categorias/{categoria_id}/productos/")
def productos_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    productos = crud.obtener_productos_por_categoria(db, categoria_id=categoria_id)
    return {
        "categoria_id": categoria_id,
        "productos": productos,
        "total": len(productos)
    }

# ... resto de endpoints existentes ...
```

---

## 🧪 Paso 5: Probar las Relaciones

### Crear categorías

```bash
# Crear categoría de electrónicos
curl -X POST "http://localhost:8000/categorias/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Electrónicos", "descripcion": "Dispositivos electrónicos"}'

# Crear categoría de libros
curl -X POST "http://localhost:8000/categorias/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Libros", "descripcion": "Libros y literatura"}'
```

### Crear productos con categoría

```bash
# Crear producto en categoría 1 (Electrónicos)
curl -X POST "http://localhost:8000/productos/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Laptop", "precio": 999.99, "descripcion": "Laptop gaming", "categoria_id": 1}'

# Crear producto en categoría 2 (Libros)
curl -X POST "http://localhost:8000/productos/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Python para Todos", "precio": 29.99, "descripcion": "Libro de programación", "categoria_id": 2}'
```

### Probar consultas con relaciones

```bash
# Ver productos con información de categoría
curl "http://localhost:8000/productos/"

# Ver categoría con sus productos
curl "http://localhost:8000/categorias/1"

# Ver solo productos de una categoría
curl "http://localhost:8000/categorias/1/productos/"
```

---

## ✅ Verificación

### Funcionalidades de Relaciones

- [ ] **Crear categorías** - Nuevas categorías se guardan correctamente
- [ ] **Crear productos con categoría** - Productos se asocian a categorías
- [ ] **Consultar productos con categoría** - Se muestra la información completa
- [ ] **Consultar categoría con productos** - Se muestran productos de la categoría
- [ ] **Filtrar por categoría** - Solo productos de una categoría específica

### Estructura Final

```text
semana-04-practica/
├── main.py          # ✅ API con endpoints de categorías
├── crud.py          # ✅ Funciones CRUD con relaciones
├── database.py      # ✅ Configuración (sin cambios)
├── models.py        # ✅ Modelos con relaciones
├── schemas.py       # ✅ Schemas con relaciones
├── requirements.txt # ✅ Dependencias (sin cambios)
└── productos.db     # ✅ Base de datos con nuevas tablas
```

---

## 🎯 Resumen

### Lo que Aprendiste

- ✅ **Relación One-to-Many** - Una categoría tiene muchos productos
- ✅ **Foreign Keys** - Conectar tablas con `ForeignKey`
- ✅ **Relationship** - Navegación entre modelos relacionados
- ✅ **Joins automáticos** - SQLAlchemy maneja las consultas
- ✅ **Datos anidados** - Respuestas con información relacionada

### Conceptos Clave

1. **ForeignKey** - Referencia a otra tabla
2. **relationship()** - Navegación entre modelos
3. **back_populates** - Relación bidireccional
4. **joinedload()** - Cargar datos relacionados
5. **Schemas anidados** - Pydantic con relaciones

### Próximo Paso

¡Ahora tu API maneja relaciones básicas! En la siguiente práctica aprenderemos sobre migraciones y testing con base de datos.

---

## 🔗 Enlaces Útiles

- [SQLAlchemy Relationships](https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html)
- [FastAPI with Relationships](https://fastapi.tiangolo.com/tutorial/sql-databases/#create-the-relationships)
- [Pydantic Nested Models](https://docs.pydantic.dev/latest/concepts/models/#nested-models)

