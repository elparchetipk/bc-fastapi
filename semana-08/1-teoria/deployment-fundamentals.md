# Fundamentos de Deployment y CI/CD

## 🎯 Objetivos de Aprendizaje

Al completar esta teoría, comprenderás:

- **Conceptos fundamentales** de deployment y DevOps
- **Estrategias de deployment** para aplicaciones modernas
- **CI/CD pipelines** y automation principles
- **Containerización** con Docker para deployment
- **Infrastructure as Code** y configuration management

## ⏱️ Tiempo Estimado

**45 minutos** de lectura y comprensión

---

## 🚀 ¿Qué es Deployment?

### Definición

**Deployment** es el proceso de hacer disponible una aplicación software en un entorno de producción donde los usuarios finales pueden acceder a ella. Es la transición del código de desarrollo a un sistema operativo que sirve a usuarios reales.

### Componentes del Deployment

```
Development → Testing → Staging → Production
     ↓            ↓         ↓          ↓
  Local Code   CI Pipeline  Pre-prod   Live Users
```

### Challenges del Deployment Tradicional

1. **"Works on My Machine"**: Diferencias entre entornos
2. **Manual Processes**: Propensos a errores humanos
3. **Downtime**: Interrupciones durante deployment
4. **Rollback Complexity**: Difícil revertir cambios
5. **Configuration Drift**: Inconsistencias entre entornos

---

## 🔄 DevOps y Culture

### Principios DevOps

```
Development + Operations = DevOps
```

#### 1. **Collaboration**

- Romper silos entre desarrollo y operaciones
- Shared responsibility para el software
- Communication y feedback constante

#### 2. **Automation**

- Automatizar procesos repetitivos
- Reducir errores humanos
- Incrementar velocity y reliability

#### 3. **Continuous Integration/Deployment**

- Integrar cambios frecuentemente
- Deployment automático y confiable
- Fast feedback loops

#### 4. **Monitoring & Feedback**

- Observabilidad en production
- Metrics-driven decisions
- Continuous improvement

### DevOps Lifecycle

```
Plan → Code → Build → Test → Release → Deploy → Operate → Monitor
  ↑                                                              ↓
  ←←←←←←←←←←← Feedback & Improvement ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
```

---

## 🏗️ Infrastructure as Code (IaC)

### Conceptos Fundamentales

#### Traditional Infrastructure

```yaml
Manual Process:
1. Login to server
2. Install dependencies
3. Configure services
4. Deploy application
5. Setup monitoring

Problems:
- Error prone
- Not reproducible
- Hard to scale
- Configuration drift
```

#### Infrastructure as Code

```yaml
Declarative Approach:
infrastructure/
├── docker-compose.yml     # Service definitions
├── Dockerfile            # Application container
├── nginx.conf            # Reverse proxy config
├── terraform/            # Cloud infrastructure
└── ansible/              # Configuration management

Benefits:
- Reproducible
- Version controlled
- Automated
- Scalable
```

### IaC Tools Ecosystem

```
Container Orchestration:
├── Docker & Docker Compose
├── Kubernetes
└── Docker Swarm

Cloud Infrastructure:
├── Terraform (multi-cloud)
├── AWS CloudFormation
├── Azure ARM Templates
└── Google Cloud Deployment Manager

Configuration Management:
├── Ansible
├── Chef
├── Puppet
└── SaltStack
```

---

## 🐳 Containerización con Docker

### ¿Por qué Containers?

#### Problema: Environment Inconsistency

```
Developer Machine: Python 3.11, Ubuntu 22.04
Test Server: Python 3.9, CentOS 7
Production: Python 3.10, RHEL 8

Result: "It works on my machine!" 🤷‍♂️
```

#### Solución: Containerización

```
Container Image:
├── Application Code
├── Python Runtime
├── Dependencies
├── Configuration
└── Operating System Layer

Result: Same environment everywhere! 🎯
```

### Docker Architecture

