# Práctica 32: Dockerfile para FastAPI

⏰ **Tiempo estimado**: 90 minutos  
🎯 **Objetivo**: Crear un Dockerfile optimizado para aplicaciones FastAPI

---

## 📋 Qué vas a lograr

Al final de esta práctica habrás:

- ✅ Creado tu primer Dockerfile para FastAPI
- ✅ Implementado multi-stage builds
- ✅ Optimizado el tamaño de la imagen
- ✅ Configurado variables de entorno
- ✅ Aplicado buenas prácticas de seguridad

---

## 🏗️ Paso 1: Preparación del Proyecto (15 min)

### **Estructura del proyecto**

```bash
# 1. Crear directorio de trabajo
mkdir fastapi-docker-optimized
cd fastapi-docker-optimized

# 2. Crear estructura de directorios
mkdir -p app tests

# 3. Verificar estructura
tree . || ls -la
```

### **Crear aplicación FastAPI**

```python
# app/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import platform
from datetime import datetime
import psutil

app = FastAPI(
    title="FastAPI Dockerized",
    description="API optimizada para containers",
    version="1.0.0"
)

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str
    environment: str

class SystemInfo(BaseModel):
    platform: str
    python_version: str
    cpu_count: int
    memory_mb: float
    hostname: str

@app.get("/")
async def root():
    return {
        "message": "🐳 FastAPI en Docker optimizado",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )

@app.get("/system", response_model=SystemInfo)
async def system_info():
    return SystemInfo(
        platform=platform.platform(),
        python_version=platform.python_version(),
        cpu_count=psutil.cpu_count(),
        memory_mb=psutil.virtual_memory().total / 1024 / 1024,
        hostname=os.getenv("HOSTNAME", "unknown")
    )

@app.get("/env")
async def environment_variables():
    """Endpoint para debugging - NO usar en producción"""
    env_vars = {
        key: value for key, value in os.environ.items()
        if not any(secret in key.lower() for secret in ['password', 'secret', 'key', 'token'])
    }
    return {"environment_variables": env_vars}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### **Archivo de dependencias**

```text
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
psutil==5.9.0
pydantic==2.5.0
```

### **Configuración adicional**

```bash
# .dockerignore
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis
.DS_Store
*.egg-info/
dist/
build/
docs/_build/
README.md
Dockerfile*
docker-compose*
.dockerignore
```

---

## 🐳 Paso 2: Dockerfile Básico (20 min)

### **Primera versión: Dockerfile simple**

```dockerfile
# Dockerfile.basic
FROM python:3.13

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app/ ./app/

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Build y test básico**

```bash
# 1. Build de la imagen
docker build -f Dockerfile.basic -t fastapi-basic .

# 2. Ver tamaño de la imagen
docker images fastapi-basic

# 3. Ejecutar container
docker run -d --name fastapi-basic-test -p 8000:8000 fastapi-basic

# 4. Probar endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
curl http://localhost:8000/system

# 5. Ver logs
docker logs fastapi-basic-test

# 6. Limpiar
docker rm -f fastapi-basic-test
```

### **Análisis del resultado**

```bash
# Ver capas de la imagen
docker history fastapi-basic

# Ver detalles de la imagen
docker inspect fastapi-basic | grep -A 5 -B 5 "Size"
```

---

## ⚡ Paso 3: Dockerfile Optimizado (25 min)

### **Versión optimizada con Alpine**

```dockerfile
# Dockerfile.optimized
FROM python:3.13-alpine

# Instalar dependencias del sistema necesarias
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    && rm -rf /var/cache/apk/*

# Crear usuario no-root
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código de aplicación
COPY app/ ./app/

# Cambiar ownership de archivos al usuario no-root
RUN chown -R appuser:appgroup /app

# Cambiar a usuario no-root
USER appuser

# Exponer puerto
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Build y comparación**

```bash
# 1. Build de la versión optimizada
docker build -f Dockerfile.optimized -t fastapi-optimized .

# 2. Comparar tamaños
docker images | grep fastapi

# 3. Ejecutar y probar
docker run -d --name fastapi-opt-test -p 8001:8000 fastapi-optimized

# 4. Verificar que funciona
curl http://localhost:8001/health

# 5. Verificar health check
docker ps  # Ver status del health check

# 6. Limpiar
docker rm -f fastapi-opt-test
```

---

## 🏗️ Paso 4: Multi-Stage Build (25 min)

### **Dockerfile con multi-stage**

```dockerfile
# Dockerfile.multistage
# Stage 1: Build stage
FROM python:3.13-alpine AS builder

# Instalar dependencias de build
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    build-base

# Crear directorio para dependencias
WORKDIR /install

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias en directorio específico
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.13-alpine AS production

# Instalar solo dependencias runtime necesarias
RUN apk add --no-cache curl

# Crear usuario no-root
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

# Copiar dependencias instaladas desde build stage
COPY --from=builder /install /usr/local

# Establecer directorio de trabajo
WORKDIR /app

# Copiar código de aplicación
COPY app/ ./app/

# Cambiar ownership al usuario no-root
RUN chown -R appuser:appgroup /app

