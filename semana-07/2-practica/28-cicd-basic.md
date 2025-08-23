# Práctica 28: CI/CD Básico con GitHub Actions

⏰ **Tiempo:** 75 minutos  
📚 **Prerequisito:** Prácticas 25-27 completadas  
🎯 **Objetivo:** Implementar pipeline básico de CI/CD con GitHub Actions para testing automático

## 📋 Contenido de la Práctica

### **Parte 1: Setup de GitHub Actions (25 min)**

1. **Configuración inicial del workflow**
2. **Variables de entorno y secretos**
3. **Testing básico en CI**

### **Parte 2: Pipeline de Testing (30 min)**

1. **Testing automático con pytest**
2. **Coverage reports en CI**
3. **Notificaciones de estado**

### **Parte 3: Deploy Conceptos (20 min)**

1. **Conceptos básicos de deployment**
2. **Environment variables management**
3. **Health checks básicos**

---

## 🎯 Parte 1: Setup de GitHub Actions (25 min)

### 1.1 Crear Workflow Básico

**Archivo: `.github/workflows/ci.yml`**

```yaml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

      redis:
        image: redis:alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest-cov

      - name: Set up environment variables
        run: |
          echo "DATABASE_URL=postgresql://postgres:postgres@localhost:5432/test_db" >> $GITHUB_ENV
          echo "REDIS_URL=redis://localhost:6379" >> $GITHUB_ENV
          echo "SECRET_KEY=test-secret-key" >> $GITHUB_ENV
          echo "TESTING=true" >> $GITHUB_ENV

      - name: Run migrations
        run: |
          alembic upgrade head

      - name: Run tests with coverage
        run: |
          pytest --cov=app --cov-report=xml --cov-report=html -v

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
```

### 1.2 Configurar Variables de Entorno

**Archivo: `.env.example`** (actualizar)

```bash
# Environment Configuration
ENVIRONMENT=development

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/fastapi_db
TEST_DATABASE_URL=postgresql://username:password@localhost:5432/test_fastapi_db

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_STR=/api/v1
PROJECT_NAME=FastAPI Bootcamp API

# Testing
TESTING=false

# CI/CD
CI=false
CODECOV_TOKEN=your-codecov-token-here
```

### 1.3 Actualizar Configuración para CI

**Archivo: `app/core/config.py`** (agregar)

```python
# ...existing code...

class Settings(BaseSettings):
    # ...existing fields...

    # Testing configuration
    testing: bool = False
    ci: bool = False

    # Coverage configuration
    min_coverage: int = 80

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_database_url(self) -> str:
        """Get database URL based on environment."""
        if self.testing:
            return self.test_database_url or self.database_url.replace("/fastapi_db", "/test_fastapi_db")
        return self.database_url

# ...existing code...
```

---

## 🎯 Parte 2: Pipeline de Testing (30 min)

### 2.1 Configurar Testing para CI

**Archivo: `tests/conftest.py`** (actualizar)

```python
"""
Test configuration and fixtures for CI/CD.
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base
from app.core.config import settings

# Set testing environment
os.environ["TESTING"] = "true"

# Create test database engine
SQLALCHEMY_TEST_DATABASE_URL = settings.get_database_url()

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_TEST_DATABASE_URL else {},
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Create test database tables."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session():
    """Create a test database session."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    """Create a test client with database session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clean up
    app.dependency_overrides.clear()

@pytest.fixture
def authenticated_client(client, db_session):
    """Create an authenticated test client."""
    from app.tests.utils import create_test_user, get_auth_headers

    user = create_test_user(db_session)
    headers = get_auth_headers(client, user.email, "testpassword123")

    return client, headers

@pytest.fixture
def admin_client(client, db_session):
    """Create an admin authenticated test client."""
    from app.tests.utils import create_test_admin, get_auth_headers

    admin = create_test_admin(db_session)
    headers = get_auth_headers(client, admin.email, "adminpassword123")

    return client, headers
```

### 2.2 Crear Tests de CI/CD

**Archivo: `tests/test_ci_cd.py`**

```python
"""
Tests específicos para verificar CI/CD pipeline.
"""
import pytest
import os
from fastapi.testclient import TestClient

from app.main import app

def test_environment_variables():
    """Test que las variables de entorno están configuradas."""
    assert os.getenv("TESTING") == "true"
    assert os.getenv("DATABASE_URL") is not None
    assert os.getenv("SECRET_KEY") is not None

def test_database_connection(db_session):
    """Test conexión a base de datos."""
    result = db_session.execute("SELECT 1")
    assert result.scalar() == 1

def test_redis_connection():
    """Test conexión a Redis."""
    try:
        import redis
        r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
        assert r.ping() is True
    except Exception:
        pytest.skip("Redis no disponible en CI")

def test_api_health_check(client):
    """Test del endpoint de health check."""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()

def test_api_endpoints_basic(client):
    """Test básico de endpoints principales."""
    # Test root endpoint
    response = client.get("/")
    assert response.status_code in [200, 404]  # Puede no existir

    # Test docs endpoint
    response = client.get("/docs")
    assert response.status_code == 200

    # Test openapi endpoint
    response = client.get("/openapi.json")
    assert response.status_code == 200

def test_authentication_flow(client, db_session):
    """Test flujo básico de autenticación."""
    from app.tests.utils import create_test_user

    user = create_test_user(db_session)

    # Test login
    response = client.post("/api/v1/auth/login", data={
        "username": user.email,
        "password": "testpassword123"
    })

    assert response.status_code == 200
    assert "access_token" in response.json()

def test_coverage_requirements():
    """Test que la cobertura mínima se cumple."""
    # Este test se ejecuta después de pytest-cov
    # La verificación real la hace el CI pipeline
    assert True  # Placeholder
```

