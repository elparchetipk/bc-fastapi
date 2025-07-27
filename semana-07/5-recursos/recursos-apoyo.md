# Recursos de Apoyo - Optimización y Performance

## Introducción

Esta sección proporciona recursos adicionales, referencias y herramientas para profundizar en los conceptos de optimización y performance de APIs con FastAPI.

---

## 📚 Referencias y Documentación

### FastAPI Performance

- **[FastAPI Performance Tips](https://fastapi.tiangolo.com/async/)** - Guía oficial de performance
- **[Async/Await Best Practices](https://fastapi.tiangolo.com/async/#concurrency-and-async-await)** - Manejo de concurrencia
- **[Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)** - Tareas en segundo plano
- **[Middleware Guide](https://fastapi.tiangolo.com/tutorial/middleware/)** - Implementación de middleware

### Redis y Caching

- **[Redis Documentation](https://redis.io/docs/)** - Documentación completa
- **[Redis Patterns](https://redis.io/docs/manual/patterns/)** - Patrones de diseño
- **[Caching Strategies](https://redis.io/docs/manual/patterns/distributed-locks/)** - Estrategias de cache
- **[Redis Python Client](https://redis-py.readthedocs.io/)** - Cliente Python redis-py

### Base de Datos y SQL

- **[PostgreSQL Performance](https://wiki.postgresql.org/wiki/Performance_Optimization)** - Optimización PostgreSQL
- **[SQLAlchemy Performance](https://docs.sqlalchemy.org/en/14/orm/loading_techniques.html)** - Técnicas de carga
- **[Database Indexing](https://use-the-index-luke.com/)** - Guía de índices
- **[Query Optimization](https://www.postgresql.org/docs/current/using-explain.html)** - Análisis de queries

### Monitoring y Observability

- **[Prometheus Documentation](https://prometheus.io/docs/)** - Sistema de monitoreo
- **[Grafana Tutorials](https://grafana.com/tutorials/)** - Dashboards y visualización
- **[Application Performance Monitoring](https://www.datadoghq.com/knowledge-center/apm/)** - Conceptos APM
- **[Python Profiling](https://docs.python.org/3/library/profile.html)** - Profiling nativo

---

## 🛠️ Herramientas y Librerías

### Performance Testing

```bash
# LoadRunner alternativo open source
pip install locust

# Apache Bench (simple HTTP load testing)
sudo apt-get install apache2-utils

# Artillery.io (Node.js based)
npm install -g artillery

# wrk (modern HTTP benchmarking tool)
sudo apt-get install wrk
```

### Monitoring Tools

```bash
# System monitoring
pip install psutil

# Application monitoring
pip install py-spy
pip install memory-profiler

# Network monitoring
pip install speedtest-cli

# Database monitoring
pip install pgcli
```

### Development Tools

```bash
# Code profiling
pip install line-profiler
pip install py-spy

# Memory analysis
pip install memory-profiler
pip install pympler

# Code quality
pip install black isort flake8
pip install mypy

# Testing
pip install pytest pytest-asyncio pytest-benchmark
```

---

## 🔧 Scripts y Configuraciones

### Docker Compose para Development

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - '8000:8000'
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/ecommerce
      - REDIS_URL=redis://redis:6379
      - DEBUG=true
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: ecommerce
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    ports:
      - '5432:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/init.sql:/docker-entrypoint-initdb.d/init.sql

  redis:
    image: redis:6-alpine
    ports:
      - '6379:6379'
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data

  prometheus:
    image: prom/prometheus
    ports:
      - '9090:9090'
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - '3000:3000'
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  postgres_data:
  redis_data:
  grafana_data:
```

### Script de Benchmarking

```python
# scripts/benchmark.py
import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict
import argparse

async def benchmark_endpoint(
    url: str,
    concurrent_users: int = 10,
    requests_per_user: int = 100,
    timeout: int = 30
) -> Dict:
    """Benchmark específico para un endpoint."""

    results = {
        'response_times': [],
        'status_codes': [],
        'errors': []
    }

    async def make_requests(session: aiohttp.ClientSession, user_id: int):
        for i in range(requests_per_user):
            start_time = time.time()
            try:
                async with session.get(url, timeout=timeout) as response:
                    response_time = time.time() - start_time
                    results['response_times'].append(response_time * 1000)  # ms
                    results['status_codes'].append(response.status)

            except asyncio.TimeoutError:
                results['errors'].append('timeout')
            except Exception as e:
                results['errors'].append(str(e))

    # Crear sesión con conexiones limitadas
    connector = aiohttp.TCPConnector(limit=concurrent_users)
    timeout_config = aiohttp.ClientTimeout(total=timeout)

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout_config
    ) as session:
        tasks = [
            make_requests(session, user_id)
            for user_id in range(concurrent_users)
        ]

        start_time = time.time()
        await asyncio.gather(*tasks)
        total_time = time.time() - start_time

    # Calcular estadísticas
    if results['response_times']:
        stats = {
            'total_requests': len(results['response_times']),
            'total_time': round(total_time, 2),
            'rps': round(len(results['response_times']) / total_time, 2),
            'avg_response_time': round(statistics.mean(results['response_times']), 2),
            'min_response_time': round(min(results['response_times']), 2),
            'max_response_time': round(max(results['response_times']), 2),
            'p95_response_time': round(statistics.quantiles(results['response_times'], n=20)[18], 2),
            'errors': len(results['errors']),
            'error_rate': round((len(results['errors']) / (len(results['response_times']) + len(results['errors']))) * 100, 2)
        }

        # Distribución de status codes
        status_distribution = {}
        for status in results['status_codes']:
            status_distribution[status] = status_distribution.get(status, 0) + 1

        stats['status_distribution'] = status_distribution
        return stats

    return {'error': 'No successful requests'}

async def main():
    parser = argparse.ArgumentParser(description='FastAPI Benchmark Tool')
    parser.add_argument('--url', default='http://localhost:8000', help='Base URL')
    parser.add_argument('--users', type=int, default=10, help='Concurrent users')
    parser.add_argument('--requests', type=int, default=100, help='Requests per user')

    args = parser.parse_args()

    endpoints = [
        '/health',
        '/products',
        '/products/1',
        '/categories',
        '/users/me'
    ]

    print(f"🚀 Starting benchmark with {args.users} users, {args.requests} requests each")
    print(f"Target: {args.url}")
    print("=" * 60)

    for endpoint in endpoints:
        print(f"\n📊 Testing {endpoint}...")
        result = await benchmark_endpoint(
            f"{args.url}{endpoint}",
            concurrent_users=args.users,
            requests_per_user=args.requests
        )

        if 'error' not in result:
            print(f"  Total Requests: {result['total_requests']}")
            print(f"  RPS: {result['rps']}")
            print(f"  Avg Response Time: {result['avg_response_time']}ms")
            print(f"  P95 Response Time: {result['p95_response_time']}ms")
            print(f"  Error Rate: {result['error_rate']}%")
            print(f"  Status Codes: {result['status_distribution']}")
        else:
            print(f"  ❌ {result['error']}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Configuración de Prometheus

```yaml
# monitoring/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - 'rules/*.yml'

scrape_configs:
  - job_name: 'fastapi-app'
    static_configs:
      - targets: ['app:8000']
    metrics_path: '/metrics'
    scrape_interval: 5s

  - job_name: 'redis'
    static_configs:
      - targets: ['redis:6379']

  - job_name: 'postgres'
    static_configs:
      - targets: ['db:5432']

alerting:
  alertmanagers:
    - static_configs:
        - targets:
            - alertmanager:9093
```

---

## 📖 Tutoriales y Guías

### Tutorial: Implementar Cache Inteligente

```python
# tutorials/smart_cache.py
"""
Tutorial: Implementación de Cache Inteligente
Aprende a crear un sistema de cache que se adapta automáticamente
basado en patrones de uso.
"""

import time
import redis
from typing import Any, Optional, Dict
from functools import wraps

class SmartCache:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.access_patterns = {}

    def adaptive_cache(self,
                      base_ttl: int = 3600,
                      min_ttl: int = 300,
                      max_ttl: int = 86400):
        """
        Decorador que ajusta TTL basado en frecuencia de acceso.

        Lógica:
        - Keys accedidos frecuentemente → TTL más largo
        - Keys accedidos raramente → TTL más corto
        """
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Generar cache key
                cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"

                # Intentar obtener del cache
                cached_value = self.redis.get(cache_key)
                if cached_value:
                    # Registrar acceso
                    self._record_access(cache_key)
                    return json.loads(cached_value)

                # Ejecutar función
                result = await func(*args, **kwargs)

                # Calcular TTL adaptativo
                adaptive_ttl = self._calculate_adaptive_ttl(
                    cache_key, base_ttl, min_ttl, max_ttl
                )

                # Guardar en cache
                self.redis.setex(
                    cache_key,
                    adaptive_ttl,
                    json.dumps(result, default=str)
                )

                return result
            return wrapper
        return decorator

    def _record_access(self, cache_key: str):
        """Registrar acceso para análisis de patrones."""
        access_key = f"access:{cache_key}"
        current_time = int(time.time())

        # Incrementar contador de accesos
        self.redis.zincrby("access_frequency", 1, cache_key)

        # Registrar timestamp del último acceso
        self.redis.hset("last_access", cache_key, current_time)

    def _calculate_adaptive_ttl(self, cache_key: str, base_ttl: int,
                               min_ttl: int, max_ttl: int) -> int:
        """Calcular TTL basado en patrones de acceso."""

        # Obtener frecuencia de acceso
        frequency = self.redis.zscore("access_frequency", cache_key) or 0

        # Obtener último acceso
        last_access = self.redis.hget("last_access", cache_key)

        if last_access:
            time_since_access = int(time.time()) - int(last_access)

            # Lógica de adaptación
            if frequency > 10 and time_since_access < 3600:
                # Muy accedido recientemente → TTL largo
                return min(max_ttl, base_ttl * 2)
            elif frequency < 2 or time_since_access > 86400:
                # Poco accedido o antiguo → TTL corto
                return max(min_ttl, base_ttl // 2)

        return base_ttl

# Ejemplo de uso
cache = SmartCache(redis.Redis())

@cache.adaptive_cache(base_ttl=3600)
async def expensive_calculation(param1: str, param2: int):
    # Simulación de cálculo costoso
    await asyncio.sleep(1)
    return f"Result for {param1}-{param2}"
```

### Tutorial: Rate Limiting por Usuario

```python
# tutorials/user_rate_limiting.py
"""
Tutorial: Rate Limiting Personalizado por Usuario
Implementa rate limiting que considera el tipo de usuario y su comportamiento.
"""

import redis
import time
from enum import Enum
from typing import Dict, Optional

class UserType(Enum):
    GUEST = "guest"
    BASIC = "basic"
    PREMIUM = "premium"
    ADMIN = "admin"

class UserRateLimiter:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

        # Configuración de límites por tipo de usuario
        self.limits = {
            UserType.GUEST: {"requests": 100, "window": 3600},
            UserType.BASIC: {"requests": 500, "window": 3600},
            UserType.PREMIUM: {"requests": 2000, "window": 3600},
            UserType.ADMIN: {"requests": 10000, "window": 3600}
        }

        # Multiplicadores por endpoint
        self.endpoint_multipliers = {
            "/products/search": 0.5,  # Búsquedas son más costosas
            "/orders": 0.3,           # Crear órdenes es crítico
            "/auth/login": 0.1,       # Login muy limitado
            "default": 1.0
        }

    async def check_rate_limit(self,
                              user_id: str,
                              user_type: UserType,
                              endpoint: str) -> Dict[str, Any]:
        """
        Verificar rate limit para usuario específico.

        Returns:
            Dict con información del rate limit
        """

        # Obtener configuración base
        base_config = self.limits[user_type]

        # Aplicar multiplicador por endpoint
        endpoint_key = self._normalize_endpoint(endpoint)
        multiplier = self.endpoint_multipliers.get(endpoint_key, 1.0)

        effective_limit = int(base_config["requests"] * multiplier)
        window = base_config["window"]

        # Verificar límite actual
        current_usage = await self._get_current_usage(
            user_id, endpoint_key, window
        )

        # Registrar request actual
        await self._record_request(user_id, endpoint_key, window)

        is_limited = current_usage >= effective_limit

        return {
            "is_limited": is_limited,
            "limit": effective_limit,
            "current": current_usage + 1,
            "remaining": max(0, effective_limit - current_usage - 1),
            "reset_time": int(time.time()) + window,
            "user_type": user_type.value
        }

    def _normalize_endpoint(self, endpoint: str) -> str:
        """Normalizar endpoint para agrupación."""
        # Convertir /products/123 a /products/{id}
        parts = endpoint.split('/')
        normalized_parts = []

        for part in parts:
            if part.isdigit():
                normalized_parts.append('{id}')
            else:
                normalized_parts.append(part)

        normalized = '/'.join(normalized_parts)
        return normalized if normalized in self.endpoint_multipliers else "default"

    async def _get_current_usage(self, user_id: str, endpoint: str, window: int) -> int:
        """Obtener uso actual en la ventana."""
        key = f"rate_limit:{user_id}:{endpoint}"
        current_time = int(time.time())
        window_start = current_time - window

        # Limpiar requests antiguos y contar actuales
        self.redis.zremrangebyscore(key, 0, window_start)
        return self.redis.zcard(key)

    async def _record_request(self, user_id: str, endpoint: str, window: int):
        """Registrar nuevo request."""
        key = f"rate_limit:{user_id}:{endpoint}"
        current_time = int(time.time())

        # Agregar request a sorted set
        self.redis.zadd(key, {str(current_time): current_time})
        self.redis.expire(key, window)

# Middleware de ejemplo
from fastapi import Request, HTTPException

class UserRateLimitMiddleware:
    def __init__(self, app, rate_limiter: UserRateLimiter):
        self.app = app
        self.rate_limiter = rate_limiter

    async def __call__(self, request: Request, call_next):
        # Obtener información del usuario (desde JWT, sesión, etc.)
        user_id = getattr(request.state, "user_id", "anonymous")
        user_type = getattr(request.state, "user_type", UserType.GUEST)

        # Verificar rate limit
        limit_info = await self.rate_limiter.check_rate_limit(
            user_id, user_type, request.url.path
        )

        if limit_info["is_limited"]:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "limit": limit_info["limit"],
                    "reset_time": limit_info["reset_time"]
                },
                headers={
                    "X-RateLimit-Limit": str(limit_info["limit"]),
                    "X-RateLimit-Remaining": str(limit_info["remaining"]),
                    "X-RateLimit-Reset": str(limit_info["reset_time"]),
                    "Retry-After": "60"
                }
            )

        # Procesar request
        response = await call_next(request)

        # Agregar headers informativos
        response.headers["X-RateLimit-Limit"] = str(limit_info["limit"])
        response.headers["X-RateLimit-Remaining"] = str(limit_info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(limit_info["reset_time"])

        return response
```

---

## 🧪 Testing y Benchmarking

### Test Suite para Performance

```python
# tests/test_performance.py
import pytest
import asyncio
import time
from httpx import AsyncClient

class TestPerformance:
    """Suite de tests de performance."""

    @pytest.mark.asyncio
    async def test_response_time_sla(self, client: AsyncClient):
        """Verificar que response times cumplen SLA."""
        endpoints = [
            "/health",
            "/products",
            "/categories",
            "/users/me"
        ]

        for endpoint in endpoints:
            start_time = time.time()
            response = await client.get(endpoint)
            response_time = (time.time() - start_time) * 1000  # ms

            assert response.status_code == 200
            assert response_time < 200, f"{endpoint} exceeded 200ms SLA: {response_time}ms"

    @pytest.mark.asyncio
    async def test_concurrent_load(self, client: AsyncClient):
        """Test de carga con usuarios concurrentes."""
        async def make_request():
            response = await client.get("/products")
            return response.status_code

        # 50 requests concurrentes
        tasks = [make_request() for _ in range(50)]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        # Verificar que todas las requests fueron exitosas
        assert all(status == 200 for status in results)

        # Verificar throughput mínimo (requests per second)
        rps = len(results) / total_time
        assert rps > 100, f"RPS too low: {rps}"

    @pytest.mark.asyncio
    async def test_cache_performance(self, client: AsyncClient):
        """Verificar mejora de performance con cache."""
        endpoint = "/products/1"

        # Primera request (sin cache)
        start_time = time.time()
        response1 = await client.get(endpoint)
        first_request_time = time.time() - start_time

        # Segunda request (con cache)
        start_time = time.time()
        response2 = await client.get(endpoint)
        cached_request_time = time.time() - start_time

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response1.json() == response2.json()

        # Cache debe ser significativamente más rápido
        improvement = (first_request_time - cached_request_time) / first_request_time
        assert improvement > 0.3, f"Cache improvement too low: {improvement * 100}%"

    @pytest.mark.asyncio
    async def test_rate_limiting(self, client: AsyncClient):
        """Verificar funcionamiento de rate limiting."""
        endpoint = "/auth/login"

        # Hacer múltiples requests rápidamente
        responses = []
        for _ in range(15):  # Más que el límite configurado
            response = await client.post(endpoint, json={
                "username": "test",
                "password": "wrong"
            })
            responses.append(response.status_code)

        # Debe haber algunas responses 429 (rate limited)
        rate_limited_count = sum(1 for status in responses if status == 429)
        assert rate_limited_count > 0, "Rate limiting not working"

    @pytest.mark.benchmark
    def test_database_query_performance(self, benchmark):
        """Benchmark de queries de base de datos."""
        from services.product_service import ProductService

        def query_products():
            # Implementar query de prueba
            return ProductService.search_products(limit=100)

        result = benchmark(query_products)

        # Verificar que el benchmark ejecutó correctamente
        assert result is not None
```

### Script de Stress Testing

```bash
#!/bin/bash
# scripts/stress_test.sh

echo "🔥 FastAPI Stress Test Suite"
echo "================================"

BASE_URL="http://localhost:8000"
CONCURRENT_USERS=100
DURATION="2m"

# Test 1: Health endpoint
echo "📊 Testing /health endpoint..."
wrk -t12 -c${CONCURRENT_USERS} -d${DURATION} --latency ${BASE_URL}/health

# Test 2: Products listing
echo "📊 Testing /products endpoint..."
wrk -t12 -c${CONCURRENT_USERS} -d${DURATION} --latency ${BASE_URL}/products

# Test 3: Product search
echo "📊 Testing /products/search endpoint..."
wrk -t12 -c${CONCURRENT_USERS} -d${DURATION} --latency \
  -s scripts/search_post.lua ${BASE_URL}/products/search

# Test 4: Mixed workload
echo "📊 Testing mixed workload..."
artillery run scripts/artillery_config.yml

echo "✅ Stress testing complete!"
```

---

## 📊 Métricas y KPIs

### Métricas Clave a Monitorear

#### Performance Metrics

- **Response Time**: Tiempo de respuesta promedio y percentiles (p50, p95, p99)
- **Throughput**: Requests por segundo (RPS)
- **Error Rate**: Porcentaje de requests fallidas
- **Latency Distribution**: Distribución de latencias

#### System Metrics

- **CPU Usage**: Uso de CPU del servidor
- **Memory Usage**: Uso de memoria RAM
- **Disk I/O**: Operaciones de lectura/escritura
- **Network I/O**: Tráfico de red

#### Application Metrics

- **Cache Hit Rate**: Porcentaje de hits en cache
- **Database Connection Pool**: Conexiones activas/disponibles
- **Queue Length**: Longitud de colas de procesamiento
- **Background Task Status**: Estado de tareas en background

#### Business Metrics

- **Active Users**: Usuarios activos concurrentes
- **API Calls per User**: Llamadas por usuario
- **Feature Usage**: Uso de características específicas
- **Conversion Rate**: Tasa de conversión de APIs

### Dashboard de Métricas (Grafana)

```json
{
  "dashboard": {
    "title": "FastAPI Performance Dashboard",
    "panels": [
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket)",
            "legendFormat": "95th percentile"
          },
          {
            "expr": "histogram_quantile(0.50, http_request_duration_seconds_bucket)",
            "legendFormat": "50th percentile"
          }
        ]
      },
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "RPS"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m]) * 100",
            "legendFormat": "Error Rate %"
          }
        ]
      }
    ]
  }
}
```

---

## 🔍 Debugging y Troubleshooting

### Herramientas de Debugging

#### py-spy (Profiling en Producción)

```bash
# Instalar py-spy
pip install py-spy

# Profiling de aplicación en ejecución
py-spy record -o profile.svg --pid $(pgrep -f "uvicorn")

# Top de funciones más costosas
py-spy top --pid $(pgrep -f "uvicorn")
```

#### Memory Profiling

```python
# memory_profiler para análisis de memoria
from memory_profiler import profile

@profile
def expensive_function():
    # Función que consume mucha memoria
    large_list = [i for i in range(1000000)]
    return sum(large_list)
```

#### Database Query Analysis

```sql
-- PostgreSQL: Analizar queries lentas
-- Habilitar logging de queries lentas
SET log_min_duration_statement = 1000; -- 1 segundo

-- Analizar plan de ejecución
EXPLAIN ANALYZE SELECT * FROM products WHERE category_id = 1;

-- Identificar queries más costosas
SELECT query, mean_time, calls
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

### Checklist de Performance Issues

#### Symptoms & Solutions

**🐌 Slow Response Times**

- [ ] Verificar indices de base de datos
- [ ] Analizar N+1 query problems
- [ ] Revisar configuración de connection pool
- [ ] Implementar/optimizar cache
- [ ] Verificar async/await usage

**📈 High CPU Usage**

- [ ] Profiling con py-spy
- [ ] Verificar loops infinitos
- [ ] Optimizar algoritmos complejos
- [ ] Revisar regex patterns
- [ ] Verificar serialización/deserialización

**💾 High Memory Usage**

- [ ] Memory profiling
- [ ] Verificar memory leaks
- [ ] Optimizar tamaño de respuestas
- [ ] Implementar pagination
- [ ] Verificar cache size limits

**🔄 High Error Rates**

- [ ] Revisar logs de errores
- [ ] Verificar rate limiting
- [ ] Analizar timeout configurations
- [ ] Verificar health de dependencias
- [ ] Implementar circuit breakers

---

## 💡 Best Practices Summary

### Development

1. **Usar async/await correctamente**
2. **Implementar logging estructurado**
3. **Escribir tests de performance**
4. **Documentar decisiones de arquitectura**
5. **Monitorear métricas desde desarrollo**

### Database

1. **Crear índices estratégicos**
2. **Evitar N+1 queries**
3. **Usar connection pooling**
4. **Implementar read replicas**
5. **Monitorear query performance**

### Caching

1. **Implementar cache hierarchy**
2. **Definir TTL strategies**
3. **Manejar cache invalidation**
4. **Monitorear hit rates**
5. **Implement cache warming**

### Monitoring

1. **Definir SLAs claros**
2. **Implementar alertas proactivas**
3. **Crear dashboards informativos**
4. **Monitorear business metrics**
5. **Implementar distributed tracing**

---

## 📞 Soporte y Comunidad

### Canales de Ayuda

- **[FastAPI Discord](https://discord.gg/VQjSZaeJmf)** - Comunidad oficial
- **[Stack Overflow](https://stackoverflow.com/questions/tagged/fastapi)** - Q&A técnico
- **[GitHub Issues](https://github.com/tiangolo/fastapi/issues)** - Reportar bugs
- **[Reddit r/FastAPI](https://reddit.com/r/FastAPI)** - Discusiones generales

### Blogs y Artículos Recomendados

- **[FastAPI Performance Tips](https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-11-dependency-injection/)** - Tutorial avanzado
- **[High Performance Python](https://realpython.com/python-performance/)** - Optimización Python
- **[Database Performance](https://use-the-index-luke.com/)** - Optimización SQL
- **[Redis Best Practices](https://redis.com/redis-best-practices/)** - Patrones Redis

### Libros Recomendados

- **"High Performance Python"** - Micha Gorelick, Ian Ozsvald
- **"Designing Data-Intensive Applications"** - Martin Kleppmann
- **"Site Reliability Engineering"** - Google SRE Team
- **"Building Microservices"** - Sam Newman

---

## 🚀 Próximos Pasos

Después de completar la semana 7, considera explorar:

1. **Microservices Architecture** - Descomponer monolito en servicios
2. **Message Queues** - Implementar processing asíncrono
3. **GraphQL** - APIs más eficientes para frontend
4. **gRPC** - Comunicación de alta performance
5. **Kubernetes** - Orquestación y escalabilidad
6. **Service Mesh** - Observabilidad avanzada
7. **Edge Computing** - Performance global

¡El journey de optimización nunca termina! 🎯
