# Especificación del Proyecto Semana 9: E-commerce Containerizado

⏰ **Tiempo total**: 6 horas distribuidas en prácticas  
🎯 **Objetivo**: Containerizar completamente la aplicación E-commerce con Docker

---

## 📋 Descripción General

Vas a tomar la aplicación E-commerce desarrollada en semanas anteriores y containerizarla completamente usando Docker y Docker Compose, aplicando todas las mejores prácticas aprendidas.

### **¿Qué construirás?**

Un **E-commerce completamente containerizado** que incluye:

- 🐳 **API FastAPI** optimizada en containers
- 🗄️ **PostgreSQL** con persistencia de datos
- 🔴 **Redis** para cache y sesiones
- 🌐 **Nginx** como reverse proxy
- 📊 **Monitoring** con Prometheus/Grafana
- 🔒 **Seguridad** aplicada a todos los containers
- 🚀 **Deployment** listo para cualquier entorno

---

## 🏗️ Arquitectura del Proyecto

```
🏪 E-commerce Containerizado
├── 🐳 FastAPI Container
│   ├── API REST completa
│   ├── Autenticación JWT
│   ├── CRUD de productos/usuarios
│   └── Sistema de órdenes
├── 🗄️ PostgreSQL Container
│   ├── Esquema optimizado
│   ├── Índices de performance
│   └── Datos persistentes
├── 🔴 Redis Container
│   ├── Cache de productos
│   ├── Sesiones de usuario
│   └── Rate limiting data
├── 🌐 Nginx Container
│   ├── Reverse proxy
│   ├── Static files serving
│   ├── SSL termination
│   └── Load balancing
└── 📊 Monitoring Stack
    ├── Prometheus metrics
    ├── Grafana dashboards
    └── Health monitoring
```

---

## 📦 Fase 1: Containerización de la API (90 min)

### **1.1 Dockerfile Optimizado**

Crear un Dockerfile multi-stage optimizado para la aplicación FastAPI:

```dockerfile
# Ejemplo de estructura esperada
FROM python:3.13-alpine AS builder
# Build stage con dependencias

FROM python:3.13-alpine AS production
# Production stage optimizado
```

**Requisitos técnicos:**

- ✅ Multi-stage build para optimización
- ✅ Usuario no-root para seguridad
- ✅ Alpine Linux para menor tamaño
- ✅ Health check configurado
- ✅ Variables de entorno
- ✅ .dockerignore optimizado

### **1.2 Aplicación FastAPI actualizada**

Actualizar la aplicación con features específicas para containers:

```python
# Estructura esperada en app/main.py
from fastapi import FastAPI
from .routers import products, users, orders, auth
from .middleware import LoggingMiddleware, MetricsMiddleware
from .database import engine, Base
from .cache import redis_client

app = FastAPI(title="E-commerce Containerized")

# Middleware para logging y métricas
app.add_middleware(LoggingMiddleware)
app.add_middleware(MetricsMiddleware)

# Health checks y métricas
@app.get("/health")
async def health_check():
    # Verificar conexiones a DB y Redis
    pass

@app.get("/metrics")
async def get_metrics():
    # Métricas para Prometheus
    pass
```

**Features requeridas:**

- ✅ Health checks robustos (DB + Redis + API)
- ✅ Métricas para Prometheus
- ✅ Logging estructurado en JSON
- ✅ Configuración via variables de entorno
- ✅ Graceful shutdown handling

### **1.3 Test de la imagen**

```bash
# Comandos para validar la imagen
docker build -t ecommerce-api:latest .
docker run -d --name api-test -p 8000:8000 ecommerce-api:latest
curl http://localhost:8000/health
docker logs api-test
docker rm -f api-test
```

---

## 🔧 Fase 2: Docker Compose Stack (90 min)

### **2.1 Configuración base**

Crear `docker-compose.yml` con todos los servicios:

```yaml
version: '3.8'

services:
  api:
    build: .
    container_name: ecommerce-api
    # Configuración completa

  db:
    image: postgres:15-alpine
    container_name: ecommerce-db
    # Configuración con volumes y health checks

  cache:
    image: redis:7-alpine
    container_name: ecommerce-cache
    # Configuración optimizada

  proxy:
    image: nginx:alpine
    container_name: ecommerce-proxy
    # Reverse proxy configurado
```

