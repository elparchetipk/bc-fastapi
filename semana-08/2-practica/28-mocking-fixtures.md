# Práctica 28: Testing Avanzado de APIs

## 🎯 Objetivo

Dominar técnicas avanzadas de testing en FastAPI incluyendo mocking, fixtures avanzadas y tests de integración en 90 minutos.

## ⏱️ Tiempo: 90 minutos

### 📋 Distribución del tiempo:

- **Fixtures avanzadas y mocking** (25 min)
- **Tests de autenticación** (25 min)
- **Tests de base de datos** (25 min)
- **Tests de integración** (15 min)

## 📋 Pre-requisitos

- ✅ Práctica 27 completada (pytest básico)
- ✅ API con autenticación JWT implementada
- ✅ Base de datos configurada (SQLite/PostgreSQL)
- ✅ Tests básicos funcionando

## 🚀 Desarrollo Paso a Paso

### Paso 1: Fixtures Avanzadas y Mocking (25 min)

#### 1.1 Instalar dependencias adicionales

```bash
pip install pytest-mock faker
```

#### 1.2 Actualizar conftest.py con fixtures avanzadas

```python
# tests/conftest.py
import pytest
from unittest.mock import Mock
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app, get_database
from models import Base
from auth import create_access_token

fake = Faker()

# Base de datos de prueba en memoria
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_db():
    """Base de datos de prueba en memoria"""
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(test_db):
    """Cliente con base de datos de prueba"""
    def override_get_database():
        try:
            yield test_db
        finally:
            test_db.close()

    app.dependency_overrides[get_database] = override_get_database
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def sample_user():
    """Usuario de ejemplo con datos aleatorios"""
    return {
        "name": fake.name(),
        "email": fake.email(),
        "age": fake.random_int(min=18, max=80)
    }

@pytest.fixture
def auth_headers():
    """Headers de autenticación válidos"""
    token = create_access_token(data={"sub": "testuser@example.com"})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def mock_external_api(mocker):
    """Mock para APIs externas"""
    return mocker.patch('requests.get')
```

#### 1.3 Tests con mocking

```python
# tests/test_mocking.py
import pytest
from unittest.mock import patch, Mock

class TestExternalAPIs:
    """Tests que usan mocking para APIs externas"""

    @patch('requests.get')
    def test_external_api_success(self, mock_get, client):
        """Test exitoso de API externa"""
        # Configurar mock
        mock_response = Mock()
        mock_response.json.return_value = {"status": "success"}
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Ejecutar test
        response = client.get("/external-data")

        # Verificar
        assert response.status_code == 200
        mock_get.assert_called_once()

    def test_email_service_mock(self, client, mocker):
        """Test con mock del servicio de email"""
        mock_send = mocker.patch('services.email.send_email')
        mock_send.return_value = True

        response = client.post("/users", json={
            "name": "Test User",
            "email": "test@example.com"
        })

        assert response.status_code == 201
        mock_send.assert_called_once_with("test@example.com")
```

---

### Paso 2: Tests de Autenticación (25 min)

#### 2.1 Tests de login y JWT

```python
# tests/test_auth.py
import pytest
from datetime import datetime, timedelta
from jose import jwt

class TestAuthentication:
    """Tests para sistema de autenticación"""

    def test_login_success(self, client, test_db):
        """Test login exitoso"""
        # Crear usuario de prueba
        user_data = {
            "email": "testuser@example.com",
            "password": "testpass123"
        }
        client.post("/register", json=user_data)

        # Intentar login
        response = client.post("/login", data={
            "username": user_data["email"],
            "password": user_data["password"]
        })

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        """Test login con credenciales inválidas"""
        response = client.post("/login", data={
            "username": "invalid@example.com",
            "password": "wrongpass"
        })

        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()

    def test_protected_endpoint_without_token(self, client):
        """Test acceso a endpoint protegido sin token"""
        response = client.get("/protected")
        assert response.status_code == 401

    def test_protected_endpoint_with_token(self, client, auth_headers):
        """Test acceso a endpoint protegido con token válido"""
        response = client.get("/protected", headers=auth_headers)
        assert response.status_code == 200

    def test_invalid_token(self, client):
        """Test con token inválido"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/protected", headers=headers)
        assert response.status_code == 401

    def test_expired_token(self, client):
        """Test con token expirado"""
        # Crear token expirado
        expired_token = jwt.encode(
            {"sub": "test@example.com", "exp": datetime.utcnow() - timedelta(hours=1)},
            "secret_key",
            algorithm="HS256"
        )
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get("/protected", headers=headers)
        assert response.status_code == 401
```

---

### Paso 3: Tests de Base de Datos (25 min)

#### 3.1 Tests CRUD con base de datos

