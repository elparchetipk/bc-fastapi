# Fundamentos de Performance y Optimización

## 🎯 Objetivos de Aprendizaje

- Comprender conceptos fundamentales de performance en APIs web
- Identificar tipos de cuellos de botella y sus causas
- Conocer métricas clave y herramientas de medición
- Entender estrategias de optimización y escalabilidad

## ⏱️ Duración Estimada

**60 minutos**

---

## 📊 Conceptos Fundamentales de Performance

### ¿Qué es Performance en APIs?

La **performance** de una API se refiere a qué tan rápido y eficientemente puede procesar requests y devolver responses. No se trata solo de velocidad, sino de una combinación de factores:

#### Métricas Clave de Performance

**1. Latencia (Response Time)**

- Tiempo desde request hasta response completa
- Medida en milisegundos (ms)
- Target típico: <200ms para APIs REST

**2. Throughput (Rendimiento)**

- Número de requests procesadas por unidad de tiempo
- Medida en requests per second (RPS)
- Target típico: >1000 RPS para APIs simples

**3. Utilización de Recursos**

- CPU, memoria, red, almacenamiento
- Medida en porcentajes de capacidad
- Target típico: <70% bajo carga normal

**4. Escalabilidad**

- Capacidad de mantener performance al incrementar carga
- Horizontal (más servidores) vs Vertical (recursos por servidor)

**5. Disponibilidad**

- Porcentaje de tiempo que la API está operativa
- Target típico: 99.9% (8.77 horas downtime/año)

### Factores que Afectan Performance

#### 1. **Application Layer**

```python
# ❌ Código ineficiente
async def get_user_posts(user_id: int):
    user = await db.get_user(user_id)
    posts = []
    for post_id in user.post_ids:
        post = await db.get_post(post_id)  # N+1 query problem
        posts.append(post)
    return posts

# ✅ Código optimizado
async def get_user_posts(user_id: int):
    # Single query con JOIN
    posts = await db.query(
        select(Post).join(User).where(User.id == user_id)
    ).all()
    return posts
```

#### 2. **Database Layer**

- Queries sin optimizar
- Falta de índices apropiados
- Connection pooling inadecuado
- Transacciones largas

#### 3. **Network Layer**

- Latencia de red
- Ancho de banda limitado
- DNS resolution time
- SSL/TLS handshake overhead

#### 4. **Infrastructure Layer**

- CPU, memoria, I/O disk limitados
- Load balancing inefficiente
- Caching insuficiente
- Deployment configuration

---

## 🔍 Identificación de Cuellos de Botella

### Tipos Comunes de Bottlenecks

#### 1. **CPU-bound Operations**

```python
# Problema: Operaciones intensivas de CPU
import hashlib

def expensive_hash(data: str, iterations: int = 100000):
    for _ in range(iterations):
        data = hashlib.sha256(data.encode()).hexdigest()
    return data

# Solución: Async + multiprocessing
import asyncio
from concurrent.futures import ProcessPoolExecutor

async def optimized_hash(data: str, iterations: int = 100000):
    loop = asyncio.get_event_loop()
    with ProcessPoolExecutor() as executor:
        return await loop.run_in_executor(executor, expensive_hash, data, iterations)
```

#### 2. **I/O-bound Operations**

```python
# Problema: I/O sincrónico
import requests

def fetch_external_data(url: str):
    response = requests.get(url)  # Blocking I/O
    return response.json()

# Solución: I/O asíncrono
import httpx

async def fetch_external_data_async(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)  # Non-blocking I/O
        return response.json()
```

#### 3. **Memory-bound Operations**

```python
# Problema: Carga de datos masivos
async def get_all_users():
    users = await db.query(select(User)).all()  # Carga todo en memoria
    return users

# Solución: Paginación y streaming
async def get_users_paginated(page: int = 1, size: int = 100):
    offset = (page - 1) * size
    users = await db.query(
        select(User).offset(offset).limit(size)
    ).all()
    return users
```

#### 4. **Database Bottlenecks**

