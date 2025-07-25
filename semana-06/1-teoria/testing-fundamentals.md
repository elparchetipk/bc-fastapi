# 🧪 Fundamentos de Testing en Python y FastAPI

## 📚 Introducción

El testing es una disciplina fundamental en el desarrollo de software que garantiza la calidad, confiabilidad y mantenibilidad del código. En esta guía aprenderemos los conceptos esenciales de testing aplicados específicamente a aplicaciones FastAPI.

---

## 🎯 ¿Por qué Testing es Crítico?

### **Beneficios del Testing**

- **🛡️ Prevención de Bugs:** Detecta errores antes de llegar a producción
- **📈 Confianza en Refactoring:** Permite cambios seguros en el código
- **📖 Documentación Viva:** Los tests actúan como especificación ejecutable
- **⚡ Desarrollo Más Rápido:** Reduce tiempo de debugging manual
- **🎯 Mejor Diseño:** Código testeable tiende a ser mejor diseñado

### **Costo del Testing vs No Testing**

```
Sin Tests:
- Desarrollo inicial: Rápido ⚡
- Mantenimiento: Muy lento 🐌
- Bugs en producción: Frecuentes 🚨
- Refactoring: Arriesgado ⚠️

Con Tests:
- Desarrollo inicial: Moderado 🚶
- Mantenimiento: Rápido ⚡
- Bugs en producción: Raros ✅
- Refactoring: Seguro 🛡️
```

---

## 🧪 Tipos de Testing

### **1. Pirámide de Testing**

```
         /\
        /  \
       / E2E \      <- Pocos tests, alto valor, lentos, costosos
      /______\
     /        \
    /Integration\ <- Cantidad moderada, verifican integración
   /____________\
  /              \
 /   Unit Tests   \  <- Muchos tests, rápidos, baratos
/________________\
```

### **Unit Tests (Base de la Pirámide)**

**Características:**

- **Scope:** Función o método individual
- **Speed:** Muy rápidos (< 1ms)
- **Dependencies:** Aislados, sin dependencias externas
- **Purpose:** Verificar lógica de negocio específica

**Ejemplo:**

```python
def calculate_tax(price: float, tax_rate: float) -> float:
    """Calcula el impuesto para un precio dado."""
    if price < 0:
        raise ValueError("Price cannot be negative")
    return price * tax_rate

# Unit Test
def test_calculate_tax_valid_input():
    result = calculate_tax(100.0, 0.1)
    assert result == 10.0

def test_calculate_tax_negative_price():
    with pytest.raises(ValueError, match="Price cannot be negative"):
        calculate_tax(-10.0, 0.1)
```

### **Integration Tests (Medio de la Pirámide)**

**Características:**

- **Scope:** Interacción entre componentes
- **Speed:** Moderados (100ms - 1s)
- **Dependencies:** Base de datos, APIs externas
- **Purpose:** Verificar que componentes trabajen juntos

**Ejemplo FastAPI:**

```python
def test_create_user_endpoint():
    response = client.post("/users", json={
        "email": "test@example.com",
        "password": "secure123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    assert "password" not in response.json()
```

### **End-to-End Tests (Cima de la Pirámide)**

**Características:**

- **Scope:** Flujo completo de usuario
- **Speed:** Lentos (segundos a minutos)
- **Dependencies:** Sistema completo, UI, base de datos
- **Purpose:** Verificar scenarios de usuario real

**Ejemplo de Flujo:**

```python
def test_complete_purchase_flow():
    # 1. Usuario se registra
    register_response = client.post("/auth/register", json=user_data)
    assert register_response.status_code == 201

    # 2. Usuario hace login
    login_response = client.post("/auth/login", data=login_data)
    token = login_response.json()["access_token"]

    # 3. Usuario agrega producto al carrito
    headers = {"Authorization": f"Bearer {token}"}
    add_to_cart = client.post("/cart", json=product_data, headers=headers)
    assert add_to_cart.status_code == 200

    # 4. Usuario completa compra
    purchase = client.post("/orders", headers=headers)
    assert purchase.status_code == 201
```

---

## 🔧 Testing con pytest

### **¿Por qué pytest?**

- **Sintaxis Simple:** No requiere herencia de clases especiales
- **Auto-discovery:** Encuentra tests automáticamente
- **Fixtures Poderosas:** Sistema robusto de setup/teardown
- **Plugins Extensos:** Ecosistema rico de extensiones
- **Reportes Ricos:** Output detallado y customizable

### **Estructura Básica de pytest**

