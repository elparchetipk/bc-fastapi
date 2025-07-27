# Ejercicios de Optimización y Performance

## Introducción

Esta sección contiene ejercicios prácticos para aplicar los conceptos de optimización y performance aprendidos en las prácticas 23-26. Los ejercicios están diseñados para reforzar el aprendizaje y proporcionar experiencia práctica con técnicas de optimización reales.

## Tiempo Estimado

3-4 horas para completar todos los ejercicios

---

## Ejercicio 1: Implementación de Cache Estratégico (45 minutos)

### Contexto

Tienes una API de e-commerce que consulta frecuentemente la misma información de productos, categorías y precios. Necesitas implementar un sistema de cache inteligente.

### Tareas

#### 1.1 Cache de Productos

Implementa un sistema de cache para productos que:

- Cache productos por ID por 15 minutos
- Cache listados de productos por categoría por 5 minutos
- Invalide automáticamente el cache cuando se actualiza un producto

```python
# Completar la implementación
from fastapi import FastAPI, Depends
import redis
import json
from typing import List, Optional

app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379, db=0)

class Product:
    def __init__(self, id: int, name: str, price: float, category: str):
        self.id = id
        self.name = name
        self.price = price
        self.category = category

# TODO: Implementar ProductCacheManager
class ProductCacheManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        # TODO: Definir TTLs y prefijos de keys

    async def get_product(self, product_id: int) -> Optional[Product]:
        # TODO: Implementar get con cache
        pass

    async def set_product(self, product: Product):
        # TODO: Implementar set con TTL
        pass

    async def get_products_by_category(self, category: str) -> List[Product]:
        # TODO: Implementar get lista con cache
        pass

    async def invalidate_product(self, product_id: int):
        # TODO: Implementar invalidación
        pass

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    # TODO: Usar cache manager
    pass

@app.get("/products/category/{category}")
async def get_products_by_category(category: str):
    # TODO: Usar cache manager
    pass

@app.put("/products/{product_id}")
async def update_product(product_id: int, product_data: dict):
    # TODO: Actualizar producto e invalidar cache
    pass
```

#### 1.2 Métricas de Cache

Implementa un sistema para medir la efectividad del cache:

```python
# TODO: Implementar CacheMetrics
class CacheMetrics:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    def record_hit(self, cache_type: str):
        # TODO: Registrar cache hit
        pass

    def record_miss(self, cache_type: str):
        # TODO: Registrar cache miss
        pass

    def get_hit_rate(self, cache_type: str) -> float:
        # TODO: Calcular hit rate
        pass

    def get_stats(self) -> dict:
        # TODO: Obtener estadísticas completas
        pass
```

### Criterios de Evaluación

- [ ] Cache de productos implementado correctamente
- [ ] TTLs configurados apropiadamente
- [ ] Invalidación de cache funcionando
- [ ] Métricas de cache tracking hits/misses
- [ ] Hit rate superior al 70% en pruebas

---

## Ejercicio 2: Optimización de Base de Datos (60 minutos)

### Contexto

Una API de gestión de usuarios tiene problemas de performance en consultas complejas. Necesitas optimizar las queries y la estructura de la base de datos.

### Tareas

#### 2.1 Análisis de Queries Lentas

Dado el siguiente modelo de datos:

```python
# models.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    created_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    content = Column(Text)
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    created_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
```

#### TODO: Optimizar estas queries problemáticas

```python
# queries.py - OPTIMIZAR ESTAS QUERIES
from sqlalchemy.orm import Session
from sqlalchemy import func

# Query 1: Usuarios con más posts (LENTA)
def get_most_active_users(db: Session, limit: int = 10):
    # TODO: Optimizar esta query que tarda mucho
    users = db.query(User).all()
    user_post_counts = []
    for user in users:
        post_count = len(user.posts)
        user_post_counts.append((user, post_count))

    # Ordenar por post count
    user_post_counts.sort(key=lambda x: x[1], reverse=True)
    return user_post_counts[:limit]

# Query 2: Posts con conteo de comentarios (LENTA)
def get_posts_with_comment_count(db: Session, page: int = 1, size: int = 20):
    # TODO: Optimizar - hace N+1 queries
    posts = db.query(Post).offset((page-1)*size).limit(size).all()
    result = []
    for post in posts:
        comment_count = len(post.comments)
        result.append({
            "post": post,
            "comment_count": comment_count
        })
    return result

# Query 3: Búsqueda de usuarios (LENTA)
def search_users(db: Session, search_term: str):
    # TODO: Optimizar - no usa índices
    return db.query(User).filter(
        User.first_name.contains(search_term) |
        User.last_name.contains(search_term) |
        User.username.contains(search_term)
    ).all()

# Query 4: Dashboard data (MÚLTIPLES QUERIES)
def get_dashboard_data(db: Session):
    # TODO: Optimizar - hace muchas queries separadas
    total_users = db.query(User).count()
    total_posts = db.query(Post).count()
    total_comments = db.query(Comment).count()
    active_users = db.query(User).filter(User.is_active == True).count()

    recent_posts = db.query(Post).order_by(Post.created_at.desc()).limit(5).all()
    recent_users = db.query(User).order_by(User.created_at.desc()).limit(5).all()

    return {
        "stats": {
            "total_users": total_users,
            "total_posts": total_posts,
            "total_comments": total_comments,
            "active_users": active_users
        },
        "recent_posts": recent_posts,
        "recent_users": recent_users
    }
```

