# Práctica 8: Validación Avanzada con Pydantic

## 🎯 Objetivo

Dominar **validaciones avanzadas Pydantic** para APIs robustas en 120 minutos (Bloque 2 post-break), enfocándose solo en validaciones que realmente usarás.

## ⏱️ Tiempo: 120 minutos (Bloque 2 post-break)

## 📋 Pre-requisitos

- ✅ Pydantic básico funcionando (Semana 2 completada)
- ✅ Endpoints POST creados (Semana 2)
- ✅ Break de 30 min completado
- ✅ Mente descansada y lista para validaciones

## 🚀 Desarrollo Rápido (Solo 3 pasos)

### Paso 1: Validadores Básicos que Realmente Usarás (40 min)

**Problema**: Tu API acepta datos incorrectos y se rompe.

**Solución**: Validaciones automáticas que funcionan.

```python
# Agregar a tu main.py existente de Semana 2
from pydantic import BaseModel, validator, Field
from typing import Optional
import re

# Modelo User mejorado con validaciones
class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=18, le=100)  # ge = greater or equal, le = less or equal
    phone: str = Field(..., min_length=10, max_length=15)

    # Validador custom para email
    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Email debe contener @')
        return v.lower()  # Convertir a minúsculas

    # Validador custom para teléfono
    @validator('phone')
    def validate_phone(cls, v):
        # Remover espacios y guiones
        phone_clean = re.sub(r'[\s\-]', '', v)
        if not phone_clean.isdigit():
            raise ValueError('Teléfono debe contener solo números')
        return phone_clean

# Modelo Product mejorado
class Product(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    price: float = Field(..., gt=0, le=1000000)  # gt = greater than
    category: str = Field(..., regex=r'^[a-zA-Z\s]+$')
    stock: int = Field(..., ge=0)
    description: Optional[str] = Field(None, max_length=500)

    @validator('name')
    def validate_name(cls, v):
        if v.strip() != v:
            raise ValueError('El nombre no puede empezar o terminar con espacios')
        return v.title()  # Primera letra en mayúscula
```

**🔍 Probar validaciones** (10 min):

```python
# Agregar endpoint de prueba
@app.post("/users/validate")
def create_user_validated(user: User):
    return {
        "message": "Usuario válido creado",
        "user": user.dict(),
        "validations": "Todas las validaciones pasaron"
    }
```

**Casos de prueba con curl:**

```bash
# ✅ Caso válido
curl -X POST "http://127.0.0.1:8000/users/validate" \
-H "Content-Type: application/json" \
-d '{"name": "Juan Pérez", "email": "juan@email.com", "age": 25, "phone": "123-456-7890"}'

# ❌ Caso inválido (email sin @)
curl -X POST "http://127.0.0.1:8000/users/validate" \
-H "Content-Type: application/json" \
-d '{"name": "Juan", "email": "juanemail.com", "age": 25, "phone": "123456"}'
```

### Paso 2: Validaciones Entre Campos (40 min)

**Problema**: Necesitas validar que múltiples campos sean consistentes entre sí.

**Solución**: Root validators que validan todo el modelo.

