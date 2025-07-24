# Práctica 11: SQLAlchemy + FastAPI Setup - Semana 4

## 🎯 Objetivo

Configurar SQLAlchemy con FastAPI para crear una base sólida de persistencia de datos, estableciendo la conexión a base de datos, modelos básicos y la estructura fundamental para las próximas prácticas.

## ⏱️ Tiempo Estimado: 90 minutos

## 📋 Pre-requisitos

- ✅ **Semana 3 completada** - APIs REST con validación
- ✅ **FastAPI funcionando** - Entorno de desarrollo configurado
- ✅ **Python 3.8+** instalado
- ✅ **Git** configurado para el proyecto

## 🚀 Paso 1: Preparación del Proyecto (15 min)

### **Estructura del Proyecto**

Crea la siguiente estructura para tu proyecto de base de datos:

```
semana-04-database/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app principal
│   ├── database.py             # Configuración SQLAlchemy
│   ├── models/
│   │   ├── __init__.py
│   │   └── product.py          # Modelos SQLAlchemy
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── product.py          # Modelos Pydantic
│   └── crud/
│       ├── __init__.py
│       └── product.py          # Operaciones CRUD
├── tests/
│   ├── __init__.py
│   └── test_products.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### **Crear las Carpetas**

```bash
# Crear estructura de proyecto
mkdir -p semana-04-database/app/{models,schemas,crud}
mkdir -p semana-04-database/tests
cd semana-04-database

# Crear archivos __init__.py
touch app/__init__.py
touch app/models/__init__.py
touch app/schemas/__init__.py
touch app/crud/__init__.py
touch tests/__init__.py
```

## 🔧 Paso 2: Instalación de Dependencias (10 min)

### **requirements.txt**

```text
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
python-dotenv==1.0.0
alembic==1.13.0
pytest==7.4.0
pytest-asyncio==0.21.0
httpx==0.25.0
```

### **Instalar dependencias**

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
# venv\\Scripts\\activate

# Instalar dependencias
pip install -r requirements.txt
```

### **.env.example**

```env
# Configuración de Base de Datos
DATABASE_URL=sqlite:///./ecommerce.db
SECRET_KEY=your-secret-key-here
DEBUG=True

# Testing
TEST_DATABASE_URL=sqlite:///./test.db
```

### **.gitignore**

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Bases de datos
*.db
*.sqlite

# Entorno
.env

# Testing
.pytest_cache/
.coverage

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
```

## 🗄️ Paso 3: Configuración de Base de Datos (20 min)

### **app/database.py**

```python
"""
Configuración de SQLAlchemy para FastAPI
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# URL de base de datos desde variables de entorno
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")

# Crear engine de SQLAlchemy
# check_same_thread=False es necesario solo para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

# Crear SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear Base class para modelos
Base = declarative_base()

# Dependency para obtener sesión de BD
def get_db():
    """
    Dependency que proporciona sesión de base de datos.
    Se cierra automáticamente al terminar la request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### **Crear archivo .env**

```bash
# Copiar ejemplo y personalizar
cp .env.example .env

# Editar con tus configuraciones
nano .env  # o tu editor preferido
```

## 📋 Paso 4: Primer Modelo SQLAlchemy (20 min)

### **app/models/product.py**

```python
"""
Modelos SQLAlchemy para productos
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    """
    Modelo SQLAlchemy para tabla de productos
    """
    __tablename__ = "products"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)

    # Timestamps automáticos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
```

### **app/models/**init**.py**

```python
"""
Importar todos los modelos para que SQLAlchemy los encuentre
"""
from .product import Product

# Lista de todos los modelos (útil para migraciones)
__all__ = ["Product"]
```

## 📨 Paso 5: Modelos Pydantic (15 min)

### **app/schemas/product.py**

```python
"""
Esquemas Pydantic para validación de API
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    """Campos base compartidos entre schemas"""
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del producto")
    price: float = Field(..., gt=0, description="Precio debe ser mayor a 0")
    stock: int = Field(0, ge=0, description="Stock no puede ser negativo")
    is_active: bool = Field(True, description="Si el producto está activo")

class ProductCreate(ProductBase):
    """Schema para crear producto (request)"""
    pass

class ProductUpdate(BaseModel):
    """Schema para actualizar producto (request)"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None

class Product(ProductBase):
    """Schema para respuesta de API"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        # Permite trabajar con objetos SQLAlchemy
        from_attributes = True  # Pydantic v2
        # orm_mode = True  # Pydantic v1 (comentado)

# Schemas para respuestas con listas
class ProductList(BaseModel):
    """Schema para lista paginada de productos"""
    items: list[Product]
    total: int
    page: int
    per_page: int
    pages: int
```

### **app/schemas/**init**.py**

```python
"""
Importar todos los schemas
"""
from .product import Product, ProductCreate, ProductUpdate, ProductList

__all__ = ["Product", "ProductCreate", "ProductUpdate", "ProductList"]
```

## ⚙️ Paso 6: Operaciones CRUD Básicas (15 min)

### **app/crud/product.py**

```python
"""
Operaciones CRUD para productos
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def get_product(db: Session, product_id: int) -> Optional[Product]:
    """Obtener producto por ID"""
    return db.query(Product).filter(Product.id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    """Obtener lista de productos con paginación"""
    return db.query(Product).offset(skip).limit(limit).all()

def get_products_count(db: Session) -> int:
    """Obtener total de productos"""
    return db.query(Product).count()

def create_product(db: Session, product: ProductCreate) -> Product:
    """Crear nuevo producto"""
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
    """Actualizar producto existente"""
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        db.commit()
        db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int) -> bool:
    """Eliminar producto"""
    db_product = get_product(db, product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
        return True
    return False
```

