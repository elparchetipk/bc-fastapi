# Ejercicios Prácticos - Semana 7: Performance y Monitoreo

## Información General

### Objetivos de Aprendizaje

Al completar estos ejercicios, los estudiantes serán capaces de:

- Identificar y resolver problemas de rendimiento
- Implementar estrategias de optimización
- Configurar sistemas de monitoreo
- Aplicar técnicas de caching efectivas

### Estructura de Ejercicios

Cada ejercicio incluye:

- ✅ **Objetivos específicos**
- ⏱️ **Tiempo estimado**
- 📋 **Requisitos previos**
- 🔧 **Implementación paso a paso**
- 🧪 **Pruebas y validación**
- 📊 **Criterios de evaluación**

---

## Ejercicio 1: Análisis y Optimización de Rendimiento

### ✅ Objetivos

- Identificar cuellos de botella en aplicaciones FastAPI
- Aplicar técnicas de profiling
- Optimizar consultas de base de datos
- Medir mejoras de rendimiento

### ⏱️ Tiempo Estimado

**45 minutos**

### 📋 Requisitos Previos

- Aplicación FastAPI con base de datos
- Datos de prueba generados
- Conocimientos básicos de SQLAlchemy

### 🔧 Implementación

#### Paso 1: Configurar Profiling

```python
# Instalar dependencias necesarias
# pip install py-spy memory-profiler line-profiler

# app/profiling/profiler.py
import cProfile
import pstats
import io
from functools import wraps
import time

def profile_endpoint(func):
    """Decorador para perfilar endpoints"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()

        start_time = time.time()
        result = await func(*args, **kwargs)
        execution_time = time.time() - start_time

        pr.disable()

        # Generar reporte
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()

        print(f"Execution time: {execution_time:.4f}s")
        print("Top 10 functions by cumulative time:")
        ps.print_stats(10)

        return result
    return wrapper
```

#### Paso 2: Crear Endpoint Problemático

```python
# app/routers/performance_test.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Post, Comment
from app.profiling.profiler import profile_endpoint

router = APIRouter(prefix="/performance", tags=["performance"])

@router.get("/slow-endpoint")
@profile_endpoint
async def slow_endpoint(db: Session = Depends(get_db)):
    """Endpoint intencionalmente lento para demostrar problemas"""
    users = db.query(User).limit(50).all()
    result = []

    for user in users:
        # Problema N+1: Una query por usuario
        posts = db.query(Post).filter(Post.author_id == user.id).all()

        user_data = {
            "id": user.id,
            "username": user.username,
            "posts": []
        }

        for post in posts:
            # Otro problema N+1: Una query por post
            comments_count = db.query(Comment).filter(Comment.post_id == post.id).count()

            user_data["posts"].append({
                "id": post.id,
                "title": post.title,
                "comments_count": comments_count
            })

        result.append(user_data)

        # Simular procesamiento adicional innecesario
        time.sleep(0.01)  # 10ms por usuario

    return {"users": result, "total": len(result)}
```

#### Paso 3: Optimizar el Endpoint

```python
from sqlalchemy.orm import joinedload
from sqlalchemy import func

@router.get("/fast-endpoint")
@profile_endpoint
async def fast_endpoint(db: Session = Depends(get_db)):
    """Versión optimizada del endpoint"""
    # Single query with eager loading and aggregation
    users_data = db.query(
        User.id,
        User.username,
        func.count(Post.id).label('posts_count'),
        func.count(Comment.id).label('comments_count')
    )\
    .outerjoin(Post, User.id == Post.author_id)\
    .outerjoin(Comment, Post.id == Comment.post_id)\
    .group_by(User.id, User.username)\
    .limit(50)\
    .all()

    # Get detailed posts data separately if needed
    user_ids = [user.id for user in users_data]
    posts_data = db.query(Post)\
        .options(joinedload(Post.author))\
        .filter(Post.author_id.in_(user_ids))\
        .all()

    # Organize data efficiently
    posts_by_user = {}
    for post in posts_data:
        if post.author_id not in posts_by_user:
            posts_by_user[post.author_id] = []
        posts_by_user[post.author_id].append({
            "id": post.id,
            "title": post.title
        })

    result = []
    for user in users_data:
        result.append({
            "id": user.id,
            "username": user.username,
            "posts": posts_by_user.get(user.id, []),
            "posts_count": user.posts_count or 0,
            "comments_count": user.comments_count or 0
        })

    return {"users": result, "total": len(result)}
```

#### 🧪 Pruebas y Validación