```sql
-- Problema: Query sin índice
SELECT * FROM posts WHERE created_at > '2024-01-01' ORDER BY created_at DESC;

-- Solución: Índice apropiado
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);
```

### Herramientas de Diagnóstico

#### 1. **Application Profiling**

```python
# cProfile - Profiling completo
import cProfile
import pstats

def profile_function():
    pr = cProfile.Profile()
    pr.enable()

    # Tu código aquí
    expensive_operation()

    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('cumulative')
    stats.print_stats(10)

# line_profiler - Profiling línea por línea
# Requiere: pip install line_profiler
@profile
def expensive_function():
    # Cada línea será analizada
    data = fetch_data()
    processed = process_data(data)
    return save_results(processed)
```

#### 2. **Memory Profiling**

```python
# memory_profiler
from memory_profiler import profile

@profile
def memory_intensive_function():
    # Analiza uso de memoria línea por línea
    big_list = [i for i in range(1000000)]
    return sum(big_list)

# py-spy - Profiling en producción sin modificar código
# pip install py-spy
# py-spy record -o profile.svg -p <PID>
```

#### 3. **Database Query Analysis**

```python
# SQLAlchemy query profiling
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Esto mostrará todas las queries ejecutadas
async def analyze_queries():
    users = await db.query(select(User)).all()
    # Verás la query exacta en logs
```

---

## 📈 Estrategias de Optimización

### 1. **Code-level Optimizations**

#### Async/Await Effectiveness

```python
# ❌ Secuencial (lento)
async def get_user_data(user_id: int):
    user = await get_user(user_id)          # 100ms
    posts = await get_user_posts(user_id)   # 150ms
    friends = await get_user_friends(user_id) # 80ms
    return {"user": user, "posts": posts, "friends": friends}
    # Total: 330ms

# ✅ Concurrente (rápido)
async def get_user_data_optimized(user_id: int):
    user_task = get_user(user_id)
    posts_task = get_user_posts(user_id)
    friends_task = get_user_friends(user_id)

    user, posts, friends = await asyncio.gather(
        user_task, posts_task, friends_task
    )
    return {"user": user, "posts": posts, "friends": friends}
    # Total: 150ms (tiempo del más lento)
```

#### Efficient Data Structures

```python
# ❌ Lista para búsquedas
user_ids = [1, 2, 3, 4, 5, 1000, 2000]
if 1000 in user_ids:  # O(n) - lento para listas largas
    process_user()

# ✅ Set para búsquedas
user_ids = {1, 2, 3, 4, 5, 1000, 2000}
if 1000 in user_ids:  # O(1) - rápido siempre
    process_user()

# ❌ Multiple database calls
users = []
for user_id in user_ids:
    user = await db.get_user(user_id)
    users.append(user)

# ✅ Single query con WHERE IN
users = await db.query(
    select(User).where(User.id.in_(user_ids))
).all()
```

### 2. **Database Optimizations**

#### Query Optimization Patterns

```python
# ❌ N+1 Query Problem
async def get_posts_with_authors():
    posts = await db.query(select(Post)).all()
    for post in posts:
        post.author = await db.get_user(post.author_id)  # N queries
    return posts

# ✅ Eager Loading con JOIN
async def get_posts_with_authors_optimized():
    posts = await db.query(
        select(Post).options(joinedload(Post.author))
    ).all()
    return posts

# ✅ Batch Loading
async def get_posts_with_authors_batch():
    posts = await db.query(select(Post)).all()
    author_ids = [post.author_id for post in posts]
    authors = await db.query(
        select(User).where(User.id.in_(author_ids))
    ).all()

    # Create lookup dictionary
    authors_dict = {author.id: author for author in authors}

    # Assign authors to posts
    for post in posts:
        post.author = authors_dict[post.author_id]

    return posts
```

#### Indexing Strategies

```sql
-- Índices para queries comunes
CREATE INDEX idx_posts_author_created ON posts(author_id, created_at DESC);
CREATE INDEX idx_users_email_active ON users(email) WHERE is_active = true;
CREATE INDEX idx_posts_content_gin ON posts USING gin(to_tsvector('english', content));

-- Índice compuesto para ORDER BY + WHERE
CREATE INDEX idx_posts_status_created ON posts(status, created_at DESC);
```

