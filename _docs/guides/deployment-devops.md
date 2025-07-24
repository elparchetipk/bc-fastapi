# Deployment Strategy & DevOps Guide

## 🎯 Deployment Architecture Overview

### Environment Strategy

```
Development  →  Staging  →  Production
     ↓            ↓           ↓
  Local Dev    Integration   Live Users
  Fast cycle   Full testing  Stable releases
  Hot reload   CI/CD gates   Zero downtime
```

### Container Strategy

```dockerfile
# Multi-stage Dockerfile for optimized builds
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim as production

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Copy installed packages from builder
COPY --from=builder /root/.local /home/app/.local

# Copy application code
WORKDIR /app
COPY --chown=app:app . .

# Switch to non-root user
USER app

# Make sure scripts in .local are usable
ENV PATH=/home/app/.local/bin:$PATH

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🐳 Docker Compose Configuration

### Development Environment

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - '8000:8000'
    volumes:
      - .:/app
      - /app/__pycache__
    environment:
      - DEBUG=true
      - DATABASE_URL=postgresql://user:pass@db:5432/fastapi_dev
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: fastapi_dev
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - '5432:5432'

  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'

  adminer:
    image: adminer
    ports:
      - '8080:8080'
    depends_on:
      - db

volumes:
  postgres_data:
```

### Production Environment

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  api:
    image: ${REGISTRY_URL}/fastapi-app:${VERSION}
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
      - SECRET_KEY=${SECRET_KEY}
    deploy:
      replicas: 3
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
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8000/health']
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: nginx:alpine
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - api
```

## ⚙️ CI/CD Pipeline

### GitHub Actions Production Pipeline

```yaml
# .github/workflows/production.yml
name: Production Deployment

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY_URL: ghcr.io/your-org/fastapi-app

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

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Cache pip packages
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run security scan
        run: |
          bandit -r src/ -f json -o bandit-report.json
          safety check --json --output safety-report.json

      - name: Run linting
        run: |
          flake8 src/ --format=json --output-file=flake8-report.json
          black --check src/
          mypy src/ --json-report mypy-report

      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379
        run: |
          pytest --cov=src/ --cov-report=xml --cov-report=html --junit-xml=junit.xml

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

      - name: Upload test results
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: test-results
          path: |
            junit.xml
            coverage.xml
            htmlcov/
            bandit-report.json
            safety-report.json
            flake8-report.json
            mypy-report/

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    outputs:
      image-tag: ${{ steps.image.outputs.tag }}

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Generate image tag
        id: image
        run: |
          echo "tag=${REGISTRY_URL}:$(date +%Y%m%d)-${GITHUB_SHA::8}" >> $GITHUB_OUTPUT

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          platforms: linux/amd64,linux/arm64
          push: true
          tags: |
            ${{ steps.image.outputs.tag }}
            ${{ env.REGISTRY_URL }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: staging

    steps:
      - name: Deploy to staging
        run: |
          echo "Deploying ${{ needs.build.outputs.image-tag }} to staging"
          # Add actual deployment commands here

  deploy-production:
    needs: [build, deploy-staging]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production

    steps:
      - name: Deploy to production
        run: |
          echo "Deploying ${{ needs.build.outputs.image-tag }} to production"
          # Add actual deployment commands here
```

## 🔄 Database Migrations

### Alembic Configuration

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from src.database.models import Base
import os

# Alembic Config object
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Target metadata for autogenerate
target_metadata = Base.metadata

def get_url():
    return os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/fastapi")

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Migration Scripts

```bash
#!/bin/bash
# scripts/migrate.sh

set -e

echo "Running database migrations..."

# Generate migration if needed
if [ "$1" = "generate" ]; then
    alembic revision --autogenerate -m "$2"
    exit 0
fi

# Run migrations
alembic upgrade head

echo "Migrations completed successfully!"
```

## 🔧 Infrastructure as Code

### Terraform Configuration

```hcl
# infrastructure/main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# ECS Cluster
resource "aws_ecs_cluster" "main" {
  name = "${var.project_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

# ECS Service
resource "aws_ecs_service" "api" {
  name            = "${var.project_name}-api"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = var.api_desired_count

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.api.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 8000
  }

  depends_on = [aws_lb_listener.api]
}

# RDS Database
resource "aws_db_instance" "main" {
  identifier     = "${var.project_name}-db"
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.db_instance_class

  allocated_storage     = 20
  max_allocated_storage = 100
  storage_encrypted     = true

  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name

  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"

  skip_final_snapshot = false
  final_snapshot_identifier = "${var.project_name}-final-snapshot"

  tags = {
    Name        = "${var.project_name}-database"
    Environment = var.environment
  }
}
```

## 📊 Monitoring & Observability

### Application Metrics

```python
# src/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
from functools import wraps

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active database connections')

def track_metrics(func):
    @wraps(func)
    async def wrapper(request, *args, **kwargs):
        start_time = time.time()

        try:
            response = await func(request, *args, **kwargs)
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()
            return response
        except Exception as e:
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                status=500
            ).inc()
            raise
        finally:
            REQUEST_DURATION.observe(time.time() - start_time)

    return wrapper

