# Práctica 22: Testing Avanzado y Optimización

## Objetivos de Aprendizaje

- Implementar técnicas avanzadas de testing (mocking, fixtures)
- Optimizar performance de tests
- Testing de APIs complejas con autenticación
- Estrategias de testing para deployment

## Duración Estimada

⏱️ **90 minutos**

## Prerrequisitos

- Prácticas 19-21 completadas
- Conocimiento de pytest básico
- Familiaridad con FastAPI y autenticación

---

## 📋 Contenido de la Práctica

### Parte 1: Mocking y Fixtures Avanzados (35 min)

#### 1.1 Configuración de Fixtures Complejos

**Crear tests/conftest.py**

```python
import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base
from app.models.user import User
from app.core.security import get_password_hash
from app.core.config import settings

# Database para testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Crear event loop para testing asíncrono."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_session():
    """Crear sesión de base de datos para tests."""
    # Crear tablas
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP para testing."""
    def get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = get_test_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture
async def test_user(db_session) -> User:
    """Usuario de prueba."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        full_name="Test User",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
async def admin_user(db_session) -> User:
    """Usuario administrador de prueba."""
    user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        full_name="Admin User",
        is_active=True,
        is_superuser=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
async def authenticated_client(client: AsyncClient, test_user: User) -> AsyncClient:
    """Cliente autenticado para testing."""
    # Login para obtener token
    login_data = {
        "username": test_user.email,
        "password": "testpassword"
    }
    response = await client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]

    # Configurar headers de autenticación
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client

@pytest.fixture
async def admin_client(client: AsyncClient, admin_user: User) -> AsyncClient:
    """Cliente administrador autenticado."""
    login_data = {
        "username": admin_user.email,
        "password": "adminpassword"
    }
    response = await client.post("/auth/login", data=login_data)
    token = response.json()["access_token"]

    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
```

#### 1.2 Mocking de Servicios Externos

**Crear tests/test_external_services.py**

```python
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from httpx import AsyncClient

from app.services.email_service import EmailService
from app.services.payment_service import PaymentService
from app.models.user import User

class TestExternalServices:
    """Tests para servicios externos con mocking."""

    @pytest.mark.asyncio
    @patch('app.services.email_service.aiosmtplib.send')
    async def test_send_welcome_email(self, mock_send, test_user: User):
        """Test envío de email de bienvenida."""
        # Configurar mock
        mock_send.return_value = AsyncMock()

        # Instanciar servicio
        email_service = EmailService()

        # Ejecutar
        result = await email_service.send_welcome_email(test_user.email, test_user.full_name)

        # Verificar
        assert result is True
        mock_send.assert_called_once()

        # Verificar argumentos del call
        call_args = mock_send.call_args
        message = call_args[0][0]
        assert test_user.email in str(message["To"])
        assert "Bienvenido" in str(message["Subject"])

    @pytest.mark.asyncio
    @patch('app.services.payment_service.httpx.AsyncClient.post')
    async def test_process_payment_success(self, mock_post):
        """Test procesamiento de pago exitoso."""
        # Configurar mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "success",
            "transaction_id": "txn_123456",
            "amount": 99.99
        }
        mock_post.return_value = mock_response

        # Instanciar servicio
        payment_service = PaymentService()

        # Ejecutar
        result = await payment_service.process_payment(
            amount=99.99,
            currency="USD",
            payment_method_id="pm_test"
        )

        # Verificar
        assert result["status"] == "success"
        assert result["transaction_id"] == "txn_123456"
        mock_post.assert_called_once()

    @pytest.mark.asyncio
    @patch('app.services.payment_service.httpx.AsyncClient.post')
    async def test_process_payment_failure(self, mock_post):
        """Test procesamiento de pago fallido."""
        # Configurar mock para falla
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": "insufficient_funds",
            "message": "Fondos insuficientes"
        }
        mock_post.return_value = mock_response

        payment_service = PaymentService()

        # Verificar que se lanza la excepción esperada
        with pytest.raises(Exception) as exc_info:
            await payment_service.process_payment(
                amount=99.99,
                currency="USD",
                payment_method_id="pm_invalid"
            )

        assert "insufficient_funds" in str(exc_info.value)
```

