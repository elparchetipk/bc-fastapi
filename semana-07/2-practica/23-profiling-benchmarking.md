# Práctica 23: Profiling y Benchmarking

## Objetivos de Aprendizaje

- Dominar herramientas de profiling para aplicaciones FastAPI
- Implementar benchmarking sistemático de endpoints
- Identificar hotspots y cuellos de botella de performance
- Analizar uso de memoria y CPU en aplicaciones reales

## Duración Estimada

⏱️ **60 minutos**

## Prerrequisitos

- Aplicación FastAPI funcional de semanas anteriores
- Conocimientos básicos de async/await
- Python 3.11+ instalado

---

## 📋 Contenido de la Práctica

### Parte 1: Setup de Herramientas de Profiling (15 min)

#### 1.1 Instalación de Herramientas

**Paso 1: Instalar dependencias de profiling**

```bash
# Herramientas de profiling
pip install py-spy memory-profiler line-profiler

# Herramientas de benchmarking
pip install locust httpx[cli]

# Métricas y monitoring
pip install psutil prometheus-client

# Actualizar requirements
echo "py-spy>=0.3.14" >> requirements-dev.txt
echo "memory-profiler>=0.61.0" >> requirements-dev.txt
echo "line-profiler>=4.1.1" >> requirements-dev.txt
echo "locust>=2.17.0" >> requirements-dev.txt
echo "psutil>=5.9.6" >> requirements-dev.txt
echo "prometheus-client>=0.19.0" >> requirements-dev.txt
```

#### 1.2 Configuración de Profiling en la Aplicación

**Crear app/core/profiling.py**

```python
import cProfile
import pstats
import io
import time
import functools
import psutil
import os
from typing import Any, Callable
from contextlib import contextmanager

class PerformanceProfiler:
    """Clase para profiling de performance en FastAPI."""

    def __init__(self):
        self.profiles = {}
        self.stats = {}

    @contextmanager
    def profile_context(self, name: str):
        """Context manager para profiling."""
        pr = cProfile.Profile()
        start_time = time.time()
        pr.enable()

        try:
            yield
        finally:
            pr.disable()
            end_time = time.time()

            # Guardar estadísticas
            s = io.StringIO()
            ps = pstats.Stats(pr, stream=s)
            ps.sort_stats('cumulative')

            self.profiles[name] = {
                'duration': end_time - start_time,
                'stats': ps,
                'timestamp': time.time()
            }

    def profile_function(self, func: Callable) -> Callable:
        """Decorator para profiling de funciones."""
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            with self.profile_context(func.__name__):
                return await func(*args, **kwargs)

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            with self.profile_context(func.__name__):
                return func(*args, **kwargs)

        return async_wrapper if hasattr(func, '__code__') and func.__code__.co_flags & 0x80 else sync_wrapper

    def get_stats(self, name: str) -> dict:
        """Obtener estadísticas de un profile."""
        if name not in self.profiles:
            return {}

        profile = self.profiles[name]
        s = io.StringIO()
        profile['stats'].print_stats(10, stream=s)

        return {
            'name': name,
            'duration': profile['duration'],
            'stats_text': s.getvalue(),
            'timestamp': profile['timestamp']
        }

    def get_system_stats(self) -> dict:
        """Obtener estadísticas del sistema."""
        process = psutil.Process(os.getpid())

        return {
            'cpu_percent': process.cpu_percent(),
            'memory_info': process.memory_info()._asdict(),
            'memory_percent': process.memory_percent(),
            'num_threads': process.num_threads(),
            'connections': len(process.connections()),
            'system_cpu': psutil.cpu_percent(),
            'system_memory': psutil.virtual_memory()._asdict()
        }

# Instancia global
profiler = PerformanceProfiler()
```

#### 1.3 Middleware de Performance

**Agregar a app/main.py**

