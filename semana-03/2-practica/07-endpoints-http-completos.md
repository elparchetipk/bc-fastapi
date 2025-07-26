# Práctica 7: Endpoints HTTP Completos - Semana 3

## 🎯 Objetivo

Implementar un conjunto completo de endpoints HTTP (GET, POST, PUT, DELETE) para crear una API REST funcional que maneje productos de inventario.

## ⏱️ Tiempo Estimado: 90 minutos

## 📋 Pre-requisitos

- ✅ API básica de Semana 1 funcionando
- ✅ Modelos Pydantic de Semana 2 implementados
- ✅ Entorno FastAPI configurado
- ✅ Postman o herramienta similar para testing

## 🚀 Paso 1: Preparación del Proyecto (15 min)

### **Estructura del Proyecto**

Organiza tu proyecto con esta estructura:

```
semana-03-api/
├── main.py
├── models/
│   ├── __init__.py
│   └── product_models.py
├── data/
│   └── products_data.py
├── requirements.txt
└── README.md
```

### **Crear los Modelos Base**

`models/product_models.py`:

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class CategoryEnum(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    home = "home"
    sports = "sports"

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    price: float = Field(..., gt=0, le=999999.99, description="Precio del producto")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del producto")
    category: CategoryEnum = Field(..., description="Categoría del producto")

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('El nombre no puede estar vacío')
        return v.strip().title()

class ProductCreate(ProductBase):
    in_stock: bool = Field(True, description="Producto en stock")
    stock_quantity: int = Field(0, ge=0, le=9999, description="Cantidad en stock")

class ProductUpdate(ProductBase):
    in_stock: bool = Field(..., description="Producto en stock")
    stock_quantity: int = Field(..., ge=0, le=9999, description="Cantidad en stock")

class ProductResponse(ProductBase):
    id: int = Field(..., description="ID único del producto")
    in_stock: bool
    stock_quantity: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Laptop Gaming",
                "price": 1299.99,
                "description": "Laptop para gaming de alta performance",
                "category": "electronics",
                "in_stock": True,
                "stock_quantity": 15,
                "created_at": "2025-07-24T10:00:00",
                "updated_at": None
            }
        }

class ProductList(BaseModel):
    products: List[ProductResponse]
    total: int
    page: int
    page_size: int

class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: Optional[str] = None
```

### **Base de Datos Simulada**

`data/products_data.py`:

```python
from datetime import datetime
from typing import Dict, List, Optional
from models.product_models import ProductResponse, CategoryEnum

# Simulamos una base de datos en memoria
products_db: Dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Laptop Gaming",
        "price": 1299.99,
        "description": "Laptop para gaming de alta performance",
        "category": CategoryEnum.electronics,
        "in_stock": True,
        "stock_quantity": 15,
        "created_at": datetime(2025, 7, 20, 10, 0, 0),
        "updated_at": None
    },
    2: {
        "id": 2,
        "name": "Camiseta Algodón",
        "price": 29.99,
        "description": "Camiseta 100% algodón, muy cómoda",
        "category": CategoryEnum.clothing,
        "in_stock": True,
        "stock_quantity": 50,
        "created_at": datetime(2025, 7, 21, 14, 30, 0),
        "updated_at": None
    },
    3: {
        "id": 3,
        "name": "Python para Principiantes",
        "price": 45.00,
        "description": "Libro completo de programación en Python",
        "category": CategoryEnum.books,
        "in_stock": False,
        "stock_quantity": 0,
        "created_at": datetime(2025, 7, 22, 9, 15, 0),
        "updated_at": None
    }
}

# Counter para IDs autoincrementales
next_id = 4

def get_next_id() -> int:
    global next_id
    current_id = next_id
    next_id += 1
    return current_id

def get_all_products() -> List[dict]:
    return list(products_db.values())

def get_product_by_id(product_id: int) -> Optional[dict]:
    return products_db.get(product_id)

def create_product(product_data: dict) -> dict:
    product_id = get_next_id()
    new_product = {
        "id": product_id,
        **product_data,
        "created_at": datetime.now(),
        "updated_at": None
    }
    products_db[product_id] = new_product
    return new_product

def update_product(product_id: int, product_data: dict) -> Optional[dict]:
    if product_id in products_db:
        updated_product = {
            **products_db[product_id],
            **product_data,
            "updated_at": datetime.now()
        }
        products_db[product_id] = updated_product
        return updated_product
    return None

def delete_product(product_id: int) -> bool:
    if product_id in products_db:
        del products_db[product_id]
        return True
    return False

