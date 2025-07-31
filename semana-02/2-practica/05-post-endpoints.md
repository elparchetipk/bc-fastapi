# Práctica 5: Endpoints POST y Parámetros

## 🎯 Objetivo Ultra-Básico

Dominar **endpoints POST y parámetros** básicos en 90 minutos (Bloque 3), consolidando todo lo aprendido.

## ⏱️ Tiempo: 90 minutos (Bloque 3)

## 📋 Pre-requisitos

- ✅ Type hints implementados (Bloque 1)
- ✅ Pydantic básico funcionando (Bloque 2)
- ✅ Al menos 1 endpoint POST creado

## 🚀 Desarrollo Ultra-Rápido (Solo 3 pasos)

### Paso 1: Parámetros de Ruta y Query (30 min)

**Parámetros de Ruta** (en la URL):

```python
# Agregar a tu main.py existente

# Parámetro de ruta simple
@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    return {"error": "Product not found"}

# Múltiples parámetros de ruta
@app.get("/categories/{category}/products/{product_id}")
def product_by_category(category: str, product_id: int) -> dict:
    return {
        "category": category,
        "product_id": product_id,
        "message": f"Searching product {product_id} in {category}"
    }
```

**Parámetros de Query** (después del ?):

```python
from typing import Optional

# Query parameters opcionales
@app.get("/search")
def search_products(
    name: Optional[str] = None,
    max_price: Optional[int] = None,
    available: Optional[bool] = None
) -> dict:
    results = products.copy()

    if name:
        results = [p for p in results if name.lower() in p["name"].lower()]
    if max_price:
        results = [p for p in results if p["price"] <= max_price]
    if available is not None:
        results = [p for p in results if p["available"] == available]

    return {"results": results, "total": len(results)}
```

**🔍 Probar** (5 min):

- http://127.0.0.1:8000/products/1
- http://127.0.0.1:8000/search?name=laptop
- http://127.0.0.1:8000/search?max_price=50000&available=true

### Paso 2: Response Models con Pydantic (30 min)

**Definir respuestas consistentes:**

```python
# Agregar estos modelos después de tu modelo Product

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    available: bool
    message: str = "Product retrieved successfully"

class ProductListResponse(BaseModel):
    products: list
    total: int
    message: str = "List retrieved successfully"

# Actualizar endpoints para usar response models
@app.get("/products", response_model=ProductListResponse)
def get_products() -> ProductListResponse:
    return ProductListResponse(
        products=products,
        total=len(products)
    )

@app.post("/products", response_model=ProductResponse)
def create_product(product: Product) -> ProductResponse:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)

    return ProductResponse(
        id=product_dict["id"],
        name=product_dict["name"],
        price=product_dict["price"],
        available=product_dict["available"],
        message="Product created successfully"
    )
```

### Paso 3: Integración y Consolidación (30 min)

**Tu API completa debería verse así:**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="My Enhanced API - Week 2")

# Modelos de datos
class Product(BaseModel):
    name: str
    price: int
    available: bool = True

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    available: bool
    message: str = "Successful operation"

class ProductListResponse(BaseModel):
    products: List[dict]
    total: int
    message: str = "List retrieved"

# Almacenamiento temporal
products = []

# Endpoints básicos
@app.get("/")
def hello_world() -> dict:
    return {"message": "Week 2 API with Pydantic and Type Hints!"}

@app.get("/products", response_model=ProductListResponse)
def get_products() -> ProductListResponse:
    return ProductListResponse(
        products=products,
        total=len(products)
    )

@app.post("/products", response_model=ProductResponse)
def create_product(product: Product) -> ProductResponse:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)

    return ProductResponse(**product_dict, message="Product created")

@app.get("/products/{product_id}")
def get_product(product_id: int) -> dict:
    for product in products:
        if product["id"] == product_id:
            return {"product": product}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/search")
def search_products(
    name: Optional[str] = None,
    max_price: Optional[int] = None
) -> dict:
    results = products.copy()

    if name:
        results = [p for p in results if name.lower() in p["name"].lower()]
    if max_price:
        results = [p for p in results if p["price"] <= max_price]

    return {"results": results, "total": len(results)}
```

**🔍 Verificación Final** (15 min):

1. Todos los endpoints funcionan
2. /docs muestra response models
3. Validación automática funciona
4. Búsqueda con parámetros funciona

## ✅ Criterios de Éxito (Solo estos 4)

1. **✅ Endpoint POST funcionando**: Con Pydantic y response model
2. **✅ Parámetros de ruta**: Al menos 1 endpoint con {id}
3. **✅ Parámetros de query**: Al menos 1 endpoint con búsqueda
4. **✅ Response models**: Respuestas consistentes

## 🚨 Si algo no funciona

**Prioridades en orden**:

1. **Que funcione el POST básico** (más importante)
2. **Que funcionen los parámetros de ruta**
3. **Que funcionen los query parameters**
4. **Response models** (si hay tiempo)

**Pide ayuda inmediatamente** si el POST no funciona.

## 📝 Reflexión (Solo 1 pregunta)

**¿Cómo mejoraron estos conceptos tu API comparada con Semana 1?**

Anota 2-3 oraciones para tu README.

---

## 🎯 Resultado Final Esperado

Al final de estos 90 minutos tendrás:

- ✅ API completa con POST, GET con parámetros
- ✅ Validación automática funcionando
- ✅ Response models para respuestas consistentes
- ✅ Manejo básico de errores
- ✅ API significativamente más robusta que Semana 1

**¡Excelente! Tu API está evolucionando profesionalmente! 🎉**

---

## 📋 Para el Bloque 4 (45 min) - Consolidación

En el último bloque:

1. **Probar todo funcionando** completamente
2. **Actualizar README** con nuevos endpoints
3. **Subir a GitHub** código mejorado
4. **Reflexión final** sobre el progreso

**Tu API está lista para ser entregada - ¡gran progreso desde Semana 1!**