# Cambiar a usuario no-root
USER appuser

# Variables de entorno
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production

# Exponer puerto
EXPOSE 8000

# Health check más eficiente
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

### **Build y análisis**

```bash
# 1. Build multi-stage
docker build -f Dockerfile.multistage -t fastapi-multistage .

# 2. Comparar todos los tamaños
docker images | grep fastapi

# 3. Analizar capas
docker history fastapi-multistage

# 4. Ejecutar y probar
docker run -d --name fastapi-multi-test -p 8002:8000 fastapi-multistage

# 5. Verificar endpoints
curl http://localhost:8002/health
curl http://localhost:8002/system
curl http://localhost:8002/env

# 6. Monitorear health checks
watch -n 2 "docker ps | grep fastapi-multi-test"

# 7. Limpiar
docker rm -f fastapi-multi-test
```

---

## 🔧 Paso 5: Variables de Entorno y Configuración (15 min)

### **Archivo de configuración**

```python
# app/config.py
import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    # App settings
    app_name: str = "FastAPI Docker"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False

    # Server settings
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1

    # Database settings (para futuro uso)
    database_url: str = "sqlite:///./app.db"

    # Security settings
    secret_key: str = "your-secret-key-change-in-production"

    # External services
    redis_url: str = "redis://localhost:6379"

    class Config:
        env_file = ".env"
        case_sensitive = False

# Instancia global de configuración
settings = Settings()
```

### **Actualizar main.py para usar configuración**

```python
# Agregar al inicio de app/main.py
from app.config import settings

# Actualizar la creación de FastAPI
app = FastAPI(
    title=settings.app_name,
    description="API optimizada para containers",
    version=settings.app_version,
    debug=settings.debug
)

# Actualizar endpoint de health
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.app_version,
        environment=settings.environment
    )

# Nuevo endpoint de configuración
@app.get("/config")
async def get_config():
    """Endpoint para verificar configuración (sin secretos)"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "debug": settings.debug,
        "host": settings.host,
        "port": settings.port,
        "workers": settings.workers
    }
```

### **Dockerfile final con configuración**

```dockerfile
# Dockerfile.final
# Build stage
FROM python:3.13-alpine AS builder

RUN apk add --no-cache gcc musl-dev linux-headers build-base

WORKDIR /install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.13-alpine AS production

RUN apk add --no-cache curl && \
    addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

COPY --from=builder /install /usr/local

WORKDIR /app
COPY app/ ./app/

RUN chown -R appuser:appgroup /app
USER appuser

# Variables de entorno con valores por defecto
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV ENVIRONMENT=production
ENV DEBUG=false
ENV HOST=0.0.0.0
ENV PORT=8000
ENV WORKERS=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# Usar variables de entorno en el comando
CMD uvicorn app.main:app --host ${HOST} --port ${PORT} --workers ${WORKERS}
```

### **Test con variables de entorno**

```bash
# 1. Build de la versión final
docker build -f Dockerfile.final -t fastapi-final .

# 2. Ejecutar con variables de entorno personalizadas
docker run -d \
  --name fastapi-final-test \
  -p 8003:8000 \
  -e ENVIRONMENT=production \
  -e DEBUG=false \
  -e APP_NAME="Mi API Dockerizada" \
  fastapi-final

# 3. Probar configuración
curl http://localhost:8003/config

# 4. Verificar health check
docker ps | grep fastapi-final-test

# 5. Ver logs
docker logs fastapi-final-test

# 6. Limpiar
docker rm -f fastapi-final-test
```

---

## 📊 Paso 6: Análisis y Comparación Final (10 min)

### **Comparación de imágenes**

```bash
# 1. Mostrar todas las imágenes creadas
docker images | grep fastapi

# 2. Análisis detallado
echo "=== COMPARACIÓN DE TAMAÑOS ==="
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}" | grep fastapi

# 3. Análisis de capas
echo "=== ANÁLISIS DE CAPAS (imagen final) ==="
docker history fastapi-final --format "table {{.CreatedBy}}\t{{.Size}}"
```

### **Benchmark de rendimiento**

```bash
# 1. Ejecutar todas las versiones en paralelo
docker run -d --name basic -p 8000:8000 fastapi-basic
docker run -d --name optimized -p 8001:8000 fastapi-optimized
docker run -d --name multistage -p 8002:8000 fastapi-multistage
docker run -d --name final -p 8003:8000 fastapi-final

# 2. Esperar que inicien
sleep 10

# 3. Test de rendimiento básico
echo "=== BENCHMARK BÁSICO ==="
for port in 8000 8001 8002 8003; do
    echo "Testing port $port:"
    time curl -s http://localhost:$port/health >/dev/null
done

# 4. Ver uso de recursos
docker stats --no-stream basic optimized multistage final

# 5. Limpiar todo
docker rm -f basic optimized multistage final
```

---

## 🔒 Paso 7: Buenas Prácticas de Seguridad (10 min)

### **Dockerfile con seguridad mejorada**

