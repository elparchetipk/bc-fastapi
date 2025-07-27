# Práctica 25: Middleware y Rate Limiting

## Objetivos

- Implementar middleware personalizado para logging y métricas
- Configurar rate limiting para proteger la API
- Implementar middleware de compresión y CORS
- Crear sistema de monitoreo de requests
- Configurar throttling por usuario y endpoint

## Duración Estimada

2.5 horas

## Prerrequisitos

- Práctica 23 y 24 completadas
- Redis configurado y funcionando
- FastAPI con base de datos configurada

---

## Paso 1: Middleware de Logging y Métricas

### 1.1 Crear middleware personalizado

Crear archivo `app/middleware/logging_middleware.py`:

```python
import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response as StarletteResponse

# Configurar logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware para logging detallado de requests y responses."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> StarletteResponse:
        # Registrar inicio del request
        start_time = time.time()
        request_id = f"{time.time()}_{id(request)}"

        # Log del request entrante
        logger.info(
            f"Request {request_id}: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )

        # Headers importantes (sin datos sensibles)
        safe_headers = {
            k: v for k, v in request.headers.items()
            if k.lower() not in ['authorization', 'cookie', 'x-api-key']
        }
        logger.debug(f"Request {request_id} headers: {safe_headers}")

        try:
            # Procesar request
            response = await call_next(request)

            # Calcular tiempo de procesamiento
            process_time = time.time() - start_time

            # Log del response
            logger.info(
                f"Response {request_id}: {response.status_code} "
                f"in {process_time:.4f}s"
            )

            # Agregar headers de timing
            response.headers["X-Process-Time"] = str(process_time)
            response.headers["X-Request-ID"] = request_id

            return response

        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Error in request {request_id}: {str(e)} "
                f"after {process_time:.4f}s"
            )
            raise

class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware para recolectar métricas de la aplicación."""

    def __init__(self, app):
        super().__init__(app)
        self.request_count = 0
        self.total_time = 0
        self.status_codes = {}
        self.endpoint_metrics = {}

    async def dispatch(
        self,
        request: Request,
        call_next: Callable
    ) -> StarletteResponse:
        start_time = time.time()

        try:
            response = await call_next(request)
            process_time = time.time() - start_time

            # Actualizar métricas
            self.request_count += 1
            self.total_time += process_time

            # Conteo por status code
            status = response.status_code
            self.status_codes[status] = self.status_codes.get(status, 0) + 1

            # Métricas por endpoint
            endpoint = f"{request.method} {request.url.path}"
            if endpoint not in self.endpoint_metrics:
                self.endpoint_metrics[endpoint] = {
                    'count': 0,
                    'total_time': 0,
                    'avg_time': 0
                }

            endpoint_data = self.endpoint_metrics[endpoint]
            endpoint_data['count'] += 1
            endpoint_data['total_time'] += process_time
            endpoint_data['avg_time'] = endpoint_data['total_time'] / endpoint_data['count']

            return response

        except Exception as e:
            # Registrar error en métricas
            self.status_codes[500] = self.status_codes.get(500, 0) + 1
            raise

    def get_metrics(self) -> dict:
        """Obtener métricas actuales."""
        avg_response_time = (
            self.total_time / self.request_count
            if self.request_count > 0 else 0
        )

        return {
            'total_requests': self.request_count,
            'avg_response_time': round(avg_response_time, 4),
            'status_codes': self.status_codes,
            'endpoints': self.endpoint_metrics
        }
```

### 1.2 Crear endpoint de métricas

Crear archivo `app/routers/metrics.py`:

```python
from fastapi import APIRouter, Depends
from typing import Dict, Any

router = APIRouter(prefix="/metrics", tags=["metrics"])

# Variable global para acceder a las métricas
# En producción, usar un sistema más robusto como Prometheus
metrics_middleware = None

def set_metrics_middleware(middleware):
    """Configurar referencia al middleware de métricas."""
    global metrics_middleware
    metrics_middleware = middleware

@router.get("/system")
async def get_system_metrics() -> Dict[str, Any]:
    """Obtener métricas del sistema."""
    if not metrics_middleware:
        return {"error": "Metrics middleware not configured"}

    return metrics_middleware.get_metrics()

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "FastAPI Performance API"
    }
```

