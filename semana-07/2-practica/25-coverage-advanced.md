# Práctica 25: Coverage Avanzado y Testing con Mocks

## 🎯 Objetivo

Implementar **testing avanzado con coverage detallado** y **mocks para dependencias externas**, llevando el testing a nivel profesional en 90 minutos.

## ⏱️ Tiempo: 90 minutos

## 📋 Pre-requisitos

- ✅ Testing básico funcionando (Semana 6)
- ✅ Sistema de autenticación y roles (Semanas 5-6)
- ✅ Pytest configurado correctamente

---

## 🚀 Desarrollo Paso a Paso

### Paso 1: Configuración de Coverage Avanzado (25 min)

#### Instalar dependencias de coverage

```bash
# Instalar herramientas de coverage
pip install pytest-cov coverage[toml]

# Actualizar requirements.txt
pip freeze > requirements.txt
```

#### Configurar coverage en `pyproject.toml`

```toml
[tool.coverage.run]
source = ["app"]
omit = [
    "app/tests/*",
    "app/migrations/*",
    "*/venv/*",
    "*/virtualenv/*",
    "*/.tox/*",
    "*/site-packages/*"
]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstract"
]
show_missing = true
precision = 2
fail_under = 80

[tool.coverage.html]
directory = "htmlcov"
```

#### Configurar pytest en `pytest.ini`

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
python_classes = Test*
addopts =
    --strict-markers
    --disable-warnings
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    auth: Authentication tests
    admin: Admin functionality tests
    slow: Slow tests
```

#### Ejecutar coverage inicial

```bash
# Ejecutar tests con coverage
pytest --cov=app --cov-report=html --cov-report=term

# Ver reporte en terminal
coverage report

# Abrir reporte HTML
open htmlcov/index.html  # macOS
# xdg-open htmlcov/index.html  # Linux
```

---

### Paso 2: Testing con Mocks Básicos (30 min)

#### Instalar pytest-mock

```bash
pip install pytest-mock
```

#### Crear `tests/test_mocks.py`

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi.testclient import TestClient
import redis

from app.main import app
from app.auth.dependencies import get_current_user
from app.models.user import User

def test_external_service_mock(client, mocker):
    """Test con mock de servicio externo"""

    # Mock de Redis
    mock_redis = mocker.patch('app.cache.redis_client')
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True

    response = client.get("/some-cached-endpoint")

    assert response.status_code == 200
    mock_redis.get.assert_called_once()

def test_database_operation_mock(client, mocker):
    """Test con mock de operación de base de datos"""

    # Mock de función de base de datos
    mock_db_operation = mocker.patch('app.crud.get_user_by_email')

    # Configurar el mock
    mock_user = User(
        id=1,
        email="test@example.com",
        full_name="Test User",
        role="user"
    )
    mock_db_operation.return_value = mock_user

    # Ejecutar test
    response = client.get("/users/test@example.com")

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    mock_db_operation.assert_called_once_with("test@example.com")

def test_authentication_dependency_mock(client, mocker):
    """Test con mock de dependencia de autenticación"""

    # Mock del usuario actual
    mock_user = User(
        id=1,
        email="admin@test.com",
        full_name="Admin User",
        role="admin"
    )

    # Mock de la dependencia
    mocker.patch('app.auth.dependencies.get_current_user', return_value=mock_user)

    response = client.get("/admin/users")

    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)

@pytest.mark.asyncio
async def test_async_operation_mock(mocker):
    """Test con mock de operación asíncrona"""

    # Mock de operación async
    mock_async_func = mocker.patch('app.services.send_email', new_callable=mocker.AsyncMock)
    mock_async_func.return_value = {"status": "sent", "id": "email-123"}

    from app.services import send_email

    result = await send_email("test@example.com", "Subject", "Body")

    assert result["status"] == "sent"
    mock_async_func.assert_called_once_with("test@example.com", "Subject", "Body")
```

#### Testing de errores con mocks

