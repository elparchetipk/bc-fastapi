# Práctica 26: Redis y Caching Básico

⏰ **Tiempo:** 60 minutos _(simplificado)_  
📚 **Prerequisito:** Semanas 1-6 completadas  
🎯 **Objetivo:** Implementar caching básico con Redis para optimizar performance de endpoints críticos

## 📋 Contenido de la Práctica _(simplificado)_

### **Parte 1: Setup de Redis (20 min)**

1. **Instalación y configuración**
2. **Conexión desde FastAPI**
3. **Operaciones básicas**

### **Parte 2: Cache Básico (30 min)**

1. **Cache simple para endpoints frecuentes**
2. **Invalidación básica**
3. **Error handling sin Redis**

### **Parte 3: Testing de Performance (10 min)**

1. **Comparación básica con/sin cache**
2. **Verificación de funcionamiento**

---

## 🎯 Parte 1: Setup de Redis (25 min)

### 1.1 Instalación de Redis

#### **Opción 1: Docker (Recomendado)**

```bash
# Levantar Redis con Docker
docker run -d \
  --name redis-cache \
  -p 6379:6379 \
  --restart unless-stopped \
  redis:7-alpine

# Verificar que está corriendo
docker ps | grep redis
```

#### **Opción 2: Instalación Local**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install redis-server

# macOS
brew install redis

# Iniciar servicio
redis-server
```

#### **Verificar Instalación**

```bash
# Conectar al CLI de Redis
redis-cli

# Dentro del CLI, probar comandos básicos
127.0.0.1:6379> ping
PONG
127.0.0.1:6379> set test "Hello Redis"
OK
127.0.0.1:6379> get test
"Hello Redis"
127.0.0.1:6379> exit
```

### 1.2 Instalar Cliente Python

```bash
# Instalar dependencias
pip install redis python-json-logger

# Verificar instalación
python -c "import redis; print('Redis client installed successfully')"
```

### 1.3 Configuración en FastAPI

**Archivo: `app/core/cache.py`** (crear)

```python
"""
Redis cache configuration and utilities.
"""
import json
import logging
from typing import Optional, Any, Union
from datetime import timedelta

import redis
from redis.exceptions import RedisError