def filter_products(
    category: Optional[str] = None,
    in_stock: Optional[bool] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> List[dict]:
    products = get_all_products()

    if category:
        products = [p for p in products if p["category"] == category]

    if in_stock is not None:
        products = [p for p in products if p["in_stock"] == in_stock]

    if min_price is not None:
        products = [p for p in products if p["price"] >= min_price]

    if max_price is not None:
        products = [p for p in products if p["price"] <= max_price]

    return products
```

## 🔧 Paso 2: Endpoints GET (25 min)

### **GET - Listar Todos los Productos**

`main.py`:

```python
from fastapi import FastAPI, HTTPException, Query, Path, status
from fastapi.responses import JSONResponse
from typing import Optional, List
from models.product_models import (
    ProductCreate, ProductUpdate, ProductResponse,
    ProductList, CategoryEnum, ErrorResponse
)
from data.products_data import (
    get_all_products, get_product_by_id, create_product,
    update_product, delete_product, filter_products
)

app = FastAPI(
    title="API de Inventario - Semana 3",
    description="API REST completa para manejo de productos",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/", summary="Endpoint de bienvenida")
async def root():
    """Endpoint básico de bienvenida"""
    return {
        "message": "API de Inventario - Semana 3",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get(
    "/products",
    response_model=ProductList,
    summary="Obtener lista de productos",
    description="Obtiene una lista paginada de productos con filtros opcionales"
)
async def get_products(
    # Filtros opcionales
    category: Optional[CategoryEnum] = Query(None, description="Filtrar por categoría"),
    in_stock: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),

    # Paginación
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Productos por página"),

    # Búsqueda
    search: Optional[str] = Query(None, min_length=1, description="Buscar en nombre y descripción")
):
    try:
        # Obtener productos filtrados
        products = filter_products(
            category=category.value if category else None,
            in_stock=in_stock,
            min_price=min_price,
            max_price=max_price
        )

        # Búsqueda por texto
        if search:
            search_lower = search.lower()
            products = [
                p for p in products
                if search_lower in p["name"].lower() or
                   (p["description"] and search_lower in p["description"].lower())
            ]

        # Calcular paginación
        total = len(products)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_products = products[start_index:end_index]

        return ProductList(
            products=paginated_products,
            total=total,
            page=page,
            page_size=page_size
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@app.get(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Obtener producto por ID",
    description="Obtiene un producto específico por su ID",
    responses={
        200: {"description": "Producto encontrado"},
        404: {"description": "Producto no encontrado"},
        400: {"description": "ID inválido"}
    }
)
async def get_product(
    product_id: int = Path(..., gt=0, description="ID del producto a obtener")
):
    # Buscar producto
    product = get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado"
        )

    return ProductResponse(**product)
```

### **Testing de Endpoints GET**

Prueba los endpoints con estos comandos:

```bash
# Obtener todos los productos
curl -X GET "http://localhost:8000/products"

# Con filtros
curl -X GET "http://localhost:8000/products?category=electronics&in_stock=true"

# Con paginación
curl -X GET "http://localhost:8000/products?page=1&page_size=5"

# Obtener producto específico
curl -X GET "http://localhost:8000/products/1"

# Producto que no existe
curl -X GET "http://localhost:8000/products/999"
```

## 📝 Paso 3: Endpoint POST (20 min)

```python
@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo producto",
    description="Crea un nuevo producto en el inventario"
)
async def create_new_product(product: ProductCreate):
    try:
        # Validar que no existe producto con el mismo nombre
        existing_products = get_all_products()
        for existing in existing_products:
            if existing["name"].lower() == product.name.lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un producto con el nombre '{product.name}'"
                )

        # Crear producto
        product_data = product.dict()
        new_product = create_product(product_data)

        return ProductResponse(**new_product)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}"
        )
```

### **Testing del POST**

```bash
# Crear producto válido
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mouse Gaming",
    "price": 79.99,
    "description": "Mouse gaming RGB con alta precisión",
    "category": "electronics",
    "in_stock": true,
    "stock_quantity": 25
  }'

# Crear producto duplicado (debe fallar)
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mouse Gaming",
    "price": 89.99,
    "description": "Otro mouse gaming",
    "category": "electronics",
    "in_stock": true,
    "stock_quantity": 10
  }'