**Requisitos del compose:**

- ✅ Networks personalizados (backend/frontend)
- ✅ Volumes persistentes para datos
- ✅ Health checks en todos los servicios
- ✅ Depends_on con conditions
- ✅ Resource limits apropiados
- ✅ Restart policies configuradas

### **2.2 Configuración de servicios**

**PostgreSQL:**

- Esquema optimizado para e-commerce
- Índices de performance
- Script de inicialización con datos demo

**Redis:**

- Configuración de memoria optimizada
- Persistencia RDB configurada
- Configuración de seguridad básica

**Nginx:**

- Reverse proxy a la API
- Serving de archivos estáticos
- Configuración de SSL (auto-firmado para desarrollo)
- Rate limiting básico

### **2.3 Variables de entorno**

Crear archivos `.env` para diferentes entornos:

```bash
# .env.development
POSTGRES_DB=ecommerce_dev
POSTGRES_USER=ecommerce_user
POSTGRES_PASSWORD=dev_password
REDIS_URL=redis://cache:6379
API_SECRET_KEY=dev-secret-key
ENVIRONMENT=development
DEBUG=true

# .env.production
POSTGRES_DB=ecommerce_prod
POSTGRES_USER=ecommerce_prod_user
POSTGRES_PASSWORD=super_secure_prod_password
REDIS_URL=redis://cache:6379
API_SECRET_KEY=production-secret-key-super-secure
ENVIRONMENT=production
DEBUG=false
```

---

## 📊 Fase 3: Monitoring y Observabilidad (90 min)

### **3.1 Métricas en la aplicación**

Implementar endpoints de métricas custom:

```python
@app.get("/metrics")
async def get_metrics():
    return {
        "http_requests_total": request_counter,
        "active_users": await get_active_users_count(),
        "products_in_stock": await get_products_count(),
        "orders_today": await get_orders_today(),
        "cache_hit_ratio": await get_cache_stats(),
        "response_time_avg": get_avg_response_time(),
        "error_rate": get_error_rate()
    }
```

### **3.2 Stack de monitoring**

Agregar servicios de monitoring al docker-compose:

```yaml
# Agregar al docker-compose.yml
prometheus:
  image: prom/prometheus:latest
  # Configuración para scraping de métricas

grafana:
  image: grafana/grafana:latest
  # Dashboards pre-configurados

alertmanager:
  image: prom/alertmanager:latest
  # Alertas básicas configuradas
```

### **3.3 Dashboards y alertas**

**Dashboard de Grafana debe incluir:**

- Request rate y response time
- Error rate y status codes
- Database performance metrics
- Cache hit ratio
- System resources (CPU, Memory)
- Business metrics (orders, products, users)

**Alertas básicas:**

- API response time > 1s
- Error rate > 5%
- Database connections > 80%
- Memory usage > 90%

---

## 🔒 Fase 4: Seguridad y Producción (90 min)

### **4.1 Hardening de seguridad**

**En Dockerfile:**

```dockerfile
# Usuario no-root
RUN adduser -D -s /bin/sh appuser
USER appuser

# Filesystem read-only
# Security labels
# Resource limits
```

**En docker-compose:**

```yaml
services:
  api:
    security_opt:
      - no-new-privileges:true
    read_only: true
    tmpfs:
      - /tmp
    mem_limit: 512m
    cpus: 0.5
```

### **4.2 Configuración de producción**

Crear `docker-compose.production.yml` con:

- Configuraciones optimizadas para producción
- Secrets management básico
- Resource limits apropiados
- Security hardening aplicado
- Backup strategy para datos

### **4.3 SSL y networking**

**Nginx con SSL:**

- Certificados auto-firmados para desarrollo
- Configuración para Let's Encrypt en producción
- HTTP/2 habilitado
- Security headers configurados

**Networking:**

- Segmentación de redes
- Firewalling básico
- Exposición mínima de puertos

---

## 🚀 Fase 5: Deployment y CI/CD (90 min)

