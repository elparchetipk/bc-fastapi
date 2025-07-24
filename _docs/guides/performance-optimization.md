# Performance & Optimization Guide - Bootcamp bc-fastapi

## 🚀 Fundamentos de Performance

### Métricas Clave de Performance

#### Response Time Targets

```python
# Establecer targets claros para diferentes tipos de endpoints
PERFORMANCE_TARGETS = {
    "simple_get": 100,      # ms - Consultas simples
    "complex_query": 500,   # ms - Queries complejas
    "file_upload": 2000,    # ms - Uploads de archivos
    "auth_endpoint": 200,   # ms - Autenticación
    "health_check": 50      # ms - Health checks
}
```

#### Database Performance Monitoring

```python
import time
from functools import wraps

def monitor_db_performance(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        execution_time = (time.time() - start_time) * 1000  # ms

        if execution_time > 1000:  # Log slow queries
            logger.warning(f"Slow query detected: {func.__name__} took {execution_time:.2f}ms")

        return result
    return wrapper

@monitor_db_performance
async def get_user_with_posts(user_id: int):
    # Implementation with proper joins instead of N+1 queries
    pass
```

## 🛠️ Optimization Techniques

### 1. Database Optimization

#### Avoiding N+1 Queries

```python
# ❌ N+1 Query Problem
async def get_users_with_posts_bad():
    users = await session.execute(select(User))
    for user in users:
        # This creates N additional queries!
        user.posts = await session.execute(
            select(Post).where(Post.user_id == user.id)
        )
    return users

# ✅ Optimized with Joins
async def get_users_with_posts_optimized():
    return await session.execute(
        select(User)
        .options(selectinload(User.posts))  # Eager loading
    ).scalars().all()
```

#### Connection Pooling

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# Optimized connection pool
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,          # Base number of connections
    max_overflow=0,        # Additional connections
    pool_pre_ping=True,    # Validate connections
    pool_recycle=3600      # Recycle connections after 1 hour
)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
```

### 2. Caching Strategies

#### Redis Implementation

```python
import redis.asyncio as redis
from typing import Optional, Any
import json
import pickle

class CacheService:
    def __init__(self, redis_url: str):
        self.redis = redis.from_url(redis_url)

    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return pickle.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600):
        try:
            serialized = json.dumps(value)
        except (TypeError, ValueError):
            serialized = pickle.dumps(value)

        await self.redis.setex(key, ttl, serialized)

    async def delete(self, key: str):
        await self.redis.delete(key)

# Usage in endpoints
cache = CacheService("redis://localhost:6379")

@app.get("/api/users/{user_id}")
async def get_user(user_id: int):
    cache_key = f"user:{user_id}"

    # Try cache first
    cached_user = await cache.get(cache_key)
    if cached_user:
        return cached_user

    # Fallback to database
    user = await database.get_user(user_id)
    if user:
        await cache.set(cache_key, user.dict(), ttl=1800)  # 30 minutes

    return user
```

#### Application-Level Caching

```python
from functools import lru_cache
from typing import List
import asyncio

# For CPU-intensive computations
@lru_cache(maxsize=1000)
def expensive_calculation(data: str) -> str:
    # Simulate expensive computation
    return data.upper().replace(" ", "_")

# For async operations (manual cache)
_async_cache = {}

async def cached_external_api_call(endpoint: str) -> dict:
    if endpoint in _async_cache:
        return _async_cache[endpoint]

    # Simulate API call
    await asyncio.sleep(0.5)
    result = {"data": f"Response from {endpoint}"}

    _async_cache[endpoint] = result
    return result
```

### 3. Async Optimization

#### Concurrent Operations

```python
import asyncio
from typing import List

async def process_multiple_users(user_ids: List[int]):
    # ❌ Sequential processing (slow)
    results = []
    for user_id in user_ids:
        user = await get_user(user_id)
        results.append(user)
    return results

async def process_multiple_users_optimized(user_ids: List[int]):
    # ✅ Concurrent processing (fast)
    tasks = [get_user(user_id) for user_id in user_ids]
    return await asyncio.gather(*tasks)

# Batch operations
async def batch_create_users(users_data: List[dict]):
    # Process in batches to avoid overwhelming the database
    batch_size = 10
    results = []

    for i in range(0, len(users_data), batch_size):
        batch = users_data[i:i + batch_size]
        batch_tasks = [create_user(user_data) for user_data in batch]
        batch_results = await asyncio.gather(*batch_tasks)
        results.extend(batch_results)

        # Small delay between batches to prevent overload
        await asyncio.sleep(0.1)

    return results
