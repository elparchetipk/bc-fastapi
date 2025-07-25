# 🔧 Práctica 19: Setup de Testing con pytest

**Duración estimada: 90 minutos**

## 🎯 Objetivos

- Configurar pytest en un proyecto FastAPI existente
- Establecer estructura de testing profesional
- Implementar fixtures básicas para testing
- Configurar herramientas de quality assurance

---

## 📋 Prerequisitos

- Proyecto FastAPI de semanas anteriores (con auth y database)
- Python 3.9+ instalado
- Conocimientos básicos de FastAPI y SQLAlchemy

---

## 🚀 Parte 1: Setup Inicial de pytest (25 min)

### **Paso 1: Instalación de Dependencias**

Primero, instalaremos las herramientas necesarias para testing:

```bash
# Instalar pytest y plugins esenciales
pip install pytest==7.4.3
pip install pytest-asyncio==0.21.1
pip install pytest-cov==4.1.0
pip install pytest-mock==3.12.0

# Para testing de APIs
pip install httpx==0.25.2

# Para generación de datos de prueba
pip install factory-boy==3.3.0
pip install faker==19.6.2

# Actualizar requirements.txt
pip freeze > requirements.txt
```

### **Paso 2: Configuración de pytest**

Crear el archivo de configuración `pytest.ini` en la raíz del proyecto:

```ini
# pytest.ini
[tool:pytest]
minversion = 6.0
addopts = -ra -q --strict-markers --strict-config
testpaths = tests
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    auth: marks tests related to authentication
    database: marks tests that require database

# Configuración para async testing
asyncio_mode = auto

# Configuración de logging para tests
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(name)s: %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S
```

### **Paso 3: Estructura de Directorios**

Crear la estructura de testing:

```bash
mkdir -p tests/{unit,integration,fixtures}
touch tests/__init__.py
touch tests/conftest.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
touch tests/fixtures/__init__.py
```

**Estructura resultante:**

```
proyecto/
├── app/
│   ├── main.py
│   ├── models/
│   ├── routers/
│   └── services/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures globales
│   ├── unit/                # Tests unitarios
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   └── test_products.py
│   ├── integration/         # Tests de integración
│   │   ├── __init__.py
│   │   ├── test_api_auth.py
│   │   ├── test_api_users.py
│   │   └── test_database.py
│   └── fixtures/            # Datos de prueba
│       ├── __init__.py
│       ├── users.py
│       └── products.py
├── pytest.ini
└── requirements.txt
```

---

## 🧪 Parte 2: Configuración de Fixtures Globales (30 min)

### **Paso 1: Database Testing Setup**

En `tests/conftest.py`, configurar la base de datos de testing:

```python
# tests/conftest.py
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import User, Product, Order

# Test database URL (usar SQLite en memoria para velocidad)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Crear engine para testing
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def test_db():
    """Create test database tables."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    """Create a fresh database session for each test."""
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    """Create a test client with database dependency override."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(db_session) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Create an async test client."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
```

### **Paso 2: User Authentication Fixtures**

Agregar fixtures para autenticación:

```python
# Continuar en tests/conftest.py
from app.services.auth import create_access_token, hash_password

@pytest.fixture
def test_password():
    """Provide a standard test password."""
    return "testpassword123"


@pytest.fixture
def test_user_data(test_password):
    """Provide test user data."""
    return {
        "email": "test@example.com",
        "username": "testuser",
        "first_name": "Test",
        "last_name": "User",
        "password": test_password
    }


@pytest.fixture
def test_user(db_session, test_user_data):
    """Create a test user in the database."""
    from app.models import User, UserRole

    user = User(
        email=test_user_data["email"],
        username=test_user_data["username"],
        first_name=test_user_data["first_name"],
        last_name=test_user_data["last_name"],
        hashed_password=hash_password(test_user_data["password"]),
        role=UserRole.CUSTOMER,
        is_active=True,
        is_verified=True
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def test_admin_user(db_session, test_password):
    """Create a test admin user."""
    from app.models import User, UserRole

    admin = User(
        email="admin@example.com",
        username="admin",
        first_name="Admin",
        last_name="User",
        hashed_password=hash_password(test_password),
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True
    )

    db_session.add(admin)
    db_session.commit()
    db_session.refresh(admin)

    return admin


@pytest.fixture
def auth_headers(test_user):
    """Provide authentication headers for test user."""
    token = create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_auth_headers(test_admin_user):
    """Provide authentication headers for admin user."""
    token = create_access_token(data={"sub": test_admin_user.email})
    return {"Authorization": f"Bearer {token}"}
```

### **Paso 3: Product and Order Fixtures**