from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisCache:
    """Redis cache manager with error handling."""

    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self._connect()

    def _connect(self):
        """Establish Redis connection with error handling."""
        try:
            self.redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            # Test connection
            self.redis_client.ping()
            logger.info("Redis connection established successfully")
        except RedisError as e:
            logger.error(f"Redis connection failed: {e}")
            self.redis_client = None

    def is_available(self) -> bool:
        """Check if Redis is available."""
        if not self.redis_client:
            return False
        try:
            self.redis_client.ping()
            return True
        except RedisError:
            return False

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache with error handling."""
        if not self.is_available():
            return None

        try:
            value = self.redis_client.get(key)
            if value is None:
                return None
            return json.loads(value)
        except (RedisError, json.JSONDecodeError) as e:
            logger.error(f"Cache get error for key {key}: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache with TTL."""
        if not self.is_available():
            return False

        try:
            serialized_value = json.dumps(value, default=str)
            return bool(self.redis_client.setex(key, ttl, serialized_value))
        except (RedisError, TypeError) as e:
            logger.error(f"Cache set error for key {key}: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if not self.is_available():
            return False

        try:
            return bool(self.redis_client.delete(key))
        except RedisError as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False

    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern."""
        if not self.is_available():
            return 0

        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                return self.redis_client.delete(*keys)
            return 0
        except RedisError as e:
            logger.error(f"Cache delete pattern error for {pattern}: {e}")
            return 0

    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if not self.is_available():
            return False

        try:
            return bool(self.redis_client.exists(key))
        except RedisError:
            return False

    def increment(self, key: str, amount: int = 1) -> Optional[int]:
        """Increment a numeric value in cache."""
        if not self.is_available():
            return None

        try:
            return self.redis_client.incr(key, amount)
        except RedisError as e:
            logger.error(f"Cache increment error for key {key}: {e}")
            return None

    def get_stats(self) -> dict:
        """Get Redis statistics."""
        if not self.is_available():
            return {"status": "unavailable"}

        try:
            info = self.redis_client.info()
            return {
                "status": "available",
                "used_memory": info.get("used_memory_human", "unknown"),
                "connected_clients": info.get("connected_clients", 0),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(
                    info.get("keyspace_hits", 0),
                    info.get("keyspace_misses", 0)
                )
            }
        except RedisError as e:
            logger.error(f"Failed to get Redis stats: {e}")
            return {"status": "error", "error": str(e)}

    def _calculate_hit_rate(self, hits: int, misses: int) -> float:
        """Calculate cache hit rate percentage."""
        total = hits + misses
        if total == 0:
            return 0.0
        return round((hits / total) * 100, 2)

# Global cache instance
cache = RedisCache()
```

### 1.4 Configuración de Settings

**Archivo: `app/core/config.py`** (actualizar)

```python
# ...existing code...

class Settings(BaseSettings):
    # ...existing settings...

    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    # Cache Configuration
    cache_default_ttl: int = 300  # 5 minutes
    cache_user_ttl: int = 600     # 10 minutes
    cache_product_ttl: int = 1800  # 30 minutes

    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 🎯 Parte 2: Cache Patterns (40 min)

### 2.1 Cache-Aside Pattern

**Archivo: `app/services/user_service.py`** (actualizar)

```python
"""
User service with caching implementation.
"""
import logging
from typing import Optional, List
from sqlalchemy.orm import Session

from app.core.cache import cache
from app.core.config import settings
from app.models.user import User
from app.schemas.user import UserResponse

logger = logging.getLogger(__name__)

class UserService:
    """User service with caching support."""

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID with cache-aside pattern."""
        cache_key = f"user:{user_id}"

        # 1. Try to get from cache first
        cached_user = cache.get(cache_key)
        if cached_user:
            logger.info(f"Cache hit for user {user_id}")
            return User(**cached_user)  # Reconstruct User object

        logger.info(f"Cache miss for user {user_id}")

        # 2. If not in cache, get from database
        user = db.query(User).filter(User.id == user_id).first()

        # 3. If found, store in cache
        if user:
            user_dict = {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            cache.set(cache_key, user_dict, ttl=settings.cache_user_ttl)
            logger.info(f"User {user_id} cached successfully")

        return user

    @staticmethod
    def get_users_list(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users list with caching."""
        cache_key = f"users:list:{skip}:{limit}"

        # Check cache first
        cached_users = cache.get(cache_key)
        if cached_users:
            logger.info(f"Cache hit for users list (skip={skip}, limit={limit})")
            return [User(**user_data) for user_data in cached_users]

        logger.info(f"Cache miss for users list (skip={skip}, limit={limit})")

        # Get from database
        users = db.query(User).offset(skip).limit(limit).all()

        # Cache the results
        if users:
            users_data = [
                {
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "is_active": user.is_active,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                }
                for user in users
            ]
            cache.set(cache_key, users_data, ttl=settings.cache_default_ttl)
            logger.info(f"Users list cached (count={len(users)})")

        return users

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email with caching."""
        cache_key = f"user:email:{email}"

        cached_user = cache.get(cache_key)
        if cached_user:
            logger.info(f"Cache hit for user email {email}")
            return User(**cached_user)

        logger.info(f"Cache miss for user email {email}")

        user = db.query(User).filter(User.email == email).first()

        if user:
            user_dict = {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "is_active": user.is_active,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            cache.set(cache_key, user_dict, ttl=settings.cache_user_ttl)
            # Also cache by ID for consistency
            cache.set(f"user:{user.id}", user_dict, ttl=settings.cache_user_ttl)

        return user
```

### 2.2 Write-Through Pattern

**Archivo: `app/services/user_service.py`** (continuar)

```python
    @staticmethod
    def update_user(db: Session, user_id: int, user_update: dict) -> Optional[User]:
        """Update user with write-through caching."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return None

        # Update database
        for key, value in user_update.items():
            if hasattr(user, key):
                setattr(user, key, value)

        db.commit()
        db.refresh(user)

        # Update cache immediately (write-through)
        user_dict = {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }

        # Update multiple cache keys
        cache.set(f"user:{user.id}", user_dict, ttl=settings.cache_user_ttl)
        cache.set(f"user:email:{user.email}", user_dict, ttl=settings.cache_user_ttl)

        # Invalidate related caches (users lists)
        cache.delete_pattern("users:list:*")

        logger.info(f"User {user_id} updated and cache refreshed")
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """Delete user and invalidate cache."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False

        # Store email for cache invalidation
        user_email = user.email

        # Delete from database
        db.delete(user)
        db.commit()

        # Invalidate all related cache entries
        cache.delete(f"user:{user_id}")
        cache.delete(f"user:email:{user_email}")
        cache.delete_pattern("users:list:*")

        logger.info(f"User {user_id} deleted and cache invalidated")
        return True
```

### 2.3 Cache Decorator

**Archivo: `app/utils/cache_decorators.py`** (crear)

```python
"""
Cache decorators for automatic caching.
"""
import functools
import inspect
import logging
from typing import Callable, Any, Optional

from app.core.cache import cache

logger = logging.getLogger(__name__)

def cached(
    key_prefix: str,
    ttl: int = 300,
    key_builder: Optional[Callable] = None
):
    """
    Decorator to automatically cache function results.

    Args:
        key_prefix: Prefix for cache keys
        ttl: Time to live in seconds
        key_builder: Custom function to build cache key
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Build cache key
            if key_builder:
                cache_key = key_builder(*args, **kwargs)
            else:
                # Default key building
                sig = inspect.signature(func)
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()

                key_parts = [key_prefix]
                for param_name, param_value in bound_args.arguments.items():
                    if param_name != 'self' and param_name != 'db':  # Skip self and db session
                        key_parts.append(f"{param_name}:{param_value}")

                cache_key = ":".join(str(part) for part in key_parts)

            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.info(f"Cache hit for {func.__name__}: {cache_key}")
                return cached_result

            logger.info(f"Cache miss for {func.__name__}: {cache_key}")

            # Execute function
            result = func(*args, **kwargs)

            # Cache result if not None
            if result is not None:
                cache.set(cache_key, result, ttl=ttl)
                logger.info(f"Result cached for {func.__name__}: {cache_key}")

            return result

        return wrapper
    return decorator

def cache_invalidate(pattern: str):
    """
    Decorator to invalidate cache patterns after function execution.

    Args:
        pattern: Cache key pattern to invalidate
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)

            # Invalidate cache after successful execution
            invalidated_count = cache.delete_pattern(pattern)
            if invalidated_count > 0:
                logger.info(f"Invalidated {invalidated_count} cache entries with pattern: {pattern}")

            return result

        return wrapper
    return decorator

# Example usage
def build_product_key(product_id: int, *args, **kwargs) -> str:
    """Custom key builder for product cache."""
    return f"product:{product_id}"

@cached(key_prefix="expensive_calculation", ttl=1800)
def expensive_calculation(param1: str, param2: int) -> dict:
    """Example of cached expensive calculation."""
    # Simulate expensive operation
    import time
    time.sleep(2)

    return {
        "result": f"calculation_result_{param1}_{param2}",
        "timestamp": time.time()
    }
```

---

## 🎯 Parte 3: Performance Testing (25 min)

### 3.1 Endpoint con Caching

**Archivo: `app/routers/users.py`** (actualizar)

```python
# ...existing imports...
from app.core.cache import cache
from app.services.user_service import UserService

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user by ID with caching."""
    user = UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get users list with caching."""
    users = UserService.get_users_list(db, skip=skip, limit=limit)
    return users

@router.get("/cache/stats")
async def get_cache_stats(current_user: User = Depends(get_current_admin)):
    """Get cache statistics (admin only)."""
    return cache.get_stats()

@router.delete("/cache/clear")
async def clear_cache(
    pattern: str = Query("*", description="Pattern to clear (default: all)"),
    current_user: User = Depends(get_current_admin)
):
    """Clear cache by pattern (admin only)."""
    cleared_count = cache.delete_pattern(pattern)
    return {
        "message": f"Cleared {cleared_count} cache entries",
        "pattern": pattern
    }
```

### 3.2 Script de Benchmarking

**Archivo: `scripts/benchmark_cache.py`** (crear)

```python
"""
Benchmark script to test cache performance.
"""
import time
import asyncio
import statistics
from typing import List, Dict
import httpx

BASE_URL = "http://localhost:8000"
TEST_USER_ID = 1
NUM_REQUESTS = 100

async def make_request(client: httpx.AsyncClient, url: str, headers: dict) -> float:
    """Make a single request and return response time."""
    start_time = time.time()
    response = await client.get(url, headers=headers)
    end_time = time.time()

    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}")

    return end_time - start_time

async def benchmark_endpoint(
    url: str,
    headers: dict,
    num_requests: int = NUM_REQUESTS
) -> Dict[str, float]:
    """Benchmark an endpoint with multiple requests."""
    response_times = []

    async with httpx.AsyncClient() as client:
        # Warm-up request
        await make_request(client, url, headers)

        # Benchmark requests
        for i in range(num_requests):
            try:
                response_time = await make_request(client, url, headers)
                response_times.append(response_time)
                if i % 10 == 0:
                    print(f"Completed {i}/{num_requests} requests")
            except Exception as e:
                print(f"Request failed: {e}")

    # Calculate statistics
    return {
        "total_requests": len(response_times),
        "avg_response_time": statistics.mean(response_times),
        "median_response_time": statistics.median(response_times),
        "min_response_time": min(response_times),
        "max_response_time": max(response_times),
        "std_dev": statistics.stdev(response_times) if len(response_times) > 1 else 0
    }

async def main():
    """Run cache performance benchmark."""
    # Get auth token first
    auth_response = httpx.post(
        f"{BASE_URL}/auth/login",
        data={"username": "admin@example.com", "password": "admin123"}
    )

    if auth_response.status_code != 200:
        print("Failed to authenticate")
        return

    token = auth_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Clear cache before testing
    clear_response = httpx.delete(
        f"{BASE_URL}/cache/clear",
        headers=headers,
        params={"pattern": "*"}
    )
    print(f"Cache cleared: {clear_response.json()}")

    # Test endpoint without cache (cold start)
    print("\n=== Testing without cache (cold start) ===")
    url = f"{BASE_URL}/users/{TEST_USER_ID}"

    cold_stats = await benchmark_endpoint(url, headers, 1)
    print(f"Cold start time: {cold_stats['avg_response_time']:.4f} seconds")

    # Test endpoint with cache (warm cache)
    print("\n=== Testing with cache (warm cache) ===")
    warm_stats = await benchmark_endpoint(url, headers, NUM_REQUESTS)

    print(f"\nCache Performance Results:")
    print(f"Average response time: {warm_stats['avg_response_time']:.4f} seconds")
    print(f"Median response time: {warm_stats['median_response_time']:.4f} seconds")
    print(f"Min response time: {warm_stats['min_response_time']:.4f} seconds")
    print(f"Max response time: {warm_stats['max_response_time']:.4f} seconds")
    print(f"Standard deviation: {warm_stats['std_dev']:.4f} seconds")

    # Performance improvement
    improvement = ((cold_stats['avg_response_time'] - warm_stats['avg_response_time'])
                   / cold_stats['avg_response_time'] * 100)
    print(f"\nPerformance improvement: {improvement:.1f}%")

    # Get cache statistics
    cache_stats_response = httpx.get(f"{BASE_URL}/cache/stats", headers=headers)
    if cache_stats_response.status_code == 200:
        cache_stats = cache_stats_response.json()
        print(f"\nCache Statistics:")
        print(f"Hit rate: {cache_stats.get('hit_rate', 'N/A')}%")
        print(f"Memory used: {cache_stats.get('used_memory', 'N/A')}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 3.3 Ejecutar Benchmark

```bash
# Asegurarse de que la API está corriendo
uvicorn app.main:app --reload --port 8000

# En otra terminal, ejecutar el benchmark
cd scripts
python benchmark_cache.py
```

### 3.4 Análisis de Resultados

**Archivo: `scripts/cache_analysis.py`** (crear)

```python
"""
Analyze cache performance and generate report.
"""
import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

def analyze_cache_performance():
    """Analyze and visualize cache performance."""

    # Simulated benchmark results (replace with actual data)
    benchmark_data = {
        "without_cache": {
            "avg_response_time": 0.245,
            "median_response_time": 0.242,
            "min_response_time": 0.210,
            "max_response_time": 0.312
        },
        "with_cache": {
            "avg_response_time": 0.023,
            "median_response_time": 0.021,
            "min_response_time": 0.018,
            "max_response_time": 0.035
        }
    }

    # Calculate improvement
    without_cache = benchmark_data["without_cache"]["avg_response_time"]
    with_cache = benchmark_data["with_cache"]["avg_response_time"]
    improvement = ((without_cache - with_cache) / without_cache) * 100

    print("Cache Performance Analysis")
    print("=" * 40)
    print(f"Average response time without cache: {without_cache:.3f}s")
    print(f"Average response time with cache: {with_cache:.3f}s")
    print(f"Performance improvement: {improvement:.1f}%")
    print(f"Speed increase: {without_cache / with_cache:.1f}x faster")

    # Create visualization
    create_performance_chart(benchmark_data)

    # Cache hit rate analysis
    analyze_cache_hit_rate()

def create_performance_chart(data):
    """Create performance comparison chart."""
    categories = ['Without Cache', 'With Cache']
    avg_times = [
        data["without_cache"]["avg_response_time"],
        data["with_cache"]["avg_response_time"]
    ]

    plt.figure(figsize=(10, 6))

    # Create bar chart
    bars = plt.bar(categories, avg_times, color=['#ff6b6b', '#4ecdc4'])
    plt.ylabel('Response Time (seconds)')
    plt.title('Cache Performance Comparison')

    # Add value labels on bars
    for bar, time_val in zip(bars, avg_times):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                f'{time_val:.3f}s', ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('cache_performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.show()

def analyze_cache_hit_rate():
    """Analyze cache hit rate trends."""
    # Simulated hit rate data over time
    hours = list(range(24))
    hit_rates = [
        85, 87, 89, 91, 93, 94, 95, 96, 94, 92,
        90, 88, 86, 87, 89, 91, 93, 95, 96, 94,
        92, 90, 88, 86
    ]

    plt.figure(figsize=(12, 6))
    plt.plot(hours, hit_rates, marker='o', linewidth=2, markersize=4)
    plt.xlabel('Hour of Day')
    plt.ylabel('Cache Hit Rate (%)')
    plt.title('Cache Hit Rate Over 24 Hours')
    plt.grid(True, alpha=0.3)
    plt.ylim(80, 100)

    # Add average line
    avg_hit_rate = np.mean(hit_rates)
    plt.axhline(y=avg_hit_rate, color='r', linestyle='--', alpha=0.7,
                label=f'Average: {avg_hit_rate:.1f}%')
    plt.legend()

    plt.tight_layout()
    plt.savefig('cache_hit_rate_trend.png', dpi=300, bbox_inches='tight')
    plt.show()

    print(f"\nCache Hit Rate Analysis:")
    print(f"Average hit rate: {avg_hit_rate:.1f}%")
    print(f"Peak hit rate: {max(hit_rates)}%")
    print(f"Lowest hit rate: {min(hit_rates)}%")

if __name__ == "__main__":
    analyze_cache_performance()
```

---

## ✅ Checklist de Verificación

### **Redis Setup**

- [ ] Redis instalado y corriendo
- [ ] Cliente Python conectando correctamente
- [ ] Configuración en FastAPI funcionando
- [ ] Error handling implementado

### **Cache Patterns**

- [ ] Cache-aside pattern implementado
- [ ] Write-through pattern funcionando
- [ ] Cache invalidation correcta
- [ ] TTL configurado apropiadamente

### **Performance Testing**

- [ ] Benchmark script ejecutado
- [ ] Métricas de performance capturadas
- [ ] Comparación con/sin cache realizada
- [ ] Cache hit rate medido

### **Production Readiness**

- [ ] Graceful degradation sin Redis
- [ ] Logging de operaciones de cache
- [ ] Configuración externalizada
- [ ] Cache statistics endpoint

---

## 🚨 Troubleshooting Común

### **Error: "Connection refused to Redis"**

```bash
# Verificar que Redis está corriendo
docker ps | grep redis

# Si no está corriendo, iniciarlo
docker start redis-cache

# Verificar conectividad
redis-cli ping
```

### **Error: "JSON not serializable"**

```python
# Problema: Objetos datetime no son JSON serializable
# Solución: Convertir a string en el cache manager
serialized_value = json.dumps(value, default=str)
```

### **Cache no mejora performance**

```python
# Verificar que el cache hit rate es alto
cache_stats = cache.get_stats()
print(f"Hit rate: {cache_stats['hit_rate']}%")

# Si es bajo, revisar:
# 1. TTL muy corto
# 2. Cache keys inconsistentes
# 3. Patrones de invalidación muy agresivos
```

---

## 🎯 Puntos Clave

1. **Cache is not a silver bullet** - Úsalo estratégicamente
2. **Measure first** - Benchmark para validar mejoras
3. **Handle failures gracefully** - App debe funcionar sin cache
4. **Monitor hit rates** - >80% es una buena meta
5. **Appropriate TTL** - Balance entre freshness y performance

¡Continúa con la **Práctica 24: Database Performance Optimization**! 🚀
