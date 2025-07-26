# Práctica 29: Configuración de Producción

## 📋 Descripción

Aprende a configurar aplicaciones FastAPI para entornos de producción, gestionando variables de entorno, secrets, y configuraciones específicas de cada ambiente.

## 🎯 Objetivos Específicos

- ✅ Gestionar configuraciones por ambiente
- ✅ Implementar manejo seguro de secrets
- ✅ Configurar logging y monitoreo
- ✅ Optimizar performance para producción

## ⏱️ Tiempo Estimado: 75 minutos

---

## 📚 Conceptos Clave

### 🔧 **Configuration Management**

**Principios fundamentales:**

- **12-Factor App**: Configuración en variables de entorno
- **Separation of Concerns**: Config vs. código
- **Environment Parity**: Consistency entre ambientes
- **Security First**: Secrets nunca en código

### 🏗️ **Ambientes Típicos**

```yaml
# Jerarquía de ambientes
Development: Desarrollo local
Testing: Testing automatizado
Staging: Pre-producción
Production: Producción real
```

---

## 🛠️ Desarrollo Práctico

### **Paso 1: Estructura de Configuración**

Crea la estructura base:

```python
# app/core/config.py
from pydantic import BaseSettings, Field, validator
from typing import Optional, List
import os
from functools import lru_cache

class Settings(BaseSettings):
    """Configuración de la aplicación usando Pydantic Settings."""

    # Application
    app_name: str = Field("FastAPI Production App", env="APP_NAME")
    app_version: str = Field("1.0.0", env="APP_VERSION")
    debug: bool = Field(False, env="DEBUG")
    environment: str = Field("production", env="ENVIRONMENT")

    # Server
    host: str = Field("0.0.0.0", env="HOST")
    port: int = Field(8000, env="PORT")
    reload: bool = Field(False, env="RELOAD")
    workers: int = Field(4, env="WORKERS")

    # Security
    secret_key: str = Field(..., env="SECRET_KEY")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    algorithm: str = Field("HS256", env="ALGORITHM")

    # Database
    database_url: str = Field(..., env="DATABASE_URL")
    database_echo: bool = Field(False, env="DATABASE_ECHO")
    database_pool_size: int = Field(5, env="DATABASE_POOL_SIZE")
    database_max_overflow: int = Field(10, env="DATABASE_MAX_OVERFLOW")

    # Redis
    redis_url: str = Field("redis://localhost:6379", env="REDIS_URL")
    redis_expire: int = Field(3600, env="REDIS_EXPIRE")

    # CORS
    cors_origins: List[str] = Field(["*"], env="CORS_ORIGINS")
    cors_allow_credentials: bool = Field(True, env="CORS_ALLOW_CREDENTIALS")
    cors_allow_methods: List[str] = Field(["*"], env="CORS_ALLOW_METHODS")
    cors_allow_headers: List[str] = Field(["*"], env="CORS_ALLOW_HEADERS")

    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")

    # Monitoring
    sentry_dsn: Optional[str] = Field(None, env="SENTRY_DSN")
    prometheus_enabled: bool = Field(True, env="PROMETHEUS_ENABLED")

    # Rate Limiting
    rate_limit_requests: int = Field(100, env="RATE_LIMIT_REQUESTS")
    rate_limit_window: int = Field(60, env="RATE_LIMIT_WINDOW")

    # File Upload
    max_file_size: int = Field(10 * 1024 * 1024, env="MAX_FILE_SIZE")  # 10MB
    upload_path: str = Field("/tmp/uploads", env="UPLOAD_PATH")

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @validator("cors_allow_methods", pre=True)
    def parse_cors_methods(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @validator("cors_allow_headers", pre=True)
    def parse_cors_headers(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    @validator("environment")
    def validate_environment(cls, v):
        allowed = ["development", "testing", "staging", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of: {allowed}")
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

@lru_cache()
def get_settings() -> Settings:
    """Obtener configuración singleton."""
    return Settings()

# Alias para facilitar importación
settings = get_settings()
```

### **Paso 2: Configuraciones por Ambiente**

