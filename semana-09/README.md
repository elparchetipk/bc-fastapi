# Semana 9: Containerización con Docker - Optimizada

⏰ **DURACIÓN TOTAL: 6 HORAS EXACTAS**  
📚 **NIVEL: Intermedio-Avanzado (construye sobre Semanas 1-8)**

## 🚨 **IMPORTANTE: Preparando para Producción**

Esta semana está diseñada para estudiantes que **ya tienen una API completa con autenticación, testing y optimización** (Semanas 1-8). Implementaremos containerización con Docker para preparar la aplicación para deployment en cualquier entorno.

- ✅ **Completamente realizable en 5h 30min efectivos**
- ✅ **Enfoque práctico en containerización esencial**
- ✅ **Preparación sólida para deployment profesional**

## 🎯 Objetivos de la Semana AJUSTADOS (Docker-Focused)

Al finalizar esta semana de 5h 30min efectivos (incluye break de 30 min), los estudiantes:

1. ✅ **Dominarán conceptos básicos** de containerización con Docker
2. ✅ **Crearán Dockerfile optimizado** para aplicaciones FastAPI
3. ✅ **Configurarán Docker Compose esencial** para multi-servicios
4. ✅ **Aplicarán configuración básica** para producción
5. ✅ **Prepararán deployment** con documentation completa

### ❌ **Lo que NO se espera dominar esta semana**

- Orquestación avanzada con Kubernetes
- Docker Swarm y clustering
- Optimización avanzada de imágenes
- CI/CD completo con Docker
- Seguridad avanzada en containers

## ⏱️ Distribución de Tiempo AJUSTADA (5h 30min efectivos)

| Bloque | Actividad                 | Tiempo | Descripción                                    |
| ------ | ------------------------- | ------ | ---------------------------------------------- |
| **1**  | Docker Básico y Conceptos | 90 min | Instalación, conceptos, primeros containers    |
| **2**  | Dockerfile para FastAPI   | 90 min | Optimización de imagen, multi-stage builds     |
| **3**  | Docker Compose Esencial   | 75 min | Orquestación básica, servicios principales     |
| **4**  | Production Deployment     | 75 min | Configuración básica, variables, health checks |

**CAMBIOS PRINCIPALES:**

- ✅ **Docker fundamentals completo**: Base sólida en 90min
- ✅ **Dockerfile mastery**: Optimización y best practices completas
- ⬇️ **Compose simplificado**: Enfoque en setup funcional (75min vs 90min)
- ⬇️ **Production básico**: Configuración esencial (75min vs 90min)
- ❌ **Eliminado**: Configuraciones avanzadas, security scanning complejo

## 📚 Contenido de la Semana

### **📋 Navegación Ordenada (Seguir este orden)**

1. **[🧭 1-teoria/](./1-teoria/)** - Conceptos de containerización y Docker
2. **[💻 2-practica/](./2-practica/)** - Implementación de containerización completa
3. **[🎯 3-ejercicios/](./3-ejercicios/)** - Ejercicios de Docker y deployment
4. **[🚀 4-proyecto/](./4-proyecto/)** - API containerizada lista para producción
5. **[📚 5-recursos/](./5-recursos/)** - Referencias y herramientas de Docker

### **💻 Prácticas**

1. [🐳 Docker Básico y Setup](./2-practica/31-docker-basics.md) _(90 min)_
2. [📦 Dockerfile para FastAPI](./2-practica/32-dockerfile-fastapi.md) _(90 min)_
3. [🔧 Docker Compose Esencial](./2-practica/33-docker-compose.md) _(75 min)_
4. [🚀 Production Deployment](./2-practica/34-production-deployment.md) _(75 min)_

**OPTIMIZADO PARA 5H 30MIN:**

- ✅ **Práctica 31-32**: Tiempo completo para fundamentos sólidos
- ⬇️ **Práctica 33**: Compose esencial, configuración funcional
- ⬇️ **Práctica 34**: Production basics, deployment preparation

### **💪 Ejercicios**

- [🎯 Ejercicios de Containerización](./3-ejercicios/ejercicios-docker.md)

### **🚀 Proyecto**

- [🏪 E-commerce Containerizado](./4-proyecto/especificacion-docker.md)

## 🐳 Tecnologías de la Semana

### **Herramientas Principales**

- **Docker** - Containerización de aplicaciones
- **Docker Compose** - Orquestación de servicios locales
- **Multi-stage builds** - Optimización de imágenes
- **Docker Hub** - Registro de imágenes

### **Stack Completo**

- **FastAPI** - API backend
- **PostgreSQL** - Base de datos en container
- **Redis** - Cache en container
- **Nginx** - Proxy reverso (opcional)

## ⏱️ **Estructura de 6 Horas (Incluye Break de 30 min)**

### **Bloque 1: Docker Básico y Conceptos (90 min)**