### 3. **Caching Strategies**

#### Multi-tier Caching

```python
from functools import wraps
import redis
import json

# Application-level cache (in-memory)
cache = {}

# Redis cache (distributed)
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cached(ttl: int = 300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{hash((args, tuple(kwargs.items())))}"

            # Check application cache first
            if cache_key in cache:
                return cache[cache_key]

            # Check Redis cache
            redis_value = redis_client.get(cache_key)
            if redis_value:
                result = json.loads(redis_value)
                cache[cache_key] = result  # Store in app cache too
                return result

            # Execute function
            result = await func(*args, **kwargs)

            # Store in both caches
            cache[cache_key] = result
            redis_client.setex(cache_key, ttl, json.dumps(result))

            return result
        return wrapper
    return decorator

# Usage
@cached(ttl=600)  # Cache for 10 minutes
async def get_popular_posts():
    return await db.query(
        select(Post).order_by(Post.likes.desc()).limit(10)
    ).all()
```

#### HTTP Caching Headers

```python
from fastapi import Response
from datetime import datetime, timedelta

@app.get("/posts/{post_id}")
async def get_post(post_id: int, response: Response):
    post = await get_post_from_db(post_id)

    # Set cache headers
    response.headers["Cache-Control"] = "public, max-age=300"  # 5 minutes
    response.headers["ETag"] = f'"{post.updated_at.timestamp()}"'
    response.headers["Last-Modified"] = post.updated_at.strftime("%a, %d %b %Y %H:%M:%S GMT")

    return post
```

---

## 📊 Monitoring y Métricas

### Key Performance Indicators (KPIs)

#### Response Time Metrics

```python
import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            return result
        finally:
            end_time = time.time()
            duration = (end_time - start_time) * 1000  # Convert to milliseconds
            print(f"{func.__name__} took {duration:.2f}ms")
    return wrapper

@measure_time
async def api_endpoint():
    # Your endpoint logic
    pass
```