```python
# Agregar al main.py después de los modelos anteriores
from pydantic import root_validator

class Order(BaseModel):
    product_name: str = Field(..., min_length=3)
    quantity: int = Field(..., gt=0, le=100)
    unit_price: float = Field(..., gt=0)
    total_price: float = Field(..., gt=0)
    discount_percent: float = Field(0, ge=0, le=50)
    shipping_required: bool = True
    shipping_cost: float = Field(0, ge=0)

    # Validar que total_price sea correcto
    @root_validator
    def validate_pricing(cls, values):
        quantity = values.get('quantity')
        unit_price = values.get('unit_price')
        total_price = values.get('total_price')
        discount = values.get('discount_percent', 0)

        if quantity and unit_price and total_price:
            # Calcular precio esperado
            subtotal = quantity * unit_price
            discount_amount = subtotal * (discount / 100)
            expected_total = subtotal - discount_amount

            # Permitir pequeña diferencia por redondeo
            if abs(total_price - expected_total) > 0.01:
                raise ValueError(
                    f'Total incorrecto. Esperado: {expected_total:.2f}, '
                    f'Recibido: {total_price:.2f}'
                )

        return values

    # Validar envío
    @root_validator
    def validate_shipping(cls, values):
        shipping_required = values.get('shipping_required')
        shipping_cost = values.get('shipping_cost')

        if shipping_required and shipping_cost == 0:
            raise ValueError('Si requiere envío, el costo debe ser mayor a 0')

        if not shipping_required and shipping_cost > 0:
            raise ValueError('Si no requiere envío, el costo debe ser 0')

        return values

# Modelo para registro completo
class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: str
    password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)
    age: int = Field(..., ge=13, le=120)
    terms_accepted: bool

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username solo puede contener letras, números y _')
        return v.lower()

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password debe tener al menos 8 caracteres')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password debe tener al menos una mayúscula')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password debe tener al menos un número')
        return v

    @root_validator
    def validate_passwords_match(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValueError('Las contraseñas no coinciden')

        return values

    @root_validator
    def validate_terms(cls, values):
        terms_accepted = values.get('terms_accepted')
        age = values.get('age')

        if not terms_accepted:
            raise ValueError('Debe aceptar los términos y condiciones')

        if age and age < 18 and terms_accepted:
            raise ValueError('Menores de 18 necesitan autorización parental')

        return values
```

**🔍 Probar validaciones cruzadas** (10 min):

```python
# Endpoints de prueba
@app.post("/orders/validate")
def create_order(order: Order):
    return {
        "message": "Orden válida",
        "order": order.dict(),
        "calculated_total": order.total_price
    }

@app.post("/users/register")
def register_user(user: UserRegistration):
    # Remover confirm_password antes de guardar
    user_data = user.dict()
    del user_data['confirm_password']

    return {
        "message": "Usuario registrado exitosamente",
        "user": user_data
    }
```

**Casos de prueba:**

```bash
# ✅ Orden válida
curl -X POST "http://127.0.0.1:8000/orders/validate" \
-H "Content-Type: application/json" \
-d '{
  "product_name": "Laptop",
  "quantity": 2,
  "unit_price": 1000.0,
  "total_price": 1800.0,
  "discount_percent": 10,
  "shipping_required": true,
  "shipping_cost": 50.0
}'

# ❌ Orden con total incorrecto
curl -X POST "http://127.0.0.1:8000/orders/validate" \
-H "Content-Type: application/json" \
-d '{
  "product_name": "Laptop",
  "quantity": 2,
  "unit_price": 1000.0,
  "total_price": 2000.0,
  "discount_percent": 10,
  "shipping_required": true,
  "shipping_cost": 50.0
}'
```

### Paso 3: Query Parameters con Validación (40 min)

**Problema**: Los query parameters también necesitan validación.

**Solución**: Usar FastAPI Query con validaciones automáticas.