### **5.1 Scripts de deployment**

```bash
#!/bin/bash
# scripts/deploy.sh
set -e

ENVIRONMENT=${1:-development}
VERSION=${2:-latest}

echo "🚀 Deploying E-commerce to $ENVIRONMENT"

# Validaciones
# Backup (si es producción)
# Rolling update
# Health checks
# Rollback en caso de error
```

### **5.2 CI/CD Pipeline básico**

Crear `.github/workflows/docker-deploy.yml`:

```yaml
name: E-commerce Docker Deploy

on:
  push:
    branches: [main, develop]

jobs:
  test:
    # Tests automatizados

  security-scan:
    # Scan de vulnerabilidades

  build-and-push:
    # Build y push de imágenes

  deploy:
    # Deployment automatizado
```

### **5.3 Testing de deployment**

Suite de tests para validar deployment:

```python
# tests/test_deployment.py
import pytest
import httpx

class TestDeployment:
    def test_api_health(self):
        # Test health endpoints

    def test_database_connectivity(self):
        # Test DB operations

    def test_cache_functionality(self):
        # Test Redis operations

    def test_full_user_journey(self):
        # Test complete e-commerce flow
```

---

## 📊 Especificaciones Técnicas Detalladas

### **API Endpoints Requeridos**

```
Authentication:
POST /auth/register    # Registro de usuario
POST /auth/login      # Login con JWT
POST /auth/logout     # Logout
GET  /auth/me         # Perfil de usuario

Products:
GET    /products           # Listar productos
POST   /products           # Crear producto (admin)
GET    /products/{id}      # Detalle de producto
PUT    /products/{id}      # Actualizar producto (admin)
DELETE /products/{id}      # Eliminar producto (admin)

Orders:
POST /orders              # Crear orden
GET  /orders              # Listar órdenes del usuario
GET  /orders/{id}         # Detalle de orden
PUT  /orders/{id}/status  # Actualizar status (admin)

Cart:
POST   /cart/add         # Agregar al carrito
GET    /cart             # Ver carrito
PUT    /cart/{item_id}   # Actualizar cantidad
DELETE /cart/{item_id}   # Remover del carrito

Admin:
GET /admin/dashboard     # Dashboard de admin
GET /admin/analytics     # Analytics básicas

System:
GET /health             # Health check
GET /metrics            # Métricas Prometheus
GET /docs               # API documentation
```

### **Modelos de Datos**

```python
# models.py estructura esperada
class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Product(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2))
    stock = Column(Integer, default=0)
    category_id = Column(Integer, ForeignKey('categories.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    total = Column(Numeric(10, 2))
    status = Column(String, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)

# Más modelos según sea necesario...
```

### **Performance Targets**

- **API Response Time**: < 200ms promedio
- **Database Query Time**: < 50ms promedio
- **Cache Hit Ratio**: > 80%
- **Container Startup Time**: < 30 segundos
- **Image Size**: API < 200MB, Total stack < 1GB
- **Memory Usage**: API < 512MB, DB < 1GB
- **CPU Usage**: < 50% promedio

---

## 🏆 Criterios de Evaluación

### **Funcionalidad (30 puntos)**

- ✅ **API completa** (15 pts) - Todos los endpoints funcionando
- ✅ **E-commerce flow** (10 pts) - Registro, login, compra, admin
- ✅ **Autenticación** (5 pts) - JWT funcionando correctamente

### **Containerización (25 puntos)**

- ✅ **Dockerfile optimizado** (10 pts) - Multi-stage, seguridad, tamaño
- ✅ **Docker Compose** (10 pts) - Servicios, networks, volumes
- ✅ **Configuración** (5 pts) - Variables de entorno, secrets

### **Observabilidad (20 puntos)**

- ✅ **Health checks** (5 pts) - API, DB, Redis funcionando
- ✅ **Métricas** (10 pts) - Prometheus metrics implementadas
- ✅ **Logging** (5 pts) - Structured logging configurado

### **Seguridad (15 puntos)**