```
┌─────────────────────────────────────────┐
│               Docker Host               │
├─────────────────────────────────────────┤
│  ┌───────────┐ ┌───────────┐ ┌─────────┐ │
│  │Container 1│ │Container 2│ │Container│ │
│  │   App A   │ │   App B   │ │   DB    │ │
│  └───────────┘ └───────────┘ └─────────┘ │
├─────────────────────────────────────────┤
│            Docker Engine                │
├─────────────────────────────────────────┤
│          Operating System               │
└─────────────────────────────────────────┘
```

### Docker Concepts Clave

#### 1. **Images** - The Blueprint

```dockerfile
# Dockerfile - Recipe for creating images
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 2. **Containers** - Running Instances

```bash
# Create and run container from image
docker run -p 8000:8000 my-fastapi-app

# Container is isolated process with own:
# - File system
# - Network interface
# - Process space
# - Resource limits
```

#### 3. **Volumes** - Persistent Data

```yaml
# docker-compose.yml
services:
  app:
    image: my-app
    volumes:
      - ./data:/app/data # Bind mount
      - database_data:/var/lib/postgresql/data # Named volume

volumes:
  database_data: # Persistent storage
```

### Container Benefits

```
Consistency: Same environment everywhere
Isolation: Applications don't interfere
Portability: Runs anywhere Docker runs
Efficiency: Lightweight compared to VMs
Scalability: Easy to scale up/down
```

---

## 🔄 CI/CD Pipelines

### Continuous Integration (CI)

#### Definición

**CI** es la práctica de integrar cambios de código frecuentemente (varias veces al día) en un repositorio compartido, donde cada integración es verificada por un build automático y tests.

#### CI Pipeline Típico

```
Code Commit → Trigger → Build → Test → Package → Notify
     ↓           ↓        ↓      ↓        ↓        ↓
  Git Push   Webhook   Compile  Unit    Docker   Slack/Email
             GitHub    Code     Tests   Image    Notification
             Actions
```

#### CI Best Practices

```yaml
Fast Feedback:
  - Builds < 10 minutes
  - Tests < 5 minutes
  - Immediate notifications

Quality Gates:
  - All tests must pass
  - Code coverage > 80%
  - Security scans pass
  - Linting checks pass

Artifact Management:
  - Versioned builds
  - Reproducible artifacts
  - Secure storage
```

### Continuous Deployment (CD)

#### Definición

**CD** extiende CI automatizando el deployment de aplicaciones a entornos de production después de pasar todas las pruebas y validaciones.

#### CD Pipeline Típico

```
CI Pipeline → Deploy to Staging → Automated Tests → Deploy to Production
     ↓              ↓                    ↓                  ↓
  Artifact      Integration        Smoke Tests        Live Traffic
  Ready         Environment        User Acceptance    Health Checks
```

#### CD Strategies

##### 1. **Blue-Green Deployment**

```
Current: Blue Environment (v1.0) ← 100% Traffic
New:     Green Environment (v1.1) ← 0% Traffic

Deploy to Green → Test Green → Switch Traffic → Blue becomes standby

Benefits:
- Zero downtime
- Instant rollback
- Full testing before switch
```

##### 2. **Rolling Deployment**

```
Instance 1: v1.0 → v1.1 ✅
Instance 2: v1.0 → v1.1 ✅
Instance 3: v1.0 → v1.1 ✅
Instance 4: v1.0 → v1.1 ✅

Benefits:
- No additional infrastructure
- Gradual rollout
- Resource efficient
```

##### 3. **Canary Deployment**

```
Production Traffic:
95% → v1.0 (Stable)
5%  → v1.1 (Canary)

Monitor metrics → Increase canary % → Full rollout

Benefits:
- Risk mitigation
- Real user feedback
- A/B testing capability
```

---

## 🛠️ GitHub Actions - CI/CD Platform

### ¿Qué son GitHub Actions?

**GitHub Actions** es una plataforma de CI/CD integrada en GitHub que permite automatizar workflows directamente en el repositorio.

### Conceptos Clave

#### 1. **Workflows**

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Run tests
        run: pytest
```

#### 2. **Events** - Triggers

```yaml
Trigger Events:
  - push: Code pushed to repository
  - pull_request: PR created/updated
  - schedule: Cron-based timing
  - workflow_dispatch: Manual trigger
  - release: Release created
```