- **31-docker-basics.md**
- Instalación y configuración de Docker
- Conceptos fundamentales: imágenes, containers, volumes
- Comandos básicos de Docker CLI
- Primeros containers con aplicaciones Python

### **☕ BREAK OBLIGATORIO (30 min)**

### **Bloque 2: Dockerfile para FastAPI (90 min)**

- **32-dockerfile-fastapi.md**
- Creación de Dockerfile optimizado
- Multi-stage builds para eficiencia
- Gestión de dependencias y requirements
- Variables de entorno y configuración

### **Bloque 3: Docker Compose Esencial (75 min)**

- **33-docker-compose.md** _(optimizado)_
- Configuración esencial de docker-compose.yml
- FastAPI + PostgreSQL + Redis setup
- Networking básico entre containers
- Testing y troubleshooting básico

### **Bloque 4: Production Deployment (75 min)**

- **34-production-deployment.md** _(optimizado)_
- Configuración básica para producción
- Variables de entorno management
- Health checks esenciales
- Deployment preparation y documentation

## 📅 Cronograma AJUSTADO de la Jornada (5h 30min efectivos)

| Tiempo      | Actividad                 | Duración | Acumulado |
| ----------- | ------------------------- | -------- | --------- |
| 12:00-13:30 | Docker Básico y Conceptos | 90 min   | 90 min    |
| 13:30-14:00 | **☕ BREAK OBLIGATORIO**  | 30 min   | 120 min   |
| 14:00-15:30 | Dockerfile para FastAPI   | 90 min   | 210 min   |
| 15:30-16:45 | Docker Compose Esencial   | 75 min   | 285 min   |
| 16:45-18:00 | Production Deployment     | 75 min   | 360 min   |

**Total**: Exactamente 5h 30min efectivos (330 minutos + 30min break)

---

## ⚡ Arquitectura de la Semana

```
📦 Aplicación Containerizada
├── 🐳 FastAPI Container
│   ├── Imagen optimizada
│   ├── Multi-stage build
│   └── Variables de entorno
├── 🗄️ PostgreSQL Container
│   ├── Persistencia de datos
│   ├── Configuración segura
│   └── Init scripts
├── 🔴 Redis Container
│   ├── Cache en memoria
│   ├── Configuración optimizada
│   └── Networking interno
└── 🌐 Nginx Container (opcional)
    ├── Proxy reverso
    ├── SSL termination
    └── Static files
```

## 💡 **Fundamentos Clave (Para empezar)**

### **Conceptos Esenciales**

- ✅ **Containers vs VMs** - Diferencias y ventajas
- ✅ **Imágenes Docker** - Layers y optimización
- ✅ **Docker Compose** - Orquestación local
- ✅ **Volumes** - Persistencia de datos
- ✅ **Networking** - Comunicación entre servicios

### **Comandos Básicos Docker**

```bash
# Gestión de contenedores
docker build -t mi-app .
docker run -p 8000:8000 mi-app
docker ps && docker logs <container-id>

# Docker Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## 🛠️ **Prerequisites (Confirmar antes de empezar)**

### **Conocimientos Previos Requeridos**

- ✅ FastAPI API completa funcionando (Semanas 1-8)
- ✅ PostgreSQL y Redis configurados localmente
- ✅ Manejo básico de terminal/comandos
- ✅ Estructura de proyecto organizada

### **Software Requerido**

- ✅ **Docker Desktop** instalado y funcionando
- ✅ **Git** para control de versiones
- ✅ **VS Code** con extensión Docker (recomendado)
- ✅ **Postman/Thunder Client** para testing

## 🚀 **¿Qué construiremos esta semana?**

### **🎯 Proyecto Final: API Completamente Containerizada**

Transformaremos nuestra API existente en una aplicación **completamente containerizada** con:

1. **Dockerfile Optimizado**

   - Multi-stage build para reducir tamaño
   - Configuración de seguridad básica
   - Variables de entorno configurables
   - Health checks integrados

2. **Docker Compose Completo**

   - Servicio FastAPI
   - Base de datos PostgreSQL
   - Cache Redis
   - Networking interno configurado

3. **Configuración de Producción**

   - Optimización de performance
   - Logs estructurados
   - Persistent volumes
   - Environment-specific configs

4. **Deployment Ready**
   - Scripts de deployment automatizados
   - Documentation completa
   - CI/CD preparation
   - Security best practices

---

## 📈 **Progresión de Dificultad**

```
Hora 1-2: Docker Fundamentals 🐳
├── instalación y setup
├── conceptos básicos de containers
├── primeros comandos Docker
└── containers simples

Hora 3-4: FastAPI + Docker 📦
├── Dockerfile creation
├── optimización de imagen
├── variables de entorno
└── testing del container

