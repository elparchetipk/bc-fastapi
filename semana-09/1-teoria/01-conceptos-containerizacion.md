# Conceptos Fundamentales de Containerización

## 🎯 Objetivos de Aprendizaje

Al finalizar esta sesión teórica, comprenderás:

- ✅ Qué es la containerización y por qué es importante
- ✅ Diferencias entre containers y máquinas virtuales
- ✅ Conceptos básicos de Docker: imágenes, containers, volumes
- ✅ Ventajas de usar containers en desarrollo y producción
- ✅ Arquitectura y componentes de Docker

---

## 🐳 ¿Qué es Docker y la Containerización?

### **Definición Simple**

**Docker** es una plataforma que permite **empaquetar aplicaciones** junto con todas sus dependencias en **containers** ligeros y portables que pueden ejecutarse en cualquier sistema que tenga Docker instalado.

```
🏠 Tu Aplicación FastAPI
├── 📄 Código Python
├── 📦 Dependencias (requirements.txt)
├── 🗄️ Base de datos
├── ⚙️ Configuración
└── 🌍 Sistema operativo

❌ PROBLEMA: "En mi máquina funciona"
✅ SOLUCIÓN: Container = Todo empaquetado junto
```

### **Analogía del Mundo Real**

Imagina que quieres enviar un regalo:

- **Sin Container**: Envías cada pieza por separado (se pueden perder o dañar)
- **Con Container**: Todo va en una caja segura que se abre igual en cualquier lugar

---

## 🆚 Containers vs Máquinas Virtuales

### **Máquinas Virtuales (VMs)**

```
🖥️ Hardware Físico
├── 💽 Sistema Operativo Host
├── 🔧 Hypervisor (VMware, VirtualBox)
├── 🖥️ VM 1: SO Completo + App 1
├── 🖥️ VM 2: SO Completo + App 2
└── 🖥️ VM 3: SO Completo + App 3
```

**Caracteristicas:**

- ❌ **Pesadas**: Cada VM incluye SO completo
- ❌ **Lentas**: Boot time de minutos
- ❌ **Recursos**: Alta consumo de RAM/CPU
- ✅ **Aislamiento**: Completo entre VMs

### **Containers**

```
🖥️ Hardware Físico
├── 💽 Sistema Operativo Host
├── 🐳 Docker Engine
├── 📦 Container 1: App + Dependencias
├── 📦 Container 2: App + Dependencias
└── 📦 Container 3: App + Dependencias
```

**Caracteristicas:**

- ✅ **Ligeros**: Comparten el kernel del host
- ✅ **Rápidos**: Start time de segundos
- ✅ **Eficientes**: Menor consumo de recursos
- ✅ **Portables**: Misma imagen en cualquier lugar

### **Comparativa Práctica**

| Aspecto              | Máquina Virtual | Container Docker |
| -------------------- | --------------- | ---------------- |
| **Tiempo de inicio** | 2-5 minutos     | 2-5 segundos     |
| **Tamaño**           | 2-20 GB         | 100-500 MB       |
| **Aislamiento**      | Completo        | Proceso-nivel    |
| **Performance**      | Overhead alto   | Near-native      |
| **Portabilidad**     | Limitada        | Excelente        |

---

## 🏗️ Arquitectura de Docker

### **Componentes Principales**

```
🎯 Docker Architecture
├── 👤 Docker Client (CLI)
│   ├── docker build
│   ├── docker run
│   └── docker push
├── 🐳 Docker Daemon
│   ├── Gestión de containers
│   ├── Gestión de imágenes
│   └── Gestión de redes
├── 📚 Docker Registry (Hub)
│   ├── Imágenes públicas
│   ├── Imágenes privadas
│   └── Versioning de imágenes
└── 🏠 Docker Host
    ├── Containers ejecutándose
    ├── Imágenes locales
    └── Volúmenes de datos
```

### **Flujo de Trabajo Típico**

```bash
# 1. Desarrollador crea Dockerfile
FROM python:3.13-slim
COPY . /app
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]

# 2. Build de la imagen
docker build -t mi-fastapi-app .

# 3. Run del container
docker run -p 8000:8000 mi-fastapi-app

# 4. Push al registry (opcional)
docker push mi-usuario/mi-fastapi-app
```

---

## 📦 Conceptos Clave: Imágenes, Containers y Volumes

### **1. Imágenes Docker**

Una **imagen** es un template de solo lectura que contiene:

```
📸 Imagen Docker = Template
├── 🐧 Base OS (Ubuntu, Alpine, etc.)
├── 🐍 Runtime (Python 3.11)
├── 📦 Dependencias (FastAPI, SQLAlchemy)
├── 📄 Código de aplicación
├── ⚙️ Configuración
└── 🚀 Comando de inicio
```

**Características:**

- ✅ **Inmutable**: No cambian una vez creadas
- ✅ **Versionadas**: Tags para diferentes versiones
- ✅ **Layered**: Construcción en capas reutilizables
- ✅ **Shareable**: Se pueden compartir via registries

### **2. Containers**

Un **container** es una instancia ejecutable de una imagen:

```
🏃‍♂️ Container = Imagen + Proceso ejecutándose
├── 📸 Imagen base (read-only)
├── 📝 Layer de escritura (read-write)
├── 🔧 Configuración runtime
├── 🌐 Network interfaces
└── 💾 File system namespace
```

**Características:**