```

## 📊 Monitoring & Profiling

### Performance Middleware

```python
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        # Log slow requests
        if process_time > 1.0:  # More than 1 second
            logger.warning(
                f"Slow request: {request.method} {request.url.path} "
                f"took {process_time:.2f}s"
            )

        return response

app.add_middleware(PerformanceMiddleware)
```

### Memory Profiling

```python
import psutil
import gc
from fastapi import BackgroundTasks

def log_memory_usage():
    process = psutil.Process()
    memory_info = process.memory_info()

    logger.info(
        f"Memory usage: RSS={memory_info.rss / 1024 / 1024:.2f}MB "
        f"VMS={memory_info.vms / 1024 / 1024:.2f}MB"
    )

@app.get("/admin/memory-status")
async def memory_status():
    process = psutil.Process()
    memory_info = process.memory_info()

    return {
        "rss_mb": memory_info.rss / 1024 / 1024,
        "vms_mb": memory_info.vms / 1024 / 1024,
        "cpu_percent": process.cpu_percent(),
        "gc_counts": gc.get_count()
    }
```

## 🔧 Optimization Tools

### Load Testing with locust

```python
# locustfile.py
from locust import HttpUser, task, between

class ApiUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Login and get token
        response = self.client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "testpass123"
        })
        self.token = response.json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task(3)
    def get_users(self):
        self.client.get("/api/users", headers=self.headers)

    @task(2)
    def get_user_profile(self):
        self.client.get("/api/users/1", headers=self.headers)

    @task(1)
    def create_post(self):
        self.client.post("/api/posts",
                        headers=self.headers,
                        json={"title": "Test Post", "content": "Content"})
```

### APM Integration (Application Performance Monitoring)

```python
# Elastic APM integration
from elasticapm.contrib.starlette import make_apm_client, ElasticAPM

apm_config = {
    'SERVICE_NAME': 'bc-fastapi',
    'SECRET_TOKEN': 'your-secret-token',
    'SERVER_URL': 'http://localhost:8200',
    'ENVIRONMENT': 'production',
}

apm = make_apm_client(apm_config)
app.add_middleware(ElasticAPM, client=apm)

# Custom performance tracking
@apm.capture_span('database-query')
async def expensive_database_operation():
    # Your database operation
    pass
```

## 📈 Implementation Roadmap

### Semana 7: Performance Basics

- Response time monitoring
- Basic caching with in-memory
- Database query optimization
- N+1 query identification and fixes

### Semana 8: Advanced Optimization

- Redis caching implementation
- Connection pooling optimization
- Async operation optimization
- Memory profiling introduction

### Semana 9: Monitoring & Profiling

- APM tools integration
- Custom performance middleware
- Load testing with locust
- Performance regression testing

### Semana 10-12: Production Performance

- Auto-scaling strategies
- Performance budgets in CI/CD
- Real-time monitoring alerts
- Performance optimization as part of code review

## ⚡ Performance Checklist

### Database Performance

- [ ] Indexes on frequently queried columns
- [ ] No N+1 query patterns
- [ ] Connection pooling configured
- [ ] Query execution time monitoring
- [ ] Database query plan analysis

### Application Performance

- [ ] Response time targets defined
- [ ] Caching strategy implemented
- [ ] Async operations optimized
- [ ] Memory usage monitored
- [ ] CPU profiling configured

### Infrastructure Performance

- [ ] Load balancing configured
- [ ] CDN for static assets
- [ ] Compression enabled (gzip)
- [ ] HTTP/2 support
- [ ] Resource limits set

### Monitoring & Alerting

- [ ] Performance metrics dashboard
- [ ] Slow query alerts
- [ ] Memory usage alerts
- [ ] Error rate monitoring
- [ ] Performance regression detection

## 🎯 Performance Targets

### Development Environment

- API response time: < 200ms (95th percentile)
- Database query time: < 100ms average
- Memory usage: < 512MB baseline
- CPU usage: < 50% under normal load

### Production Environment

- API response time: < 100ms (95th percentile)
- Database query time: < 50ms average
- Memory usage: < 1GB baseline
- CPU usage: < 30% under normal load
- Uptime: > 99.9%