# Start metrics server
start_http_server(9090)
```

### Logging Configuration

```python
# src/logging/config.py
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id

        if hasattr(record, 'request_id'):
            log_entry['request_id'] = record.request_id

        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)

        return json.dumps(log_entry)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s',
        handlers=[logging.StreamHandler()]
    )

    # Set custom formatter
    for handler in logging.root.handlers:
        handler.setFormatter(JSONFormatter())
```

## 🚨 Health Checks & Readiness

### Health Check Endpoint

```python
# src/health/checks.py
from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from src.database.connection import get_session
from src.cache.client import get_redis_client
import asyncio

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@router.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with dependencies"""
    checks = {}

    # Database check
    try:
        async with get_session() as session:
            await session.execute(text("SELECT 1"))
        checks["database"] = {"status": "healthy"}
    except Exception as e:
        checks["database"] = {"status": "unhealthy", "error": str(e)}

    # Redis check
    try:
        redis = await get_redis_client()
        await redis.ping()
        checks["redis"] = {"status": "healthy"}
    except Exception as e:
        checks["redis"] = {"status": "unhealthy", "error": str(e)}

    # Overall status
    overall_status = "healthy" if all(
        check["status"] == "healthy" for check in checks.values()
    ) else "unhealthy"

    return {
        "status": overall_status,
        "checks": checks,
        "timestamp": datetime.utcnow()
    }
```

## 📋 Deployment Checklist

### Pre-deployment

- [ ] All tests passing in CI/CD
- [ ] Security scans completed
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] SSL certificates updated
- [ ] Backup procedures verified

### Deployment

- [ ] Blue-green deployment strategy
- [ ] Rolling updates configured
- [ ] Health checks passing
- [ ] Monitoring alerts active
- [ ] Rollback plan prepared
- [ ] Load balancer configuration updated

### Post-deployment

- [ ] Application metrics normal
- [ ] Error rates within threshold
- [ ] Performance metrics acceptable
- [ ] User acceptance testing completed
- [ ] Documentation updated
- [ ] Team notification sent

## 🎯 Implementation Timeline

### Semana 8: Basic Deployment

- Docker containerization
- Basic CI/CD pipeline
- Health checks implementation
- Environment configuration

### Semana 9: Advanced DevOps

- Multi-stage deployments
- Database migrations
- Infrastructure as Code
- Monitoring setup

### Semana 10: Production Readiness

- Security hardening
- Performance optimization
- Comprehensive monitoring
- Disaster recovery planning

### Semana 11-12: Enterprise Deployment

- Auto-scaling configuration
- Advanced observability
- Cost optimization
- Documentation completion