#### 2.2 Crear Índices Optimizados

```sql
-- TODO: Crear índices para optimizar las queries anteriores
-- Escribir los comandos SQL CREATE INDEX apropiados

-- Índice para búsqueda de usuarios:
-- TODO: CREATE INDEX ...

-- Índice para posts por fecha:
-- TODO: CREATE INDEX ...

-- Índice compuesto para comments:
-- TODO: CREATE INDEX ...

-- Índice para usuarios activos:
-- TODO: CREATE INDEX ...
```

#### 2.3 Connection Pooling

```python
# TODO: Configurar connection pooling optimizado
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_optimized_engine(database_url: str):
    # TODO: Configurar engine con pooling óptimo
    return create_engine(
        database_url,
        # TODO: Agregar configuración de pool
        # pool_size=?,
        # max_overflow=?,
        # pool_timeout=?,
        # pool_recycle=?
    )
```

### Criterios de Evaluación

- [ ] Queries optimizadas reducen tiempo de ejecución >50%
- [ ] Índices creados apropiadamente
- [ ] Connection pool configurado
- [ ] No hay N+1 query problems
- [ ] Queries usan joins en lugar de loops

---

## Ejercicio 3: Middleware Custom de Performance (45 minutos)

### Contexto

Necesitas crear middleware personalizado para detectar automáticamente endpoints lentos y aplicar optimizaciones dinámicas.

### Tareas

#### 3.1 Middleware de Detección de Performance

```python
# TODO: Implementar PerformanceDetectionMiddleware
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import asyncio
from collections import defaultdict
from typing import Dict, List

class PerformanceDetectionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, slow_threshold: float = 1.0):
        super().__init__(app)
        self.slow_threshold = slow_threshold
        self.endpoint_stats = defaultdict(list)
        self.slow_endpoints = set()

    async def dispatch(self, request: Request, call_next):
        # TODO: Implementar detección de endpoints lentos
        # 1. Medir tiempo de respuesta
        # 2. Almacenar estadísticas por endpoint
        # 3. Detectar automáticamente endpoints lentos
        # 4. Aplicar optimizaciones automáticas
        pass

    def is_slow_endpoint(self, endpoint: str) -> bool:
        # TODO: Determinar si un endpoint es consistentemente lento
        pass

    def get_endpoint_stats(self) -> Dict:
        # TODO: Obtener estadísticas de performance por endpoint
        pass

    async def apply_automatic_optimization(self, request: Request, endpoint: str):
        # TODO: Aplicar optimizaciones automáticas para endpoints lentos
        # Ejemplos: cache automático, compresión, etc.
        pass
```

#### 3.2 Middleware de Rate Limiting Adaptativo

```python
# TODO: Implementar AdaptiveRateLimitMiddleware
class AdaptiveRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_client):
        super().__init__(app)
        self.redis = redis_client
        self.base_limits = {
            "GET": 100,    # requests per minute
            "POST": 30,
            "PUT": 20,
            "DELETE": 10
        }

    async def dispatch(self, request: Request, call_next):
        # TODO: Implementar rate limiting que se adapta a la carga del sistema
        # 1. Verificar métricas del sistema (CPU, memoria)
        # 2. Ajustar límites dinámicamente
        # 3. Aplicar rate limiting más estricto si el sistema está bajo presión
        pass

    async def get_system_load(self) -> float:
        # TODO: Obtener carga actual del sistema
        pass

    def calculate_adaptive_limit(self, base_limit: int, system_load: float) -> int:
        # TODO: Calcular límite adaptativo basado en carga del sistema
        pass
```

### Criterios de Evaluación

- [ ] Middleware detecta endpoints lentos automáticamente
- [ ] Rate limiting se adapta a carga del sistema
- [ ] Estadísticas de performance se almacenan correctamente
- [ ] Optimizaciones automáticas se aplican cuando es necesario
- [ ] Middleware no afecta significativamente la performance

