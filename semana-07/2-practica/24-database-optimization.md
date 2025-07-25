# Práctica 24: Optimización de Base de Datos

## Objetivo

Aprender técnicas de optimización de bases de datos para mejorar el rendimiento de aplicaciones FastAPI.

## Duración Estimada

⏱️ **70 minutos**

- Preparación: 10 minutos
- Implementación: 45 minutos
- Pruebas y validación: 15 minutos

## Requisitos Previos

- Tener SQLAlchemy configurado (Semana 4)
- Conocimiento básico de perfilado (Práctica 23)
- Aplicación con múltiples modelos y relaciones

## Conceptos Teóricos

### 1. Problemas de Rendimiento Comunes

- N+1 queries
- Consultas no optimizadas
- Falta de índices
- Transacciones innecesarias

### 2. Técnicas de Optimización

- Eager loading vs lazy loading
- Query optimization
- Database indexing
- Connection pooling
- Pagination

## Implementación

### Paso 1: Configuración del Entorno de Pruebas

Primero, configuremos un escenario con datos de prueba:

```python
# scripts/generate_test_data.py
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Post, Comment
from faker import Faker
import random

fake = Faker()

def generate_test_data():
    """Genera datos de prueba para optimización"""
    db = next(get_db())

    # Crear usuarios
    users = []
    for i in range(100):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            full_name=fake.name()
        )
        db.add(user)
        users.append(user)

    db.commit()

    # Crear posts
    posts = []
    for i in range(500):
        post = Post(
            title=fake.sentence(),
            content=fake.text(),
            author_id=random.choice(users).id
        )
        db.add(post)
        posts.append(post)

    db.commit()

    # Crear comentarios
    for i in range(2000):
        comment = Comment(
            content=fake.text(),
            post_id=random.choice(posts).id,
            author_id=random.choice(users).id
        )
        db.add(comment)

    db.commit()
    print("Datos de prueba generados exitosamente")

if __name__ == "__main__":
    generate_test_data()
```

### Paso 2: Detección de Problemas N+1

Creemos un endpoint que demuestre el problema N+1:

```python
# app/routers/optimization.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models import User, Post, Comment
import time

router = APIRouter(prefix="/optimization", tags=["optimization"])

@router.get("/users-posts-slow")
async def get_users_posts_slow(db: Session = Depends(get_db)):
    """Endpoint lento con problema N+1"""
    start_time = time.time()

    # Esto genera N+1 queries
    users = db.query(User).limit(10).all()
    result = []

    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "posts_count": len(user.posts),  # Esto genera una query por usuario
            "posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "comments_count": len(post.comments)  # Otra query por post
                }
                for post in user.posts
            ]
        }
        result.append(user_data)

    execution_time = time.time() - start_time
    return {
        "data": result,
        "execution_time": execution_time,
        "query_type": "N+1 problem"
    }
```

### Paso 3: Optimización con Eager Loading

Ahora optimicemos el endpoint anterior:

```python
from sqlalchemy.orm import joinedload, selectinload

@router.get("/users-posts-optimized")
async def get_users_posts_optimized(db: Session = Depends(get_db)):
    """Endpoint optimizado con eager loading"""
    start_time = time.time()

    # Eager loading para evitar N+1
    users = db.query(User)\
        .options(
            selectinload(User.posts)
            .selectinload(Post.comments)
        )\
        .limit(10)\
        .all()

    result = []
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "posts_count": len(user.posts),
            "posts": [
                {
                    "id": post.id,
                    "title": post.title,
                    "comments_count": len(post.comments)
                }
                for post in user.posts
            ]
        }
        result.append(user_data)

    execution_time = time.time() - start_time
    return {
        "data": result,
        "execution_time": execution_time,
        "query_type": "optimized eager loading"
    }
```

### Paso 4: Optimización con Consultas Agregadas

Para casos donde solo necesitamos conteos:

```python
@router.get("/users-stats-optimized")
async def get_users_stats_optimized(db: Session = Depends(get_db)):
    """Endpoint optimizado con consultas agregadas"""
    start_time = time.time()

    # Una sola query con agregaciones
    users_stats = db.query(
        User.id,
        User.username,
        func.count(Post.id).label('posts_count'),
        func.count(Comment.id).label('comments_count')
    )\
    .outerjoin(Post, User.id == Post.author_id)\
    .outerjoin(Comment, Post.id == Comment.post_id)\
    .group_by(User.id, User.username)\
    .limit(10)\
    .all()

    result = [
        {
            "id": user.id,
            "username": user.username,
            "posts_count": user.posts_count,
            "comments_count": user.comments_count
        }
        for user in users_stats
    ]

    execution_time = time.time() - start_time
    return {
        "data": result,
        "execution_time": execution_time,
        "query_type": "aggregated query"
    }
```

### Paso 5: Implementación de Paginación Eficiente

```python
from app.schemas import PaginationParams

@router.get("/posts-paginated")
async def get_posts_paginated(
    params: PaginationParams = Depends(),
    db: Session = Depends(get_db)
):
    """Paginación eficiente de posts"""
    start_time = time.time()

    # Calcular offset
    offset = (params.page - 1) * params.size

    # Query optimizada con paginación
    posts_query = db.query(Post)\
        .options(joinedload(Post.author))\
        .order_by(Post.created_at.desc())

    # Contar total (para metadatos de paginación)
    total = posts_query.count()

    # Obtener posts paginados
    posts = posts_query.offset(offset).limit(params.size).all()

    execution_time = time.time() - start_time

    return {
        "data": [
            {
                "id": post.id,
                "title": post.title,
                "author": post.author.username,
                "created_at": post.created_at
            }
            for post in posts
        ],
        "pagination": {
            "page": params.page,
            "size": params.size,
            "total": total,
            "pages": (total + params.size - 1) // params.size
        },
        "execution_time": execution_time
    }
```

