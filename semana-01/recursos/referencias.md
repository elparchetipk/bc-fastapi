# Recursos y Referencias - Semana 1

## 📚 Documentación Oficial

### FastAPI

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [FastAPI GitHub Repository](https://github.com/tiangolo/fastapi)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Advanced User Guide](https://fastapi.tiangolo.com/advanced/)

### Pydantic

- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Pydantic GitHub](https://github.com/pydantic/pydantic)
- [Type Hints Guide](https://pydantic-docs.helpmanual.io/usage/types/)

### Python Type Hints

- [Python Typing Documentation](https://docs.python.org/3/library/typing.html)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [mypy - Static Type Checker](http://mypy-lang.org/)

## 🛠️ Herramientas de Desarrollo

### Editores y IDEs

- [VS Code with Python Extension](https://code.visualstudio.com/docs/languages/python)
- [PyCharm](https://www.jetbrains.com/pycharm/)
- [Vim/Neovim with Python plugins](https://github.com/python-mode/python-mode)

### Testing Tools

- [pytest](https://docs.pytest.org/)
- [httpx - HTTP client](https://www.python-httpx.org/)
- [FastAPI TestClient](https://fastapi.tiangolo.com/tutorial/testing/)

### API Development

- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- [HTTPie](https://httpie.io/)
- [curl](https://curl.se/)

## 📖 Libros Recomendados

### Python

- "Effective Python" by Brett Slatkin
- "Python Tricks" by Dan Bader
- "Fluent Python" by Luciano Ramalho
- "Clean Code in Python" by Mariano Anaya

### API Design

- "RESTful API Design" by Matthias Biehl
- "Building APIs with Node.js" (concepts apply to FastAPI)
- "API Design Patterns" by JJ Geewax

### Web Development

- "Architecture Patterns with Python" by Harry Percival
- "Building Microservices" by Sam Newman

## 🎥 Videos y Cursos

### YouTube Channels

- [ArjanCodes](https://www.youtube.com/c/ArjanCodes) - Python best practices
- [mCoding](https://www.youtube.com/c/mCoding) - Advanced Python
- [Real Python](https://www.youtube.com/c/realpython) - Python tutorials

### Cursos Online

- [FastAPI Course by TestDriven.io](https://testdriven.io/courses/tdd-fastapi/)
- [Python API Development with FastAPI](https://www.udemy.com/course/fastapi-the-complete-course/)
- [Real Python FastAPI Tutorials](https://realpython.com/tutorials/fastapi/)

## 🌐 Blogs y Artículos

### FastAPI Specific

- [FastAPI Blog](https://fastapi.tiangolo.com/blog/)
- [Sebastián Ramírez's Blog](https://tiangolo.com/)
- [TestDriven.io FastAPI Articles](https://testdriven.io/blog/topics/fastapi/)

### General Python/API

- [Real Python](https://realpython.com/)
- [Python.org Blog](https://blog.python.org/)
- [API Evangelist](https://apievangelist.com/)

## 🛠️ Herramientas de Línea de Comandos

### Instalación y Gestión

```bash
# Gestión de paquetes
pip install fastapi uvicorn[standard]
poetry add fastapi uvicorn[standard]

# Entornos virtuales
python -m venv venv
conda create -n fastapi-env python=3.9

# Ejecutar aplicación
uvicorn main:app --reload
uvicorn main:app --host 0.0.0.0 --port 8000

# Testing
pytest
pytest --cov=app
pytest -v tests/

# Linting y formateo
black .
flake8 .
isort .
mypy .
```

### Comandos útiles de HTTP

```bash
# GET request
curl http://localhost:8000/users

# POST request
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{"name":"Juan","email":"juan@email.com"}'

# PUT request
curl -X PUT "http://localhost:8000/users/1" \
     -H "Content-Type: application/json" \
     -d '{"name":"Juan Carlos"}'

# DELETE request
curl -X DELETE "http://localhost:8000/users/1"

# With query parameters
curl "http://localhost:8000/users?page=1&limit=10"
```

## 📊 Cheat Sheets

### FastAPI Quick Reference

```python
from fastapi import FastAPI, HTTPException, Depends, Query, Path, Body
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

# Basic endpoint
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Path parameters
@app.get("/users/{user_id}")
async def get_user(user_id: int = Path(..., ge=1)):
    return {"user_id": user_id}

# Query parameters
@app.get("/items")
async def get_items(skip: int = 0, limit: int = Query(10, le=100)):
    return {"skip": skip, "limit": limit}

# Request body
class User(BaseModel):
    name: str
    email: str

@app.post("/users")
async def create_user(user: User):
    return user

# Dependencies
def get_db():
    return "database_connection"

@app.get("/users")
async def get_users(db = Depends(get_db)):
    return {"db": db}
```

### Pydantic Models

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

class User(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: int = Field(..., ge=18, le=120)
    status: Status = Status.ACTIVE
    tags: Optional[List[str]] = None
    created_at: datetime = Field(default_factory=datetime.now)

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v.strip().title()

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Juan Pérez",
                "email": "juan@email.com",
                "age": 25,
                "status": "active",
                "tags": ["developer", "python"]
            }
        }
```

### HTTP Status Codes

```python
from fastapi import HTTPException, status

# Success
return Response(status_code=status.HTTP_200_OK)          # 200
return Response(status_code=status.HTTP_201_CREATED)     # 201
return Response(status_code=status.HTTP_204_NO_CONTENT)  # 204

# Client Errors
raise HTTPException(status.HTTP_400_BAD_REQUEST)         # 400
raise HTTPException(status.HTTP_401_UNAUTHORIZED)        # 401
raise HTTPException(status.HTTP_403_FORBIDDEN)           # 403
raise HTTPException(status.HTTP_404_NOT_FOUND)           # 404

# Server Errors
raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR) # 500
```

## 🔧 Configuración de Desarrollo

### requirements.txt básico

```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic[email]==2.5.0
python-multipart==0.0.6
pytest==7.4.3
httpx==0.25.2
python-dotenv==1.0.0
```

### .env ejemplo

```
# Application
APP_NAME="Mi FastAPI App"
APP_VERSION="1.0.0"
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL="sqlite:///./app.db"

# Security
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### VS Code settings.json

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

## 🐛 Debugging y Troubleshooting

### Errores Comunes

1. **ImportError**: Módulo no encontrado

   ```bash
   pip install missing-package
   # o verificar PYTHONPATH
   ```

2. **ValidationError**: Error de validación Pydantic

   ```python
   # Verificar tipos de datos
   # Revisar validadores personalizados
   # Comprobar campos requeridos
   ```

3. **404 Not Found**: Endpoint no existe
   ```python
   # Verificar decorador @app.get/post/put/delete
   # Comprobar path parameters
   # Revisar orden de rutas
   ```

### Logging para debugging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.get("/debug")
async def debug_endpoint():
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    return {"message": "Check logs"}
```

## 🌟 Mejores Prácticas

### Estructura de Proyecto

```
app/
├── __init__.py
├── main.py
├── core/
│   ├── __init__.py
│   ├── config.py
│   └── security.py
├── models/
│   ├── __init__.py
│   └── user.py
├── routers/
│   ├── __init__.py
│   └── users.py
├── services/
│   ├── __init__.py
│   └── user_service.py
└── tests/
    ├── __init__.py
    └── test_users.py
```

### Naming Conventions

- **Variables**: snake_case
- **Functions**: snake_case
- **Classes**: PascalCase
- **Constants**: UPPER_SNAKE_CASE
- **Files**: snake_case.py
- **Endpoints**: kebab-case

### Error Handling

```python
from fastapi import HTTPException

def get_user_or_404(user_id: int):
    user = database.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )
    return user
```

## 📱 Extensiones y Plugins

### VS Code Extensions

- Python
- Pylance
- Python Docstring Generator
- REST Client
- Thunder Client
- GitLens

### Herramientas Adicionales

- **pre-commit**: Hooks de Git para calidad de código
- **black**: Formateo automático
- **isort**: Organización de imports
- **flake8**: Linting
- **mypy**: Type checking

## 🔗 APIs Públicas para Practicar

### APIs Gratuitas

- [JSONPlaceholder](https://jsonplaceholder.typicode.com/)
- [HTTPBin](https://httpbin.org/)
- [ReqRes](https://reqres.in/)
- [JSON Server](https://github.com/typicode/json-server)

### Para Integración

- [OpenWeatherMap API](https://openweathermap.org/api)
- [GitHub API](https://docs.github.com/en/rest)
- [REST Countries](https://restcountries.com/)

## 🎯 Próximos Pasos (Semana 2)

### Temas a Estudiar

- SQLAlchemy ORM
- Database migrations con Alembic
- Authentication y Authorization
- JWT Tokens
- Middleware avanzado
- Background tasks
- WebSockets
- Testing avanzado
- Docker deployment

### Preparación Recomendada

- Repasar conceptos de SQL
- Familiarizarse con Docker básico
- Leer sobre OAuth2 y JWT
- Practicar con bases de datos

¡Utiliza estos recursos para profundizar en FastAPI y convertirte en un desarrollador más competente! 🚀
