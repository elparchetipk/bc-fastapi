# Práctica 2: Primera API FastAPI - Versión Simplificada

## 🎯 Objetivo

Crear tu primera API FastAPI funcional en 150 minutos, enfocándonos en la experiencia exitosa inmediata.

## ⏱️ Tiempo Estimado: 150 minutos (incluye buffer generoso)

## 📋 Pre-requisitos

- ✅ Entorno configurado (Práctica 1)
- ✅ Python + FastAPI + Uvicorn instalados
- ✅ Entorno virtual activo

## 🚀 Desarrollo Rápido (4 pasos)

### Paso 1: Crear API Básica (30 min)

```bash
# Asegúrate de estar en tu proyecto
cd mi-primera-api
source venv/bin/activate

# Crear archivo main.py
cat > main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI(
    title="Mi Primera API",
    description="API creada en el Bootcamp FastAPI - Semana 1",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola desde FastAPI!", "status": "funcionando"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}
EOF

# Ejecutar la API
uvicorn main:app --reload
```

**🔍 Verificación (5 min):**

1. Abre http://127.0.0.1:8000 → Verifica el JSON
2. Abre http://127.0.0.1:8000/health → Verifica el health check
3. Abre http://127.0.0.1:8000/docs → ¡Esta es la magia de FastAPI!

### Paso 2: Agregar Endpoints Útiles (45 min)

```python
# Actualizar main.py
from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Dict, Any

app = FastAPI(
    title="Mi Primera API",
    description="API creada en el Bootcamp FastAPI - Semana 1",
    version="1.0.0"
)

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
```

**🔍 Pruebas (10 min):**

- http://127.0.0.1:8000/saludo/Juan
- http://127.0.0.1:8000/info
- Revisa la documentación en /docs

### Paso 3: Datos con POST (45 min)

```python
# Agregar al main.py (después de los imports)
from pydantic import BaseModel

# Modelo para recibir datos
class Persona(BaseModel):
    nombre: str
    edad: int
    email: str = None

# Almacenamiento temporal (en memoria)
personas = []

# Agregar estos endpoints después de los existentes

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
```

**🔍 Pruebas (10 min):**

1. Ve a http://127.0.0.1:8000/docs
2. Prueba el endpoint POST /personas con:
   ```json
   {
     "nombre": "Ana",
     "edad": 25,
     "email": "ana@ejemplo.com"
   }
   ```
3. Verifica GET /personas
4. Prueba GET /personas/1

### Paso 4: Manejo de Errores Básico (30 min)

```python
# Agregar al main.py
from fastapi import HTTPException, status

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
```

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
```

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
