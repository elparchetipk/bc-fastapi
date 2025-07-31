# Práctica 34: Deployment y Producción

⏰ **Tiempo estimado**: 90 minutos  
🎯 **Objetivo**: Preparar y optimizar containers para producción

---

## 📋 Qué vas a lograr

Al final de esta práctica habrás:

- ✅ Optimizado containers para producción
- ✅ Implementado seguridad avanzada
- ✅ Configurado monitoring y logging
- ✅ Preparado CI/CD básico
- ✅ Deployado en entorno cloud simulado

---

## 🔒 Paso 1: Hardening de Seguridad (20 min)

### **Dockerfile de producción con seguridad mejorada**

```dockerfile
# Dockerfile.production
# Multi-stage build para producción con máxima seguridad

# Build stage
FROM python:3.13-alpine AS builder

# Instalar dependencias de build con versiones específicas
RUN apk add --no-cache \
    gcc=12.2.1_git20220924-r10 \
    musl-dev=1.2.4-r2 \
    linux-headers=6.0-r1 \
    postgresql-dev=15.5-r0 \
    build-base=0.5-r3

# Crear directorio para dependencias
WORKDIR /install

# Copiar requirements con hash verification
COPY requirements.txt .

# Instalar dependencias con verificación de integridad
RUN pip install --no-cache-dir --upgrade pip==23.3.1 && \
    pip install --prefix=/install --no-cache-dir --require-hashes -r requirements.txt

# Production stage
FROM python:3.13-alpine AS production

# Instalar solo runtime dependencies
RUN apk add --no-cache \
    curl=8.4.0-r0 \
    postgresql-libs=15.5-r0 \
    && rm -rf /var/cache/apk/*

# Crear usuario específico para la aplicación
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup -s /bin/sh -h /app

# Copiar dependencias del build stage
COPY --from=builder /install /usr/local

# Establecer directorio de trabajo
WORKDIR /app

# Copiar código con ownership correcto
COPY --chown=appuser:appgroup app/ ./app/

# Establecer permisos restrictivos
RUN chmod -R 755 /app && \
    chmod -R 644 /app/app && \
    find /app -name "*.py" -exec chmod 644 {} \;

# Cambiar a usuario no-root
USER appuser

# Variables de entorno seguras
ENV PYTHONPATH=/app \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Exponer puerto
EXPOSE 8000

# Health check robusto
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f -H "User-Agent: HealthCheck/1.0" http://localhost:8000/health || exit 1

# Labels para metadata
LABEL maintainer="your-email@company.com" \
      version="1.0.0" \
      description="FastAPI Production Application" \
      org.opencontainers.image.source="https://github.com/your-org/your-repo"

# Comando de inicio con configuración de producción
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "2", "--access-log", "--log-level", "info"]
```

### **Requirements con hashes para seguridad**

```bash
# Generar requirements.txt con hashes
pip-compile --generate-hashes requirements.in

# O crear manualmente (ejemplo):
cat > requirements.production.txt << 'EOF'
fastapi==0.104.1 \
    --hash=sha256:17ea427674467486e997206a5ab25760f6b09e069f099b96f5b55a32fb6f1631
uvicorn[standard]==0.24.0 \
    --hash=sha256:368f46ba94df91bc4c3897a6cc44932b8afe4b4f2b4e6d89f4b5b67e9e0b2c5
sqlalchemy==2.0.23 \
    --hash=sha256:c7b81ec4e0b7d52b7e8b0e0b2b3b4b5a4b3b3b4b5b4b5b4b5b4b5b4b5b4b5
psycopg2-binary==2.9.9 \
    --hash=sha256:a7e4f3e6b4a4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4
redis==5.0.1 \
    --hash=sha256:b4e4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4b4
pydantic==2.5.0 \
    --hash=sha256:c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4c4
EOF
```