```python
import time
from fastapi import Request, Response
from app.core.profiling import profiler

@app.middleware("http")
async def performance_middleware(request: Request, call_next):
    """Middleware para medir performance de requests."""
    start_time = time.time()

    # Información de la request
    endpoint = f"{request.method} {request.url.path}"

    # Procesar request
    response = await call_next(request)

    # Calcular métricas
    process_time = time.time() - start_time

    # Agregar headers de performance
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Endpoint"] = endpoint

    # Log performance
    print(f"🚀 {endpoint}: {process_time:.4f}s")

    return response

# Endpoint para estadísticas de profiling
@app.get("/debug/profile/{name}")
async def get_profile_stats(name: str):
    """Obtener estadísticas de profiling."""
    return profiler.get_stats(name)

@app.get("/debug/system")
async def get_system_stats():
    """Obtener estadísticas del sistema."""
    return profiler.get_system_stats()
```

### Parte 2: Profiling de Código Python (20 min)

#### 2.1 Profiling con cProfile

**Crear scripts/profile_app.py**

```python
#!/usr/bin/env python3

import cProfile
import pstats
import io
import asyncio
from app.main import app
from app.core.profiling import profiler

async def profile_endpoint_simulation():
    """Simular requests a endpoints para profiling."""
    from httpx import AsyncClient

    async with AsyncClient(app=app, base_url="http://test") as client:

        # Simular múltiples requests
        tasks = []
        for i in range(50):
            tasks.append(client.get(f"/users/{i % 10 + 1}"))
            tasks.append(client.get("/posts/"))
            if i % 5 == 0:
                tasks.append(client.post("/posts/", json={
                    "title": f"Test Post {i}",
                    "content": f"Content for post {i}"
                }))

        # Ejecutar todas las requests
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        print(f"Executed {len(responses)} requests")
        return responses

def run_profiling():
    """Ejecutar profiling completo."""
    print("🔍 Starting application profiling...")

    # Configurar profiler
    pr = cProfile.Profile()
    pr.enable()

    # Ejecutar simulación
    asyncio.run(profile_endpoint_simulation())

    pr.disable()

    # Analizar resultados
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s)
    ps.sort_stats('cumulative')

    print("\n📊 Profiling Results:")
    ps.print_stats(20)  # Top 20 functions

    print("\n📊 Functions that call others frequently:")
    ps.print_callers(10)

    # Guardar resultados en archivo
    with open("profile_results.txt", "w") as f:
        ps.print_stats(stream=f)

    print("\n💾 Results saved to profile_results.txt")

if __name__ == "__main__":
    run_profiling()
```

#### 2.2 Line-by-Line Profiling

**Crear scripts/line_profiler_example.py**

```python
#!/usr/bin/env python3

# Para usar line_profiler:
# 1. Instalar: pip install line_profiler
# 2. Agregar @profile a funciones que quieres analizar
# 3. Ejecutar: kernprof -l -v line_profiler_example.py

import time
import asyncio
from typing import List

@profile
def expensive_synchronous_operation(n: int) -> List[int]:
    """Operación sincrónica costosa para analizar."""
    result = []

    # Simulación de operación costosa
    for i in range(n):
        # Operación matemática compleja
        value = sum(x**2 for x in range(i % 100))
        result.append(value)

        # Simulación de I/O
        if i % 1000 == 0:
            time.sleep(0.001)  # 1ms delay

    return result

@profile
async def expensive_async_operation(n: int) -> List[int]:
    """Operación asíncrona costosa para analizar."""
    result = []

    for i in range(n):
        # Operación matemática
        value = sum(x**2 for x in range(i % 100))
        result.append(value)

        # Async I/O simulation
        if i % 1000 == 0:
            await asyncio.sleep(0.001)

    return result

@profile
def main():
    """Función principal para profiling."""
    # Test synchronous operation
    sync_result = expensive_synchronous_operation(10000)
    print(f"Sync result length: {len(sync_result)}")

    # Test asynchronous operation
    async def run_async():
        async_result = await expensive_async_operation(10000)
        print(f"Async result length: {len(async_result)}")

    asyncio.run(run_async())

if __name__ == "__main__":
    main()
```