#### 3. **Jobs** - Work Units

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    runs-on: ubuntu-latest
    needs: build # Runs after build
    steps: [...]

  deploy:
    runs-on: ubuntu-latest
    needs: [build, test] # Runs after both
    if: github.ref == 'refs/heads/main'
    steps: [...]
```

#### 4. **Actions** - Reusable Components

```yaml
Popular Actions:
  - actions/checkout@v4 # Clone repository
  - actions/setup-python@v4 # Setup Python environment
  - docker/build-push-action # Build Docker images
  - actions/upload-artifact # Store build artifacts
  - actions/deploy-pages # Deploy to GitHub Pages
```

### GitHub Actions Ecosystem

```
GitHub Marketplace:
├── 15,000+ Actions available
├── Community maintained
├── Verified publisher actions
└── Custom organization actions

Common Categories:
├── Language Setup (Python, Node.js, Java)
├── Cloud Deploy (AWS, Azure, GCP)
├── Testing (Codecov, SonarCloud)
├── Security (Snyk, OWASP)
├── Notifications (Slack, Teams)
└── Utilities (Cache, Artifacts)
```

---

## 🌐 Production Environment Considerations

### Environment Parity

#### Development vs Production

```yaml
Development:
  - SQLite database
  - DEBUG = True
  - No HTTPS
  - Single instance
  - Local file storage

Production:
  - PostgreSQL cluster
  - DEBUG = False
  - HTTPS required
  - Load balanced instances
  - Cloud storage (S3)
  - CDN for static files
```

#### Configuration Management

```python
# config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    cors_origins: list = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

    class Config:
        env_file = ".env"

# Different .env files per environment
# .env.development
# .env.staging
# .env.production
```

### Security Considerations

#### 1. **Secrets Management**

```yaml
Never in Code:
❌ SECRET_KEY = "super-secret-key"
❌ DATABASE_URL = "postgresql://user:pass@host/db"

Environment Variables:
✅ SECRET_KEY = os.getenv("SECRET_KEY")
✅ DATABASE_URL = os.getenv("DATABASE_URL")

Secret Management:
✅ GitHub Secrets
✅ AWS Secrets Manager
✅ HashiCorp Vault
✅ Azure Key Vault
```

#### 2. **HTTPS/TLS**

```python
# Force HTTPS in production
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if not settings.debug:
    app.add_middleware(HTTPSRedirectMiddleware)
```

#### 3. **CORS Configuration**

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # Specific domains
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Performance & Scalability

#### 1. **Application Server**

```python
# Don't use for production
uvicorn main:app --host 0.0.0.0 --port 8000

# Production server
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

#### 2. **Reverse Proxy**

```nginx
# nginx.conf
upstream fastapi {
    server app1:8000;
    server app2:8000;
    server app3:8000;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://fastapi;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 3. **Health Checks**

```python
# health.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}

@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    checks = {}

    # Database check
    try:
        db.execute("SELECT 1")
        checks["database"] = {"status": "healthy"}
    except Exception as e:
        checks["database"] = {"status": "unhealthy", "error": str(e)}

    # Overall status
    overall_status = "healthy" if all(
        check["status"] == "healthy" for check in checks.values()
    ) else "unhealthy"

    return {"status": overall_status, "checks": checks}
```

---

## 📊 Monitoring y Observability

### Three Pillars of Observability

#### 1. **Metrics**

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('http_requests_total', 'HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)

    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_DURATION.observe(time.time() - start_time)

    return response
```

#### 2. **Logging**

```python
# Structured logging
import structlog

logger = structlog.get_logger()

@app.middleware("http")
async def logging_middleware(request, call_next):
    start_time = time.time()

    logger.info("Request started",
                method=request.method,
                path=request.url.path)

    response = await call_next(request)
    duration = time.time() - start_time

    logger.info("Request completed",
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration=duration)

    return response
```

#### 3. **Tracing**

```python
# Distributed tracing
import uuid

@app.middleware("http")
async def tracing_middleware(request, call_next):
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    request.state.trace_id = trace_id

    response = await call_next(request)
    response.headers["X-Trace-ID"] = trace_id

    return response
```