```python
# test_example.py

def test_simple_assertion():
    """Test básico con assertion simple."""
    assert 2 + 2 == 4

def test_with_setup():
    """Test con setup inline."""
    # Setup
    user = User(name="Test User", email="test@test.com")

    # Action
    result = user.get_display_name()

    # Assert
    assert result == "Test User"

def test_with_fixture(user_fixture):
    """Test usando fixture."""
    assert user_fixture.email == "test@test.com"
```

### **Convenciones de pytest**

```python
# Estructura de archivos
tests/
├── __init__.py
├── conftest.py          # Fixtures compartidas
├── test_auth.py         # Tests para módulo auth
├── test_users.py        # Tests para módulo users
└── test_products.py     # Tests para módulo products

# Naming conventions
- Archivos: test_*.py o *_test.py
- Funciones: test_*()
- Clases: Test* (opcional)
- Métodos: test_*()
```

---

## 🎭 Fixtures en pytest

### **¿Qué son las Fixtures?**

Las fixtures son funciones que proporcionan data o setup para tests. Son la base del sistema de dependency injection de pytest.

### **Fixture Básica**

```python
# conftest.py
import pytest
from app.models import User

@pytest.fixture
def user():
    """Fixture que crea un usuario de prueba."""
    return User(
        name="Test User",
        email="test@example.com",
        is_active=True
    )

# test_users.py
def test_user_display_name(user):
    assert user.get_display_name() == "Test User"

def test_user_is_active(user):
    assert user.is_active is True
```

### **Fixture Scopes**

```python
@pytest.fixture(scope="function")  # Default: nueva instancia por test
def user_function():
    return create_user()

@pytest.fixture(scope="class")     # Una instancia por test class
def user_class():
    return create_user()

@pytest.fixture(scope="module")    # Una instancia por módulo
def database_connection():
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture(scope="session")   # Una instancia por sesión de testing
def global_config():
    return load_config()
```

### **Fixtures con Cleanup**

```python
@pytest.fixture
def temporary_file():
    """Fixture que crea archivo temporal y lo limpia."""
    file_path = "/tmp/test_file.txt"

    # Setup
    with open(file_path, "w") as f:
        f.write("test content")

    yield file_path  # Provee el valor al test

    # Cleanup
    os.remove(file_path)

def test_file_content(temporary_file):
    with open(temporary_file, "r") as f:
        content = f.read()
    assert content == "test content"
```

---

## 🌐 Testing FastAPI Applications

### **TestClient de FastAPI**

FastAPI incluye `TestClient` basado en Starlette para testing fácil:

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

### **Testing Endpoints con Datos**

```python
def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Laptop", "price": 999.99}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["price"] == 999.99
    assert "id" in data

def test_create_item_invalid_data():
    response = client.post(
        "/items/",
        json={"name": "", "price": -10}  # Invalid data
    )
    assert response.status_code == 422  # Validation error
```

### **Testing con Headers y Authentication**

```python
def test_protected_endpoint():
    # Sin token
    response = client.get("/users/me")
    assert response.status_code == 401

    # Con token válido
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200

def test_admin_only_endpoint():
    admin_token = get_admin_token()
    user_token = get_user_token()

    # Admin puede acceder
    response = client.delete(
        "/users/123",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200

    # Usuario regular no puede
    response = client.delete(
        "/users/123",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403
```

---

## 🗃️ Testing con Base de Datos

### **Estrategias de Database Testing**

#### **1. Base de Datos de Testing Separada**

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Test database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(test_db):
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

#### **2. Transaccional Testing**

```python
@pytest.fixture
def db_session():
    session = TestingSessionLocal()
    transaction = session.begin()
    yield session
    transaction.rollback()  # Rollback después de cada test
    session.close()
```

### **Factory Pattern para Test Data**

```python
# tests/factories.py
import factory
from app.models import User, Product

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker("name")
    email = factory.Faker("email")
    is_active = True

class ProductFactory(factory.Factory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    price = factory.Faker("pydecimal", left_digits=3, right_digits=2, positive=True)
    category = factory.Faker("word")

# Usage in tests
def test_user_creation():
    user = UserFactory()
    assert user.name is not None
    assert "@" in user.email

def test_multiple_products():
    products = ProductFactory.create_batch(5)
    assert len(products) == 5
```

---

## 🎭 Mocking y Test Doubles

### **¿Cuándo Usar Mocks?**

- **External APIs:** No queremos hacer calls reales
- **Slow Operations:** Base de datos, file I/O
- **Unpredictable Behavior:** Random, time, network
- **Error Scenarios:** Simular failures

### **Tipos de Test Doubles**

