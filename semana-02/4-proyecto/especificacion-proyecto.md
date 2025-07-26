# Proyecto Semana 2: Sistema de Gestión de Tareas

## 🎯 Objetivo del Proyecto

Desarrollar una **API de gestión de tareas** que demuestre todos los conceptos aprendidos en la Semana 2: type hints, Pydantic, async/await, y endpoints FastAPI avanzados.

## 📋 Especificaciones Funcionales

### **Entidades del Sistema:**

1. **User**: Gestión de usuarios del sistema
2. **Project**: Agrupación de tareas relacionadas
3. **Task**: Elementos de trabajo individuales
4. **Comment**: Notas y actualizaciones en tareas

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

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class UserType(str, Enum):
    admin = "admin"
    manager = "manager"
    developer = "developer"
    viewer = "viewer"

# Modelo base para User
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    type: UserType
    active: bool = True

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")

class UserResponse(UserBase):
    id: int
    registration_date: datetime
    last_access: Optional[datetime] = None

# Modelo base para Project
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    start_date: date
    due_date: Optional[date] = None
    manager_id: int = Field(..., ge=1)

    @validator('due_date')
    def validate_due_date(cls, v, values):
        if v and values.get('start_date'):
            if v <= values['start_date']:
                raise ValueError('Due date must be after start date')
        return v

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    creation_date: datetime
    total_tasks: int = 0
    completed_tasks: int = 0

# Modelo base para Task
class TaskBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.pending
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[date] = None
    project_id: int = Field(..., ge=1)
    assigned_to: Optional[int] = Field(None, ge=1)
    estimated_hours: Optional[float] = Field(None, ge=0.1, le=1000)

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    creation_date: datetime
    update_date: datetime
    created_by: int

# Modelo para Comment
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)
    task_id: int = Field(..., ge=1)

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    creation_date: datetime
    author_id: int
    author_name: str
```

### **2. Endpoints Requeridos**

#### **Users (`/users`)**

```python
# CRUD básico
POST   /users                    # Crear usuario
GET    /users                    # Listar usuarios
GET    /users/{user_id}          # Obtener usuario específico
PUT    /users/{user_id}          # Actualizar usuario completo
PATCH  /users/{user_id}          # Actualizar usuario parcial
DELETE /users/{user_id}          # Desactivar usuario (soft delete)

# Endpoints adicionales
GET    /users/search            # Buscar por nombre/email
GET    /users/{user_id}/tasks  # Tareas asignadas al usuario
PATCH  /users/{user_id}/last-access  # Actualizar último acceso
```

#### **Projects (`/projects`)**

```python
# CRUD básico
POST   /projects                  # Crear proyecto
GET    /projects                  # Listar proyectos
GET    /projects/{project_id}    # Obtener proyecto específico
PUT    /projects/{project_id}    # Actualizar proyecto completo
DELETE /projects/{project_id}    # Eliminar proyecto

# Endpoints adicionales
GET    /projects/search          # Buscar proyectos
GET    /projects/{project_id}/tasks    # Tareas del proyecto
GET    /projects/{project_id}/statistics  # Stats del proyecto
```

#### **Tasks (`/tasks`)**

```python
# CRUD básico
POST   /tasks                     # Crear tarea
GET    /tasks                     # Listar tareas con filtros
GET    /tasks/{task_id}          # Obtener tarea específica
PUT    /tasks/{task_id}          # Actualizar tarea completa
PATCH  /tasks/{task_id}          # Actualizar tarea parcial
DELETE /tasks/{task_id}          # Eliminar tarea

# Endpoints adicionales
GET    /tasks/search             # Búsqueda avanzada
PATCH  /tasks/{task_id}/status  # Cambiar solo estado
PATCH  /tasks/{task_id}/assign # Asignar/reasignar tarea
GET    /tasks/statistics       # Estadísticas generales
```

#### **Comments (`/comments`)**

```python
POST   /comments               # Crear comentario
GET    /comments/task/{task_id}  # Comentarios de una tarea
PUT    /comments/{comment_id}   # Actualizar comentario
DELETE /comments/{comment_id}   # Eliminar comentario
```

### **3. Funcionalidades Async Requeridas**

Implementar estos endpoints como **async** para simular operaciones lentas:

```python
# Simular validación externa de email
async def validate_external_email(email: str) -> bool:
    await asyncio.sleep(0.5)  # Simular latencia API externa
    return "@" in email and "." in email

# Simular notificación por email
async def send_notification(user_id: int, message: str) -> bool:
    await asyncio.sleep(0.3)  # Simular envío
    return True

# Simular backup de datos
async def backup_project(project_id: int) -> dict:
    await asyncio.sleep(1)  # Simular proceso de backup
    return {"backup_id": f"bk_{project_id}_{datetime.now().timestamp()}"}

# Endpoints async requeridos:
@app.post("/users", response_model=UserResponse)
async def create_user_async(user: UserCreate):
    # Validar email externamente
    email_valid = await validate_external_email(user.email)
    # Crear usuario y enviar notificación en paralelo
    pass

@app.patch("/tasks/{task_id}/status")
async def change_task_status_async(task_id: int, new_status: TaskStatus):
    # Cambiar estado y notificar a usuarios relevantes en paralelo
    pass

@app.delete("/projects/{project_id}")
async def delete_project_async(project_id: int):
    # Hacer backup antes de eliminar
    pass
```

### **4. Filtros y Búsquedas Avanzadas**

```python
# Ejemplo para tasks
@app.get("/tasks/search", response_model=List[TaskResponse])
async def search_tasks(
    title: Optional[str] = Query(None, min_length=1),
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    project_id: Optional[int] = Query(None, ge=1),
    assigned_to: Optional[int] = Query(None, ge=1),
    due_date_from: Optional[date] = None,
    due_date_to: Optional[date] = None,
    # Paginación
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    # Ordenamiento
    order_by: str = Query("creation_date", regex="^(title|creation_date|due_date|priority)$"),
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
mkdir task-management-week2
cd task-management-week2

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

- Implementar CRUD para users
- Implementar CRUD para projects
- Implementar CRUD para tasks
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

- GET /users - Listar usuarios
- POST /tasks - Crear tarea
- GET /tasks/search - Búsqueda avanzada

## Ejemplos de Uso

\`\`\`bash

# Crear usuario

curl -X POST "http://localhost:8000/users" \
 -H "Content-Type: application/json" \
 -d '{"name": "Juan", "email": "juan@example.com", "type": "developer", "password": "12345678"}'
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