```python
# tests/test_database.py
import pytest

class TestDatabaseOperations:
    """Tests para operaciones de base de datos"""

    def test_create_user_in_db(self, client, sample_user, test_db):
        """Test creación de usuario en BD"""
        response = client.post("/users", json=sample_user)
        assert response.status_code == 201

        # Verificar que se guardó en BD
        user_id = response.json()["id"]
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 200
        assert get_response.json()["email"] == sample_user["email"]

    def test_user_duplicate_email(self, client, sample_user):
        """Test usuario con email duplicado"""
        # Crear primer usuario
        client.post("/users", json=sample_user)

        # Intentar crear segundo usuario con mismo email
        response = client.post("/users", json=sample_user)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_update_user(self, client, sample_user):
        """Test actualización de usuario"""
        # Crear usuario
        create_response = client.post("/users", json=sample_user)
        user_id = create_response.json()["id"]

        # Actualizar usuario
        updated_data = {"name": "Updated Name"}
        response = client.put(f"/users/{user_id}", json=updated_data)

        assert response.status_code == 200
        assert response.json()["name"] == "Updated Name"

    def test_delete_user(self, client, sample_user):
        """Test eliminación de usuario"""
        # Crear usuario
        create_response = client.post("/users", json=sample_user)
        user_id = create_response.json()["id"]

        # Eliminar usuario
        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204

        # Verificar que no existe
        get_response = client.get(f"/users/{user_id}")
        assert get_response.status_code == 404

class TestDatabaseConstraints:
    """Tests para restricciones de base de datos"""

    def test_user_email_validation(self, client):
        """Test validación de email en BD"""
        invalid_user = {
            "name": "Test User",
            "email": "invalid-email",
            "age": 25
        }
        response = client.post("/users", json=invalid_user)
        assert response.status_code == 422

    def test_required_fields(self, client):
        """Test campos requeridos"""
        incomplete_user = {"name": "Test User"}
        response = client.post("/users", json=incomplete_user)
        assert response.status_code == 422
```

---

### Paso 4: Tests de Integración (15 min)

#### 4.1 Tests de flujo completo

```python
# tests/test_integration.py
import pytest

class TestUserWorkflow:
    """Tests de flujo completo de usuario"""

    def test_complete_user_lifecycle(self, client):
        """Test del ciclo completo: registro -> login -> operaciones -> logout"""
        # 1. Registro
        user_data = {
            "name": "Integration User",
            "email": "integration@example.com",
            "password": "testpass123"
        }
        register_response = client.post("/register", json=user_data)
        assert register_response.status_code == 201

        # 2. Login
        login_response = client.post("/login", data={
            "username": user_data["email"],
            "password": user_data["password"]
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 3. Operaciones autenticadas
        profile_response = client.get("/users/me", headers=headers)
        assert profile_response.status_code == 200
        assert profile_response.json()["email"] == user_data["email"]

        # 4. Actualizar perfil
        update_response = client.put("/users/me",
                                   json={"name": "Updated Name"},
                                   headers=headers)
        assert update_response.status_code == 200

    def test_api_error_handling(self, client, auth_headers):
        """Test manejo de errores en flujo de API"""
        # Test 404
        response = client.get("/users/999999", headers=auth_headers)
        assert response.status_code == 404

        # Test 422
        response = client.post("/users", json={"invalid": "data"}, headers=auth_headers)
        assert response.status_code == 422

        # Test 403 (si aplica)
        response = client.delete("/admin/users/1", headers=auth_headers)
        assert response.status_code in [403, 404]  # Dependiendo de tu implementación
```

#### 4.2 Ejecutar todos los tests

```bash
# Ejecutar todos los tests
pytest -v

# Ejecutar con coverage
pytest --cov=. --cov-report=html

# Ejecutar solo tests de integración
pytest tests/test_integration.py -v
```

## 🎯 Ejercicios Rápidos

### Ejercicio 1: Mock Personalizado (5 min)

Crea un mock para una dependencia específica de tu API.

### Ejercicio 2: Test de Validación (5 min)

Agrega un test para validar un campo específico de tu modelo.

## ✅ Entregables

Al finalizar esta práctica debes tener:

1. ✅ **Fixtures avanzadas** configuradas
2. ✅ **Tests con mocking** funcionando
3. ✅ **Tests de autenticación** completos
4. ✅ **Tests de base de datos** implementados
5. ✅ **Tests de integración** ejecutándose

## 📚 Recursos de Apoyo

- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)
- [FastAPI Testing - Advanced](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Faker Documentation](https://faker.readthedocs.io/)

## 🔗 Próxima Práctica

En la siguiente práctica trabajaremos con **cobertura de código** y **documentación de tests**.

---

💡 **Tip**: Los mocks son poderosos, pero úsalos solo cuando sea necesario. Tests reales son más confiables.