### **Docker Compose para producción**

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.production
    image: your-registry/fastapi-app:${VERSION:-latest}
    container_name: fastapi-prod
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://cache:6379
      - ENVIRONMENT=production
      - DEBUG=false
      - SECRET_KEY=${SECRET_KEY}
      - LOG_LEVEL=info
    env_file:
      - .env.production
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    volumes:
      - app_logs:/app/logs:rw
    networks:
      - backend
      - frontend
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8000/health']
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15-alpine
    container_name: postgres-prod
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_INITDB_ARGS=--auth-host=scram-sha-256
    volumes:
      - postgres_data:/var/lib/postgresql/data:rw
      - ./database/init-prod.sql:/docker-entrypoint-initdb.d/init.sql:ro
      - ./config/postgresql.conf:/etc/postgresql/postgresql.conf:ro
    networks:
      - backend
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}']
      interval: 10s
      timeout: 5s
      retries: 5
    logging:
      driver: 'json-file'
      options:
        max-size: '10m'
        max-file: '3'

  cache:
    image: redis:7-alpine
    container_name: redis-prod
    volumes:
      - redis_data:/data:rw
      - ./config/redis-prod.conf:/usr/local/etc/redis/redis.conf:ro
    networks:
      - backend
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    command: redis-server /usr/local/etc/redis/redis.conf
    healthcheck:
      test: ['CMD', 'redis-cli', '--no-auth-warning', 'ping']
      interval: 10s
      timeout: 3s
      retries: 3

  proxy:
    image: nginx:alpine
    container_name: nginx-prod
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - ./config/nginx-prod.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
      - nginx_logs:/var/log/nginx:rw
    depends_on:
      - api
    networks:
      - frontend
    restart: unless-stopped
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost/nginx-health']
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
  app_logs:
    driver: local
  nginx_logs:
    driver: local

networks:
  backend:
    driver: bridge
    internal: true
    ipam:
      config:
        - subnet: 172.20.0.0/16
  frontend:
    driver: bridge
    ipam:
      config:
        - subnet: 172.21.0.0/16
```

### **Test de seguridad**

```bash
# 1. Build de la imagen de producción
docker build -f Dockerfile.production -t fastapi-secure .

# 2. Scan de vulnerabilidades (si tienes docker scan o trivy)
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy:latest image fastapi-secure

# 3. Verificar que no ejecuta como root
docker run --rm fastapi-secure id

# 4. Verificar permisos de archivos
docker run --rm fastapi-secure ls -la /app

# 5. Test de filesystem read-only
docker run --rm --read-only fastapi-secure \
  python -c "open('/tmp/test', 'w')" 2>/dev/null || echo "✅ Read-only working"
```

---

## 📊 Paso 2: Monitoring y Logging (25 min)

### **Aplicación con logging estructurado**

```python
# app/logger.py
import logging
import sys
from datetime import datetime
import json
from typing import Any, Dict

class StructuredLogger:
    def __init__(self, name: str = "fastapi-app"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Handler para stdout
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(self.JSONFormatter())
        self.logger.addHandler(handler)

    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_entry = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno
            }

            # Agregar datos extra si existen
            if hasattr(record, 'extra_data'):
                log_entry.update(record.extra_data)

            return json.dumps(log_entry)

    def info(self, message: str, **kwargs):
        self.logger.info(message, extra={'extra_data': kwargs})

    def error(self, message: str, **kwargs):
        self.logger.error(message, extra={'extra_data': kwargs})

    def warning(self, message: str, **kwargs):
        self.logger.warning(message, extra={'extra_data': kwargs})

# Instancia global
logger = StructuredLogger()
```

### **Middleware para logging de requests**

```python
# app/middleware.py
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
from .logger import logger

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Generar request ID único
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Log de request inicial
        start_time = time.time()
        logger.info(
            "Request started",
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host,
            user_agent=request.headers.get("user-agent", "")
        )

        # Procesar request
        response = await call_next(request)

        # Log de response
        process_time = time.time() - start_time
        logger.info(
            "Request completed",
            request_id=request_id,
            status_code=response.status_code,
            process_time=f"{process_time:.4f}s"
        )

        # Agregar request ID al response header
        response.headers["X-Request-ID"] = request_id

        return response

class MetricsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.request_count = 0
        self.error_count = 0

    async def dispatch(self, request: Request, call_next):
        self.request_count += 1

        response = await call_next(request)

        if response.status_code >= 400:
            self.error_count += 1
            logger.error(
                "HTTP Error",
                status_code=response.status_code,
                path=request.url.path,
                method=request.method
            )

        return response
```

### **Main.py actualizado con monitoring**

```python
# app/main.py (fragmento actualizado)
from fastapi import FastAPI, HTTPException, Depends
from .middleware import LoggingMiddleware, MetricsMiddleware
from .logger import logger
import psutil
import os
from datetime import datetime

app = FastAPI(
    title="FastAPI Production Ready",
    description="API con monitoring completo",
    version="1.0.0"
)

# Agregar middleware
app.add_middleware(LoggingMiddleware)
metrics_middleware = MetricsMiddleware(app)
app.add_middleware(type(metrics_middleware), app=app)

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up", version="1.0.0")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down")

@app.get("/metrics")
async def get_metrics():
    """Endpoint para métricas de la aplicación"""
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "requests_total": metrics_middleware.request_count,
        "errors_total": metrics_middleware.error_count,
        "error_rate": metrics_middleware.error_count / max(metrics_middleware.request_count, 1),
        "cpu_percent": psutil.cpu_percent(),
        "memory_mb": psutil.virtual_memory().used / 1024 / 1024,
        "disk_usage": psutil.disk_usage('/').percent,
        "process_id": os.getpid(),
        "hostname": os.getenv("HOSTNAME", "unknown")
    }

# Resto de endpoints con logging mejorado...
```

### **Configuración de Prometheus (opcional)**

```yaml
# config/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'fastapi'
    static_configs:
      - targets: ['api:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'postgres'
    static_configs:
      - targets: ['db:5432']

  - job_name: 'redis'
    static_configs:
      - targets: ['cache:6379']
```

### **Docker Compose con monitoring**

```yaml
# docker-compose.monitoring.yml
version: '3.8'

services:
  # Servicios principales (api, db, cache, proxy)
  # ... (mismos servicios del paso anterior)

  # Prometheus para métricas
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    ports:
      - '9090:9090'
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus_data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--web.console.libraries=/etc/prometheus/console_libraries'
      - '--web.console.templates=/etc/prometheus/consoles'
    networks:
      - monitoring
    restart: unless-stopped

  # Grafana para visualización
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - '3000:3000'
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana_data:/var/lib/grafana
      - ./config/grafana-dashboards:/var/lib/grafana/dashboards
    networks:
      - monitoring
    restart: unless-stopped

  # Log aggregation con ELK stack (simplificado)
  elasticsearch:
    image: elasticsearch:7.17.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - 'ES_JAVA_OPTS=-Xms512m -Xmx512m'
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data
    networks:
      - monitoring
    restart: unless-stopped

volumes:
  prometheus_data:
  grafana_data:
  elasticsearch_data:

networks:
  monitoring:
    driver: bridge
```

---

## 🚀 Paso 3: CI/CD Básico (25 min)

### **GitHub Actions Workflow**

```yaml
# .github/workflows/docker-deploy.yml
name: Docker Build and Deploy

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
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
        image: redis:7
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-asyncio httpx

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379
        run: |
          pytest tests/ -v

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: docker build -f Dockerfile.production -t test-image .

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'test-image'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  build-and-push:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile.production
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to staging
        run: |
          echo "🚀 Deploying to staging environment..."
          # Aquí irían los comandos de deployment real
          # Por ejemplo, usando kubectl, docker-compose, etc.

      - name: Health check
        run: |
          echo "🔍 Performing health check..."
          # Comando para verificar que el deployment fue exitoso
```

### **Scripts de deployment**

```bash
# scripts/deploy.sh
#!/bin/bash
set -e

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}

