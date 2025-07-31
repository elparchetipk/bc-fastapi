# Testing y Calidad de Código en FastAPI

⏰ **Duración de Lectura:** 20-30 minutos  
🎯 **Objetivo:** Comprender los fundamentos de testing y calidad en desarrollo profesional  
📚 **Nivel:** Intermedio - construye sobre conocimientos de Semanas 1-7

---

## 🧪 ¿Por qué Testing es Fundamental?

### **La Realidad del Desarrollo Sin Tests**

```python
# 😱 Código sin tests - pesadilla de mantenimiento
@app.post("/users/")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # ¿Qué pasa si user.email es None?
    # ¿Qué pasa si la BD está down?
    # ¿Qué pasa si el email ya existe?
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    return db_user
```

### **Con Testing Robusto**

```python
# ✅ Código con tests - confianza total
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Validado por tests: email único, formato correcto
    if await get_user_by_email(db, user.email):
        raise HTTPException(400, "Email already registered")

    try:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Database error: {str(e)}")
```

---

## 🔬 Tipos de Testing en APIs

### **1. Unit Tests - Lógica Individual**

```python
# test_user_validation.py
def test_user_email_validation():
    """Test que valida formato de email"""
    user_data = {"email": "invalid-email", "name": "Test"}

    with pytest.raises(ValidationError):
        UserCreate(**user_data)
```

### **2. Integration Tests - Componentes Juntos**

```python
# test_user_db_integration.py
async def test_create_user_with_database(test_db):
    """Test que valida integración con BD"""
    user_data = {"email": "test@example.com", "name": "Test User"}

    user = await create_user_in_db(test_db, user_data)
    assert user.email == user_data["email"]
    assert user.id is not None
```

### **3. API Tests - Endpoints Completos**

```python
# test_user_endpoints.py
async def test_create_user_endpoint(client: AsyncClient):
    """Test que valida endpoint completo"""
    response = await client.post("/users/", json={
        "email": "test@example.com",
        "name": "Test User"
    })

    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
```

---

## 🏗️ Arquitectura de Testing

### **Test Pyramid - Distribución Ideal**

```
           /\
          /  \
         / UI \      ← Pocos tests (5%)
        /______\
       /        \
      / API/E2E  \    ← Algunos tests (15%)
     /____________\
    /              \
   / Integration    \  ← Moderados tests (30%)
  /__________________ \
 /                    \
/ Unit Tests           \ ← Muchos tests (50%)
/_______________________\
```

### **En FastAPI - Estructura Recomendada**

```
tests/
├── unit/
│   ├── test_models.py      # Pydantic models
│   ├── test_utils.py       # Utilities functions
│   └── test_services.py    # Business logic
├── integration/
│   ├── test_database.py    # DB operations
│   └── test_auth.py        # Auth flows
├── api/
│   ├── test_users.py       # User endpoints
│   ├── test_posts.py       # Post endpoints
│   └── test_auth.py        # Auth endpoints
└── conftest.py             # Shared fixtures
```

---

## ⚙️ pytest - Framework de Testing

### **Conceptos Fundamentales**

#### **1. Test Functions**

```python
def test_function_name():
    # Arrange - Preparar datos
    user_email = "test@example.com"

    # Act - Ejecutar función
    result = validate_email(user_email)

    # Assert - Verificar resultado
    assert result is True
```

#### **2. Fixtures - Datos de Prueba Reutilizables**

```python
@pytest.fixture
def sample_user():
    """Fixture que provee un usuario de prueba"""
    return {
        "id": 1,
        "email": "test@example.com",
        "name": "Test User",
        "is_active": True
    }

def test_user_serialization(sample_user):
    user = User(**sample_user)
    assert user.email == sample_user["email"]
```

#### **3. Parametrized Tests**

```python
@pytest.mark.parametrize("email,expected", [
    ("test@example.com", True),
    ("invalid-email", False),
    ("", False),
    (None, False)
])
def test_email_validation(email, expected):
    assert validate_email(email) == expected
```

