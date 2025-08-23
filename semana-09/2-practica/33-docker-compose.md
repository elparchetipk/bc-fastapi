# Práctica 33: Docker Compose Esencial

⏰ **Tiempo estimado**: 75 minutos _(optimizado)_  
🎯 **Objetivo**: Orquestar servicios esenciales con Docker Compose para FastAPI

---

## 📋 Qué vas a lograr

Al final de esta práctica habrás:

- ✅ Configurado Docker Compose esencial para FastAPI stack
- ✅ Orquestado FastAPI + PostgreSQL + Redis
- ✅ Implementado networking básico automático
- ✅ Configurado volumes esenciales para persistencia
- ✅ Aplicado variables de entorno básicas

**OPTIMIZADO PARA 75MIN:**
- ✅ Enfoque en configuración funcional
- ✅ Setup más directo y práctico
- ⬇️ Menos configuraciones complejas
- ⬇️ Troubleshooting básico incluido

---

## 🏗️ Paso 1: Setup Rápido del Proyecto (10 min)

### **Estructura simplificada**

```bash
# 1. Crear directorio principal
mkdir fastapi-compose-stack
cd fastapi-compose-stack

# 2. Crear estructura esencial
mkdir -p {app,config}

# 3. Verificar estructura
ls -la
```

### **FastAPI app simplificada para testing**

```python
# app/main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from datetime import datetime
import os
import redis
import json

# Configuración de base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/fastapi_db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Redis setup
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# Modelos SQLAlchemy
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Modelos Pydantic
class UserCreate(BaseModel):
    username: str
    email: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# FastAPI app
app = FastAPI(
    title="FastAPI Compose Stack",
    description="API con PostgreSQL y Redis",
    version="1.0.0"
)

# Dependency para obtener sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints
@app.get("/")
async def root():
    return {
        "message": "🐳 FastAPI con Docker Compose",
        "services": ["PostgreSQL", "Redis"],
        "endpoints": ["/users", "/health", "/cache"]
    }

@app.get("/health")
async def health_check():
    # Verificar conexión a PostgreSQL
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "healthy"
    except Exception as e:
        db_status = f"error: {str(e)}"

    # Verificar conexión a Redis
    try:
        redis_client.ping()
        redis_status = "healthy"
    except Exception as e:
        redis_status = f"error: {str(e)}"

    return {
        "status": "healthy",
        "database": db_status,
        "cache": redis_status,
        "timestamp": datetime.utcnow()
    }

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si usuario ya existe
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Crear nuevo usuario
    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Cache en Redis
    cache_key = f"user:{db_user.id}"
    user_data = {
        "id": db_user.id,
        "username": db_user.username,
        "email": db_user.email,
        "is_active": db_user.is_active,
        "created_at": db_user.created_at.isoformat()
    }
    redis_client.setex(cache_key, 300, json.dumps(user_data))  # 5 min TTL

    return db_user

@app.get("/users", response_model=list[UserResponse])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    # Intentar obtener desde cache primero
    cache_key = f"user:{user_id}"
    cached_user = redis_client.get(cache_key)

    if cached_user:
        user_data = json.loads(cached_user)
        user_data['created_at'] = datetime.fromisoformat(user_data['created_at'])
        return UserResponse(**user_data)

    # Si no está en cache, obtener de DB
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    return db_user

@app.get("/cache/stats")
async def cache_stats():
    """Estadísticas del cache Redis"""
    try:
        info = redis_client.info()
        return {
            "connected_clients": info.get("connected_clients"),
            "used_memory_human": info.get("used_memory_human"),
            "total_commands_processed": info.get("total_commands_processed"),
            "keyspace": info.get("db0", {})
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

@app.delete("/cache/clear")
async def clear_cache():
    """Limpiar todo el cache"""
    try:
        redis_client.flushdb()
        return {"message": "Cache cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Redis error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### **Requirements actualizado**

```text
# requirements.txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
redis==5.0.1
pydantic==2.5.0
```

### **Dockerfile para la aplicación**

```dockerfile
# Dockerfile
FROM python:3.13-alpine AS builder

RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev

WORKDIR /install
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.13-alpine AS production

