# Práctica 12: CRUD Mejorado con Base de Datos

## 🎯 Objetivo

Mejorar las operaciones CRUD básicas añadiendo validaciones simples y manejo de errores comunes. Aprenderás a:

- Validar datos antes de guardar
- Manejar errores comunes de base de datos
- Implementar búsquedas básicas
- Añadir funcionalidades útiles

## ⏱️ Tiempo: 45 minutos

## 📋 Pre-requisitos

- ✅ Práctica 11 completada (SQLAlchemy Setup)
- ✅ API básica funcionando
- ✅ Base de datos con tabla productos

---

## 🚀 Paso 1: Mejorar Validaciones (15 min)

### Actualizar schemas.py

```python
from pydantic import BaseModel, validator

class ProductoBase(BaseModel):
    nombre: str
    precio: float
    descripcion: str

    @validator('nombre')
    def validar_nombre(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('El nombre no puede estar vacío')
        return v.strip()

    @validator('precio')
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    nombre: str = None
    precio: float = None
    descripcion: str = None

    @validator('precio')
    def validar_precio(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El precio debe ser mayor a 0')
        return v

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True
```

---

## 🔧 Paso 2: Funciones CRUD Mejoradas (15 min)

### Crear archivo crud.py

```python
from sqlalchemy.orm import Session
from sqlalchemy import or_
import models, schemas

def crear_producto(db: Session, producto: schemas.ProductoCreate):
    """Crear un nuevo producto"""
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto

def obtener_producto(db: Session, producto_id: int):
    """Obtener producto por ID"""
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

def obtener_productos(db: Session, skip: int = 0, limit: int = 10):
    """Obtener lista de productos con paginación"""
    return db.query(models.Producto).offset(skip).limit(limit).all()

def buscar_productos(db: Session, busqueda: str):
    """Buscar productos por nombre o descripción"""
    return db.query(models.Producto).filter(
        or_(
            models.Producto.nombre.contains(busqueda),
            models.Producto.descripcion.contains(busqueda)
        )
    ).all()

def actualizar_producto(db: Session, producto_id: int, producto: schemas.ProductoUpdate):
    """Actualizar producto existente"""
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto:
        # Solo actualizar campos que no sean None
        update_data = producto.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_producto, field, value)
        db.commit()
        db.refresh(db_producto)
    return db_producto

def eliminar_producto(db: Session, producto_id: int):
    """Eliminar producto"""
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto

def contar_productos(db: Session):
    """Contar total de productos"""
    return db.query(models.Producto).count()
```

---

## 🌐 Paso 3: Actualizar API Principal (10 min)

### Actualizar main.py

```python
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, get_db

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Productos Mejorada")

# CREATE - Crear producto con validaciones
@app.post("/productos/", response_model=schemas.Producto)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    try:
        return crud.crear_producto(db=db, producto=producto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# READ - Listar productos con paginación
@app.get("/productos/")
def listar_productos(
    skip: int = Query(0, ge=0, description="Saltar elementos"),
    limit: int = Query(10, ge=1, le=100, description="Límite de elementos"),
    db: Session = Depends(get_db)
):
    productos = crud.obtener_productos(db, skip=skip, limit=limit)
    total = crud.contar_productos(db)
    return {
        "productos": productos,
        "total": total,
        "pagina": skip // limit + 1,
        "por_pagina": limit
    }

# READ - Buscar productos
@app.get("/productos/buscar/")
def buscar_productos(
    q: str = Query(..., min_length=1, description="Término de búsqueda"),
    db: Session = Depends(get_db)
):
    productos = crud.buscar_productos(db, busqueda=q)
    return {
        "busqueda": q,
        "productos": productos,
        "total": len(productos)
    }

# READ - Obtener producto por ID
@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.obtener_producto(db, producto_id=producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

# UPDATE - Actualizar producto parcialmente
@app.patch("/productos/{producto_id}", response_model=schemas.Producto)
def actualizar_producto(
    producto_id: int,
    producto: schemas.ProductoUpdate,
    db: Session = Depends(get_db)
):
    db_producto = crud.actualizar_producto(db, producto_id=producto_id, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

# DELETE - Eliminar producto
@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = crud.eliminar_producto(db, producto_id=producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": f"Producto {producto_id} eliminado correctamente"}

# STATS - Estadísticas básicas
@app.get("/productos/stats/resumen")
def estadisticas_productos(db: Session = Depends(get_db)):
    total = crud.contar_productos(db)
    productos = crud.obtener_productos(db, limit=total)

    if not productos:
        return {"total": 0, "precio_promedio": 0, "precio_max": 0, "precio_min": 0}

    precios = [p.precio for p in productos]
    return {
        "total": total,
        "precio_promedio": sum(precios) / len(precios),
        "precio_max": max(precios),
        "precio_min": min(precios)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 🧪 Paso 4: Probar las Nuevas Funcionalidades (5 min)

### Probar Paginación

```bash
# Primera página (10 productos)
curl "http://localhost:8000/productos/?skip=0&limit=10"

