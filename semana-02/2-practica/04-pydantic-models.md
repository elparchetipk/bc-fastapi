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
@app.post("/usuarios")
def crear_usuario(datos):
    # ¿Qué pasa si datos no tiene 'nombre'?
    # ¿Qué pasa si 'edad' es texto en lugar de número?
    return {"usuario": datos}
```

**Solución con Pydantic:**

```python
from pydantic import BaseModel

# Definir QUÉ datos esperas
class Usuario(BaseModel):
    nombre: str
    edad: int
    email: str

@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    # Pydantic garantiza que los datos son correctos
    return {"usuario": usuario.dict()}
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

app = FastAPI(title="Mi API con Pydantic")

# Tu primer modelo de datos
class Producto(BaseModel):
    nombre: str
    precio: int  # en centavos para evitar decimales
    disponible: bool = True  # valor por defecto

# Lista temporal para guardar productos
productos = []

# Endpoint GET (como antes)
@app.get("/")
def hola_mundo() -> dict:
    return {"mensaje": "¡API con Pydantic!"}

# NUEVO: Endpoint POST con Pydantic
@app.post("/productos")
def crear_producto(producto: Producto) -> dict:
    producto_dict = producto.dict()
    producto_dict["id"] = len(productos) + 1
    productos.append(producto_dict)
    return {"mensaje": "Producto creado", "producto": producto_dict}

# Endpoint para ver todos los productos
@app.get("/productos")
def obtener_productos() -> dict:
    return {"productos": productos, "total": len(productos)}
```

**🔍 Verificación (10 min):**

1. Ejecuta `uvicorn main:app --reload`
2. Ve a http://127.0.0.1:8000/docs
3. Busca el endpoint POST /productos
4. Pruébalo con estos datos:

```json
{
  "nombre": "Laptop",
  "precio": 150000,
  "disponible": true
}
```

### Paso 3: Validación Automática en Acción (40 min)

**Probar qué pasa con datos incorrectos** (en /docs):

```json
// Datos correctos ✅
{
  "nombre": "Mouse",
  "precio": 2500,
  "disponible": false
}

// Datos incorrectos ❌ (precio como texto)
{
  "nombre": "Teclado",
  "precio": "muy caro",
  "disponible": true
}

// Datos incompletos ❌ (falta precio)
{
  "nombre": "Monitor"
}
```

**Modelo más completo** (si hay tiempo):

```python
from typing import Optional

class UsuarioCompleto(BaseModel):
    nombre: str
    edad: int
    email: str
    telefono: Optional[str] = None  # campo opcional
    activo: bool = True

@app.post("/usuarios")
def crear_usuario(usuario: UsuarioCompleto) -> dict:
    return {"usuario": usuario.dict(), "valido": True}
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