### **Testing Asíncrono**

```python
import pytest_asyncio

@pytest_asyncio.async_def
async def test_async_user_creation():
    user_data = {"email": "test@example.com", "name": "Test"}
    user = await create_user_async(user_data)
    assert user.email == user_data["email"]
```

---

## 🔧 TestClient - Testing de FastAPI

### **Setup Básico**

```python
from fastapi.testclient import TestClient
from httpx import AsyncClient
import pytest

# Sync testing
client = TestClient(app)

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200

# Async testing (recomendado)
@pytest.mark.asyncio
async def test_read_users_async():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/")
    assert response.status_code == 200
```

### **Testing con Autenticación**

```python
@pytest.fixture
async def authenticated_client():
    """Cliente con usuario autenticado"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Login para obtener token
        login_response = await ac.post("/auth/login", json={
            "email": "test@example.com",
            "password": "testpass"
        })
        token = login_response.json()["access_token"]

        # Configurar headers
        ac.headers.update({"Authorization": f"Bearer {token}"})
        yield ac

async def test_protected_endpoint(authenticated_client):
    response = await authenticated_client.get("/users/me")
    assert response.status_code == 200
```

---

## 📊 Coverage - Midiendo Cobertura

### **Instalación y Configuración**

```bash
pip install pytest-cov
```

```ini
# pytest.ini
[tool:pytest]
addopts = --cov=app --cov-report=html --cov-report=term-missing
testpaths = tests
```

### **Interpretando Reports**

```bash
# Terminal output
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
app/main.py             25      3    88%    23-25
app/models.py           45      0   100%
app/auth.py             30      8    73%    67-74
--------------------------------------------------
TOTAL                  100     11    89%
```

### **Configuración de Coverage**

```ini
# .coveragerc
[run]
source = app
omit =
    app/tests/*
    app/config.py
    app/__init__.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

---

## 🎯 Mocking - Aislando Dependencias

### **¿Cuándo Usar Mocks?**

```python
# ❌ Test lento y frágil - depende de servicio externo
def test_send_email():
    email_service = EmailService()  # ¡Envía email real!
    result = email_service.send("test@example.com", "Test")
    assert result.success

# ✅ Test rápido y confiable - mock del servicio
@patch('app.services.EmailService')
def test_send_email_mocked(mock_email_service):
    mock_email_service.send.return_value = EmailResult(success=True)

    result = send_welcome_email("test@example.com")
    assert result.success
    mock_email_service.send.assert_called_once()
```

### **Mocking en FastAPI**

```python
# test_dependencies.py
from unittest.mock import AsyncMock

async def test_endpoint_with_mocked_db():
    # Mock de la dependencia de base de datos
    mock_db = AsyncMock()
    mock_db.get_user.return_value = User(id=1, email="test@example.com")

    # Override dependency
    app.dependency_overrides[get_db] = lambda: mock_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/users/1")

    assert response.status_code == 200
    mock_db.get_user.assert_called_once_with(1)
