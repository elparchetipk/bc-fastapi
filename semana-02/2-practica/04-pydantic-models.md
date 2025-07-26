# Práctica 4: Pydantic Modelos Básicos

## 🎯 Objetivo Ultra-Básico

Aprender **Pydantic básico** para validación automática de datos en 120 minutos (Bloque 2 post-break), enfocándose solo en lo esencial.

## ⏱️ Tiempo: 120 minutos (Bloque 2 post-break)

## 📋 Pre-requisitos

- ✅ API con type hints (Bloque 1 completado)
- ✅ Break de 30 min completado
- ✅ Mente descansada y lista para validación

## 🚀 Desarrollo Ultra-Rápido (Solo 3 pasos)

### Paso 1: ¿Qué es Pydantic? (40 min)

**Concepto Simple**: Pydantic valida automáticamente los datos que llegan a tu API.

**Problema sin Pydantic:**

```python
# Alguien envía datos incorrectos a tu API
# Tu API se rompe o da resultados raros
@app.post("/users")
def create_user(data):
    # ¿Qué pasa si data no tiene 'name'?
    # ¿Qué pasa si 'age' es texto en lugar de número?
    return {"user": data}
```

**Solución con Pydantic:**

```python
from pydantic import BaseModel

# Definir QUÉ datos esperas
class User(BaseModel):
    name: str
    age: int
    email: str

@app.post("/users")
def create_user(user: User):
    # Pydantic garantiza que los datos son correctos
    return {"user": user.dict()}
```

**Instalar Pydantic** (si no está):

```bash
pip install pydantic
```

### Paso 2: Tu Primer Modelo Pydantic (40 min)

**Actualiza tu main.py** (agregar al inicio):

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="My API with Pydantic")

# Tu primer modelo de datos
class Product(BaseModel):
    name: str
    price: int  # en centavos para evitar decimales
    available: bool = True  # valor por defecto

# Lista temporal para guardar productos
products = []

# Endpoint GET (como antes)
@app.get("/")
def hello_world() -> dict:
    return {"message": "API with Pydantic!"}

# NUEVO: Endpoint POST con Pydantic
@app.post("/products")
def create_product(product: Product) -> dict:
    product_dict = product.dict()
    product_dict["id"] = len(products) + 1
    products.append(product_dict)
    return {"message": "Product created", "product": product_dict}

# Endpoint para ver todos los productos
@app.get("/products")
def get_products() -> dict:
    return {"products": products, "total": len(products)}
```

**🔍 Verificación (10 min):**

1. Ejecuta `uvicorn main:app --reload`
2. Ve a http://127.0.0.1:8000/docs
3. Busca el endpoint POST /products
4. Pruébalo con estos datos:

```json
{
  "name": "Laptop",
  "price": 150000,
  "available": true
}
```

### Paso 3: Validación Automática en Acción (40 min)

**Probar qué pasa con datos incorrectos** (en /docs):

```json
// Datos correctos ✅
{
  "name": "Mouse",
  "price": 2500,
  "available": false
}

// Datos incorrectos ❌ (price como texto)
{
  "name": "Keyboard",
  "price": "very expensive",
  "available": true
}

// Datos incompletos ❌ (falta price)
{
  "name": "Monitor"
}
```

**Modelo más completo** (si hay tiempo):

```python
from typing import Optional

class CompleteUser(BaseModel):
    name: str
    age: int
    email: str
    phone: Optional[str] = None  # campo opcional
    active: bool = True

@app.post("/users")
def create_user(user: CompleteUser) -> dict:
    return {"user": user.dict(), "valid": True}
```

**🔍 Entender los errores** (10 min):

- Pydantic te dice exactamente qué está mal
- Los errores aparecen en /docs automáticamente
- Tu API no se rompe, solo rechaza datos incorrectos

## ✅ Criterios de Éxito (Solo estos 3)

1. **✅ Modelo Pydantic funcionando**: Al menos 1 clase BaseModel
2. **✅ Endpoint POST funcionando**: Acepta datos y los valida
3. **✅ Validación automática**: Rechaza datos incorrectos correctamente

## 🚨 Si algo no funciona

**NO te compliques**. Pydantic puede ser confuso al principio:

1. **Revisa imports**: `from pydantic import BaseModel`
2. **Verifica indentación**: Python es estricto con espacios
3. **Pide ayuda**: El instructor está para esto
4. **Usa ejemplos simples**: Copia exacto del código de arriba

## 📝 Reflexión (Solo 1 pregunta)

**¿Cómo te ayuda Pydantic a crear APIs más robustas?**

Anota 2-3 oraciones para incluir en tu README.

---

## 🎯 Resultado Final Esperado

Al final de estos 120 minutos tendrás:

- ✅ Al menos 1 modelo Pydantic funcionando
- ✅ Endpoint POST que valida datos automáticamente
- ✅ Comprensión de validación automática
- ✅ API más robusta y profesional
- ✅ Preparación para endpoints más complejos (Bloque 3)

**¡Increíble! Tu API ahora valida datos automáticamente! 🎉**

---

## 📋 Para el Bloque 3 (90 min)

Con Pydantic funcionando, en el Bloque 3 aprenderás:

1. **Parámetros de ruta y query** con validación
2. **Response models** para respuestas consistentes
3. **Integración completa** de conceptos

**Guarda tu main.py con Pydantic - lo evolucionaremos en Bloque 3**
