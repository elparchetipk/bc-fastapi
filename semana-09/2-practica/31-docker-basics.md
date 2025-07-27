# Práctica 31: Docker Básico y Setup

⏰ **Tiempo estimado**: 90 minutos  
🎯 **Objetivo**: Instalar Docker y crear tus primeros containers

---

## 📋 Qué vas a lograr

Al final de esta práctica habrás:

- ✅ Instalado y configurado Docker Desktop
- ✅ Ejecutado tu primer container
- ✅ Comprendido comandos básicos de Docker
- ✅ Explorado imágenes públicas de Docker Hub
- ✅ Creado tu primer container con Python

---

## 🛠️ Paso 1: Instalación de Docker Desktop (15 min)

### **Para Windows**

1. **Descargar Docker Desktop**

   ```bash
   # Visitar: https://docs.docker.com/desktop/install/windows-install/
   # Descargar Docker Desktop for Windows
   ```

2. **Instalar y configurar**

   - Ejecutar el instalador descargado
   - Habilitar WSL 2 cuando sea solicitado
   - Reiniciar cuando sea necesario

3. **Verificar instalación**
   ```bash
   docker --version
   docker-compose --version
   ```

### **Para macOS**

1. **Descargar Docker Desktop**

   ```bash
   # Visitar: https://docs.docker.com/desktop/install/mac-install/
   # Escolher versión según tu chip (Intel o Apple Silicon)
   ```

2. **Instalar**

   - Abrir el archivo .dmg descargado
   - Arrastrar Docker a Applications
   - Abrir Docker desde Applications

3. **Verificar**
   ```bash
   docker --version
   docker-compose --version
   ```

### **Para Linux (Ubuntu/Debian)**

```bash
# 1. Actualizar sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar dependencias
sudo apt install apt-transport-https ca-certificates curl gnupg lsb-release

# 3. Añadir clave GPG de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 4. Añadir repositorio
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Instalar Docker
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 6. Añadir usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker

# 7. Verificar
docker --version
docker compose version
```

### **Para RedHat/Fedora/CentOS**

```bash
# 1. Actualizar sistema
sudo dnf update -y

# 2. Instalar dependencias
sudo dnf install -y dnf-plugins-core

# 3. Añadir repositorio oficial de Docker
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# 4. Instalar Docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# 5. Iniciar y habilitar Docker
sudo systemctl start docker
sudo systemctl enable docker

# 6. Añadir usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker

# 7. Verificar
docker --version
docker compose version
```

---

## 🚀 Paso 2: Primer Container - Hello World (10 min)

### **Test Básico de Docker**

```bash
# 1. Ejecutar el container hello-world
docker run hello-world

# 🎯 Esto debería mostrar:
# Hello from Docker!
# This message shows that your installation appears to be working correctly.
```

### **¿Qué pasó internamente?**

```bash
# 1. Docker buscó la imagen 'hello-world' localmente
# 2. No la encontró, así que la descargó de Docker Hub
# 3. Creó un container desde esa imagen
# 4. Ejecutó el container (mostró el mensaje)
# 5. El container se detuvo automáticamente
```

### **Verificar estado**

```bash
# Ver containers ejecutándose actualmente
docker ps

# Ver todos los containers (incluyendo parados)
docker ps -a

# Ver imágenes descargadas
docker images
```

---

## 🐍 Paso 3: Container con Python (20 min)

### **Ejecutar Python interactivo**

```bash
# 1. Ejecutar Python 3.13 en modo interactivo
docker run -it python:3.13

# Esto abre un prompt de Python dentro del container
>>> print("¡Hola desde Docker!")
>>> import sys
>>> print(f"Python version: {sys.version}")
>>> exit()
```

### **Ejecutar script Python**

```bash
# 1. Crear un archivo test.py en tu máquina local
cat > test_docker.py << 'EOF'
#!/usr/bin/env python3

print("🐳 ¡Hola desde Python en Docker!")
print("📦 Este script se ejecuta dentro de un container")

import platform
import os

print(f"🐧 OS: {platform.system()}")
print(f"🏗️ Arquitectura: {platform.machine()}")
print(f"🐍 Python: {platform.python_version()}")
print(f"📁 Working directory: {os.getcwd()}")
EOF

# 2. Ejecutar el script dentro de un container
docker run --rm -v $(pwd):/app -w /app python:3.13 python test_docker.py
```

### **Explicación del comando**

```bash
docker run \
  --rm \                    # Eliminar container cuando termine
  -v $(pwd):/app \         # Montar directorio actual en /app del container
  -w /app \                # Directorio de trabajo dentro del container
  python:3.13 \            # Imagen a usar
  python test_docker.py    # Comando a ejecutar
```

