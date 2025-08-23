# Semana 7: Testing Avanzado y Performance Básica

⏰ **DURACIÓN T### **💻 Prácticas\*\*

1. [🔍 Coverage Avanzado y Testing con Mocks](./2-practica/25-coverage-advanced.md) _(90 min)_
2. [🔴 Redis y Caching Básico](./2-practica/26-redis-basic.md) _(60 min)_
3. [🗃️ Database Optimization Básica](./2-practica/27-database-basic.md) _(60 min)_
4. [🔧 CI/CD con GitHub Actions](./2-practica/28-cicd-basic.md) _(75 min)_
5. [✅ Consolidación y Testing Final](./2-practica/29-final-integration.md) _(45 min)_ HORAS EXACTAS**  
   📚 **NIVEL: Intermedio-Avanzado (construye sobre Semanas 1-6)\*\*

## 🚨 **IMPORTANTE: Testing + Performance Básica**

Esta semana está diseñada para estudiantes que **ya tienen una API completa con autenticación, roles y testing básico** (Semanas 1-6). Implementaremos testing avanzado con coverage y optimizaciones básicas de performance.

- ✅ **Completamente realizable en 6 horas**
- ✅ **Enfoque práctico en testing robusto + performance**
- ✅ **Preparación para CI/CD y producción básica**

## 🎯 Objetivos de la Semana AJUSTADOS (Fundamentales)

Al finalizar esta semana de 5h 30min efectivos (incluye break de 30 min), los estudiantes:

1. ✅ **Implementarán coverage avanzado** con reportes detallados
2. ✅ **Configurarán CI/CD básico** con GitHub Actions
3. ✅ **Aplicarán caching básico** con Redis para consultas frecuentes
4. ✅ **Optimizarán consultas** de base de datos con índices básicos
5. ✅ **Consolidarán sistema completo** con testing y performance

### ❌ **Lo que NO se espera dominar esta semana** (MOVIDO A SEMANA 8)

- ~~Middleware personalizado avanzado~~ → **Semana 8**
- ~~Rate limiting complejo~~ → **Semana 8**
- ~~Monitoring avanzado con métricas~~ → **Semana 8**
- ~~Profiling de performance complejo~~ → **Semana 8**
- Microservicios y arquitectura distribuida
- Clusters de Redis y alta disponibilidad

## ⏱️ Distribución de Tiempo AJUSTADA (5h 30min efectivos)

| Bloque | Actividad                   | Tiempo | Descripción                                 |
| ------ | --------------------------- | ------ | ------------------------------------------- |
| **1**  | Coverage y Testing Avanzado | 90 min | Coverage reports, mocks, fixtures avanzadas |
| **2**  | Redis y Caching Básico      | 60 min | Redis setup, cache patterns básicos         |
| **3**  | Database Optimization       | 60 min | Índices básicos, EXPLAIN, connection pool   |
| **4**  | CI/CD Introducción          | 75 min | GitHub Actions, testing automático          |
| **5**  | Consolidación Final         | 45 min | Testing completo, debugging, documentación  |

**CAMBIOS PRINCIPALES:**

- ✅ **Agregado**: Coverage avanzado y testing con mocks (desde Semana 6)
- ✅ **Agregado**: CI/CD básico con GitHub Actions
- ⬇️ **Reducido**: Redis de 90 a 60 minutos (solo básico)
- ⬇️ **Reducido**: Database optimization de 90 a 60 minutos
- ❌ **Eliminado**: Middleware avanzado (se mueve a Semana 8)
- ❌ **Eliminado**: Monitoring complejo (se mueve a Semana 8)

## 📚 Contenido de la Semana

### **📋 Navegación Ordenada (Seguir este orden)**

1. **[🧭 1-teoria/](./1-teoria/)** - Conceptos de performance y optimización
2. **[💻 2-practica/](./2-practica/)** - Implementación de optimizaciones
3. **[🎯 3-ejercicios/](./3-ejercicios/)** - Ejercicios de performance
4. **[🚀 4-proyecto/](./4-proyecto/)** - API optimizada para producción
5. **[📚 5-recursos/](./5-recursos/)** - Referencias y herramientas

### **🧭 Teoría**

- [⚡ Performance y Optimización en APIs](./1-teoria/performance-concepts.md)

### **💻 Prácticas**

