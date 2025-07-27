# Conceptos de Performance y Optimización en APIs

📚 **Fundamentos de optimización para APIs en producción**  
⏰ **Tiempo de lectura:** 30-45 minutos  
🎯 **Objetivo:** Comprender los principios fundamentales de performance

---

## 🎯 ¿Qué es Performance en APIs?

### **Definición**

**Performance en APIs** se refiere a qué tan rápido y eficientemente una API puede procesar requests y devolver responses, mientras utiliza los recursos del sistema de manera óptima.

### **Métricas Clave**

1. **Response Time** (Tiempo de Respuesta)

   - Tiempo desde request hasta response completa
   - Meta típica: <200ms para operaciones CRUD básicas

2. **Throughput** (Rendimiento)

   - Requests procesados por segundo (RPS)
   - Meta típica: >1000 RPS para APIs bien optimizadas

3. **Resource Usage** (Uso de Recursos)

   - CPU, Memoria, Disk I/O, Network I/O
   - Eficiencia en el uso de recursos disponibles

4. **Availability** (Disponibilidad)
   - Uptime del servicio
   - Meta típica: 99.9% (8.77 horas down/año)

---

## ⚡ Principios de Optimización

### **1. Medir Antes de Optimizar**

```python
# Ejemplo: Profiling básico
import time
import functools

def timing_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def slow_endpoint():
    # Tu código aquí
    pass
```

### **2. Ley de Pareto (80/20)**

- **80% de los problemas** vienen del **20% del código**
- **Identifica bottlenecks** antes de optimizar
- **Prioriza optimizaciones** con mayor impacto

### **3. Optimización Prematura es Evil**

> "Premature optimization is the root of all evil" - Donald Knuth

- Primero funcionalidad, luego performance
- Optimiza solo bottlenecks identificados
- Mantén código legible y mantenible

---

## 🗂️ Estrategias de Caching

### **¿Qué es Caching?**

**Caching** es el proceso de almacenar datos frecuentemente accedidos en una ubicación de acceso rápido para reducir el tiempo de acceso en requests futuros.

### **Tipos de Cache**

#### **1. Application-Level Cache**

```python
# Cache en memoria simple
cache = {}

def get_user_cached(user_id: int):
    if user_id in cache:
        return cache[user_id]  # Cache hit

    user = database.get_user(user_id)  # Cache miss
    cache[user_id] = user
    return user
```

#### **2. Database Query Cache**

```python
# Con SQLAlchemy
from sqlalchemy.orm import sessionmaker

# Query cache automático
users = session.query(User).filter(User.active == True).all()
```

#### **3. External Cache (Redis)**

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_user_redis(user_id: int):
    # Intentar obtener del cache
    cached_user = redis_client.get(f"user:{user_id}")
    if cached_user:
        return json.loads(cached_user)

    # Si no está en cache, obtener de DB
    user = database.get_user(user_id)
    redis_client.setex(f"user:{user_id}", 300, json.dumps(user))  # TTL 5 min
    return user
```

### **Cache Patterns**

#### **1. Cache-Aside (Lazy Loading)**

```python
def get_product(product_id: int):
    # 1. Check cache first
    cached = redis_client.get(f"product:{product_id}")
    if cached:
        return json.loads(cached)

    # 2. If miss, load from database
    product = db.query(Product).filter(Product.id == product_id).first()

    # 3. Update cache
    if product:
        redis_client.setex(f"product:{product_id}", 600, json.dumps(product.dict()))

    return product
```

#### **2. Write-Through**

```python
def update_product(product_id: int, product_data: dict):
    # 1. Update database
    product = db.query(Product).filter(Product.id == product_id).first()
    for key, value in product_data.items():
        setattr(product, key, value)
    db.commit()

    # 2. Update cache immediately
    redis_client.setex(f"product:{product_id}", 600, json.dumps(product.dict()))

    return product
```

#### **3. Write-Behind (Write-Back)**

```python
# Cache se actualiza inmediatamente, DB se actualiza después
def update_product_writeback(product_id: int, product_data: dict):
    # 1. Update cache immediately
    redis_client.hset(f"product:{product_id}", mapping=product_data)

    # 2. Queue database update for later (background task)
    background_tasks.add_task(update_database, product_id, product_data)
