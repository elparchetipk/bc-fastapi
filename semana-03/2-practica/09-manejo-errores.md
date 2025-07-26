# Práctica 9: Manejo de Errores Básico

## 🎯 Objetivo Básico

Manejar **errores de forma profesional** en tu API en 90 minutos (Bloque 3), enfocándose solo en lo que realmente necesitas para una API robusta.

## ⏱️ Tiempo: 90 minutos (Bloque 3)

## 📋 Pre-requisitos

- ✅ Validación avanzada funcionando (Práctica 8 completada)
- ✅ Endpoints con Pydantic (Semana 2)
- ✅ Comprensión básica de HTTP status codes
- ✅ Energía para el último bloque del día

## 🚀 Desarrollo Rápido (Solo 3 pasos)

### Paso 1: Manejo Básico de Errores (30 min)

**Problema**: Tu API da errores confusos y no ayudan al usuario.

**Solución**: HTTPException con mensajes claros.

```python
# Agregar a tu main.py existente de Semana 2
from fastapi import HTTPException

# Lista simple para simular base de datos
products = [
    {"id": 1, "name": "Laptop", "price": 1500.0, "stock": 10},
    {"id": 2, "name": "Mouse", "price": 25.0, "stock": 50},
    {"id": 3, "name": "Teclado", "price": 75.0, "stock": 0}
]

# Endpoint con manejo de errores básico
@app.get("/products/{product_id}")
def get_product(product_id: int):
    # Error: ID inválido
    if product_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="ID del producto debe ser mayor a 0"
        )

    # Buscar producto
    for product in products:
        if product["id"] == product_id:
            return {"success": True, "product": product}

    # Error: No encontrado
    raise HTTPException(
        status_code=404,
        detail=f"Producto con ID {product_id} no encontrado"
    )

@app.post("/products")
def create_product(product: dict):
    # Validación básica
    if "name" not in product:
        raise HTTPException(
            status_code=400,
            detail="El campo 'name' es obligatorio"
        )

    if "price" not in product:
        raise HTTPException(
            status_code=400,
            detail="El campo 'price' es obligatorio"
        )

    if product["price"] <= 0:
        raise HTTPException(
            status_code=400,
            detail="El precio debe ser mayor a 0"
        )

    # Verificar que no exista el nombre
    for existing in products:
        if existing["name"].lower() == product["name"].lower():
            raise HTTPException(
                status_code=409,
                detail=f"Ya existe un producto con el nombre '{product['name']}'"
            )

    # Crear producto
    new_id = max([p["id"] for p in products]) + 1
    new_product = {
        "id": new_id,
        "name": product["name"],
        "price": product["price"],
        "stock": product.get("stock", 0)
    }

    products.append(new_product)
    return {"success": True, "product": new_product}

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    # Buscar y eliminar
    for i, product in enumerate(products):
        if product["id"] == product_id:
            deleted_product = products.pop(i)
            return {"success": True, "message": f"Producto '{deleted_product['name']}' eliminado"}

    # Error: No encontrado
    raise HTTPException(
        status_code=404,
        detail=f"No se puede eliminar: producto con ID {product_id} no existe"
    )
```

**🔍 Probar errores** (10 min):

```bash
# ✅ Producto existente
curl "http://127.0.0.1:8000/products/1"

# ❌ Error 404 - No encontrado
curl "http://127.0.0.1:8000/products/999"

# ❌ Error 400 - ID inválido
curl "http://127.0.0.1:8000/products/-1"

# ✅ Crear producto válido
curl -X POST "http://127.0.0.1:8000/products" \
-H "Content-Type: application/json" \
-d '{"name": "Monitor", "price": 300.0, "stock": 5}'

# ❌ Error 409 - Nombre duplicado
curl -X POST "http://127.0.0.1:8000/products" \
-H "Content-Type: application/json" \
-d '{"name": "Laptop", "price": 1000.0}'

# ❌ Error 400 - Campo faltante
curl -X POST "http://127.0.0.1:8000/products" \
-H "Content-Type: application/json" \
-d '{"price": 100.0}'
```

### Paso 2: Respuestas de Error Consistentes (30 min)

**Problema**: Los errores de tu API se ven diferentes cada vez.

**Solución**: Formato estándar para todas las respuestas de error.

