# Fundamentos Teóricos - FastAPI y Python Moderno

## 🎯 Conceptos Fundamentales

### 1. ¿Qué es FastAPI?

FastAPI es un framework web moderno y de alto rendimiento para construir APIs con Python 3.8+ basado en type hints estándar de Python.

#### Características Principales

- **Alto rendimiento**: Comparable a NodeJS y Go
- **Rápido de codificar**: Incrementa la velocidad de desarrollo de 200% a 300%
- **Menos bugs**: Reduce errores humanos aproximadamente en 40%
- **Intuitivo**: Excelente soporte del editor con autocompletado
- **Fácil**: Diseñado para ser fácil de usar y aprender
- **Corto**: Minimiza duplicación de código
- **Robusto**: Código listo para producción con documentación automática
- **Basado en estándares**: Basado en (y totalmente compatible con) OpenAPI y JSON Schema

### 2. Arquitectura de FastAPI

```
┌─────────────────────────────────────────────┐
│                FastAPI App                  │
├─────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────────┐   │
│  │   Router    │  │    Dependency       │   │
│  │   Sistema   │  │    Injection        │   │
│  └─────────────┘  └─────────────────────┘   │
├─────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────────────┐   │
│  │  Pydantic   │  │    Middleware       │   │
│  │  Validation │  │    Sistema          │   │
│  └─────────────┘  └─────────────────────┘   │
├─────────────────────────────────────────────┤
│             Starlette (ASGI)                │
├─────────────────────────────────────────────┤
│             Uvicorn (Server)                │
└─────────────────────────────────────────────┘
```

### 3. Type Hints en Python

Los type hints son anotaciones que indican el tipo esperado de variables, parámetros y valores de retorno.

#### ¿Por qué son importantes?

1. **Claridad del código**: Hace el código más legible
2. **Herramientas de desarrollo**: Mejor autocompletado y detección de errores
3. **Documentación automática**: FastAPI genera docs basándose en tipos
4. **Validación automática**: Pydantic valida datos basándose en tipos

#### Ejemplo de evolución

```python
# Sin type hints
def process_user(data):
    return {"id": data["id"], "name": data["name"].upper()}

# Con type hints básicos
def process_user(data: dict) -> dict:
    return {"id": data["id"], "name": data["name"].upper()}

# Con type hints específicos
from typing import Dict, Any
def process_user(data: Dict[str, Any]) -> Dict[str, Any]:
    return {"id": data["id"], "name": data["name"].upper()}

# Con Pydantic (FastAPI way)
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

def process_user(data: User) -> UserResponse:
    return UserResponse(id=data.id, name=data.name.upper())
```

### 4. Pydantic - El Corazón de FastAPI

Pydantic es una librería de validación de datos que utiliza type hints de Python.

#### Beneficios

1. **Validación automática**: Tipos, rangos, formatos
2. **Serialización**: Conversión entre tipos de datos
3. **Documentación**: Genera esquemas JSON automáticamente
4. **Rendimiento**: Validación rápida basada en Rust
5. **IDE Support**: Autocompletado y detección de errores

#### Ciclo de vida de datos en FastAPI

```
Request JSON → Pydantic Model → Python Objects → Business Logic →
Pydantic Response Model → JSON Response
```

### 5. Programación Asíncrona

FastAPI está construido sobre programación asíncrona, permitiendo manejar múltiples requests concurrentemente.

#### Conceptos Clave

- **async/await**: Sintaxis para funciones asíncronas
- **Event Loop**: Bucle que maneja operaciones asíncronas
- **Coroutines**: Funciones que pueden pausarse y reanudarse
- **Concurrencia**: Múltiples tareas progresando simultáneamente

#### Cuándo usar async

```python
# Usar async cuando:
@app.get("/external-api")
async def call_external_api():
    # Llamadas a APIs externas
    # Operaciones de base de datos
    # Operaciones de archivos I/O
    # Cualquier operación que "espera"
    pass

# No async cuando:
@app.get("/calculation")
def heavy_calculation():
    # Cálculos intensivos de CPU
    # Operaciones que no "esperan"
    # Procesamientos síncronos
    pass
```