#### 1.3 Testing con Bases de Datos Temporales

**Crear tests/test_database_operations.py**

```python
import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.crud.user import user_crud
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User

class TestUserCRUD:
    """Tests para operaciones CRUD de usuarios."""

    @pytest.mark.asyncio
    async def test_create_user(self, db_session: Session):
        """Test creación de usuario."""
        user_data = UserCreate(
            email="newuser@example.com",
            password="newpassword",
            full_name="New User"
        )

        user = await user_crud.create(db_session, obj_in=user_data)

        assert user.email == user_data.email
        assert user.full_name == user_data.full_name
        assert user.is_active is True
        assert hasattr(user, "hashed_password")
        assert user.hashed_password != user_data.password

    @pytest.mark.asyncio
    async def test_get_user_by_email(self, db_session: Session, test_user: User):
        """Test obtener usuario por email."""
        user = await user_crud.get_by_email(db_session, email=test_user.email)

        assert user is not None
        assert user.email == test_user.email
        assert user.id == test_user.id

    @pytest.mark.asyncio
    async def test_update_user(self, db_session: Session, test_user: User):
        """Test actualización de usuario."""
        update_data = UserUpdate(full_name="Updated Name")

        updated_user = await user_crud.update(
            db_session,
            db_obj=test_user,
            obj_in=update_data
        )

        assert updated_user.full_name == "Updated Name"
        assert updated_user.email == test_user.email

    @pytest.mark.asyncio
    async def test_delete_user(self, db_session: Session, test_user: User):
        """Test eliminación de usuario."""
        deleted_user = await user_crud.remove(db_session, id=test_user.id)

        assert deleted_user.id == test_user.id

        # Verificar que no existe
        user = await user_crud.get(db_session, id=test_user.id)
        assert user is None

    @pytest.mark.asyncio
    async def test_duplicate_email_error(self, db_session: Session, test_user: User):
        """Test error al crear usuario con email duplicado."""
        user_data = UserCreate(
            email=test_user.email,  # Email ya existe
            password="password",
            full_name="Duplicate User"
        )

        with pytest.raises(HTTPException) as exc_info:
            await user_crud.create(db_session, obj_in=user_data)

        assert exc_info.value.status_code == 400
        assert "already registered" in str(exc_info.value.detail)
```

### Parte 2: Testing de Performance (25 min)

#### 2.1 Tests de Carga Básicos

**Crear tests/test_performance.py**

```python
import pytest
import asyncio
import time
from httpx import AsyncClient
from concurrent.futures import ThreadPoolExecutor

class TestPerformance:
    """Tests de performance y carga."""

    @pytest.mark.asyncio
    async def test_endpoint_response_time(self, client: AsyncClient):
        """Test tiempo de respuesta de endpoint."""
        start_time = time.time()

        response = await client.get("/health")

        end_time = time.time()
        response_time = end_time - start_time

        assert response.status_code == 200
        assert response_time < 1.0  # Menos de 1 segundo

    @pytest.mark.asyncio
    async def test_concurrent_requests(self, authenticated_client: AsyncClient):
        """Test requests concurrentes."""
        async def make_request():
            response = await authenticated_client.get("/users/me")
            return response.status_code

        # Ejecutar 10 requests concurrentes
        tasks = [make_request() for _ in range(10)]
        results = await asyncio.gather(*tasks)

        # Verificar que todas las requests fueron exitosas
        assert all(status == 200 for status in results)

    @pytest.mark.asyncio
    async def test_database_query_performance(self, db_session, test_user):
        """Test performance de consultas a base de datos."""
        # Crear múltiples usuarios para testing
        users = []
        for i in range(100):
            user = User(
                email=f"user{i}@example.com",
                hashed_password="hashedpassword",
                full_name=f"User {i}"
            )
            users.append(user)

        db_session.add_all(users)
        db_session.commit()

        # Medir tiempo de consulta
        start_time = time.time()

        result = db_session.query(User).filter(User.is_active == True).all()

        end_time = time.time()
        query_time = end_time - start_time

        assert len(result) >= 100
        assert query_time < 0.5  # Menos de 500ms

    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_stress_endpoint(self, client: AsyncClient):
        """Test de estrés para endpoint público."""
        success_count = 0
        error_count = 0

        async def make_request():
            nonlocal success_count, error_count
            try:
                response = await client.get("/health")
                if response.status_code == 200:
                    success_count += 1
                else:
                    error_count += 1
            except Exception:
                error_count += 1

        # Ejecutar 50 requests concurrentes
        tasks = [make_request() for _ in range(50)]
        await asyncio.gather(*tasks, return_exceptions=True)

        # Verificar que al menos 90% fueron exitosas
        total_requests = success_count + error_count
        success_rate = success_count / total_requests

        assert success_rate >= 0.9  # 90% de éxito mínimo
```

