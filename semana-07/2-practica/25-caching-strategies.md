# Práctica 25: Estrategias de Caching

## Objetivo

Implementar diferentes estrategias de caching para mejorar significativamente el rendimiento de aplicaciones FastAPI.

## Duración Estimada

⏱️ **75 minutos**

- Preparación: 15 minutos
- Implementación: 45 minutos
- Pruebas y optimización: 15 minutos

## Requisitos Previos

- Conocimientos de Redis básico
- Configuración de base de datos (Semana 4)
- Comprensión de serialización/deserialización

## Conceptos Teóricos

### 1. Tipos de Cache

- **In-Memory Cache**: Cache en memoria de la aplicación
- **Distributed Cache**: Cache distribuido (Redis)
- **Database Query Cache**: Cache de consultas de BD
- **HTTP Response Cache**: Cache de respuestas HTTP

### 2. Estrategias de Cache

- **Cache-Aside**: La aplicación gestiona el cache
- **Write-Through**: Escribir en cache y BD simultáneamente
- **Write-Behind**: Escribir en cache primero, BD después
- **Refresh-Ahead**: Refrescar cache antes de expiración

### 3. Patrones de Invalidación

- **TTL (Time To Live)**: Expiración por tiempo
- **Event-based**: Invalidación por eventos
- **Manual**: Invalidación explícita

## Implementación

### Paso 1: Configuración de Redis

Primero, configuremos Redis como nuestro cache distribuido:

```python
# app/cache/redis_client.py
import redis
import json
import pickle
from typing import Any, Optional
from datetime import timedelta
import asyncio
import aioredis
from app.config import settings

class RedisCache:
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self._client = None
        self._async_client = None

    @property
    def client(self):
        """Cliente Redis síncrono"""
        if self._client is None:
            self._client = redis.from_url(self.redis_url, decode_responses=True)
        return self._client

    @property
    async def async_client(self):
        """Cliente Redis asíncrono"""
        if self._async_client is None:
            self._async_client = aioredis.from_url(self.redis_url)
        return self._async_client

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Guardar valor en cache"""
        try:
            serialized_value = json.dumps(value, default=str)
            if ttl:
                return self.client.setex(key, ttl, serialized_value)
            else:
                return self.client.set(key, serialized_value)
        except (TypeError, ValueError):
            # Fallback a pickle para objetos complejos
            serialized_value = pickle.dumps(value)
            if ttl:
                return self.client.setex(key, ttl, serialized_value)
            else:
                return self.client.set(key, serialized_value)

    def get(self, key: str) -> Optional[Any]:
        """Obtener valor del cache"""
        value = self.client.get(key)
        if value is None:
            return None

        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            # Intentar deserializar con pickle
            try:
                return pickle.loads(value)
            except:
                return value

    async def aset(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Guardar valor en cache (asíncrono)"""
        client = await self.async_client
        try:
            serialized_value = json.dumps(value, default=str)
            if ttl:
                return await client.setex(key, ttl, serialized_value)
            else:
                return await client.set(key, serialized_value)
        except (TypeError, ValueError):
            serialized_value = pickle.dumps(value)
            if ttl:
                return await client.setex(key, ttl, serialized_value)
            else:
                return await client.set(key, serialized_value)

    async def aget(self, key: str) -> Optional[Any]:
        """Obtener valor del cache (asíncrono)"""
        client = await self.async_client
        value = await client.get(key)
        if value is None:
            return None

        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            try:
                return pickle.loads(value)
            except:
                return value

    def delete(self, key: str) -> bool:
        """Eliminar clave del cache"""
        return self.client.delete(key) > 0

    async def adelete(self, key: str) -> bool:
        """Eliminar clave del cache (asíncrono)"""
        client = await self.async_client
        return await client.delete(key) > 0

    def exists(self, key: str) -> bool:
        """Verificar si existe una clave"""
        return self.client.exists(key) > 0

    def flush_pattern(self, pattern: str) -> int:
        """Eliminar todas las claves que coincidan con un patrón"""
        keys = self.client.keys(pattern)
        if keys:
            return self.client.delete(*keys)
        return 0

# Instancia global del cache
cache = RedisCache()
```

