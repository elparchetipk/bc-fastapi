# Proyecto Final - Semana 9: E-commerce Containerizado

## 📋 Información General

Este es el proyecto final de la semana 9, donde aplicarás todos los conocimientos adquiridos sobre containerización con Docker para desarrollar un sistema completo de e-commerce con arquitectura de microservicios.

## 🎯 Objetivos del Proyecto

- **Implementar** una aplicación FastAPI completa containerizada
- **Orquestar** múltiples servicios con Docker Compose
- **Configurar** pipeline de CI/CD automatizado
- **Implementar** monitoreo y observabilidad
- **Aplicar** mejores prácticas de seguridad
- **Documentar** la arquitectura y deployment

## 📁 Estructura del Proyecto

```
proyecto-ecommerce/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   └── main.py
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── database/
│   ├── init/
│   └── migrations/
├── nginx/
│   └── nginx.conf
├── monitoring/
│   ├── prometheus/
│   └── grafana/
├── scripts/
│   ├── deploy.sh
│   ├── backup.sh
│   └── health-check.sh
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── docker-compose.yml
├── docker-compose.prod.yml
├── .env.example
└── README.md
```

## ⏱️ Estimación de Tiempo

| Fase       | Actividad                   | Tiempo | Dificultad   |
| ---------- | --------------------------- | ------ | ------------ |
| **Fase 1** | Desarrollo Backend API      | 2.5h   | Intermedia   |
| **Fase 2** | Containerización            | 1h     | Básica       |
| **Fase 3** | Orquestación Multi-servicio | 1h     | Intermedia   |
| **Fase 4** | CI/CD y Deployment          | 1h     | Avanzada     |
| **Fase 5** | Monitoreo y Seguridad       | 1h     | Avanzada     |
| **Fase 6** | Documentación y Testing     | 0.5h   | Básica       |
| **Total**  |                             | **7h** | **Avanzada** |

> **Nota**: El tiempo puede variar según la experiencia previa. Se recomienda priorizar las fases 1-3 si se cuenta con tiempo limitado.

## 🚀 Quick Start

### Prerrequisitos

```bash
# Verificar instalaciones
docker --version                 # >= 20.10
docker-compose --version         # >= 1.29
git --version                   # >= 2.25
```

### Instalación Rápida

```bash
# 1. Clonar proyecto base (si se proporciona)
git clone [repository-url] proyecto-ecommerce
cd proyecto-ecommerce

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# 3. Construir y levantar servicios
docker-compose up --build -d

# 4. Verificar servicios
docker-compose ps
docker-compose logs -f

# 5. Acceder a la aplicación
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# Grafana: http://localhost:3001
# Prometheus: http://localhost:9090
```

## 📋 Checklist de Desarrollo

### ✅ Fase 1: Backend API (2.5h)

#### Funcionalidades Básicas

- [ ] **Autenticación** (registro, login, JWT)
- [ ] **Gestión de usuarios** (perfil, roles)
- [ ] **Catálogo de productos** (CRUD productos)
- [ ] **Carrito de compras** (agregar, quitar, actualizar)
- [ ] **Órdenes** (crear, consultar, actualizar estado)
- [ ] **Endpoints de salud** (/health, /metrics)

#### Estructura Técnica

- [ ] **Models** con SQLAlchemy
- [ ] **Schemas** con Pydantic
- [ ] **API Routes** organizadas por módulos
- [ ] **Middleware** de autenticación
- [ ] **Exception handlers** personalizados
- [ ] **Logging** configurado
- [ ] **Tests unitarios** básicos

### ✅ Fase 2: Containerización (1h)

#### Backend Dockerfile

- [ ] **Multi-stage build** implementado
- [ ] **Imagen base** optimizada (python:slim)
- [ ] **Usuario no-root** configurado
- [ ] **Dependencies** cachadas eficientemente
- [ ] **Health check** incluido
- [ ] **Variables de entorno** parametrizadas

#### Frontend Dockerfile

- [ ] **Build stage** para compilación
- [ ] **Nginx** para servir archivos estáticos
- [ ] **Configuración** optimizada para producción

### ✅ Fase 3: Orquestación (1h)

#### Docker Compose