```python
# Agregar al main.py después de los imports
from datetime import datetime

# Función para crear respuestas de error consistentes
def create_error_response(message: str, status_code: int, details: dict = None):
    return {
        "success": False,
        "error": {
            "message": message,
            "status_code": status_code,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
    }

# Función para crear respuestas de éxito consistentes
def create_success_response(message: str, data: dict = None):
    return {
        "success": True,
        "message": message,
        "data": data or {},
        "timestamp": datetime.now().isoformat()
    }

# Actualizar endpoints con respuestas consistentes
@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id <= 0:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="ID del producto debe ser mayor a 0",
                status_code=400,
                details={"provided_id": product_id, "min_id": 1}
            )
        )

    for product in products:
        if product["id"] == product_id:
            return create_success_response(
                message="Producto encontrado",
                data={"product": product}
            )

    raise HTTPException(
        status_code=404,
        detail=create_error_response(
            message=f"Producto con ID {product_id} no encontrado",
            status_code=404,
            details={"requested_id": product_id, "available_ids": [p["id"] for p in products]}
        )
    )

@app.post("/products")
def create_product(product: dict):
    # Validaciones con respuestas consistentes
    if "name" not in product:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="El campo 'name' es obligatorio",
                status_code=400,
                details={"missing_field": "name", "received_fields": list(product.keys())}
            )
        )

    if "price" not in product:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="El campo 'price' es obligatorio",
                status_code=400,
                details={"missing_field": "price", "received_fields": list(product.keys())}
            )
        )

    if product["price"] <= 0:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="El precio debe ser mayor a 0",
                status_code=400,
                details={"provided_price": product["price"], "min_price": 0.01}
            )
        )

    # Verificar duplicados
    for existing in products:
        if existing["name"].lower() == product["name"].lower():
            raise HTTPException(
                status_code=409,
                detail=create_error_response(
                    message=f"Ya existe un producto con el nombre '{product['name']}'",
                    status_code=409,
                    details={
                        "conflicting_name": product["name"],
                        "existing_product_id": existing["id"]
                    }
                )
            )

    # Crear producto
    new_id = max([p["id"] for p in products]) + 1 if products else 1
    new_product = {
        "id": new_id,
        "name": product["name"],
        "price": product["price"],
        "stock": product.get("stock", 0)
    }

    products.append(new_product)
    return create_success_response(
        message=f"Producto '{new_product['name']}' creado exitosamente",
        data={"product": new_product}
    )

# Endpoint para listar todos los productos
@app.get("/products")
def get_all_products():
    return create_success_response(
        message=f"Se encontraron {len(products)} productos",
        data={
            "products": products,
            "total": len(products)
        }
    )
```

**🔍 Probar respuestas consistentes** (10 min):

```bash
# ✅ Respuesta de éxito consistente
curl "http://127.0.0.1:8000/products/1"

# ❌ Error consistente - No encontrado
curl "http://127.0.0.1:8000/products/999"

# ✅ Lista de productos
curl "http://127.0.0.1:8000/products"

# ❌ Error consistente - Campo faltante
curl -X POST "http://127.0.0.1:8000/products" \
-H "Content-Type: application/json" \
-d '{"price": 100.0}'

# ✅ Crear producto exitoso
curl -X POST "http://127.0.0.1:8000/products" \
-H "Content-Type: application/json" \
-d '{"name": "Auriculares", "price": 45.0, "stock": 20}'
```

**Nota**: Ahora todas las respuestas (éxito y error) tienen el mismo formato con `success`, `message`, `timestamp` y detalles específicos.

### Paso 3: Logs Básicos (30 min)

**Problema**: No sabes qué está pasando en tu API cuando algo falla.

**Solución**: Logging simple pero efectivo.