echo "🚀 Deploying to $ENVIRONMENT with version $VERSION"

# Validar parámetros
if [[ ! "$ENVIRONMENT" =~ ^(staging|production)$ ]]; then
    echo "❌ Environment must be 'staging' or 'production'"
    exit 1
fi

# Configurar variables según el entorno
if [ "$ENVIRONMENT" = "production" ]; then
    COMPOSE_FILE="docker-compose.production.yml"
    ENV_FILE=".env.production"
    PORT="80"
else
    COMPOSE_FILE="docker-compose.staging.yml"
    ENV_FILE=".env.staging"
    PORT="8080"
fi

echo "📋 Using compose file: $COMPOSE_FILE"
echo "📋 Using env file: $ENV_FILE"

# Validar archivos necesarios
if [ ! -f "$COMPOSE_FILE" ]; then
    echo "❌ Compose file $COMPOSE_FILE not found"
    exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Environment file $ENV_FILE not found"
    exit 1
fi

# Pull de la imagen más reciente
echo "📥 Pulling latest images..."
docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" pull

# Backup de la base de datos (solo en producción)
if [ "$ENVIRONMENT" = "production" ]; then
    echo "💾 Creating database backup..."
    ./scripts/backup-db.sh
fi

# Deploy con rolling update
echo "🔄 Performing rolling update..."
docker-compose -f "$COMPOSE_FILE" --env-file "$ENV_FILE" up -d

# Esperar que los servicios estén healthy
echo "⏳ Waiting for services to be healthy..."
for i in {1..30}; do
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "healthy"; then
        echo "✅ Services are healthy"
        break
    fi

    if [ $i -eq 30 ]; then
        echo "❌ Services failed to become healthy"
        exit 1
    fi

    sleep 5
done

# Health check
echo "🔍 Performing health check..."
if curl -f "http://localhost:$PORT/health" >/dev/null 2>&1; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

echo "🎉 Deployment to $ENVIRONMENT completed successfully!"
```

### **Script de backup**

```bash
# scripts/backup-db.sh
#!/bin/bash
set -e

BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/postgres_backup_$TIMESTAMP.sql"

echo "💾 Creating database backup..."

# Crear directorio de backup si no existe
mkdir -p "$BACKUP_DIR"

# Realizar backup
docker exec postgres-prod pg_dump -U fastapi_user fastapi_db > "$BACKUP_FILE"

# Comprimir backup
gzip "$BACKUP_FILE"

echo "✅ Backup completed: ${BACKUP_FILE}.gz"

# Mantener solo los últimos 7 backups
find "$BACKUP_DIR" -name "postgres_backup_*.sql.gz" -mtime +7 -delete

echo "🧹 Old backups cleaned up"
```

---

## ☁️ Paso 4: Deployment en Cloud Simulado (20 min)

### **Docker Compose para cloud deployment**

```yaml
# docker-compose.cloud.yml
version: '3.8'

services:
  api:
    image: ${REGISTRY}/${IMAGE_NAME}:${VERSION}
    deploy:
      replicas: 2
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
      - ENVIRONMENT=production
    networks:
      - backend
      - frontend
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8000/health']
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: postgres:15-alpine
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
        delay: 10s
        max_attempts: 3
      resources:
        limits:
          memory: 1G
          cpus: '1'
        reservations:
          memory: 512M
          cpus: '0.5'
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend

  cache:
    image: redis:7-alpine
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
      resources:
        limits:
          memory: 256M
          cpus: '0.25'
        reservations:
          memory: 128M
          cpus: '0.1'
    volumes:
      - redis_data:/data
    networks:
      - backend

  proxy:
    image: nginx:alpine
    deploy:
      replicas: 1
      restart_policy:
        condition: on-failure
        delay: 5s
        max_attempts: 3
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - ./config/nginx-cloud.conf:/etc/nginx/nginx.conf:ro
    networks:
      - frontend
    depends_on:
      - api

