# Práctica 4: FastAPI Intermedio - Semana 2

## 🎯 Objetivo

Expandir la API de Semana 1 con características intermedias de FastAPI, construyendo sobre los modelos Pydantic del bloque anterior.

## ⏱️ Tiempo Estimado: 90 minutos

## 📋 Pre-requisitos

- ✅ API de Semana 1 funcionando
- ✅ Modelos Pydantic implementados (bloque anterior)
- ✅ Conocimiento básico de HTTP methods

## 🔄 Continuando desde la API Anterior

Vamos a expandir la API que ya tienes con métodos HTTP adicionales y características avanzadas:

## 🚀 Paso 1: Métodos HTTP Completos (25 min)

Agregar operaciones CRUD completas a tu `main.py`:

```python
# Importaciones adicionales
from fastapi import FastAPI, HTTPException, status, Query, Path, Body
from typing import Optional, List, Dict, Any

# Modelo para actualización parcial
class PersonaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=50)
    edad: Optional[int] = Field(None, ge=18, le=120)
    email: Optional[EmailStr] = None
    categoria: Optional[CategoriaPersona] = None
    activo: Optional[bool] = None

# PUT - Actualización completa
@app.put("/personas/{persona_id}", response_model=PersonaResponse)
def actualizar_persona_completa(
    persona_id: int = Path(..., ge=1, description="ID de la persona"),
    persona_nueva: PersonaCreate = Body(..., description="Datos completos de la persona")
):
    """Actualizar todos los datos de una persona"""
    # Buscar persona existente
    for i, persona in enumerate(personas):
        if persona.id == persona_id:
            # Crear nueva instancia con ID y timestamp preservados
            persona_actualizada = PersonaResponse(
                id=persona.id,
                timestamp=persona.timestamp,
                **persona_nueva.dict()
            )
            personas[i] = persona_actualizada
            return persona_actualizada

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Persona con ID {persona_id} no encontrada"
    )

# PATCH - Actualización parcial
@app.patch("/personas/{persona_id}", response_model=PersonaResponse)
def actualizar_persona_parcial(
    persona_id: int = Path(..., ge=1),
    persona_update: PersonaUpdate = Body(...)
):
    """Actualizar solo algunos campos de una persona"""
    for i, persona in enumerate(personas):
        if persona.id == persona_id:
            # Crear diccionario con datos actuales
            datos_actuales = persona.dict()

            # Actualizar solo campos proporcionados
            datos_nuevos = persona_update.dict(exclude_unset=True)
            datos_actuales.update(datos_nuevos)

            # Crear nueva instancia
            persona_actualizada = PersonaResponse(**datos_actuales)
            personas[i] = persona_actualizada
            return persona_actualizada

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Persona con ID {persona_id} no encontrada"
    )

# DELETE - Eliminar
@app.delete("/personas/{persona_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_persona(persona_id: int = Path(..., ge=1)):
    """Eliminar una persona (soft delete)"""
    for i, persona in enumerate(personas):
        if persona.id == persona_id:
            # Soft delete - marcar como inactivo
            persona.activo = False
            return  # 204 No Content no retorna body

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Persona con ID {persona_id} no encontrada"
    )

# DELETE - Eliminar permanentemente
@app.delete("/personas/{persona_id}/permanente")
def eliminar_persona_permanente(persona_id: int = Path(..., ge=1)):
    """Eliminar persona permanentemente"""
    for i, persona in enumerate(personas):
        if persona.id == persona_id:
            persona_eliminada = personas.pop(i)
            return {
                "mensaje": "Persona eliminada permanentemente",
                "persona": persona_eliminada
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Persona con ID {persona_id} no encontrada"
    )
```

## 🔍 Paso 2: Parámetros de Consulta Avanzados (20 min)