#### 2.3 Memory Profiling

**Crear scripts/memory_profiler_example.py**

```python
#!/usr/bin/env python3

from memory_profiler import profile
import numpy as np
import pandas as pd

@profile
def memory_intensive_function():
    """Función para analizar uso de memoria."""

    # Crear lista grande
    big_list = []
    for i in range(100000):
        big_list.append(f"String number {i}")

    # Crear array de NumPy
    big_array = np.random.random((1000, 1000))

    # Crear DataFrame de Pandas
    df = pd.DataFrame({
        'col1': np.random.random(50000),
        'col2': np.random.randint(0, 100, 50000),
        'col3': [f"text_{i}" for i in range(50000)]
    })

    # Operaciones que consumen memoria
    df_grouped = df.groupby('col2').agg({
        'col1': ['mean', 'std', 'count'],
        'col3': 'count'
    })

    # Limpiar memoria (explícitamente)
    del big_list, big_array, df

    return df_grouped

@profile
def optimized_memory_function():
    """Versión optimizada para memoria."""

    # Usar generador en lugar de lista
    def string_generator(n):
        for i in range(n):
            yield f"String number {i}"

    # Procesar en chunks
    chunk_size = 10000
    total_count = 0

    for chunk_start in range(0, 100000, chunk_size):
        chunk_data = list(string_generator(chunk_size))
        total_count += len(chunk_data)
        del chunk_data  # Liberar memoria inmediatamente

    return total_count

if __name__ == "__main__":
    print("🧠 Memory profiling - Standard function:")
    result1 = memory_intensive_function()

    print("\n🧠 Memory profiling - Optimized function:")
    result2 = optimized_memory_function()

    print(f"\nResults: {len(result1)} vs {result2}")
```

### Parte 3: Benchmarking de Endpoints (15 min)

#### 3.1 Benchmarking con Locust

**Crear locustfile.py**

```python
from locust import HttpUser, task, between
import random
import json

class FastAPIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        """Setup inicial para cada usuario."""
        # Login si es necesario
        login_response = self.client.post("/auth/login", json={
            "username": "testuser@example.com",
            "password": "testpassword"
        })

        if login_response.status_code == 200:
            token = login_response.json().get("access_token")
            self.client.headers.update({"Authorization": f"Bearer {token}"})

    @task(5)
    def get_posts(self):
        """Test GET /posts/ - tarea más frecuente."""
        response = self.client.get("/posts/")
        if response.status_code != 200:
            print(f"GET /posts/ failed: {response.status_code}")

    @task(3)
    def get_single_post(self):
        """Test GET /posts/{id}."""
        post_id = random.randint(1, 100)
        response = self.client.get(f"/posts/{post_id}")
        # No verificar 404 porque puede ser válido

    @task(2)
    def get_user_profile(self):
        """Test GET /users/me."""
        response = self.client.get("/users/me")
        if response.status_code not in [200, 401]:
            print(f"GET /users/me failed: {response.status_code}")

    @task(1)
    def create_post(self):
        """Test POST /posts/ - tarea menos frecuente."""
        post_data = {
            "title": f"Load Test Post {random.randint(1, 10000)}",
            "content": f"This is a load test post created at {random.random()}",
            "tags": ["load-test", "performance"]
        }

        response = self.client.post("/posts/", json=post_data)
        if response.status_code not in [201, 401]:
            print(f"POST /posts/ failed: {response.status_code}")

    @task(1)
    def search_posts(self):
        """Test buscar posts."""
        search_terms = ["test", "python", "fastapi", "performance", "load"]
        term = random.choice(search_terms)

        response = self.client.get(f"/posts/search?q={term}")
        if response.status_code != 200:
            print(f"Search failed: {response.status_code}")

class HeavyUser(HttpUser):
    """Usuario que hace operaciones más pesadas."""
    wait_time = between(2, 5)
    weight = 1  # Menos usuarios de este tipo

    @task
    def heavy_operation(self):
        """Operación que consume más recursos."""
        # Crear múltiples posts en secuencia
        for i in range(5):
            post_data = {
                "title": f"Heavy Load Post {i}",
                "content": "Content " * 100  # Contenido más largo
            }
            self.client.post("/posts/", json=post_data)

    @task
    def bulk_read(self):
        """Leer múltiples recursos."""
        for i in range(10):
            self.client.get(f"/posts/{random.randint(1, 100)}")

# Configuración de test personalizada
class QuickTest(HttpUser):
    """Test rápido para desarrollo."""
    wait_time = between(0.5, 1)

    @task
    def quick_health_check(self):
        self.client.get("/health")

    @task
    def quick_posts_check(self):
        self.client.get("/posts/")
```