### Paso 2: Decoradores de Cache

Creemos decoradores para simplificar el uso del cache:

```python
# app/cache/decorators.py
import functools
import hashlib
import inspect
from typing import Callable, Any, Optional
from app.cache.redis_client import cache

def generate_cache_key(func_name: str, args: tuple, kwargs: dict) -> str:
    """Generar clave única para el cache"""
    # Crear string único basado en función y argumentos
    key_parts = [func_name]

    # Agregar argumentos posicionales
    for arg in args:
        if hasattr(arg, '__dict__'):
            # Para objetos complejos, usar su representación
            key_parts.append(str(hash(str(arg.__dict__))))
        else:
            key_parts.append(str(arg))

    # Agregar argumentos con nombre
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}:{v}")

    # Crear hash para evitar claves muy largas
    key_string = ":".join(key_parts)
    return f"cache:{hashlib.md5(key_string.encode()).hexdigest()}"

def cached(ttl: int = 300, key_prefix: str = ""):
    """
    Decorador para cachear resultados de funciones

    Args:
        ttl: Tiempo de vida en segundos
        key_prefix: Prefijo adicional para la clave
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Generar clave de cache
            base_key = generate_cache_key(func.__name__, args, kwargs)
            cache_key = f"{key_prefix}:{base_key}" if key_prefix else base_key

            # Intentar obtener del cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                return cached_result

            # Ejecutar función y cachear resultado
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result

        # Agregar método para invalidar cache
        def invalidate(*args, **kwargs):
            base_key = generate_cache_key(func.__name__, args, kwargs)
            cache_key = f"{key_prefix}:{base_key}" if key_prefix else base_key
            cache.delete(cache_key)

        wrapper.invalidate = invalidate
        wrapper.cache_key_generator = lambda *args, **kwargs: (
            f"{key_prefix}:{generate_cache_key(func.__name__, args, kwargs)}"
            if key_prefix else generate_cache_key(func.__name__, args, kwargs)
        )

        return wrapper
    return decorator

def async_cached(ttl: int = 300, key_prefix: str = ""):
    """Decorador para cachear funciones asíncronas"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            base_key = generate_cache_key(func.__name__, args, kwargs)
            cache_key = f"{key_prefix}:{base_key}" if key_prefix else base_key

            cached_result = await cache.aget(cache_key)
            if cached_result is not None:
                return cached_result

            result = await func(*args, **kwargs)
            await cache.aset(cache_key, result, ttl)
            return result

        async def invalidate(*args, **kwargs):
            base_key = generate_cache_key(func.__name__, args, kwargs)
            cache_key = f"{key_prefix}:{base_key}" if key_prefix else base_key
            await cache.adelete(cache_key)

        wrapper.invalidate = invalidate
        return wrapper
    return decorator
```

### Paso 3: Cache de Consultas de Base de Datos

Implementemos cache específico para consultas de BD:

```python
# app/cache/database_cache.py
from sqlalchemy.orm import Session
from app.cache.decorators import cached
from app.models import User, Post
from typing import List, Optional
import json

class DatabaseCache:

    @staticmethod
    @cached(ttl=600, key_prefix="user")
    def get_user_by_id(db: Session, user_id: int) -> Optional[dict]:
        """Cache de usuario por ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "created_at": user.created_at.isoformat()
            }
        return None

    @staticmethod
    @cached(ttl=300, key_prefix="posts")
    def get_user_posts(db: Session, user_id: int, limit: int = 10) -> List[dict]:
        """Cache de posts de usuario"""
        posts = db.query(Post)\
            .filter(Post.author_id == user_id)\
            .order_by(Post.created_at.desc())\
            .limit(limit)\
            .all()

        return [
            {
                "id": post.id,
                "title": post.title,
                "content": post.content[:200],  # Solo preview
                "created_at": post.created_at.isoformat()
            }
            for post in posts
        ]

    @staticmethod
    @cached(ttl=900, key_prefix="stats")
    def get_user_stats(db: Session, user_id: int) -> dict:
        """Cache de estadísticas de usuario"""
        from sqlalchemy import func

        stats = db.query(
            func.count(Post.id).label('posts_count'),
            func.count(Comment.id).label('comments_count')
        )\
        .outerjoin(Post, Post.author_id == user_id)\
        .outerjoin(Comment, Comment.author_id == user_id)\
        .first()

        return {
            "posts_count": stats.posts_count or 0,
            "comments_count": stats.comments_count or 0
        }

    @staticmethod
    def invalidate_user_cache(user_id: int):
        """Invalidar todo el cache relacionado con un usuario"""
        # Invalidar cache directo
        DatabaseCache.get_user_by_id.invalidate(None, user_id)
        DatabaseCache.get_user_posts.invalidate(None, user_id)
        DatabaseCache.get_user_stats.invalidate(None, user_id)

        # Invalidar patrones relacionados
        cache.flush_pattern(f"user:*:{user_id}:*")
        cache.flush_pattern(f"posts:*:{user_id}:*")
        cache.flush_pattern(f"stats:*:{user_id}:*")
```

### Paso 4: Cache de Respuestas HTTP

Implementemos cache a nivel de respuesta HTTP:

```python
# app/cache/response_cache.py
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import json
import hashlib
from app.cache.redis_client import cache

class ResponseCache:

    @staticmethod
    def generate_request_key(request: Request) -> str:
        """Generar clave única para una request"""
        # Combinar método, URL y parámetros
        key_parts = [
            request.method,
            str(request.url),
            json.dumps(dict(request.query_params), sort_keys=True)
        ]

        # Agregar headers relevantes si es necesario
        if request.headers.get("authorization"):
            # Hash del token para incluir usuario sin exponer datos
            auth_hash = hashlib.md5(
                request.headers["authorization"].encode()
            ).hexdigest()[:8]
            key_parts.append(auth_hash)

        key_string = ":".join(key_parts)
        return f"response:{hashlib.md5(key_string.encode()).hexdigest()}"

    @staticmethod
    async def get_cached_response(request: Request) -> Optional[dict]:
        """Obtener respuesta cacheada"""
        cache_key = ResponseCache.generate_request_key(request)
        return await cache.aget(cache_key)

    @staticmethod
    async def cache_response(
        request: Request,
        response_data: dict,
        ttl: int = 300
    ) -> bool:
        """Cachear respuesta"""
        cache_key = ResponseCache.generate_request_key(request)
        return await cache.aset(cache_key, response_data, ttl)

def cache_response(ttl: int = 300):
    """Decorador para cachear respuestas HTTP"""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Intentar obtener respuesta cacheada
            cached_response = await ResponseCache.get_cached_response(request)
            if cached_response:
                return JSONResponse(content=cached_response)

            # Ejecutar función original
            response = await func(request, *args, **kwargs)

            # Cachear respuesta si es exitosa
            if isinstance(response, (dict, list)):
                await ResponseCache.cache_response(request, response, ttl)
                return JSONResponse(content=response)
            elif hasattr(response, 'body') and response.status_code == 200:
                try:
                    response_data = json.loads(response.body)
                    await ResponseCache.cache_response(request, response_data, ttl)
                except:
                    pass  # No cachear si no se puede serializar

            return response
        return wrapper
    return decorator
```

### Paso 5: Middleware de Cache

Creemos un middleware para aplicar cache automáticamente:

```python
# app/middleware/cache_middleware.py
from fastapi import Request, Response
from fastapi.responses import JSONResponse
import time
import json
from app.cache.response_cache import ResponseCache

async def cache_middleware(request: Request, call_next):
    """Middleware para cache automático de respuestas"""

    # Solo cachear GET requests
    if request.method != "GET":
        return await call_next(request)

    # Verificar si la ruta debe ser cacheada
    cacheable_paths = ["/users/", "/posts/", "/stats/"]
    if not any(path in str(request.url) for path in cacheable_paths):
        return await call_next(request)

    # Intentar obtener respuesta cacheada
    cached_response = await ResponseCache.get_cached_response(request)
    if cached_response:
        response = JSONResponse(content=cached_response)
        response.headers["X-Cache"] = "HIT"
        response.headers["X-Cache-Time"] = "0"
        return response

    # Ejecutar request original
    start_time = time.time()
    response = await call_next(request)
    execution_time = time.time() - start_time

    # Cachear respuesta exitosa
    if response.status_code == 200:
        try:
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            response_data = json.loads(response_body.decode())

            # Determinar TTL basado en la ruta
            ttl = 300  # 5 minutos por defecto
            if "/stats/" in str(request.url):
                ttl = 900  # 15 minutos para stats
            elif "/users/" in str(request.url):
                ttl = 600  # 10 minutos para usuarios

            await ResponseCache.cache_response(request, response_data, ttl)

            # Crear nueva respuesta con headers de cache
            new_response = JSONResponse(content=response_data)
            new_response.headers["X-Cache"] = "MISS"
            new_response.headers["X-Cache-Time"] = f"{execution_time:.4f}"

            return new_response

        except Exception as e:
            # Si no se puede cachear, devolver respuesta original
            pass

    response.headers["X-Cache"] = "SKIP"
    response.headers["X-Cache-Time"] = f"{execution_time:.4f}"
    return response
```

### Paso 6: Endpoints con Cache Implementado

```python
# app/routers/cached_endpoints.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.cache.database_cache import DatabaseCache
from app.cache.decorators import async_cached
from app.cache.response_cache import cache_response
import time

router = APIRouter(prefix="/cached", tags=["cached"])

@router.get("/user/{user_id}")
async def get_user_cached(user_id: int, db: Session = Depends(get_db)):
    """Endpoint con cache de usuario"""
    start_time = time.time()

    # Usar cache de base de datos
    user_data = DatabaseCache.get_user_by_id(db, user_id)

    execution_time = time.time() - start_time

    if user_data:
        return {
            "user": user_data,
            "cache_info": {
                "execution_time": execution_time,
                "cached": True
            }
        }
    else:
        return {"error": "User not found"}

@router.get("/user/{user_id}/posts")
@cache_response(ttl=600)
async def get_user_posts_cached(
    request: Request,
    user_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Endpoint con cache de posts"""
    posts = DatabaseCache.get_user_posts(db, user_id, limit)
    return {
        "posts": posts,
        "count": len(posts)
    }

@router.get("/user/{user_id}/stats")
async def get_user_stats_cached(user_id: int, db: Session = Depends(get_db)):
    """Endpoint con cache de estadísticas"""
    stats = DatabaseCache.get_user_stats(db, user_id)
    return {"stats": stats}

@router.post("/user/{user_id}/invalidate")
async def invalidate_user_cache(user_id: int):
    """Endpoint para invalidar cache de usuario"""
    DatabaseCache.invalidate_user_cache(user_id)
    return {"message": f"Cache invalidated for user {user_id}"}

@router.get("/cache/stats")
async def get_cache_stats():
    """Estadísticas del cache"""
    info = cache.client.info()
    return {
        "used_memory": info.get("used_memory_human"),
        "connected_clients": info.get("connected_clients"),
        "total_commands_processed": info.get("total_commands_processed"),
        "keyspace_hits": info.get("keyspace_hits"),
        "keyspace_misses": info.get("keyspace_misses"),
        "hit_rate": (
            info.get("keyspace_hits", 0) /
            (info.get("keyspace_hits", 0) + info.get("keyspace_misses", 1))
        ) * 100
    }
```

### Paso 7: Cache de Sesiones y Autenticación