```python
def test_redis_connection_error_handling(client, mocker):
    """Test manejo de errores cuando Redis falla"""

    # Mock que simula error de conexión
    mock_redis = mocker.patch('app.cache.redis_client')
    mock_redis.get.side_effect = redis.ConnectionError("Redis unavailable")

    # La aplicación debe funcionar sin cache
    response = client.get("/cached-endpoint")

    assert response.status_code == 200
    # Verificar que se manejó el error correctamente

def test_database_timeout_mock(client, mocker):
    """Test manejo de timeout de base de datos"""

    # Mock que simula timeout
    from sqlalchemy.exc import TimeoutError
    mock_db = mocker.patch('app.database.get_db')
    mock_db.side_effect = TimeoutError("statement timeout")

    response = client.get("/users")

    assert response.status_code == 503  # Service Unavailable
```

---

### Paso 3: Fixtures Avanzadas y Factories (20 min)

#### Actualizar `tests/conftest.py`

```python
import pytest
import factory
from datetime import datetime, timedelta
from app.models.user import User
from app.auth.password import get_password_hash

class UserFactory(factory.Factory):
    """Factory para crear usuarios de testing"""

    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"user{n}@example.com")
    full_name = factory.Faker('name')
    hashed_password = factory.LazyFunction(lambda: get_password_hash("testpass123"))
    role = "user"
    is_active = True

class AdminUserFactory(UserFactory):
    """Factory para crear administradores"""

    email = factory.Sequence(lambda n: f"admin{n}@example.com")
    role = "admin"

@pytest.fixture
def user_factory():
    """Fixture que retorna la factory de usuarios"""
    return UserFactory

@pytest.fixture
def admin_factory():
    """Fixture que retorna la factory de admins"""
    return AdminUserFactory

@pytest.fixture
def bulk_users(db, user_factory):
    """Fixture que crea múltiples usuarios para testing"""
    users = []
    for i in range(10):
        user = user_factory.create()
        db.add(user)
        users.append(user)

    db.commit()
    return users

@pytest.fixture
def authenticated_client(client, test_user):
    """Cliente autenticado para tests"""
    from app.auth.jwt_handler import create_access_token

    token = create_access_token({"sub": test_user.email})
    client.headers = {"Authorization": f"Bearer {token}"}
    return client

@pytest.fixture
def admin_client(client, admin_user):
    """Cliente con permisos de admin"""
    from app.auth.jwt_handler import create_access_token

    token = create_access_token({"sub": admin_user.email})
    client.headers = {"Authorization": f"Bearer {token}"}
    return client
```

#### Tests usando factories

```python
def test_bulk_user_operations(bulk_users, admin_client):
    """Test operaciones con múltiples usuarios"""

    response = admin_client.get("/admin/users")

    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 10  # Al menos los 10 creados por bulk_users

def test_user_creation_with_factory(db, user_factory):
    """Test creación de usuario usando factory"""

    user = user_factory.create(email="specific@example.com")
    db.add(user)
    db.commit()

    assert user.email == "specific@example.com"
    assert user.role == "user"
    assert user.is_active is True
```

---

### Paso 4: Coverage Analysis y Optimización (15 min)

#### Análisis de coverage detallado

```bash
# Generar reporte detallado
coverage run -m pytest
coverage report --show-missing

# Identificar líneas no cubiertas
coverage html
```

#### Mejorar coverage en áreas críticas