---

## Ejercicio 4: Sistema de Monitoring Custom (60 minutos)

### Contexto

Desarrolla un sistema de monitoring específico para tu aplicación que vaya más allá de las métricas básicas.

### Tareas

#### 4.1 Métricas Custom de Negocio

```python
# TODO: Implementar BusinessMetricsCollector
class BusinessMetricsCollector:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def track_user_action(self, user_id: str, action: str, metadata: dict):
        # TODO: Trackear acciones específicas de usuarios
        # Ejemplos: login, purchase, api_call, etc.
        pass

    async def track_feature_usage(self, feature_name: str, user_id: str):
        # TODO: Trackear uso de features específicas
        pass

    async def track_business_event(self, event_type: str, value: float, metadata: dict):
        # TODO: Trackear eventos de negocio (ventas, conversiones, etc.)
        pass

    async def get_user_behavior_metrics(self, time_window: int = 3600) -> dict:
        # TODO: Analizar comportamiento de usuarios
        pass

    async def get_feature_adoption_metrics(self) -> dict:
        # TODO: Métricas de adopción de features
        pass

    async def get_business_kpis(self) -> dict:
        # TODO: KPIs clave del negocio
        pass
```

#### 4.2 Sistema de Alertas Inteligentes

```python
# TODO: Implementar SmartAlertManager
class SmartAlertManager:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.alert_rules = []

    def add_alert_rule(self, rule: dict):
        # TODO: Agregar regla de alerta
        # Formato: {
        #   "name": "High Error Rate",
        #   "condition": lambda metrics: metrics['error_rate'] > 5,
        #   "severity": "critical",
        #   "cooldown": 300
        # }
        pass

    async def evaluate_alerts(self, metrics: dict):
        # TODO: Evaluar todas las reglas de alerta
        pass

    async def send_alert(self, alert: dict):
        # TODO: Enviar alerta (log, webhook, email, etc.)
        pass

    def add_dynamic_threshold(self, metric_name: str, std_dev_multiplier: float = 2.0):
        # TODO: Crear umbral dinámico basado en datos históricos
        pass
```

#### 4.3 Dashboard de Métricas Custom

```python
# TODO: Implementar endpoints para dashboard custom
from fastapi import APIRouter

router = APIRouter(prefix="/custom-metrics")

@router.get("/business-overview")
async def get_business_overview():
    # TODO: Obtener overview de métricas de negocio
    pass

@router.get("/user-behavior")
async def get_user_behavior_analysis():
    # TODO: Análisis de comportamiento de usuarios
    pass

@router.get("/feature-usage")
async def get_feature_usage():
    # TODO: Estadísticas de uso de features
    pass

@router.get("/performance-trends")
async def get_performance_trends():
    # TODO: Tendencias de performance a lo largo del tiempo
    pass
```

### Criterios de Evaluación

- [ ] Métricas custom implementadas y funcionando
- [ ] Sistema de alertas inteligentes operativo
- [ ] Dashboard custom muestra datos relevantes
- [ ] Alertas dinámicas basadas en datos históricos
- [ ] Métricas de negocio trackean valor real

---

## Ejercicio 5: Optimización de Carga y Stress Testing (45 minutos)

### Contexto

Configura un sistema completo de testing de carga para identificar límites y cuellos de botella.

### Tareas

#### 5.1 Suite de Load Testing

```python
# TODO: Implementar LoadTestSuite
import asyncio
import aiohttp
import time
import statistics
from dataclasses import dataclass
from typing import List

@dataclass
class LoadTestResult:
    endpoint: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    p95_response_time: float
    requests_per_second: float
    error_rate: float

class LoadTestSuite:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = []

    async def run_endpoint_test(
        self,
        endpoint: str,
        method: str = "GET",
        concurrent_users: int = 10,
        requests_per_user: int = 100,
        payload: dict = None
    ) -> LoadTestResult:
        # TODO: Implementar test de carga para un endpoint específico
        pass

    async def run_scenario_test(self, scenario: List[dict]) -> List[LoadTestResult]:
        # TODO: Ejecutar escenario complejo de múltiples endpoints
        # Formato scenario: [
        #   {"endpoint": "/users", "method": "GET", "weight": 0.4},
        #   {"endpoint": "/posts", "method": "GET", "weight": 0.3},
        #   {"endpoint": "/auth/login", "method": "POST", "weight": 0.3}
        # ]
        pass

    async def run_stress_test(self, max_concurrent_users: int = 100) -> dict:
        # TODO: Encontrar punto de quiebre de la aplicación
        pass

    def generate_report(self) -> dict:
        # TODO: Generar reporte completo de performance
        pass
```