RUN apk add --no-cache curl postgresql-libs && \
    addgroup -g 1001 -S appgroup && \
    adduser -u 1001 -S appuser -G appgroup

COPY --from=builder /install /usr/local

WORKDIR /app
COPY app/ ./app/

RUN chown -R appuser:appgroup /app
USER appuser

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 🐳 Paso 2: Docker Compose Básico (20 min)

### **Primera versión de docker-compose.yml**

```yaml
# docker-compose.yml
version: '3.8'

services:
  # Aplicación FastAPI
  api:
    build: .
    container_name: fastapi-app
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=postgresql://fastapi_user:fastapi_password@db:5432/fastapi_db
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    restart: unless-stopped

  # Base de datos PostgreSQL
  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_DB=fastapi_db
      - POSTGRES_USER=fastapi_user
      - POSTGRES_PASSWORD=fastapi_password
    ports:
      - '5432:5432'
    restart: unless-stopped

  # Cache Redis
  cache:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - '6379:6379'
    restart: unless-stopped
```

### **Primera ejecución**

```bash
# 1. Build y levantar servicios
docker-compose up --build

# 2. En otra terminal, probar la aplicación
curl http://localhost:8000/
curl http://localhost:8000/health

# 3. Crear un usuario
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "docker_user", "email": "user@example.com"}'

# 4. Obtener usuarios
curl http://localhost:8000/users

# 5. Ver logs de todos los servicios
docker-compose logs

# 6. Detener servicios
docker-compose down
```

---

## 💾 Paso 3: Volumes Persistentes (20 min)

### **Docker Compose con volumes**

```yaml
# docker-compose.volumes.yml
version: '3.8'

services:
  api:
    build: .
    container_name: fastapi-app
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=postgresql://fastapi_user:fastapi_password@db:5432/fastapi_db
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    restart: unless-stopped
    volumes:
      # Volume para logs de aplicación
      - ./logs:/app/logs
      # Bind mount para development (opcional)
      - ./app:/app/app:ro

  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_DB=fastapi_db
      - POSTGRES_USER=fastapi_user
      - POSTGRES_PASSWORD=fastapi_password
    ports:
      - '5432:5432'
    volumes:
      # Volume persistente para datos de PostgreSQL
      - postgres_data:/var/lib/postgresql/data
      # Script de inicialización
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    restart: unless-stopped

  cache:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - '6379:6379'
    volumes:
      # Volume persistente para datos de Redis
      - redis_data:/data
      # Configuración personalizada de Redis
      - ./config/redis.conf:/usr/local/etc/redis/redis.conf:ro
    command: redis-server /usr/local/etc/redis/redis.conf
    restart: unless-stopped

# Volumes nombrados
volumes:
  postgres_data:
    driver: local
  redis_data:
    driver: local
```

### **Scripts de inicialización**

```sql
-- database/init.sql
-- Script de inicialización de la base de datos

-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Crear índices adicionales para performance
-- (Se ejecutará después de que SQLAlchemy cree las tablas)

-- Función para logs de auditoría
CREATE OR REPLACE FUNCTION log_user_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO user_audit_log (user_id, action, timestamp)
        VALUES (NEW.id, 'CREATED', NOW());
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO user_audit_log (user_id, action, timestamp)
        VALUES (NEW.id, 'UPDATED', NOW());
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO user_audit_log (user_id, action, timestamp)
        VALUES (OLD.id, 'DELETED', NOW());
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Crear tabla de logs de auditoría
CREATE TABLE IF NOT EXISTS user_audit_log (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(50),
    timestamp TIMESTAMP DEFAULT NOW()
);
```

### **Configuración de Redis**

```conf
# config/redis.conf
# Configuración básica de Redis para producción

# Network
bind 0.0.0.0
port 6379
timeout 0
tcp-keepalive 300

# Memory
maxmemory 256mb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

# Logging
loglevel notice
logfile ""

# Security
# requirepass your_redis_password  # Descomentar en producción

# Performance
tcp-backlog 511
databases 16
```

### **Test con volumes persistentes**