---

## 🎯 Platform Options para Deployment

### Cloud Platforms

#### 1. **Platform as a Service (PaaS)**

```yaml
Heroku:
  - Simple git push deployment
  - Add-ons ecosystem
  - Automatic scaling
  - Built-in monitoring

Railway:
  - Modern developer experience
  - GitHub integration
  - Database included
  - Automatic HTTPS

Render:
  - Free tier available
  - Auto-deploy from Git
  - Custom domains
  - Background workers
```

#### 2. **Container Platforms**

```yaml
AWS ECS:
  - Container orchestration
  - Integrates with AWS services
  - Auto-scaling
  - Load balancing

Google Cloud Run:
  - Serverless containers
  - Pay per request
  - Auto-scaling to zero
  - Custom domains

Azure Container Instances:
  - Simple container deployment
  - Virtual network integration
  - Persistent storage
  - Windows containers support
```

#### 3. **Kubernetes**

```yaml
Kubernetes Features:
  - Container orchestration
  - Service discovery
  - Auto-scaling
  - Rolling updates
  - Health checks
  - Config management

Managed Kubernetes:
  - AWS EKS
  - Google GKE
  - Azure AKS
  - DigitalOcean DOKS
```

### Choosing the Right Platform

#### Decision Matrix

```yaml
Simple Apps (MVP/Prototype):
✅ Heroku, Railway, Render
- Easy deployment
- Minimal configuration
- Built-in databases

Production Apps (Scale):
✅ AWS ECS, Google Cloud Run
- Performance control
- Cost optimization
- Enterprise features

Enterprise/Complex:
✅ Kubernetes
- Full control
- Multi-cloud
- Advanced networking
```

---

## 🔧 Best Practices Summary

### 1. **Deployment Automation**

```yaml
✅ DO:
  - Automate everything possible
  - Use Infrastructure as Code
  - Implement proper testing
  - Monitor deployments
  - Plan rollback strategies

❌ DON'T:
  - Manual deployment steps
  - Different configs per environment
  - Deploy without testing
  - Ignore monitoring
  - Skip documentation
```

### 2. **Security First**

```yaml
✅ DO:
  - Use secrets management
  - Implement HTTPS everywhere
  - Scan for vulnerabilities
  - Principle of least privilege
  - Regular security updates

❌ DON'T:
  - Hardcode secrets
  - Use HTTP in production
  - Ignore security scans
  - Over-privileged access
  - Skip security patches
```

### 3. **Observability**

```yaml
✅ DO:
  - Implement health checks
  - Structure logs properly
  - Track key metrics
  - Set up alerting
  - Plan for debugging

❌ DON'T:
  - Deploy blind
  - Ignore logs
  - Skip monitoring
  - No alerting setup
  - Poor error handling
```

---

## 🎓 Próximos Pasos

### Temas que Exploraremos

1. **Docker & Containerización** - Crear containers optimizados
2. **GitHub Actions CI/CD** - Implementar pipelines automáticos
3. **Production Configuration** - Configurar para entornos reales
4. **Deployment Strategies** - Aplicar estrategias de deployment

### Skills que Desarrollarás

- Container creation y optimization
- CI/CD pipeline design
- Production configuration
- Monitoring implementation
- Security hardening
- Performance optimization

### Preparación para el Mercado Laboral

```yaml
Junior DevOps Engineer:
  - Docker fundamentals ✅
  - CI/CD pipelines ✅
  - Cloud platforms ✅
  - Monitoring basics ✅

Software Engineer:
  - Deployment knowledge ✅
  - Container awareness ✅
  - Production mindset ✅
  - Automation skills ✅

Full-Stack Developer:
  - End-to-end delivery ✅
  - DevOps collaboration ✅
  - Production support ✅
  - Performance awareness ✅
```

---

**¡Ahora que comprendes los fundamentos, estás listo para aplicar estos conceptos en prácticas hands-on!** 🚀

En las siguientes prácticas, implementaremos cada uno de estos conceptos paso a paso, desde la containerización hasta el deployment automático en producción.
