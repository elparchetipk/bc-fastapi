# Práctica 2: Primera API FastAPI

## 🎯 Objetivo Básico

Crear tu primera API FastAPI funcional en **120 minutos** (después del break de 30 min), enfocándonos únicamente en que **funcione**.

## ⏱️ Tiempo: 120 minutos (Bloque 2 post-break)

## 📋 Pre-requisitos

- ✅ Entorno configurado (Práctica 1 - Bloque 1)
- ✅ Break de 30 min completado
- ✅ Mente descansada y lista para crear tu primera API

## 🚀 Desarrollo Ultra-Rápido (Solo 3 pasos)

### Paso 1: API Mínima Viable (40 min)

```bash
# En tu proyecto (debería estar del Bloque 1)
cd mi-primera-api
source venv/bin/activate  # o como activaste tu entorno

# Crear UN SOLO archivo: main.py
cat > main.py << 'EOF'
from fastapi import FastAPI

# Crear la aplicación (lo más simple posible)
app = FastAPI(title="Mi Primera API")

# Endpoint 1: Hello World (OBLIGATORIO)
@app.get("/")
def hola_mundo():
    return {"mensaje": "¡Mi primera API FastAPI!"}

# Endpoint 2: Info básica (OBLIGATORIO)
@app.get("/info")
def info():
    return {"api": "FastAPI", "semana": 1, "status": "funcionando"}
EOF

# Ejecutar la API (comando simple)
uvicorn main:app --reload
```

**🔍 Verificación Básica (10 min):**

1. Abre http://127.0.0.1:8000 → Deberías ver el JSON con "Mi primera API FastAPI"
2. Abre http://127.0.0.1:8000/info → Deberías ver info de tu API

**✅ Si ves JSON en ambas URLs: ¡ÉXITO!**

### Paso 2: Documentación Automática (30 min)

```bash
# Tu API ya incluye documentación automática
# Solo necesitas verla:

# 1. Abrir en browser (más importante)
# http://127.0.0.1:8000/docs

# 2. Probar los endpoints desde la interfaz
# Clic en GET / → Try it out → Execute
# Clic en GET /info → Try it out → Execute
```

**🎯 Objetivo**: Entender que FastAPI genera documentación automáticamente

### Paso 3: Personalización Mínima (40 min)

Solo si todo está funcionando, vamos a personalizar UN POCO:

```python
# Actualizar main.py (agregar solo al final)
from fastapi import FastAPI

app = FastAPI(title="Mi Primera API")

@app.get("/")
def hola_mundo():
    return {"mensaje": "¡Mi primera API FastAPI!"}

@app.get("/info")
def info():
    return {"api": "FastAPI", "semana": 1, "status": "funcionando"}

# NUEVO: Endpoint personalizado (solo si hay tiempo)
@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"saludo": f"¡Hola {nombre}!"}
```

**🔍 Verificación**: http://127.0.0.1:8000/saludo/TuNombre

## ✅ Criterios de Éxito (Solo estos 3)

1. **✅ API ejecutándose**: http://127.0.0.1:8000 responde JSON
2. **✅ Documentación visible**: http://127.0.0.1:8000/docs se abre
3. **✅ Endpoint funcional**: Al menos uno de los endpoints responde

## 🚨 Si algo no funciona

**NO te compliques**. Llama al instructor inmediatamente. El objetivo es que TODOS tengan una API funcionando al final del Bloque 2.

## 📝 Reflexión (Solo 1 pregunta)

**¿Qué fue lo más sorprendente de crear tu primera API?**

Anota una respuesta de 2-3 oraciones para incluir en tu README.

---

## 🎯 Resultado Final Esperado

Al final de estos 120 minutos tendrás:

- ✅ API FastAPI funcionando
- ✅ 2-3 endpoints básicos
- ✅ Documentación automática accesible
- ✅ Código listo para subir a GitHub
- ✅ Confianza para continuar en Semana 2

**¡Felicidades por tu primera API! 🎉**

---

## 📋 Para el Bloque 3 (Práctica)

Con esta API funcionando, en el Bloque 3 (90 min) harás:

1. **Ejercicios básicos** con tu API
2. **Subir a GitHub** (paso a paso)
3. **Crear README** ultra-básico
4. **Verificar que todo funciona**

**Guarda este archivo main.py - lo necesitaremos en el Bloque 3**