```python
# Endpoint con múltiples parámetros de consulta
@app.get("/personas/buscar", response_model=List[PersonaResponse])
def buscar_personas(
    # Parámetros de filtro
    nombre: Optional[str] = Query(None, min_length=2, description="Buscar por nombre"),
    categoria: Optional[CategoriaPersona] = Query(None, description="Filtrar por categoría"),
    edad_min: Optional[int] = Query(None, ge=18, description="Edad mínima"),
    edad_max: Optional[int] = Query(None, le=120, description="Edad máxima"),
    activo: bool = Query(True, description="Filtrar por estado activo"),

    # Parámetros de paginación
    page: int = Query(1, ge=1, description="Número de página"),
    size: int = Query(10, ge=1, le=100, description="Elementos por página"),

    # Parámetros de ordenamiento
    order_by: str = Query("id", regex="^(id|nombre|edad|categoria)$", description="Campo para ordenar"),
    order_direction: str = Query("asc", regex="^(asc|desc)$", description="Dirección del ordenamiento")
):
    """Búsqueda avanzada de personas con filtros, paginación y ordenamiento"""

    # Aplicar filtros
    resultado = [p for p in personas if p.activo == activo]

    if nombre:
        resultado = [p for p in resultado if nombre.lower() in p.nombre.lower()]

    if categoria:
        resultado = [p for p in resultado if p.categoria == categoria]

    if edad_min is not None:
        resultado = [p for p in resultado if p.edad >= edad_min]

    if edad_max is not None:
        resultado = [p for p in resultado if p.edad <= edad_max]

    # Ordenamiento
    reverse = order_direction == "desc"
    resultado.sort(key=lambda x: getattr(x, order_by), reverse=reverse)

    # Paginación
    total = len(resultado)
    inicio = (page - 1) * size
    fin = inicio + size
    resultado_paginado = resultado[inicio:fin]

    # Agregar metadata de paginación en headers (buena práctica)
    return resultado_paginado

# Endpoint de estadísticas
@app.get("/personas/estadisticas")
def obtener_estadisticas_personas():
    """Obtener estadísticas de personas"""
    if not personas:
        return {"mensaje": "No hay personas registradas"}

    # Calcular estadísticas
    activas = [p for p in personas if p.activo]
    por_categoria = {}
    edades = [p.edad for p in activas]

    for categoria in CategoriaPersona:
        por_categoria[categoria.value] = len([p for p in activas if p.categoria == categoria])

    return {
        "total_personas": len(personas),
        "personas_activas": len(activas),
        "personas_inactivas": len(personas) - len(activas),
        "por_categoria": por_categoria,
        "edad_promedio": round(sum(edades) / len(edades), 1) if edades else 0,
        "edad_minima": min(edades) if edades else 0,
        "edad_maxima": max(edades) if edades else 0
    }
```

## 📊 Paso 3: Response Models y Status Codes (20 min)

```python
# Modelos de respuesta especializados
class PersonaResumen(BaseModel):
    """Modelo resumido para listados"""
    id: int
    nombre: str
    categoria: CategoriaPersona
    activo: bool

class OperacionExitosa(BaseModel):
    """Modelo para operaciones exitosas"""
    success: bool = True
    mensaje: str
    data: Optional[Dict[str, Any]] = None

class ErrorDetalle(BaseModel):
    """Modelo para errores detallados"""
    error: str
    detalle: str
    codigo: int
    timestamp: datetime = Field(default_factory=datetime.now)

# Endpoint con múltiples response models
@app.get("/personas/resumen",
         response_model=List[PersonaResumen],
         responses={
             200: {"description": "Lista de personas resumida"},
             404: {"model": ErrorDetalle, "description": "No se encontraron personas"}
         })
def obtener_resumen_personas():
    """Obtener resumen de todas las personas activas"""
    activas = [p for p in personas if p.activo]

    if not activas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron personas activas"
        )

    return [PersonaResumen(**p.dict()) for p in activas]

# Endpoint con respuesta customizada
@app.post("/personas/batch",
          response_model=OperacionExitosa,
          status_code=status.HTTP_201_CREATED)
def crear_personas_lote(personas_nuevas: List[PersonaCreate]):
    """Crear múltiples personas en una operación"""
    if len(personas_nuevas) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se pueden crear más de 10 personas por lote"
        )

    personas_creadas = []
    for persona_data in personas_nuevas:
        # Verificar email único
        if any(p.email == persona_data.email for p in personas):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Email {persona_data.email} ya existe"
            )

        nueva_persona = PersonaResponse(
            id=len(personas) + len(personas_creadas) + 1,
            timestamp=datetime.now(),
            **persona_data.dict()
        )
        personas_creadas.append(nueva_persona)

    # Agregar todas las personas
    personas.extend(personas_creadas)

    return OperacionExitosa(
        mensaje=f"Se crearon {len(personas_creadas)} personas exitosamente",
        data={"personas_creadas": len(personas_creadas)}
    )
```

