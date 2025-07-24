# Práctica 14: Migraciones y Testing con Bases de Datos

**⏱️ Tiempo estimado:** 90 minutos  
**🎯 Objetivo:** Implementar migraciones con Alembic y testing de bases de datos

## 📋 En esta práctica aprenderás

- Configuración y uso de Alembic para migraciones
- Versionado de esquemas de base de datos
- Testing con bases de datos temporales
- Fixtures y mocks para testing
- Pruebas de endpoints con persistencia

## 🗂️ Estructura del Proyecto

```text
mi_api_tienda/
├── alembic/                # ← NUEVO: Configuración Alembic
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── alembic.ini
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models/
│   └── crud/
├── tests/                  # ← NUEVO: Tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_products.py
│   └── test_orders.py
├── alembic.ini
└── requirements.txt
```

## 🔧 Paso 1: Configurar Alembic

### Instalar dependencias

Actualizar `requirements.txt`:

```text
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
alembic==1.13.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

```bash
pip install -r requirements.txt
```

### Inicializar Alembic

```bash
# Desde el directorio del proyecto
alembic init alembic

# Esto crea:
# - alembic/ directory
# - alembic.ini file
```

### Configurar `alembic.ini`

Editar `alembic.ini`:

```ini
# Alembic Config file.

[alembic]
# path to migration scripts
script_location = alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python-dateutil library that can be
# installed by adding `alembic[tz]` to the pip requirements
# string value is passed to dateutil.tz.gettz()
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version file format
version_file_format = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# version directory
version_path_separator = os  # default

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = sqlite:///./tienda.db


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

### Configurar `alembic/env.py`

```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Agregar el directorio padre al path para importar app
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.database import Base
from app.models import user, product, order  # Importar todos los modelos

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## 🔧 Paso 2: Crear Migración Inicial

```bash
# Crear primera migración
alembic revision --autogenerate -m "Initial migration"

# Esto genera un archivo en alembic/versions/
```

### Revisar la migración generada

El archivo generado debería verse similar a:

```python
"""Initial migration

Revision ID: abc123def456
Revises:
Create Date: 2024-01-15 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'abc123def456'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('full_name', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # ... más tablas ...
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ... más drops ...
    # ### end Alembic commands ###
```

### Aplicar la migración

```bash
# Aplicar migraciones pendientes
alembic upgrade head

# Ver historial de migraciones
alembic history --verbose

# Ver migración actual
alembic current
```

## 🔧 Paso 3: Ejemplo de Nueva Migración

Supongamos que queremos agregar un campo `phone` a los usuarios:

### Modificar el modelo

En `app/models/user.py`:

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    phone = Column(String, nullable=True)  # ← NUEVO CAMPO
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación One-to-Many con Orders
    orders = relationship("Order", back_populates="user")
```

### Generar migración

```bash
alembic revision --autogenerate -m "Add phone field to users"
```

### Aplicar migración

```bash
alembic upgrade head
```

### Rollback si es necesario

```bash
# Volver a migración anterior
alembic downgrade -1

# Volver a migración específica
alembic downgrade abc123def456
```

## 🔧 Paso 4: Configurar Testing

### Crear `tests/conftest.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_db, Base

# Base de datos en memoria para tests
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
def db_session():
    """Crear base de datos temporal para cada test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client():
    """Cliente de pruebas para FastAPI"""
    with TestClient(app) as c:
        yield c

