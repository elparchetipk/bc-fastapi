# Proyecto Semana 7: Sistema de Performance y Monitoreo

## Información del Proyecto

### 📋 Descripción General

Desarrollar un sistema completo de performance monitoring y optimización para una aplicación FastAPI, implementando técnicas de profiling, caching avanzado, y monitoreo en tiempo real.

### 🎯 Objetivos de Aprendizaje

Al completar este proyecto, los estudiantes serán capaces de:

- **Análisis de Performance**: Identificar cuellos de botella y optimizar aplicaciones
- **Caching Estratégico**: Implementar múltiples niveles de cache
- **Monitoreo Integral**: Configurar métricas, logs y alertas
- **Observabilidad**: Crear dashboards y sistemas de diagnóstico

### ⏱️ Tiempo Estimado

**4-5 horas** (distribuidas durante la semana)

### 📊 Peso en Evaluación

- **40%** - Funcionalidad y optimización
- **25%** - Calidad del código y arquitectura
- **20%** - Sistema de monitoreo
- **15%** - Documentación y presentación

---

## Especificación Técnica

### 🛠️ Stack Tecnológico Requerido

#### Backend

- **Framework**: FastAPI 0.104+
- **Base de Datos**: PostgreSQL con SQLAlchemy
- **Cache**: Redis 6.0+
- **Monitoreo**: Prometheus + Grafana (opcional)
- **Profiling**: py-spy, memory-profiler

#### Herramientas de Desarrollo

```bash
# Dependencias principales
pip install fastapi uvicorn sqlalchemy psycopg2-binary
pip install redis prometheus-client psutil
pip install py-spy memory-profiler line-profiler
```

### 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────┐
│   Load Balancer │    │    FastAPI   │    │  PostgreSQL │
│   (opcional)    │────│  Application │────│  Database   │
└─────────────────┘    └──────────────┘    └─────────────┘
                              │
                       ┌──────────────┐    ┌─────────────┐
                       │    Redis     │    │ Prometheus  │
                       │    Cache     │    │  Metrics    │
                       └──────────────┘    └─────────────┘
                              │
                       ┌──────────────┐    ┌─────────────┐
                       │  Monitoring  │    │   Grafana   │
                       │  Dashboard   │    │ Dashboard   │
                       └──────────────┘    └─────────────┘
```

---

## Componentes del Proyecto

### 1. 🚀 Sistema Base (30% del proyecto)

#### Aplicación FastAPI con Datos de Prueba

```python
# Estructura mínima requerida
app/
├── main.py                 # Aplicación principal
├── models/
│   ├── __init__.py
│   ├── user.py            # Modelo Usuario
│   ├── post.py            # Modelo Post
│   └── comment.py         # Modelo Comentario
├── routers/
│   ├── users.py           # Endpoints de usuarios
│   ├── posts.py           # Endpoints de posts
│   └── comments.py        # Endpoints de comentarios
├── database.py            # Configuración de BD
└── config.py              # Configuración
```

**Requisitos del sistema base:**

- Mínimo 3 modelos relacionados (User, Post, Comment)
- CRUD completo para cada modelo
- Relaciones entre modelos (1:N, N:M)
- 1000+ registros de prueba por modelo
- Endpoints con problemas de rendimiento intencionados

### 2. 📊 Sistema de Profiling y Análisis (25% del proyecto)

#### Componentes Requeridos

```python
profiling/
├── profiler.py            # Decorador de profiling
├── performance_analyzer.py # Análisis de queries
├── benchmarking.py        # Herramientas de benchmark
└── reports/               # Reportes generados
    ├── before_optimization.md
    └── after_optimization.md
```

**Funcionalidades requeridas:**

- Decorador para perfilar endpoints automáticamente
- Identificación de queries N+1
- Medición de tiempo de ejecución y uso de memoria
- Generación de reportes comparativos
- Dashboard web básico para visualizar resultados

### 3. 🗃️ Sistema de Cache Multicapa (25% del proyecto)

#### Arquitectura de Cache

```python
cache/
├── redis_client.py        # Cliente Redis
├── decorators.py          # Decoradores de cache
├── strategies.py          # Estrategias de caching
├── invalidation.py        # Sistema de invalidación
└── monitoring.py          # Monitoreo de cache
```

**Implementaciones requeridas:**

1. **Cache de Aplicación (In-Memory)**

   ```python
   from functools import lru_cache

   @lru_cache(maxsize=1000)
   def get_user_permissions(user_id: int) -> List[str]:
       # Cache para datos que cambian raramente
       pass
   ```

2. **Cache de Base de Datos (Redis)**

   ```python
   @cached(ttl=300, key_prefix="user")
   async def get_user_with_stats(user_id: int):
       # Cache para consultas costosas
       pass
   ```

3. **Cache de Respuestas HTTP**

   ```python
   @response_cache(ttl=600)
   async def get_trending_posts():
       # Cache para endpoints públicos
       pass
   ```

4. **Cache de Sesiones**
   ```python
   async def cache_user_session(user_id: int, session_data: dict):
       # Cache para datos de sesión
       pass
   ```

### 4. 📈 Sistema de Monitoreo (20% del proyecto)

#### Métricas Requeridas

```python
monitoring/
├── metrics.py             # Definición de métricas
├── middleware.py          # Middleware de captura
├── health_checks.py       # Health checks
├── alerting.py           # Sistema de alertas
└── dashboard/            # Dashboard web
    ├── templates/
    │   └── dashboard.html
    └── static/
        ├── js/
        └── css/