## 🔧 Paso 4: Middleware y Headers Custom (15 min)

```python
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
import time

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, ser más específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware custom para timing
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Agregar header con tiempo de procesamiento"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(round(process_time, 4))
    return response

# Endpoint con headers custom
@app.get("/health/detailed")
def health_check_detailed():
    """Health check con información detallada"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat(),
        "total_personas": len(personas),
        "personas_activas": len([p for p in personas if p.activo]),
        "memoria_usada_mb": "N/A"  # En producción, usar psutil
    }
```

## 🧪 Paso 5: Testing de Endpoints (10 min)

Crear script de testing rápido:

```python
# test_endpoints.py
import requests
import json

BASE_URL = "http://localhost:8000"

def test_crud_completo():
    """Test del flujo CRUD completo"""
    print("🧪 Testing CRUD completo...")

    # 1. Crear persona
    nueva_persona = {
        "nombre": "María Test",
        "edad": 30,
        "email": "maria.test@ejemplo.com",
        "categoria": "estudiante"
    }

    response = requests.post(f"{BASE_URL}/personas", json=nueva_persona)
    assert response.status_code == 201
    persona_creada = response.json()
    persona_id = persona_creada["id"]
    print(f"✅ Persona creada con ID {persona_id}")

    # 2. Leer persona
    response = requests.get(f"{BASE_URL}/personas/{persona_id}")
    assert response.status_code == 200
    print("✅ Persona leída correctamente")

    # 3. Actualizar persona (PATCH)
    update_data = {"edad": 31}
    response = requests.patch(f"{BASE_URL}/personas/{persona_id}", json=update_data)
    assert response.status_code == 200
    persona_actualizada = response.json()
    assert persona_actualizada["edad"] == 31
    print("✅ Persona actualizada con PATCH")

    # 4. Buscar personas
    response = requests.get(f"{BASE_URL}/personas/buscar?nombre=María")
    assert response.status_code == 200
    resultados = response.json()
    assert len(resultados) >= 1
    print("✅ Búsqueda funcionando")

    # 5. Eliminar persona (soft delete)
    response = requests.delete(f"{BASE_URL}/personas/{persona_id}")
    assert response.status_code == 204
    print("✅ Soft delete funcionando")

    print("🎉 Todos los tests pasaron!")

if __name__ == "__main__":
    test_crud_completo()
```

## 🎯 Objetivos Logrados

Al finalizar esta práctica, habrás implementado:

- ✅ **CRUD completo** (Create, Read, Update, Delete)
- ✅ **Múltiples métodos HTTP** (GET, POST, PUT, PATCH, DELETE)
- ✅ **Parámetros de consulta avanzados** con validación
- ✅ **Paginación y ordenamiento** básicos
- ✅ **Response models especializados** según contexto
- ✅ **Status codes apropiados** para cada operación
- ✅ **Middleware custom** para timing y CORS
- ✅ **Testing básico** de endpoints

## 📊 Comparación: Semana 1 vs Semana 2

| Aspecto          | Semana 1             | Semana 2                           |
| ---------------- | -------------------- | ---------------------------------- |
| **Endpoints**    | 4-5 básicos          | 12+ con CRUD completo              |
| **Métodos HTTP** | GET, POST            | GET, POST, PUT, PATCH, DELETE      |
| **Validación**   | Básica               | Avanzada con Pydantic              |
| **Parámetros**   | Simples              | Query params con validación        |
| **Respuestas**   | JSON simple          | Response models + status codes     |
| **Features**     | Funcionalidad básica | Búsqueda, paginación, estadísticas |

## 🔄 Próximos Pasos

1. **Prueba todos los endpoints** con diferentes parámetros
2. **Experimenta con la documentación** en `/docs`
3. **Semana 3**: Conectar a base de datos real
4. **Semana 4**: Añadir autenticación y autorización

## 📝 Entregable de Este Bloque

- **API con CRUD completo** funcionando
- **Al menos 12 endpoints** diferentes
- **Búsqueda y filtros** implementados
- **Testing básico** pasando
- **Documentación actualizada** en `/docs`

---

**💡 Tip**: Tu API ahora tiene características de nivel profesional. ¡La documentación automática en `/docs` se ve increíble con todos estos endpoints!