```bash
# 1. Crear directorios necesarios
mkdir -p logs database config

# 2. Copiar archivos de configuración
# (los archivos init.sql y redis.conf ya están creados arriba)

# 3. Levantar con volumes
docker-compose -f docker-compose.volumes.yml up --build -d

# 4. Verificar volumes creados
docker volume ls

# 5. Crear algunos datos de prueba
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "persistent_user", "email": "persistent@example.com"}'

# 6. Verificar datos
curl http://localhost:8000/users

# 7. Detener servicios pero mantener volumes
docker-compose -f docker-compose.volumes.yml down

# 8. Levantar de nuevo y verificar que los datos persisten
docker-compose -f docker-compose.volumes.yml up -d
curl http://localhost:8000/users

# Los datos deben seguir ahí
```

---

## 🌐 Paso 4: Networking Avanzado (15 min)

### **Docker Compose con networks personalizados**

```yaml
# docker-compose.networks.yml
version: '3.8'

services:
  api:
    build: .
    container_name: fastapi-app
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=postgresql://fastapi_user:fastapi_password@db:5432/fastapi_db
      - REDIS_URL=redis://cache:6379
    depends_on:
      - db
      - cache
    networks:
      - backend
      - frontend
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_DB=fastapi_db
      - POSTGRES_USER=fastapi_user
      - POSTGRES_PASSWORD=fastapi_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - backend
    restart: unless-stopped
    # No exponemos puerto 5432 al host (más seguro)

  cache:
    image: redis:7-alpine
    container_name: redis-cache
    volumes:
      - redis_data:/data
    networks:
      - backend
    restart: unless-stopped
    # No exponemos puerto 6379 al host (más seguro)

  # Proxy reverso (opcional pero recomendado)
  proxy:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - '80:80'
      - '443:443'
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
    networks:
      - frontend
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:

networks:
  # Red para comunicación entre servicios backend
  backend:
    driver: bridge
    internal: true # Sin acceso a internet

  # Red para servicios expuestos
  frontend:
    driver: bridge
```

### **Configuración de Nginx**

```nginx
# config/nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream fastapi_backend {
        server api:8000;
    }

    server {
        listen 80;
        server_name localhost;

        # Proxy to FastAPI
        location / {
            proxy_pass http://fastapi_backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check endpoint
        location /nginx-health {
            access_log off;
            return 200 "healthy\n";
            add_header Content-Type text/plain;
        }
    }
}
```

### **Test de networking**

```bash
# 1. Crear configuración de nginx
mkdir -p config

# 2. Levantar con networks
docker-compose -f docker-compose.networks.yml up --build -d

# 3. Verificar networks creados
docker network ls | grep fastapi

# 4. Inspeccionar la red backend
docker network inspect fastapi-compose-stack_backend

# 5. Probar conectividad interna
docker exec fastapi-app ping -c 3 db
docker exec fastapi-app ping -c 3 cache

# 6. Probar a través del proxy
curl http://localhost/health

# 7. Verificar que servicios backend no son accesibles directamente desde host
# Esto debe fallar:
curl http://localhost:5432 || echo "✅ PostgreSQL no accesible desde host"
curl http://localhost:6379 || echo "✅ Redis no accesible desde host"

# 8. Ver logs de nginx
docker logs nginx-proxy
```

---

## ⚙️ Paso 5: Variables de Entorno y Configuración (10 min)

### **Archivo .env para configuración**

```bash
# .env
# Variables de entorno para development

# Database
POSTGRES_DB=fastapi_db
POSTGRES_USER=fastapi_user
POSTGRES_PASSWORD=your_secure_password_here

# Redis
REDIS_PASSWORD=your_redis_password_here

# Application
ENVIRONMENT=development
DEBUG=true
SECRET_KEY=your-secret-key-change-in-production

# External ports
API_PORT=8000
POSTGRES_PORT=5432
REDIS_PORT=6379
NGINX_PORT=80
```

### **Docker Compose con archivo .env**