---

## 📊 Paso 4: Explorando Docker Hub (15 min)

### **Buscar imágenes populares**

```bash
# 1. Buscar imágenes de Python
docker search python

# 2. Buscar imágenes de PostgreSQL
docker search postgres

# 3. Buscar imágenes de Redis
docker search redis
```

### **Descargar imágenes específicas**

```bash
# 1. Descargar PostgreSQL oficial
docker pull postgres:15

# 2. Descargar Redis Alpine (imagen ligera)
docker pull redis:7-alpine

# 3. Descargar Nginx Alpine
docker pull nginx:alpine

# 4. Descargar Python Alpine (más ligero)
docker pull python:3.13-alpine

# 5. Ver todas las imágenes descargadas
docker images
```

### **🏆 Mejores Prácticas para Imágenes**

#### **✅ Usar Imágenes Oficiales y Verificadas**

```bash
# ✅ BUENO: Imágenes oficiales de Docker Hub
docker pull python:3.13          # Imagen oficial de Python
docker pull postgres:15          # Imagen oficial de PostgreSQL
docker pull redis:7              # Imagen oficial de Redis
docker pull nginx:alpine         # Imagen oficial de Nginx

# ✅ BUENO: Imágenes verificadas
docker search --filter is-official=true python
docker search --filter is-automated=true redis
```

#### **🪶 Preferir Imágenes Alpine (Recomendado)**

Las imágenes Alpine son **significativamente más ligeras** y **más seguras**:

```bash
# 📊 Comparación de tamaños:
# python:3.13        -> ~900MB
# python:3.13-slim   -> ~130MB
# python:3.13-alpine -> ~50MB   🏆 MÁS LIGERO

# ✅ Imágenes Alpine recomendadas:
docker pull python:3.13-alpine    # Python ligero
docker pull node:18-alpine        # Node.js ligero
docker pull nginx:alpine          # Nginx ligero
docker pull redis:7-alpine        # Redis ligero
docker pull postgres:15-alpine    # PostgreSQL ligero
```

#### **🚫 Evitar Imágenes No Oficiales**

```bash
# ❌ MALO: Imágenes de terceros sin verificar
docker pull randomuser/python-app     # No oficial, riesgo de seguridad
docker pull unknown/postgres-custom   # Sin verificación

# ✅ BUENO: Verificar antes de usar
docker search python --filter is-official=true
docker search python --filter stars=3000
```

#### **🔍 Verificar Información de Imágenes**

```bash
# Ver información detallada
docker inspect python:3.13-alpine

# Ver historial de capas
docker history python:3.13-alpine

# Comparar tamaños
docker images | grep python
```

### **Información de imágenes**

```bash
# Ver detalles de una imagen
docker inspect python:3.13

# Ver capas de la imagen
docker history python:3.13

# Ver tamaño de las imágenes
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

---

## 🗄️ Paso 5: Containers con Servicios (20 min)

### **PostgreSQL Container**

```bash
# 1. Ejecutar PostgreSQL en background
docker run -d \
  --name postgres-test \
  -e POSTGRES_DB=testdb \
  -e POSTGRES_USER=testuser \
  -e POSTGRES_PASSWORD=testpass \
  -p 5432:5432 \
  postgres:15

# 2. Verificar que está ejecutándose
docker ps

# 3. Ver logs del container
docker logs postgres-test

# 4. Conectar a la base de datos
docker exec -it postgres-test psql -U testuser -d testdb

# Dentro del prompt SQL:
# \l                    # Listar bases de datos
# \dt                   # Listar tablas
# \q                    # Salir
```

### **Redis Container**

```bash
# 1. Ejecutar Redis Alpine (imagen ligera)
docker run -d \
  --name redis-test \
  -p 6379:6379 \
  redis:7-alpine

# 2. Verificar status
docker ps

# 3. Conectar a Redis
docker exec -it redis-test redis-cli

# Dentro del prompt Redis:
# set test "¡Hola Redis!"
# get test
# keys *
# quit
```

### **Web Server Simple**

```bash
# 1. Ejecutar Nginx
docker run -d \
  --name nginx-test \
  -p 8080:80 \
  nginx:alpine

# 2. Verificar en navegador
# Abrir: http://localhost:8080
# Deberías ver la página de bienvenida de Nginx

# 3. Ver logs de acceso
docker logs nginx-test
```

---

## 🔧 Paso 6: Gestión de Containers (10 min)

### **Comandos de gestión básicos**

```bash
# 1. Listar containers ejecutándose
docker ps

