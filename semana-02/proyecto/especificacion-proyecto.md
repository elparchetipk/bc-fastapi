# Proyecto Semana 2: Sistema de Gestión de Tareas

## 🎯 Objetivo del Proyecto

Desarrollar una **API de gestión de tareas** que demuestre todos los conceptos aprendidos en la Semana 2: type hints, Pydantic, async/await, y endpoints FastAPI avanzados.

## 📋 Especificaciones Funcionales

### **Entidades del Sistema:**

1. **Usuario**: Gestión de usuarios del sistema
2. **Proyecto**: Agrupación de tareas relacionadas
3. **Tarea**: Elementos de trabajo individuales
4. **Comentario**: Notas y actualizaciones en tareas

### **Funcionalidades Requeridas:**

- ✅ CRUD completo para todas las entidades
- ✅ Búsqueda y filtros avanzados
- ✅ Validación robusta de datos
- ✅ Operaciones asíncronas donde corresponda
- ✅ API REST siguiendo mejores prácticas

## 🏗️ Especificación Técnica

### **1. Modelos Pydantic Requeridos**

```python
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime, date
from enum import Enum
from typing import Optional, List

class EstadoTarea(str, Enum):
    pendiente = "pendiente"
    en_progreso = "en_progreso"
    completada = "completada"
    cancelada = "cancelada"

class PrioridadTarea(str, Enum):
    baja = "baja"
    media = "media"
    alta = "alta"
    critica = "critica"

class TipoUsuario(str, Enum):
    admin = "admin"
    manager = "manager"
    developer = "developer"
    viewer = "viewer"

# Modelo base para Usuario
class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    tipo: TipoUsuario
    activo: bool = True

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")

class UsuarioResponse(UsuarioBase):
    id: int
    fecha_registro: datetime
    ultimo_acceso: Optional[datetime] = None

# Modelo base para Proyecto
class ProyectoBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=500)
    fecha_inicio: date
    fecha_limite: Optional[date] = None
    manager_id: int = Field(..., ge=1)

    @validator('fecha_limite')
    def validar_fecha_limite(cls, v, values):
        if v and values.get('fecha_inicio'):
            if v <= values['fecha_inicio']:
                raise ValueError('Fecha límite debe ser posterior a fecha de inicio')
        return v

class ProyectoCreate(ProyectoBase):
    pass

class ProyectoResponse(ProyectoBase):
    id: int
    fecha_creacion: datetime
    total_tareas: int = 0
    tareas_completadas: int = 0

# Modelo base para Tarea
class TareaBase(BaseModel):
    titulo: str = Field(..., min_length=5, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=1000)
    estado: EstadoTarea = EstadoTarea.pendiente
    prioridad: PrioridadTarea = PrioridadTarea.media
    fecha_limite: Optional[date] = None
    proyecto_id: int = Field(..., ge=1)
    asignado_a: Optional[int] = Field(None, ge=1)
    estimacion_horas: Optional[float] = Field(None, ge=0.1, le=1000)

class TareaCreate(TareaBase):
    pass

class TareaResponse(TareaBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime
    creado_por: int

# Modelo para Comentario
class ComentarioBase(BaseModel):
    contenido: str = Field(..., min_length=1, max_length=1000)
    tarea_id: int = Field(..., ge=1)

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioResponse(ComentarioBase):
    id: int
    fecha_creacion: datetime
    autor_id: int
    autor_nombre: str
```

### **2. Endpoints Requeridos**

#### **Usuarios (`/usuarios`)**

```python
# CRUD básico
POST   /usuarios                    # Crear usuario
GET    /usuarios                    # Listar usuarios
GET    /usuarios/{user_id}          # Obtener usuario específico
PUT    /usuarios/{user_id}          # Actualizar usuario completo
PATCH  /usuarios/{user_id}          # Actualizar usuario parcial
DELETE /usuarios/{user_id}          # Desactivar usuario (soft delete)

# Endpoints adicionales
GET    /usuarios/buscar            # Buscar por nombre/email
GET    /usuarios/{user_id}/tareas  # Tareas asignadas al usuario
PATCH  /usuarios/{user_id}/ultimo-acceso  # Actualizar último acceso
```

#### **Proyectos (`/proyectos`)**