```python
# 1. STUB - Respuesta predeterminada
def test_with_stub(mocker):
    mocker.patch("app.services.get_exchange_rate", return_value=1.2)
    result = calculate_price_in_usd(100, "EUR")
    assert result == 120.0

# 2. MOCK - Verificar interacciones
def test_with_mock(mocker):
    mock_email = mocker.patch("app.services.send_email")

    register_user("test@example.com")

    mock_email.assert_called_once_with(
        to="test@example.com",
        subject="Welcome!"
    )

# 3. SPY - Mock parcial
def test_with_spy(mocker):
    user_service = UserService()
    spy = mocker.spy(user_service, "validate_email")

    user_service.create_user("test@example.com")

    spy.assert_called_once_with("test@example.com")

# 4. FAKE - Implementación simplificada
class FakeEmailService:
    def __init__(self):
        self.sent_emails = []

    def send_email(self, to, subject, body):
        self.sent_emails.append({"to": to, "subject": subject, "body": body})

@pytest.fixture
def fake_email_service():
    return FakeEmailService()
```

### **Mocking con pytest-mock**

```python
# Mock de función externa
def test_api_call(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"rate": 1.2}
    mock_response.status_code = 200

    mocker.patch("requests.get", return_value=mock_response)

    result = get_exchange_rate("USD", "EUR")
    assert result == 1.2

# Mock de método de clase
def test_user_save(mocker):
    mock_save = mocker.patch.object(User, "save")

    user = User(name="Test")
    user_service = UserService()
    user_service.create_user(user)

    mock_save.assert_called_once()

# Mock de variable de entorno
def test_config_loading(mocker):
    mocker.patch.dict("os.environ", {"DEBUG": "true"})
    config = load_config()
    assert config.debug is True
```

---

## ⚡ Testing Asíncrono

### **pytest-asyncio Setup**

```python
# pytest.ini
[tool:pytest]
asyncio_mode = auto

# O usando decorator
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected_value
```

### **Testing FastAPI Endpoints Async**

```python
import httpx
import pytest
from app.main import app

@pytest.mark.asyncio
async def test_async_endpoint():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/async-endpoint")
    assert response.status_code == 200

# Fixture para async client
@pytest.fixture
async def async_client():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.mark.asyncio
async def test_with_async_client(async_client):
    response = await async_client.post("/users", json={"name": "Test"})
    assert response.status_code == 201
```

### **Mocking Async Functions**

```python
@pytest.mark.asyncio
async def test_async_service(mocker):
    # Mock async function
    mock_async_func = mocker.patch(
        "app.services.fetch_user_data",
        return_value=asyncio.coroutine(lambda: {"id": 1, "name": "Test"})()
    )

    result = await user_service.get_user_info(1)
    assert result["name"] == "Test"
    mock_async_func.assert_called_once_with(1)
```

---

## 📊 Coverage Analysis

### **¿Qué es Coverage?**

Coverage mide qué porcentaje del código es ejecutado durante los tests.

### **Tipos de Coverage**

- **Line Coverage:** % de líneas ejecutadas
- **Branch Coverage:** % de ramas (if/else) ejecutadas
- **Function Coverage:** % de funciones llamadas
- **Statement Coverage:** % de statements ejecutados

### **Configurando Coverage**

```toml
# pyproject.toml
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

### **Ejecutando Coverage**

```bash
# Ejecutar tests con coverage
pytest --cov=app --cov-report=html --cov-report=term-missing

# Solo reporte de coverage
coverage run -m pytest
coverage report
coverage html
```

### **Interpretando Coverage Reports**

```
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
app/__init__.py          2      0   100%
app/main.py             45      3    93%   23-25
app/models.py           67      8    88%   45, 67-72, 89
app/services.py         34      0   100%
--------------------------------------------------
TOTAL                  148     11    93%
```

**Interpretación:**

- **Stmts:** Total de statements
- **Miss:** Statements no ejecutados
- **Cover:** Porcentaje de coverage
- **Missing:** Líneas específicas no cubiertas

---

## 🎯 Estrategias de Testing

### **Test-Driven Development (TDD)**

```python
# 1. RED - Escribir test que falla
def test_calculate_discount():
    result = calculate_discount(100, 0.1)
    assert result == 10

# 2. GREEN - Escribir mínimo código para pasar
def calculate_discount(price, rate):
    return price * rate

# 3. REFACTOR - Mejorar el código
def calculate_discount(price: float, rate: float) -> float:
    if not 0 <= rate <= 1:
        raise ValueError("Rate must be between 0 and 1")
    return price * rate