```

---

## 📝 Documentación Automática

### **OpenAPI 3.0 Personalizada**

```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Enterprise API",
        version="2.0.0",
        description="API with comprehensive testing and quality",
        routes=app.routes,
    )

    # Customizations
    openapi_schema["info"]["x-logo"] = {
        "url": "https://example.com/logo.png"
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

### **Examples en Models**

```python
from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    email: str = Field(..., example="user@example.com")
    name: str = Field(..., example="John Doe")
    age: int = Field(..., gt=0, le=120, example=25)

    class Config:
        schema_extra = {
            "example": {
                "email": "john.doe@company.com",
                "name": "John Doe",
                "age": 28
            }
        }
```

### **Docstrings Estructurados**

````python
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.

    Args:
        user: User data for creation
        db: Database session

    Returns:
        UserResponse: Created user data

    Raises:
        HTTPException: 400 if email already exists
        HTTPException: 422 if validation fails

    Example:
        ```python
        user_data = {
            "email": "user@example.com",
            "name": "John Doe",
            "age": 25
        }
        response = await client.post("/users/", json=user_data)
        ```
    """
    if await get_user_by_email(db, user.email):
        raise HTTPException(400, "Email already registered")

    return await create_user_in_db(db, user)
````

---

## ⚡ Code Quality Tools

### **Black - Formateo Automático**

```python
# Antes de Black
def create_user(email:str,name:str,age:int=None)->User:
    if email is None or name is None:raise ValueError("Missing data")
    return User(email=email,name=name,age=age)

# Después de Black
def create_user(email: str, name: str, age: int = None) -> User:
    if email is None or name is None:
        raise ValueError("Missing data")
    return User(email=email, name=name, age=age)
```

**Configuración:**

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py38']
include = '\.pyi?$'
extend-exclude = '''
/(
  migrations
  | .venv
  | build
)/
'''
```

### **isort - Organización de Imports**

```python
# Antes de isort
from fastapi import FastAPI
import os
from app.models import User
from pydantic import BaseModel
import sys
from typing import List

# Después de isort
import os
import sys
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

from app.models import User
```

### **flake8 - Linting**

```ini
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    migrations,
    .venv
per-file-ignores =
    __init__.py:F401
```

### **pre-commit - Automation**

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.8

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ['--profile', 'black']

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

---

## 🚀 CI/CD Preparation

### **GitHub Actions Example**

```yaml
# .github/workflows/quality.yml
name: Quality Checks

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.8

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run Black
        run: black --check .

      - name: Run isort
        run: isort --check-only .

      - name: Run flake8
        run: flake8 .

      - name: Run tests with coverage
        run: pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### **Quality Scripts**

```bash
#!/bin/bash
# scripts/quality.sh

echo "🔍 Running quality checks..."

echo "📏 Checking code formatting..."
black --check . || exit 1

echo "📦 Checking import organization..."
isort --check-only . || exit 1

echo "🔍 Running linting..."
flake8 . || exit 1

echo "🧪 Running tests with coverage..."
pytest --cov=app --cov-report=term-missing || exit 1

echo "✅ All quality checks passed!"
```

---

## 🎯 Best Practices Summary

### **Testing Guidelines**

1. **✅ Write tests first** (TDD approach)
2. **✅ Test behavior, not implementation**
3. **✅ Keep tests simple and focused**
4. **✅ Use descriptive test names**
5. **✅ Mock external dependencies**
6. **✅ Maintain >80% coverage**

### **Quality Guidelines**

1. **✅ Automate formatting** with Black
2. **✅ Organize imports** with isort
3. **✅ Check code quality** with flake8
4. **✅ Use pre-commit hooks**
5. **✅ Document public APIs**
6. **✅ Write clear docstrings**

### **CI/CD Guidelines**

1. **✅ Run tests on every commit**
2. **✅ Block merges with failing tests**
3. **✅ Generate coverage reports**
4. **✅ Automate quality checks**
5. **✅ Use quality gates**
6. **✅ Monitor technical debt**

---

## 📚 Recursos Adicionales

### **Documentación Oficial**

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Black Documentation](https://black.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)

### **Libros Recomendados**

- "Test-Driven Development with Python" - Harry Percival
- "Clean Code" - Robert C. Martin
- "The Pragmatic Programmer" - Andy Hunt

### **Tools y Extensions**

- **VS Code**: Python Test Explorer, Coverage Gutters
- **PyCharm**: Built-in testing tools
- **Browser**: Coverage reports HTML

---

**🧪 ¡Ahora tienes las bases teóricas para construir software de calidad profesional!**

En las siguientes prácticas implementaremos estos conceptos paso a paso, creando una suite de testing completa y configurando todas las herramientas de calidad para tu API FastAPI.