- [ ] **Servicios** definidos (app, db, redis, nginx)
- [ ] **Networks** configuradas correctamente
- [ ] **Volumes** para persistencia
- [ ] **Environment variables** organizadas
- [ ] **Dependencies** entre servicios
- [ ] **Health checks** en servicios críticos

#### Servicios Incluidos

- [ ] **FastAPI** (backend)
- [ ] **PostgreSQL** (base de datos)
- [ ] **Redis** (cache/sessions)
- [ ] **Nginx** (proxy reverso)
- [ ] **Prometheus** (métricas)
- [ ] **Grafana** (visualización)

### ✅ Fase 4: CI/CD (1h)

#### GitHub Actions

- [ ] **Workflow** de CI/CD configurado
- [ ] **Tests** automatizados
- [ ] **Build** de imágenes Docker
- [ ] **Security scanning** con Trivy
- [ ] **Push** a registry
- [ ] **Deploy** a staging/producción

#### Pipeline Stages

- [ ] **Lint** y **format check**
- [ ] **Unit tests** y **coverage**
- [ ] **Security scans**
- [ ] **Docker build** y **push**
- [ ] **Deployment** condicional

### ✅ Fase 5: Monitoreo y Seguridad (1h)

#### Observabilidad

- [ ] **Prometheus** métricas configuradas
- [ ] **Grafana** dashboards importados
- [ ] **Health checks** en todos los servicios
- [ ] **Logging** centralizado
- [ ] **Alertas** básicas configuradas

#### Seguridad

- [ ] **Secrets** gestionados correctamente
- [ ] **Network policies** aplicadas
- [ ] **Image scanning** configurado
- [ ] **Non-root users** en contenedores
- [ ] **Security headers** en Nginx

### ✅ Fase 6: Documentación (0.5h)

#### Documentación Técnica

- [ ] **README.md** completo
- [ ] **API documentation** actualizada
- [ ] **Architecture diagram** incluido
- [ ] **Deployment guide** detallado
- [ ] **Troubleshooting** section

## 🎯 Criterios de Evaluación

### Funcionalidad (30%)

- **API completa**: Todos los endpoints funcionan correctamente
- **Base de datos**: Modelos y relaciones implementadas
- **Autenticación**: Sistema de usuarios funcional
- **Frontend básico**: Interfaz para probar la API

### Containerización (25%)

- **Dockerfiles optimizados**: Multi-stage, security, size
- **Imágenes eficientes**: Tiempo de build y tamaño
- **Configuración correcta**: Variables de entorno, health checks

### Orquestación (20%)

- **Docker Compose**: Servicios bien definidos
- **Networking**: Comunicación entre servicios
- **Persistence**: Volúmenes correctamente configurados
- **Escalabilidad**: Capacidad de escalar servicios

### DevOps (15%)

- **CI/CD**: Pipeline automatizado funcional
- **Testing**: Tests automatizados pasando
- **Security**: Vulnerabilities scanning implementado
- **Deployment**: Proceso de deploy automatizado

### Observabilidad (10%)

- **Monitoring**: Métricas y dashboards configurados
- **Logging**: Logs centralizados y estructurados
- **Health checks**: Monitoreo de salud de servicios
- **Alerting**: Alertas básicas configuradas

## 🛠️ Comandos de Validación

### Verificación de Funcionalidad

```bash
# 1. Verificar que todos los servicios estén running
docker-compose ps

# 2. Health checks
curl http://localhost:8000/health
curl http://localhost:8000/metrics

# 3. API endpoints básicos
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# 4. Frontend accesible
curl -I http://localhost:3000

# 5. Monitoreo accesible
curl -I http://localhost:3001  # Grafana
curl -I http://localhost:9090  # Prometheus
```

### Validación de Seguridad

```bash
# Scan de vulnerabilidades
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasecurity/trivy image proyecto-ecommerce_app:latest

# Verificar usuarios no-root
docker-compose exec app whoami

# Verificar puertos expuestos
docker-compose port app 8000
```

### Performance y Recursos

```bash
# Métricas de recursos
docker stats

# Tiempo de inicio
docker-compose down
time docker-compose up -d

# Tamaño de imágenes
docker images | grep proyecto-ecommerce
```

## 🔧 Scripts de Utilidad

### Script de Deployment

