# Ejercicios Prácticos - Semana 9: Containerización

⏰ **Tiempo estimado**: 2-3 horas  
🎯 **Objetivo**: Consolidar conocimientos de Docker y containerización

---

## 📋 Instrucciones Generales

- ✅ Completa los ejercicios en orden secuencial
- ✅ Documenta tus soluciones en archivos README
- ✅ Testea cada ejercicio antes de continuar
- ✅ Guarda evidencias (screenshots, logs) de tu trabajo

---

## 🐳 Ejercicio 1: Dockerfile Optimizado (45 min)

### **Objetivo**

Crear un Dockerfile optimizado para una aplicación Flask simple

### **Instrucciones**

1. **Crear aplicación Flask básica**

   ```python
   # app.py
   from flask import Flask, jsonify
   import os
   import psutil
   from datetime import datetime

   app = Flask(__name__)

   @app.route('/')
   def home():
       return jsonify({
           "message": "Flask en Docker",
           "timestamp": datetime.now().isoformat(),
           "hostname": os.getenv("HOSTNAME", "unknown")
       })

   @app.route('/health')
   def health():
       return jsonify({
           "status": "healthy",
           "cpu_percent": psutil.cpu_percent(),
           "memory_mb": psutil.virtual_memory().used / 1024 / 1024
       })

   if __name__ == '__main__':
       app.run(host='0.0.0.0', port=5000)
   ```

2. **Crear requirements.txt**

   ```text
   Flask==2.3.3
   psutil==5.9.0
   ```

3. **Crear 3 versiones de Dockerfile**:
   - `Dockerfile.basic` - Versión simple con python:3.13
   - `Dockerfile.alpine` - Versión con Alpine Linux
   - `Dockerfile.multistage` - Multi-stage build optimizado

### **Requisitos técnicos**

- ✅ Usuario no-root en versión Alpine y multistage
- ✅ Health check configurado
- ✅ Variables de entorno para configuración
- ✅ Optimización de capas para cache de Docker
- ✅ .dockerignore apropiado

### **Criterios de evaluación**

- **Tamaño de imagen** - Alpine debe ser < 100MB
- **Seguridad** - No ejecutar como root
- **Performance** - Build time optimizado
- **Health check** - Funcionando correctamente

### **Entregables**

```
ejercicio-1/
├── app.py
├── requirements.txt
├── Dockerfile.basic
├── Dockerfile.alpine
├── Dockerfile.multistage
├── .dockerignore
└── README.md          # Comparación de tamaños y análisis
```

---

## 🔧 Ejercicio 2: Docker Compose Multi-Servicio (60 min)

### **Objetivo**

Crear un stack completo con aplicación web, base de datos y cache

### **Instrucciones**

1. **Crear aplicación FastAPI con base de datos**

   ```python
   # main.py
   from fastapi import FastAPI, HTTPException
   from sqlalchemy import create_engine, Column, Integer, String, create_all
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker, Session
   from pydantic import BaseModel
   import redis
   import os

   # Tu código aquí - implementar CRUD básico con PostgreSQL y Redis
   ```

2. **Configurar servicios en docker-compose.yml**:
   - **api**: Tu aplicación FastAPI
   - **db**: PostgreSQL 13
   - **cache**: Redis 6
   - **proxy**: Nginx como reverse proxy

### **Requisitos técnicos**

- ✅ Networks personalizados (backend/frontend)
- ✅ Volumes persistentes para datos
- ✅ Variables de entorno en archivo .env
- ✅ Health checks para todos los servicios
- ✅ Depends_on con conditions

### **Funcionalidades a implementar**

- **API endpoints**: CRUD de usuarios
- **Cache**: Cache de consultas frecuentes
- **Proxy**: Load balancing básico
- **Logs**: Structured logging

### **Criterios de evaluación**

- **Funcionalidad** - CRUD completo funcionando
- **Persistencia** - Datos sobreviven reinicio
- **Networking** - Comunicación correcta entre servicios
- **Configuración** - Variables de entorno bien manejadas

### **Entregables**

```
ejercicio-2/
├── app/
│   ├── main.py
│   └── models.py
├── config/
│   └── nginx.conf
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md          # Instrucciones de uso
```

---

## 🚀 Ejercicio 3: Pipeline CI/CD Básico (45 min)

### **Objetivo**

Implementar un pipeline básico con GitHub Actions

### **Instrucciones**

1. **Crear workflow de CI/CD**

   - Test automatizado
   - Build de imagen Docker
   - Scan de seguridad básico
   - Push a registry (simulado)

