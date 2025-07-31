# Semana 7: Optimización y Performance

⏰ **DURACIÓN TOTAL: 6 HORAS EXACTAS**  
📚 **NIVEL: Intermedio-Avanzado (construye sobre Semanas 1-6)**

## 🚨 **IMPORTANTE: Optimizando para Producción**

Esta semana está diseñada para estudiantes que **ya tienen una API completa con autenticación y testing** (Semanas 1-6). Implementaremos técnicas de optimización y monitoring para preparar la aplicación para producción.

- ✅ **Completamente realizable en 6 horas**
- ✅ **Enfoque práctico en performance real**
- ✅ **Preparación para deployment en producción**

## 🎯 Objetivos de la Semana (Fundamentales)

Al finalizar esta semana de 6 horas (incluye break de 30 min), los estudiantes:

1. ✅ **Implementarán caching** con Redis para optimización de consultas
2. ✅ **Configurarán monitoring** básico de performance y logs
3. ✅ **Optimizarán consultas** de base de datos con técnicas avanzadas
4. ✅ **Aplicarán middleware** para rate limiting y compresión
5. ✅ **Medirán performance** con herramientas de profiling

### ❌ **Lo que NO se espera dominar esta semana**

- Microservicios y arquitectura distribuida
- Clusters de Redis y alta disponibilidad
- Monitoring avanzado con Prometheus/Grafana completo
- Load balancing y auto-scaling
- CDN y optimización de red avanzada

## ⏱️ Distribución de Tiempo (6 horas total)

| Bloque | Actividad                  | Tiempo | Descripción                                   |
| ------ | -------------------------- | ------ | --------------------------------------------- |
| **1**  | Caching con Redis          | 90 min | Redis setup, cache patterns, invalidation     |
| **2**  | Database Optimization      | 90 min | Query optimization, indexes, connections      |
| **3**  | Middleware y Rate Limiting | 90 min | Custom middleware, rate limiting, compression |
| **4**  | Monitoring y Profiling     | 90 min | Logs, metrics, performance monitoring         |

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

1. [🔴 Redis y Caching Strategies](./2-practica/23-redis-caching.md) _(90 min)_
2. [🗃️ Database Performance Optimization](./2-practica/24-database-optimization.md) _(90 min)_
3. [🛠️ Middleware y Rate Limiting](./2-practica/25-middleware-rate-limiting.md) _(90 min)_
4. [📊 Monitoring y Performance Analysis](./2-practica/26-monitoring-profiling.md) _(90 min)_

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

### **Bloque 1: Redis y Caching (90 min)**

- **23-redis-caching.md**
- Instalación y configuración de Redis
- Patrones de cache (Cache-Aside, Write-Through)
- Implementación de cache en endpoints críticos
- Cache invalidation strategies

### **Bloque 2: Database Optimization (90 min)**

- **24-database-optimization.md**
- Análisis de queries lentas con EXPLAIN
- Creación de índices estratégicos
- Connection pooling avanzado
- Lazy loading vs eager loading

### **Bloque 3: Middleware y Rate Limiting (90 min)**

- **25-middleware-rate-limiting.md**
- Custom middleware para métricas
- Rate limiting por usuario/IP
- Compresión de respuestas
- Request/Response logging

### **Bloque 4: Monitoring y Profiling (90 min)**

- **26-monitoring-profiling.md**
- Structured logging implementation
- Performance profiling con py-spy
- Memory usage analysis
- Métricas de aplicación básicas

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

## 📅 Cronograma de la Jornada de 6 Horas

| Tiempo      | Actividad                       | Duración | Acumulado |
| ----------- | ------------------------------- | -------- | --------- |
| 12:00-13:30 | Redis y Caching                 | 90 min   | 90 min    |
| 13:30-14:00 | Database Optimization (parte 1) | 30 min   | 120 min   |
| 14:00-14:30 | **☕ BREAK OBLIGATORIO**        | 30 min   | 150 min   |
| 14:30-15:30 | Database Optimization (parte 2) | 60 min   | 210 min   |
| 15:30-17:00 | Middleware y Rate Limiting      | 90 min   | 300 min   |
| 17:00-18:00 | Monitoring y Profiling          | 60 min   | 360 min   |

**Total**: Exactamente 6 horas (360 minutos)

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