```python
# CRUD básico
POST   /proyectos                  # Crear proyecto
GET    /proyectos                  # Listar proyectos
GET    /proyectos/{proyecto_id}    # Obtener proyecto específico
PUT    /proyectos/{proyecto_id}    # Actualizar proyecto completo
DELETE /proyectos/{proyecto_id}    # Eliminar proyecto

# Endpoints adicionales
GET    /proyectos/buscar          # Buscar proyectos
GET    /proyectos/{proyecto_id}/tareas    # Tareas del proyecto
GET    /proyectos/{proyecto_id}/estadisticas  # Stats del proyecto
```

#### **Tareas (`/tareas`)**

```python
# CRUD básico
POST   /tareas                     # Crear tarea
GET    /tareas                     # Listar tareas con filtros
GET    /tareas/{tarea_id}          # Obtener tarea específica
PUT    /tareas/{tarea_id}          # Actualizar tarea completa
PATCH  /tareas/{tarea_id}          # Actualizar tarea parcial
DELETE /tareas/{tarea_id}          # Eliminar tarea

# Endpoints adicionales
GET    /tareas/buscar             # Búsqueda avanzada
PATCH  /tareas/{tarea_id}/estado  # Cambiar solo estado
PATCH  /tareas/{tarea_id}/asignar # Asignar/reasignar tarea
GET    /tareas/estadisticas       # Estadísticas generales
```

#### **Comentarios (`/comentarios`)**

```python
POST   /comentarios               # Crear comentario
GET    /comentarios/tarea/{tarea_id}  # Comentarios de una tarea
PUT    /comentarios/{comentario_id}   # Actualizar comentario
DELETE /comentarios/{comentario_id}   # Eliminar comentario
```

### **3. Funcionalidades Async Requeridas**

Implementar estos endpoints como **async** para simular operaciones lentas:

```python
# Simular validación externa de email
async def validar_email_externo(email: str) -> bool:
    await asyncio.sleep(0.5)  # Simular latencia API externa
    return "@" in email and "." in email

# Simular notificación por email
async def enviar_notificacion(usuario_id: int, mensaje: str) -> bool:
    await asyncio.sleep(0.3)  # Simular envío
    return True

# Simular backup de datos
async def backup_proyecto(proyecto_id: int) -> dict:
    await asyncio.sleep(1)  # Simular proceso de backup
    return {"backup_id": f"bk_{proyecto_id}_{datetime.now().timestamp()}"}

# Endpoints async requeridos:
@app.post("/usuarios", response_model=UsuarioResponse)
async def crear_usuario_async(usuario: UsuarioCreate):
    # Validar email externamente
    email_valido = await validar_email_externo(usuario.email)
    # Crear usuario y enviar notificación en paralelo
    pass

@app.patch("/tareas/{tarea_id}/estado")
async def cambiar_estado_tarea_async(tarea_id: int, nuevo_estado: EstadoTarea):
    # Cambiar estado y notificar a usuarios relevantes en paralelo
    pass

@app.delete("/proyectos/{proyecto_id}")
async def eliminar_proyecto_async(proyecto_id: int):
    # Hacer backup antes de eliminar
    pass
```

### **4. Filtros y Búsquedas Avanzadas**

```python
# Ejemplo para tareas
@app.get("/tareas/buscar", response_model=List[TareaResponse])
async def buscar_tareas(
    titulo: Optional[str] = Query(None, min_length=1),
    estado: Optional[EstadoTarea] = None,
    prioridad: Optional[PrioridadTarea] = None,
    proyecto_id: Optional[int] = Query(None, ge=1),
    asignado_a: Optional[int] = Query(None, ge=1),
    fecha_limite_desde: Optional[date] = None,
    fecha_limite_hasta: Optional[date] = None,
    # Paginación
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    # Ordenamiento
    order_by: str = Query("fecha_creacion", regex="^(titulo|fecha_creacion|fecha_limite|prioridad)$"),
    order_dir: str = Query("desc", regex="^(asc|desc)$")
):
    # Implementar lógica de filtrado, ordenamiento y paginación
    pass
```

## 📊 Criterios de Evaluación

### **1. Funcionalidad (40 puntos)**

- ✅ Todos los endpoints implementados y funcionando
- ✅ Validación correcta con Pydantic
- ✅ Filtros y búsquedas operativas
- ✅ Operaciones CRUD completas

