# Práctica 3: Python Type Hints Básicos

## 🎯 Objetivo Ultra-Básico

Aprender **solo los type hints esenciales** para APIs en 75 minutos (Bloque 1), enfocándose únicamente en lo que necesitas para FastAPI.

## ⏱️ Tiempo: 75 minutos (Bloque 1 pre-break)

## 📋 Pre-requisitos

- ✅ API de Semana 1 funcionando
- ✅ main.py con endpoints básicos
- ✅ Python ejecutándose correctamente

## 🚀 Desarrollo Ultra-Rápido (Solo 3 pasos)

### Paso 1: Type Hints Básicos (25 min)

**Concepto**: Los type hints le dicen a Python (y a ti) qué tipo de datos espera una función.

```python
# Sin type hints (como en Semana 1)
def saludar(nombre):
    return f"Hola {nombre}!"

# Con type hints (lo que aprenderemos hoy)
def saludar(nombre: str) -> str:
    return f"Hola {nombre}!"
```

**🔍 Tipos básicos que necesitas:**

```python
# Tipos simples para APIs
def crear_usuario(nombre: str, edad: int, activo: bool) -> dict:
    return {"nombre": nombre, "edad": edad, "activo": activo}

def obtener_numeros() -> list:
    return [1, 2, 3, 4, 5]

def configuracion() -> dict:
    return {"debug": True, "version": "1.0"}
```

### Paso 2: Aplicar a tu API de Semana 1 (25 min)

**Toma tu main.py de Semana 1** y añade type hints:

```python
from fastapi import FastAPI

app = FastAPI(title="Mi Primera API")

# ANTES (Semana 1)
@app.get("/")
def hola_mundo():
    return {"mensaje": "¡Mi primera API FastAPI!"}

# DESPUÉS (con type hints)
@app.get("/")
def hola_mundo() -> dict:
    return {"mensaje": "¡Mi primera API FastAPI!"}

# Si tenías endpoint con parámetro
@app.get("/saludo/{nombre}")
def saludar(nombre: str) -> dict:
    return {"saludo": f"¡Hola {nombre}!"}

# Endpoint con múltiples parámetros
@app.get("/calcular/{num1}/{num2}")
def calcular(num1: int, num2: int) -> dict:
    suma = num1 + num2
    return {"resultado": suma, "operacion": "suma"}
```

**🔍 Verificación (5 min):**

1. Ejecuta `uvicorn main:app --reload`
2. Ve a http://127.0.0.1:8000/docs
3. Los endpoints deberían seguir funcionando igual

### Paso 3: Type Hints para Listas y Diccionarios (25 min)

**Para APIs más útiles** (solo lo básico):

```python
from typing import List, Dict

# Lista de strings
@app.get("/frutas")
def obtener_frutas() -> List[str]:
    return ["manzana", "banana", "naranja"]

# Lista de números
@app.get("/numeros")
def obtener_numeros() -> List[int]:
    return [1, 2, 3, 4, 5]

# Diccionario con estructura conocida
@app.get("/usuario/{user_id}")
def obtener_usuario(user_id: int) -> Dict[str, str]:
    return {
        "id": str(user_id),
        "nombre": "Usuario Demo",
        "email": "demo@ejemplo.com"
    }
```

**🔍 Verificación Final:**

- Todos tus endpoints tienen type hints
- La API sigue funcionando
- /docs muestra la información correcta

## ✅ Criterios de Éxito (Solo estos 3)

1. **✅ Funciones con type hints**: Al menos 3 funciones con tipos
2. **✅ API funcionando**: Todo sigue trabajando como antes
3. **✅ Comprensión básica**: Entiendes qué hacen los tipos

## 🚨 Si algo no funciona

**NO te compliques**. Los type hints son solo ayuda visual. Si algo se rompe:

1. **Quita los type hints temporalmente**
2. **Pide ayuda al instructor**
3. **Asegúrate de que la API funcione sin tipos primero**

## 📝 Reflexión (Solo 1 pregunta)

**¿Los type hints hacen tu código más claro? ¿Por qué?**

Anota 2-3 oraciones para incluir en tu README.

---

## 🎯 Resultado Final Esperado

Al final de estos 75 minutos tendrás:

- ✅ Type hints básicos en tu API
- ✅ Comprensión de str, int, bool, list, dict
- ✅ API funcionando igual que antes pero más clara
- ✅ Preparación para Pydantic (después del break)

**¡Excelente! Ahora tu código es más profesional! 🎉**

---

## 📋 Para el Break (30 min)

Durante el break obligatorio:

1. **Descansa** - Los type hints pueden ser confusos al principio
2. **Revisa tu código** - Mira cómo se ve con los tipos
3. **Prepárate mentalmente** - Después del break: Pydantic (validación automática)

**Guarda tu main.py actualizado - lo necesitaremos después del break**