2. **Configurar ambientes**
   - Desarrollo (docker-compose local)
   - Staging (con variables específicas)
   - Producción (configuración optimizada)

### **Requisitos técnicos**

- ✅ Tests ejecutándose en GitHub Actions
- ✅ Build condicional según branch
- ✅ Versionado automático de imágenes
- ✅ Deploy scripts automatizados

### **Criterios de evaluación**

- **Pipeline** - Workflow completo sin errores
- **Testing** - Tests pasando consistentemente
- **Seguridad** - Scan básico implementado
- **Automatización** - Deploy script funcional

### **Entregables**

```
ejercicio-3/
├── .github/workflows/
│   ├── ci.yml
│   └── deploy.yml
├── scripts/
│   ├── deploy.sh
│   └── test.sh
├── docker-compose.staging.yml
├── docker-compose.production.yml
└── README.md          # Explicación del pipeline
```

---

## 🔍 Ejercicio 4: Monitoring y Observabilidad (45 min)

### **Objetivo**

Implementar monitoring básico para aplicación containerizada

### **Instrucciones**

1. **Agregar métricas a tu aplicación**

   ```python
   # Implementar endpoints de métricas
   @app.get("/metrics")
   async def metrics():
       # Retornar métricas de sistema y aplicación
       pass
   ```

2. **Configurar stack de monitoring**

   - **Prometheus** para recolección de métricas
   - **Grafana** para visualización
   - **AlertManager** para alertas básicas

3. **Implementar logging estructurado**
   - JSON logs con información relevante
   - Diferentes niveles de log
   - Agregación centralizada

### **Requisitos técnicos**

- ✅ Métricas custom en aplicación
- ✅ Dashboard básico en Grafana
- ✅ Alertas configuradas
- ✅ Logs estructurados en JSON

### **Criterios de evaluación**

- **Métricas** - Datos útiles y precisos
- **Visualización** - Dashboard informativo
- **Alertas** - Configuración apropiada
- **Logs** - Estructura consistente

### **Entregables**

```
ejercicio-4/
├── monitoring/
│   ├── prometheus.yml
│   ├── grafana-dashboard.json
│   └── alertmanager.yml
├── docker-compose.monitoring.yml
├── app/
│   ├── main.py         # Con métricas
│   └── logger.py       # Logging estructurado
└── README.md           # Guía de monitoring
```

---

## 🏗️ Ejercicio 5: Optimización y Performance (30 min)

### **Objetivo**

Optimizar containers para performance en producción

### **Instrucciones**

1. **Analizar y optimizar imagen Docker**

   - Reducir capas innecesarias
   - Optimizar orden de comandos
   - Usar .dockerignore efectivo

2. **Implementar estrategias de cache**

   - Cache de dependencias
   - Cache de build stages
   - Cache de datos de aplicación

3. **Configurar resource limits**
   - Memory limits apropiados
   - CPU limits y requests
   - Health checks optimizados

### **Benchmarks a realizar**

```bash
# Build time comparison
time docker build -t app:v1 .
time docker build -t app:v2 . # Con optimizaciones

# Image size comparison
docker images | grep app

# Runtime performance
docker stats app_container
```

### **Criterios de evaluación**

- **Build time** - Reducción significativa
- **Image size** - Optimización demostrable
- **Runtime performance** - Uso eficiente de recursos
- **Documentation** - Análisis completo de optimizaciones

### **Entregables**

```
ejercicio-5/
├── Dockerfile.original
├── Dockerfile.optimized
├── .dockerignore
├── benchmark-results.md
└── README.md           # Análisis de optimizaciones
```

---

## 🎯 Ejercicio Integrador: Stack Completo (45 min)

### **Objetivo**

Integrar todos los conceptos en un proyecto completo

### **Descripción del proyecto**

Crear un sistema de "URL Shortener" (como bit.ly) completamente containerizado

### **Componentes requeridos**

1. **API Backend** (FastAPI)

   - Crear URLs cortas
   - Redirigir URLs
   - Estadísticas básicas
   - Rate limiting

2. **Base de datos** (PostgreSQL)

   - Almacenar URLs y metadata
   - Índices optimizados

3. **Cache** (Redis)

   - Cache de URLs frecuentes
   - Rate limiting data

4. **Frontend** (Nginx serving static files)

   - Interfaz web simple
   - API documentation

5. **Monitoring** (Prometheus + Grafana)
   - Métricas de uso
   - Performance monitoring

### **Requisitos funcionales**