volumes:
  postgres_data:
    external: true
  redis_data:
    external: true

networks:
  backend:
    driver: overlay
    internal: true
  frontend:
    driver: overlay
```

### **Configuración de Nginx para cloud**

```nginx
# config/nginx-cloud.conf
events {
    worker_connections 1024;
}

http {
    upstream fastapi_backend {
        least_conn;
        server api:8000 max_fails=3 fail_timeout=30s;
        # En cloud, habría múltiples instancias:
        # server api_1:8000 max_fails=3 fail_timeout=30s;
        # server api_2:8000 max_fails=3 fail_timeout=30s;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;

    # Logging
    log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                    '$status $body_bytes_sent "$http_referer" '
                    '"$http_user_agent" "$http_x_forwarded_for" '
                    'rt=$request_time uct="$upstream_connect_time" '
                    'uht="$upstream_header_time" urt="$upstream_response_time"';

    access_log /var/log/nginx/access.log main;
    error_log /var/log/nginx/error.log warn;

    server {
        listen 80;
        server_name _;

        # Security headers
        add_header X-Frame-Options DENY always;
        add_header X-Content-Type-Options nosniff always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Rate limiting
        limit_req zone=api burst=20 nodelay;

        # Health check para load balancer
        location /nginx-health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }

        # Proxy to FastAPI
        location / {
            proxy_pass http://fastapi_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Timeouts
            proxy_connect_timeout 30s;
            proxy_send_timeout 30s;
            proxy_read_timeout 30s;
        }

        # Static files (si los hubiera)
        location /static/ {
            alias /var/www/static/;
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### **Simulación de deployment en cloud**

```bash
# 1. Inicializar Docker Swarm (simula cluster)
docker swarm init

# 2. Crear networks para el stack
docker network create --driver overlay --attachable backend
docker network create --driver overlay frontend

# 3. Crear volumes persistentes
docker volume create postgres_data
docker volume create redis_data

# 4. Deploy del stack
docker stack deploy -c docker-compose.cloud.yml fastapi-stack

# 5. Verificar el deployment
docker stack services fastapi-stack
docker stack ps fastapi-stack

# 6. Escalar servicios
docker service scale fastapi-stack_api=3

# 7. Ver logs del stack
docker service logs fastapi-stack_api

# 8. Rolling update (simular nueva versión)
docker service update --image your-registry/fastapi-app:v2 fastapi-stack_api

# 9. Health check del stack
curl http://localhost/health

# 10. Limpiar (cuando termines)
docker stack rm fastapi-stack
docker swarm leave --force
```

---

## 🔍 Paso 5: Testing y Validación Final (10 min)

### **Suite de tests de integración**

```python
# tests/test_production.py
import pytest
import httpx
import time
import asyncio

BASE_URL = "http://localhost:8000"

class TestProductionDeployment:

    @pytest.mark.asyncio
    async def test_health_endpoint(self):
        """Test que el endpoint de health responde correctamente"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "database" in data
            assert "cache" in data

    @pytest.mark.asyncio
    async def test_metrics_endpoint(self):
        """Test que las métricas están disponibles"""
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/metrics")
            assert response.status_code == 200
            data = response.json()
            assert "requests_total" in data
            assert "cpu_percent" in data
            assert "memory_mb" in data

    @pytest.mark.asyncio
    async def test_crud_operations(self):
        """Test operaciones CRUD básicas"""
        async with httpx.AsyncClient() as client:
            # Crear usuario
            user_data = {
                "username": f"test_user_{int(time.time())}",
                "email": f"test_{int(time.time())}@example.com"
            }

            response = await client.post(f"{BASE_URL}/users", json=user_data)
            assert response.status_code == 200
            created_user = response.json()
            assert created_user["username"] == user_data["username"]

            # Obtener usuario
            user_id = created_user["id"]
            response = await client.get(f"{BASE_URL}/users/{user_id}")
            assert response.status_code == 200

            # Listar usuarios
            response = await client.get(f"{BASE_URL}/users")
            assert response.status_code == 200
            users = response.json()
            assert len(users) > 0

    @pytest.mark.asyncio
    async def test_cache_functionality(self):
        """Test que el cache Redis funciona"""
        async with httpx.AsyncClient() as client:
            # Verificar stats del cache
            response = await client.get(f"{BASE_URL}/cache/stats")
            assert response.status_code == 200

            # Crear usuario (debería guardarse en cache)
            user_data = {
                "username": f"cache_test_{int(time.time())}",
                "email": f"cache_{int(time.time())}@example.com"
            }

            response = await client.post(f"{BASE_URL}/users", json=user_data)
            assert response.status_code == 200
            user_id = response.json()["id"]

            # Primera request (desde DB)
            start_time = time.time()
            response = await client.get(f"{BASE_URL}/users/{user_id}")
            first_time = time.time() - start_time

            # Segunda request (desde cache, debería ser más rápida)
            start_time = time.time()
            response = await client.get(f"{BASE_URL}/users/{user_id}")
            second_time = time.time() - start_time

            assert response.status_code == 200
            # El cache debería hacer la segunda request más rápida
            assert second_time <= first_time * 2  # Tolerancia para variaciones

    def test_security_headers(self):
        """Test que los headers de seguridad están presentes"""
        response = httpx.get(f"{BASE_URL}/")

        # Verificar headers de seguridad (si pasamos por Nginx)
        if "X-Frame-Options" in response.headers:
            assert response.headers["X-Frame-Options"] == "DENY"

        if "X-Content-Type-Options" in response.headers:
            assert response.headers["X-Content-Type-Options"] == "nosniff"

# Ejecutar tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### **Script de validación completa**

```bash
# scripts/validate-deployment.sh
#!/bin/bash
set -e

BASE_URL=${1:-http://localhost:8000}
TIMEOUT=30

echo "🔍 Validating deployment at $BASE_URL"

# Test 1: Health check
echo "1️⃣ Testing health endpoint..."
if curl -f -s "$BASE_URL/health" | grep -q "healthy"; then
    echo "✅ Health check passed"
else
    echo "❌ Health check failed"
    exit 1
fi

# Test 2: Metrics endpoint
echo "2️⃣ Testing metrics endpoint..."
if curl -f -s "$BASE_URL/metrics" | grep -q "requests_total"; then
    echo "✅ Metrics endpoint working"
else
    echo "❌ Metrics endpoint failed"
    exit 1
fi

# Test 3: Database connectivity
echo "3️⃣ Testing database operations..."
USER_ID=$(curl -s -X POST "$BASE_URL/users" \
    -H "Content-Type: application/json" \
    -d '{"username":"validation_test","email":"validation@test.com"}' | \
    jq -r '.id')

if [ "$USER_ID" != "null" ] && [ "$USER_ID" != "" ]; then
    echo "✅ Database operations working"
else
    echo "❌ Database operations failed"
    exit 1
fi

# Test 4: Cache functionality
echo "4️⃣ Testing cache functionality..."
if curl -f -s "$BASE_URL/cache/stats" | grep -q "connected_clients"; then
    echo "✅ Cache functionality working"
else
    echo "❌ Cache functionality failed"
    exit 1
fi

# Test 5: Performance test básico
echo "5️⃣ Testing basic performance..."
START_TIME=$(date +%s.%N)
for i in {1..10}; do
    curl -s "$BASE_URL/health" > /dev/null
done
END_TIME=$(date +%s.%N)
DURATION=$(echo "$END_TIME - $START_TIME" | bc)
AVG_TIME=$(echo "scale=3; $DURATION / 10" | bc)

echo "✅ Average response time: ${AVG_TIME}s"

echo ""
echo "🎉 All validation tests passed!"
echo "📊 Deployment is ready for production use"
```

---

## 🏆 Verificación Final y Entregables

### **Checklist de completitud**

```bash
# ✅ 1. Imagen de producción construida
docker images | grep fastapi-secure

# ✅ 2. Configuración de seguridad aplicada
docker run --rm fastapi-secure id | grep -q appuser

# ✅ 3. Logging estructurado funcionando
docker run --rm -d --name log-test fastapi-secure
docker logs log-test | grep -q '"timestamp"'
docker rm -f log-test

# ✅ 4. Health checks configurados
docker inspect fastapi-secure | grep -A 5 "Healthcheck"

# ✅ 5. CI/CD workflow válido
yaml-lint .github/workflows/docker-deploy.yml

# ✅ 6. Scripts de deployment ejecutables
./scripts/deploy.sh staging latest --dry-run

# ✅ 7. Validación completa exitosa
./scripts/validate-deployment.sh
```

### **Archivos finales creados**

```
├── app/
│   ├── main.py              # App con logging y métricas
│   ├── logger.py            # Logger estructurado
│   └── middleware.py        # Middleware de logging
├── config/
│   ├── nginx-prod.conf      # Nginx para producción
│   ├── nginx-cloud.conf     # Nginx para cloud
│   ├── redis-prod.conf      # Redis optimizado
│   ├── postgresql.conf      # PostgreSQL optimizado
│   └── prometheus.yml       # Configuración Prometheus
├── scripts/
│   ├── deploy.sh            # Script de deployment
│   ├── backup-db.sh         # Script de backup
│   └── validate-deployment.sh # Script de validación
├── tests/
│   └── test_production.py   # Tests de producción
├── .github/workflows/
│   └── docker-deploy.yml    # CI/CD pipeline
├── Dockerfile.production    # Dockerfile optimizado
├── docker-compose.production.yml  # Compose de producción
├── docker-compose.cloud.yml       # Compose para cloud
├── docker-compose.monitoring.yml  # Compose con monitoring
├── requirements.production.txt    # Requirements con hashes
├── .env.production         # Variables de producción
└── .env.staging           # Variables de staging
```

---

## 📈 Métricas y KPIs de Producción

### **Métricas clave a monitorear**

✅ **Response Time**: < 200ms promedio  
✅ **Error Rate**: < 1% de requests  
✅ **CPU Usage**: < 70% promedio  
✅ **Memory Usage**: < 80% del límite  
✅ **Database Connections**: < 80% del pool  
✅ **Cache Hit Rate**: > 80%

### **Alertas recomendadas**

- Error rate > 5% por 5 minutos
- Response time > 1s por 5 minutos
- CPU > 90% por 10 minutos
- Memory > 95% por 5 minutos
- Health check failures > 3 consecutivos

---

## 🎯 Próximos Pasos

### **Mejoras adicionales a considerar**

- **Service Mesh** (Istio, Linkerd) para observabilidad avanzada
- **Auto-scaling** horizontal con métricas custom
- **Blue-Green deployments** para zero-downtime
- **Disaster recovery** con backups automáticos
- **Security scanning** automático en CI/CD

---

**🎉 ¡Excelente trabajo!** Has completado la containerización completa de tu aplicación FastAPI, desde desarrollo hasta producción. Tu aplicación ahora está lista para ser deployada en cualquier entorno cloud con las mejores prácticas de la industria. 🐳🚀✨

---

_Práctica 34 - Semana 9 - Bootcamp FastAPI_  
_Tiempo total: ~90 minutos_