#### 2.2 Profiling de Tests

**Crear scripts/profile_tests.py**

```python
#!/usr/bin/env python3

import cProfile
import pstats
import subprocess
import sys
from pathlib import Path

def profile_tests():
    """Ejecutar tests con profiling."""
    print("🔍 Ejecutando profiling de tests...")

    # Ejecutar pytest con profiling
    profiler = cProfile.Profile()

    profiler.enable()

    # Ejecutar tests
    result = subprocess.run([
        sys.executable, "-m", "pytest",
        "tests/", "-v", "--tb=short"
    ], capture_output=True, text=True)

    profiler.disable()

    # Guardar estadísticas
    stats_file = "test_profile.stats"
    profiler.dump_stats(stats_file)

    # Generar reporte
    stats = pstats.Stats(stats_file)
    stats.sort_stats('cumulative')

    print("\n📊 Top 10 funciones por tiempo acumulativo:")
    stats.print_stats(10)

    print(f"\n💾 Estadísticas guardadas en: {stats_file}")
    print("🔍 Para análisis detallado:")
    print(f"   python -m pstats {stats_file}")

    return result.returncode == 0

if __name__ == "__main__":
    success = profile_tests()
    sys.exit(0 if success else 1)
```

### Parte 3: Testing en Diferentes Entornos (30 min)

#### 3.1 Configuración Multi-Environment

**Crear tests/environments/test_config.py**

```python
import pytest
import os
from unittest.mock import patch

from app.core.config import Settings

class TestEnvironmentConfigurations:
    """Tests para diferentes configuraciones de entorno."""

    @patch.dict(os.environ, {
        "ENVIRONMENT": "development",
        "DEBUG": "true",
        "DATABASE_URL": "sqlite:///./test_dev.db"
    })
    def test_development_config(self):
        """Test configuración de desarrollo."""
        settings = Settings()

        assert settings.ENVIRONMENT == "development"
        assert settings.DEBUG is True
        assert "sqlite" in settings.DATABASE_URL

    @patch.dict(os.environ, {
        "ENVIRONMENT": "production",
        "DEBUG": "false",
        "DATABASE_URL": "postgresql://user:pass@localhost/prod"
    })
    def test_production_config(self):
        """Test configuración de producción."""
        settings = Settings()

        assert settings.ENVIRONMENT == "production"
        assert settings.DEBUG is False
        assert "postgresql" in settings.DATABASE_URL

    @patch.dict(os.environ, {
        "ENVIRONMENT": "testing",
        "DATABASE_URL": "sqlite:///:memory:"
    })
    def test_testing_config(self):
        """Test configuración de testing."""
        settings = Settings()

        assert settings.ENVIRONMENT == "testing"
        assert settings.DATABASE_URL == "sqlite:///:memory:"
```

#### 3.2 Testing de Deployment

**Crear tests/deployment/test_health_checks.py**