```python
# API Endpoints requeridos
POST /shorten     # Crear URL corta
GET /{short_id}   # Redirigir a URL original
GET /stats/{short_id}  # Estadísticas de una URL
GET /health       # Health check
GET /metrics      # Métricas Prometheus
```

### **Requisitos técnicos**

- ✅ Multi-stage Dockerfile optimizado
- ✅ Docker Compose con todos los servicios
- ✅ Variables de entorno para configuración
- ✅ Health checks en todos los servicios
- ✅ Volumes persistentes
- ✅ Networks segmentados
- ✅ CI/CD pipeline básico
- ✅ Monitoring configurado
- ✅ Logging estructurado

### **Criterios de evaluación**

- **Funcionalidad** (30%) - Todas las features funcionando
- **Containerización** (25%) - Dockerfile y Compose optimizados
- **Seguridad** (20%) - Buenas prácticas aplicadas
- **Monitoring** (15%) - Observabilidad implementada
- **Documentación** (10%) - README completo y claro

### **Entregables**

```
url-shortener/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── config.py
│   └── utils.py
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
├── monitoring/
│   ├── prometheus.yml
│   ├── grafana-dashboard.json
│   └── alerts.yml
├── config/
│   └── nginx.conf
├── scripts/
│   ├── deploy.sh
│   ├── backup.sh
│   └── test.sh
├── .github/workflows/
│   └── ci-cd.yml
├── tests/
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── docker-compose.production.yml
├── requirements.txt
├── .env.example
├── .dockerignore
└── README.md
```

---

## 📊 Criterios de Evaluación General

### **Excelente (90-100 puntos)**

- ✅ Todos los ejercicios completados
- ✅ Dockerfile optimizados con multi-stage builds
- ✅ Seguridad implementada (usuario no-root, resource limits)
- ✅ Monitoring y logging configurados
- ✅ CI/CD pipeline funcional
- ✅ Documentación completa y clara
- ✅ Proyecto integrador completamente funcional

### **Bueno (80-89 puntos)**

- ✅ 4-5 ejercicios completados correctamente
- ✅ Dockerfiles funcionales con optimizaciones básicas
- ✅ Docker Compose con servicios funcionando
- ✅ Algunas prácticas de seguridad aplicadas
- ✅ Documentación básica presente

### **Satisfactorio (70-79 puntos)**

- ✅ 3-4 ejercicios completados
- ✅ Containers ejecutándose correctamente
- ✅ Configuración básica de Docker Compose
- ✅ Funcionalidad principal implementada

### **Necesita Mejora (< 70 puntos)**

- ❌ Menos de 3 ejercicios completados
- ❌ Problemas en configuración básica
- ❌ Falta de documentación
- ❌ Containers no ejecutándose correctamente

---

## 🆘 Ayuda y Recursos

### **Comandos útiles para debugging**

```bash
# Ver logs de containers
docker logs container-name -f

# Acceder al shell de un container
docker exec -it container-name /bin/sh

# Ver uso de recursos
docker stats

# Inspeccionar networks
docker network ls
docker network inspect network-name

# Ver volumes
docker volume ls
docker volume inspect volume-name

# Limpiar sistema
docker system prune -a
```

### **Troubleshooting común**

1. **Puerto ya en uso**: Cambiar puerto en docker-compose.yml
2. **Permission denied**: Verificar usuario en Dockerfile
3. **Cannot connect to database**: Verificar depends_on y health checks
4. **Out of space**: Limpiar imágenes y containers no usados
5. **Build failures**: Verificar .dockerignore y context

---

## 📝 Formato de Entrega

### **Estructura del repositorio**

```
semana-09-ejercicios/
├── ejercicio-1/
├── ejercicio-2/
├── ejercicio-3/
├── ejercicio-4/
├── ejercicio-5/
├── proyecto-integrador/
├── EJERCICIOS_COMPLETADOS.md    # Checklist de ejercicios
└── README.md                   # Resumen y aprendizajes
```

### **README.md principal debe incluir**

- ✅ Lista de ejercicios completados
- ✅ Principales desafíos encontrados
- ✅ Soluciones implementadas
- ✅ Aprendizajes clave
- ✅ Instrucciones para ejecutar cada ejercicio

---

**🎯 ¡A containerizar!** Estos ejercicios te darán experiencia práctica completa con Docker y te prepararán para trabajar en entornos de producción reales. 🐳🚀

---

_Ejercicios Semana 9 - Bootcamp FastAPI_  
_Tiempo total estimado: 4-5 horas_