## Paso 2: Rate Limiting con Redis

### 2.1 Implementar rate limiter

Crear archivo `app/middleware/rate_limit.py`:

```python
import time
import redis
from typing import Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Middleware para rate limiting usando Redis."""

    def __init__(
        self,
        app,
        redis_client: redis.Redis,
        default_requests: int = 100,
        default_window: int = 3600,  # 1 hora
    ):
        super().__init__(app)
        self.redis = redis_client
        self.default_requests = default_requests
        self.default_window = default_window

        # Configuración por endpoint
        self.endpoint_limits = {
            'POST /users': {'requests': 10, 'window': 300},  # 10 req/5min
            'GET /users': {'requests': 50, 'window': 300},   # 50 req/5min
            'POST /auth/login': {'requests': 5, 'window': 300},  # 5 req/5min
        }

    async def dispatch(self, request: Request, call_next):
        # Obtener identificador del cliente
        client_id = self._get_client_id(request)
        endpoint_key = f"{request.method} {request.url.path}"

        # Verificar rate limit
        if await self._is_rate_limited(client_id, endpoint_key):
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Try again later.",
                headers={"Retry-After": "60"}
            )

        # Procesar request
        response = await call_next(request)

        # Agregar headers de rate limit
        limit_info = await self._get_limit_info(client_id, endpoint_key)
        response.headers.update(limit_info)

        return response

    def _get_client_id(self, request: Request) -> str:
        """Obtener identificador único del cliente."""
        # Usar IP + User-Agent como identificador
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        return f"{client_ip}:{hash(user_agent)}"

    async def _is_rate_limited(self, client_id: str, endpoint: str) -> bool:
        """Verificar si el cliente ha excedido el rate limit."""
        # Obtener configuración para el endpoint
        config = self.endpoint_limits.get(
            endpoint,
            {'requests': self.default_requests, 'window': self.default_window}
        )

        key = f"rate_limit:{client_id}:{endpoint}"
        current_time = int(time.time())
        window_start = current_time - config['window']

        try:
            # Usar Redis sorted set para tracking temporal
            pipe = self.redis.pipeline()

            # Limpiar requests antiguos
            pipe.zremrangebyscore(key, 0, window_start)

            # Contar requests en la ventana actual
            pipe.zcard(key)

            # Agregar request actual
            pipe.zadd(key, {str(current_time): current_time})

            # Establecer TTL
            pipe.expire(key, config['window'])

            results = pipe.execute()
            request_count = results[1]  # Resultado del zcard

            return request_count >= config['requests']

        except redis.RedisError:
            # En caso de error de Redis, permitir el request
            return False

    async def _get_limit_info(self, client_id: str, endpoint: str) -> dict:
        """Obtener información del límite actual."""
        config = self.endpoint_limits.get(
            endpoint,
            {'requests': self.default_requests, 'window': self.default_window}
        )

        key = f"rate_limit:{client_id}:{endpoint}"
        current_time = int(time.time())
        window_start = current_time - config['window']

        try:
            # Limpiar y contar
            self.redis.zremrangebyscore(key, 0, window_start)
            current_count = self.redis.zcard(key)

            remaining = max(0, config['requests'] - current_count)
            reset_time = current_time + config['window']

            return {
                "X-RateLimit-Limit": str(config['requests']),
                "X-RateLimit-Remaining": str(remaining),
                "X-RateLimit-Reset": str(reset_time),
                "X-RateLimit-Window": str(config['window'])
            }

        except redis.RedisError:
            return {
                "X-RateLimit-Limit": str(config['requests']),
                "X-RateLimit-Remaining": str(config['requests']),
                "X-RateLimit-Reset": str(current_time + config['window']),
                "X-RateLimit-Window": str(config['window'])
            }

class IPWhitelistMiddleware(BaseHTTPMiddleware):
    """Middleware para whitelist de IPs."""

    def __init__(self, app, whitelist: list = None):
        super().__init__(app)
        self.whitelist = whitelist or []

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host if request.client else None

        # Si hay whitelist y la IP no está en ella
        if self.whitelist and client_ip not in self.whitelist:
            # Verificar si es una IP local o de desarrollo
            if not self._is_local_ip(client_ip):
                raise HTTPException(
                    status_code=403,
                    detail="Access denied from this IP address"
                )

        return await call_next(request)

    def _is_local_ip(self, ip: str) -> bool:
        """Verificar si es una IP local."""
        if not ip:
            return False

        local_patterns = ['127.', '192.168.', '10.', '172.']
        return any(ip.startswith(pattern) for pattern in local_patterns)
```

