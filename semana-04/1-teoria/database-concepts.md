# Teoría - Semana 4: Bases de Datos Básicas

## 📖 Introducción

En las semanas anteriores trabajamos con **datos en memoria** (listas de Python). El problema es que se **pierden al reiniciar** la aplicación. Esta semana aprenderemos a usar **bases de datos** para que los datos sean **permanentes**.

---

## 🎯 Objetivos de Aprendizaje

Al finalizar esta semana podrás:

- Entender por qué necesitamos bases de datos
- Configurar SQLite con FastAPI
- Crear modelos básicos con SQLAlchemy
- Realizar operaciones CRUD simples

---

## 💾 ¿Por qué Bases de Datos?

### Problema: Datos en Memoria

```python
# ❌ Se pierden al reiniciar
productos = [
    {"id": 1, "nombre": "Laptop", "precio": 999.99}
]

@app.post("/productos")
def crear_producto(producto: dict):
    productos.append(producto)  # ¡Se pierde!
    return producto
```

### Solución: Base de Datos

```python
# ✅ Los datos persisten
@app.post("/productos")
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()  # Guardado permanente
    return db_producto
```

---

## 📊 ¿Qué es SQLite?

**SQLite** es una base de datos **simple** y perfecta para aprender:

- ✅ **Un solo archivo** - No necesita servidor
- ✅ **Fácil configuración** - Cero setup
- ✅ **Ideal para desarrollo** - Sin complicaciones

```python
# Crear base de datos SQLite (un archivo)
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
```

---

## 🔧 ¿Qué es SQLAlchemy (ORM)?

**ORM** = Object-Relational Mapping. Nos permite trabajar con objetos Python en lugar de SQL directo.

### Sin ORM (Difícil)

```python
import sqlite3
cursor.execute("INSERT INTO productos (nombre, precio) VALUES (?, ?)", (nombre, precio))
```

### Con ORM (Fácil)

```python
producto = Producto(nombre="Laptop", precio=999.99)
db.add(producto)
db.commit()
```

---

## 📋 Tipos de Modelos

### 1. Modelo SQLAlchemy (Tabla)

```python
# models.py
from sqlalchemy import Column, Integer, String, Float

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    precio = Column(Float)
```

### 2. Modelo Pydantic (API)

```python
# schemas.py
class ProductoCreate(BaseModel):
    nombre: str
    precio: float

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: float
```

---

## 🔄 Operaciones CRUD Básicas

### Create (Crear)

```python
@app.post("/productos")
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    return db_producto
```

### Read (Leer)

```python
@app.get("/productos")
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()

@app.get("/productos/{id}")
def obtener_producto(id: int, db: Session = Depends(get_db)):
    return db.query(Producto).filter(Producto.id == id).first()
```

### Update (Actualizar)

```python
@app.put("/productos/{id}")
def actualizar_producto(id: int, producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == id).first()
    db_producto.nombre = producto.nombre
    db_producto.precio = producto.precio
    db.commit()
    return db_producto
```

### Delete (Eliminar)

```python
@app.delete("/productos/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    db_producto = db.query(Producto).filter(Producto.id == id).first()
    db.delete(db_producto)
    db.commit()
    return {"mensaje": "Producto eliminado"}
```

---

## 🔗 Configuración Básica

### 1. Conexión a la Base de Datos

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

### 2. Dependencia para la Sesión

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 📝 Ejemplo Completo Básico

```python
# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import models, schemas, database

app = FastAPI()

# Crear tablas
models.Base.metadata.create_all(bind=database.engine)

@app.post("/productos", response_model=schemas.ProductoResponse)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(database.get_db)):
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)  # Obtener el ID generado
    return db_producto

@app.get("/productos")
def listar_productos(db: Session = Depends(database.get_db)):
    return db.query(models.Producto).all()
```

---

## ✅ Resumen

### Conceptos Clave

1. **Persistencia** - Los datos se guardan permanentemente
2. **SQLite** - Base de datos simple en un archivo
3. **ORM** - Trabajar con objetos Python en lugar de SQL
4. **CRUD** - Create, Read, Update, Delete
5. **Sesiones** - Conexiones a la base de datos

### Lo que Aprendiste

- ✅ Por qué usar bases de datos
- ✅ Configurar SQLite con FastAPI
- ✅ Crear modelos básicos
- ✅ Operaciones CRUD simples

### Próximo Paso

En la práctica implementarás tu primera API con base de datos real.

---

## 📚 Referencias

- [FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [SQLAlchemy Core](https://docs.sqlalchemy.org/en/14/core/)
- [SQLite Documentación](https://www.sqlite.org/docs.html)