```

## 🔄 Paso 4: Endpoint PUT (20 min)

```python
@app.put(
    "/products/{product_id}",
    response_model=ProductResponse,
    summary="Actualizar producto completo",
    description="Actualiza completamente un producto existente"
)
async def update_existing_product(
    product_id: int = Path(..., gt=0, description="ID del producto a actualizar"),
    product: ProductUpdate
):
    try:
        # Verificar que el producto existe
        existing_product = get_product_by_id(product_id)
        if not existing_product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {product_id} no encontrado"
            )

        # Validar que no hay conflicto de nombres (excepto consigo mismo)
        all_products = get_all_products()
        for existing in all_products:
            if (existing["id"] != product_id and
                existing["name"].lower() == product.name.lower()):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe otro producto con el nombre '{product.name}'"
                )

        # Actualizar producto
        product_data = product.dict()
        updated_product = update_product(product_id, product_data)

        return ProductResponse(**updated_product)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar producto: {str(e)}"
        )
```

### **Testing del PUT**

```bash
# Actualizar producto existente
curl -X PUT "http://localhost:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Gaming Pro",
    "price": 1599.99,
    "description": "Laptop gaming de última generación",
    "category": "electronics",
    "in_stock": true,
    "stock_quantity": 8
  }'

# Intentar actualizar producto que no existe
curl -X PUT "http://localhost:8000/products/999" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Producto Inexistente",
    "price": 99.99,
    "description": "Este producto no debería actualizarse",
    "category": "electronics",
    "in_stock": true,
    "stock_quantity": 1
  }'
```

## 🗑️ Paso 5: Endpoint DELETE (10 min)

```python
@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar producto",
    description="Elimina un producto del inventario",
    responses={
        204: {"description": "Producto eliminado exitosamente"},
        404: {"description": "Producto no encontrado"}
    }
)
async def delete_existing_product(
    product_id: int = Path(..., gt=0, description="ID del producto a eliminar")
):
    # Verificar que el producto existe
    existing_product = get_product_by_id(product_id)
    if not existing_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con ID {product_id} no encontrado"
        )

    # Eliminar producto
    deleted = delete_product(product_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar el producto"
        )

    # Return 204 No Content (sin body)
    return None
```

### **Testing del DELETE**

```bash
# Eliminar producto existente
curl -X DELETE "http://localhost:8000/products/3"

# Verificar que se eliminó
curl -X GET "http://localhost:8000/products/3"

# Intentar eliminar producto que no existe
curl -X DELETE "http://localhost:8000/products/999"
```

## 🧪 Paso 6: Testing Completo y Documentación (15 min)

### **Ejecutar la API**

```bash
# Instalar dependencias
pip install fastapi uvicorn

# Ejecutar servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Verificar Documentación Automática**

1. **Swagger UI**: http://localhost:8000/docs
2. **ReDoc**: http://localhost:8000/redoc

### **Secuencia de Testing Completa**

```bash
# 1. Listar productos iniciales
curl -X GET "http://localhost:8000/products"

# 2. Crear nuevo producto
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tablet Android",
    "price": 299.99,
    "description": "Tablet con pantalla HD de 10 pulgadas",
    "category": "electronics",
    "in_stock": true,
    "stock_quantity": 12
  }'

# 3. Obtener el producto creado (asume que el ID es 4)
curl -X GET "http://localhost:8000/products/4"

# 4. Actualizar el producto
curl -X PUT "http://localhost:8000/products/4" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Tablet Android Pro",
    "price": 399.99,
    "description": "Tablet premium con pantalla OLED",
    "category": "electronics",
    "in_stock": true,
    "stock_quantity": 8
  }'

# 5. Listar productos con filtros
curl -X GET "http://localhost:8000/products?category=electronics&min_price=200"

# 6. Eliminar producto
curl -X DELETE "http://localhost:8000/products/4"

# 7. Verificar eliminación
curl -X GET "http://localhost:8000/products/4"
```

## ✅ Entregables

Al finalizar esta práctica deberías tener:

1. ✅ **API funcionando** con 5 endpoints completos
2. ✅ **CRUD completo** para productos
3. ✅ **Validación robusta** en todos los endpoints
4. ✅ **Manejo de errores** apropiado
5. ✅ **Documentación automática** funcional
6. ✅ **Código organizado** en módulos

## 🎯 Próximo Paso

En la siguiente práctica (08-validacion-avanzada.md) expandiremos estos endpoints con validación más sofisticada y manejo de parámetros avanzados.

---

_Práctica desarrollada para Semana 3 - Bootcamp FastAPI_  
_Tiempo estimado: 90 minutos_