```python
# Agregar al main.py
from fastapi import Query, Depends, HTTPException
from typing import List, Optional

# Clase para parámetros de búsqueda
class ProductFilters:
    def __init__(
        self,
        name: Optional[str] = Query(None, min_length=2, max_length=50),
        min_price: Optional[float] = Query(None, ge=0, le=1000000),
        max_price: Optional[float] = Query(None, ge=0, le=1000000),
        category: Optional[str] = Query(None, regex=r'^[a-zA-Z\s]+$'),
        in_stock: Optional[bool] = Query(None),
        tags: Optional[List[str]] = Query(None),
        page: int = Query(1, ge=1, le=100),
        limit: int = Query(10, ge=1, le=50)
    ):
        # Validar que min_price <= max_price
        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise ValueError("min_price no puede ser mayor que max_price")

        self.name = name
        self.min_price = min_price
        self.max_price = max_price
        self.category = category
        self.in_stock = in_stock
        self.tags = tags
        self.page = page
        self.limit = limit

# Endpoints con query parameters validados
@app.get("/products/search")
def search_products(filters: ProductFilters = Depends()):
    # Simular base de datos
    all_products = [
        {"id": 1, "name": "Laptop Gaming", "price": 1500.0, "category": "electronics", "in_stock": True, "tags": ["gaming", "powerful"]},
        {"id": 2, "name": "Mouse Wireless", "price": 50.0, "category": "electronics", "in_stock": True, "tags": ["wireless", "ergonomic"]},
        {"id": 3, "name": "Teclado Mecánico", "price": 120.0, "category": "electronics", "in_stock": False, "tags": ["mechanical", "rgb"]},
        {"id": 4, "name": "Monitor 4K", "price": 800.0, "category": "electronics", "in_stock": True, "tags": ["4k", "gaming"]},
        {"id": 5, "name": "Camiseta Deportiva", "price": 25.0, "category": "clothing", "in_stock": True, "tags": ["sport", "comfortable"]}
    ]

    # Aplicar filtros
    filtered_products = all_products.copy()

    if filters.name:
        filtered_products = [p for p in filtered_products
                           if filters.name.lower() in p["name"].lower()]

    if filters.min_price is not None:
        filtered_products = [p for p in filtered_products
                           if p["price"] >= filters.min_price]

    if filters.max_price is not None:
        filtered_products = [p for p in filtered_products
                           if p["price"] <= filters.max_price]

    if filters.category:
        filtered_products = [p for p in filtered_products
                           if p["category"] == filters.category]

    if filters.in_stock is not None:
        filtered_products = [p for p in filtered_products
                           if p["in_stock"] == filters.in_stock]

    if filters.tags:
        filtered_products = [p for p in filtered_products
                           if any(tag in p["tags"] for tag in filters.tags)]

    # Paginación
    start = (filters.page - 1) * filters.limit
    end = start + filters.limit
    paginated_products = filtered_products[start:end]

    return {
        "products": paginated_products,
        "total": len(filtered_products),
        "page": filters.page,
        "limit": filters.limit,
        "total_pages": (len(filtered_products) + filters.limit - 1) // filters.limit,
        "filters_applied": {
            "name": filters.name,
            "price_range": f"{filters.min_price}-{filters.max_price}",
            "category": filters.category,
            "in_stock": filters.in_stock,
            "tags": filters.tags
        }
    }

# Endpoint adicional con validación de rangos
@app.get("/products/price-range")
def get_products_by_price(
    min_price: float = Query(..., ge=0, le=1000000, description="Precio mínimo"),
    max_price: float = Query(..., ge=0, le=1000000, description="Precio máximo")
):
    # Validación manual adicional
    if min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="El precio mínimo no puede ser mayor al precio máximo"
        )

    return {
        "message": f"Buscando productos entre ${min_price} y ${max_price}",
        "range": {"min": min_price, "max": max_price},
        "range_valid": True
    }
```

**🔍 Probar query parameters** (10 min):

```bash
# ✅ Búsqueda válida
curl "http://127.0.0.1:8000/products/search?name=laptop&min_price=1000&max_price=2000"

# ✅ Búsqueda con categoría y stock
curl "http://127.0.0.1:8000/products/search?category=electronics&in_stock=true&page=1&limit=5"

# ✅ Búsqueda con tags múltiples
curl "http://127.0.0.1:8000/products/search?tags=gaming&tags=powerful"

# ❌ Error: min_price mayor que max_price
curl "http://127.0.0.1:8000/products/price-range?min_price=500&max_price=100"

# ❌ Error: página inválida
curl "http://127.0.0.1:8000/products/search?page=0"

# ❌ Error: límite muy alto
curl "http://127.0.0.1:8000/products/search?limit=1000"
```

**🎯 Verificación Final** (10 min):

Abre <http://127.0.0.1:8000/docs> y verifica que:

1. Los endpoints muestran validaciones automáticas
2. Los parámetros tienen descripções claras
3. Los tipos de datos están bien definidos
4. Los rangos y restricciones aparecen en la documentación

## ✅ Checkpoint: ¿Qué Aprendiste?

Al final de esta práctica deberías tener:

1. **Validadores básicos**: Field con restricciones simples
2. **Validadores custom**: @validator para lógica específica
3. **Validaciones cruzadas**: @root_validator para múltiples campos
4. **Query parameters**: Validación automática de parámetros URL
5. **Manejo de errores**: Mensajes claros cuando algo falla

**🔥 Lo más importante**: Tu API ahora rechaza datos incorrectos automáticamente y le dice al usuario exactamente qué está mal.

## 🎯 Próximo Paso

En la siguiente práctica aprenderás sobre **Manejo de Errores Avanzado** para hacer tu API aún más robusta.
