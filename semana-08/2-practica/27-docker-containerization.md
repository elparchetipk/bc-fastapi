# Práctica 27: Containerización con Docker

## 📋 Descripción

Aprende a containerizar aplicaciones FastAPI usando Docker, desde conceptos básicos hasta estrategias avanzadas de optimización.

## 🎯 Objetivos Específicos

- ✅ Crear Dockerfiles optimizados para FastAPI
- ✅ Implementar multi-stage builds
- ✅ Configurar Docker Compose para desarrollo
- ✅ Gestionar imágenes y registros

## ⏱️ Tiempo Estimado: 75 minutos

---

## 📚 Conceptos Clave

### 🐳 **¿Qué es Docker?**

Docker es una plataforma de containerización que permite:

- Empaquetar aplicaciones con sus dependencias
- Garantizar consistencia entre entornos
- Facilitar deployment y escalabilidad
- Aislar aplicaciones y recursos

### 🏗️ **Componentes Principales**

```yaml
# Ecosistema Docker
Dockerfile: Receta para construir imágenes
Image: Plantilla inmutable de la aplicación
Container: Instancia ejecutable de una imagen
Registry: Repositorio de imágenes (Docker Hub, ECR)
Compose: Orquestación de múltiples servicios
```

---

## 🛠️ Desarrollo Práctico

### **Paso 1: Proyecto Base FastAPI**

Primero, creemos una aplicación FastAPI simple:

```python
# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI(
    title="API Containerized",
    description="FastAPI app optimizada para Docker",
    version="1.0.0"
)

class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str

@app.get("/")
async def root():
    return {"message": "FastAPI en Docker! 🐳"}

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )

@app.get("/info")
async def get_info():
    return {
        "python_version": "3.11",
        "fastapi_version": "0.104.1",
        "container": os.getenv("HOSTNAME", "localhost")
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
```

### **Paso 2: Dockerfile Básico**

Crea tu primer Dockerfile:

```dockerfile
# Dockerfile.basic
FROM python:3.11-slim

# Metadata
LABEL maintainer="tu-email@ejemplo.com"
LABEL description="FastAPI Containerized App"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Directorio de trabajo
WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app/ ./app/

# Exponer puerto
EXPOSE 8000

# Usuario no-root
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Paso 3: Requirements Optimizado**

```txt
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
```

### **Paso 4: Dockerfile Multi-Stage**

Para optimización avanzada:

```dockerfile
# Dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias de build
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim as runtime

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/appuser/.local/bin:$PATH"

# Crear usuario
RUN useradd --create-home --shell /bin/bash appuser

# Copiar dependencias desde builder
COPY --from=builder /root/.local /home/appuser/.local

# Cambiar al usuario app
USER appuser
WORKDIR /home/appuser/app

# Copiar código de aplicación
COPY --chown=appuser:appuser app/ .

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# Comando de inicio
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Paso 5: Docker Compose para Desarrollo**

```yaml
# docker-compose.yml
version: '3.8'

services:
  # FastAPI Application
  fastapi-app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fastapi-container
    ports:
      - '8000:8000'
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://user:password@postgres:5432/fastapi_db
    volumes:
      - ./app:/home/appuser/app
    depends_on:
      - postgres
      - redis
    networks:
      - app-network
    restart: unless-stopped

  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: fastapi_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - '5432:5432'
    networks:
      - app-network
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - '6379:6379'
    volumes:
      - redis_data:/data
    networks:
      - app-network
    restart: unless-stopped

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - '80:80'
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - fastapi-app
    networks:
      - app-network
    restart: unless-stopped

# Named volumes
volumes:
  postgres_data:
  redis_data:

# Networks
networks:
  app-network:
    driver: bridge
```

### **Paso 6: Configuración Nginx**

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream fastapi {
        server fastapi-app:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # Security headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;

        # Logging
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        # Main application
        location / {
            proxy_pass http://fastapi;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Static files (if any)
        location /static {
            alias /app/static;
            expires 1d;
            add_header Cache-Control "public, immutable";
        }

        # Health check
        location /health {
            proxy_pass http://fastapi/health;
            access_log off;
        }
    }
}
```

---

## 🔨 Ejercicios Prácticos

### **Ejercicio 1: Build y Run Básico**

```bash
# 1. Construir imagen
docker build -t mi-fastapi-app .

# 2. Ejecutar contenedor
docker run -d -p 8000:8000 --name fastapi-container mi-fastapi-app

# 3. Verificar logs
docker logs fastapi-container

# 4. Probar aplicación
curl http://localhost:8000/health
```

### **Ejercicio 2: Docker Compose**

```bash
# 1. Levantar todos los servicios
docker-compose up -d

# 2. Ver estado de servicios
docker-compose ps

# 3. Ver logs
docker-compose logs fastapi-app