```

### **Behavior-Driven Development (BDD)**

```python
# Given-When-Then pattern
def test_user_registration():
    # Given - Estado inicial
    initial_user_count = User.count()
    user_data = {"email": "test@example.com", "password": "secure123"}

    # When - Acción
    response = client.post("/auth/register", json=user_data)

    # Then - Resultado esperado
    assert response.status_code == 201
    assert User.count() == initial_user_count + 1
    assert response.json()["email"] == user_data["email"]
```

### **Property-Based Testing**

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=0), st.floats(min_value=0, max_value=1))
def test_calculate_discount_properties(price, rate):
    """Test que el descuento nunca exceda el precio original."""
    discount = calculate_discount(price, rate)
    assert 0 <= discount <= price
```

---

## 🔍 Quality Assurance Tools

### **Linting con flake8**

```python
# .flake8
[flake8]
max-line-length = 88
exclude = migrations,venv,env
ignore = E203,W503

# Ejemplo de violaciones
def bad_function( x,y ):  # E201,E202: Whitespace issues
    if x>5:               # E225: Missing whitespace around operator
        return y*2        # E225: Missing whitespace around operator
```

### **Formatting con black**

```python
# Antes de black
def function(x,y,z):
    if x>5:return y*z
    else:return x+y

# Después de black
def function(x, y, z):
    if x > 5:
        return y * z
    else:
        return x + y
```

### **Type Checking con mypy**

```python
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

# Ejemplo con type hints
def process_user_data(user_id: int, data: Dict[str, Any]) -> User:
    user = User.get(user_id)
    if user is None:
        raise ValueError(f"User {user_id} not found")

    user.update(data)
    return user
```

---

## 🔄 Continuous Integration

### **GitHub Actions para Testing**

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v3
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests with coverage
        run: |
          pytest --cov=app --cov-report=xml --cov-report=term-missing

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### **Pre-commit Hooks**

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
```

---

## 📈 Best Practices

### **DO - Mejores Prácticas**

```python
# ✅ Tests descriptivos y específicos
def test_user_can_update_own_profile_but_not_others():
    pass

# ✅ Arrange-Act-Assert pattern
def test_calculate_tax():
    # Arrange
    price = 100.0
    tax_rate = 0.1

    # Act
    result = calculate_tax(price, tax_rate)

    # Assert
    assert result == 10.0

# ✅ Un concepto por test
def test_invalid_email_raises_validation_error():
    with pytest.raises(ValidationError, match="Invalid email format"):
        create_user("invalid-email")

# ✅ Fixtures para setup complejo
@pytest.fixture
def authenticated_user():
    user = User.create(email="test@example.com")
    token = create_token(user)
    return {"user": user, "token": token}
```

### **DON'T - Anti-patterns**

```python
# ❌ Tests ambiguos
def test_user_stuff():
    pass

# ❌ Tests dependientes
def test_create_user():
    global created_user
    created_user = User.create("test@example.com")

def test_user_can_login():  # Depende del test anterior
    assert created_user.login("password")

# ❌ Tests sin assertions
def test_user_creation():
    User.create("test@example.com")  # ¿Qué estamos verificando?

# ❌ Testing implementation details
def test_user_creation_calls_validate_email():
    with patch.object(User, '_validate_email') as mock:
        User.create("test@example.com")
        mock.assert_called_once()
```

---

## 🎯 Ejercicios Prácticos

### **Ejercicio 1: Test Básico**

```python
# Implementa la función y su test
def is_prime(n: int) -> bool:
    """Verifica si un número es primo."""
    # Tu implementación aquí
    pass

def test_is_prime():
    # Tu test aquí
    pass
```

### **Ejercicio 2: Test con FastAPI**

```python
# Implementa el endpoint y su test
@app.post("/users")
async def create_user(user: UserCreate):
    # Tu implementación aquí
    pass

def test_create_user_endpoint():
    # Tu test aquí
    pass
```

### **Ejercicio 3: Test con Mock**

```python
# Test que verifique que se envía email al crear usuario
def test_user_creation_sends_welcome_email():
    # Tu test con mock aquí
    pass
```

---

## 📚 Recursos Adicionales

- **[pytest Documentation](https://docs.pytest.org/)** - Documentación oficial
- **[FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)** - Testing guide oficial
- **[Python Testing 101](https://realpython.com/python-testing/)** - Tutorial comprehensivo
- **[Test-Driven Development by Example](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530)** - Libro clásico de TDD

---

**🎯 El testing no es opcional en desarrollo profesional. Es la diferencia entre código que funciona y código en el que confías.**
