# Recursos de Apoyo - Testing y Quality Assurance

## 📚 Documentación Oficial

### Framework de Testing

- **[pytest Documentation](https://docs.pytest.org/)** - Documentación completa del framework
- **[pytest-asyncio](https://pytest-asyncio.readthedocs.io/)** - Testing asíncrono
- **[httpx Documentation](https://www.python-httpx.org/)** - Cliente HTTP para testing

### FastAPI Testing

- **[FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)** - Guía oficial
- **[Testing Dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/)** - Override de dependencias
- **[Testing WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)** - Testing avanzado

### Quality Assurance

- **[Black Documentation](https://black.readthedocs.io/)** - Code formatter
- **[isort Documentation](https://pycqa.github.io/isort/)** - Import sorting
- **[flake8 Documentation](https://flake8.pycqa.org/)** - Style guide enforcement
- **[mypy Documentation](https://mypy.readthedocs.io/)** - Static type checking
- **[Coverage.py](https://coverage.readthedocs.io/)** - Code coverage measurement

---

## 🛠️ Herramientas Recomendadas

### Testing Frameworks

```bash
# Framework principal
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0

# Cliente HTTP para testing
httpx>=0.24.0

# Mocking y fixtures
pytest-mock>=3.11.0
factory-boy>=3.3.0
freezegun>=1.2.0

# Performance testing
pytest-benchmark>=4.0.0
pytest-xdist>=3.3.0  # Paralelización
```

### Quality Assurance

```bash
# Formateo y linting
black>=23.7.0
isort>=5.12.0
flake8>=6.0.0
mypy>=1.5.0

# Security scanning
bandit>=1.7.5
safety>=2.3.0

# Complexity analysis
radon>=6.0.1
vulture>=2.9.1  # Dead code detection
```

### CI/CD Tools

```bash
# Pre-commit hooks
pre-commit>=3.3.0

# GitHub Actions
# (No installation needed, configuration only)

# Load testing
locust>=2.16.0
```

---

## 📖 Tutoriales y Guías

### Testing Fundamentals

#### 1. pytest Básico

```python
# test_example.py
def test_simple():
    assert 1 + 1 == 2

def test_with_fixture(sample_data):
    assert sample_data is not None

@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 3),
    (3, 4)
])
def test_parametrized(input, expected):
    assert input + 1 == expected
```

#### 2. Fixtures Avanzados

```python
# conftest.py
@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("sqlite:///test.db")
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

#### 3. Mocking Patterns

```python
from unittest.mock import Mock, patch, AsyncMock

# Mock simple
@patch('app.service.external_api_call')
def test_with_mock(mock_api):
    mock_api.return_value = {"status": "success"}
    result = my_function()
    assert result == "success"

# Mock asíncrono
@patch('app.service.async_api_call')
async def test_async_mock(mock_async):
    mock_async.return_value = AsyncMock(return_value="result")
    result = await my_async_function()
    assert result == "result"
```

### FastAPI Testing Patterns

#### 1. Testing Endpoints

```python
@pytest.mark.asyncio
async def test_create_item(client: AsyncClient):
    response = await client.post(
        "/items/",
        json={"name": "Test Item", "description": "Test"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
```

#### 2. Testing Authentication

```python
@pytest.fixture
async def authenticated_client(client: AsyncClient):
    # Login to get token
    login_response = await client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "test"}
    )
    token = login_response.json()["access_token"]

    # Set authorization header
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client
```

#### 3. Database Testing

```python
@pytest.fixture
async def test_db():
    # Setup test database
    engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
```

---

## 🎯 Mejores Prácticas

### Testing Best Practices

#### 1. Organización de Tests

```
tests/
├── conftest.py           # Fixtures globales
├── unit/                 # Tests unitarios
│   ├── test_models.py
│   ├── test_schemas.py
│   └── test_utils.py
├── integration/          # Tests de integración
│   ├── test_api.py
│   └── test_database.py
├── e2e/                  # Tests end-to-end
│   └── test_workflows.py
└── fixtures/             # Fixtures específicos
    ├── user_fixtures.py
    └── data_fixtures.py
```

#### 2. Naming Conventions

```python
# Buenas prácticas para nombres
def test_should_create_user_when_valid_data_provided():
    """Test should describe the expected behavior."""
    pass

def test_should_raise_error_when_invalid_email():
    """Test should describe error conditions."""
    pass

class TestUserService:
    """Group related tests in classes."""

    def test_create_user_success(self):
        pass

    def test_create_user_duplicate_email_error(self):
        pass
```

#### 3. Test Structure (AAA Pattern)

```python
def test_user_creation():
    # Arrange
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }

    # Act
    user = create_user(user_data)

    # Assert
    assert user.email == user_data["email"]
    assert user.is_active is True
```

### Quality Assurance Best Practices

#### 1. Configuración Óptima

```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.coverage.run]
source = ["app"]
omit = ["*/tests/*", "*/migrations/*"]

[tool.coverage.report]
precision = 2
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError"
]
```

#### 2. Scripts de Automatización

```bash
#!/bin/bash
# scripts/test_all.sh

set -e  # Exit on any error

echo "🧹 Formatting code..."
black app tests

echo "📦 Sorting imports..."
isort app tests

echo "🔍 Linting..."
flake8 app tests

echo "🔧 Type checking..."
mypy app

echo "🧪 Running tests..."
pytest --cov=app --cov-report=html --cov-report=term-missing

echo "✅ All checks passed!"
```

---

## 📊 Métricas y Objetivos

### Coverage Targets

```yaml
# Objetivos de cobertura por tipo de código
Models: 95%+ # Lógica de negocio crítica
Services: 90%+ # Servicios de aplicación
API Routes: 85%+ # Endpoints HTTP
Utils: 80%+ # Funciones de utilidad
Config: 70%+ # Configuración
```

### Performance Benchmarks

```python
# Objetivos de performance para testing
Response Time: < 200ms    # API endpoints
Test Suite: < 5 minutes   # Ejecución completa
DB Queries: < 100ms       # Consultas individuales
Load Test: 100+ req/s     # Throughput mínimo
```

---

## 🔧 Configuraciones de Ejemplo

### GitHub Actions CI/CD

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run quality checks
        run: |
          black --check app tests
          isort --check-only app tests
          flake8 app tests
          mypy app

      - name: Run tests
        run: |
          pytest --cov=app --cov-report=xml --cov-report=term-missing
        env:
          DATABASE_URL: postgresql://postgres:test@localhost/test

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ['--profile', 'black']

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

---

## 🎓 Recursos de Aprendizaje

### Cursos Online

- **[Testing Python Applications](https://realpython.com/python-testing/)** - Real Python
- **[pytest Course](https://www.pluralsight.com/courses/testing-python-pytest)** - Pluralsight
- **[FastAPI Testing](https://testdriven.io/courses/tdd-fastapi/)** - Test-Driven Development

### Libros Recomendados

- **"Effective Python Testing with pytest"** - Brian Okken
- **"Architecture Patterns with Python"** - Harry Percival & Bob Gregory
- **"Clean Code"** - Robert C. Martin

### Videos y Talks

- **[pytest: Rapid, Simple, Effective Testing](https://www.youtube.com/watch?v=9jmT2u7r8iw)** - Brian Okken
- **[Testing FastAPI Applications](https://www.youtube.com/watch?v=GV0W6FvvANA)** - Sebastián Ramírez
- **[Advanced pytest Techniques](https://www.youtube.com/watch?v=jUCOqeJYGns)** - Florian Bruhin

---

## 🛠️ Herramientas de Desarrollo

### VS Code Extensions

```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.flake8",
    "ms-python.black-formatter",
    "ms-python.isort",
    "charliermarsh.ruff",
    "ms-python.mypy-type-checker",
    "littlefoxteam.vscode-python-test-adapter"
  ]
}
```

### PyCharm Configurations

- **Test Runner**: Configure pytest as default
- **Code Style**: Import Black configuration
- **Type Checking**: Enable mypy integration
- **Coverage**: Enable coverage display in editor

---

## 📝 Checklists de Referencia

### Pre-commit Checklist

- [ ] Tests pasan localmente
- [ ] Coverage ≥ objetivo definido
- [ ] Black formatting aplicado
- [ ] Imports organizados con isort
- [ ] Sin errores de flake8
- [ ] Type checking con mypy exitoso
- [ ] Documentación actualizada

### Release Checklist

- [ ] Todos los tests CI/CD pasan
- [ ] Coverage reports generados
- [ ] Performance tests ejecutados
- [ ] Security scans completados
- [ ] Load testing validado
- [ ] Documentación actualizada
- [ ] CHANGELOG.md actualizado

---

## 🚨 Troubleshooting Común

### Problemas Frecuentes

#### 1. Tests Async Fallan

```python
# ❌ Incorrecto
def test_async_function():
    result = async_function()
    assert result == expected

# ✅ Correcto
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

#### 2. Database Tests Interfieren

```python
# ✅ Usar transacciones para aislamiento
@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

#### 3. Mocks No Funcionan

```python
# ❌ Mock en lugar incorrecto
@patch('test_module.external_service')
def test_function(mock_service):
    pass

# ✅ Mock en el lugar donde se usa
@patch('app.service.external_service')
def test_function(mock_service):
    pass
```

---

## 📞 Soporte y Comunidad

### Comunidades

- **[pytest Gitter](https://gitter.im/pytest-dev/pytest)** - Chat en tiempo real
- **[FastAPI Discord](https://discord.gg/VQjSZaeJmf)** - Comunidad oficial
- **[Python Testing Reddit](https://www.reddit.com/r/learnpython/)** - Discusiones

### Stack Overflow Tags

- `pytest`
- `fastapi-testing`
- `python-testing`
- `pytest-asyncio`
- `test-coverage`

---

_Estos recursos proporcionan una base sólida para dominar testing y quality assurance en FastAPI, con referencias actualizadas y ejemplos prácticos para el desarrollo profesional._