- ✅ **Container security** (8 pts) - Usuario no-root, resource limits
- ✅ **Network security** (4 pts) - Segmentación, exposición mínima
- ✅ **Application security** (3 pts) - Input validation, SQL injection prevention

### **Deployment (10 puntos)**

- ✅ **Scripts** (5 pts) - Deploy, backup, rollback scripts
- ✅ **CI/CD** (3 pts) - Pipeline básico funcionando
- ✅ **Documentation** (2 pts) - README completo, instrucciones claras

---

## 🎯 Entregables Finales

### **Estructura del proyecto**

```
semana-09-proyecto/
├── app/
│   ├── main.py              # FastAPI app principal
│   ├── models.py            # Modelos SQLAlchemy
│   ├── routers/             # Routers organizados por dominio
│   ├── middleware.py        # Logging y metrics middleware
│   ├── config.py            # Configuración centralizada
│   └── utils.py             # Utilidades
├── config/
│   ├── nginx.conf           # Configuración Nginx
│   ├── redis.conf           # Configuración Redis
│   ├── prometheus.yml       # Configuración Prometheus
│   └── grafana-dashboard.json # Dashboard Grafana
├── monitoring/
│   ├── alerts.yml           # Reglas de alertas
│   └── dashboards/          # Dashboards adicionales
├── scripts/
│   ├── deploy.sh            # Script de deployment
│   ├── backup.sh            # Script de backup
│   ├── restore.sh           # Script de restore
│   └── health-check.sh      # Script de health check
├── tests/
│   ├── test_api.py          # Tests de API
│   ├── test_deployment.py   # Tests de deployment
│   └── test_integration.py  # Tests de integración
├── .github/workflows/
│   └── docker-deploy.yml    # CI/CD pipeline
├── database/
│   ├── init.sql             # Script de inicialización
│   └── sample-data.sql      # Datos de ejemplo
├── Dockerfile               # Dockerfile optimizado
├── docker-compose.yml       # Compose para development
├── docker-compose.production.yml # Compose para producción
├── requirements.txt         # Dependencias Python
├── .env.example            # Template de variables
├── .dockerignore           # Files to ignore
└── README.md               # Documentación completa
```

### **README.md debe incluir**

- ✅ **Descripción del proyecto** y arquitectura
- ✅ **Instrucciones de setup** para development
- ✅ **Comandos para deployment** en diferentes entornos
- ✅ **Documentación de API** (enlaces a /docs)
- ✅ **Configuración de monitoring** y dashboards
- ✅ **Troubleshooting** común
- ✅ **Roadmap** de mejoras futuras

---

## 🚀 Comandos de Validación

### **Setup y ejecución**

```bash
# 1. Clonar y setup
git clone <repository>
cd semana-09-proyecto

# 2. Levantar entorno de desarrollo
cp .env.example .env
docker-compose up --build -d

# 3. Verificar que todos los servicios están healthy
docker-compose ps

# 4. Ejecutar tests
./scripts/health-check.sh
python -m pytest tests/ -v

# 5. Verificar funcionalidad completa
curl http://localhost/docs              # API docs
curl http://localhost/health            # Health check
curl http://localhost:3000              # Grafana dashboard

# 6. Test de producción
docker-compose -f docker-compose.production.yml up -d
./scripts/deploy.sh production latest
```

### **Performance validation**

```bash
# Test de carga básico
ab -n 1000 -c 10 http://localhost/products

# Métricas de containers
docker stats

# Verificar métricas
curl http://localhost/metrics
```

---

## 🎉 Proyecto Destacado

Al completar este proyecto habrás creado un **sistema e-commerce completamente containerizado y production-ready** que incluye:

- 🛍️ **E-commerce completo** con todas las funcionalidades
- 🐳 **Containerización profesional** con Docker
- 📊 **Observabilidad completa** con monitoring
- 🔒 **Seguridad implementada** en todos los niveles
- 🚀 **Deployment automatizado** listo para cloud
- 📚 **Documentación profesional** para equipos

¡Este proyecto será una excelente adición a tu portfolio profesional! 🌟

---

_Proyecto Semana 9 - Bootcamp FastAPI_  
_Tiempo total: 6 horas distribuidas en 4 prácticas de 90 minutos_