```python
import pytest
from httpx import AsyncClient

class TestDeploymentReadiness:
    """Tests para verificar preparación para deployment."""

    @pytest.mark.asyncio
    async def test_health_endpoint(self, client: AsyncClient):
        """Test endpoint de salud."""
        response = await client.get("/health")

        assert response.status_code == 200

        health_data = response.json()
        assert "status" in health_data
        assert health_data["status"] == "ok"
        assert "timestamp" in health_data

    @pytest.mark.asyncio
    async def test_readiness_endpoint(self, client: AsyncClient):
        """Test endpoint de preparación."""
        response = await client.get("/ready")

        assert response.status_code == 200

        readiness_data = response.json()
        assert "database" in readiness_data
        assert "redis" in readiness_data
        assert readiness_data["database"] == "connected"

    @pytest.mark.asyncio
    async def test_metrics_endpoint(self, client: AsyncClient):
        """Test endpoint de métricas."""
        response = await client.get("/metrics")

        assert response.status_code == 200

        # Verificar formato Prometheus
        metrics_text = response.text
        assert "http_requests_total" in metrics_text
        assert "http_request_duration_seconds" in metrics_text

    @pytest.mark.asyncio
    async def test_cors_headers(self, client: AsyncClient):
        """Test configuración CORS."""
        response = await client.options("/users/", headers={
            "Origin": "https://example.com",
            "Access-Control-Request-Method": "GET"
        })

        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" in response.headers

    @pytest.mark.asyncio
    async def test_security_headers(self, client: AsyncClient):
        """Test headers de seguridad."""
        response = await client.get("/health")

        headers = response.headers
        assert "X-Content-Type-Options" in headers
        assert "X-Frame-Options" in headers
        assert "X-XSS-Protection" in headers
```

#### 3.3 Tests de Integración Completos

**Crear tests/integration/test_full_workflow.py**

```python
import pytest
from httpx import AsyncClient

class TestFullWorkflow:
    """Tests de integración completos."""

    @pytest.mark.asyncio
    async def test_complete_user_journey(self, client: AsyncClient):
        """Test journey completo de usuario."""

        # 1. Registro de usuario
        register_data = {
            "email": "journey@example.com",
            "password": "password123",
            "full_name": "Journey User"
        }

        response = await client.post("/auth/register", json=register_data)
        assert response.status_code == 201

        user_data = response.json()
        assert user_data["email"] == register_data["email"]

        # 2. Login
        login_data = {
            "username": register_data["email"],
            "password": register_data["password"]
        }

        response = await client.post("/auth/login", data=login_data)
        assert response.status_code == 200

        token_data = response.json()
        token = token_data["access_token"]

        # 3. Acceder a perfil con token
        headers = {"Authorization": f"Bearer {token}"}
        response = await client.get("/users/me", headers=headers)
        assert response.status_code == 200

        profile_data = response.json()
        assert profile_data["email"] == register_data["email"]

        # 4. Actualizar perfil
        update_data = {"full_name": "Updated Journey User"}
        response = await client.put("/users/me", json=update_data, headers=headers)
        assert response.status_code == 200

        updated_profile = response.json()
        assert updated_profile["full_name"] == update_data["full_name"]

        # 5. Logout (si implementado)
        response = await client.post("/auth/logout", headers=headers)
        assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_error_handling_workflow(self, client: AsyncClient):
        """Test manejo de errores en workflow."""

        # 1. Intentar acceso sin autenticación
        response = await client.get("/users/me")
        assert response.status_code == 401

        # 2. Login con credenciales incorrectas
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }

        response = await client.post("/auth/login", data=login_data)
        assert response.status_code == 401

        # 3. Registro con email inválido
        register_data = {
            "email": "invalid-email",
            "password": "password123",
            "full_name": "Invalid User"
        }

        response = await client.post("/auth/register", json=register_data)
        assert response.status_code == 422
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Implementar Test Suite Completo

**Objetivo:** Crear suite completo de tests para un endpoint

```python
# Implementar tests para endpoint /items/
# Incluir:
# - Tests unitarios para CRUD
# - Tests de integración con autenticación
# - Tests de performance
# - Mocking de servicios externos
```

### Ejercicio 2: Optimización de Tests

**Objetivo:** Optimizar velocidad de ejecución de tests

```bash
# 1. Identificar tests lentos
pytest --durations=10

# 2. Paralelizar tests
pip install pytest-xdist
pytest -n 4