```

**Métricas obligatorias:**

- Request rate (requests/second)
- Response time (percentiles 50, 95, 99)
- Error rate (4xx, 5xx)
- Active connections
- Database connection pool
- Cache hit/miss ratio
- Memory usage
- CPU usage

---

## Entregables Específicos

### 📁 1. Código Fuente

```
proyecto-performance/
├── app/                   # Aplicación FastAPI
├── profiling/            # Sistema de profiling
├── cache/                # Sistema de cache
├── monitoring/           # Sistema de monitoreo
├── tests/                # Tests de performance
├── scripts/              # Scripts de utilidad
├── docker-compose.yml    # Configuración Docker
├── requirements.txt      # Dependencias
└── README.md            # Documentación principal
```

### 📊 2. Reportes de Performance

#### Reporte de Análisis Inicial

```markdown
# Análisis de Performance - Estado Inicial

## Métricas Base

- Endpoint /users: 2.3s promedio, 15 queries
- Endpoint /posts: 4.1s promedio, 50+ queries
- Endpoint /stats: 6.7s promedio, 100+ queries

## Problemas Identificados

1. Problema N+1 en /users/{id}/posts
2. Consultas no optimizadas en estadísticas
3. Falta de índices en columnas consultadas
4. Ausencia de cache para datos estáticos

## Plan de Optimización

[Detallar estrategias específicas]
```

#### Reporte de Optimización

```markdown
# Resultados de Optimización

## Mejoras Implementadas

1. Eager loading con selectinload()
2. Cache Redis para consultas frecuentes
3. Índices de base de datos optimizados
4. Paginación eficiente

## Resultados Obtenidos

- Endpoint /users: 0.2s promedio (90% mejora)
- Endpoint /posts: 0.5s promedio (88% mejora)
- Endpoint /stats: 0.3s promedio (95% mejora)

## Métricas de Cache

- Hit rate: 78%
- Reducción de queries: 65%
```

### 🎥 3. Demostración en Vivo

#### Presentación Requerida (10 minutos)

1. **Demostración del problema** (2 min)

   - Mostrar endpoints lentos
   - Explicar cuellos de botella identificados

2. **Soluciones implementadas** (4 min)

   - Cache en acción
   - Comparación antes/después
   - Dashboard de métricas

3. **Resultados y aprendizajes** (3 min)

   - Métricas de mejora
   - Lecciones aprendidas
   - Próximos pasos

4. **Q&A** (1 min)

---

## Criterios de Evaluación

### 📋 Rúbrica Detallada

| Componente       | Excelente (4)                                                  | Bueno (3)                                | Satisfactorio (2)                   | Insuficiente (1)     |
| ---------------- | -------------------------------------------------------------- | ---------------------------------------- | ----------------------------------- | -------------------- |
| **Sistema Base** | Aplicación completa, modelos complejos, datos extensos         | Aplicación funcional con modelos básicos | Sistema básico funcionando          | Sistema incompleto   |
| **Profiling**    | Análisis detallado, múltiples herramientas, reportes completos | Profiling básico con reportes            | Identificación de problemas básicos | Análisis superficial |
| **Optimización** | Mejoras >80%, múltiples técnicas                               | Mejoras 60-80%, técnicas variadas        | Mejoras 40-60%, técnicas básicas    | Mejoras <40%         |
| **Cache**        | Multicapa, estrategias avanzadas, alta eficiencia              | Cache funcional, buenas estrategias      | Cache básico efectivo               | Cache básico         |
| **Monitoreo**    | Sistema completo, alertas, dashboard                           | Métricas principales, visualización      | Métricas básicas                    | Monitoreo mínimo     |

### 🎯 Puntos de Evaluación Específicos

#### Funcionalidad (40 puntos)

- [ ] **Sistema base completo** (10 pts)
- [ ] **Profiling implementado** (10 pts)
- [ ] **Optimizaciones efectivas** (10 pts)
- [ ] **Cache multicapa funcionando** (10 pts)

#### Calidad Técnica (25 puntos)

- [ ] **Código limpio y documentado** (8 pts)
- [ ] **Manejo de errores apropiado** (7 pts)
- [ ] **Tests de performance** (5 pts)
- [ ] **Configuración Docker** (5 pts)

#### Monitoreo (20 puntos)

- [ ] **Métricas comprehensivas** (8 pts)
- [ ] **Dashboard funcional** (7 pts)
- [ ] **Health checks** (5 pts)

#### Documentación (15 puntos)

- [ ] **README completo** (5 pts)
- [ ] **Reportes detallados** (5 pts)
- [ ] **Presentación clara** (5 pts)

---

## Guía de Implementación

### 🚦 Hitos del Proyecto

#### Semana 7 - Día 1-2: Análisis y Setup

- [ ] Configurar aplicación base con datos de prueba
- [ ] Implementar sistema de profiling
- [ ] Identificar problemas de performance
- [ ] Documentar estado inicial

#### Semana 7 - Día 3-4: Optimización

- [ ] Optimizar consultas de base de datos
- [ ] Implementar sistema de cache
- [ ] Configurar monitoreo básico
- [ ] Medir mejoras obtenidas

#### Semana 7 - Día 5-6: Monitoreo y Finalizacion

- [ ] Completar dashboard de monitoreo
- [ ] Implementar alertas
- [ ] Generar reportes finales
- [ ] Preparar presentación

### 💡 Tips de Implementación

#### Profiling Efectivo

```python
# Usar context managers para medición precisa
import time
import contextlib