```dockerfile
# Dockerfile.secure
FROM python:3.13-alpine AS builder

# Instalar dependencias con versiones específicas
RUN apk add --no-cache \
    gcc=12.2.1_git20220924-r10 \
    musl-dev=1.2.4-r2 \
    linux-headers=6.0-r1 \
    build-base=0.5-r3

WORKDIR /install
COPY requirements.txt .

# Usar pip con flags de seguridad
RUN pip install --no-cache-dir --upgrade pip==23.3.1 && \
    pip install --prefix=/install --no-cache-dir --no-deps -r requirements.txt

FROM python:3.13-alpine AS production

# Instalar solo lo necesario
RUN apk add --no-cache curl=8.4.0-r0 && \
    rm -rf /var/cache/apk/*

# Crear usuario con UID/GID específicos
RUN addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup -s /bin/sh

COPY --from=builder /install /usr/local

# Crear directorio con permisos restrictivos
WORKDIR /app
RUN chown appuser:appgroup /app && \
    chmod 755 /app

# Copiar código y establecer permisos
COPY --chown=appuser:appgroup app/ ./app/
RUN chmod -R 644 /app && \
    chmod 755 /app

USER appuser

# Variables de entorno seguras
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

EXPOSE 8000

# Health check mejorado
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Labels para metadata
LABEL maintainer="tu-email@ejemplo.com"
LABEL version="1.0.0"
LABEL description="FastAPI aplicación securizada"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Escaneo de seguridad básico**

```bash
# 1. Build de la versión segura
docker build -f Dockerfile.secure -t fastapi-secure .

# 2. Escaneo básico con docker scan (si está disponible)
docker scan fastapi-secure || echo "Docker scan no disponible"

# 3. Verificar usuario no-root
docker run --rm fastapi-secure whoami

# 4. Verificar permisos
docker run --rm fastapi-secure ls -la /app

# 5. Test final
docker run -d --name secure-test -p 8004:8000 fastapi-secure
curl http://localhost:8004/health
docker rm -f secure-test
```

---

## 🏆 Verificación y Entregables

### **Checklist de completitud**

```bash
# ✅ 1. Todas las imágenes creadas exitosamente
docker images | grep fastapi | wc -l  # Debería mostrar 5+

# ✅ 2. Imagen final funciona correctamente
docker run -d --name final-check -p 8000:8000 fastapi-final
curl http://localhost:8000/health
docker rm -f final-check

# ✅ 3. Variables de entorno funcionan
docker run --rm -e ENVIRONMENT=testing fastapi-final \
    python -c "from app.config import settings; print(f'Environment: {settings.environment}')"

# ✅ 4. Health check configurado
docker inspect fastapi-final | grep -A 5 "Healthcheck"

# ✅ 5. Usuario no-root
docker run --rm fastapi-final whoami | grep appuser
```

### **Archivos creados en esta práctica**

```
fastapi-docker-optimized/
├── app/
│   ├── main.py          # API con endpoints optimizados
│   └── config.py        # Configuración con Pydantic
├── requirements.txt     # Dependencias Python
├── .dockerignore       # Archivos a ignorar en build
├── Dockerfile.basic    # Versión básica
├── Dockerfile.optimized # Versión con Alpine
├── Dockerfile.multistage # Multi-stage build
├── Dockerfile.final    # Con configuración
└── Dockerfile.secure   # Con seguridad mejorada
```

---

## 📈 Comparación de Resultados

### **Tamaños típicos esperados**

| Dockerfile | Tamaño aproximado | Características         |
| ---------- | ----------------- | ----------------------- |
| basic      | ~1GB              | Imagen Python completa  |
| optimized  | ~200MB            | Alpine + optimizaciones |
| multistage | ~150MB            | Sin dependencias build  |
| final      | ~150MB            | + configuración         |
| secure     | ~150MB            | + security hardening    |

### **Mejores prácticas aplicadas**

✅ **Imagen base ligera** (Alpine)  
✅ **Multi-stage builds** para reducir tamaño  
✅ **Usuario no-root** para seguridad  
✅ **Health checks** para monitoring  
✅ **Variables de entorno** para configuración  
✅ **.dockerignore** para optimizar context  
✅ **Capas ordenadas** para cache efectivo

---

## 📝 Próximos Pasos

### **En la siguiente práctica...**

🔜 **Práctica 33: Docker Compose**

- Orquestación de múltiples servicios
- FastAPI + PostgreSQL + Redis
- Networking entre containers
- Volumes persistentes

### **Conceptos para recordar**

- **Multi-stage builds** reducen drásticamente el tamaño
- **Alpine Linux** es ideal para containers productivos
- **Variables de entorno** proporcionan flexibilidad
- **Health checks** son esenciales para producción
- **Seguridad** debe considerarse desde el diseño

---

**🎯 ¡Excelente trabajo!** Has creado Dockerfiles optimizados siguiendo las mejores prácticas de la industria. Tu aplicación FastAPI ya está lista para ser deployada en cualquier entorno que soporte Docker. 🐳✨

---

_Práctica 32 - Semana 9 - Bootcamp FastAPI_  
_Tiempo total: ~90 minutos_