# 3. Usar marks para categorizar
pytest -m "not slow"
```

### Ejercicio 3: Testing de Error Scenarios

**Objetivo:** Implementar tests para casos de error

```python
# Tests para:
# - Errores de validación
# - Timeouts de servicios externos
# - Fallos de base de datos
# - Errores de autenticación/autorización
```

---

## 📊 Métricas Avanzadas

### Performance Benchmarks

| Métrica               | Objetivo    | Herramienta      |
| --------------------- | ----------- | ---------------- |
| Tiempo de respuesta   | < 200ms     | pytest-benchmark |
| Requests concurrentes | 100+        | asyncio          |
| Throughput            | 1000+ req/s | locust           |
| Memory usage          | < 100MB     | memory-profiler  |

### Coverage Detallado

```bash
# Coverage por módulo
coverage report --show-missing

# Coverage HTML con detalles
coverage html --show-contexts

# Coverage por branches
pytest --cov=app --cov-branch
```

---

## 🚀 Deployment Testing

### Smoke Tests

**Crear tests/smoke/test_production.py**

```python
import pytest
import os
from httpx import AsyncClient

@pytest.mark.skipif(
    os.getenv("ENVIRONMENT") != "production",
    reason="Solo para producción"
)
class TestProductionSmoke:
    """Smoke tests para producción."""

    @pytest.mark.asyncio
    async def test_api_is_alive(self):
        """Test que la API está respondiendo."""
        base_url = os.getenv("API_BASE_URL", "https://api.example.com")

        async with AsyncClient(base_url=base_url) as client:
            response = await client.get("/health")
            assert response.status_code == 200

    @pytest.mark.asyncio
    async def test_database_connectivity(self):
        """Test conectividad con base de datos."""
        # Implementar test de conectividad
        pass
```

### Load Testing

**Crear tests/load/locustfile.py**

```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Login al iniciar."""
        response = self.client.post("/auth/login", data={
            "username": "test@example.com",
            "password": "testpassword"
        })

        if response.status_code == 200:
            token = response.json()["access_token"]
            self.client.headers.update({
                "Authorization": f"Bearer {token}"
            })

    @task(3)
    def get_profile(self):
        """Obtener perfil de usuario."""
        self.client.get("/users/me")

    @task(1)
    def get_health(self):
        """Check health endpoint."""
        self.client.get("/health")
```

---

## ✅ Criterios de Evaluación

### Nivel Básico (60-70%)

- [ ] Implementa fixtures básicos para testing
- [ ] Usa mocking para servicios externos simples
- [ ] Ejecuta tests de performance básicos

### Nivel Intermedio (71-85%)

- [ ] Configura fixtures complejos con bases de datos
- [ ] Implementa tests de integración completos
- [ ] Usa profiling para optimizar tests
- [ ] Configura testing multi-environment

### Nivel Avanzado (86-100%)

- [ ] Implementa suite completo de tests avanzados
- [ ] Configura load testing con Locust
- [ ] Implementa smoke tests para producción
- [ ] Optimiza performance de test suite
- [ ] Integra métricas avanzadas de testing

---

## 📚 Recursos Adicionales

### Herramientas Avanzadas

- **pytest-benchmark**: Performance testing
- **pytest-xdist**: Paralelización de tests
- **locust**: Load testing
- **hypothesis**: Property-based testing
- **factory-boy**: Test data factories

### Mejores Prácticas

1. **Aislamiento**: Tests independientes entre sí
2. **Rapidez**: Test suite que ejecute en < 5 minutos
3. **Claridad**: Tests autodocumentados
4. **Mantenibilidad**: Fixtures reutilizables
5. **Realismo**: Datos de test realistas

---

## 🎯 Próximos Pasos

1. **Implementar** suite completo de tests avanzados
2. **Optimizar** performance del test suite
3. **Configurar** load testing para APIs críticas
4. **Establecer** pipeline de testing en CI/CD
5. **Crear** documentación de testing guidelines

---

_Esta práctica completa el módulo de testing, proporcionando herramientas avanzadas para garantizar la calidad y performance de aplicaciones FastAPI en producción._