@contextlib.contextmanager
def timer():
    start = time.perf_counter()
    yield
    end = time.perf_counter()
    print(f"Execution time: {end - start:.4f} seconds")

# Uso
with timer():
    result = expensive_operation()
```

#### Cache Inteligente

```python
# Implementar invalidación automática
def invalidate_related_cache(user_id: int):
    patterns = [
        f"user:{user_id}:*",
        f"posts:user:{user_id}:*",
        f"stats:user:{user_id}:*"
    ]
    for pattern in patterns:
        cache.delete_pattern(pattern)
```

#### Monitoreo Eficiente

```python
# Usar sampling para reducir overhead
import random

def should_monitor() -> bool:
    # Monitorear solo 10% de las requests
    return random.random() < 0.1
```

---

## Recursos de Apoyo

### 📚 Documentación Técnica

- [FastAPI Performance](https://fastapi.tiangolo.com/advanced/async-sql-databases/)
- [SQLAlchemy Performance](https://docs.sqlalchemy.org/en/14/orm/loading_techniques.html)
- [Redis Caching Patterns](https://redis.io/docs/manual/patterns/)
- [Prometheus Best Practices](https://prometheus.io/docs/practices/naming/)

### 🛠️ Herramientas Recomendadas

- **Profiling**: py-spy, line_profiler, memory_profiler
- **Load Testing**: locust, ab (Apache Bench)
- **Monitoring**: Prometheus, Grafana, Jaeger
- **Database**: pgAdmin, DataGrip

### 🎯 Ejemplos de Referencia

- [FastAPI Monitoring Example](https://github.com/prometheus/client_python)
- [Redis Caching Patterns](https://redislabs.com/redis-best-practices/)
- [SQLAlchemy Performance Tips](https://docs.sqlalchemy.org/en/14/orm/loading_techniques.html)

---

## Criterios de Entrega

### 📅 Fecha Límite

**Viernes de la Semana 7 - 23:59**

### 📦 Método de Entrega

1. **Repositorio GitHub** con código completo
2. **README.md** con instrucciones de instalación
3. **Video de demostración** (10 minutos máximo)
4. **Reportes** en formato Markdown o PDF

### ✅ Checklist Pre-entrega

- [ ] Código ejecuta sin errores
- [ ] Datos de prueba incluidos
- [ ] Docker Compose funciona
- [ ] Documentación completa
- [ ] Video de demostración grabado
- [ ] Reportes de performance incluidos

---

## Soporte y Consultas

### 💬 Canales de Comunicación

- **Discord**: Canal #semana7-performance
- **Office Hours**: Martes y Jueves 19:00-20:00
- **Email**: soporte@bootcamp.com

### 🆘 Problemas Comunes

1. **Docker no inicia**: Verificar puertos disponibles
2. **Redis connection error**: Confirmar configuración
3. **Queries muy lentas**: Verificar índices de BD
4. **Cache no funciona**: Revisar configuración TTL

¡Éxito en el desarrollo del proyecto! 🚀

---

_Esta especificación está diseñada para ser completada en el tiempo asignado de la Semana 7, con énfasis en aplicación práctica de conceptos de performance y monitoreo._
