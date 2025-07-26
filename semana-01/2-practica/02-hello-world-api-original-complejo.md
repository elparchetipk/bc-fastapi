# Práctica 2: Primera API FastAPI - Ultra Simplificada

## 🎯 Objetivo Ultra-Básico

Crear tu primera API FastAPI funcional en **120 minutos** (después del break de 30 min), enfocándonos únicamente en que **funcione**.

## ⏱️ Tiempo: 120 minutos (Bloque 2 post-break)

> **🔄 AJUSTE APLICADO**: Esta práctica ha sido ultra-simplificada para garantizar éxito en el tiempo asignado.

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

3. Abre http://127.0.0.1:8000/docs → ¡Esta es la magia de FastAPI!

### Paso 2: Agregar Endpoints Útiles (45 min)

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
resultado = num1 / num2
return {
"operacion": f"{num1} / {num2}",
"resultado": resultado,
"timestamp": datetime.now().isoformat()
}

@app.delete("/personas/{persona_id}")
def eliminar_persona(persona_id: int):
for i, persona in enumerate(personas):
if persona["id"] == persona_id:
persona_eliminada = personas.pop(i)
return {
"mensaje": "Persona eliminada exitosamente",
"persona": persona_eliminada
}
raise HTTPException(
status_code=status.HTTP_404_NOT_FOUND,
detail=f"Persona con ID {persona_id} no encontrada"
)

````

**🔍 Pruebas de errores (10 min):**

- http://127.0.0.1:8000/division/10/0 (debe dar error)
- http://127.0.0.1:8000/division/10/2 (debe funcionar)
- DELETE /personas/999 en /docs (debe dar error 404)

## ✅ Archivo Final Completo

Tu `main.py` final debe verse así:

```python
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from typing import Dict, Any, List

app = FastAPI(
    title="Mi Primera API",
    description="API creada en el Bootcamp FastAPI - Semana 1",
    version="1.0.0"
)

# Modelo para recibir datos
class Persona(BaseModel):
    nombre: str
    edad: int
    email: str = None

# Almacenamiento temporal (en memoria)
personas = []

@app.get("/")
def read_root():
    return {
        "mensaje": "¡Hola desde FastAPI!",
        "timestamp": datetime.now().isoformat(),
        "status": "funcionando"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/saludo/{nombre}")
def saludar_persona(nombre: str):
    return {
        "mensaje": f"¡Hola {nombre}!",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/info")
def obtener_info():
    return {
        "api": "Mi Primera API FastAPI",
        "creador": "Estudiante Bootcamp",
        "semana": 1,
        "tecnologias": ["Python", "FastAPI", "Uvicorn"],
        "timestamp": datetime.now().isoformat()
    }

@app.post("/personas")
def crear_persona(persona: Persona):
    persona_dict = persona.dict()
    persona_dict["id"] = len(personas) + 1
    persona_dict["timestamp"] = datetime.now().isoformat()
    personas.append(persona_dict)
    return {
        "mensaje": "Persona creada exitosamente",
        "persona": persona_dict
    }

@app.get("/personas")
def listar_personas():
    return {
        "total": len(personas),
        "personas": personas
    }

@app.get("/personas/{persona_id}")
def obtener_persona(persona_id: int):
    for persona in personas:
        if persona["id"] == persona_id:
            return persona
    raise HTTPException(status_code=404, detail="Persona no encontrada")

@app.delete("/personas/{persona_id}")
def eliminar_persona(persona_id: int):
    for i, persona in enumerate(personas):
        if persona["id"] == persona_id:
            persona_eliminada = personas.pop(i)
            return {
                "mensaje": "Persona eliminada exitosamente",
                "persona": persona_eliminada
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Persona con ID {persona_id} no encontrada"
    )

@app.get("/division/{num1}/{num2}")
def dividir_numeros(num1: float, num2: float):
    if num2 == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede dividir por cero"
        )
    resultado = num1 / num2
    return {
        "operacion": f"{num1} / {num2}",
        "resultado": resultado,
        "timestamp": datetime.now().isoformat()
    }
````

## 🎯 Objetivos Logrados

Al finalizar esta práctica, habrás creado una API que:

- ✅ **Responde en múltiples endpoints**
- ✅ **Maneja parámetros de ruta y cuerpo**
- ✅ **Valida datos con Pydantic**
- ✅ **Genera documentación automática**
- ✅ **Maneja errores apropiadamente**
- ✅ **Funciona como base para proyectos reales**

## 🔄 Próximos Pasos

1. **Inmediato**: Experimenta creando nuevos endpoints
2. **Semana 2**: Aprenderemos persistencia de datos
3. **Semana 3**: Conectaremos a bases de datos reales

## 🆘 Problemas Comunes

### Error: "Module 'pydantic' has no attribute 'BaseModel'"

```bash
# Reinstalar pydantic
pip install --upgrade pydantic
```

### Error: Puerto 8000 ocupado

```bash
# Usar puerto diferente
uvicorn main:app --reload --port 8001
```

### API no recarga automáticamente

```bash
# Verificar flag --reload
uvicorn main:app --reload
```

## 📝 Entregable

Al final de la clase:

1. **Archivo `main.py` funcionando**
2. **API ejecutándose en tu máquina**
3. **Captura de pantalla de /docs**
4. **Commit en Git con el código**

**Comando para commit:**

```bash
git add main.py
git commit -m "feat: primera API FastAPI funcionando

- Endpoints básicos implementados
- Validación con Pydantic
- Manejo de errores básico
- Documentación automática activa"
```

---

**💡 Tip**: Esta API es tu primera victoria. En 150 minutos, has creado algo que demuestra el poder de FastAPI. ¡Celebra este logro antes de continuar!