#### 3.2 Scripts de Benchmarking Automatizado

**Crear scripts/benchmark.py**

```python
#!/usr/bin/env python3

import subprocess
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics

class BenchmarkRunner:
    """Clase para ejecutar benchmarks automatizados."""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results = {}

    def simple_request_test(self, endpoint: str, num_requests: int = 100):
        """Test simple de múltiples requests."""
        print(f"🚀 Testing {endpoint} with {num_requests} requests...")

        times = []
        errors = 0

        def make_request():
            start_time = time.time()
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                end_time = time.time()

                if response.status_code == 200:
                    return end_time - start_time
                else:
                    return None
            except Exception as e:
                print(f"Error: {e}")
                return None

        # Ejecutar requests secuencialmente
        for i in range(num_requests):
            response_time = make_request()
            if response_time:
                times.append(response_time)
            else:
                errors += 1

            if i % 10 == 0:
                print(f"  Progress: {i}/{num_requests}")

        # Calcular estadísticas
        if times:
            stats = {
                'endpoint': endpoint,
                'requests': num_requests,
                'successful': len(times),
                'errors': errors,
                'min_time': min(times),
                'max_time': max(times),
                'avg_time': statistics.mean(times),
                'median_time': statistics.median(times),
                'p95_time': statistics.quantiles(times, n=20)[18] if len(times) > 20 else max(times),
                'total_time': sum(times)
            }
        else:
            stats = {'error': 'No successful requests'}

        self.results[endpoint] = stats
        return stats

    def concurrent_request_test(self, endpoint: str, num_requests: int = 100, concurrency: int = 10):
        """Test con requests concurrentes."""
        print(f"🚀 Concurrent test {endpoint}: {num_requests} requests, {concurrency} concurrent...")

        times = []
        errors = 0

        def make_request():
            start_time = time.time()
            try:
                response = requests.get(f"{self.base_url}{endpoint}")
                end_time = time.time()

                if response.status_code == 200:
                    return end_time - start_time
                else:
                    return None
            except Exception:
                return None

        # Ejecutar requests concurrentemente
        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            futures = [executor.submit(make_request) for _ in range(num_requests)]

            for future in as_completed(futures):
                response_time = future.result()
                if response_time:
                    times.append(response_time)
                else:
                    errors += 1

        # Calcular estadísticas
        if times:
            stats = {
                'endpoint': endpoint,
                'requests': num_requests,
                'concurrency': concurrency,
                'successful': len(times),
                'errors': errors,
                'min_time': min(times),
                'max_time': max(times),
                'avg_time': statistics.mean(times),
                'median_time': statistics.median(times),
                'p95_time': statistics.quantiles(times, n=20)[18] if len(times) > 20 else max(times),
                'requests_per_second': len(times) / max(times) if times else 0
            }
        else:
            stats = {'error': 'No successful requests'}

        concurrent_key = f"{endpoint}_concurrent"
        self.results[concurrent_key] = stats
        return stats

    def run_apache_bench(self, endpoint: str, num_requests: int = 1000, concurrency: int = 10):
        """Ejecutar Apache Bench (ab) si está disponible."""
        try:
            cmd = [
                'ab',
                '-n', str(num_requests),
                '-c', str(concurrency),
                '-g', f'ab_results_{endpoint.replace("/", "_")}.tsv',
                f"{self.base_url}{endpoint}"
            ]

            print(f"🔧 Running Apache Bench: {' '.join(cmd)}")
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

            if result.returncode == 0:
                print("✅ Apache Bench completed successfully")
                # Parsear resultados básicos
                output = result.stdout
                stats = self.parse_ab_output(output)
                self.results[f"{endpoint}_ab"] = stats
                return stats
            else:
                print(f"❌ Apache Bench failed: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            print("⏰ Apache Bench timed out")
            return None
        except FileNotFoundError:
            print("⚠️ Apache Bench not found. Install with: apt-get install apache2-utils")
            return None

    def parse_ab_output(self, output: str) -> dict:
        """Parsear output de Apache Bench."""
        lines = output.split('\n')
        stats = {}

        for line in lines:
            if 'Requests per second:' in line:
                stats['requests_per_second'] = float(line.split(':')[1].strip().split()[0])
            elif 'Time per request:' in line and 'mean' in line:
                stats['time_per_request_mean'] = float(line.split(':')[1].strip().split()[0])
            elif 'Transfer rate:' in line:
                stats['transfer_rate'] = float(line.split(':')[1].strip().split()[0])

        return stats

    def generate_report(self):
        """Generar reporte de resultados."""
        print("\n📊 BENCHMARK RESULTS SUMMARY")
        print("=" * 50)

        for endpoint, stats in self.results.items():
            if 'error' in stats:
                print(f"\n❌ {endpoint}: {stats['error']}")
                continue

            print(f"\n📈 {endpoint}:")
            if 'successful' in stats:
                print(f"  Successful requests: {stats['successful']}/{stats.get('requests', 'N/A')}")
                print(f"  Average time: {stats['avg_time']:.4f}s")
                print(f"  Median time: {stats['median_time']:.4f}s")
                print(f"  95th percentile: {stats.get('p95_time', 'N/A'):.4f}s")
                if 'requests_per_second' in stats:
                    print(f"  Requests/second: {stats['requests_per_second']:.2f}")

        # Guardar resultados en JSON
        with open('benchmark_results.json', 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n💾 Detailed results saved to benchmark_results.json")

def main():
    """Función principal de benchmarking."""
    benchmark = BenchmarkRunner()

    # Endpoints a testear
    endpoints = [
        "/health",
        "/posts/",
        "/users/me",
        "/posts/1"
    ]

    print("🚀 Starting benchmark tests...")

    for endpoint in endpoints:
        # Test secuencial
        benchmark.simple_request_test(endpoint, num_requests=50)
        time.sleep(1)

        # Test concurrente
        benchmark.concurrent_request_test(endpoint, num_requests=100, concurrency=5)
        time.sleep(1)

        # Apache Bench (si está disponible)
        benchmark.run_apache_bench(endpoint, num_requests=500, concurrency=10)
        time.sleep(2)

    # Generar reporte
    benchmark.generate_report()

if __name__ == "__main__":
    main()
```

