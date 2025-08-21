# Práctica 10: Estructura Básica del Proyecto

## 🎯 Objetivo Básico

Organizar tu código FastAPI en una **estructura simple y profesional** en 90 minutos (Bloque final), enfocándose solo en lo esencial para un proyecto limpio.

## ⏱️ Tiempo: 90 minutos (Bloque final)

## 📋 Pre-requisitos

- ✅ Manejo de errores funcionando (Práctica 9 completada)
- ✅ Todas las prácticas de la Semana 2 completadas
- ✅ Conocimiento básico de organización de archivos
- ✅ Energía para el último empujón del bootcamp

## 🚀 Desarrollo Rápido (Solo 3 pasos)

### Paso 1: Estructura Simple del Proyecto (30 min)

**Problema**: Tu código está todo en un archivo `main.py` y es difícil de mantener.

**Solución**: Separar en archivos organizados pero simples.

```bash
# Crear estructura básica
mkdir mi-api-organizada
cd mi-api-organizada

# Crear carpetas principales
mkdir models
mkdir routers
mkdir services

# Crear archivos básicos
touch main.py
touch models/__init__.py
touch models/product.py
touch routers/__init__.py
touch routers/products.py
touch services/__init__.py
touch services/product_service.py
```

**Estructura final simple:**

```
mi-api-organizada/
├── main.py                 # Archivo principal
├── models/
│   ├── __init__.py
│   └── product.py          # Modelos Pydantic
├── routers/
│   ├── __init__.py
│   └── products.py         # Endpoints de productos
└── services/
    ├── __init__.py
    └── product_service.py  # Lógica de negocio
```

**1. Crear modelos organizados** (`models/product.py`):

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0, le=1000000)
    stock: int = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)

    @validator('name')
    def validate_name(cls, v):
        if v.strip() != v:
            raise ValueError('El nombre no puede empezar o terminar con espacios')
        return v.title()

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    price: Optional[float] = Field(None, gt=0, le=1000000)
    stock: Optional[int] = Field(None, ge=0)

class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
```

**2. Crear servicio de lógica** (`services/product_service.py`):

```python
from typing import List, Optional
from datetime import datetime
from models.product import ProductCreate, ProductUpdate, ProductResponse

# Base de datos simulada (en memoria)
products_db = [
    {
        "id": 1,
        "name": "Laptop Gaming",
        "price": 1500.0,
        "stock": 10,
        "description": "Laptop para gaming de alta gama",
        "created_at": datetime.now()
    },
    {
        "id": 2,
        "name": "Mouse Inalámbrico",
        "price": 45.0,
        "stock": 50,
        "description": "Mouse ergonómico inalámbrico",
        "created_at": datetime.now()
    }
]

class ProductService:

    @staticmethod
    def get_all_products() -> List[dict]:
        return products_db

    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[dict]:
        for product in products_db:
            if product["id"] == product_id:
                return product
        return None

    @staticmethod
    def create_product(product_data: ProductCreate) -> dict:
        # Verificar nombre único
        for existing in products_db:
            if existing["name"].lower() == product_data.name.lower():
                raise ValueError(f"Ya existe un producto con el nombre '{product_data.name}'")

        # Crear nuevo producto
        new_id = max([p["id"] for p in products_db]) + 1 if products_db else 1
        new_product = {
            "id": new_id,
            "name": product_data.name,
            "price": product_data.price,
            "stock": product_data.stock,
            "description": product_data.description,
            "created_at": datetime.now()
        }

        products_db.append(new_product)
        return new_product

    @staticmethod
    def update_product(product_id: int, product_data: ProductUpdate) -> Optional[dict]:
        for i, product in enumerate(products_db):
            if product["id"] == product_id:
                # Actualizar solo campos proporcionados
                if product_data.name is not None:
                    product["name"] = product_data.name
                if product_data.price is not None:
                    product["price"] = product_data.price
                if product_data.stock is not None:
                    product["stock"] = product_data.stock
                if product_data.description is not None:
                    product["description"] = product_data.description

                products_db[i] = product
                return product
        return None

    @staticmethod
    def delete_product(product_id: int) -> bool:
        for i, product in enumerate(products_db):
            if product["id"] == product_id:
                products_db.pop(i)
                return True
        return False
