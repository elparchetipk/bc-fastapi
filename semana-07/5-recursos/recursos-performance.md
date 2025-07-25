# Recursos de Apoyo - Semana 7: Performance y Monitoreo

## 📚 Documentación Oficial

### FastAPI y Performance

- **[FastAPI Advanced User Guide](https://fastapi.tiangolo.com/advanced/)** - Guía avanzada oficial
- **[Async SQL Databases](https://fastapi.tiangolo.com/advanced/async-sql-databases/)** - Uso asíncrono de bases de datos
- **[Dependencies with yield](https://fastapi.tiangolo.com/advanced/dependencies-with-yield/)** - Gestión de recursos
- **[Testing Dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/)** - Testing para performance

### SQLAlchemy y Optimización

- **[Loading Techniques](https://docs.sqlalchemy.org/en/14/orm/loading_techniques.html)** - Técnicas de carga optimizada
- **[Query API](https://docs.sqlalchemy.org/en/14/orm/query.html)** - API de consultas
- **[Relationship Loading](https://docs.sqlalchemy.org/en/14/orm/loading_relationships.html)** - Carga de relaciones
- **[Performance Tips](https://docs.sqlalchemy.org/en/14/orm/tutorial.html#performance-tips)** - Tips de rendimiento

### Redis y Caching

- **[Redis Documentation](https://redis.io/documentation)** - Documentación completa
- **[Redis Best Practices](https://redis.io/docs/manual/clients-guide/)** - Mejores prácticas
- **[Caching Patterns](https://redis.io/docs/manual/patterns/)** - Patrones de cache
- **[Redis Python Client](https://redis-py.readthedocs.io/)** - Cliente Python oficial

### Prometheus y Monitoreo

- **[Prometheus Documentation](https://prometheus.io/docs/)** - Documentación oficial
- **[Client Libraries](https://prometheus.io/docs/instrumenting/clientlibs/)** - Librerías cliente
- **[Best Practices](https://prometheus.io/docs/practices/naming/)** - Mejores prácticas
- **[Query Language](https://prometheus.io/docs/prometheus/latest/querying/basics/)** - PromQL

---

## 🛠️ Herramientas y Librerías

### Profiling y Debugging

```bash
# Herramientas de profiling
pip install py-spy              # Profiling sin modificar código
pip install memory-profiler     # Análisis de memoria
pip install line-profiler       # Profiling línea por línea
pip install pyflame             # Profiling de llama
pip install scalene             # Profiler moderno con GPU support
```

### Monitoreo y Métricas

```bash
# Librerías de monitoreo
pip install prometheus-client   # Cliente Prometheus para Python
pip install psutil             # Información del sistema
pip install datadog            # Integración con Datadog
pip install newrelic           # New Relic APM
pip install sentry-sdk         # Error tracking
```

### Testing y Benchmarking

```bash
# Herramientas de testing
pip install locust             # Load testing
pip install pytest-benchmark   # Benchmarking en pytest
pip install httpx             # Cliente HTTP async
pip install aiohttp           # Cliente/servidor HTTP async
```

### Bases de Datos y Cache

```bash
# Optimización de BD y cache
pip install redis             # Cliente Redis
pip install asyncpg           # Driver PostgreSQL async
pip install databases         # ORM async wrapper
pip install sqlalchemy-utils  # Utilidades SQLAlchemy
```

---

## 🎯 Tutoriales y Guías Prácticas

### Performance Optimization

1. **[FastAPI Performance Tuning](https://testdriven.io/blog/fastapi-performance/)** - Guía completa de optimización
2. **[Python Performance Tips](https://wiki.python.org/moin/PythonSpeed/PerformanceTips)** - Tips generales de Python
3. **[Database Performance](https://use-the-index-luke.com/)** - Guía de índices y optimización SQL
4. **[Async Python Patterns](https://docs.python.org/3/library/asyncio-task.html)** - Patrones asíncronos

### Caching Strategies

1. **[Redis Caching Strategies](https://redis.com/redis-best-practices/caching/)** - Estrategias de cache
2. **[HTTP Caching](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)** - Cache HTTP
3. **[Application-Level Caching](https://realpython.com/caching-in-python/)** - Cache en aplicaciones Python
4. **[Cache Invalidation](https://martinfowler.com/bliki/TwoHardThings.html)** - Invalidación de cache

### Monitoring and Observability

1. **[The Four Golden Signals](https://sre.google/sre-book/monitoring-distributed-systems/)** - Señales doradas de monitoreo
2. **[Prometheus Monitoring](https://prometheus.io/docs/guides/go-application/)** - Guía de monitoreo
3. **[Distributed Tracing](https://opentracing.io/guides/python/)** - Tracing distribuido
4. **[Log Aggregation](https://www.elastic.co/guide/en/logstash/current/introduction.html)** - Agregación de logs

---

## 🧪 Ejemplos de Código

### Profiling Automático

```python
# decorador_profiling.py
import cProfile
import functools
import io
import pstats

def profile(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()

        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        print(s.getvalue())

        return result
    return wrapper

# Uso
@profile
def expensive_function():
    return sum(i*i for i in range(10000))
```

### Cache con TTL Dinámico

```python
# cache_dinamico.py
import time
from functools import wraps
from typing import Dict, Any, Optional

class DynamicCache:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._access_count: Dict[str, int] = {}

    def get_ttl(self, key: str) -> int:
        """TTL dinámico basado en frecuencia de acceso"""
        access_count = self._access_count.get(key, 0)
        if access_count > 100:
            return 3600  # 1 hora para datos muy accedidos
        elif access_count > 10:
            return 900   # 15 minutos para datos moderadamente accedidos
        else:
            return 300   # 5 minutos para datos poco accedidos

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None

        item = self._cache[key]
        if time.time() > item['expires']:
            del self._cache[key]
            return None

        self._access_count[key] = self._access_count.get(key, 0) + 1
        return item['value']

    def set(self, key: str, value: Any) -> None:
        ttl = self.get_ttl(key)
        self._cache[key] = {
            'value': value,
            'expires': time.time() + ttl
        }

# Uso
cache = DynamicCache()

def cached_with_dynamic_ttl(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

        result = cache.get(cache_key)
        if result is not None:
            return result

        result = func(*args, **kwargs)
        cache.set(cache_key, result)
        return result
    return wrapper
```

### Métricas Personalizadas

```python
# metricas_custom.py
from prometheus_client import Counter, Histogram, Gauge
import time
import functools

# Métricas personalizadas
BUSINESS_TRANSACTIONS = Counter(
    'business_transactions_total',
    'Total business transactions',
    ['transaction_type', 'status']
)

USER_SESSIONS = Gauge(
    'active_user_sessions',
    'Active user sessions'
)

CACHE_PERFORMANCE = Histogram(
    'cache_operation_duration_seconds',
    'Cache operation duration',
    ['operation']
)

def track_business_metric(transaction_type: str):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                BUSINESS_TRANSACTIONS.labels(
                    transaction_type=transaction_type,
                    status='success'
                ).inc()
                return result
            except Exception as e:
                BUSINESS_TRANSACTIONS.labels(
                    transaction_type=transaction_type,
                    status='error'
                ).inc()
                raise
        return wrapper
    return decorator

# Uso
@track_business_metric('user_registration')
async def register_user(user_data: dict):
    # Lógica de registro
    pass
```

### Health Check Avanzado

```python
# health_check_avanzado.py
from fastapi import APIRouter, Depends, HTTPException
import asyncio
import time
from typing import Dict, Any

router = APIRouter()

class HealthChecker:
    def __init__(self):
        self.checks = []
        self.cache = {}
        self.cache_ttl = 30  # 30 segundos

    def register_check(self, name: str, check_func, timeout: int = 5):
        """Registrar un health check"""
        self.checks.append({
            'name': name,
            'func': check_func,
            'timeout': timeout
        })

    async def run_check(self, check: Dict[str, Any]) -> Dict[str, Any]:
        """Ejecutar un health check individual"""
        start_time = time.time()

        try:
            result = await asyncio.wait_for(
                check['func'](),
                timeout=check['timeout']
            )

            return {
                'status': 'healthy',
                'response_time': time.time() - start_time,
                'details': result
            }
        except asyncio.TimeoutError:
            return {
                'status': 'timeout',
                'response_time': time.time() - start_time,
                'error': f"Check timed out after {check['timeout']}s"
            }
        except Exception as e:
            return {
                'status': 'unhealthy',
                'response_time': time.time() - start_time,
                'error': str(e)
            }

    async def run_all_checks(self) -> Dict[str, Any]:
        """Ejecutar todos los health checks"""
        cache_key = 'all_checks'

        # Verificar cache
        if cache_key in self.cache:
            cached_time, cached_result = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                cached_result['cached'] = True
                return cached_result

        # Ejecutar checks en paralelo
        tasks = [
            self.run_check(check) for check in self.checks
        ]

        results = await asyncio.gather(*tasks)

        # Compilar resultado
        overall_status = 'healthy'
        check_results = {}

        for check, result in zip(self.checks, results):
            check_results[check['name']] = result

            if result['status'] == 'unhealthy':
                overall_status = 'unhealthy'
            elif result['status'] == 'timeout' and overall_status == 'healthy':
                overall_status = 'degraded'

        final_result = {
            'status': overall_status,
            'timestamp': time.time(),
            'checks': check_results,
            'cached': False
        }

        # Cachear resultado
        self.cache[cache_key] = (time.time(), final_result)

        return final_result

# Ejemplo de uso
health_checker = HealthChecker()

async def check_database():
    # Simular check de base de datos
    await asyncio.sleep(0.1)
    return {'connections': 10, 'slow_queries': 2}

async def check_redis():
    # Simular check de Redis
    await asyncio.sleep(0.05)
    return {'memory_usage': '45MB', 'connected_clients': 5}

# Registrar checks
health_checker.register_check('database', check_database)
health_checker.register_check('redis', check_redis)

@router.get('/health')
async def health_endpoint():
    return await health_checker.run_all_checks()
```

---

## 📊 Dashboards y Visualización

### Grafana Dashboards

```json
// grafana_dashboard.json
{
  "dashboard": {
    "title": "FastAPI Performance Dashboard",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{method}} {{endpoint}}"
          }
        ]
      },
      {
        "title": "Response Time",
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
            "legendFormat": "95th percentile"
          }
        ]
      }
    ]
  }
}
```

### Dashboard HTML Simple

```html
<!-- dashboard_simple.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Performance Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <meta
      http-equiv="refresh"
      content="10" />
  </head>
  <body>
    <div class="container">
      <h1>FastAPI Performance Dashboard</h1>

      <div class="metrics-grid">
        <div class="metric-card">
          <h3>Active Requests</h3>
          <div
            class="metric-value"
            id="active-requests">
            0
          </div>
        </div>

        <div class="metric-card">
          <h3>Average Response Time</h3>
          <div
            class="metric-value"
            id="avg-response-time">
            0ms
          </div>
        </div>

        <div class="metric-card">
          <h3>Cache Hit Rate</h3>
          <div
            class="metric-value"
            id="cache-hit-rate">
            0%
          </div>
        </div>
      </div>

      <canvas id="performanceChart"></canvas>
    </div>

    <script>
      async function updateMetrics() {
        try {
          const response = await fetch('/monitoring/metrics/summary');
          const data = await response.json();

          document.getElementById('active-requests').textContent =
            data.active_requests;
          document.getElementById('avg-response-time').textContent =
            data.avg_response_time.toFixed(2) + 'ms';
          document.getElementById('cache-hit-rate').textContent =
            (data.cache_hit_rate * 100).toFixed(1) + '%';
        } catch (error) {
          console.error('Error updating metrics:', error);
        }
      }

      // Actualizar cada 5 segundos
      setInterval(updateMetrics, 5000);
      updateMetrics(); // Inicial
    </script>
  </body>
</html>
```

---

## 🔧 Scripts de Utilidad

### Script de Generación de Datos

```python
# generate_test_data.py
import asyncio
from sqlalchemy.orm import Session
from faker import Faker
import random
from app.database import get_db
from app.models import User, Post, Comment

fake = Faker()

async def generate_users(db: Session, count: int = 1000):
    """Generar usuarios de prueba"""
    users = []
    for i in range(count):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            full_name=fake.name(),
            is_active=random.choice([True, False])
        )
        users.append(user)

        if len(users) >= 100:  # Batch insert
            db.add_all(users)
            db.commit()
            users = []

    if users:
        db.add_all(users)
        db.commit()

async def generate_posts(db: Session, count: int = 5000):
    """Generar posts de prueba"""
    users = db.query(User).all()
    user_ids = [user.id for user in users]

    posts = []
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            content=fake.text(max_nb_chars=2000),
            author_id=random.choice(user_ids),
            published=random.choice([True, False])
        )
        posts.append(post)

        if len(posts) >= 100:
            db.add_all(posts)
            db.commit()
            posts = []

    if posts:
        db.add_all(posts)
        db.commit()

if __name__ == "__main__":
    db = next(get_db())

    print("Generating test data...")
    asyncio.run(generate_users(db, 1000))
    asyncio.run(generate_posts(db, 5000))
    print("Test data generated successfully!")
```

### Script de Benchmark

```python
# benchmark.py
import asyncio
import aiohttp
import time
import statistics
from typing import List

class PerformanceBenchmark:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []

    async def single_request(self, session: aiohttp.ClientSession, endpoint: str) -> float:
        """Realizar una request y medir tiempo"""
        start_time = time.time()

        try:
            async with session.get(f"{self.base_url}{endpoint}") as response:
                await response.text()
                return time.time() - start_time
        except Exception as e:
            print(f"Error in request to {endpoint}: {e}")
            return -1

    async def load_test(self, endpoint: str, concurrent_users: int = 10, requests_per_user: int = 10):
        """Realizar load test"""
        print(f"Load testing {endpoint} with {concurrent_users} users, {requests_per_user} requests each")

        async with aiohttp.ClientSession() as session:
            tasks = []

            for user in range(concurrent_users):
                for request in range(requests_per_user):
                    task = asyncio.create_task(
                        self.single_request(session, endpoint)
                    )
                    tasks.append(task)

            start_time = time.time()
            response_times = await asyncio.gather(*tasks)
            total_time = time.time() - start_time

            # Filtrar errores
            valid_times = [t for t in response_times if t > 0]

            if valid_times:
                return {
                    'endpoint': endpoint,
                    'total_requests': len(valid_times),
                    'total_time': total_time,
                    'requests_per_second': len(valid_times) / total_time,
                    'avg_response_time': statistics.mean(valid_times),
                    'median_response_time': statistics.median(valid_times),
                    'p95_response_time': statistics.quantiles(valid_times, n=20)[18],  # 95th percentile
                    'min_response_time': min(valid_times),
                    'max_response_time': max(valid_times),
                    'error_rate': (len(response_times) - len(valid_times)) / len(response_times) * 100
                }
            else:
                return {'error': 'All requests failed'}

    async def run_benchmark_suite(self):
        """Ejecutar suite completo de benchmarks"""
        endpoints = [
            '/users/',
            '/posts/',
            '/users/1',
            '/users/1/posts',
            '/stats/global'
        ]

        for endpoint in endpoints:
            result = await self.load_test(endpoint)
            self.results.append(result)
            print(f"Completed: {endpoint}")

            # Pausa entre tests
            await asyncio.sleep(2)

    def generate_report(self):
        """Generar reporte de resultados"""
        print("\n" + "="*80)
        print("PERFORMANCE BENCHMARK REPORT")
        print("="*80)

        for result in self.results:
            if 'error' in result:
                print(f"\nEndpoint: {result.get('endpoint', 'Unknown')} - FAILED")
                continue

            print(f"\nEndpoint: {result['endpoint']}")
            print(f"  Total Requests: {result['total_requests']}")
            print(f"  Requests/sec: {result['requests_per_second']:.2f}")
            print(f"  Avg Response Time: {result['avg_response_time']*1000:.2f}ms")
            print(f"  Median Response Time: {result['median_response_time']*1000:.2f}ms")
            print(f"  95th Percentile: {result['p95_response_time']*1000:.2f}ms")
            print(f"  Error Rate: {result['error_rate']:.2f}%")

if __name__ == "__main__":
    benchmark = PerformanceBenchmark("http://localhost:8000")

    async def main():
        await benchmark.run_benchmark_suite()
        benchmark.generate_report()

    asyncio.run(main())
```

---

## 📖 Recursos de Aprendizaje

### Libros Recomendados

1. **"High Performance Python"** - Micha Gorelick & Ian Ozsvald
2. **"Effective Python"** - Brett Slatkin
3. **"Site Reliability Engineering"** - Google SRE Team
4. **"Designing Data-Intensive Applications"** - Martin Kleppmann

### Cursos Online

1. **[Python Performance](https://realpython.com/python-performance/)** - Real Python
2. **[Database Performance](https://www.postgresqltutorial.com/postgresql-performance/)** - PostgreSQL Tutorial
3. **[Redis University](https://university.redis.com/)** - Cursos oficiales de Redis
4. **[Prometheus Monitoring](https://training.promlabs.com/)** - Training oficial

### Blogs y Artículos

1. **[FastAPI Performance Tips](https://testdriven.io/blog/fastapi-performance/)** - Test Driven IO
2. **[Python Performance](https://wiki.python.org/moin/PythonSpeed)** - Python Wiki
3. **[Redis Best Practices](https://redis.com/redis-best-practices/)** - Redis Labs
4. **[Monitoring Best Practices](https://sre.google/sre-book/)** - Google SRE

### Comunidades

1. **[FastAPI Discord](https://discord.gg/VQjSZaeJmf)** - Comunidad oficial
2. **[Python Performance](https://www.reddit.com/r/Python/)** - Reddit Python
3. **[Redis Community](https://redis.io/community)** - Comunidad Redis
4. **[SRE Community](https://www.reddit.com/r/sre/)** - Site Reliability Engineering

---

## 🎯 Checklist de Recursos

### Para Profiling

- [ ] py-spy instalado y configurado
- [ ] memory-profiler para análisis de memoria
- [ ] line-profiler para profiling detallado
- [ ] Scripts de benchmark personalizados

### Para Caching

- [ ] Redis configurado y funcionando
- [ ] Decoradores de cache implementados
- [ ] Estrategias de invalidación definidas
- [ ] Monitoreo de hit/miss ratio

### Para Monitoreo

- [ ] Prometheus client configurado
- [ ] Métricas personalizadas definidas
- [ ] Health checks implementados
- [ ] Dashboard básico funcionando

### Para Testing

- [ ] locust para load testing
- [ ] pytest-benchmark para micro-benchmarks
- [ ] Scripts de generación de datos
- [ ] Reportes automatizados

---

_Estos recursos están diseñados para complementar el aprendizaje de la Semana 7 y proporcionar referencias continuas para proyectos futuros._