1. Ejecuta ambos endpoints y compara los tiempos
2. Usa herramientas de profiling para identificar diferencias
3. Documenta las mejoras obtenidas

#### 📊 Criterios de Evaluación

- [ ] Implementaste profiling correctamente
- [ ] Identificaste problemas N+1
- [ ] Aplicaste optimizaciones efectivas
- [ ] Documentaste mejoras de rendimiento (mínimo 50% más rápido)

---

## Ejercicio 2: Implementación de Sistema de Cache

### ✅ Objetivos

- Configurar Redis para caching
- Implementar diferentes estrategias de cache
- Medir impacto en rendimiento
- Gestionar invalidación de cache

### ⏱️ Tiempo Estimado

**50 minutos**

### 📋 Requisitos Previos

- Redis instalado y configurado
- Conocimientos básicos de decoradores Python
- Aplicación con endpoints funcionando

### 🔧 Implementación

#### Paso 1: Configurar Cliente Redis

```python
# app/cache/redis_setup.py
import redis
import json
import pickle
from typing import Any, Optional

class CacheClient:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.client = redis.from_url(redis_url, decode_responses=False)

    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Guardar valor en cache"""
        try:
            # Intentar JSON primero
            serialized = json.dumps(value, default=str).encode()
        except (TypeError, ValueError):
            # Fallback a pickle
            serialized = pickle.dumps(value)

        return self.client.setex(key, ttl, serialized)

    def get(self, key: str) -> Optional[Any]:
        """Obtener valor del cache"""
        value = self.client.get(key)
        if value is None:
            return None

        try:
            return json.loads(value.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            return pickle.loads(value)

    def delete(self, key: str) -> bool:
        """Eliminar clave"""
        return self.client.delete(key) > 0

    def exists(self, key: str) -> bool:
        """Verificar existencia"""
        return self.client.exists(key) > 0

cache_client = CacheClient()
```

#### Paso 2: Crear Decorador de Cache

```python
# app/cache/decorators.py
import functools
import hashlib
from app.cache.redis_setup import cache_client

def cached(ttl: int = 300, key_prefix: str = ""):
    """Decorador para cachear resultados"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Generar clave única
            cache_key = generate_cache_key(func.__name__, args, kwargs, key_prefix)

            # Intentar obtener del cache
            cached_result = cache_client.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Ejecutar función y cachear
            result = await func(*args, **kwargs)
            cache_client.set(cache_key, result, ttl)
            return result

        # Agregar función de invalidación
        def invalidate(*args, **kwargs):
            cache_key = generate_cache_key(func.__name__, args, kwargs, key_prefix)
            cache_client.delete(cache_key)

        wrapper.invalidate = invalidate
        return wrapper
    return decorator

def generate_cache_key(func_name: str, args: tuple, kwargs: dict, prefix: str = "") -> str:
    """Generar clave única para cache"""
    key_parts = [func_name]

    # Agregar argumentos
    for arg in args[1:]:  # Saltar 'self' si existe
        if hasattr(arg, '__dict__'):
            key_parts.append(str(hash(str(arg.__dict__))))
        else:
            key_parts.append(str(arg))

    # Agregar kwargs
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}:{v}")

    key_string = ":".join(key_parts)
    key_hash = hashlib.md5(key_string.encode()).hexdigest()

    return f"{prefix}:{key_hash}" if prefix else key_hash
```

#### Paso 3: Implementar Cache en Endpoints

```python
# app/routers/cached_endpoints.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.cache.decorators import cached
import time

router = APIRouter(prefix="/cached", tags=["cached"])

@router.get("/users/{user_id}")
@cached(ttl=600, key_prefix="user")
async def get_user_cached(user_id: int, db: Session = Depends(get_db)):
    """Obtener usuario con cache"""
    start_time = time.time()

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    execution_time = time.time() - start_time

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "execution_time": execution_time,
        "cached": False  # Se actualiza automáticamente en cache hit
    }

@router.get("/stats/global")
@cached(ttl=900, key_prefix="stats")
async def get_global_stats(db: Session = Depends(get_db)):
    """Estadísticas globales con cache"""
    start_time = time.time()

    stats = db.query(
        func.count(User.id).label('total_users'),
        func.count(Post.id).label('total_posts'),
        func.count(Comment.id).label('total_comments')
    ).first()

    execution_time = time.time() - start_time

    return {
        "total_users": stats.total_users,
        "total_posts": stats.total_posts,
        "total_comments": stats.total_comments,
        "execution_time": execution_time,
        "cached": False
    }

@router.delete("/cache/user/{user_id}")
async def invalidate_user_cache(user_id: int):
    """Invalidar cache de usuario específico"""
    get_user_cached.invalidate(user_id, None)  # None para db session
    return {"message": f"Cache invalidated for user {user_id}"}
```