- ✅ **Stateful**: Pueden tener datos temporales
- ✅ **Aislados**: Procesos independientes
- ✅ **Efímeros**: Se pueden crear/destruir fácilmente
- ✅ **Escalables**: Múltiples instances de misma imagen

### **3. Volumes**

Los **volumes** son mecanismos para persistir datos:

```
💾 Volume = Persistencia de datos
├── 🏠 Host filesystem mount
├── 📁 Named volumes (gestionados por Docker)
├── 🔗 Bind mounts (carpetas del host)
└── 💨 tmpfs mounts (memoria RAM)
```

**Casos de uso:**

- ✅ **Base de datos**: Persistir datos entre recreaciones
- ✅ **Logs**: Mantener logs accesibles
- ✅ **Configuración**: Inyectar configs del host
- ✅ **Development**: Hot reload de código

---

## 🌟 Ventajas de Docker para FastAPI

### **1. Desarrollo Local**

```bash
# Sin Docker: Setup complejo
pip install python3.11
pip install postgresql
pip install redis
export DATABASE_URL=...
export REDIS_URL=...
python -m venv env
source env/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload

# Con Docker: Un comando
docker-compose up
```

### **2. Deployment Consistente**

```yaml
# docker-compose.yml
version: '3.8'
services:
  api:
    build: .
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/mydb
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: mydb
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass

  redis:
    image: redis:7-alpine
```

### **3. Escalabilidad Horizontal**

```bash
# Crear múltiples instances de la API
docker-compose up --scale api=3

# Load balancer automático
# Cada request va a instance diferente
```

### **4. Aislamiento y Seguridad**

```dockerfile
# Container ejecuta como usuario no-root
FROM python:3.13-slim
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

# Aplicación aislada del host
# No acceso directo al filesystem del host
# Network aislado por defecto
```

---

## 🔧 Docker en el Contexto del Bootcamp

### **Progresión Natural**

```
Semana 1-3: FastAPI Básico
├── Desarrollo local
├── Dependencies management
└── API functionality

Semana 4-6: Base de Datos y Auth
├── PostgreSQL local
├── JWT authentication
└── CRUD operations

Semana 7-8: Testing y Optimización
├── Automated testing
├── Performance optimization
└── Code quality

Semana 9: 🐳 CONTAINERIZACIÓN
├── Encapsular todo el stack
├── Reproducible environments
├── Production-ready deployment
└── Scalable architecture
```

### **¿Por qué Docker ahora?**

1. **Base sólida**: Ya tienes una aplicación completa funcionando
2. **Complejidad manageable**: Múltiples servicios (API, DB, Redis)
3. **Deployment readiness**: Necesitas portabilidad para producción
4. **Industry standard**: Docker es el estándar en la industria

---

## 🎯 Use Cases Reales en Producción

### **1. Microservicios**

```
🏢 E-commerce Application
├── 🛍️ Product Service (FastAPI + PostgreSQL)
├── 👤 User Service (FastAPI + PostgreSQL)
├── 💳 Payment Service (FastAPI + Stripe)
├── 📧 Email Service (FastAPI + Redis)
└── 🌐 Gateway (Nginx)

# Cada servicio en su propio container
# Deployment independiente
# Scaling independiente
```

### **2. CI/CD Pipelines**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build and push Docker image
        run: |
          docker build -t myapp:${{ github.sha }} .
          docker push myapp:${{ github.sha }}
      - name: Deploy to production
        run: |
          docker service update --image myapp:${{ github.sha }} production-api
```

### **3. Development Team Consistency**

```bash
# Nuevo desarrollador en el equipo
git clone proyecto-repo
cd proyecto-repo
docker-compose up

# ✅ Misma versión de Python
# ✅ Misma versión de PostgreSQL
# ✅ Mismas dependencias
# ✅ Misma configuración
# ❌ ZERO "en mi máquina funciona"
```

---

## 🚀 Preparándose para la Práctica

### **Conceptos para Recordar**

1. **Imagen vs Container**

   - Imagen = Template/Class
   - Container = Instance/Object

2. **Dockerfile**

   - Receta para construir imagen
   - Instrucciones paso a paso

3. **Docker Compose**

   - Orquestación de múltiples containers
   - Definición declarativa de servicios

4. **Volumes**
   - Persistencia de datos
   - Separación de datos y aplicación

### **Comandos Esenciales a Practicar**

```bash
# Gestión básica
docker --version
docker images
docker ps
docker logs <container-id>

# Build y run
docker build -t mi-app .
docker run -p 8000:8000 mi-app

# Docker Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

---

## 📝 Resumen y Próximos Pasos

### **Conceptos Clave Aprendidos**

✅ **Containerización** - Empaquetado de aplicaciones  
✅ **Docker Architecture** - Cliente, daemon, registry  
✅ **Imágenes y Containers** - Templates vs instances  
✅ **Volumes** - Persistencia de datos  
✅ **Ventajas** - Portabilidad, consistency, escalabilidad

### **En la Siguiente Práctica...**

🔜 **Práctica 31: Docker Básico**

- Instalación y verificación de Docker
- Primeros containers con Python
- Exploración de imágenes existentes
- Comandos básicos de gestión

---

**💡 Recuerda**: Docker no es solo una herramienta técnica, es una **filosofía de deployment** que cambió la industria. ¡Vamos a aplicarla! 🐳

---

_Teoría Semana 9 - Bootcamp FastAPI_  
_Tiempo de lectura: ~30 minutos_
