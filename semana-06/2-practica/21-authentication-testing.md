# Práctica 21: Testing con Autenticación

⏰ **Tiempo:** 90 minutos  
📚 **Prerequisito:** Prácticas 19-20 completadas  
🎯 **Objetivo:** Implementar testing para endpoints protegidos y autenticación

## 📋 Contenido de la Práctica

### **Parte 1: Testing de Autenticación (30 min)**

1. **Setup para Testing de Auth**
2. **Tests de Login/Registro**
3. **Fixtures para Tokens**

### **Parte 2: Testing de Endpoints Protegidos (45 min)**

1. **Headers de Autorización**
2. **Testing con Usuarios Mock**
3. **Casos de Autenticación Fallida**

### **Parte 3: Organización Avanzada (15 min)**

1. **Fixtures Compartidas**
2. **Helpers para Auth**
3. **Cleanup de Tests**

---

## 🎯 Parte 1: Testing de Autenticación (30 min)

### 1.1 Setup para Testing de Auth

Primero, configuramos fixtures específicas para autenticación:

**Archivo: `tests/conftest.py`** (actualizar)

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models.user import User
from app.auth.password import get_password_hash
from app.auth.jwt_handler import create_access_token

# Database de testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db():
    """Fixture para sesión de base de datos de testing."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    """Fixture para cliente de testing con DB."""
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(db):
    """Fixture para usuario de testing."""
    user_data = {
        "email": "test@example.com",
        "full_name": "Test User",
        "hashed_password": get_password_hash("testpassword123")
    }
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def auth_headers(test_user):
    """Fixture para headers de autenticación."""
    token = create_access_token({"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def admin_user(db):
    """Fixture para usuario administrador."""
    user_data = {
        "email": "admin@example.com",
        "full_name": "Admin User",
        "hashed_password": get_password_hash("adminpass123"),
        "is_admin": True
    }
    user = User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@pytest.fixture
def admin_headers(admin_user):
    """Fixture para headers de administrador."""
    token = create_access_token({"sub": admin_user.email})
    return {"Authorization": f"Bearer {token}"}
```

### 1.2 Tests de Login/Registro

**Archivo: `tests/test_auth.py`** (crear)

```python
import pytest
from fastapi.testclient import TestClient

def test_register_user_success(client):
    """Test registro de usuario exitoso."""
    user_data = {
        "email": "newuser@example.com",
        "password": "newpassword123",
        "full_name": "New User"
    }

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["full_name"] == user_data["full_name"]
    assert "id" in data
    assert "hashed_password" not in data  # No debe retornar password

def test_register_user_duplicate_email(client, test_user):
    """Test registro con email duplicado."""
    user_data = {
        "email": test_user.email,  # Email que ya existe
        "password": "password123",
        "full_name": "Duplicate User"
    }

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

def test_register_invalid_email(client):
    """Test registro con email inválido."""
    user_data = {
        "email": "invalid-email",
        "password": "password123",
        "full_name": "Invalid User"
    }

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 422

def test_login_success(client, test_user):
    """Test login exitoso."""
    login_data = {
        "username": test_user.email,  # OAuth2 usa 'username'
        "password": "testpassword123"
    }

    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    """Test login con contraseña incorrecta."""
    login_data = {
        "username": test_user.email,
        "password": "wrongpassword"
    }

    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()

def test_login_nonexistent_user(client):
    """Test login con usuario inexistente."""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "password123"
    }

    response = client.post("/auth/login", data=login_data)

    assert response.status_code == 401

@pytest.mark.parametrize("email,password,expected_status", [
    ("", "password123", 422),  # Email vacío
    ("test@example.com", "", 422),  # Password vacío
    ("invalid-email", "password123", 422),  # Email inválido
])
def test_login_validation_errors(client, email, password, expected_status):
    """Test validaciones de login."""
    login_data = {"username": email, "password": password}
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == expected_status
```

---

## 🎯 Parte 2: Testing de Endpoints Protegidos (45 min)

### 2.1 Headers de Autorización

**Archivo: `tests/test_protected_endpoints.py`** (crear)

```python
import pytest
from fastapi.testclient import TestClient

class TestProtectedEndpoints:
    """Tests para endpoints que requieren autenticación."""

    def test_get_profile_success(self, client, auth_headers):
        """Test obtener perfil con autenticación válida."""
        response = client.get("/users/me", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "email" in data
        assert "full_name" in data
        assert "id" in data
        assert "hashed_password" not in data

    def test_get_profile_no_auth(self, client):
        """Test obtener perfil sin autenticación."""
        response = client.get("/users/me")

        assert response.status_code == 401
        assert "Not authenticated" in response.json()["detail"]

    def test_get_profile_invalid_token(self, client):
        """Test obtener perfil con token inválido."""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/users/me", headers=headers)

        assert response.status_code == 401

    def test_update_profile_success(self, client, auth_headers):
        """Test actualizar perfil con autenticación."""
        update_data = {
            "full_name": "Updated Name",
            "email": "updated@example.com"
        }

        response = client.put("/users/me", json=update_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["full_name"] == update_data["full_name"]
        assert data["email"] == update_data["email"]

    def test_update_profile_no_auth(self, client):
        """Test actualizar perfil sin autenticación."""
        update_data = {"full_name": "Updated Name"}
        response = client.put("/users/me", json=update_data)

        assert response.status_code == 401

class TestTasksAuth:
    """Tests para endpoints de tasks con autenticación."""

    def test_create_task_success(self, client, auth_headers):
        """Test crear task con autenticación."""
        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high"
        }

        response = client.post("/tasks/", json=task_data, headers=auth_headers)

        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["user_id"] is not None

    def test_create_task_no_auth(self, client):
        """Test crear task sin autenticación."""
        task_data = {"title": "Test Task", "description": "Test Description"}
        response = client.post("/tasks/", json=task_data)

        assert response.status_code == 401

    def test_get_user_tasks(self, client, auth_headers):
        """Test obtener tasks del usuario autenticado."""
        # Primero crear una task
        task_data = {"title": "User Task", "description": "User Task Description"}
        client.post("/tasks/", json=task_data, headers=auth_headers)

        # Obtener tasks del usuario
        response = client.get("/tasks/me", headers=auth_headers)

        assert response.status_code == 200
        tasks = response.json()
        assert isinstance(tasks, list)
        assert len(tasks) >= 1
        assert tasks[0]["title"] == task_data["title"]

    def test_update_own_task(self, client, auth_headers):
        """Test actualizar task propia."""
        # Crear task
        task_data = {"title": "Original Task", "description": "Original Description"}
        create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
        task_id = create_response.json()["id"]

        # Actualizar task
        update_data = {"title": "Updated Task", "completed": True}
        response = client.put(f"/tasks/{task_id}", json=update_data, headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == update_data["title"]
        assert data["completed"] == True

    def test_delete_own_task(self, client, auth_headers):
        """Test eliminar task propia."""
        # Crear task
        task_data = {"title": "Task to Delete", "description": "Will be deleted"}
        create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
        task_id = create_response.json()["id"]

        # Eliminar task
        response = client.delete(f"/tasks/{task_id}", headers=auth_headers)

        assert response.status_code == 204

        # Verificar que no existe
        get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404
```

### 2.2 Testing con Usuarios Mock

**Archivo: `tests/test_user_isolation.py`** (crear)

```python
import pytest
from fastapi.testclient import TestClient

class TestUserIsolation:
    """Tests para verificar aislamiento entre usuarios."""

    @pytest.fixture
    def second_user(self, db):
        """Fixture para segundo usuario."""
        from app.models.user import User
        from app.auth.password import get_password_hash

        user_data = {
            "email": "second@example.com",
            "full_name": "Second User",
            "hashed_password": get_password_hash("secondpass123")
        }
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @pytest.fixture
    def second_auth_headers(self, second_user):
        """Headers para segundo usuario."""
        from app.auth.jwt_handler import create_access_token
        token = create_access_token({"sub": second_user.email})
        return {"Authorization": f"Bearer {token}"}

    def test_users_see_only_own_tasks(self, client, auth_headers, second_auth_headers):
        """Test que usuarios solo ven sus propias tasks."""
        # Usuario 1 crea una task
        task1_data = {"title": "User 1 Task", "description": "Task by user 1"}
        client.post("/tasks/", json=task1_data, headers=auth_headers)

        # Usuario 2 crea una task
        task2_data = {"title": "User 2 Task", "description": "Task by user 2"}
        client.post("/tasks/", json=task2_data, headers=second_auth_headers)

        # Usuario 1 obtiene sus tasks
        response1 = client.get("/tasks/me", headers=auth_headers)
        user1_tasks = response1.json()

        # Usuario 2 obtiene sus tasks
        response2 = client.get("/tasks/me", headers=second_auth_headers)
        user2_tasks = response2.json()

        # Verificaciones
        assert len(user1_tasks) == 1
        assert len(user2_tasks) == 1
        assert user1_tasks[0]["title"] == "User 1 Task"
        assert user2_tasks[0]["title"] == "User 2 Task"

    def test_cannot_access_other_user_task(self, client, auth_headers, second_auth_headers):
        """Test que un usuario no puede acceder a tasks de otro usuario."""
        # Usuario 1 crea una task
        task_data = {"title": "Private Task", "description": "Only for user 1"}
        create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
        task_id = create_response.json()["id"]

        # Usuario 2 intenta acceder a la task del usuario 1
        response = client.get(f"/tasks/{task_id}", headers=second_auth_headers)

        assert response.status_code == 404  # O 403 según implementación

    def test_cannot_modify_other_user_task(self, client, auth_headers, second_auth_headers):
        """Test que un usuario no puede modificar tasks de otro usuario."""
        # Usuario 1 crea una task
        task_data = {"title": "Original Task", "description": "Original"}
        create_response = client.post("/tasks/", json=task_data, headers=auth_headers)
        task_id = create_response.json()["id"]

        # Usuario 2 intenta modificar la task del usuario 1
        update_data = {"title": "Hacked Task", "description": "Hacked"}
        response = client.put(f"/tasks/{task_id}", json=update_data, headers=second_auth_headers)

        assert response.status_code in [403, 404]  # Forbidden o Not Found
```

---

## 🎯 Parte 3: Organización Avanzada (15 min)

### 3.1 Fixtures Compartidas

**Archivo: `tests/fixtures/auth_fixtures.py`** (crear)

```python
"""Fixtures específicas para autenticación."""
import pytest
from app.models.user import User
from app.auth.password import get_password_hash
from app.auth.jwt_handler import create_access_token

@pytest.fixture
def user_factory(db):
    """Factory para crear usuarios de testing."""
    def _create_user(email="test@example.com", password="testpass123", **kwargs):
        user_data = {
            "email": email,
            "hashed_password": get_password_hash(password),
            "full_name": kwargs.get("full_name", "Test User"),
            **kwargs
        }
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    return _create_user

@pytest.fixture
def auth_factory():
    """Factory para crear headers de autenticación."""
    def _create_auth_headers(user_email):
        token = create_access_token({"sub": user_email})
        return {"Authorization": f"Bearer {token}"}
    return _create_auth_headers
```

### 3.2 Helpers para Auth

**Archivo: `tests/helpers/auth_helpers.py`** (crear)

```python
"""Helpers para testing de autenticación."""
from typing import Dict, Any
from fastapi.testclient import TestClient

def login_user(client: TestClient, email: str, password: str) -> Dict[str, Any]:
    """Helper para hacer login y obtener token."""
    login_data = {"username": email, "password": password}
    response = client.post("/auth/login", data=login_data)
    return response.json()

def create_authenticated_user(client: TestClient, user_data: Dict[str, Any]) -> Dict[str, Any]:
    """Helper para crear usuario y obtener token en un paso."""
    # Registrar usuario
    register_response = client.post("/auth/register", json=user_data)
    if register_response.status_code != 201:
        raise Exception(f"Failed to create user: {register_response.json()}")

    # Hacer login
    token_data = login_user(client, user_data["email"], user_data["password"])

    return {
        "user": register_response.json(),
        "token": token_data["access_token"],
        "headers": {"Authorization": f"Bearer {token_data['access_token']}"}
    }

def assert_unauthorized(response):
    """Helper para verificar respuesta de no autorizado."""
    assert response.status_code == 401
    assert "detail" in response.json()

def assert_forbidden(response):
    """Helper para verificar respuesta de prohibido."""
    assert response.status_code == 403
    assert "detail" in response.json()
```

### 3.3 Cleanup de Tests

**Actualizar `tests/conftest.py`:**

```python
# ... código anterior ...

@pytest.fixture(autouse=True)
def cleanup_database(db):
    """Limpia la base de datos después de cada test."""
    yield
    # Limpiar todas las tablas en orden correcto (por foreign keys)
    db.execute("DELETE FROM tasks")
    db.execute("DELETE FROM users")
    db.commit()

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup inicial para el ambiente de testing."""
    print("\n🧪 Iniciando ambiente de testing...")
    yield
    print("\n✅ Tests completados, limpiando ambiente...")