```python
# app/core/environments.py
from typing import Type
from .config import Settings

class DevelopmentSettings(Settings):
    """Configuración para desarrollo."""
    debug: bool = True
    reload: bool = True
    workers: int = 1
    database_echo: bool = True
    log_level: str = "DEBUG"
    cors_origins: list = ["http://localhost:3000", "http://localhost:8080"]

class TestingSettings(Settings):
    """Configuración para testing."""
    debug: bool = True
    database_url: str = "sqlite:///./test.db"
    secret_key: str = "test-secret-key-not-for-production"
    redis_url: str = "redis://localhost:6379/1"

class StagingSettings(Settings):
    """Configuración para staging."""
    debug: bool = False
    workers: int = 2
    log_level: str = "INFO"

class ProductionSettings(Settings):
    """Configuración para producción."""
    debug: bool = False
    reload: bool = False
    workers: int = 4
    log_level: str = "WARNING"
    database_echo: bool = False

def get_environment_settings() -> Type[Settings]:
    """Obtener configuración basada en el ambiente."""
    environment = Settings().environment.lower()

    environment_map = {
        "development": DevelopmentSettings,
        "testing": TestingSettings,
        "staging": StagingSettings,
        "production": ProductionSettings,
    }

    return environment_map.get(environment, ProductionSettings)

# Configuración activa
settings = get_environment_settings()()
```

### **Paso 3: Gestión de Secrets**

```python
# app/core/secrets.py
import os
import json
import boto3
from typing import Dict, Any, Optional
from functools import lru_cache

class SecretsManager:
    """Gestor de secrets para diferentes proveedores."""

    def __init__(self, provider: str = "env"):
        self.provider = provider

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Obtener un secret por clave."""
        if self.provider == "env":
            return self._get_from_env(key, default)
        elif self.provider == "aws":
            return self._get_from_aws_secrets_manager(key, default)
        elif self.provider == "vault":
            return self._get_from_vault(key, default)
        else:
            raise ValueError(f"Unsupported secrets provider: {self.provider}")

    def _get_from_env(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Obtener secret desde variables de entorno."""
        return os.getenv(key, default)

    def _get_from_aws_secrets_manager(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Obtener secret desde AWS Secrets Manager."""
        try:
            client = boto3.client('secretsmanager')
            response = client.get_secret_value(SecretId=key)
            return response['SecretString']
        except Exception as e:
            print(f"Error getting secret from AWS: {e}")
            return default

    def _get_from_vault(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Obtener secret desde HashiCorp Vault."""
        # Implementación para Vault
        return default

    def get_database_credentials(self) -> Dict[str, str]:
        """Obtener credenciales de base de datos."""
        return {
            "username": self.get_secret("DB_USERNAME", "postgres"),
            "password": self.get_secret("DB_PASSWORD", ""),
            "host": self.get_secret("DB_HOST", "localhost"),
            "port": self.get_secret("DB_PORT", "5432"),
            "database": self.get_secret("DB_NAME", "fastapi_db"),
        }

@lru_cache()
def get_secrets_manager() -> SecretsManager:
    """Obtener gestor de secrets singleton."""
    provider = os.getenv("SECRETS_PROVIDER", "env")
    return SecretsManager(provider)
```

### **Paso 4: Logging Configurado**

```python
# app/core/logging.py
import logging
import sys
import json
from datetime import datetime
from typing import Dict, Any
from pythonjsonlogger import jsonlogger
from .config import settings

class CustomJSONFormatter(jsonlogger.JsonFormatter):
    """Formateador JSON personalizado para logs."""

    def add_fields(self, log_record: Dict[str, Any], record: logging.LogRecord, message_dict: Dict[str, Any]):
        super().add_fields(log_record, record, message_dict)

        # Añadir campos personalizados
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['level'] = record.levelname
        log_record['logger'] = record.name
        log_record['app'] = settings.app_name
        log_record['version'] = settings.app_version
        log_record['environment'] = settings.environment

        # Añadir información de contexto si está disponible
        if hasattr(record, 'user_id'):
            log_record['user_id'] = record.user_id
        if hasattr(record, 'request_id'):
            log_record['request_id'] = record.request_id

def setup_logging():
    """Configurar logging para la aplicación."""

    # Configurar nivel de logging
    log_level = getattr(logging, settings.log_level.upper())

    # Crear formateador
    if settings.log_format.lower() == "json":
        formatter = CustomJSONFormatter(
            fmt='%(timestamp)s %(level)s %(logger)s %(message)s'
        )
    else:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    # Configurar handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Configurar root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(handler)

    # Configurar loggers específicos
    logging.getLogger("uvicorn").setLevel(log_level)
    logging.getLogger("fastapi").setLevel(log_level)
    logging.getLogger("sqlalchemy.engine").setLevel(
        logging.INFO if settings.database_echo else logging.WARNING
    )

    return logging.getLogger(__name__)

# Logger principal
logger = setup_logging()
```