### Parte 4: Análisis de Resultados y Optimización (10 min)

#### 4.1 Dashboard de Performance

**Crear app/api/debug.py**

```python
from fastapi import APIRouter, Depends
from app.core.profiling import profiler
import psutil
import time

router = APIRouter(prefix="/debug", tags=["debug"])

@router.get("/performance")
async def get_performance_dashboard():
    """Dashboard de performance en tiempo real."""

    # Estadísticas del sistema
    system_stats = profiler.get_system_stats()

    # Información del proceso
    process = psutil.Process()

    # Estadísticas de red si hay conexiones
    connections = []
    try:
        for conn in process.connections():
            connections.append({
                'fd': conn.fd,
                'family': conn.family.name if conn.family else 'unknown',
                'type': conn.type.name if conn.type else 'unknown',
                'laddr': f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else None,
                'raddr': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else None,
                'status': conn.status
            })
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        connections = []

    return {
        'timestamp': time.time(),
        'system': system_stats,
        'process': {
            'pid': process.pid,
            'create_time': process.create_time(),
            'cpu_times': process.cpu_times()._asdict(),
            'memory_full_info': process.memory_full_info()._asdict(),
            'io_counters': process.io_counters()._asdict() if hasattr(process, 'io_counters') else {},
            'num_fds': process.num_fds() if hasattr(process, 'num_fds') else None,
            'connections': connections[:10]  # Limitar a 10 para no sobrecargar
        },
        'profiles': list(profiler.profiles.keys())
    }

@router.get("/performance/endpoint/{endpoint_name}")
async def get_endpoint_performance(endpoint_name: str):
    """Performance específica de un endpoint."""
    stats = profiler.get_stats(endpoint_name)
    return stats

@router.post("/performance/clear")
async def clear_performance_data():
    """Limpiar datos de performance."""
    profiler.profiles.clear()
    profiler.stats.clear()
    return {"message": "Performance data cleared"}

# Agregar al main.py
# app.include_router(debug.router)
```