#### 🧪 Pruebas y Validación

1. Compara tiempos de respuesta con y sin cache
2. Verifica que la invalidación funciona correctamente
3. Monitorea el hit rate del cache

#### 📊 Criterios de Evaluación

- [ ] Configuraste Redis correctamente
- [ ] Implementaste decoradores de cache
- [ ] Aplicaste cache a endpoints apropiados
- [ ] Implementaste invalidación de cache
- [ ] Documentaste mejoras de rendimiento (hit rate >70%)

---

## Ejercicio 3: Sistema de Monitoreo Completo

### ✅ Objetivos

- Configurar métricas de aplicación
- Implementar health checks
- Crear dashboard de monitoreo
- Configurar alertas básicas

### ⏱️ Tiempo Estimado

**60 minutos**

### 📋 Requisitos Previos

- Conocimientos básicos de Prometheus
- Comprensión de métricas de aplicación
- JavaScript básico para dashboard

### 🔧 Implementación

#### Paso 1: Configurar Métricas

```python
# app/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, Info
import time
import psutil

# Métricas de aplicación
REQUEST_COUNT = Counter(
    'app_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'app_request_duration_seconds',
    'Request duration',
    ['method', 'endpoint']
)

ACTIVE_USERS = Gauge(
    'app_active_users',
    'Active users'
)

DATABASE_QUERY_COUNT = Counter(
    'app_database_queries_total',
    'Database queries',
    ['operation']
)

CACHE_OPERATIONS = Counter(
    'app_cache_operations_total',
    'Cache operations',
    ['operation', 'result']
)

APP_INFO = Info(
    'app_info',
    'Application information'
)

class MetricsCollector:
    def __init__(self):
        APP_INFO.info({
            'version': '1.0.0',
            'environment': 'development'
        })

    def track_request(self, method: str, endpoint: str, status: int, duration: float):
        """Registrar métricas de request"""
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).inc()

        REQUEST_DURATION.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)

    def track_database_query(self, operation: str):
        """Registrar query de base de datos"""
        DATABASE_QUERY_COUNT.labels(operation=operation).inc()

    def track_cache_operation(self, operation: str, result: str):
        """Registrar operación de cache"""
        CACHE_OPERATIONS.labels(operation=operation, result=result).inc()

    def update_system_metrics(self):
        """Actualizar métricas del sistema"""
        # Esta función se puede llamar periódicamente
        pass

metrics = MetricsCollector()
```

#### Paso 2: Middleware de Monitoreo

```python
# app/middleware/monitoring.py
from fastapi import Request, Response
import time
import uuid
from app.monitoring.metrics import metrics

async def monitoring_middleware(request: Request, call_next):
    """Middleware para capturar métricas automáticamente"""
    # Información de la request
    request_id = str(uuid.uuid4())
    start_time = time.time()
    method = request.method
    path = request.url.path

    # Agregar ID a request
    request.state.request_id = request_id

    status_code = 200
    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception as e:
        status_code = 500
        raise
    finally:
        # Calcular duración y registrar métricas
        duration = time.time() - start_time
        metrics.track_request(method, path, status_code, duration)

        # Agregar headers de monitoreo
        if 'response' in locals():
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Response-Time"] = f"{duration:.4f}"

    return response
```

#### Paso 3: Health Checks

```python
# app/routers/health.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.cache.redis_setup import cache_client
import time

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
async def basic_health():
    """Health check básico"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

@router.get("/detailed")
async def detailed_health(db: Session = Depends(get_db)):
    """Health check detallado"""
    checks = {}
    overall_status = "healthy"

    # Check database
    try:
        start_time = time.time()
        db.execute("SELECT 1")
        db_time = time.time() - start_time

        checks["database"] = {
            "status": "healthy",
            "response_time": f"{db_time:.4f}s"
        }
    except Exception as e:
        checks["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        overall_status = "unhealthy"

    # Check Redis
    try:
        start_time = time.time()
        cache_client.client.ping()
        cache_time = time.time() - start_time

        checks["cache"] = {
            "status": "healthy",
            "response_time": f"{cache_time:.4f}s"
        }
    except Exception as e:
        checks["cache"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        if overall_status == "healthy":
            overall_status = "degraded"

    # Check system resources
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    checks["system"] = {
        "memory_usage": f"{memory.percent:.1f}%",
        "disk_usage": f"{disk.percent:.1f}%",
        "cpu_usage": f"{psutil.cpu_percent(interval=1):.1f}%"
    }

    if memory.percent > 90 or disk.percent > 90:
        if overall_status == "healthy":
            overall_status = "degraded"

    return {
        "status": overall_status,
        "timestamp": time.time(),
        "checks": checks
    }

@router.get("/metrics")
async def get_metrics():
    """Endpoint para métricas de Prometheus"""
    from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
    from fastapi.responses import Response

    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
```