### **2. Implementación Técnica (30 puntos)**

- ✅ Type hints en 95% del código
- ✅ Uso correcto de async/await (mínimo 3 endpoints)
- ✅ Modelos Pydantic bien diseñados
- ✅ Status codes HTTP apropiados

### **3. Calidad del Código (20 puntos)**

- ✅ Código limpio y bien estructurado
- ✅ Nombres de variables descriptivos
- ✅ Comentarios donde sea necesario
- ✅ Separación de responsabilidades

### **4. Documentación (10 puntos)**

- ✅ README con instrucciones claras
- ✅ Documentación automática rica en `/docs`
- ✅ Ejemplos de uso básicos
- ✅ Descripción de decisiones técnicas

## 🚀 Guía de Implementación

### **Paso 1: Setup del Proyecto (30 min)**

```bash
# Crear estructura
mkdir proyecto-tareas-semana2
cd proyecto-tareas-semana2

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install "fastapi[all]" uvicorn python-multipart

# Crear archivos base
touch main.py models.py README.md
```

### **Paso 2: Modelos Pydantic (45 min)**

- Implementar todos los modelos base
- Agregar validaciones custom
- Probar modelos con datos de ejemplo

### **Paso 3: Endpoints Básicos (60 min)**

- Implementar CRUD para usuarios
- Implementar CRUD para proyectos
- Implementar CRUD para tareas
- Probar con datos básicos

### **Paso 4: Funcionalidades Avanzadas (45 min)**

- Agregar filtros y búsquedas
- Implementar endpoints async
- Agregar validaciones cruzadas
- Implementar comentarios

### **Paso 5: Testing y Documentación (30 min)**

- Probar todos los endpoints
- Crear README completo
- Verificar documentación automática
- Testing básico (opcional)

## 📝 Entregables

### **Archivos Requeridos:**

1. **`main.py`** - API principal con todos los endpoints
2. **`models.py`** - Modelos Pydantic separados (opcional)
3. **`README.md`** - Documentación del proyecto
4. **`requirements.txt`** - Dependencias del proyecto

### **Formato de Entrega:**

- **Repositorio GitHub** con código fuente
- **Video demo** (5-7 minutos) mostrando funcionalidades
- **Archivo de pruebas** (Postman collection o script Python)

### **Ejemplo de README:**

```markdown
# Sistema de Gestión de Tareas - Semana 2

## Descripción

API REST para gestión de tareas, proyectos y usuarios desarrollada con FastAPI.

## Características

- ✅ CRUD completo para usuarios, proyectos y tareas
- ✅ Validación robusta con Pydantic
- ✅ Operaciones asíncronas
- ✅ Búsqueda y filtros avanzados

## Instalación

\`\`\`bash
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

## Endpoints Principales

- GET /usuarios - Listar usuarios
- POST /tareas - Crear tarea
- GET /tareas/buscar - Búsqueda avanzada

## Ejemplos de Uso

\`\`\`bash

# Crear usuario

curl -X POST "http://localhost:8000/usuarios" \
 -H "Content-Type: application/json" \
 -d '{"nombre": "Juan", "email": "juan@ejemplo.com", "tipo": "developer", "password": "12345678"}'
\`\`\`

## Decisiones Técnicas

- Async/await para operaciones que simulan I/O
- Soft delete para usuarios (mantener integridad referencial)
- Paginación por defecto en listados
```

## 🎯 Consejos para el Éxito

1. **Empieza simple**: Implementa un endpoint a la vez
2. **Prueba constantemente**: Usa `/docs` para verificar funcionalidad
3. **Organiza el código**: Separa modelos si el archivo crece mucho
4. **Documenta decisiones**: Explica por qué elegiste async vs sync
5. **Valida datos**: Usa Pydantic al máximo para validación robusta

## 🏆 Oportunidades de Bonus

- **+5 puntos**: Implementar soft delete consistente
- **+5 puntos**: Middleware para logging de requests
- **+5 puntos**: Validación de permisos básica (admin puede todo, developer solo sus tareas)
- **+10 puntos**: Testing automatizado con pytest
- **+10 puntos**: Exportación de datos (CSV, JSON)

---

**🎯 Objetivo**: Demostrar dominio de todos los conceptos de la Semana 2 en un proyecto práctico y realista.