```bash
#!/bin/bash
# scripts/deploy.sh

set -e

echo "🚀 Starting deployment..."

# Build images
echo "📦 Building images..."
docker-compose build

# Run tests
echo "🧪 Running tests..."
docker-compose run --rm app python -m pytest

# Deploy
echo "🌐 Deploying services..."
docker-compose up -d

# Health checks
echo "🏥 Checking health..."
sleep 10
curl -f http://localhost:8000/health || exit 1

echo "✅ Deployment successful!"
```

### Script de Backup

```bash
#!/bin/bash
# scripts/backup.sh

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

echo "💾 Creating backup..."

# Database backup
docker-compose exec -T db pg_dump -U postgres ecommerce > $BACKUP_DIR/database.sql

# Application data backup
docker run --rm -v proyecto-ecommerce_app_data:/data -v $PWD/$BACKUP_DIR:/backup alpine tar czf /backup/app_data.tar.gz /data

echo "✅ Backup created in $BACKUP_DIR"
```

## 📚 Recursos de Apoyo

### Documentación de Referencia

- [Especificación completa](./especificacion-docker.md)
- [Docker Cheatsheet](../5-recursos/docker-cheatsheet.md)
- [Herramientas Docker](../5-recursos/herramientas-docker.md)

### Templates y Ejemplos

- **FastAPI**: [Documentación oficial](https://fastapi.tiangolo.com/)
- **Docker Compose**: [Awesome Compose](https://github.com/docker/awesome-compose)
- **GitHub Actions**: [Docker workflows](https://docs.github.com/en/actions/publishing-packages/publishing-docker-images)

### Debugging

```bash
# Ver logs detallados
docker-compose logs -f [servicio]

# Acceder a contenedor
docker-compose exec [servicio] /bin/bash

# Verificar configuración
docker-compose config

# Reiniciar servicio
docker-compose restart [servicio]
```

## 🚨 Troubleshooting Común

### Problema: Puerto en uso

```bash
# Encontrar proceso
sudo lsof -i :8000
# Cambiar puerto en docker-compose.yml
```

### Problema: Base de datos no conecta

```bash
# Verificar red
docker network inspect proyecto-ecommerce_default
# Verificar logs de DB
docker-compose logs db
```

### Problema: Imagen muy grande

```bash
# Analizar capas
dive proyecto-ecommerce_app:latest
# Optimizar Dockerfile con multi-stage
```

## 📬 Entrega del Proyecto

### Repositorio

1. **Crear repositorio** público en GitHub
2. **Estructura clara** siguiendo el template
3. **README.md** profesional con instrucciones
4. **Commits descriptivos** documentando el progreso

### Documentación Required

- [ ] **README.md** principal con quick start
- [ ] **ARCHITECTURE.md** con diagrama de la solución
- [ ] **DEPLOYMENT.md** con instrucciones de producción
- [ ] **API.md** con documentación de endpoints
- [ ] **MONITORING.md** con guía de observabilidad

### Evidencias

- [ ] **Screenshots** de la aplicación funcionando
- [ ] **Video demo** (opcional, 2-3 minutos)
- [ ] **Logs** de deployment exitoso
- [ ] **Métricas** de monitoreo funcionando

## 🎉 Criterios de Éxito

### Mínimo Viable (Aprobado)

- ✅ API básica funcionando
- ✅ Containerización correcta
- ✅ Docker Compose orquestando servicios
- ✅ Documentación básica

### Implementación Completa (Excelente)

- ✅ Todas las funcionalidades implementadas
- ✅ CI/CD pipeline funcionando
- ✅ Monitoreo configurado
- ✅ Seguridad aplicada
- ✅ Documentación profesional

### Implementación Avanzada (Sobresaliente)

- ✅ Optimizaciones avanzadas
- ✅ Features adicionales
- ✅ Tests comprehensivos
- ✅ Deployment multi-ambiente
- ✅ Innovaciones técnicas

---

## 💡 Consejos Finales

1. **Planifica bien** el tiempo - es un proyecto extenso
2. **Empieza simple** y ve agregando complejidad
3. **Testea frecuentemente** cada componente
4. **Documenta mientras desarrollas**
5. **No dudes en consultar** los recursos proporcionados
6. **Prioriza la funcionalidad** sobre características avanzadas

---

**¡Éxito con tu proyecto de e-commerce containerizado! 🐳🛒**
