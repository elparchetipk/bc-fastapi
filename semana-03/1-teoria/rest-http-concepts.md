# Week 3 Theory: REST and HTTP Fundamentals

## What is REST?

REST (Representational State Transfer) is a way to design web APIs that are easy to understand and use.

### Key REST Principles

1. **Consistent URLs** - Similar resources use similar URL patterns
2. **HTTP Methods** - Use the right method for each action
3. **Status Codes** - Return meaningful response codes

## HTTP Methods

### GET - Read Data

```python
@app.get("/users")        # Get all users
@app.get("/users/{id}")   # Get specific user
```

### POST - Create Data

```python
@app.post("/users")       # Create new user
```

### PUT - Update Data

```python
@app.put("/users/{id}")   # Update existing user
```

### DELETE - Remove Data

```python
@app.delete("/users/{id}") # Delete user
```

## HTTP Status Codes

### Success Codes

- `200 OK` - Request successful
- `201 Created` - New resource created
- `204 No Content` - Successful deletion

### Error Codes

- `400 Bad Request` - Invalid data sent
- `404 Not Found` - Resource doesn't exist
- `500 Internal Server Error` - Server problem

## Error Handling in FastAPI

```python
from fastapi import HTTPException

@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return users[user_id]
```

## Best Practices

1. **Use clear URL patterns**: `/users/{id}` not `/getUserById`
2. **Return appropriate status codes**: 404 for not found, 400 for bad data
3. **Handle errors gracefully**: Always return meaningful error messages
4. **Keep it simple**: Don't overcomplicate your API design
   @app.get("/products/{product_id}")
   async def get_product(product_id: int):
   return {"product": {...}}

# ✅ Búsqueda con parámetros

@app.get("/products")
async def search_products(
category: str = None,
min_price: float = None,
max_price: float = None
):
return {"products": [...]}

````

**Características importantes:**

- ✅ **Idempotente**: Múltiples calls = mismo resultado
- ✅ **Safe**: No modifica datos
- ✅ **Cacheable**: Puede ser cacheado

#### **POST - Crear Recursos**

**Propósito**: Crear nuevos recursos

```python
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    description: str

@app.post("/products", status_code=201)
async def create_product(product: ProductCreate):
    # Crear nuevo producto
    new_product = {
        "id": 123,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "created_at": "2025-07-24T10:00:00"
    }
    return new_product
````

**Características importantes:**

- ❌ **No idempotente**: Múltiples calls = múltiples recursos
- ❌ **No safe**: Modifica el estado
- ✅ **Status code 201**: Para creación exitosa

#### **PUT - Actualizar/Reemplazar Recursos**

**Propósito**: Reemplazar completamente un recurso existente

```python
class ProductUpdate(BaseModel):
    name: str
    price: float
    description: str
    in_stock: bool