1. [� Coverage Avanzado y Testing con Mocks](./2-practica/25-coverage-advanced.md) _(90 min)_
2. [�🔴 Redis y Caching Básico](./2-practica/26-redis-basic.md) _(60 min)_
3. [🗃️ Database Optimization Básica](./2-practica/27-database-basic.md) _(60 min)_
4. [� CI/CD con GitHub Actions](./2-practica/28-cicd-basic.md) _(75 min)_
5. [� Consolidación y Testing Final](./2-practica/29-final-integration.md) _(45 min)_

**ELIMINADO/MOVIDO A SEMANA 8:**

- ~~Middleware personalizado~~ → **Semana 8**
- ~~Rate limiting avanzado~~ → **Semana 8**
- ~~Monitoring y profiling~~ → **Semana 8**

### **💪 Ejercicios**

- [🎯 Ejercicios de Optimización](./3-ejercicios/ejercicios-performance.md)

### **🚀 Proyecto**

- [🏪 E-commerce High Performance](./4-proyecto/especificacion-performance.md)

### **📚 Recursos**

- [📖 Recursos de Performance](./5-recursos/recursos-apoyo.md)

---

## ⚡ Tecnologías de la Semana

### **Stack de Performance**

- **Redis**: Sistema de cache en memoria para optimización
- **SQLAlchemy Optimizations**: Query optimization y connection pooling
- **Slowapi**: Middleware para rate limiting en FastAPI
- **Uvicorn**: Configuraciones avanzadas del servidor ASGI

### **Herramientas de Monitoring**

- **Python Profilers**: cProfile, py-spy para análisis de performance
- **FastAPI Middleware**: Custom middleware para métricas
- **Logging**: Structured logging con loguru
- **Memory Profiling**: memory_profiler para análisis de memoria

### **Database Performance**

- **PostgreSQL Indexes**: Optimización de consultas con índices
- **Connection Pooling**: Gestión eficiente de conexiones DB
- **Query Analysis**: EXPLAIN y optimización de queries
- **Async Database Operations**: Operaciones asíncronas avanzadas

---

## ⏱️ **Estructura de 6 Horas (Incluye Break de 30 min)**

### **Bloque 1: Coverage y Testing Avanzado (90 min)**

- **25-coverage-advanced.md**
- Coverage reports con HTML/XML
- Testing con mocks y fixtures avanzadas
- Integración con herramientas de CI

### **Bloque 2: Redis y Caching Básico (60 min)**

- **26-redis-basic.md** _(simplificado)_
- Instalación y configuración de Redis
- Cache básico para endpoints críticos
- Invalidación simple de cache

### **Bloque 3: Database Optimization Básica (60 min)**

- **27-database-basic.md** _(simplificado)_
- Análisis básico con EXPLAIN
- Creación de índices estratégicos básicos
- Connection pooling simple

### **Bloque 4: CI/CD Introducción (75 min)**

- **28-cicd-basic.md** _(nuevo)_
- GitHub Actions workflow básico
- Testing automático en CI
- Deploy concepts fundamentales

---

## 🎯 **Quick Start**

### **Requisitos Previos**

- ✅ **Semanas 1-6 completadas** (API con auth y testing)
- ✅ **PostgreSQL funcionando** correctamente
- ✅ **Docker instalado** para Redis
- ✅ **API base** con usuarios y CRUD implementado

### **Setup Rápido**

```bash
# 1. Navegar a semana 7
cd semana-07

# 2. Instalar dependencias de performance
pip install redis slowapi loguru memory-profiler py-spy

# 3. Levantar Redis con Docker
docker run -d --name redis-cache -p 6379:6379 redis:alpine

# 4. Verificar conexión Redis
python -c "import redis; r=redis.Redis(); print('Redis OK:', r.ping())"

# 5. Empezar con práctica 23
cd 2-practica && cat 23-redis-caching.md
```

## 📅 Cronograma AJUSTADO de la Jornada (5h 30min efectivos)

| Tiempo      | Actividad                   | Duración | Acumulado |
| ----------- | --------------------------- | -------- | --------- |
| 12:00-13:30 | Coverage y Testing Avanzado | 90 min   | 90 min    |
| 13:30-14:00 | **☕ BREAK OBLIGATORIO**    | 30 min   | 120 min   |
| 14:00-15:00 | Redis y Caching Básico      | 60 min   | 180 min   |
| 15:00-16:00 | Database Optimization       | 60 min   | 240 min   |
| 16:00-17:15 | CI/CD con GitHub Actions    | 75 min   | 315 min   |
| 17:15-18:00 | Consolidación Final         | 45 min   | 360 min   |