```python
# Agregar al main.py después de los imports
import logging

# Configurar logging básico
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Actualizar endpoints con logging
@app.get("/products/{product_id}")
def get_product(product_id: int):
    logger.info(f"Buscando producto con ID: {product_id}")

    if product_id <= 0:
        logger.warning(f"ID inválido recibido: {product_id}")
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="ID del producto debe ser mayor a 0",
                status_code=400,
                details={"provided_id": product_id, "min_id": 1}
            )
        )

    for product in products:
        if product["id"] == product_id:
            logger.info(f"Producto encontrado: {product['name']}")
            return create_success_response(
                message="Producto encontrado",
                data={"product": product}
            )

    logger.warning(f"Producto no encontrado: ID {product_id}")
    raise HTTPException(
        status_code=404,
        detail=create_error_response(
            message=f"Producto con ID {product_id} no encontrado",
            status_code=404,
            details={"requested_id": product_id, "available_ids": [p["id"] for p in products]}
        )
    )

@app.post("/products")
def create_product(product: dict):
    logger.info(f"Intentando crear producto: {product.get('name', 'SIN_NOMBRE')}")

    # Validaciones con logging
    if "name" not in product:
        logger.error("Intento de crear producto sin nombre")
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="El campo 'name' es obligatorio",
                status_code=400,
                details={"missing_field": "name", "received_fields": list(product.keys())}
            )
        )

    if "price" not in product:
        logger.error(f"Intento de crear producto '{product['name']}' sin precio")
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="El campo 'price' es obligatorio",
                status_code=400,
                details={"missing_field": "price", "received_fields": list(product.keys())}
            )
        )

    if product["price"] <= 0:
        logger.error(f"Precio inválido para producto '{product['name']}': {product['price']}")
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                message="El precio debe ser mayor a 0",
                status_code=400,
                details={"provided_price": product["price"], "min_price": 0.01}
            )
        )

    # Verificar duplicados
    for existing in products:
        if existing["name"].lower() == product["name"].lower():
            logger.warning(f"Intento de crear producto duplicado: '{product['name']}'")
            raise HTTPException(
                status_code=409,
                detail=create_error_response(
                    message=f"Ya existe un producto con el nombre '{product['name']}'",
                    status_code=409,
                    details={
                        "conflicting_name": product["name"],
                        "existing_product_id": existing["id"]
                    }
                )
            )

    # Crear producto
    new_id = max([p["id"] for p in products]) + 1 if products else 1
    new_product = {
        "id": new_id,
        "name": product["name"],
        "price": product["price"],
        "stock": product.get("stock", 0)
    }

    products.append(new_product)
    logger.info(f"Producto creado exitosamente: ID {new_id}, Nombre: {new_product['name']}")

    return create_success_response(
        message=f"Producto '{new_product['name']}' creado exitosamente",
        data={"product": new_product}
    )

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    logger.info(f"Intentando eliminar producto con ID: {product_id}")

    for i, product in enumerate(products):
        if product["id"] == product_id:
            deleted_product = products.pop(i)
            logger.info(f"Producto eliminado: ID {product_id}, Nombre: {deleted_product['name']}")
            return create_success_response(
                message=f"Producto '{deleted_product['name']}' eliminado exitosamente",
                data={"deleted_product": deleted_product}
            )

    logger.warning(f"Intento de eliminar producto inexistente: ID {product_id}")
    raise HTTPException(
        status_code=404,
        detail=create_error_response(
            message=f"No se puede eliminar: producto con ID {product_id} no existe",
            status_code=404,
            details={"requested_id": product_id, "available_ids": [p["id"] for p in products]}
        )
    )

# Endpoint para estadísticas (con logging)
@app.get("/stats")
def get_stats():
    logger.info("Consultando estadísticas de la API")

    total_products = len(products)
    total_stock = sum(p.get("stock", 0) for p in products)
    avg_price = sum(p["price"] for p in products) / total_products if total_products > 0 else 0

    stats = {
        "total_products": total_products,
        "total_stock": total_stock,
        "average_price": round(avg_price, 2)
    }

    logger.info(f"Estadísticas calculadas: {stats}")

    return create_success_response(
        message="Estadísticas calculadas exitosamente",
        data={"stats": stats}
    )
```

**🔍 Probar con logs** (10 min):

```bash
# Ejecuta tu API y observa los logs en la terminal

# ✅ Crear producto (observa los logs)
curl -X POST "http://127.0.0.1:8000/products" \
-H "Content-Type: application/json" \
-d '{"name": "Tablet", "price": 250.0, "stock": 15}'

# ❌ Error con logs
curl -X POST "http://127.0.0.1:8000/products" \
-H "Content-Type: application/json" \
-d '{"price": 100.0}'

# ✅ Consultar producto (observa los logs)
curl "http://127.0.0.1:8000/products/1"

# ✅ Ver estadísticas (observa los logs)
curl "http://127.0.0.1:8000/stats"

# ❌ Eliminar producto inexistente (observa los logs)
curl -X DELETE "http://127.0.0.1:8000/products/999"
```

**En tu terminal verás logs como:**

```
2025-07-26 10:30:15 - INFO - Buscando producto con ID: 1
2025-07-26 10:30:15 - INFO - Producto encontrado: Laptop
2025-07-26 10:30:45 - INFO - Intentando crear producto: Tablet
2025-07-26 10:30:45 - INFO - Producto creado exitosamente: ID 4, Nombre: Tablet
2025-07-26 10:31:00 - ERROR - Intento de crear producto sin nombre
```

## ✅ Checkpoint: ¿Qué Aprendiste?

Al final de esta práctica deberías tener:

1. **Manejo básico de errores**: HTTPException con mensajes claros
2. **Respuestas consistentes**: Formato estándar para éxito y error
3. **Logging efectivo**: Registro de eventos importantes
4. **API más robusta**: Mejor experiencia para el usuario
5. **Depuración fácil**: Logs que ayudan a encontrar problemas

**🔥 Lo más importante**: Tu API ahora maneja errores de forma profesional y puedes ver qué está pasando cuando algo falla.

## 🎯 Próximo Paso

¡Felicidades! Has completado las prácticas básicas de FastAPI. En el proyecto final aplicarás todo lo aprendido.