## Paso 3: Middleware de Compresión y CORS

### 3.1 Configurar middlewares adicionales

Crear archivo `app/middleware/__init__.py`:

```python
from .logging_middleware import RequestLoggingMiddleware, MetricsMiddleware
from .rate_limit import RateLimitMiddleware, IPWhitelistMiddleware

__all__ = [
    'RequestLoggingMiddleware',
    'MetricsMiddleware',
    'RateLimitMiddleware',
    'IPWhitelistMiddleware'
]
```

### 3.2 Actualizar main.py

Actualizar `app/main.py`:

```python
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.middleware import (
    RequestLoggingMiddleware,
    MetricsMiddleware,
    RateLimitMiddleware,
    IPWhitelistMiddleware
)
from app.routers import users, metrics
from app.routers.metrics import set_metrics_middleware
from app.core.config import settings

# Crear aplicación
app = FastAPI(
    title="FastAPI Performance API",
    description="API optimizada con middleware y rate limiting",
    version="1.0.0"
)

# Configurar Redis
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True
)

# Middleware de seguridad (primero)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1", "*.yourdomain.com"]
)

# IP Whitelist (opcional, para entornos específicos)
if settings.ENVIRONMENT == "production":
    app.add_middleware(
        IPWhitelistMiddleware,
        whitelist=settings.ALLOWED_IPS
    )

# Rate Limiting
app.add_middleware(
    RateLimitMiddleware,
    redis_client=redis_client,
    default_requests=100,
    default_window=3600
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compresión
app.add_middleware(
    GZipMiddleware,
    minimum_size=1000  # Comprimir respuestas > 1KB
)

# Logging y métricas
app.add_middleware(RequestLoggingMiddleware)

# Métricas (último para capturar todo)
metrics_middleware = MetricsMiddleware(app)
app.add_middleware(lambda app: metrics_middleware)
set_metrics_middleware(metrics_middleware)

# Incluir routers
app.include_router(users.router)
app.include_router(metrics.router)

@app.get("/")
async def root():
    return {
        "message": "FastAPI Performance API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    try:
        # Verificar Redis
        redis_client.ping()
        redis_status = "connected"
    except:
        redis_status = "disconnected"

    return {
        "status": "healthy",
        "redis": redis_status,
        "version": "1.0.0"
    }
```

## Paso 4: Testing y Benchmarking

### 4.1 Script de pruebas de rate limiting

Crear archivo `tests/test_rate_limiting.py`:

```python
import asyncio
import aiohttp
import time
from typing import List, Dict

async def test_rate_limit(
    url: str = "http://localhost:8000",
    endpoint: str = "/users",
    requests_count: int = 20,
    concurrent: int = 5
) -> Dict:
    """Probar rate limiting enviando múltiples requests."""

    results = {
        'successful': 0,
        'rate_limited': 0,
        'errors': 0,
        'response_times': [],
        'status_codes': []
    }

    async def make_request(session: aiohttp.ClientSession, request_id: int):
        start_time = time.time()
        try:
            async with session.get(f"{url}{endpoint}") as response:
                response_time = time.time() - start_time
                results['response_times'].append(response_time)
                results['status_codes'].append(response.status)

                if response.status == 200:
                    results['successful'] += 1
                elif response.status == 429:
                    results['rate_limited'] += 1
                    print(f"Request {request_id}: Rate limited")
                else:
                    results['errors'] += 1

                # Mostrar headers de rate limit
                headers = dict(response.headers)
                rate_limit_info = {
                    k: v for k, v in headers.items()
                    if k.startswith('X-RateLimit')
                }
                if rate_limit_info:
                    print(f"Request {request_id}: {rate_limit_info}")

        except Exception as e:
            results['errors'] += 1
            print(f"Request {request_id}: Error - {e}")

    # Ejecutar requests
    connector = aiohttp.TCPConnector(limit=concurrent)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Crear semáforo para controlar concurrencia
        semaphore = asyncio.Semaphore(concurrent)

        async def bounded_request(request_id):
            async with semaphore:
                await make_request(session, request_id)

        # Ejecutar todos los requests
        tasks = [
            bounded_request(i)
            for i in range(requests_count)
        ]
        await asyncio.gather(*tasks)

    # Calcular estadísticas
    if results['response_times']:
        avg_time = sum(results['response_times']) / len(results['response_times'])
        results['avg_response_time'] = round(avg_time, 4)
        results['max_response_time'] = round(max(results['response_times']), 4)
        results['min_response_time'] = round(min(results['response_times']), 4)

    return results

async def main():
    """Ejecutar pruebas de rate limiting."""
    print("🧪 Iniciando pruebas de Rate Limiting...")

    # Prueba 1: Requests normales
    print("\n📊 Prueba 1: 10 requests concurrentes")
    results1 = await test_rate_limit(
        requests_count=10,
        concurrent=5
    )
    print(f"Resultados: {results1}")

    # Esperar un momento
    await asyncio.sleep(2)

    # Prueba 2: Superar rate limit
    print("\n📊 Prueba 2: 30 requests para superar límite")
    results2 = await test_rate_limit(
        requests_count=30,
        concurrent=10
    )
    print(f"Resultados: {results2}")

    # Prueba 3: Endpoint específico con límite bajo
    print("\n📊 Prueba 3: Testing endpoint con límite bajo")
    results3 = await test_rate_limit(
        endpoint="/users",
        requests_count=15,
        concurrent=8
    )
    print(f"Resultados: {results3}")

if __name__ == "__main__":
    asyncio.run(main())
```

### 4.2 Script de monitoreo

Crear archivo `scripts/monitor_performance.py`:

```python
import asyncio
import aiohttp
import time
import json
from datetime import datetime

async def monitor_api_performance(
    base_url: str = "http://localhost:8000",
    duration_minutes: int = 5,
    interval_seconds: int = 10
):
    """Monitorear performance de la API por un período de tiempo."""

    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    results = []

    async with aiohttp.ClientSession() as session:
        while time.time() < end_time:
            timestamp = datetime.now().isoformat()

            # Test health endpoint
            health_start = time.time()
            try:
                async with session.get(f"{base_url}/health") as response:
                    health_time = time.time() - health_start
                    health_status = response.status
                    health_success = response.status == 200
            except Exception as e:
                health_time = time.time() - health_start
                health_status = 0
                health_success = False

            # Test metrics endpoint
            metrics_start = time.time()
            try:
                async with session.get(f"{base_url}/metrics/system") as response:
                    metrics_time = time.time() - metrics_start
                    metrics_status = response.status
                    metrics_success = response.status == 200

                    if metrics_success:
                        metrics_data = await response.json()
                    else:
                        metrics_data = {}

            except Exception as e:
                metrics_time = time.time() - metrics_start
                metrics_status = 0
                metrics_success = False
                metrics_data = {}

            # Guardar resultados
            result = {
                'timestamp': timestamp,
                'health': {
                    'response_time': round(health_time, 4),
                    'status': health_status,
                    'success': health_success
                },
                'metrics': {
                    'response_time': round(metrics_time, 4),
                    'status': metrics_status,
                    'success': metrics_success,
                    'data': metrics_data
                }
            }

            results.append(result)

            print(f"[{timestamp}] Health: {health_time:.4f}s ({health_status}) | "
                  f"Metrics: {metrics_time:.4f}s ({metrics_status})")

            # Esperar antes del siguiente check
            await asyncio.sleep(interval_seconds)

    # Guardar resultados
    with open(f'monitoring_results_{int(start_time)}.json', 'w') as f:
        json.dump(results, f, indent=2)

    # Mostrar resumen
    print("\n📊 Resumen del monitoreo:")
    print(f"Duración: {duration_minutes} minutos")
    print(f"Total de checks: {len(results)}")

    health_times = [r['health']['response_time'] for r in results if r['health']['success']]
    if health_times:
        print(f"Health endpoint - Avg: {sum(health_times)/len(health_times):.4f}s, "
              f"Max: {max(health_times):.4f}s, Min: {min(health_times):.4f}s")

    metrics_times = [r['metrics']['response_time'] for r in results if r['metrics']['success']]
    if metrics_times:
        print(f"Metrics endpoint - Avg: {sum(metrics_times)/len(metrics_times):.4f}s, "
              f"Max: {max(metrics_times):.4f}s, Min: {min(metrics_times):.4f}s")

if __name__ == "__main__":
    asyncio.run(monitor_api_performance())
```