**Total**: Exactamente 5h 30min efectivos (330 minutos + 30min break)

---

## 📊 **Métricas de Éxito**

### **Performance Targets**

- 🎯 **Response Time**: <200ms para endpoints CRUD básicos
- 🎯 **Cache Hit Ratio**: >80% en endpoints frecuentes
- 🎯 **Memory Usage**: <512MB para aplicación completa
- 🎯 **Database Connections**: Pool eficiente <20 conexiones
- 🎯 **Rate Limiting**: 100 requests/min por usuario

### **Monitoring Básico**

- ✅ **Request/Response Logging**: Todas las operaciones
- ✅ **Error Tracking**: 4xx y 5xx responses
- ✅ **Performance Metrics**: Response times por endpoint
- ✅ **Resource Usage**: CPU, Memory, Database connections
- ✅ **Cache Metrics**: Hit ratio, miss ratio, invalidations

---

## 💡 **Tips para el Éxito**

### **Enfoque Pragmático**

1. **Mide antes de optimizar** - Profile first, optimize second
2. **80/20 Rule** - Enfócate en las optimizaciones que más impacto tienen
3. **Cache inteligentemente** - No todo necesita cache
4. **Monitor en tiempo real** - Métricas deben ser visible y actionable

### **Mejores Prácticas**

1. **Graceful Degradation** - App funciona sin cache/Redis
2. **Cache Invalidation** - Estrategia clara para mantener consistencia
3. **Rate Limiting Justo** - No bloquear usuarios legítimos
4. **Logging Estructurado** - JSON logs para análisis posterior

### **Evitar Sobre-optimización**

1. **Optimizar solo bottlenecks reales** identificados por profiling
2. **Mantener código legible** - Performance no debe sacrificar claridad
3. **Testing de performance** - Verificar mejoras con datos
4. **Documentar optimizaciones** - Explicar por qué y cómo

---

## 🔧 **Configuración de Herramientas**

### **Redis Configuration**

```bash
# Producción con persistencia
docker run -d --name redis-prod \
  -p 6379:6379 \
  -v redis_data:/data \
  redis:alpine redis-server --appendonly yes
```

### **PostgreSQL Optimization**

```sql
-- Configuraciones básicas para performance
ALTER SYSTEM SET shared_buffers = '256MB';
ALTER SYSTEM SET effective_cache_size = '1GB';
ALTER SYSTEM SET maintenance_work_mem = '64MB';
SELECT pg_reload_conf();
```

### **FastAPI Performance Settings**

```python
# uvicorn con optimizaciones
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --access-log
```

---

## 🚨 **Consideraciones Importantes**

### **Production Readiness**

- ⚠️ **Cache Failures**: App debe funcionar sin Redis
- ⚠️ **Rate Limiting**: Configurar límites apropiados
- ⚠️ **Memory Leaks**: Monitor memory usage continuamente
- ⚠️ **Database Connections**: Evitar connection pool exhaustion

### **Security**

- 🔒 **Redis Security**: Configurar auth si está expuesto
- 🔒 **Rate Limiting Bypass**: Evitar bypass con headers
- 🔒 **Log Sanitization**: No loggear información sensible
- 🔒 **Error Information**: No exponer detalles internos

### **Scalability**

- 📈 **Horizontal Scaling**: Preparar para múltiples instancias
- 📈 **Database Scaling**: Read replicas consideration
- 📈 **Cache Distribution**: Redis Cluster para escala mayor
- 📈 **Stateless Design**: App debe ser stateless

---

## 🎓 **Criterios de Evaluación**

### **Performance (40%)**

- Cache implementation funcionando correctamente
- Database queries optimizadas
- Response times mejorados vs baseline
- Memory usage controlado

### **Monitoring (30%)**

- Logging estructurado implementado
- Métricas básicas capturadas
- Profiling realizado y documentado
- Rate limiting funcionando

### **Código (30%)**

- Middleware implementado correctamente
- Error handling para cache failures
- Configuración externalizada
- Documentación de optimizaciones

---

¡Prepárate para llevar tu API FastAPI al siguiente nivel de performance! ⚡🚀