```

### **Cache Invalidation**

```python
# Estrategias para invalidar cache
class CacheManager:
    def __init__(self):
        self.redis = redis.Redis()

    def invalidate_user_cache(self, user_id: int):
        """Invalidar cache específico de usuario"""
        self.redis.delete(f"user:{user_id}")

    def invalidate_pattern(self, pattern: str):
        """Invalidar múltiples keys por patrón"""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)

    def set_with_tags(self, key: str, value: str, tags: list, ttl: int = 300):
        """Cache con tags para invalidación grupal"""
        self.redis.setex(key, ttl, value)
        for tag in tags:
            self.redis.sadd(f"tag:{tag}", key)

    def invalidate_by_tag(self, tag: str):
        """Invalidar todos los caches con un tag específico"""
        keys = self.redis.smembers(f"tag:{tag}")
        if keys:
            self.redis.delete(*keys)
            self.redis.delete(f"tag:{tag}")
```

---

## 🗃️ Optimización de Base de Datos

### **1. Query Optimization**

#### **N+1 Problem**

```python
# ❌ Problema N+1 (1 query + N queries)
users = session.query(User).all()  # 1 query
for user in users:
    print(user.posts)  # N queries (una por cada user)

# ✅ Solución: Eager Loading
users = session.query(User).options(joinedload(User.posts)).all()  # 1 query
for user in users:
    print(user.posts)  # Sin queries adicionales
```

#### **Query Analysis con EXPLAIN**

```sql
-- Analizar performance de query
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'user@example.com';

-- Ejemplo de output:
-- Seq Scan on users (cost=0.00..25.00 rows=1000 width=32) (actual time=0.123..5.456 rows=1 loops=1)
--   Filter: (email = 'user@example.com'::text)
-- Planning Time: 0.234 ms
-- Execution Time: 5.678 ms
```

### **2. Database Indexes**

#### **Tipos de Índices**

```sql
-- Índice simple
CREATE INDEX idx_users_email ON users(email);

-- Índice compuesto
CREATE INDEX idx_users_status_created ON users(status, created_at);

-- Índice parcial
CREATE INDEX idx_active_users_email ON users(email) WHERE status = 'active';

-- Índice único
CREATE UNIQUE INDEX idx_users_email_unique ON users(email);
```

#### **Estrategias de Indexing**

```python
# En SQLAlchemy models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)  # Índice único
    status = Column(String, index=True)  # Índice simple
    created_at = Column(DateTime, index=True)

    # Índice compuesto
    __table_args__ = (
        Index('idx_user_status_created', 'status', 'created_at'),
        Index('idx_active_users', 'email', postgresql_where=Column('status') == 'active'),
    )
```

### **3. Connection Pooling**

```python
# Configuración de connection pool
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://user:pass@localhost/dbname",
    poolclass=QueuePool,
    pool_size=20,          # Conexiones en el pool
    max_overflow=30,       # Conexiones adicionales si es necesario
    pool_pre_ping=True,    # Verificar conexiones antes de usar
    pool_recycle=3600,     # Reciclar conexiones cada hora
)
```

### **4. Async Database Operations**

```python
# Operaciones asíncronas para mejor throughput
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

async_engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/dbname"
)

async def get_users_async(db: AsyncSession, limit: int = 100):
    result = await db.execute(
        select(User).limit(limit)
    )
    return result.scalars().all()

# Operaciones concurrentes
async def get_multiple_resources():
    async with AsyncSession(async_engine) as session:
        users_task = asyncio.create_task(get_users_async(session))
        products_task = asyncio.create_task(get_products_async(session))

        users, products = await asyncio.gather(users_task, products_task)
        return users, products
```

---

## 🛠️ Middleware para Performance

### **1. Rate Limiting**

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.get("/api/users")
@limiter.limit("10/minute")  # 10 requests por minuto
async def get_users(request: Request):
    return {"users": []}
```

### **2. Response Compression**

```python
from fastapi.middleware.gzip import GZipMiddleware

# Comprimir responses automáticamente
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### **3. Custom Performance Middleware**

```python
import time
from fastapi import Request, Response

@app.middleware("http")
async def performance_middleware(request: Request, call_next):
    start_time = time.time()

    # Procesar request
    response = await call_next(request)

    # Calcular tiempo de procesamiento
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    # Log performance metrics
    logger.info(f"{request.method} {request.url.path} - {process_time:.4f}s")

    return response
```

---

## 📊 Monitoring y Profiling

### **1. Structured Logging**

```python
import structlog

# Configurar structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="ISO"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.make_filtering_bound_logger(20),
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Uso en endpoints
@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    logger.info("fetching_user", user_id=user_id)

    try:
        user = await get_user_from_db(user_id)
        logger.info("user_fetched", user_id=user_id, execution_time=0.234)
        return user
    except Exception as e:
        logger.error("user_fetch_failed", user_id=user_id, error=str(e))
        raise