```

---

## ✅ Checklist de Verificación

### **Testing de Autenticación**

- [ ] Tests de registro (exitoso, email duplicado, validaciones)
- [ ] Tests de login (exitoso, credenciales incorrectas)
- [ ] Fixtures para usuarios y tokens
- [ ] Tests parametrizados para casos edge

### **Endpoints Protegidos**

- [ ] Tests con headers de autorización válidos
- [ ] Tests sin autenticación (401)
- [ ] Tests con tokens inválidos
- [ ] Verificación de aislamiento entre usuarios

### **Organización**

- [ ] Fixtures reutilizables organizadas
- [ ] Helpers para operaciones comunes
- [ ] Cleanup automático de base de datos
- [ ] Estructura clara de tests por módulo

---

## 🚨 Troubleshooting Común

### **Error: "Token has expired"**

```python
# En conftest.py, crear tokens con tiempo suficiente
token = create_access_token(
    {"sub": user.email},
    expires_delta=timedelta(hours=1)  # Suficiente para tests
)
```

### **Error: "Database locked"**

```python
# Usar StaticPool para SQLite en tests
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Importante para tests
)
```

### **Error: "User already exists"**

```python
# Limpiar DB entre tests
@pytest.fixture(autouse=True)
def cleanup_database(db):
    yield
    db.execute("DELETE FROM tasks")
    db.execute("DELETE FROM users")
    db.commit()
```

---

## 🎯 Puntos Clave

1. **Fixtures son fundamentales** para testing de auth
2. **Aislamiento entre usuarios** es crítico
3. **Cleanup automático** evita problemas
4. **Headers de autorización** deben ser consistentes
5. **Testing de casos negativos** es igual de importante

¡Continúa con la **Práctica 22: Coverage y Calidad**! 🚀