# 2. Listar todos los containers
docker ps -a

# 3. Detener containers
docker stop postgres-test redis-test nginx-test

# 4. Iniciar containers detenidos
docker start postgres-test

# 5. Reiniciar containers
docker restart postgres-test

# 6. Eliminar containers
docker rm postgres-test redis-test nginx-test

# 7. Forzar eliminación de container ejecutándose
docker rm -f nginx-test
```

### **Limpieza del sistema**

```bash
# 1. Eliminar containers parados
docker container prune

# 2. Eliminar imágenes no usadas
docker image prune

# 3. Limpieza completa (¡cuidado!)
docker system prune -a

# 4. Ver uso de espacio
docker system df
```

---

## 🎯 Ejercicio Práctico: Mi Primera API en Container (15 min)

### **Crear API FastAPI simple**

```bash
# 1. Crear directorio para el ejercicio
mkdir docker-fastapi-test
cd docker-fastapi-test

# 2. Crear archivo de dependencias
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
EOF

# 3. Crear API simple
cat > main.py << 'EOF'
from fastapi import FastAPI
import platform
import os

app = FastAPI(title="API en Docker", version="1.0.0")

@app.get("/")
async def root():
    return {
        "message": "¡Hola desde FastAPI en Docker!",
        "platform": platform.platform(),
        "python_version": platform.python_version(),
        "hostname": os.environ.get("HOSTNAME", "unknown")
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "fastapi-docker"}
EOF
```

### **Ejecutar API en Container**

```bash
# 1. Ejecutar con bind mount (development)
docker run --rm \
  -p 8000:8000 \
  -v $(pwd):/app \
  -w /app \
  python:3.13 \
  bash -c "pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port 8000"

# 2. Probar la API
# Abrir en navegador: http://localhost:8000
# Ver documentación: http://localhost:8000/docs

# 3. Probar con curl
curl http://localhost:8000/
curl http://localhost:8000/health
```

> **💡 Tip**: Para producción, considera usar `python:3.13-alpine` en lugar de `python:3.13` para una imagen más ligera y segura.

---

## 🔍 Paso 7: Inspección y Debugging (10 min)

### **Inspeccionar containers**

```bash
# 1. Ejecutar un container long-running para práctica
docker run -d --name debug-test python:3.13 python -c "import time; [time.sleep(1) for _ in range(3600)]"

# 2. Inspeccionar el container
docker inspect debug-test

# 3. Ver procesos ejecutándose
docker top debug-test

# 4. Ver estadísticas de recursos
docker stats debug-test

# 5. Acceder al filesystem del container
docker exec -it debug-test bash

# Dentro del container:
# ls -la
# cat /etc/os-release
# ps aux
# exit

# 6. Limpiar
docker rm -f debug-test
```

### **Logs y troubleshooting**

```bash
# 1. Ver logs en tiempo real
docker logs -f container-name

# 2. Ver últimas 20 líneas de logs
docker logs --tail 20 container-name

# 3. Ver logs con timestamps
docker logs -t container-name

# 4. Ver uso de recursos
docker stats

# 5. Ver información del sistema Docker
docker info
```

---

## 🏆 Verificación de Completitud

### **Checklist de validación**

Ejecuta estos comandos para verificar que todo está funcionando:

```bash
# ✅ 1. Docker instalado y funcionando
docker --version && echo "✅ Docker CLI OK"

# ✅ 2. Docker Compose disponible
docker-compose --version || docker compose version && echo "✅ Compose OK"

# ✅ 3. Poder ejecutar containers
docker run --rm hello-world && echo "✅ Container execution OK"

# ✅ 4. Bind mounts funcionando
echo "test" > test.txt && docker run --rm -v $(pwd):/app alpine cat /app/test.txt && rm test.txt && echo "✅ Volumes OK"

# ✅ 5. Port mapping funcionando
docker run -d --name test-nginx -p 8080:80 nginx:alpine
curl -s http://localhost:8080 >/dev/null && echo "✅ Port mapping OK"
docker rm -f test-nginx

# ✅ 6. Network access
docker run --rm alpine ping -c 1 google.com >/dev/null && echo "✅ Network OK"
```

### **Comandos esenciales aprendidos**

```bash
# Gestión básica
docker run          # Ejecutar container
docker ps           # Listar containers
docker images       # Listar imágenes
docker logs         # Ver logs
docker exec         # Ejecutar comando en container

# Gestión de lifecycle
docker start        # Iniciar container
docker stop         # Detener container
docker restart      # Reiniciar container
docker rm           # Eliminar container