#### 🧪 Pruebas y Validación

1. Verifica que las métricas se generan correctamente
2. Prueba los health checks en diferentes escenarios
3. Confirma que el middleware captura todas las requests

#### 📊 Criterios de Evaluación

- [ ] Configuraste métricas de Prometheus
- [ ] Implementaste middleware de monitoreo
- [ ] Creaste health checks detallados
- [ ] Verificaste captura de métricas en tiempo real

---

## Evaluación General

### Rúbrica de Evaluación

| Criterio                     | Excelente (4)                                                     | Bueno (3)                                        | Satisfactorio (2)                            | Necesita Mejora (1)                 |
| ---------------------------- | ----------------------------------------------------------------- | ------------------------------------------------ | -------------------------------------------- | ----------------------------------- |
| **Profiling y Optimización** | Identifica y resuelve múltiples problemas, documenta mejoras >70% | Identifica problemas principales, mejoras 50-70% | Identifica algunos problemas, mejoras 30-50% | Profiling básico, mejoras <30%      |
| **Sistema de Cache**         | Implementa múltiples estrategias, hit rate >80%                   | Cache funcional, hit rate 60-80%                 | Cache básico, hit rate 40-60%                | Cache implementado pero ineficiente |
| **Monitoreo**                | Sistema completo con alertas y dashboard                          | Métricas y health checks completos               | Monitoreo básico funcional                   | Métricas básicas solamente          |
| **Calidad del Código**       | Código limpio, bien documentado, siguiendo estándares             | Código claro con documentación adecuada          | Código funcional con documentación básica    | Código funcional pero poco claro    |

### Entregables Esperados

#### 📁 Estructura de Archivos

```
ejercicios-semana7/
├── profiling/
│   ├── profiler.py
│   ├── performance_test.py
│   └── optimization_report.md
├── cache/
│   ├── redis_setup.py
│   ├── decorators.py
│   ├── cached_endpoints.py
│   └── cache_performance_report.md
├── monitoring/
│   ├── metrics.py
│   ├── monitoring_middleware.py
│   ├── health_checks.py
│   └── monitoring_report.md
└── README.md
```

#### 📊 Reportes Requeridos

1. **Reporte de Optimización**: Comparación antes/después con métricas
2. **Reporte de Cache**: Hit rates, mejoras de rendimiento, estrategias utilizadas
3. **Reporte de Monitoreo**: Métricas implementadas, health checks, observaciones

### 🚀 Desafíos Adicionales (Opcionales)

#### Desafío 1: Cache Inteligente

Implementa un sistema de cache que:

- Ajuste automáticamente TTL basado en frecuencia de acceso
- Implemente cache warming para datos críticos
- Maneje gracefully fallos de Redis

#### Desafío 2: Alertas Avanzadas

Crea un sistema de alertas que:

- Detecte patrones anómalos en el tráfico
- Envíe notificaciones por diferentes canales
- Implemente escalamiento automático de alertas

#### Desafío 3: Dashboard Interactivo

Desarrolla un dashboard que:

- Muestre métricas en tiempo real
- Permita filtrar por diferentes períodos
- Incluya gráficos de tendencias y comparaciones

---

## Recursos de Apoyo

### 📚 Documentación Recomendada

- [FastAPI Performance](https://fastapi.tiangolo.com/advanced/async-sql-databases/)
- [Redis Caching Patterns](https://redis.io/docs/manual/patterns/)
- [Prometheus Metrics](https://prometheus.io/docs/concepts/metric_types/)

### 🛠️ Herramientas Útiles

- **py-spy**: Profiling en producción
- **memory-profiler**: Análisis de memoria
- **redis-cli**: Debugging de cache
- **htop**: Monitoreo de sistema

### 💡 Tips de Debugging

- Usa `EXPLAIN ANALYZE` para optimizar queries SQL
- Monitorea conexiones de base de datos con `pg_stat_activity`
- Utiliza `redis-cli monitor` para debug de cache
- Configura logging apropiado para cada componente

¡Éxito en los ejercicios! Recuerda que la optimización es un proceso iterativo. 🚀