### **app/crud/**init**.py**

```python
"""
Importar todas las operaciones CRUD
"""
from . import product

__all__ = ["product"]
```

## 🚀 Paso 7: FastAPI Application (10 min)

### **app/main.py**

```python
"""
FastAPI application principal
"""
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Importar configuración y dependencias
from app.database import SessionLocal, engine, get_db, Base
from app.models import Product  # Importar para crear tablas
from app.schemas.product import Product as ProductSchema, ProductCreate, ProductUpdate
from app.crud import product as crud_product

# Crear tablas en base de datos
Base.metadata.create_all(bind=engine)

# Crear instancia de FastAPI
app = FastAPI(
    title="E-commerce API",
    description="API para manejo de productos con SQLAlchemy",
    version="1.0.0"
)

@app.get("/")
def read_root():
    """Endpoint raíz"""
    return {"message": "E-commerce API with Database", "version": "1.0.0"}

@app.get("/products", response_model=List[ProductSchema])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de productos"""
    products = crud_product.get_products(db, skip=skip, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=ProductSchema)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Obtener producto específico"""
    db_product = crud_product.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return db_product

@app.post("/products", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Crear nuevo producto"""
    return crud_product.create_product(db=db, product=product)

@app.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    """Actualizar producto existente"""
    db_product = crud_product.update_product(db, product_id, product_update)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return db_product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Eliminar producto"""
    success = crud_product.delete_product(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

# Health check endpoint
@app.get("/health")
def health_check():
    """Verificar estado de la aplicación"""
    return {"status": "healthy", "database": "connected"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🧪 Paso 8: Testing Básico (5 min)

### **tests/test_products.py**

```python
"""
Tests básicos para endpoints de productos
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base

# Base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_product(client):
    """Test crear producto"""
    response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "description": "A test product",
            "price": 99.99,
            "stock": 10
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 99.99

def test_get_products(client):
    """Test obtener lista de productos"""
    response = client.get("/products")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_health_check(client):
    """Test health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

## ✅ Paso 9: Ejecutar y Verificar (5 min)

### **Ejecutar la aplicación**

```bash
# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload

# En otra terminal, verificar endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
```

### **Ejecutar tests**

```bash
# Ejecutar tests
pytest tests/ -v

# Si todo está bien, deberías ver:
# test_create_product PASSED
# test_get_products PASSED
# test_health_check PASSED
```

### **Probar con datos**

```bash
# Crear un producto de prueba
curl -X POST "http://localhost:8000/products" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Laptop Gaming",
       "description": "Laptop para gaming de alta gama",
       "price": 1299.99,
       "stock": 5
     }'

# Obtener todos los productos
curl http://localhost:8000/products

# Obtener producto específico
curl http://localhost:8000/products/1
```

## 📋 Verificación de Completitud

### **✅ Checklist de Finalización**

- [ ] ✅ **Estructura de proyecto** creada correctamente
- [ ] ✅ **Dependencias instaladas** sin errores
- [ ] ✅ **Base de datos configurada** (SQLAlchemy + SQLite)
- [ ] ✅ **Modelo SQLAlchemy** funcionando (Product)
- [ ] ✅ **Schemas Pydantic** validando correctamente
- [ ] ✅ **CRUD operations** implementadas
- [ ] ✅ **FastAPI app** ejecutándose sin errores
- [ ] ✅ **Endpoints responden** correctamente
- [ ] ✅ **Tests básicos** pasando
- [ ] ✅ **Base de datos persiste** datos entre reinicios

### **🔧 Verificación Manual**

1. **Crear producto** vía POST
2. **Consultar productos** vía GET
3. **Reiniciar aplicación**
4. **Verificar que datos persisten**
5. **Ejecutar tests** exitosamente

## 🎯 Resultado Esperado

Al finalizar esta práctica tendrás:

- ✅ **Setup completo** de SQLAlchemy con FastAPI
- ✅ **Primer modelo** funcionando con persistencia
- ✅ **CRUD básico** implementado
- ✅ **Testing configurado** para futuras prácticas
- ✅ **Base sólida** para las próximas 3 prácticas

### **Archivos creados:**

- `app/database.py` - Configuración SQLAlchemy
- `app/models/product.py` - Modelo de productos
- `app/schemas/product.py` - Validación Pydantic
- `app/crud/product.py` - Operaciones CRUD
- `app/main.py` - FastAPI application
- `tests/test_products.py` - Tests básicos

## 🚀 Próximos Pasos

Esta práctica establece las bases para:

- **Práctica 12**: CRUD completo con validaciones avanzadas
- **Práctica 13**: Relaciones entre tablas (Foreign Keys)
- **Práctica 14**: Migraciones con Alembic y testing avanzado

## 🆘 Troubleshooting

### **Error: "No module named 'app'"**

```bash
# Asegúrate de ejecutar desde el directorio raíz
cd semana-04-database
python -m uvicorn app.main:app --reload
```

### **Error: "database is locked"**

```bash
# Cerrar todas las conexiones y reiniciar
pkill -f uvicorn
rm ecommerce.db
uvicorn app.main:app --reload
```

### **Error: "Table doesn't exist"**

```python
# Verificar que Base.metadata.create_all() se ejecute
# En app/main.py, línea después de imports
```

### **Error en tests: "fixture not found"**

```bash
# Instalar pytest si no está
pip install pytest pytest-asyncio httpx
```

---

**🎉 ¡Felicitaciones!** Has configurado exitosamente SQLAlchemy con FastAPI. Ahora tienes una base sólida para desarrollar APIs con persistencia real.
