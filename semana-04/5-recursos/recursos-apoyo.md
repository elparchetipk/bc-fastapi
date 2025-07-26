# Recursos de Apoyo - Semana 4

## 📚 Documentación Oficial y Referencias

### SQLAlchemy

- **[SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)** - Documentación oficial completa
- **[SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)** - Tutorial paso a paso
- **[SQLAlchemy Relationships](https://docs.sqlalchemy.org/en/20/orm/relationships.html)** - Guía de relaciones
- **[SQLAlchemy Query Guide](https://docs.sqlalchemy.org/en/20/orm/queryguide.html)** - Consultas avanzadas

### Alembic

- **[Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)** - Documentación oficial
- **[Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)** - Tutorial básico
- **[Migration Environment](https://alembic.sqlalchemy.org/en/latest/tutorial.html#the-migration-environment)** - Configuración del entorno

### FastAPI y Bases de Datos

- **[FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)** - Tutorial oficial
- **[FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)** - Testing con FastAPI
- **[Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)** - Inyección de dependencias

### Pydantic

- **[Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)** - Documentación v2
- **[Data Validation](https://docs.pydantic.dev/latest/concepts/validators/)** - Validadores personalizados
- **[Field Types](https://docs.pydantic.dev/latest/api/fields/)** - Tipos de campo disponibles

### Testing

- **[pytest Documentation](https://docs.pytest.org/)** - Framework de testing
- **[pytest-asyncio](https://pytest-asyncio.readthedocs.io/)** - Testing asíncrono
- **[HTTPX](https://www.python-httpx.org/)** - Cliente HTTP para testing

---

## 🛠️ Herramientas y Utilidades

### Desarrollo Local

#### Base de Datos

- **[SQLite Browser](https://sqlitebrowser.org/)** - GUI para SQLite
- **[DBeaver](https://dbeaver.io/)** - Cliente universal de BD
- **[DB Browser for SQLite](https://sqlitebrowser.org/)** - Herramienta específica SQLite

#### IDEs y Editores

- **[VS Code Extensions](https://marketplace.visualstudio.com/)**:
  - Python
  - SQLite Viewer
  - REST Client
  - Thunder Client (Postman alternativo)

#### API Testing

- **[Postman](https://www.postman.com/)** - Testing de APIs
- **[Insomnia](https://insomnia.rest/)** - Cliente REST alternativo
- **[httpie](https://httpie.io/)** - Cliente HTTP de línea de comandos

### Monitoreo y Debugging

- **[Swagger UI](https://swagger.io/tools/swagger-ui/)** - Documentación automática (incluida en FastAPI)
- **[SQLAlchemy logging](https://docs.sqlalchemy.org/en/20/core/engines.html#configuring-logging)** - Logs de SQL
- **[pytest-cov](https://pytest-cov.readthedocs.io/)** - Coverage de tests

---

## 📖 Tutoriales y Guías Complementarias

### Tutoriales de SQLAlchemy

1. **[Real Python - SQLAlchemy Tutorial](https://realpython.com/python-sqlite-sqlalchemy/)**

   - Tutorial completo con ejemplos prácticos
   - Desde básico hasta avanzado

2. **[SQLAlchemy Core vs ORM](https://docs.sqlalchemy.org/en/20/tutorial/)**

   - Diferencias entre Core y ORM
   - Cuándo usar cada uno

3. **[Database Design Patterns](https://www.sqlalchemy.org/features.html)**
   - Patrones comunes de diseño
   - Mejores prácticas

### Tutoriales de Alembic

1. **[Database Migrations with Alembic](https://realpython.com/alembic-database-migrations/)**

   - Guía paso a paso
   - Casos de uso comunes

2. **[Advanced Alembic Usage](https://alembic.sqlalchemy.org/en/latest/cookbook.html)**
   - Casos avanzados
   - Trucos y tips

### FastAPI Avanzado

1. **[FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)**

   - Recopilación de mejores prácticas
   - Estructura de proyectos

2. **[FastAPI Production Guide](https://fastapi.tiangolo.com/deployment/)**
   - Despliegue en producción
   - Configuración de servidor

---

## 🎥 Videos y Recursos Multimedia

### Canales de YouTube

1. **[ArjanCodes](https://www.youtube.com/@ArjanCodes)**

   - Videos sobre arquitectura de software
   - FastAPI y SQLAlchemy

2. **[mCoding](https://www.youtube.com/@mCoding)**

   - Python avanzado
   - Mejores prácticas

3. **[Tech With Tim](https://www.youtube.com/@TechWithTim)**
   - Tutoriales de FastAPI
   - Proyectos prácticos

### Cursos Online

1. **[FastAPI - The Complete Course](https://www.udemy.com/course/fastapi-the-complete-course/)**

   - Curso completo en Udemy
   - Incluye bases de datos

2. **[Python API Development Comprehensive Course](https://www.youtube.com/watch?v=0sOvCWFmrtA)**
   - Curso gratuito en YouTube
   - 19 horas de contenido

---

## 📚 Libros Recomendados

### Python y APIs

1. **"FastAPI Modern Python Web Development"** por Bill Lubanovic

   - Libro específico de FastAPI
   - Ejemplos prácticos

2. **"Architecture Patterns with Python"** por Harry Percival y Bob Gregory
   - Patrones de arquitectura
   - Testing y TDD

### Bases de Datos

1. **"SQL and Relational Theory"** por C.J. Date

   - Fundamentos teóricos sólidos
   - Mejores prácticas de diseño

2. **"Database Design for Mere Mortals"** por Michael Hernandez
   - Diseño de bases de datos relacionales
   - Fácil de entender

---

## 🔧 Snippets y Templates Útiles

### Configuración Base SQLAlchemy

```python
# database.py template
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Modelo Base Reutilizable

```python
# models/base.py
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.database import Base

class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

### CRUD Base Genérico

```python
# crud/base.py
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
```

### Configuración de Testing

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c
```

---

## 🚨 Errores Comunes y Soluciones

### SQLAlchemy

#### Error: "Table already exists"

```python
# Solución: Usar Base.metadata.create_all() solo una vez
# O verificar antes de crear
if not engine.dialect.has_table(engine, 'table_name'):
    Base.metadata.create_all(bind=engine)
```

#### Error: "DetachedInstanceError"

```python
# Problema: Usar objeto fuera de sesión
# Solución: Refrescar o hacer merge
db.refresh(db_obj)
# o
db_obj = db.merge(db_obj)
```

#### Error: "Multiple rows returned by scalar"

```python
# Problema: .scalar() con múltiples resultados
# Solución: Usar .first() o .all()
result = query.first()  # En lugar de .scalar()
```

### Alembic

#### Error: "Target database is not up to date"

```bash
# Verificar versión actual
alembic current

# Aplicar migraciones pendientes
alembic upgrade head
```

#### Error: "Can't locate revision identifier"

```bash
# Limpiar y regenerar
alembic stamp head
alembic revision --autogenerate -m "New migration"
```

### FastAPI + SQLAlchemy

#### Error: "RuntimeError: There is no current event loop"

```python
# Problema: Uso de async sin configurar
# Solución: Usar sync o configurar async apropiadamente
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
```

#### Error: "Relationship circular import"

```python
# Problema: Importaciones circulares en relaciones
# Solución: Usar string references
class User(Base):
    orders = relationship("Order", back_populates="user")  # String reference
```

---

## 🎯 Ejercicios Adicionales de Práctica

### Ejercicio 1: Optimización de Consultas

Implementar y comparar diferentes estrategias de carga:

```python
# Eager loading
users = session.query(User).options(selectinload(User.orders)).all()

# Lazy loading (default)
users = session.query(User).all()
for user in users:
    print(len(user.orders))  # Genera N+1 queries

# Joined loading
users = session.query(User).options(joinedload(User.orders)).all()
```

### Ejercicio 2: Consultas Complejas

```python
# Subconsultas
subquery = session.query(func.avg(Review.rating)).filter(
    Review.product_id == Product.id
).scalar_subquery()

products = session.query(Product, subquery.label('avg_rating')).all()

# Window functions
from sqlalchemy import func, select
stmt = select(
    Order.id,
    Order.total_amount,
    func.row_number().over(
        partition_by=Order.user_id,
        order_by=Order.created_at.desc()
    ).label('order_rank')
).where(Order.status == 'completed')
```

### Ejercicio 3: Testing Avanzado

```python
# Test con fixtures complejas
@pytest.fixture
def user_with_orders(db):
    user = User(username="testuser", email="test@example.com")
    db.add(user)
    db.flush()

    for i in range(3):
        order = Order(user_id=user.id, total_amount=100.0 * (i + 1))
        db.add(order)

    db.commit()
    return user

def test_user_total_spent(db, user_with_orders):
    total = db.query(func.sum(Order.total_amount)).filter(
        Order.user_id == user_with_orders.id
    ).scalar()
    assert total == 600.0  # 100 + 200 + 300
```

---

## 🌟 Proyectos de Inspiración

### APIs de Referencia

1. **[FastAPI SQL Databases Example](https://github.com/tiangolo/fastapi/tree/master/docs/src/sql_databases)**

   - Ejemplo oficial de FastAPI
   - Estructura recomendada

2. **[Full Stack FastAPI PostgreSQL](https://github.com/tiangolo/full-stack-fastapi-postgresql)**

   - Proyecto completo con frontend
   - Configuración de producción

3. **[FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)**
   - Recopilación de mejores prácticas
   - Ejemplos de código

### Proyectos Open Source

1. **[Starlette Applications](https://github.com/encode/starlette/tree/master/examples)**

   - Ejemplos con Starlette (base de FastAPI)
   - Patrones útiles

2. **[FastAPI Users](https://github.com/fastapi-users/fastapi-users)**
   - Sistema de usuarios completo
   - Autenticación y autorización

---

## 🎓 Certificaciones y Cursos Avanzados

### Certificaciones

1. **[Microsoft: Introduction to Python](https://docs.microsoft.com/en-us/learn/paths/intro-to-python/)**

   - Certificación gratuita
   - Incluye APIs y bases de datos

2. **[Google Cloud: APIs with Python](https://cloud.google.com/python)**
   - Desarrollo de APIs en la nube
   - Integración con servicios cloud

### Cursos Especializados

1. **[Architecture Patterns with Python](https://www.cosmicpython.com/)**

   - Libro y curso avanzado
   - Patrones de arquitectura

2. **[Test-Driven Development with Python](https://www.obeythetestinggoat.com/)**
   - TDD específicamente con Python
   - Incluye testing de APIs

---

## 📞 Comunidad y Soporte

### Foros y Comunidades

1. **[FastAPI GitHub Discussions](https://github.com/tiangolo/fastapi/discussions)**

   - Preguntas y respuestas oficiales
   - Anuncios de nuevas features

2. **[SQLAlchemy Discord](https://discord.gg/FescjbY)**

   - Chat en tiempo real
   - Ayuda de la comunidad

3. **[r/FastAPI](https://www.reddit.com/r/FastAPI/)**
   - Subreddit oficial
   - Proyectos y preguntas

### Stack Overflow

- **Tags relevantes:**
  - `fastapi`
  - `sqlalchemy`
  - `alembic`
  - `pydantic`
  - `python-testing`

### Slack/Discord

- **[Python Discord](https://discord.gg/python)**
- **[FastAPI Discord](https://discord.gg/VQjSZaeJmf)**

---

¡Utiliza estos recursos para profundizar tus conocimientos y convertirte en un experto en desarrollo de APIs con FastAPI y SQLAlchemy! 🚀