#### 5.2 Análisis Automático de Resultados

```python
# TODO: Implementar PerformanceAnalyzer
class PerformanceAnalyzer:
    def __init__(self):
        self.benchmarks = {
            "response_time_acceptable": 500,  # ms
            "response_time_good": 200,
            "error_rate_acceptable": 1.0,    # %
            "min_rps": 100
        }

    def analyze_results(self, results: List[LoadTestResult]) -> dict:
        # TODO: Analizar resultados y dar recomendaciones
        pass

    def identify_bottlenecks(self, results: List[LoadTestResult]) -> List[str]:
        # TODO: Identificar posibles cuellos de botella
        pass

    def generate_recommendations(self, analysis: dict) -> List[str]:
        # TODO: Generar recomendaciones de optimización
        pass
```

### Criterios de Evaluación

- [ ] Load testing suite implementada
- [ ] Diferentes tipos de test (load, stress, scenario)
- [ ] Análisis automático de resultados
- [ ] Identificación de cuellos de botella
- [ ] Recomendaciones actionables generadas

---

## Ejercicio Bonus: Optimización de Red y CDN (30 minutos)

### Contexto

Implementa optimizaciones a nivel de red y simulación de CDN para mejorar performance.

### Tareas

#### Middleware de Compresión Inteligente

```python
# TODO: Implementar SmartCompressionMiddleware
class SmartCompressionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.compression_algorithms = ["gzip", "br", "deflate"]
        self.min_size_for_compression = 1024  # bytes

    async def dispatch(self, request: Request, call_next):
        # TODO: Aplicar compresión inteligente basada en:
        # 1. Tipo de contenido
        # 2. Tamaño de respuesta
        # 3. Algoritmos soportados por cliente
        # 4. Performance histórica por algoritmo
        pass

    def choose_best_algorithm(self, accept_encoding: str, content_type: str) -> str:
        # TODO: Elegir mejor algoritmo basado en contexto
        pass
```

---

## Criterios de Evaluación Global

### Funcionalidad (40%)

- [ ] Todos los ejercicios implementados correctamente
- [ ] Código funciona sin errores críticos
- [ ] Implementaciones siguen buenas prácticas

### Performance (30%)

- [ ] Optimizaciones muestran mejoras medibles
- [ ] Cache hit rate > 70%
- [ ] Queries optimizadas son >50% más rápidas
- [ ] Load testing muestra límites claros

### Código y Arquitectura (20%)

- [ ] Código limpio y bien estructurado
- [ ] Uso correcto de patrones de diseño
- [ ] Manejo adecuado de errores
- [ ] Documentación clara

### Innovación y Análisis (10%)

- [ ] Soluciones creativas implementadas
- [ ] Análisis profundo de resultados
- [ ] Recomendaciones valuable proporcionadas
- [ ] Uso avanzado de herramientas

---

## Entrega

### Formato

1. **Código fuente** completo de todos los ejercicios
2. **Documentación** explicando decisiones de diseño
3. **Resultados de testing** con análisis
4. **Reporte de performance** antes y después de optimizaciones

### Archivos a Entregar

```
ejercicios-performance/
├── ejercicio-1-cache/
│   ├── product_cache.py
│   ├── cache_metrics.py
│   └── tests/
├── ejercicio-2-database/
│   ├── optimized_queries.py
│   ├── indices.sql
│   └── performance_comparison.md
├── ejercicio-3-middleware/
│   ├── performance_middleware.py
│   ├── adaptive_rate_limit.py
│   └── tests/
├── ejercicio-4-monitoring/
│   ├── business_metrics.py
│   ├── smart_alerts.py
│   └── custom_dashboard.py
├── ejercicio-5-load-testing/
│   ├── load_test_suite.py
│   ├── performance_analyzer.py
│   └── test_results/
├── bonus-network/
│   └── smart_compression.py
└── README.md
```

## Recursos de Apoyo

- [FastAPI Performance Tips](https://fastapi.tiangolo.com/async/)
- [Redis Caching Patterns](https://redis.io/docs/manual/patterns/)
- [SQLAlchemy Performance Tips](https://docs.sqlalchemy.org/en/14/orm/examples.html)
- [aiohttp Load Testing](https://docs.aiohttp.org/en/stable/client_performance.html)

## Tiempo Total Estimado

**3-4 horas** distribuidas como:

- Ejercicio 1 (Cache): 45 min
- Ejercicio 2 (Database): 60 min
- Ejercicio 3 (Middleware): 45 min
- Ejercicio 4 (Monitoring): 60 min
- Ejercicio 5 (Load Testing): 45 min
- Bonus (Network): 30 min
- Documentación y testing: 30 min