## Paso 5: Configuración y Variables de Entorno

### 5.1 Actualizar configuración

Actualizar `app/core/config.py`:

```python
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Base de datos
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    DEFAULT_RATE_LIMIT: int = 100
    DEFAULT_RATE_WINDOW: int = 3600

    # CORS y Seguridad
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    ALLOWED_IPS: List[str] = []

    # Entorno
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env"

settings = Settings()
```

### 5.2 Archivo .env de ejemplo

Crear archivo `.env.example`:

```bash
# Base de datos
DATABASE_URL=postgresql://user:password@localhost/dbname

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Rate Limiting
RATE_LIMIT_ENABLED=true
DEFAULT_RATE_LIMIT=100
DEFAULT_RATE_WINDOW=3600

# CORS y Seguridad
ALLOWED_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
ALLOWED_IPS=[]

# Entorno
ENVIRONMENT=development
DEBUG=true

# Logging
LOG_LEVEL=INFO
```

## Verificación

### ✅ Checklist de Verificación

- [ ] Middleware de logging implementado y funcionando
- [ ] Middleware de métricas recolectando datos
- [ ] Rate limiting configurado con Redis
- [ ] Endpoints protegidos según configuración
- [ ] Headers de rate limit en respuestas
- [ ] Middleware de compresión configurado
- [ ] CORS configurado correctamente
- [ ] Tests de rate limiting ejecutados
- [ ] Monitoreo de performance funcionando
- [ ] Configuración de entorno actualizada

### 🧪 Pruebas a Realizar

1. **Verificar middleware de logging:**

   ```bash
   curl http://localhost:8000/users
   # Verificar logs en consola
   ```

2. **Probar rate limiting:**

   ```bash
   python tests/test_rate_limiting.py
   ```

3. **Verificar métricas:**

   ```bash
   curl http://localhost:8000/metrics/system
   ```

4. **Monitoreo de performance:**
   ```bash
   python scripts/monitor_performance.py
   ```

### 🔧 Troubleshooting

**Redis no conecta:**

- Verificar que Redis esté ejecutándose: `redis-cli ping`
- Verificar configuración en `.env`

**Rate limiting no funciona:**

- Verificar logs de Redis
- Verificar configuración de límites por endpoint

**Middleware no procesa requests:**

- Verificar orden de middleware en `main.py`
- Verificar logs de errores

### 📈 Análisis de Resultados

Después de ejecutar las pruebas:

1. **Revisar logs** para verificar el middleware de logging
2. **Analizar métricas** del endpoint `/metrics/system`
3. **Verificar rate limiting** con múltiples requests
4. **Monitorear performance** durante carga

### 🎯 Próximos Pasos

- Práctica 26: Implementar monitoring y profiling avanzado
- Configurar alertas basadas en métricas
- Optimizar configuración de rate limiting según uso real

---

## Recursos Adicionales

- [FastAPI Middleware](https://fastapi.tiangolo.com/tutorial/middleware/)
- [Redis Rate Limiting Patterns](https://redis.io/docs/manual/patterns/distributed-locks/)
- [CORS Configuration](https://fastapi.tiangolo.com/tutorial/cors/)
- [GZip Compression](https://fastapi.tiangolo.com/advanced/middleware/#gzipmiddleware)