### **Paso 5: Middleware de Monitoreo**

```python
# app/middleware/monitoring.py
import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import logging

logger = logging.getLogger(__name__)

class MonitoringMiddleware(BaseHTTPMiddleware):
    """Middleware para monitoreo y logging de requests."""

    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        # Generar ID único para la request
        request_id = str(uuid.uuid4())

        # Añadir ID a headers
        request.state.request_id = request_id

        # Log de request entrante
        start_time = time.time()
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host,
                "user_agent": request.headers.get("user-agent"),
            }
        )

        try:
            # Procesar request
            response = await call_next(request)

            # Calcular tiempo de procesamiento
            process_time = time.time() - start_time

            # Log de response
            logger.info(
                "Request completed",
                extra={
                    "request_id": request_id,
                    "status_code": response.status_code,
                    "process_time": process_time,
                }
            )

            # Añadir headers de respuesta
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(process_time)

            return response

        except Exception as e:
            # Log de error
            process_time = time.time() - start_time
            logger.error(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "process_time": process_time,
                },
                exc_info=True
            )
            raise
```

### **Paso 6: Health Checks Avanzados**

```python
# app/api/health.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
import redis
import psutil
import time
from ..database import get_db
from ..core.config import settings

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    timestamp: float
    version: str
    environment: str
    checks: Dict[str, Any]

class DetailedHealthResponse(HealthResponse):
    system: Dict[str, Any]
    dependencies: Dict[str, Any]

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check básico."""
    return HealthResponse(
        status="healthy",
        timestamp=time.time(),
        version=settings.app_version,
        environment=settings.environment,
        checks={"basic": "ok"}
    )

@router.get("/health/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check(db: Session = Depends(get_db)):
    """Health check detallado con verificación de dependencias."""

    checks = {}
    dependencies = {}

    # Verificar base de datos
    try:
        db.execute("SELECT 1")
        checks["database"] = "healthy"
        dependencies["database"] = {
            "status": "connected",
            "url": settings.database_url.split("@")[-1]  # Sin credenciales
        }
    except Exception as e:
        checks["database"] = "unhealthy"
        dependencies["database"] = {
            "status": "error",
            "error": str(e)
        }

    # Verificar Redis
    try:
        r = redis.from_url(settings.redis_url)
        r.ping()
        checks["redis"] = "healthy"
        dependencies["redis"] = {
            "status": "connected",
            "url": settings.redis_url.split("@")[-1]
        }
    except Exception as e:
        checks["redis"] = "unhealthy"
        dependencies["redis"] = {
            "status": "error",
            "error": str(e)
        }

    # Información del sistema
    system = {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "uptime": time.time() - psutil.boot_time()
    }

    # Determinar estado general
    overall_status = "healthy" if all(
        check == "healthy" for check in checks.values()
    ) else "unhealthy"

    return DetailedHealthResponse(
        status=overall_status,
        timestamp=time.time(),
        version=settings.app_version,
        environment=settings.environment,
        checks=checks,
        system=system,
        dependencies=dependencies
    )

@router.get("/ready")
async def readiness_check():
    """Readiness check para Kubernetes."""
    # Verificar que la aplicación está lista para recibir tráfico
    return {"status": "ready", "timestamp": time.time()}

@router.get("/live")
async def liveness_check():
    """Liveness check para Kubernetes."""
    # Verificar que la aplicación está viva
    return {"status": "alive", "timestamp": time.time()}
```

---

## 🔨 Ejercicios Prácticos

### **Ejercicio 1: Variables de Entorno**

Crea archivos de configuración para cada ambiente:

```bash
# .env.development
APP_NAME="FastAPI Dev"
DEBUG=true
DATABASE_URL="postgresql://user:pass@localhost/dev_db"
REDIS_URL="redis://localhost:6379/0"
LOG_LEVEL="DEBUG"
CORS_ORIGINS="http://localhost:3000,http://localhost:8080"

# .env.staging
APP_NAME="FastAPI Staging"
DEBUG=false
DATABASE_URL="postgresql://user:pass@staging-db/app_db"
REDIS_URL="redis://staging-redis:6379/0"
LOG_LEVEL="INFO"
CORS_ORIGINS="https://staging.miapp.com"

# .env.production
APP_NAME="FastAPI Production"
DEBUG=false
DATABASE_URL="${DATABASE_URL}"
REDIS_URL="${REDIS_URL}"
LOG_LEVEL="WARNING"
CORS_ORIGINS="https://miapp.com"
SECRET_KEY="${SECRET_KEY}"
```