### Paso 6: Optimización de Connection Pool

```python
# app/database.py (actualización)
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

# Configuración optimizada del engine
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,          # Número de conexiones permanentes
    max_overflow=30,       # Conexiones adicionales permitidas
    pool_pre_ping=True,    # Verificar conexiones antes de usar
    pool_recycle=3600,     # Reciclar conexiones cada hora
    echo=False             # Desactivar en producción
)
```

### Paso 7: Middleware de Monitoreo de Queries

```python
# app/middleware/query_monitoring.py
from fastapi import Request, Response
from sqlalchemy import event
from sqlalchemy.engine import Engine
import time
import logging

logger = logging.getLogger(__name__)

class QueryCounter:
    def __init__(self):
        self.reset()

    def reset(self):
        self.query_count = 0
        self.total_time = 0
        self.queries = []

    def add_query(self, statement, duration):
        self.query_count += 1
        self.total_time += duration
        self.queries.append({
            "statement": str(statement),
            "duration": duration
        })

query_counter = QueryCounter()

@event.listens_for(Engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    context._query_start_time = time.time()

@event.listens_for(Engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - context._query_start_time
    query_counter.add_query(statement, total)

async def query_monitoring_middleware(request: Request, call_next):
    """Middleware para monitorear queries por request"""
    query_counter.reset()

    response = await call_next(request)

    # Agregar headers con información de performance
    response.headers["X-Query-Count"] = str(query_counter.query_count)
    response.headers["X-Query-Time"] = f"{query_counter.total_time:.4f}"

    # Log queries lentas
    if query_counter.total_time > 1.0:  # Más de 1 segundo
        logger.warning(
            f"Slow request: {request.url} - "
            f"{query_counter.query_count} queries in {query_counter.total_time:.4f}s"
        )

    return response
```

### Paso 8: Herramientas de Análisis

```python
# app/routers/analysis.py
from fastapi import APIRouter
from app.middleware.query_monitoring import query_counter

router = APIRouter(prefix="/analysis", tags=["analysis"])

@router.get("/query-analysis")
async def get_query_analysis():
    """Análisis de queries de la última request"""
    return {
        "total_queries": query_counter.query_count,
        "total_time": query_counter.total_time,
        "average_time": (
            query_counter.total_time / query_counter.query_count
            if query_counter.query_count > 0 else 0
        ),
        "queries": query_counter.queries[-10:]  # Últimas 10 queries
    }

@router.get("/slow-queries")
async def get_slow_queries():
    """Identificar queries lentas"""
    slow_queries = [
        query for query in query_counter.queries
        if query["duration"] > 0.1  # Más de 100ms
    ]

    return {
        "slow_queries": sorted(
            slow_queries,
            key=lambda x: x["duration"],
            reverse=True
        )
    }
```

## Ejercicios Prácticos

### Ejercicio 1: Comparación de Rendimiento

1. Implementa ambos endpoints (lento y optimizado)
2. Genera datos de prueba
3. Compara los tiempos de ejecución
4. Documenta las diferencias

### Ejercicio 2: Identificación de N+1

1. Crea un endpoint con problema N+1
2. Usa el middleware de monitoreo
3. Identifica el problema
4. Implementa la solución

### Ejercicio 3: Optimización de Consultas Personalizadas

1. Crea una consulta compleja con múltiples joins
2. Mide su rendimiento
3. Optimízala usando técnicas aprendidas
4. Compara resultados

## Métricas de Evaluación

### ✅ Checklist de Completitud

- [ ] Implementaste detección de problemas N+1
- [ ] Aplicaste eager loading correctamente
- [ ] Creaste consultas agregadas eficientes
- [ ] Implementaste paginación optimizada
- [ ] Configuraste connection pooling
- [ ] Agregaste monitoreo de queries
- [ ] Documentaste mejoras de rendimiento

### 📊 Indicadores de Rendimiento

- **Reducción de queries**: Mínimo 50% menos queries
- **Tiempo de respuesta**: Mejora de al menos 30%
- **Uso de memoria**: Optimización visible
- **Escalabilidad**: Rendimiento consistente con más datos

## Troubleshooting

### Problema: Las optimizaciones no mejoran el rendimiento

```python
# Verificar que las relaciones estén bien definidas
class User(Base):
    posts = relationship("Post", back_populates="author", lazy="select")

# Usar lazy="select" para control manual del loading
```

### Problema: Memoria alta con eager loading

```python
# Usar selectinload en lugar de joinedload para relaciones 1:N
users = db.query(User)\
    .options(selectinload(User.posts))\
    .all()
```

### Problema: Queries duplicadas

```python
# Verificar que no haya lazy loading accidental
from sqlalchemy.orm import noload
users = db.query(User).options(noload(User.posts)).all()
```

## Recursos Adicionales

- [SQLAlchemy Performance Tips](https://docs.sqlalchemy.org/en/14/orm/loading_techniques.html)
- [Database Indexing Strategies](https://use-the-index-luke.com/)
- [FastAPI Database Patterns](https://fastapi.tiangolo.com/advanced/sql-databases/)

## Próximos Pasos

En la siguiente práctica, implementaremos estrategias de caching para mejorar aún más el rendimiento de nuestra aplicación.