# Segunda página
curl "http://localhost:8000/productos/?skip=10&limit=10"
```

### Probar Búsqueda

```bash
# Buscar productos que contengan "laptop"
curl "http://localhost:8000/productos/buscar/?q=laptop"
```

### Probar Actualización Parcial

```bash
# Solo actualizar el precio
curl -X PATCH "http://localhost:8000/productos/1" \
     -H "Content-Type: application/json" \
     -d '{"precio": 1299.99}'

# Solo actualizar nombre y descripción
curl -X PATCH "http://localhost:8000/productos/1" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Laptop Gaming Pro", "descripcion": "Laptop para gaming profesional"}'
```

### Probar Estadísticas

```bash
# Ver resumen de productos
curl "http://localhost:8000/productos/stats/resumen"
```

---

## ✅ Verificación

### Nuevas Funcionalidades

- [ ] **Validaciones** - Los datos se validan antes de guardar
- [ ] **Paginación** - Puedes navegar por páginas de productos
- [ ] **Búsqueda** - Puedes buscar productos por texto
- [ ] **Actualización parcial** - Puedes actualizar solo algunos campos
- [ ] **Estadísticas** - Puedes ver resumen de datos
- [ ] **Manejo de errores** - Los errores se muestran claramente

### Estructura Final

```text
semana-04-practica/
├── main.py          # ✅ API mejorada con nuevas funciones
├── crud.py          # ✅ Funciones CRUD separadas
├── database.py      # ✅ Configuración (sin cambios)
├── models.py        # ✅ Modelo (sin cambios)
├── schemas.py       # ✅ Schemas con validaciones
├── requirements.txt # ✅ Dependencias (sin cambios)
└── productos.db     # ✅ Base de datos
```

---

## 🎯 Resumen

### Lo que Añadiste

- ✅ **Validaciones Pydantic** - Datos siempre correctos
- ✅ **Funciones CRUD separadas** - Código más organizado
- ✅ **Paginación** - Manejo de listas grandes
- ✅ **Búsqueda** - Filtrar productos por texto
- ✅ **Actualización parcial** - PATCH en lugar de PUT
- ✅ **Estadísticas básicas** - Insights de los datos

### Conceptos Aprendidos

1. **Validadores Pydantic** - `@validator` para validaciones custom
2. **Separación de responsabilidades** - CRUD en archivo separado
3. **Query Parameters** - Parámetros de consulta en FastAPI
4. **Operaciones SQL** - `contains()`, `count()`, paginación
5. **Manejo de errores** - `try/except` y `HTTPException`

### Próximo Paso

¡Tu API ahora es mucho más robusta! En la siguiente práctica aprenderemos sobre relaciones entre tablas.

---

## 🔗 Enlaces Útiles

- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [FastAPI Query Parameters](https://fastapi.tiangolo.com/tutorial/query-params/)
- [SQLAlchemy Querying](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#querying)