# 4. Escalar aplicación
docker-compose up -d --scale fastapi-app=3

# 5. Limpiar
docker-compose down -v
```

### **Ejercicio 3: Optimización de Imagen**

```dockerfile
# Dockerfile.optimized
FROM python:3.11-alpine as builder

# Instalar dependencias de compilación
RUN apk add --no-cache gcc musl-dev libffi-dev

WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-alpine

# Instalar dependencias de runtime
RUN apk add --no-cache curl

# Copiar wheels desde builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Instalar desde wheels
RUN pip install --no-cache /wheels/*

# Crear usuario
RUN adduser -D -s /bin/sh appuser
USER appuser

WORKDIR /home/appuser/app
COPY --chown=appuser:appuser app/ .

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📊 Scripts de Utilidad

### **Script de Build Automatizado**

```bash
#!/bin/bash
# scripts/build.sh

set -e

IMAGE_NAME="mi-fastapi-app"
VERSION=${1:-latest}
REGISTRY=${2:-""}

echo "🐳 Building Docker image..."

# Build multi-platform
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag ${IMAGE_NAME}:${VERSION} \
    --tag ${IMAGE_NAME}:latest \
    .

# Tag para registry si se especifica
if [ ! -z "$REGISTRY" ]; then
    docker tag ${IMAGE_NAME}:${VERSION} ${REGISTRY}/${IMAGE_NAME}:${VERSION}
    echo "📦 Tagged for registry: ${REGISTRY}/${IMAGE_NAME}:${VERSION}"
fi

echo "✅ Build completed successfully!"

# Mostrar información de la imagen
docker images ${IMAGE_NAME}:${VERSION}
```

### **Script de Health Check**

```bash
#!/bin/bash
# scripts/healthcheck.sh

CONTAINER_NAME=${1:-fastapi-container}
MAX_ATTEMPTS=30
ATTEMPT=1

echo "🔍 Checking health of container: $CONTAINER_NAME"

while [ $ATTEMPT -le $MAX_ATTEMPTS ]; do
    if docker exec $CONTAINER_NAME curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Container is healthy!"
        exit 0
    fi

    echo "⏳ Attempt $ATTEMPT/$MAX_ATTEMPTS - Container not ready yet..."
    sleep 2
    ((ATTEMPT++))
done

echo "❌ Container failed health check after $MAX_ATTEMPTS attempts"
exit 1
```

---

## 🎯 Mejores Prácticas

### **📋 Dockerfile Best Practices**

1. **Usar imágenes base pequeñas** (alpine, slim)
2. **Multi-stage builds** para reducir tamaño
3. **Cachear layers** ordenando comandos eficientemente
4. **Usuario no-root** para seguridad
5. **Health checks** para monitoreo
6. **Variables de entorno** para configuración

### **🔧 Optimización de Performance**

```dockerfile
# Optimizaciones comunes
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Ordenar comandos para aprovechar cache
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ .
```

### **🛡️ Seguridad**

```dockerfile
# Escanear vulnerabilidades
RUN apt-get update && apt-get upgrade -y

# Usuario no-root
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Secrets como variables de entorno
ENV DATABASE_PASSWORD_FILE=/run/secrets/db_password
```

---

## ✅ Checklist de Validación

### **🐳 Docker Setup**

- [ ] Dockerfile creado y optimizado
- [ ] Multi-stage build implementado
- [ ] Usuario no-root configurado
- [ ] Health check funcionando

### **🏗️ Docker Compose**

- [ ] Servicios definidos correctamente
- [ ] Redes y volúmenes configurados
- [ ] Variables de entorno gestionadas
- [ ] Dependencias entre servicios

### **🔧 Optimización**

- [ ] Imagen final < 200MB
- [ ] Build time < 2 minutos
- [ ] Startup time < 10 segundos
- [ ] Health check respondiendo

### **📝 Documentación**

- [ ] README con instrucciones
- [ ] Scripts de automatización
- [ ] Configuraciones documentadas
- [ ] Troubleshooting guide

---

## 📚 Recursos Adicionales

### **🔗 Enlaces Útiles**

- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI Docker](https://fastapi.tiangolo.com/deployment/docker/)
- [Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)

### **🛠️ Herramientas**

- **Docker Desktop**: Desarrollo local
- **Docker Scout**: Análisis de vulnerabilidades
- **Hadolint**: Linter para Dockerfiles
- **Dive**: Análisis de capas de imagen

---

## 🚀 Entregables

1. **Dockerfile optimizado** con multi-stage build
2. **Docker Compose** para stack completo
3. **Scripts de automatización** (build, deploy, health)
4. **Documentación** de setup y troubleshooting

## ⏭️ Próximos Pasos

En la siguiente práctica trabajaremos con **GitHub Actions** para automatizar el proceso de build y deployment de nuestras imágenes Docker.
