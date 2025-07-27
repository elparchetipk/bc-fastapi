}# Práctica 19: Pytest Setup y Configuración

## 🎯 Objetivo

Configurar **pytest** en un proyecto FastAPI e implementar los primeros tests básicos en 90 minutos, estableciendo una base sólida para testing automatizado.

## ⏱️ Tiempo: 90 minutos

## 📋 Pre-requisitos

- ✅ Proyecto FastAPI funcionando (Semana 1-5 completada)
- ✅ API con autenticación implementada
- ✅ Conocimientos básicos de Python y FastAPI
- ✅ Entorno virtual activado

## 🚀 Desarrollo Paso a Paso

### Paso 1: Instalación de Dependencias (15 min)

#### Instalar librerías de testing

```bash
# En tu directorio del proyecto
pip install pytest httpx pytest-asyncio coverage

# Verificar instalación
pytest --version
```

#### Actualizar requirements.txt

```text
# Dependencias existentes
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# NUEVAS: Para testing
pytest==7.4.3
httpx==0.25.2
pytest-asyncio==0.21.1
coverage==7.3.2
```

#### ¿Para qué sirve cada librería?

- **`pytest`**: Framework principal de testing
- **`httpx`**: Cliente HTTP para testear APIs (usado por TestClient)
- **`pytest-asyncio`**: Soporte para testing de código asíncrono
- **`coverage`**: Medir cobertura de código

---

### Paso 2: Estructura de Testing (20 min)

#### Crear estructura de carpetas

```bash
# Desde la raíz de tu proyecto
mkdir tests
touch tests/__init__.py
touch tests/conftest.py
touch tests/test_main.py
touch tests/test_auth.py
touch tests/test_users.py

# Verificar estructura
tree tests/
```

#### Estructura esperada

```text
tu-proyecto/
├── main.py
├── auth.py
├── models.py
├── database.py
├── requirements.txt
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Configuración y fixtures
│   ├── test_main.py         # Tests de endpoints básicos
│   ├── test_auth.py         # Tests de autenticación
│   └── test_users.py        # Tests de usuarios
```

#### Configurar conftest.py

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import get_db, Base

# Base de datos de testing en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas de testing
Base.metadata.create_all(bind=engine)

def override_get_db():
    """Override de la dependencia de BD para testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override de dependencia
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Cliente de testing para FastAPI"""
    return TestClient(app)

@pytest.fixture
def test_user():
    """Datos de usuario de prueba"""
    return {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }
```

---

### Paso 3: Primer Test Básico (25 min)

#### Crear test de endpoint principal

```python
# tests/test_main.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    """Test del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200
    # Ajustar según tu endpoint raíz
    assert "message" in response.json()