```

### **2. Performance Profiling**

```python
# Profiling con cProfile
import cProfile
import pstats

def profile_endpoint():
    profiler = cProfile.Profile()
    profiler.enable()

    # Tu código aquí
    result = expensive_operation()

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 funciones más lentas

    return result
```

### **3. Memory Profiling**

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    # Función que consume mucha memoria
    large_list = [i for i in range(1000000)]
    return large_list

# Uso: python -m memory_profiler script.py
```

### **4. Application Metrics**

```python
# Métricas básicas de aplicación
class MetricsCollector:
    def __init__(self):
        self.request_count = 0
        self.error_count = 0
        self.response_times = []

    def record_request(self, response_time: float, status_code: int):
        self.request_count += 1
        self.response_times.append(response_time)

        if status_code >= 400:
            self.error_count += 1

    def get_stats(self):
        avg_response_time = sum(self.response_times) / len(self.response_times)
        error_rate = (self.error_count / self.request_count) * 100

        return {
            "total_requests": self.request_count,
            "avg_response_time": avg_response_time,
            "error_rate": error_rate,
            "errors": self.error_count
        }

metrics = MetricsCollector()

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response_time = time.time() - start_time

    metrics.record_request(response_time, response.status_code)
    return response
```

---

## 🎯 Mejores Prácticas

### **1. Caching Guidelines**

- ✅ **Cache data that doesn't change frequently**
- ✅ **Set appropriate TTL** (Time To Live)
- ✅ **Handle cache failures gracefully**
- ✅ **Monitor cache hit/miss ratios**
- ❌ **Don't cache user-specific sensitive data**
- ❌ **Don't cache data that changes frequently**

### **2. Database Optimization**

- ✅ **Use indexes on frequently queried columns**
- ✅ **Avoid N+1 queries with eager loading**
- ✅ **Use connection pooling**
- ✅ **Analyze slow queries with EXPLAIN**
- ❌ **Don't over-index (impacts write performance)**
- ❌ **Don't fetch unnecessary columns**

### **3. API Design for Performance**

- ✅ **Implement pagination for large datasets**
- ✅ **Use appropriate HTTP status codes**
- ✅ **Compress responses when beneficial**
- ✅ **Implement proper error handling**
- ❌ **Don't return massive payloads**
- ❌ **Don't expose internal implementation details**

### **4. Monitoring and Alerting**

- ✅ **Log structured data for analysis**
- ✅ **Monitor key performance metrics**
- ✅ **Set up alerting for critical thresholds**
- ✅ **Profile production performance regularly**
- ❌ **Don't log sensitive information**
- ❌ **Don't ignore error patterns**

---

## 🚨 Performance Anti-Patterns

### **1. Over-Caching**

```python
# ❌ Bad: Cachear todo sin criterio
def bad_caching():
    cache.set("user_data", user_data, ttl=86400)  # 24 hours for sensitive data
    cache.set("random_number", random.random(), ttl=3600)  # Caching random data

# ✅ Good: Cache estratégico
def good_caching():
    # Solo cache datos costosos de obtener y que no cambian frecuentemente
    if not cache.exists("expensive_calculation"):
        result = expensive_database_aggregation()
        cache.set("expensive_calculation", result, ttl=1800)  # 30 min
```

### **2. Premature Optimization**

```python
# ❌ Bad: Optimizar sin medir
def premature_optimization():
    # Código complejo para "performance" sin evidencia de que sea necesario
    result = complex_algorithm_that_might_be_faster()

# ✅ Good: Medir primero, optimizar después
@timing_decorator
def measured_approach():
    # Implementación simple primero
    result = simple_algorithm()
    # Solo optimizar si el profiling muestra que es un bottleneck
```

### **3. Ignoring Database Performance**

```python
# ❌ Bad: Queries ineficientes
def bad_queries():
    users = session.query(User).all()  # Obtener todos los usuarios
    for user in users:
        if user.status == 'active':  # Filtrar en Python
            print(user.email)

# ✅ Good: Queries optimizadas
def good_queries():
    active_users = session.query(User).filter(User.status == 'active').all()
    for user in active_users:
        print(user.email)
```

---

## 🎓 Próximos Pasos

Después de dominar estos conceptos fundamentales:

1. **Implementa caching** en tu API siguiendo los patrones aprendidos
2. **Optimiza tus queries** más lentas usando EXPLAIN
3. **Configura monitoring** básico para métricas clave
4. **Aplica middleware** para rate limiting y compresión
5. **Perfila tu aplicación** para identificar bottlenecks reales

¡En las prácticas implementaremos cada uno de estos conceptos de manera práctica! ⚡