#### Custom Metrics with Prometheus

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
REQUEST_COUNT = Counter('app_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('app_request_duration_seconds', 'Request latency')
ACTIVE_CONNECTIONS = Gauge('app_active_connections', 'Active connections')

# Middleware para métricas automáticas
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()

    # Increment request counter
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()

    # Process request
    response = await call_next(request)

    # Record latency
    REQUEST_LATENCY.observe(time.time() - start_time)

    return response
```

### Structured Logging

```python
import structlog
import logging

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Usage in endpoints
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    logger.info("Fetching user", user_id=user_id, action="get_user")

    start_time = time.time()
    try:
        user = await db.get_user(user_id)
        logger.info(
            "User fetched successfully",
            user_id=user_id,
            duration=time.time() - start_time,
            status="success"
        )
        return user
    except Exception as e:
        logger.error(
            "Error fetching user",
            user_id=user_id,
            error=str(e),
            duration=time.time() - start_time,
            status="error"
        )
        raise
```

---

## 🚀 Estrategias de Escalabilidad

### Horizontal vs Vertical Scaling

#### Vertical Scaling (Scale Up)

- **Pros**: Simple, no cambios en código
- **Cons**: Límite máximo, single point of failure
- **Cuándo usar**: Cargas pequeñas a medianas

#### Horizontal Scaling (Scale Out)

- **Pros**: Escalabilidad casi infinita, fault tolerance
- **Cons**: Complejidad en arquitectura, estado distribuido
- **Cuándo usar**: Cargas grandes, alta disponibilidad

### Load Balancing Strategies

```python
# nginx.conf para load balancing
upstream fastapi_backend {
    least_conn;  # Algorithm: least_conn, ip_hash, round_robin
    server 127.0.0.1:8001 weight=3;
    server 127.0.0.1:8002 weight=3;
    server 127.0.0.1:8003 weight=2;
    server 127.0.0.1:8004 backup;  # Backup server
}

server {
    listen 80;
    location / {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### Database Scaling Patterns

```python
# Read Replicas
class DatabaseRouter:
    def __init__(self):
        self.write_db = create_engine("postgresql://master:5432/db")
        self.read_db = create_engine("postgresql://replica:5432/db")

    async def read_query(self, query):
        # Route read operations to replica
        async with self.read_db.begin() as conn:
            return await conn.execute(query)

    async def write_query(self, query):
        # Route write operations to master
        async with self.write_db.begin() as conn:
            return await conn.execute(query)

# Sharding (partitioning)
def get_shard(user_id: int, num_shards: int = 4):
    return user_id % num_shards

async def get_user_posts(user_id: int):
    shard = get_shard(user_id)
    db = get_database_shard(shard)
    return await db.query(
        select(Post).where(Post.user_id == user_id)
    ).all()
```

---

## 📋 Performance Testing Strategies

### Load Testing con Locust

```python
# locustfile.py
from locust import HttpUser, task, between
import random

class APIUser(HttpUser):
    wait_time = between(1, 3)  # Wait 1-3 seconds between requests

    def on_start(self):
        # Login and get token
        response = self.client.post("/auth/login", json={
            "username": "testuser",
            "password": "testpass"
        })
        self.token = response.json()["access_token"]
        self.client.headers.update({"Authorization": f"Bearer {self.token}"})

    @task(3)
    def get_posts(self):
        self.client.get("/posts/")

    @task(2)
    def get_user_profile(self):
        self.client.get("/users/me")

    @task(1)
    def create_post(self):
        self.client.post("/posts/", json={
            "title": f"Test Post {random.randint(1, 1000)}",
            "content": "This is a test post content"
        })

# Ejecutar: locust -f locustfile.py --host=http://localhost:8000
```

### Benchmarking con Apache Bench

```bash
# Test básico
ab -n 1000 -c 10 http://localhost:8000/health
# -n: número total de requests
# -c: concurrency level

# Test con autenticación
ab -n 1000 -c 10 -H "Authorization: Bearer <token>" http://localhost:8000/posts/

# Test con POST data
ab -n 100 -c 5 -p post_data.json -T application/json http://localhost:8000/posts/
```

---

## 🎯 Best Practices Summary

### Code Optimization

1. **Use async/await** para I/O operations
2. **Batch operations** instead of loops
3. **Choose appropriate data structures**
4. **Implement efficient algorithms**

### Database Optimization

1. **Add proper indexes** for common queries
2. **Use connection pooling**
3. **Optimize query patterns** (avoid N+1)
4. **Implement pagination** for large datasets

### Caching Strategy

1. **Cache at multiple levels** (app, Redis, HTTP)
2. **Cache expensive operations**
3. **Implement cache invalidation**
4. **Monitor cache hit rates**

### Monitoring & Observability

1. **Track key metrics** (latency, throughput, errors)
2. **Use structured logging**
3. **Set up alerts** for anomalies
4. **Regular performance testing**

### Scalability Planning

1. **Design for horizontal scaling**
2. **Implement load balancing**
3. **Plan database scaling strategy**
4. **Monitor resource utilization**

---

## 📚 Herramientas y Recursos

### Profiling Tools

- **cProfile**: Built-in Python profiler
- **py-spy**: Production profiling
- **line_profiler**: Line-by-line analysis
- **memory_profiler**: Memory usage analysis

### Load Testing Tools

- **Locust**: Python-based, programmable
- **Apache Bench (ab)**: Simple HTTP benchmarking
- **wrk**: Modern HTTP benchmarking tool
- **Artillery**: Node.js-based load testing

### Monitoring Tools

- **Prometheus**: Metrics collection
- **Grafana**: Visualization and dashboards
- **Jaeger**: Distributed tracing
- **Sentry**: Error tracking and performance

### Database Tools

- **pgAdmin**: PostgreSQL administration
- **Redis CLI**: Redis monitoring
- **EXPLAIN ANALYZE**: Query execution plans
- **pg_stat_statements**: PostgreSQL query statistics

---

_La optimización de performance es un proceso iterativo: medir, identificar, optimizar, validar, repetir. Siempre comienza midiendo el estado actual antes de optimizar._