### **Ejercicio 2: Dockerfile Multi-Environment**

```dockerfile
# Dockerfile.production
FROM python:3.11-slim as production

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    ENVIRONMENT=production

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
WORKDIR /home/appuser/app

# Instalar dependencias Python
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY --chown=appuser:appuser app/ .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# Comando de producción
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### **Ejercicio 3: Configuración Kubernetes**

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fastapi-config
data:
  APP_NAME: 'FastAPI Production'
  ENVIRONMENT: 'production'
  LOG_LEVEL: 'INFO'
  WORKERS: '4'

---
apiVersion: v1
kind: Secret
metadata:
  name: fastapi-secrets
type: Opaque
stringData:
  DATABASE_URL: 'postgresql://user:password@db:5432/app'
  SECRET_KEY: 'your-super-secret-key'
  REDIS_URL: 'redis://redis:6379'

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fastapi
  template:
    metadata:
      labels:
        app: fastapi
    spec:
      containers:
        - name: fastapi
          image: mi-fastapi-app:latest
          ports:
            - containerPort: 8000
          envFrom:
            - configMapRef:
                name: fastapi-config
            - secretRef:
                name: fastapi-secrets
          livenessProbe:
            httpGet:
              path: /live
              port: 8000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
```

---

## 🎯 Mejores Prácticas

### **📋 Configuration Best Practices**

1. **Never hardcode secrets** en el código
2. **Use environment variables** para configuración
3. **Validate configurations** al startup
4. **Document required variables** en README
5. **Use type hints** para configuraciones

### **🔧 Security Practices**

```python
# Ejemplo de validación de configuración
def validate_production_config(settings: Settings):
    """Validar configuración para producción."""
    if settings.environment == "production":
        if settings.debug:
            raise ValueError("Debug must be False in production")
        if settings.secret_key == "dev-secret":
            raise ValueError("Must use secure secret key in production")
        if "localhost" in settings.database_url:
            raise ValueError("Cannot use localhost database in production")
```

### **🛡️ Monitoring Setup**

```python
# app/core/monitoring.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from prometheus_client import Counter, Histogram, generate_latest

# Métricas Prometheus
REQUEST_COUNT = Counter('requests_total', 'Total requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('request_duration_seconds', 'Request duration')

def setup_monitoring(settings: Settings):
    """Configurar monitoreo y error tracking."""

    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.environment,
            integrations=[
                FastApiIntegration(),
                SqlalchemyIntegration(),
            ],
            traces_sample_rate=1.0 if settings.environment != "production" else 0.1,
        )
```

---

## ✅ Checklist de Validación

### **🔧 Configuration Management**

- [ ] Settings configurados por ambiente
- [ ] Variables de entorno documentadas
- [ ] Secrets gestionados securely
- [ ] Validación de configuración

### **📊 Monitoring & Logging**

- [ ] Logging estructurado implementado
- [ ] Health checks configurados
- [ ] Métricas de aplicación
- [ ] Error tracking activo

### **🚀 Production Readiness**

- [ ] Performance optimizada
- [ ] Security headers configurados
- [ ] Rate limiting implementado
- [ ] Documentation completa

### **🛡️ Security**

- [ ] Secrets nunca en código
- [ ] HTTPS configurado
- [ ] CORS configurado apropiadamente
- [ ] Input validation en place

---

## 📚 Recursos Adicionales

### **🔗 Enlaces Útiles**

- [12-Factor App](https://12factor.net/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/usage/settings/)
- [FastAPI Production](https://fastapi.tiangolo.com/deployment/)

### **🛠️ Herramientas**

- **Pydantic Settings**: Configuration management
- **Sentry**: Error tracking
- **Prometheus**: Metrics collection
- **Grafana**: Monitoring dashboards

---

## 🚀 Entregables

1. **Configuration classes** para cada ambiente
2. **Secrets management** implementado
3. **Logging y monitoring** configurado
4. **Health checks** completos

## ⏭️ Próximos Pasos

En la siguiente práctica implementaremos **estrategias de deployment** avanzadas como blue-green y rolling updates.