#### 4.2 Script de Análisis Automatizado

**Crear scripts/analyze_performance.py**

```python
#!/usr/bin/env python3

import json
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

def analyze_benchmark_results():
    """Analizar resultados de benchmark y generar reportes."""

    # Cargar resultados
    results_file = Path("benchmark_results.json")
    if not results_file.exists():
        print("❌ No benchmark results found. Run benchmark.py first.")
        return

    with open(results_file) as f:
        results = json.load(f)

    # Preparar datos para análisis
    data = []
    for endpoint, stats in results.items():
        if 'error' not in stats and 'avg_time' in stats:
            data.append({
                'endpoint': endpoint,
                'avg_time': stats['avg_time'],
                'median_time': stats['median_time'],
                'p95_time': stats.get('p95_time', stats['max_time']),
                'requests_per_second': stats.get('requests_per_second', 0),
                'successful_requests': stats.get('successful', 0),
                'error_rate': stats.get('errors', 0) / stats.get('requests', 1) * 100
            })

    if not data:
        print("❌ No valid data to analyze")
        return

    df = pd.DataFrame(data)

    # Generar gráficos
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('API Performance Analysis', fontsize=16)

    # Gráfico 1: Response Times
    axes[0, 0].bar(df['endpoint'], df['avg_time'])
    axes[0, 0].set_title('Average Response Time by Endpoint')
    axes[0, 0].set_ylabel('Time (seconds)')
    axes[0, 0].tick_params(axis='x', rotation=45)

    # Gráfico 2: Throughput
    throughput_data = df[df['requests_per_second'] > 0]
    if not throughput_data.empty:
        axes[0, 1].bar(throughput_data['endpoint'], throughput_data['requests_per_second'])
        axes[0, 1].set_title('Requests per Second by Endpoint')
        axes[0, 1].set_ylabel('Requests/sec')
        axes[0, 1].tick_params(axis='x', rotation=45)

    # Gráfico 3: Response Time Distribution
    axes[1, 0].boxplot([df['avg_time'], df['median_time'], df['p95_time']],
                       labels=['Average', 'Median', '95th Percentile'])
    axes[1, 0].set_title('Response Time Distribution')
    axes[1, 0].set_ylabel('Time (seconds)')

    # Gráfico 4: Error Rates
    axes[1, 1].bar(df['endpoint'], df['error_rate'])
    axes[1, 1].set_title('Error Rate by Endpoint')
    axes[1, 1].set_ylabel('Error Rate (%)')
    axes[1, 1].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

    # Generar reporte textual
    print("\n📊 PERFORMANCE ANALYSIS REPORT")
    print("=" * 50)

    # Mejores y peores performers
    best_response_time = df.loc[df['avg_time'].idxmin()]
    worst_response_time = df.loc[df['avg_time'].idxmax()]

    print(f"\n🏆 Best Response Time: {best_response_time['endpoint']} ({best_response_time['avg_time']:.4f}s)")
    print(f"🐌 Worst Response Time: {worst_response_time['endpoint']} ({worst_response_time['avg_time']:.4f}s)")

    if df['requests_per_second'].max() > 0:
        best_throughput = df.loc[df['requests_per_second'].idxmax()]
        print(f"🚀 Best Throughput: {best_throughput['endpoint']} ({best_throughput['requests_per_second']:.2f} req/s)")

    # Recomendaciones
    print(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")

    slow_endpoints = df[df['avg_time'] > 0.2]  # > 200ms
    if not slow_endpoints.empty:
        print(f"⚠️ Slow endpoints (>200ms): {', '.join(slow_endpoints['endpoint'])}")
        print("   Recommendations: Add caching, optimize queries, add indexing")

    high_error_endpoints = df[df['error_rate'] > 5]  # > 5% error rate
    if not high_error_endpoints.empty:
        print(f"🚨 High error rate endpoints: {', '.join(high_error_endpoints['endpoint'])}")
        print("   Recommendations: Check error handling, validate input, monitor dependencies")

    low_throughput = df[df['requests_per_second'] < 100]  # < 100 req/s
    if not low_throughput.empty:
        print(f"📉 Low throughput endpoints: {', '.join(low_throughput['endpoint'])}")
        print("   Recommendations: Optimize database queries, implement caching, use async operations")

    print(f"\n📈 Summary Statistics:")
    print(f"   Average response time: {df['avg_time'].mean():.4f}s")
    print(f"   Median response time: {df['median_time'].median():.4f}s")
    print(f"   Total successful requests: {df['successful_requests'].sum()}")
    print(f"   Average error rate: {df['error_rate'].mean():.2f}%")

if __name__ == "__main__":
    try:
        analyze_benchmark_results()
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Install with: pip install matplotlib pandas")
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Profile Your App

1. **Ejecutar profiling** en tu aplicación actual
2. **Identificar** las 5 funciones más lentas
3. **Documentar** hallazgos en un reporte

### Ejercicio 2: Benchmark Comparison

1. **Ejecutar benchmark** en múltiples endpoints
2. **Comparar** performance antes y después de optimizaciones
3. **Generar gráficos** de comparación

### Ejercicio 3: Memory Analysis

1. **Identificar** operaciones que consumen mucha memoria
2. **Optimizar** al menos una función memory-intensive
3. **Validar** mejoras con memory profiler

---

## ✅ Criterios de Evaluación

### Nivel Básico (60-70%)

- [ ] Configura herramientas básicas de profiling
- [ ] Ejecuta benchmarks simples
- [ ] Identifica problemas obvios de performance

### Nivel Intermedio (71-85%)

- [ ] Usa múltiples herramientas de profiling
- [ ] Analiza resultados sistemáticamente
- [ ] Implementa monitoring básico

### Nivel Avanzado (86-100%)

- [ ] Integra profiling en workflow de desarrollo
- [ ] Automatiza benchmarking
- [ ] Crea dashboards de performance

---

## 🎯 Próximos Pasos

1. **Identificar cuellos de botella** usando las herramientas aprendidas
2. **Optimizar código** basado en findings de profiling
3. **Implementar monitoring** continuo de performance
4. **Preparar para Práctica 24**: Optimización de base de datos

---

_El profiling efectivo es la base de toda optimización. Sin mediciones precisas, las optimizaciones son solo conjeturas._