### 6. REST API Design Principles

#### Principios fundamentales

1. **Stateless**: Cada request contiene toda la información necesaria
2. **Client-Server**: Separación clara entre cliente y servidor
3. **Cacheable**: Responses deben ser cacheables cuando sea apropiado
4. **Layered System**: Arquitectura en capas
5. **Uniform Interface**: Interfaz consistente

#### HTTP Methods y su propósito

- **GET**: Obtener datos (idempotente, safe)
- **POST**: Crear recursos (no idempotente)
- **PUT**: Actualizar completo (idempotente)
- **PATCH**: Actualización parcial (no idempotente)
- **DELETE**: Eliminar recursos (idempotente)

#### Status Codes importantes

- **2xx Success**: 200 (OK), 201 (Created), 204 (No Content)
- **4xx Client Error**: 400 (Bad Request), 401 (Unauthorized), 404 (Not Found)
- **5xx Server Error**: 500 (Internal Server Error), 503 (Service Unavailable)

### 7. OpenAPI y Documentación Automática

FastAPI genera documentación automática basada en el estándar OpenAPI 3.0.

#### Beneficios

1. **Documentación siempre actualizada**
2. **Testing interactivo**
3. **Generación de clientes**
4. **Validación de contratos**

#### Componentes de OpenAPI

```yaml
openapi: 3.0.0
info:
  title: Mi API
  version: 1.0.0
paths:
  /users:
    get:
      summary: Obtener usuarios
      responses:
        200:
          description: Lista de usuarios
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
```

## 🔧 Patrones de Diseño en FastAPI

### 1. Dependency Injection

```python
from fastapi import Depends

def get_database():
    # Conexión a base de datos
    return database

@app.get("/users")
async def get_users(db = Depends(get_database)):
    return db.get_users()
```

### 2. Repository Pattern

```python
class UserRepository:
    def __init__(self, db):
        self.db = db

    def get_user(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

def get_user_repository(db = Depends(get_database)):
    return UserRepository(db)

@app.get("/users/{user_id}")
async def get_user(user_id: int, repo = Depends(get_user_repository)):
    return repo.get_user(user_id)
```

### 3. Service Layer

```python
class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserCreate):
        # Lógica de negocio
        if self.repository.email_exists(user_data.email):
            raise HTTPException(400, "Email already exists")
        return self.repository.create_user(user_data)
```

## 📊 Mejores Prácticas

### 1. Estructura del Proyecto

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── users.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── user_service.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── user_repository.py
│   └── core/
│       ├── __init__.py
│       ├── config.py
│       └── database.py
├── tests/
├── requirements.txt
└── README.md
```

### 2. Manejo de Errores

```python
from fastapi import HTTPException

class UserNotFoundError(Exception):
    pass

@app.exception_handler(UserNotFoundError)
async def user_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Usuario no encontrado"}
    )
```

### 3. Validación de Datos

```python
from pydantic import validator, Field

class User(BaseModel):
    email: EmailStr
    age: int = Field(..., ge=18, le=120)

    @validator('email')
    def email_must_be_corporate(cls, v):
        if not v.endswith('@empresa.com'):
            raise ValueError('Debe ser email corporativo')
        return v
```

## 🎯 Conceptos para la Semana 2

- **Database Integration** (SQLAlchemy, databases)
- **Authentication & Authorization** (OAuth2, JWT)
- **Advanced Dependency Injection**
- **Background Tasks**
- **WebSockets**
- **Testing** (pytest, TestClient)
- **Deployment** (Docker, cloud platforms)

## 📚 Recursos Adicionales

- [FastAPI Official Docs](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [OpenAPI Specification](https://swagger.io/specification/)
- [REST API Design](https://restfulapi.net/)

## 🧠 Preguntas de Reflexión

1. ¿Cuáles son las ventajas de usar type hints en Python?
2. ¿Cómo FastAPI utiliza Pydantic para validación?
3. ¿Cuándo deberías usar async vs sync en FastAPI?
4. ¿Qué beneficios proporciona la documentación automática?
5. ¿Cómo se relacionan los principios REST con FastAPI?