```python
# tests/test_edge_cases.py

def test_invalid_token_formats(client):
    """Test diferentes formatos de token inválidos"""

    invalid_tokens = [
        "",
        "Bearer",
        "Bearer ",
        "Bearer invalid-token",
        "InvalidScheme token",
        "Bearer " + "x" * 1000,  # Token muy largo
    ]

    for token in invalid_tokens:
        response = client.get(
            "/auth/me",
            headers={"Authorization": token}
        )
        assert response.status_code == 401

def test_password_edge_cases(client):
    """Test casos edge de passwords"""

    edge_passwords = [
        "",  # Vacío
        "x",  # Muy corto
        "x" * 1000,  # Muy largo
        "password123",  # Común
        "P@ssw0rd!",  # Complejo
        "😀🔐🚀",  # Emojis
    ]

    for password in edge_passwords:
        response = client.post("/auth/register", json={
            "email": f"test+{len(password)}@example.com",
            "full_name": "Test User",
            "password": password
        })

        # Verificar validación de password
        if len(password) < 8:
            assert response.status_code == 422
        else:
            assert response.status_code in [201, 400]  # Created o email ya existe

def test_database_constraint_violations(client, db):
    """Test violaciones de constraints de base de datos"""

    # Crear usuario inicial
    response1 = client.post("/auth/register", json={
        "email": "unique@example.com",
        "full_name": "First User",
        "password": "password123"
    })
    assert response1.status_code == 201

    # Intentar crear usuario con mismo email
    response2 = client.post("/auth/register", json={
        "email": "unique@example.com",
        "full_name": "Second User",
        "password": "password456"
    })
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"]
```

#### Configurar CI/CD coverage

```yaml
# .github/workflows/test.yml (preview para próxima práctica)
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests with coverage
        run: |
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

---

## ✅ Verificación de Coverage

### Coverage Report Example

```bash
# Ejecutar análisis final
pytest --cov=app --cov-report=term-missing --cov-report=html

# Output esperado:
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
app/__init__.py                   0      0   100%
app/main.py                      45      2    96%   23, 67
app/auth/dependencies.py         30      1    97%   45
app/auth/jwt_handler.py          25      0   100%
app/models/user.py               20      0   100%
app/routers/auth.py              55      3    95%   78, 89, 123
app/routers/admin.py             40      2    95%   67, 89
-----------------------------------------------------------
TOTAL                           215     8    96%
```

### Métricas de Calidad Esperadas

- **Coverage Total**: >95%
- **Branch Coverage**: >90%
- **Missing Lines**: <10 líneas críticas
- **Tests per Module**: Al menos 3-5 tests por archivo

---

## ✅ Checklist de Completado

### **Configuración**

- [ ] **pytest-cov** instalado y configurado
- [ ] **Coverage config** en pyproject.toml
- [ ] **HTML reports** generándose correctamente
- [ ] **Fail-under threshold** configurado en 80%

### **Mocking**

- [ ] **External services** mockeados apropiadamente
- [ ] **Database operations** con mocks para isolation
- [ ] **Authentication dependencies** mockeadas para tests
- [ ] **Error scenarios** cubiertos con mocks

### **Advanced Fixtures**

- [ ] **Factories** para creación de datos de test
- [ ] **Bulk data** fixtures para tests de volumen
- [ ] **Authenticated clients** para tests de endpoints protegidos
- [ ] **Admin clients** para tests de funcionalidad administrativa

### **Coverage Analysis**

- [ ] **Coverage >95%** en módulos críticos
- [ ] **Edge cases** cubiertos con tests específicos
- [ ] **Error handling** verificado con tests
- [ ] **Documentation** de areas no cubiertas

---

## 🎯 Objetivo Alcanzado

**Has implementado testing de nivel profesional** con:

1. **Coverage exhaustivo** con reportes detallados
2. **Mocking estratégico** para isolation de tests
3. **Fixtures avanzadas** para generación de datos
4. **Edge case testing** para robustez
5. **Análisis de calidad** con métricas claras

**🚀 Siguiente:** En la siguiente práctica implementarás cache básico con Redis.

---

## 📚 Conceptos Aplicados

- **Test Coverage Analysis** con métricas cuantificables
- **Mock Objects** para isolation y control
- **Factory Pattern** para generación de datos de test
- **Edge Case Testing** para robustez
- **CI/CD Integration** básica para testing automatizado

**¡Testing avanzado con coverage profesional implementado exitosamente!** 🧪📊✨