```

---

### Paso 2: Archivo Principal Organizado (30 min)

**Problema**: El `main.py` debe conectar todos los componentes.

**Solución**: Crear un archivo principal simple pero completo.

**1. Archivo principal** (`main.py`):

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.products import router as products_router

# Crear aplicación FastAPI
app = FastAPI(
    title="Mi API Organizada",
    description="API de productos con estructura profesional",
    version="1.0.0"
)

# Configurar CORS básico
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(products_router, prefix="/api/v1")

# Endpoint de salud
@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
```

**2. Testing básico**:

```bash
# Ejecutar la API
python main.py

# Probar endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/products/

# Crear producto
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Producto Nuevo", "price": 99.99, "stock": 5}'
```

---

### Paso 3: Mejoras y Testing (30 min)

**Problema**: Necesitas validar que todo funcione correctamente.

**Solución**: Probar la API y hacer ajustes finales.

**1. Testing completo de la estructura:**

```bash
# Verificar que todos los archivos existen
ls -la mi-api-organizada/
ls -la mi-api-organizada/models/
ls -la mi-api-organizada/routers/
ls -la mi-api-organizada/services/

# Ejecutar la API
cd mi-api-organizada
python main.py
```

**2. Probar todos los endpoints:**

```bash
# Health check
curl http://localhost:8000/health

# Obtener productos
curl http://localhost:8000/api/v1/products/

# Crear producto
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smartphone",
    "price": 699.99,
    "stock": 15,
    "description": "Smartphone moderno"
  }'

# Obtener producto específico
curl http://localhost:8000/api/v1/products/1

# Actualizar producto
curl -X PUT http://localhost:8000/api/v1/products/1 \
  -H "Content-Type: application/json" \
  -d '{"price": 1299.99, "stock": 8}'

# Eliminar producto
curl -X DELETE http://localhost:8000/api/v1/products/1
```

**3. Verificar documentación automática:**

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 💻 Ejemplos Prácticos

### **Estructura Final:**

```
mi-api-organizada/
├── main.py                    # 🚀 Aplicación principal
├── models/
│   ├── __init__.py
│   └── product.py            # 📦 Modelos Pydantic
├── routers/
│   ├── __init__.py
│   └── products.py           # 🛣️ Endpoints REST
└── services/
    ├── __init__.py
    └── product_service.py     # 🔧 Lógica de negocio
```

### **¿Qué lograste?**

✅ **Separación de responsabilidades**: Cada archivo tiene una función específica  
✅ **Código organizado**: Fácil de mantener y escalar  
✅ **Estructura profesional**: Siguiendo mejores prácticas  
✅ **API funcional**: Con todos los endpoints CRUD  
✅ **Documentación automática**: Swagger y ReDoc incluidos

## ✅ Entregables

Al finalizar esta práctica deberías tener:

1. ✅ **Estructura de proyecto profesional** completamente organizada
2. ✅ **Separación clara de responsabilidades** entre modelos, servicios y routers
3. ✅ **API funcional** con todos los endpoints CRUD
4. ✅ **Código mantenible** y fácil de escalar
5. ✅ **Documentación automática** con Swagger UI

### **Comandos de Testing Final**

```bash
# Ejecutar la API estructurada
cd mi-api-organizada
python main.py

# Testing de endpoints
curl -X GET "http://localhost:8000/health"
curl -X GET "http://localhost:8000/api/v1/products/"

# Documentación automática
# http://localhost:8000/docs
# http://localhost:8000/redoc
```

---

_Práctica desarrollada para Semana 3 - Bootcamp FastAPI_  
_Tiempo estimado: 90 minutos_