@app.put("/products/{product_id}")
async def update_product(product_id: int, product: ProductUpdate):
    # Verificar que existe
    if not product_exists(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    # Reemplazar completamente
    updated_product = {
        "id": product_id,
        **product.dict(),
        "updated_at": "2025-07-24T10:30:00"
    }
    return updated_product
```

**Características importantes:**

- ✅ **Idempotente**: Múltiples calls = mismo resultado
- ❌ **No safe**: Modifica datos
- 🔄 **Reemplazo completo**: Todos los campos se actualizan

#### **PATCH - Actualización Parcial**

**Propósito**: Actualizar parcialmente un recurso

```python
from typing import Optional

class ProductPatch(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    in_stock: Optional[bool] = None

@app.patch("/products/{product_id}")
async def patch_product(product_id: int, product: ProductPatch):
    # Solo actualizar campos proporcionados
    existing_product = get_product(product_id)
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Actualización parcial
    for field, value in product.dict(exclude_unset=True).items():
        setattr(existing_product, field, value)

    return existing_product
```

#### **DELETE - Eliminar Recursos**

**Propósito**: Eliminar un recurso específico

```python
@app.delete("/products/{product_id}", status_code=204)
async def delete_product(product_id: int):
    if not product_exists(product_id):
        raise HTTPException(status_code=404, detail="Product not found")

    # Eliminar producto
    delete_product_from_db(product_id)

    # 204 No Content = eliminación exitosa sin body
    return None
```

**Características importantes:**

- ✅ **Idempotente**: Eliminar algo ya eliminado = mismo resultado
- ❌ **No safe**: Modifica estado
- ✅ **Status code 204**: Sin contenido tras eliminación exitosa

---

### 3. Status Codes HTTP Esenciales

#### **2xx - Éxito**

```python
from fastapi import status

# 200 OK - Operación exitosa con contenido
@app.get("/products/{id}", status_code=200)

# 201 Created - Recurso creado exitosamente
@app.post("/products", status_code=201)

# 204 No Content - Operación exitosa sin contenido
@app.delete("/products/{id}", status_code=204)
```

#### **4xx - Errores del Cliente**

```python
from fastapi import HTTPException

# 400 Bad Request - Datos inválidos
if not valid_data:
    raise HTTPException(status_code=400, detail="Invalid input data")

# 401 Unauthorized - No autenticado
raise HTTPException(status_code=401, detail="Authentication required")

# 403 Forbidden - No autorizado
raise HTTPException(status_code=403, detail="Access denied")

# 404 Not Found - Recurso no existe
raise HTTPException(status_code=404, detail="Product not found")

# 409 Conflict - Conflicto en el estado
raise HTTPException(status_code=409, detail="Product already exists")

# 422 Unprocessable Entity - Validación falló
# FastAPI lo maneja automáticamente con Pydantic
```

#### **5xx - Errores del Servidor**

```python
# 500 Internal Server Error - Error interno
try:
    process_data()
except Exception as e:
    raise HTTPException(status_code=500, detail="Internal server error")

# 503 Service Unavailable - Servicio no disponible
if not service_available():
    raise HTTPException(status_code=503, detail="Service temporarily unavailable")
```

---

### 4. Tipos de Parámetros en FastAPI

#### **Path Parameters - Parámetros de Ruta**

```python
from fastapi import Path

@app.get("/products/{product_id}")
async def get_product(
    product_id: int = Path(..., gt=0, description="ID del producto")
):
    return {"product_id": product_id}

# Con validación avanzada
@app.get("/users/{user_id}/products/{product_id}")
async def get_user_product(
    user_id: int = Path(..., gt=0, le=999999),
    product_id: int = Path(..., gt=0, le=999999)
):
    return {"user_id": user_id, "product_id": product_id}
```

#### **Query Parameters - Parámetros de Consulta**

```python
from fastapi import Query
from typing import Optional, List

@app.get("/products")
async def search_products(
    # Parámetro obligatorio
    category: str = Query(..., min_length=1, max_length=50),

    # Parámetros opcionales
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),

    # Parámetro con valor por defecto
    in_stock: bool = Query(True),

    # Lista de valores
    tags: Optional[List[str]] = Query(None),

    # Paginación
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    return {
        "category": category,
        "filters": {
            "min_price": min_price,
            "max_price": max_price,
            "in_stock": in_stock,
            "tags": tags
        },
        "pagination": {
            "page": page,
            "page_size": page_size
        }
    }
```

#### **Request Body - Cuerpo de la Petición**

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, le=999999.99)
    description: Optional[str] = Field(None, max_length=1000)
    category: str = Field(..., min_length=1, max_length=50)

class ProductCreate(ProductBase):
    in_stock: bool = Field(True)

class ProductUpdate(ProductBase):
    in_stock: bool

@app.post("/products")
async def create_product(product: ProductCreate):
    return {"created": product.dict()}

# Múltiples parámetros combinados
@app.put("/users/{user_id}/products/{product_id}")
async def update_user_product(
    user_id: int = Path(..., gt=0),
    product_id: int = Path(..., gt=0),
    product: ProductUpdate,
    notify_user: bool = Query(False)
):
    return {
        "user_id": user_id,
        "product_id": product_id,
        "product": product.dict(),
        "notify_user": notify_user
    }
```

---

### 5. Mejores Prácticas para APIs REST

#### **Naming Conventions**

```python
# ✅ Usar sustantivos, no verbos
GET /products        # No: GET /getProducts
POST /products       # No: POST /createProduct
DELETE /products/123 # No: DELETE /deleteProduct/123

# ✅ Usar plurales para colecciones
GET /products        # Todos los productos
GET /products/123    # Un producto específico

# ✅ Jerarquías claras
GET /users/123/orders/456/items  # Items del order 456 del user 123
```

#### **Consistencia en Responses**

```python
# ✅ Estructura consistente
{
    "success": true,
    "data": {...},
    "message": "Operation completed successfully"
}

# ✅ Errores consistentes
{
    "success": false,
    "error": {
        "code": "PRODUCT_NOT_FOUND",
        "message": "Product with ID 123 not found",
        "details": {...}
    }
}
```

#### **Versionado**

```python
# ✅ Versión en URL
@app.get("/api/v1/products")
@app.get("/api/v2/products")

# ✅ O en headers
@app.get("/api/products")
async def get_products(
    request: Request,
    version: str = Header("1.0")
):
    if version == "2.0":
        return new_format_response()
    return legacy_format_response()
```

---

### 6. Validación y Manejo de Errores

#### **Validación con Pydantic**

```python
from pydantic import BaseModel, validator, Field
from typing import Optional
import re

class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, le=999999.99)
    sku: str = Field(..., regex=r'^[A-Z]{2,3}-\d{4,6}$')
    category: str

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty or whitespace')
        return v.strip().title()

    @validator('category')
    def category_must_be_valid(cls, v):
        valid_categories = ['electronics', 'clothing', 'books', 'home']
        if v.lower() not in valid_categories:
            raise ValueError(f'Category must be one of: {valid_categories}')
        return v.lower()
```

#### **Manejo Proactivo de Errores**

```python
from fastapi import HTTPException

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    # Validación de entrada
    if product_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="Product ID must be positive"
        )

    # Buscar producto
    product = get_product_from_db(product_id)
    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {product_id} not found"
        )

    # Verificar disponibilidad
    if not product.active:
        raise HTTPException(
            status_code=410,  # Gone
            detail="Product is no longer available"
        )

    return product
```

---

## 🎯 Resumen de Conceptos Clave

### **Para recordar siempre:**

1. **REST = Predictibilidad**: Usar convenciones estándar
2. **HTTP Methods**: Cada uno tiene un propósito específico
3. **Status Codes**: Comunican el resultado claramente
4. **Validación**: Validar siempre datos de entrada
5. **Consistencia**: Mantener patrones a lo largo de la API
6. **Errores**: Manejar proactivamente y dar feedback útil

### **Checklist antes de publicar un endpoint:**

- ✅ ¿Usa el método HTTP correcto?
- ✅ ¿La URL sigue convenciones REST?
- ✅ ¿Valida todos los parámetros de entrada?
- ✅ ¿Maneja todos los casos de error?
- ✅ ¿Retorna el status code apropiado?
- ✅ ¿El response es consistente con otros endpoints?

---

_Teoría desarrollada para Semana 3 - Bootcamp FastAPI_  
_Fecha: 24 de julio de 2025_