```python
# Continuar en tests/conftest.py
@pytest.fixture
def test_product_data():
    """Provide test product data."""
    return {
        "name": "Test Product",
        "description": "A product for testing",
        "price": 99.99,
        "category": "ELECTRONICS",
        "stock_quantity": 10
    }


@pytest.fixture
def test_product(db_session, test_product_data, test_user):
    """Create a test product in the database."""
    from app.models import Product, ProductCategory

    product = Product(
        name=test_product_data["name"],
        description=test_product_data["description"],
        price=test_product_data["price"],
        category=ProductCategory(test_product_data["category"]),
        stock_quantity=test_product_data["stock_quantity"],
        created_by=test_user.id
    )

    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)

    return product


@pytest.fixture
def multiple_products(db_session, test_user):
    """Create multiple test products."""
    from app.models import Product, ProductCategory

    products_data = [
        {
            "name": "Laptop",
            "description": "Gaming laptop",
            "price": 1299.99,
            "category": ProductCategory.ELECTRONICS,
            "stock_quantity": 5
        },
        {
            "name": "Book",
            "description": "Programming book",
            "price": 39.99,
            "category": ProductCategory.BOOKS,
            "stock_quantity": 20
        },
        {
            "name": "T-Shirt",
            "description": "Cotton t-shirt",
            "price": 19.99,
            "category": ProductCategory.CLOTHING,
            "stock_quantity": 50
        }
    ]

    products = []
    for data in products_data:
        product = Product(
            **data,
            created_by=test_user.id
        )
        db_session.add(product)
        products.append(product)

    db_session.commit()

    for product in products:
        db_session.refresh(product)

    return products
```

---

## 🧪 Parte 3: Primeros Tests Unitarios (20 min)

### **Paso 1: Test de Modelos**

Crear `tests/unit/test_models.py`:

```python
# tests/unit/test_models.py
import pytest
from app.models import User, Product, UserRole, ProductCategory
from app.services.auth import hash_password, verify_password


class TestUserModel:
    """Tests para el modelo User."""

    def test_user_creation(self, db_session):
        """Test básico de creación de usuario."""
        user = User(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            hashed_password=hash_password("password123"),
            role=UserRole.CUSTOMER
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.role == UserRole.CUSTOMER
        assert user.is_active is True  # Default value
        assert user.created_at is not None

    def test_password_hashing(self):
        """Test que el password se hashea correctamente."""
        password = "mysecretpassword"
        hashed = hash_password(password)

        assert hashed != password
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_user_display_name(self, test_user):
        """Test del método display_name si existe."""
        expected_name = f"{test_user.first_name} {test_user.last_name}"
        assert test_user.get_display_name() == expected_name


class TestProductModel:
    """Tests para el modelo Product."""

    def test_product_creation(self, db_session, test_user):
        """Test básico de creación de producto."""
        product = Product(
            name="Test Product",
            description="A test product",
            price=99.99,
            category=ProductCategory.ELECTRONICS,
            stock_quantity=10,
            created_by=test_user.id
        )

        db_session.add(product)
        db_session.commit()
        db_session.refresh(product)

        assert product.id is not None
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.category == ProductCategory.ELECTRONICS
        assert product.is_active is True  # Default value
        assert product.created_at is not None

    def test_product_price_validation(self):
        """Test que el precio no puede ser negativo."""
        with pytest.raises(ValueError):
            Product(
                name="Invalid Product",
                price=-10.00,
                category=ProductCategory.ELECTRONICS
            )

    def test_product_stock_operations(self, test_product, db_session):
        """Test de operaciones de stock."""
        initial_stock = test_product.stock_quantity

        # Reducir stock
        test_product.reduce_stock(3)
        assert test_product.stock_quantity == initial_stock - 3

        # Aumentar stock
        test_product.increase_stock(2)
        assert test_product.stock_quantity == initial_stock - 1

        # No permitir stock negativo
        with pytest.raises(ValueError):
            test_product.reduce_stock(initial_stock + 10)
```

### **Paso 2: Test de Servicios**

Crear `tests/unit/test_auth_service.py`:

```python
# tests/unit/test_auth_service.py
import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta

from app.services.auth import (
    create_access_token,
    verify_token,
    hash_password,
    verify_password,
    authenticate_user
)
from app.models import User, UserRole


class TestAuthService:
    """Tests para el servicio de autenticación."""

    def test_create_access_token(self):
        """Test creación de token JWT."""
        data = {"sub": "test@example.com"}
        token = create_access_token(data)

        assert isinstance(token, str)
        assert len(token) > 0
        assert "." in token  # JWT tiene puntos separadores

    def test_create_token_with_expiration(self):
        """Test token con tiempo de expiración personalizado."""
        data = {"sub": "test@example.com"}
        expires_delta = timedelta(minutes=15)
        token = create_access_token(data, expires_delta)

        # Verificar que el token se puede decodificar
        payload = verify_token(token)
        assert payload is not None
        assert payload["sub"] == "test@example.com"

    def test_verify_valid_token(self):
        """Test verificación de token válido."""
        data = {"sub": "test@example.com", "role": "customer"}
        token = create_access_token(data)

        payload = verify_token(token)

        assert payload is not None
        assert payload["sub"] == "test@example.com"
        assert payload["role"] == "customer"

    def test_verify_invalid_token(self):
        """Test verificación de token inválido."""
        invalid_token = "invalid.token.here"

        payload = verify_token(invalid_token)
        assert payload is None

    @patch('app.services.auth.jwt.decode')
    def test_verify_expired_token(self, mock_decode):
        """Test verificación de token expirado."""
        from jose import JWTError
        mock_decode.side_effect = JWTError("Token expired")

        payload = verify_token("expired.token")
        assert payload is None

    def test_password_hashing_and_verification(self):
        """Test completo de hash y verificación de passwords."""
        password = "supersecurepassword123"

        # Hash del password
        hashed = hash_password(password)

        # Verificaciones
        assert hashed != password
        assert len(hashed) > 0
        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_authenticate_user_success(self, db_session, test_user, test_password):
        """Test autenticación exitosa."""
        authenticated_user = authenticate_user(
            db_session, test_user.email, test_password
        )

        assert authenticated_user is not None
        assert authenticated_user.id == test_user.id
        assert authenticated_user.email == test_user.email

    def test_authenticate_user_wrong_password(self, db_session, test_user):
        """Test autenticación con password incorrecto."""
        authenticated_user = authenticate_user(
            db_session, test_user.email, "wrongpassword"
        )

        assert authenticated_user is None

    def test_authenticate_user_not_found(self, db_session):
        """Test autenticación con usuario inexistente."""
        authenticated_user = authenticate_user(
            db_session, "nonexistent@example.com", "password"
        )

        assert authenticated_user is None
```

---

## 🧪 Parte 4: Ejecutar y Validar Tests (15 min)

### **Paso 1: Ejecutar Tests Básicos**

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con output verboso
pytest -v

# Ejecutar solo tests unitarios
pytest tests/unit/ -v

# Ejecutar un archivo específico
pytest tests/unit/test_models.py -v

# Ejecutar un test específico
pytest tests/unit/test_models.py::TestUserModel::test_user_creation -v
```

### **Paso 2: Verificar Coverage**

```bash
# Ejecutar tests con coverage
pytest --cov=app --cov-report=term-missing

# Generar reporte HTML
pytest --cov=app --cov-report=html

# Abrir reporte en navegador
open htmlcov/index.html  # macOS
# o
xdg-open htmlcov/index.html  # Linux
```

### **Paso 3: Configurar Coverage**

Crear `.coveragerc`:

```ini
# .coveragerc
[run]
source = app
omit =
    */venv/*
    */env/*
    */tests/*
    */migrations/*
    */__pycache__/*
    */conftest.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:

[html]
directory = htmlcov
```

### **Paso 4: Debugging Tests**

```bash
# Ejecutar con debugger automático en fallos
pytest --pdb

# Mostrar print statements
pytest -s

# Ejecutar solo tests que fallaron la última vez
pytest --lf

# Ejecutar hasta el primer fallo
pytest -x

# Ejecutar tests en paralelo (instalar pytest-xdist)
pip install pytest-xdist
pytest -n auto
```

---

## 📊 Parte 5: Configuración de Quality Assurance (Extra)

### **Paso 1: Configurar pre-commit**

```bash
# Instalar pre-commit
pip install pre-commit

# Crear configuración
cat > .pre-commit-config.yaml << EOF
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
EOF

# Instalar los hooks
pre-commit install

# Ejecutar en todos los archivos
pre-commit run --all-files
```

### **Paso 2: Configurar Herramientas de Quality**

Crear `pyproject.toml`:

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true
line_length = 88

[tool.coverage.run]
source = ["app"]
omit = [
    "*/tests/*",
    "*/venv/*",
    "*/__pycache__/*",
    "*/migrations/*"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError"
]
```

---

## ✅ Verificación Final

### **Checklist de Completitud**

- [ ] pytest instalado y configurado
- [ ] Estructura de tests creada
- [ ] conftest.py con fixtures básicas
- [ ] Tests unitarios funcionando
- [ ] Coverage measurement configurado
- [ ] Pre-commit hooks instalados
- [ ] Todos los tests pasan

### **Comandos de Verificación**

```bash
# Verificar que todo funciona
pytest --cov=app --cov-report=term-missing -v

# Verificar quality tools
black --check app/ tests/
isort --check-only app/ tests/
flake8 app/ tests/

# Ejecutar pre-commit
pre-commit run --all-files
```

---

## 🎯 Entregables

1. **Estructura de testing** completa y organizada
2. **Fixtures básicas** funcionando para auth y database
3. **Tests unitarios** para modelos y servicios básicos
4. **Coverage setup** con reportes configurados
5. **Quality tools** configurados (black, isort, flake8)

---

## 📚 Recursos Adicionales

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [pytest-asyncio Documentation](https://pytest-asyncio.readthedocs.io/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)

---

**🎯 Con este setup, tienes una base sólida para testing que crecerá con tu proyecto. En las siguientes prácticas construiremos sobre esta fundación.**
