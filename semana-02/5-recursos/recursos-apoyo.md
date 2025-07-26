# Recursos de Apoyo - Semana 2

## 📚 Documentación y Referencias

### **Type Hints en Python**

- [Python Type Hints - Documentación Oficial](https://docs.python.org/3/library/typing.html)
- [mypy - Static Type Checker](https://mypy.readthedocs.io/en/stable/)
- [typing_extensions](https://pypi.org/project/typing-extensions/) - Características adicionales

### **Pydantic**

- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/) - Documentación completa
- [Pydantic GitHub](https://github.com/samuelcolvin/pydantic) - Código fuente y ejemplos
- [Pydantic Validators](https://pydantic-docs.helpmanual.io/usage/validators/) - Validadores custom

### **FastAPI**

- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Documentación oficial
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) - Tutorial paso a paso
- [FastAPI Advanced User Guide](https://fastapi.tiangolo.com/advanced/) - Características avanzadas

### **Async/Await en Python**

- [Python asyncio](https://docs.python.org/3/library/asyncio.html) - Documentación oficial
- [Real Python - Async IO](https://realpython.com/async-io-python/) - Tutorial completo
- [httpx](https://www.python-httpx.org/) - Cliente HTTP async

---

## 🛠️ Herramientas Útiles

### **Editores y IDEs**

- **VS Code**: Con extensiones Python, Pylance, REST Client
- **PyCharm**: IDE completo para Python
- **Vim/Neovim**: Con plugins para Python y FastAPI

### **Testing de APIs**

- **Postman**: Interface gráfica para testing
- **httpie**: Cliente HTTP desde línea de comandos
- **curl**: Herramienta básica pero poderosa
- **REST Client**: Extensión de VS Code

### **Validación de Código**

```bash
# Instalar herramientas de desarrollo
pip install mypy black isort flake8

# Verificar tipos
mypy main.py

# Formatear código
black main.py

# Ordenar imports
isort main.py

# Linting
flake8 main.py
```

---

## 📋 Cheat Sheets

### **Type Hints Esenciales**

```python
from typing import List, Dict, Optional, Union, Any, Callable
from datetime import datetime, date

# Tipos básicos
name: str = "Juan"
age: int = 25
price: float = 29.99
active: bool = True

# Colecciones
numbers: List[int] = [1, 2, 3]
config: Dict[str, str] = {"host": "localhost"}
data: Dict[str, Any] = {"name": "Juan", "age": 25}

# Opcionales
email: Optional[str] = None  # Puede ser str o None
result: Union[str, int] = "texto"  # Puede ser str o int

# Funciones
def process(data: List[str]) -> Dict[str, int]:
    return {"total": len(data)}

# Async
async def get_data() -> List[Dict[str, Any]]:
    return [{"id": 1, "name": "test"}]
```

### **Pydantic Patterns**

```python
from pydantic import BaseModel, Field, validator, root_validator
from enum import Enum
from datetime import datetime
from typing import Optional

class Status(str, Enum):
    active = "active"
    inactive = "inactive"

class MyModel(BaseModel):
    # Field con validación
    name: str = Field(..., min_length=2, max_length=50, description="Nombre completo")
    age: int = Field(..., ge=18, le=120, description="Edad en años")
    email: Optional[str] = Field(None, regex=r'^[^@]+@[^@]+\.[^@]+$')
    status: Status = Status.active

    # Validator simple
    @validator('name')
    def normalize_name(cls, v):
        return v.strip().title()

    # Validator con values
    @validator('email')
    def validate_email_status(cls, v, values):
        if values.get('status') == Status.active and not v:
            raise ValueError('Email requerido para usuarios activos')
        return v

    # Root validator
    @root_validator
    def validate_complete_model(cls, values):
        # Validaciones que requieren múltiples campos
        return values

    # Configuración
    class Config:
        use_enum_values = True  # Serializar enums como valores
        validate_assignment = True  # Validar al asignar
        schema_extra = {
            "example": {
                "name": "Juan Pérez",
                "age": 30,
                "email": "juan@example.com",
                "status": "active"
            }
        }
```

### **FastAPI Patterns**

```python
from fastapi import FastAPI, HTTPException, Query, Path, Body, status
from typing import List, Optional

app = FastAPI()

# Endpoint básico
@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int = Path(..., ge=1, description="ID del usuario")):
    # Lógica aquí
    pass

# Query parameters con validación
@app.get("/users", response_model=List[User])
def list_users(
    active: bool = Query(True, description="Filtrar por estado"),
    limit: int = Query(10, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación")
):
    pass

# Request body
@app.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate = Body(..., description="Datos del usuario")):
    pass

# Múltiples response models
@app.get("/users/{user_id}",
         responses={
             200: {"model": User, "description": "Usuario encontrado"},
             404: {"model": ErrorModel, "description": "Usuario no encontrado"}
         })
def get_complete_user(user_id: int):
    pass

# Async endpoint
@app.get("/users/{user_id}/external")
async def get_external_data(user_id: int):
    # Operaciones async aquí
    result = await external_call(user_id)
    return result
```

### **Async/Await Patterns**

```python
import asyncio
import httpx
from typing import List

# Función async básica
async def slow_operation():
    await asyncio.sleep(1)
    return "completed"

# Multiple operaciones en paralelo
async def process_batch(items: List[str]):
    tasks = [process_item(item) for item in items]
    results = await asyncio.gather(*tasks)
    return results

# HTTP client async
async def external_api_call(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

# Con timeout
async def operation_with_timeout():
    try:
        result = await asyncio.wait_for(
            slow_operation(),
            timeout=5.0
        )
        return result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Timeout")

# Semáforo para limitar concurrencia
semaphore = asyncio.Semaphore(3)

async def limited_operation():
    async with semaphore:
        await slow_operation()
        return "completed"
```

---

## 🔧 Scripts Útiles

### **Script de Testing Básico**

```python
#!/usr/bin/env python3
"""
Script para probar endpoints de la API
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_user_crud():
    """Test completo de CRUD de usuarios"""
    print("🧪 Testing CRUD de usuarios...")

    # 1. Crear usuario
    new_user = {
        "name": "Test User",
        "email": "test@example.com",
        "type": "developer",
        "password": "12345678"
    }

    response = requests.post(f"{BASE_URL}/users", json=new_user)
    assert response.status_code == 201, f"Error creando usuario: {response.text}"
    user = response.json()
    user_id = user["id"]
    print(f"✅ Usuario creado con ID {user_id}")

    # 2. Obtener usuario
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200, f"Error obteniendo usuario: {response.text}"
    print("✅ Usuario obtenido correctamente")

    # 3. Actualizar usuario
    update_data = {"name": "Test User Updated"}
    response = requests.patch(f"{BASE_URL}/users/{user_id}", json=update_data)
    assert response.status_code == 200, f"Error actualizando usuario: {response.text}"
    print("✅ Usuario actualizado correctamente")

    # 4. Listar usuarios
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200, f"Error listando usuarios: {response.text}"
    users = response.json()
    assert len(users) > 0, "No se encontraron usuarios"
    print(f"✅ Lista de usuarios obtenida: {len(users)} usuarios")

    print("🎉 Test CRUD usuarios completado!")

if __name__ == "__main__":
    test_user_crud()
```

### **Script de Población de Datos**

```python
#!/usr/bin/env python3
"""
Script para poblar la API con datos de ejemplo
"""
import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000"

def populate_data():
    """Poblar API con datos de ejemplo"""
    print("📊 Poblando datos de ejemplo...")

    # Usuarios
    users = [
        {"name": "Admin User", "email": "admin@company.com", "type": "admin", "password": "admin123"},
        {"name": "Manager Test", "email": "manager@company.com", "type": "manager", "password": "manager123"},
        {"name": "Dev Frontend", "email": "frontend@company.com", "type": "developer", "password": "dev123"},
        {"name": "Dev Backend", "email": "backend@company.com", "type": "developer", "password": "dev123"},
        {"name": "QA Tester", "email": "qa@company.com", "type": "viewer", "password": "qa123"},
    ]

    user_ids = []
    for user in users:
        response = requests.post(f"{BASE_URL}/users", json=user)
        if response.status_code == 201:
            user_ids.append(response.json()["id"])
            print(f"✅ Usuario creado: {user['name']}")

    # Proyectos
    projects = [
        {
            "name": "Web System",
            "description": "Desarrollo del sistema web principal",
            "start_date": str(date.today()),
            "due_date": str(date.today() + timedelta(days=90)),
            "manager_id": user_ids[1] if len(user_ids) > 1 else 1
        },
        {
            "name": "Mobile App",
            "description": "Aplicación móvil complementaria",
            "start_date": str(date.today()),
            "due_date": str(date.today() + timedelta(days=60)),
            "manager_id": user_ids[1] if len(user_ids) > 1 else 1
        }
    ]

    project_ids = []
    for project in projects:
        response = requests.post(f"{BASE_URL}/projects", json=project)
        if response.status_code == 201:
            project_ids.append(response.json()["id"])
            print(f"✅ Proyecto creado: {project['name']}")

    # Tareas
    tasks = [
        {
            "title": "Configure development environment",
            "description": "Configurar Docker y dependencias",
            "status": "completed",
            "priority": "high",
            "project_id": project_ids[0] if project_ids else 1,
            "assigned_to": user_ids[2] if len(user_ids) > 2 else 1,
            "estimated_hours": 8.0
        },
        {
            "title": "Design database",
            "description": "Crear schema de la base de datos",
            "status": "in_progress",
            "priority": "high",
            "project_id": project_ids[0] if project_ids else 1,
            "assigned_to": user_ids[3] if len(user_ids) > 3 else 1,
            "estimated_hours": 16.0
        },
        {
            "title": "Implement authentication",
            "description": "Sistema de login y registro",
            "status": "pending",
            "priority": "medium",
            "project_id": project_ids[0] if project_ids else 1,
            "assigned_to": user_ids[3] if len(user_ids) > 3 else 1,
            "estimated_hours": 20.0
        }
    ]

    for task in tasks:
        response = requests.post(f"{BASE_URL}/tasks", json=task)
        if response.status_code == 201:
            print(f"✅ Tarea creada: {task['title']}")

    print("🎉 Datos de ejemplo creados exitosamente!")

if __name__ == "__main__":
    populate_data()
```

---

## 📖 Ejemplos de Código Adicionales

### **Middleware Custom**

```python
from fastapi import Request
import time
import logging

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware para logging de requests"""
    start_time = time.time()

    # Log del request
    logging.info(f"Request: {request.method} {request.url}")

    response = await call_next(request)

    # Log del response
    process_time = time.time() - start_time
    logging.info(f"Response: {response.status_code} - {process_time:.4f}s")

    # Agregar header con tiempo
    response.headers["X-Process-Time"] = str(process_time)

    return response
```

### **Manejo Global de Errores**

```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "message": "Los datos proporcionados no son válidos",
            "details": exc.errors()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": f"HTTP {exc.status_code}",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )
```

---

## 🔗 Enlaces Adicionales

### **Tutoriales y Cursos**

- [FastAPI Tutorial - Real Python](https://realpython.com/fastapi-python-web-apis/)
- [Async Python - Real Python](https://realpython.com/async-io-python/)
- [Pydantic Tutorial](https://pydantic-docs.helpmanual.io/usage/models/)

### **Proyectos de Ejemplo**

- [FastAPI Examples](https://github.com/tiangolo/fastapi/tree/master/docs_src)
- [Full Stack FastAPI PostgreSQL](https://github.com/tiangolo/full-stack-fastapi-postgresql)

### **Comunidad**

- [FastAPI GitHub Discussions](https://github.com/tiangolo/fastapi/discussions)
- [Reddit r/FastAPI](https://www.reddit.com/r/FastAPI/)
- [Stack Overflow - FastAPI Tag](https://stackoverflow.com/questions/tagged/fastapi)

---

**💡 Tip**: Mantén estos recursos como referencia durante el desarrollo. No intentes memorizar todo, pero familiarízate con dónde encontrar información cuando la necesites.
