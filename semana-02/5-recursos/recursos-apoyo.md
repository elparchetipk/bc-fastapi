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
nombre: str = "Juan"
edad: int = 25
precio: float = 29.99
activo: bool = True

# Colecciones
numeros: List[int] = [1, 2, 3]
configuracion: Dict[str, str] = {"host": "localhost"}
datos: Dict[str, Any] = {"nombre": "Juan", "edad": 25}

# Opcionales
email: Optional[str] = None  # Puede ser str o None
resultado: Union[str, int] = "texto"  # Puede ser str o int

# Funciones
def procesar(datos: List[str]) -> Dict[str, int]:
    return {"total": len(datos)}

# Async
async def obtener_datos() -> List[Dict[str, Any]]:
    return [{"id": 1, "nombre": "test"}]
```

### **Pydantic Patterns**

```python
from pydantic import BaseModel, Field, validator, root_validator
from enum import Enum
from datetime import datetime
from typing import Optional

class Estado(str, Enum):
    activo = "activo"
    inactivo = "inactivo"

class MiModelo(BaseModel):
    # Field con validación
    nombre: str = Field(..., min_length=2, max_length=50, description="Nombre completo")
    edad: int = Field(..., ge=18, le=120, description="Edad en años")
    email: Optional[str] = Field(None, regex=r'^[^@]+@[^@]+\.[^@]+$')
    estado: Estado = Estado.activo

    # Validator simple
    @validator('nombre')
    def normalizar_nombre(cls, v):
        return v.strip().title()

    # Validator con values
    @validator('email')
    def validar_email_estado(cls, v, values):
        if values.get('estado') == Estado.activo and not v:
            raise ValueError('Email requerido para usuarios activos')
        return v

    # Root validator
    @root_validator
    def validar_modelo_completo(cls, values):
        # Validaciones que requieren múltiples campos
        return values

    # Configuración
    class Config:
        use_enum_values = True  # Serializar enums como valores
        validate_assignment = True  # Validar al asignar
        schema_extra = {
            "example": {
                "nombre": "Juan Pérez",
                "edad": 30,
                "email": "juan@ejemplo.com",
                "estado": "activo"
            }
        }
```

### **FastAPI Patterns**

```python
from fastapi import FastAPI, HTTPException, Query, Path, Body, status
from typing import List, Optional

app = FastAPI()

# Endpoint básico
@app.get("/usuarios/{user_id}", response_model=Usuario)
def obtener_usuario(user_id: int = Path(..., ge=1, description="ID del usuario")):
    # Lógica aquí
    pass

# Query parameters con validación
@app.get("/usuarios", response_model=List[Usuario])
def listar_usuarios(
    activo: bool = Query(True, description="Filtrar por estado"),
    limit: int = Query(10, ge=1, le=100, description="Límite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginación")
):
    pass

# Request body
@app.post("/usuarios", response_model=Usuario, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate = Body(..., description="Datos del usuario")):
    pass

# Múltiples response models
@app.get("/usuarios/{user_id}",
         responses={
             200: {"model": Usuario, "description": "Usuario encontrado"},
             404: {"model": ErrorModel, "description": "Usuario no encontrado"}
         })
def obtener_usuario_completo(user_id: int):
    pass

# Async endpoint
@app.get("/usuarios/{user_id}/external")
async def obtener_datos_externos(user_id: int):
    # Operaciones async aquí
    resultado = await llamada_externa(user_id)
    return resultado
```

### **Async/Await Patterns**

```python
import asyncio
import httpx
from typing import List

# Función async básica
async def operacion_lenta():
    await asyncio.sleep(1)
    return "completado"

# Multiple operaciones en paralelo
async def procesar_lote(items: List[str]):
    tareas = [procesar_item(item) for item in items]
    resultados = await asyncio.gather(*tareas)
    return resultados