def test_health_check():
    """Test de health check (si existe)"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_docs_endpoint():
    """Test de que la documentación está disponible"""
    response = client.get("/docs")
    assert response.status_code == 200

def test_openapi_endpoint():
    """Test del schema OpenAPI"""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
```

#### Ejecutar tu primer test

```bash
# Ejecutar todos los tests
pytest

# Ejecutar solo un archivo
pytest tests/test_main.py

# Ejecutar con más detalle
pytest -v
```

#### Output esperado

```bash
$ pytest -v
========================= test session starts =========================
collected 4 items

tests/test_main.py::test_read_root PASSED                    [25%]
tests/test_main.py::test_health_check PASSED                [50%]
tests/test_main.py::test_docs_endpoint PASSED               [75%]
tests/test_main.py::test_openapi_endpoint PASSED           [100%]

========================= 4 passed in 0.45s =========================
```

---

### Paso 4: Testing con Fixtures (30 min)

#### Usar fixture de cliente

```python
# tests/test_main.py (versión mejorada)
import pytest

def test_read_root(client):
    """Test usando fixture de cliente"""
    response = client.get("/")
    assert response.status_code == 200

def test_invalid_endpoint(client):
    """Test de endpoint que no existe"""
    response = client.get("/nonexistent")
    assert response.status_code == 404

def test_get_users_empty(client):
    """Test de lista de usuarios vacía"""
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == []
```

#### Fixture para datos de prueba

```python
# Agregar a tests/conftest.py
@pytest.fixture
def sample_users():
    """Lista de usuarios de prueba"""
    return [
        {
            "email": "user1@example.com",
            "password": "password123",
            "name": "User One"
        },
        {
            "email": "user2@example.com",
            "password": "password456",
            "name": "User Two"
        }
    ]

@pytest.fixture
def auth_headers():
    """Headers de autenticación (versión simple)"""
    # Por ahora retorna headers vacíos, mejoraremos después
    return {}
```

#### Test usando múltiples fixtures

```python
# tests/test_users.py
import pytest

def test_user_data_structure(test_user):
    """Test de estructura de datos del usuario"""
    assert "email" in test_user
    assert "password" in test_user
    assert "name" in test_user
    assert "@" in test_user["email"]

def test_multiple_users(sample_users):
    """Test con múltiples usuarios"""
    assert len(sample_users) == 2
    assert all("email" in user for user in sample_users)

def test_create_user_endpoint(client, test_user):
    """Test básico de creación de usuario"""
    response = client.post("/auth/register", json=test_user)
    # Ajustar según tu API
    assert response.status_code in [201, 200]
```

---

### Paso 5: Configuración Avanzada de pytest (20 min)

#### Crear pytest.ini

```ini
# pytest.ini (en la raíz del proyecto)
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-markers
    --disable-warnings
markers =
    slow: marks tests as slow
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

#### Marcadores para organizar tests

```python
# tests/test_main.py
import pytest

@pytest.mark.unit
def test_read_root(client):
    """Test unitario del endpoint raíz"""
    response = client.get("/")
    assert response.status_code == 200

@pytest.mark.integration
def test_user_creation_flow(client, test_user):
    """Test de integración completo"""
    # Crear usuario
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == 201

    # Verificar que existe
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"]
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200

@pytest.mark.slow
def test_database_heavy_operation(client):
    """Test que puede ser lento"""
    # Operación que toma tiempo
    pass
```

#### Ejecutar tests por marcadores

```bash
# Solo tests unitarios
pytest -m unit

# Solo tests de integración
pytest -m integration

# Excluir tests lentos
pytest -m "not slow"

# Combinar marcadores
pytest -m "unit and not slow"
```

---

## 🧪 Testing Manual

### Verificación Paso a Paso

#### 1. Verificar instalación

```bash
pytest --version
# Debería mostrar: pytest 7.4.3
```

#### 2. Ejecutar tests básicos

```bash
pytest tests/test_main.py -v
# Todos los tests deberían pasar
```

#### 3. Verificar fixtures

```bash
pytest tests/test_users.py -v
# Verificar que fixtures funcionan
```

#### 4. Verificar marcadores

```bash
pytest -m unit -v
# Solo tests marcados como unit
```

---

## 📊 Checklist de Verificación

### ✅ Setup Básico

- [ ] pytest instalado correctamente
- [ ] Estructura de carpeta `tests/` creada
- [ ] `conftest.py` configurado con fixtures básicas
- [ ] TestClient funcionando

### ✅ Tests Funcionando

- [ ] Test básico del endpoint raíz pasa
- [ ] Test de documentación (/docs) pasa
- [ ] Tests usando fixtures funcionan
- [ ] Marcadores configurados correctamente

### ✅ Configuración

- [ ] `pytest.ini` configurado
- [ ] Base de datos de testing separada
- [ ] Override de dependencias funciona
- [ ] Fixtures reutilizables creadas

---

## 🔧 Troubleshooting

### ❌ Error: "ModuleNotFoundError"

```bash
# Solución: Agregar directorio actual al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# O ejecutar desde directorio del proyecto
python -m pytest
```

### ❌ Error: "Database locked"

```python
# En conftest.py, asegurar cleanup
@pytest.fixture(autouse=True)
def cleanup_db():
    """Limpiar BD después de cada test"""
    yield
    # Cleanup code aquí
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
```

### ❌ Tests muy lentos

```python
# Usar BD en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
```

---

## 📚 Recursos Adicionales

### Documentación Oficial

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [httpx Testing](https://www.python-httpx.org/)

### Comandos Útiles

```bash
# Ejecutar tests con cobertura
pytest --cov=.

# Ejecutar un test específico
pytest tests/test_main.py::test_read_root

# Ejecutar tests en paralelo (requiere pytest-xdist)
pytest -n auto

# Modo verboso con salida de print
pytest -v -s
```

---

## 🎯 Próximos Pasos

En la siguiente práctica aprenderás:

1. **Testing de endpoints** - CRUD completo
2. **Validación de respuestas** - JSON, status codes
3. **Testing de errores** - 404, 422, 500
4. **Organización avanzada** - Tests más complejos

¡Has establecido una base sólida para testing automatizado! 🧪✨