Hora 5-6: Orquestación Completa 🔧
├── docker-compose setup
├── servicios múltiples
├── networking y volumes
└── deployment preparation
```

---

## 🎯 **Quick Start**

### **Requisitos Previos**

- ✅ **Semanas 1-8 completadas** (API con testing y optimización)
- ✅ **Docker Desktop instalado** y funcionando
- ✅ **PostgreSQL y Redis** configurados localmente
- ✅ **API base** completamente funcional

### **Setup Rápido**

```bash
# 1. Navegar a semana 9
cd semana-09

# 2. Verificar Docker instalación
docker --version && docker-compose --version

# 3. Verificar que la API funciona localmente
cd ../proyecto-final/backend
uvicorn main:app --reload

# 4. Regresar a semana 9 y empezar con práctica 31
cd ../../semana-09/2-practica
cat 31-docker-basics.md
```

---

## 🎯 **Criterios de Éxito**

### **Al final de esta semana (6h), habrás logrado:**

✅ **Container Funcional**: API ejecutándose en Docker sin problemas  
✅ **Docker Compose**: Orquestación completa con BD y cache  
✅ **Imagen Optimizada**: Dockerfile eficiente y seguro  
✅ **Deployment Ready**: Configuración lista para producción  
✅ **Documentation**: Instrucciones claras de deployment

### **🏆 BONUS (Si terminas temprano):**

- 🎯 **Registry Push**: Subir imagen a Docker Hub
- 📊 **Monitoring**: Container health monitoring
- 🔒 **Security Scan**: Análisis básico de vulnerabilidades
- 🚀 **Cloud Deployment**: Deploy en plataforma cloud

---

## 📋 Prerrequisitos Técnicos

### **Conocimientos Previos Requeridos**

- ✅ FastAPI fundamentals y APIs REST (Semanas 1-3)
- ✅ Database operations y autenticación (Semanas 4-5)
- ✅ Testing y optimización (Semanas 6-8)
- ✅ Terminal/command line básico
- ✅ Conceptos de redes básicos

### **Software Requerido**

```bash
# Verificar instalaciones
docker --version          # >= 20.x
docker-compose --version  # >= 1.29.x
git --version            # >= 2.x
python --version         # >= 3.11
```

---

## 🎓 Competencias que Desarrollarás

**Al inicio de la semana ya sabes:**

- Crear APIs REST completas con FastAPI
- Implementar autenticación y testing
- Optimizar performance y aplicar security
- Trabajar con bases de datos y caching

**Al final de la semana dominarás:**

- ✅ **Containerización básica** - Docker fundamentals
- ✅ **Dockerfile creation** - Imágenes optimizadas
- ✅ **Docker Compose** - Orquestación local
- ✅ **Production setup** - Deployment preparation
- ✅ **Container security** - Buenas prácticas básicas

---

## 💡 Tips para el Éxito

### **🎯 Enfoque Recomendado**

1. **Entiende los conceptos** antes de implementar
2. **Practica incrementalmente** - un container a la vez
3. **Documenta tus configuraciones** para reference
4. **Testa cada step** antes de continuar

### **⚠️ Errores Comunes a Evitar**

- No verificar que Docker esté running
- Olvidar exponer puertos correctamente
- No configurar variables de entorno
- Crear imágenes muy pesadas sin optimización

### **🚀 Estrategias de Productividad**

- Usa docker-compose para development
- Aprovecha el cache de layers de Docker
- Mantén imágenes pequeñas con multi-stage builds
- Documenta todos los comandos útiles

---

## 📊 Evaluación Final

**Rubrica disponible**: [Ver rúbrica completa](./RUBRICA_EVALUACION.md)

### **Distribución de Puntos**

- **40%** - Prácticas (31-34)
- **25%** - Ejercicios de containerización
- **30%** - Proyecto final containerizado
- **5%** - Participación y documentación

---

## 🆘 Soporte

### **Durante la Clase**

- 🙋‍♀️ **Preguntas en tiempo real** sobre Docker
- 💡 **Troubleshooting** de containers que no inician
- 🔧 **Debugging** de problemas de networking

### **Recursos de Apoyo**

- 📚 [Documentación oficial Docker](https://docs.docker.com/)
- 🎥 [Video tutoriales específicos](./5-recursos/)
- 💬 **Discord**: Canal #semana9-docker
- 📧 **Email**: Instructor disponible 24/7

---

## 🌟 Proyecto Destacado

Al final de esta semana habrás creado una **aplicación completamente containerizada** que incluye:

- 🐳 API FastAPI optimizada en Docker
- 🗄️ Base de datos PostgreSQL persistente
- 🔴 Cache Redis para performance
- 🔧 Orquestación completa con Docker Compose
- 🚀 Configuración lista para cualquier entorno

---

¡Prepárate para llevar tu aplicación al siguiente nivel con containerización profesional! 🐳🚀

---

_Última actualización: 27 de julio de 2025_  
_Bootcamp FastAPI - EPTI Development_