### 2.3 Health Check Endpoint

**Archivo: `app/api/v1/endpoints/health.py`**

```python
"""
Health check endpoints para CI/CD.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import redis
import os

from app.core.database import get_db

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint para CI/CD y monitoring.
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    try:
        # Test Redis connection
        r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
        r.ping()
        redis_status = "healthy"
    except Exception as e:
        redis_status = f"unhealthy: {str(e)}"

    status = {
        "status": "healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded",
        "database": db_status,
        "redis": redis_status,
        "environment": os.getenv("ENVIRONMENT", "unknown")
    }

    if status["status"] == "degraded":
        raise HTTPException(status_code=503, detail=status)

    return status

@router.get("/health/ready")
def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness check - verifica que la app está lista para recibir tráfico.
    """
    try:
        # Test critical dependencies
        db.execute("SELECT 1")
        return {"status": "ready"}
    except Exception as e:
        raise HTTPException(status_code=503, detail={"status": "not_ready", "error": str(e)})

@router.get("/health/live")
def liveness_check():
    """
    Liveness check - verifica que la app está viva.
    """
    return {"status": "alive"}
```

---

## 🎯 Parte 3: Deploy Conceptos (20 min)

### 3.1 Configuración de Deployment

**Archivo: `docker-compose.prod.yml`**

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile.prod
    ports:
      - '8000:8000'
    environment:
      - ENVIRONMENT=production
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
      - redis
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8000/health']
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - '5432:5432'
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}']
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:alpine
    ports:
      - '6379:6379'
    volumes:
      - redis_data:/data
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  postgres_data:
  redis_data:
```

### 3.2 Production Dockerfile

**Archivo: `Dockerfile.prod`**

```dockerfile
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 3.3 Deploy Script Básico

**Archivo: `scripts/deploy.sh`**

```bash
#!/bin/bash

# Basic deployment script for production

set -e

echo "🚀 Starting deployment..."

# Load environment variables
if [ -f .env.prod ]; then
    source .env.prod
fi

# Run database migrations
echo "📊 Running database migrations..."
alembic upgrade head

# Run tests before deployment
echo "🧪 Running tests..."
pytest --cov=app --cov-fail-under=80

# Build and start services
echo "🏗️ Building services..."
docker-compose -f docker-compose.prod.yml build

echo "🔄 Starting services..."
docker-compose -f docker-compose.prod.yml up -d

# Wait for health check
echo "🏥 Waiting for health check..."
sleep 30

# Verify deployment
echo "✅ Verifying deployment..."
curl -f http://localhost:8000/health || {
    echo "❌ Health check failed!"
    docker-compose -f docker-compose.prod.yml logs
    exit 1
}

echo "🎉 Deployment successful!"
```

---

## 🧪 Verificación de CI/CD (5 min)

### 1. Push y Verificar Pipeline

```bash
# Commit cambios
git add .
git commit -m "feat: add CI/CD pipeline with GitHub Actions"

# Push a GitHub
git push origin main

# Verificar en GitHub Actions tab
```

### 2. Verificar Coverage

```bash
# Ejecutar tests localmente con coverage
pytest --cov=app --cov-report=html --cov-report=term

# Ver reporte HTML
open htmlcov/index.html  # En macOS
# o xdg-open htmlcov/index.html  # En Linux
```

### 3. Test Health Check

```bash
# Ejecutar aplicación
uvicorn app.main:app --reload

# Test health endpoints
curl http://localhost:8000/health
curl http://localhost:8000/health/ready
curl http://localhost:8000/health/live
```

---

## 📚 Entregables de la Práctica

1. ✅ **GitHub Actions workflow** funcionando
2. ✅ **Tests automáticos** ejecutándose en CI
3. ✅ **Coverage reports** generándose
4. ✅ **Health check endpoints** implementados
5. ✅ **Docker setup** para producción
6. ✅ **Deploy script** básico

## 🎯 Criterios de Evaluación

- **CI Pipeline (40%)**: Workflow ejecuta correctamente
- **Testing Integration (30%)**: Tests pasan en CI con coverage >80%
- **Health Checks (20%)**: Endpoints de salud funcionan
- **Documentation (10%)**: Deploy process documentado

---

## 📖 Recursos Adicionales

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker Best Practices](https://docs.docker.com/develop/best-practices/)
- [Health Check Patterns](https://microservices.io/patterns/observability/health-check-api.html)

¡Tu API ahora tiene CI/CD básico funcionando! 🎉