```yaml
# docker-compose.env.yml
version: '3.8'

services:
  api:
    build: .
    container_name: fastapi-app
    ports:
      - '${API_PORT}:8000'
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://cache:6379
      - ENVIRONMENT=${ENVIRONMENT}
      - DEBUG=${DEBUG}
      - SECRET_KEY=${SECRET_KEY}
    env_file:
      - .env
    depends_on:
      - db
      - cache
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    ports:
      - '${POSTGRES_PORT}:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  cache:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - '${REDIS_PORT}:6379'
    volumes:
      - redis_data:/data
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
```

### **Test con variables de entorno**

```bash
# 1. Verificar que el archivo .env existe
cat .env

# 2. Levantar con variables de entorno
docker-compose -f docker-compose.env.yml up --build -d

# 3. Verificar que las variables se aplicaron
docker exec fastapi-app env | grep -E "(DATABASE_URL|ENVIRONMENT|DEBUG)"

# 4. Probar funcionalidad
curl http://localhost:8000/health

# 5. Para producción, crear .env.production
cat > .env.production << 'EOF'
POSTGRES_DB=fastapi_prod
POSTGRES_USER=fastapi_prod_user
POSTGRES_PASSWORD=super_secure_production_password
REDIS_PASSWORD=secure_redis_password
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=production-secret-key-super-secure
API_PORT=8000
POSTGRES_PORT=5432
REDIS_PORT=6379
NGINX_PORT=80
EOF

# 6. Test con configuración de producción
docker-compose -f docker-compose.env.yml --env-file .env.production up -d
```

---

## 🔧 Paso 6: Docker Compose Final Optimizado (10 min)

### **Versión final con todas las mejores prácticas**

```yaml
# docker-compose.final.yml
version: '3.8'

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: fastapi-app
    ports:
      - '${API_PORT:-8000}:8000'
    environment:
      - DATABASE_URL=postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}
      - REDIS_URL=redis://cache:6379
      - ENVIRONMENT=${ENVIRONMENT:-production}
      - DEBUG=${DEBUG:-false}
      - SECRET_KEY=${SECRET_KEY}
    env_file:
      - .env
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_started
    volumes:
      - ./logs:/app/logs
    networks:
      - backend
      - frontend
    restart: unless-stopped
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8000/health']
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    restart: unless-stopped
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}']
      interval: 10s
      timeout: 5s
      retries: 5

  cache:
    image: redis:7-alpine
    container_name: redis-cache
    volumes:
      - redis_data:/data
      - ./config/redis.conf:/usr/local/etc/redis/redis.conf:ro
    networks:
      - backend
    restart: unless-stopped
    command: redis-server /usr/local/etc/redis/redis.conf
    healthcheck:
      test: ['CMD', 'redis-cli', 'ping']
      interval: 10s
      timeout: 3s
      retries: 3

  proxy:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - '${NGINX_PORT:-80}:80'
    volumes:
      - ./config/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - api
    networks:
      - frontend
    restart: unless-stopped
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

networks:
  backend:
    driver: bridge
    internal: true
  frontend:
    driver: bridge
```

### **Comandos de gestión**

```bash
# 1. Script para development
cat > dev.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting development environment..."
docker-compose -f docker-compose.final.yml --env-file .env up --build -d
echo "✅ Services started!"
echo "📊 API: http://localhost:8000"
echo "📊 Docs: http://localhost:8000/docs"
echo "🔍 Health: http://localhost:8000/health"
EOF

chmod +x dev.sh

# 2. Script para production
cat > prod.sh << 'EOF'
#!/bin/bash
echo "🚀 Starting production environment..."
docker-compose -f docker-compose.final.yml --env-file .env.production up -d
echo "✅ Production services started!"
EOF

chmod +x prod.sh

# 3. Script para logs
cat > logs.sh << 'EOF'
#!/bin/bash
docker-compose -f docker-compose.final.yml logs -f $1
EOF

chmod +x logs.sh

# 4. Test final
./dev.sh

# 5. Verificar que todos los servicios están healthy
docker-compose -f docker-compose.final.yml ps

# 6. Verificar health checks
watch -n 2 "docker-compose -f docker-compose.final.yml ps"
```

---

## 🏆 Verificación y Pruebas Finales

### **Test completo del stack**