# HTTP client async
async def llamada_api_externa(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()

# Con timeout
async def operacion_con_timeout():
    try:
        resultado = await asyncio.wait_for(
            operacion_lenta(),
            timeout=5.0
        )
        return resultado
    except asyncio.TimeoutError:
        raise HTTPException(status_code=408, detail="Timeout")

# Semáforo para limitar concurrencia
semaforo = asyncio.Semaphore(3)

async def operacion_limitada():
    async with semaforo:
        await operacion_lenta()
        return "completado"
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

def test_crud_usuario():
    """Test completo de CRUD de usuarios"""
    print("🧪 Testing CRUD de usuarios...")

    # 1. Crear usuario
    nuevo_usuario = {
        "nombre": "Test User",
        "email": "test@ejemplo.com",
        "tipo": "developer",
        "password": "12345678"
    }

    response = requests.post(f"{BASE_URL}/usuarios", json=nuevo_usuario)
    assert response.status_code == 201, f"Error creando usuario: {response.text}"
    usuario = response.json()
    user_id = usuario["id"]
    print(f"✅ Usuario creado con ID {user_id}")

    # 2. Obtener usuario
    response = requests.get(f"{BASE_URL}/usuarios/{user_id}")
    assert response.status_code == 200, f"Error obteniendo usuario: {response.text}"
    print("✅ Usuario obtenido correctamente")

    # 3. Actualizar usuario
    update_data = {"nombre": "Test User Updated"}
    response = requests.patch(f"{BASE_URL}/usuarios/{user_id}", json=update_data)
    assert response.status_code == 200, f"Error actualizando usuario: {response.text}"
    print("✅ Usuario actualizado correctamente")

    # 4. Listar usuarios
    response = requests.get(f"{BASE_URL}/usuarios")
    assert response.status_code == 200, f"Error listando usuarios: {response.text}"
    usuarios = response.json()
    assert len(usuarios) > 0, "No se encontraron usuarios"
    print(f"✅ Lista de usuarios obtenida: {len(usuarios)} usuarios")

    print("🎉 Test CRUD usuarios completado!")

if __name__ == "__main__":
    test_crud_usuario()
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

def poblar_datos():
    """Poblar API con datos de ejemplo"""
    print("📊 Poblando datos de ejemplo...")

    # Usuarios
    usuarios = [
        {"nombre": "Admin User", "email": "admin@empresa.com", "tipo": "admin", "password": "admin123"},
        {"nombre": "Manager Test", "email": "manager@empresa.com", "tipo": "manager", "password": "manager123"},
        {"nombre": "Dev Frontend", "email": "frontend@empresa.com", "tipo": "developer", "password": "dev123"},
        {"nombre": "Dev Backend", "email": "backend@empresa.com", "tipo": "developer", "password": "dev123"},
        {"nombre": "QA Tester", "email": "qa@empresa.com", "tipo": "viewer", "password": "qa123"},
    ]

    user_ids = []
    for usuario in usuarios:
        response = requests.post(f"{BASE_URL}/usuarios", json=usuario)
        if response.status_code == 201:
            user_ids.append(response.json()["id"])
            print(f"✅ Usuario creado: {usuario['nombre']}")

    # Proyectos
    proyectos = [
        {
            "nombre": "Sistema Web",
            "descripcion": "Desarrollo del sistema web principal",
            "fecha_inicio": str(date.today()),
            "fecha_limite": str(date.today() + timedelta(days=90)),
            "manager_id": user_ids[1] if len(user_ids) > 1 else 1
        },
        {
            "nombre": "App Mobile",
            "descripcion": "Aplicación móvil complementaria",
            "fecha_inicio": str(date.today()),
            "fecha_limite": str(date.today() + timedelta(days=60)),
            "manager_id": user_ids[1] if len(user_ids) > 1 else 1
        }
    ]

    proyecto_ids = []
    for proyecto in proyectos:
        response = requests.post(f"{BASE_URL}/proyectos", json=proyecto)
        if response.status_code == 201:
            proyecto_ids.append(response.json()["id"])
            print(f"✅ Proyecto creado: {proyecto['nombre']}")

    # Tareas
    tareas = [
        {
            "titulo": "Configurar entorno de desarrollo",
            "descripcion": "Configurar Docker y dependencias",
            "estado": "completada",
            "prioridad": "alta",
            "proyecto_id": proyecto_ids[0] if proyecto_ids else 1,
            "asignado_a": user_ids[2] if len(user_ids) > 2 else 1,
            "estimacion_horas": 8.0
        },
        {
            "titulo": "Diseñar base de datos",
            "descripcion": "Crear schema de la base de datos",
            "estado": "en_progreso",
            "prioridad": "alta",
            "proyecto_id": proyecto_ids[0] if proyecto_ids else 1,
            "asignado_a": user_ids[3] if len(user_ids) > 3 else 1,
            "estimacion_horas": 16.0
        },
        {
            "titulo": "Implementar autenticación",
            "descripcion": "Sistema de login y registro",
            "estado": "pendiente",
            "prioridad": "media",
            "proyecto_id": proyecto_ids[0] if proyecto_ids else 1,
            "asignado_a": user_ids[3] if len(user_ids) > 3 else 1,
            "estimacion_horas": 20.0
        }
    ]

    for tarea in tareas:
        response = requests.post(f"{BASE_URL}/tareas", json=tarea)
        if response.status_code == 201:
            print(f"✅ Tarea creada: {tarea['titulo']}")

    print("🎉 Datos de ejemplo creados exitosamente!")

if __name__ == "__main__":
    poblar_datos()
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