# Limpieza
docker system prune # Limpiar recursos no usados
docker container prune  # Limpiar containers parados
docker image prune  # Limpiar imágenes no usadas
```

---

## 🏆 Mejores Prácticas - Resumen

### **🪶 ¿Por qué Alpine?**

**Ventajas de las imágenes Alpine:**

1. **Tamaño Reducido**: 90% menos espacio (50MB vs 900MB)
2. **Seguridad**: Menor superficie de ataque
3. **Velocidad**: Descarga e inicio más rápidos
4. **Eficiencia**: Menos recursos del sistema

```bash
# 📊 Comparación real:
docker images | grep python
# python:3.13        -> 920MB
# python:3.13-slim   -> 131MB
# python:3.13-alpine -> 51MB   🏆

# 🚀 Tiempo de descarga Alpine: 3x más rápido
# 💾 Espacio en disco: 18x menos
# 🛡️ Vulnerabilidades: 5x menos
```

### **✅ Imágenes Oficiales Recomendadas**

```bash
# Lenguajes de programación
python:3.13-alpine      # Python ligero
node:18-alpine          # Node.js ligero
golang:1.21-alpine      # Go ligero

# Bases de datos
postgres:15-alpine      # PostgreSQL ligero
mysql:8.0               # MySQL oficial
redis:7-alpine          # Redis ligero
mongo:6.0               # MongoDB oficial

# Servidores web
nginx:alpine            # Nginx ligero
httpd:alpine            # Apache ligero
caddy:alpine            # Caddy ligero

# Herramientas
alpine:latest           # Base Alpine pura
busybox:latest          # Herramientas básicas
```

### **🔒 Validación de Imágenes**

```bash
# ✅ Verificar que es imagen oficial
docker search python --filter is-official=true

# ✅ Verificar popularidad (stars)
docker search redis --filter stars=1000

# ✅ Ver información de seguridad
docker scan python:3.13-alpine  # Si tienes Docker Pro

# ✅ Verificar en Docker Hub
# Buscar el badge "Official Image" o "Verified Publisher"
```

### **📋 Checklist de Selección de Imágenes**

- [ ] ✅ **¿Es imagen oficial?** (Docker Official Images)
- [ ] ✅ **¿Está actualizada?** (última versión estable)
- [ ] ✅ **¿Hay versión Alpine?** (usar si es posible)
- [ ] ✅ **¿Tiene buenas calificaciones?** (>1000 stars)
- [ ] ✅ **¿Es de un publisher verificado?** (empresa conocida)
- [ ] ✅ **¿Tiene documentación?** (README completo)
- [ ] ❌ **¿Evitar imágenes `:latest`?** (usar tags específicos)
- [ ] ❌ **¿Evitar imágenes de usuarios desconocidos?**

---

## 📝 Reflexión y Próximos Pasos

### **¿Qué hemos logrado?**

✅ **Ambiente de Docker funcionando** - Setup completo  
✅ **Comprensión básica** - Containers, imágenes, commands  
✅ **Experiencia práctica** - Ejecutar servicios reales  
✅ **Debugging skills** - Logs, inspect, exec  
✅ **Workflow básico** - Development con containers

### **Próxima práctica: Dockerfile para FastAPI**

En la siguiente práctica aprenderás:

- Crear tu propio Dockerfile
- Optimizar imágenes para FastAPI
- Multi-stage builds
- Variables de entorno y configuración

---

## 🆘 Troubleshooting Común

### **Docker no inicia**

```bash
# Windows: Verificar que WSL 2 está habilitado
wsl --status

# Linux: Verificar que el servicio está ejecutándose
sudo systemctl status docker
sudo systemctl start docker

# macOS: Reiniciar Docker Desktop desde la aplicación
```

### **Permission denied (Linux)**

```bash
# Añadir usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker

# O ejecutar con sudo temporalmente
sudo docker run hello-world
```

### **Puerto ya en uso**

```bash
# Encontrar qué proceso usa el puerto
lsof -i :8000

# O cambiar el puerto
docker run -p 8001:8000 mi-app
```

### **Container no se conecta a internet**

```bash
# Verificar DNS del container
docker run --rm alpine nslookup google.com

# Verificar configuración de red
docker network ls
docker network inspect bridge
```

---

**🎯 ¡Felicitaciones!** Has completado tu introducción a Docker. En la siguiente práctica crearemos un Dockerfile optimizado para nuestra aplicación FastAPI. 🐳

---

_Práctica 31 - Semana 9 - Bootcamp FastAPI_  
_Tiempo total: ~90 minutos_