```bash
# 1. Verificar que todos los servicios están up y healthy
docker-compose -f docker-compose.final.yml ps

# 2. Test de conectividad completa
echo "=== TESTING COMPLETE STACK ==="

# API health
curl -s http://localhost:8000/health | jq '.'

# Crear usuario (test PostgreSQL)
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "compose_test", "email": "compose@test.com"}' | jq '.'

# Obtener usuario (test cache Redis)
USER_ID=$(curl -s http://localhost:8000/users | jq '.[0].id')
curl -s "http://localhost:8000/users/$USER_ID" | jq '.'

# Test cache stats
curl -s http://localhost:8000/cache/stats | jq '.'

# Test a través de Nginx proxy
curl -s http://localhost/health | jq '.'

echo "✅ All tests passed!"
```

### **Verificación de volúmenes y persistencia**

```bash
# 1. Verificar volumes
docker volume ls | grep fastapi

# 2. Ver contenido del volume de PostgreSQL
docker exec postgres-db ls -la /var/lib/postgresql/data

# 3. Ver contenido del volume de Redis
docker exec redis-cache ls -la /data

# 4. Test de persistencia
echo "=== PERSISTENCE TEST ==="

# Crear dato de prueba
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"username": "persistence_test", "email": "persist@test.com"}'

# Parar servicios
docker-compose -f docker-compose.final.yml down

# Reiniciar servicios
docker-compose -f docker-compose.final.yml up -d

# Esperar que inicien
sleep 10

# Verificar que el dato persiste
curl -s http://localhost:8000/users | grep "persistence_test" && echo "✅ Persistence working!"
```

---

## 📊 Análisis de Performance y Recursos

### **Monitoreo de recursos**

```bash
# 1. Ver uso de recursos por container
docker stats

# 2. Ver información detallada de networks
docker network ls
docker network inspect fastapi-compose-stack_backend
docker network inspect fastapi-compose-stack_frontend

# 3. Ver información de volumes
docker volume inspect fastapi-compose-stack_postgres_data
docker volume inspect fastapi-compose-stack_redis_data

# 4. Análisis de logs
docker-compose -f docker-compose.final.yml logs --tail=50 api
docker-compose -f docker-compose.final.yml logs --tail=50 db
docker-compose -f docker-compose.final.yml logs --tail=50 cache
```

---

## 📝 Archivos Finales Creados

```
fastapi-compose-stack/
├── app/
│   └── main.py              # FastAPI app con PostgreSQL + Redis
├── database/
│   └── init.sql             # Script de inicialización DB
├── config/
│   ├── redis.conf           # Configuración Redis
│   └── nginx.conf           # Configuración Nginx
├── logs/                    # Directorio para logs
├── scripts/                 # Scripts de gestión
├── requirements.txt         # Dependencias Python
├── Dockerfile              # Imagen optimizada de FastAPI
├── .dockerignore           # Archivos a ignorar
├── docker-compose.yml      # Versión básica
├── docker-compose.volumes.yml    # Con volumes
├── docker-compose.networks.yml   # Con networks
├── docker-compose.env.yml        # Con variables de entorno
├── docker-compose.final.yml      # Versión final optimizada
├── .env                    # Variables development
├── .env.production         # Variables production
├── dev.sh                  # Script development
├── prod.sh                 # Script production
└── logs.sh                 # Script para logs
```

---

## 🎯 Próximos Pasos

### **En la siguiente práctica...**

🔜 **Práctica 34: Production Deployment**

- Optimización para producción
- Seguridad en containers
- CI/CD básico con Docker
- Deployment en cloud

### **Conceptos clave aprendidos**

✅ **Orquestación multi-servicio** con Docker Compose  
✅ **Networking** entre containers  
✅ **Volumes persistentes** para datos  
✅ **Variables de entorno** para configuración  
✅ **Health checks** para monitoring  
✅ **Proxy reverso** con Nginx

---

**🎯 ¡Excelente trabajo!** Has creado un stack completo con FastAPI, PostgreSQL y Redis, completamente orquestado y listo para cualquier entorno. Tu aplicación ahora es verdaderamente portable y escalable. 🐳🎉

---

_Práctica 33 - Semana 9 - Bootcamp FastAPI_  
_Tiempo total: ~90 minutos_