```python
# app/cache/auth_cache.py
from app.cache.decorators import async_cached
from app.cache.redis_client import cache
import jwt
from datetime import datetime, timedelta

class AuthCache:

    @staticmethod
    async def cache_user_session(user_id: int, session_data: dict, ttl: int = 3600):
        """Cachear datos de sesión de usuario"""
        cache_key = f"session:user:{user_id}"
        await cache.aset(cache_key, session_data, ttl)

    @staticmethod
    async def get_user_session(user_id: int) -> dict:
        """Obtener datos de sesión de usuario"""
        cache_key = f"session:user:{user_id}"
        return await cache.aget(cache_key)

    @staticmethod
    async def invalidate_user_session(user_id: int):
        """Invalidar sesión de usuario"""
        cache_key = f"session:user:{user_id}"
        await cache.adelete(cache_key)

    @staticmethod
    async def cache_jwt_blacklist(jti: str, exp: datetime):
        """Cachear JWT en blacklist"""
        cache_key = f"blacklist:jwt:{jti}"
        ttl = int((exp - datetime.utcnow()).total_seconds())
        if ttl > 0:
            await cache.aset(cache_key, True, ttl)

    @staticmethod
    async def is_jwt_blacklisted(jti: str) -> bool:
        """Verificar si JWT está en blacklist"""
        cache_key = f"blacklist:jwt:{jti}"
        return await cache.aget(cache_key) is not None
```

## Ejercicios Prácticos

### Ejercicio 1: Implementación Básica

1. Configura Redis y el cliente de cache
2. Implementa cache para un endpoint simple
3. Mide las mejoras de rendimiento
4. Documenta los resultados

### Ejercicio 2: Cache Inteligente

1. Implementa invalidación automática
2. Crea diferentes TTL para diferentes tipos de datos
3. Implementa cache warming
4. Monitorea hit/miss rates

### Ejercicio 3: Cache Distribuido

1. Configura cache para múltiples instancias
2. Implementa estrategias de consistencia
3. Maneja fallos de Redis gracefully
4. Implementa fallback a cache local

## Métricas de Evaluación

### ✅ Checklist de Completitud

- [ ] Configuraste Redis correctamente
- [ ] Implementaste decoradores de cache
- [ ] Creaste cache de consultas DB
- [ ] Implementaste cache de respuestas HTTP
- [ ] Agregaste middleware de cache
- [ ] Implementaste invalidación de cache
- [ ] Añadiste monitoreo de cache

### 📊 Indicadores de Rendimiento

- **Hit Rate**: Mínimo 70% de hit rate
- **Tiempo de respuesta**: Reducción de 50-90%
- **Uso de memoria**: Eficiente y controlado
- **Escalabilidad**: Consistente bajo carga

## Troubleshooting

### Problema: Cache no se actualiza

```python
# Verificar TTL y estrategias de invalidación
cache.client.ttl("cache_key")  # Ver tiempo restante

# Invalidación manual si es necesario
cache.flush_pattern("pattern:*")
```

### Problema: Memoria alta en Redis

```python
# Configurar políticas de eviction
redis.config_set("maxmemory-policy", "allkeys-lru")

# Monitorear uso de memoria
info = cache.client.info("memory")
print(f"Used memory: {info['used_memory_human']}")
```

### Problema: Serialización de objetos complejos

```python
# Usar pickle para objetos no JSON-serializables
import pickle

def safe_serialize(obj):
    try:
        return json.dumps(obj, default=str)
    except:
        return pickle.dumps(obj)
```

## Recursos Adicionales

- [Redis Documentation](https://redis.io/documentation)
- [Caching Patterns](https://docs.aws.amazon.com/AmazonElastiCache/latest/red-ug/Strategies.html)
- [FastAPI Caching](https://fastapi.tiangolo.com/advanced/response-model/)

## Próximos Pasos

En la siguiente práctica, implementaremos monitoreo y APM para observar el rendimiento en tiempo real.