@pytest.fixture
def sample_user_data():
    """Datos de usuario para pruebas"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "phone": "+1234567890"
    }

@pytest.fixture
def sample_product_data():
    """Datos de producto para pruebas"""
    return {
        "name": "Test Product",
        "description": "A test product",
        "price": 29.99,
        "stock": 100,
        "category": "test"
    }
```

### Crear `tests/test_users.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud.user import user_crud
from app.schemas.user import UserCreate

def test_create_user(client: TestClient, sample_user_data):
    """Test crear usuario vía API"""
    response = client.post("/users/", json=sample_user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == sample_user_data["email"]
    assert data["username"] == sample_user_data["username"]
    assert "id" in data

def test_read_users(client: TestClient, sample_user_data):
    """Test obtener lista de usuarios"""
    # Crear usuario
    client.post("/users/", json=sample_user_data)

    # Obtener lista
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["email"] == sample_user_data["email"]

def test_read_user(client: TestClient, sample_user_data):
    """Test obtener usuario específico"""
    # Crear usuario
    response = client.post("/users/", json=sample_user_data)
    user_id = response.json()["id"]

    # Obtener usuario específico
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == sample_user_data["email"]

def test_read_user_not_found(client: TestClient):
    """Test usuario no encontrado"""
    response = client.get("/users/999")
    assert response.status_code == 404

def test_create_user_duplicate_email(client: TestClient, sample_user_data):
    """Test error al crear usuario con email duplicado"""
    # Crear primer usuario
    client.post("/users/", json=sample_user_data)

    # Intentar crear segundo usuario con mismo email
    duplicate_data = sample_user_data.copy()
    duplicate_data["username"] = "different_username"

    response = client.post("/users/", json=duplicate_data)
    assert response.status_code == 400

def test_user_crud_direct(db_session: Session, sample_user_data):
    """Test CRUD directo sin API"""
    # Crear usuario
    user_create = UserCreate(**sample_user_data)
    user = user_crud.create_user(db=db_session, user=user_create)

    assert user.email == sample_user_data["email"]
    assert user.username == sample_user_data["username"]
    assert user.id is not None

    # Obtener usuario
    user_found = user_crud.get_user(db=db_session, user_id=user.id)
    assert user_found is not None
    assert user_found.email == sample_user_data["email"]

    # Obtener por email
    user_by_email = user_crud.get_user_by_email(db=db_session, email=sample_user_data["email"])
    assert user_by_email is not None
    assert user_by_email.id == user.id
```

### Crear `tests/test_products.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud.product import product_crud
from app.schemas.product import ProductCreate, ProductUpdate

def test_create_product(client: TestClient, sample_product_data):
    """Test crear producto vía API"""
    response = client.post("/products/", json=sample_product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_product_data["name"]
    assert data["price"] == sample_product_data["price"]
    assert "id" in data

def test_read_products(client: TestClient, sample_product_data):
    """Test obtener productos con filtros"""
    # Crear producto
    client.post("/products/", json=sample_product_data)

    # Obtener todos los productos
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

def test_update_product(client: TestClient, sample_product_data):
    """Test actualizar producto"""
    # Crear producto
    response = client.post("/products/", json=sample_product_data)
    product_id = response.json()["id"]

    # Actualizar producto
    update_data = {"name": "Updated Product", "price": 39.99}
    response = client.put(f"/products/{product_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 39.99

def test_delete_product(client: TestClient, sample_product_data):
    """Test eliminar producto"""
    # Crear producto
    response = client.post("/products/", json=sample_product_data)
    product_id = response.json()["id"]

    # Eliminar producto
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 200

    # Verificar que no existe
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404

def test_search_products(client: TestClient, sample_product_data):
    """Test búsqueda de productos"""
    # Crear varios productos
    products_data = [
        {"name": "Laptop Gaming", "description": "Gaming laptop", "price": 1200.00, "stock": 5, "category": "electronics"},
        {"name": "Gaming Mouse", "description": "RGB mouse", "price": 45.00, "stock": 20, "category": "electronics"},
        {"name": "Office Chair", "description": "Ergonomic chair", "price": 200.00, "stock": 10, "category": "furniture"},
    ]

    for product_data in products_data:
        client.post("/products/", json=product_data)

    # Buscar por nombre
    response = client.get("/products/search?q=Gaming")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2  # Laptop Gaming y Gaming Mouse

    # Filtrar por categoría
    response = client.get("/products/?category=furniture")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Office Chair"
```

### Crear `tests/test_orders.py`

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_create_order(client: TestClient, sample_user_data, sample_product_data):
    """Test crear orden completa"""
    # Crear usuario
    user_response = client.post("/users/", json=sample_user_data)
    user_id = user_response.json()["id"]

    # Crear producto
    product_response = client.post("/products/", json=sample_product_data)
    product_id = product_response.json()["id"]

    # Crear orden
    order_data = {
        "customer_email": sample_user_data["email"],
        "products": [
            {
                "product_id": product_id,
                "quantity": 2
            }
        ]
    }

    response = client.post(f"/orders/?user_id={user_id}", json=order_data)
    assert response.status_code == 200

    data = response.json()
    assert data["customer_email"] == sample_user_data["email"]
    assert data["total_amount"] == sample_product_data["price"] * 2
    assert len(data["products"]) == 1

def test_create_order_insufficient_stock(client: TestClient, sample_user_data, sample_product_data):
    """Test orden con stock insuficiente"""
    # Crear producto con poco stock
    product_data = sample_product_data.copy()
    product_data["stock"] = 1

    product_response = client.post("/products/", json=product_data)
    product_id = product_response.json()["id"]

    # Intentar crear orden con más cantidad que stock
    order_data = {
        "customer_email": sample_user_data["email"],
        "products": [
            {
                "product_id": product_id,
                "quantity": 5  # Más que el stock disponible
            }
        ]
    }

    response = client.post("/orders/", json=order_data)
    assert response.status_code == 400
    assert "Stock insuficiente" in response.json()["detail"]

def test_get_user_orders(client: TestClient, sample_user_data, sample_product_data):
    """Test obtener órdenes de un usuario"""
    # Crear usuario y producto
    user_response = client.post("/users/", json=sample_user_data)
    user_id = user_response.json()["id"]

    product_response = client.post("/products/", json=sample_product_data)
    product_id = product_response.json()["id"]

    # Crear dos órdenes
    for i in range(2):
        order_data = {
            "customer_email": sample_user_data["email"],
            "products": [
                {
                    "product_id": product_id,
                    "quantity": 1
                }
            ]
        }
        client.post(f"/orders/?user_id={user_id}", json=order_data)

    # Obtener órdenes del usuario
    response = client.get(f"/users/{user_id}/orders")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert all(order["user"]["id"] == user_id for order in data)
```

## 🔧 Paso 5: Ejecutar Tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar tests con verbose
pytest -v

# Ejecutar tests específicos
pytest tests/test_users.py

# Ejecutar con coverage
pip install pytest-cov
pytest --cov=app tests/

# Generar reporte HTML de coverage
pytest --cov=app --cov-report=html tests/
```

## 🔧 Paso 6: Scripts de Administración

### Crear `scripts/migrate.py`

```python
#!/usr/bin/env python3
"""Script para gestionar migraciones"""

import subprocess
import sys
import argparse

def run_command(command):
    """Ejecutar comando y mostrar salida"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print(f"Warning: {result.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando: {command}")
        print(f"Salida: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def create_migration(message):
    """Crear nueva migración"""
    command = f"alembic revision --autogenerate -m '{message}'"
    print(f"Creando migración: {message}")
    return run_command(command)

def upgrade_database(revision="head"):
    """Aplicar migraciones"""
    command = f"alembic upgrade {revision}"
    print(f"Aplicando migraciones hasta: {revision}")
    return run_command(command)

def downgrade_database(revision):
    """Revertir migraciones"""
    command = f"alembic downgrade {revision}"
    print(f"Revirtiendo a: {revision}")
    return run_command(command)

def show_history():
    """Mostrar historial de migraciones"""
    command = "alembic history --verbose"
    print("Historial de migraciones:")
    return run_command(command)

def show_current():
    """Mostrar migración actual"""
    command = "alembic current"
    print("Migración actual:")
    return run_command(command)

def main():
    parser = argparse.ArgumentParser(description='Gestión de migraciones de base de datos')
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponibles')

    # Crear migración
    create_parser = subparsers.add_parser('create', help='Crear nueva migración')
    create_parser.add_argument('message', help='Mensaje de la migración')

    # Aplicar migraciones
    upgrade_parser = subparsers.add_parser('upgrade', help='Aplicar migraciones')
    upgrade_parser.add_argument('--revision', default='head', help='Revisión objetivo')

    # Revertir migraciones
    downgrade_parser = subparsers.add_parser('downgrade', help='Revertir migraciones')
    downgrade_parser.add_argument('revision', help='Revisión objetivo')

    # Historial
    subparsers.add_parser('history', help='Mostrar historial')

    # Actual
    subparsers.add_parser('current', help='Mostrar migración actual')

    args = parser.parse_args()

    if args.command == 'create':
        success = create_migration(args.message)
    elif args.command == 'upgrade':
        success = upgrade_database(args.revision)
    elif args.command == 'downgrade':
        success = downgrade_database(args.revision)
    elif args.command == 'history':
        success = show_history()
    elif args.command == 'current':
        success = show_current()
    else:
        parser.print_help()
        return

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

### Hacer ejecutable el script

```bash
chmod +x scripts/migrate.py

# Ejemplos de uso:
python scripts/migrate.py create "Add new field to user"
python scripts/migrate.py upgrade
python scripts/migrate.py history
python scripts/migrate.py current
python scripts/migrate.py downgrade -1
```

## ✅ Ejercicios de Práctica

1. **Migración de datos**: Crear migración que agregue datos iniciales
2. **Test de rendimiento**: Medir tiempos de consultas complejas
3. **Rollback automático**: Script que revierta última migración si hay errores
4. **Backup automático**: Crear backup antes de aplicar migraciones

## 🎯 Entregables

- [ ] Alembic configurado y funcionando
- [ ] Al menos 2 migraciones aplicadas
- [ ] Suite de tests completa (usuarios, productos, órdenes)
- [ ] Coverage de tests > 80%
- [ ] Scripts de administración funcionando

## 📚 Conceptos Clave Aprendidos

- **Migraciones**: Versionado de esquemas de BD
- **Alembic**: Herramienta de migraciones para SQLAlchemy
- **Testing con BD**: Bases de datos temporales para tests
- **Fixtures**: Datos de prueba reutilizables
- **Coverage**: Medición de cobertura de tests

---

## 🚨 Problemas Comunes

### Error: "Target database is not up to date"

```bash
# Verificar estado actual
alembic current

# Aplicar migraciones pendientes
alembic upgrade head
```

### Tests fallan por BD persistente

```python
# Asegurar BD limpia en conftest.py
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```

### Migración automática incompleta

```python
# Revisar manualmente la migración generada
# Agregar cambios faltantes si es necesario
def upgrade():
    # Comandos auto-generados...

    # Comandos manuales adicionales si es necesario
    pass
```

## 🎉 ¡Felicitaciones!

Has completado las 4 semanas del bootcamp y ahora puedes:

- ✅ Crear APIs REST completas con FastAPI
- ✅ Trabajar con bases de datos y ORMs
- ✅ Implementar relaciones complejas
- ✅ Gestionar migraciones de BD
- ✅ Escribir tests robustos
- ✅ Manejar autenticación y autorización
- ✅ Implementar validaciones avanzadas

¡Continúa construyendo proyectos increíbles! 🚀
