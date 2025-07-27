# Recursos de Apoyo - Testing y Calidad

📚 **Guía completa de recursos para testing con FastAPI**  
🎯 **Para consulta durante y después del bootcamp**

## 📖 Documentación Oficial

### **FastAPI Testing**

- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/) - Guía oficial
- [Testing Dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/) - Override dependencies
- [Testing WebSockets](https://fastapi.tiangolo.com/advanced/testing-websockets/) - Testing avanzado

### **pytest Documentation**

- [pytest Documentation](https://docs.pytest.org/) - Documentación completa
- [pytest Fixtures](https://docs.pytest.org/en/6.2.x/fixture.html) - Guía de fixtures
- [pytest Parametrize](https://docs.pytest.org/en/6.2.x/parametrize.html) - Tests parametrizados

### **Coverage.py**

- [Coverage.py Docs](https://coverage.readthedocs.io/) - Documentación oficial
- [Configuration](https://coverage.readthedocs.io/en/6.5.0/config.html) - Configuración .coveragerc

---

## 🛠️ Herramientas Esenciales

### **Testing Frameworks**

#### **pytest** (Principal)

```bash
pip install pytest pytest-asyncio pytest-cov
```

- Framework de testing más popular para Python
- Fixtures poderosas y flexibles
- Plugins extensivos

#### **httpx** (HTTP Client para Testing)

```bash
pip install httpx
```

- Cliente HTTP moderno para testing
- Compatible con FastAPI TestClient
- Soporte async/await

#### **pytest-cov** (Coverage)

```bash
pip install pytest-cov
```

- Plugin para medir coverage con pytest
- Integración perfecta
- Múltiples formatos de reporte

### **Quality Tools**

#### **black** (Code Formatting)

```bash
pip install black
black app/ tests/
```

- Formateador automático de código
- Estilo consistente
- Integración con IDEs

#### **flake8** (Linting)

```bash
pip install flake8
flake8 app/ tests/
```

- Linter para Python
- Detecta errores de estilo
- Configurable

#### **mypy** (Type Checking)

```bash
pip install mypy
mypy app/
```

- Verificador de tipos estáticos
- Detecta errores de tipos
- Mejora calidad del código

### **Database Testing**

#### **SQLAlchemy Testing**

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

# Engine para testing
engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
```

#### **Factory Boy** (Factories para Testing)

```bash
pip install factory-boy
```

- Factories para crear objetos de testing
- Datos realistas
- Relaciones complejas

---

## 📋 Checklists de Testing

### **Setup Inicial**

- [ ] **pytest instalado** y configurado
- [ ] **pytest.ini** creado con configuraciones
- [ ] **.coveragerc** configurado
- [ ] **Estructura tests/** organizada
- [ ] **conftest.py** con fixtures base
- [ ] **requirements-dev.txt** actualizado

### **Tests de Autenticación**

- [ ] **Registro de usuario** (éxito y fallos)
- [ ] **Login** (credenciales válidas e inválidas)
- [ ] **JWT tokens** (generación y validación)
- [ ] **Token expiration** manejado correctamente
- [ ] **Refresh tokens** funcionando
- [ ] **Logout** invalidando tokens

### **Tests de Endpoints**

- [ ] **GET endpoints** (éxito, 404, sin auth)
- [ ] **POST endpoints** (creación, validaciones)
- [ ] **PUT endpoints** (actualización, permisos)
- [ ] **DELETE endpoints** (eliminación, verificación)
- [ ] **Paginación** funcionando correctamente
- [ ] **Filtros y búsqueda** implementados

### **Tests de Seguridad**

- [ ] **Aislamiento entre usuarios** verificado
- [ ] **Autorización** funcionando (roles/permisos)
- [ ] **Validación de entrada** robusta
- [ ] **SQL injection** prevenido
- [ ] **XSS protection** implementado
- [ ] **Rate limiting** (si aplica)

### **Coverage y Calidad**

- [ ] **Coverage >85%** en módulos críticos
- [ ] **Tests de edge cases** incluidos
- [ ] **Error handling** probado
- [ ] **Integration tests** E2E
- [ ] **Performance tests** básicos
- [ ] **Documentation** de tests actualizada

---

## 💡 Patrones y Mejores Prácticas

### **Organización de Tests**

#### **Estructura Recomendada**

```
tests/
├── conftest.py              # Configuración global
├── fixtures/                # Fixtures organizadas
│   ├── auth_fixtures.py
│   ├── user_fixtures.py
│   └── database_fixtures.py
├── helpers/                 # Funciones helper
│   ├── auth_helpers.py
│   └── test_utils.py
├── unit/                    # Tests unitarios
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/             # Tests de integración
│   ├── test_auth_flow.py
│   ├── test_user_workflow.py
│   └── test_api_endpoints.py
└── e2e/                     # Tests end-to-end
    ├── test_complete_scenarios.py
    └── test_user_journeys.py
```

#### **Naming Conventions**

```python
# ✅ Buenos nombres
def test_should_return_404_when_user_not_found():
    pass

def test_should_create_task_with_valid_data():
    pass

def test_should_reject_invalid_email_format():
    pass

# ❌ Malos nombres
def test_user():
    pass

def test_1():
    pass

def test_something():
    pass
```

### **Fixtures Efectivas**

#### **Scope de Fixtures**

```python
@pytest.fixture(scope="session")
def app():
    """App instance - una vez por sesión."""
    pass

@pytest.fixture(scope="module")
def db_engine():
    """Engine de DB - una vez por módulo."""
    pass

@pytest.fixture(scope="function")  # Default
def user():
    """Usuario - nuevo para cada test."""
    pass
```

#### **Factories vs Fixtures**

```python
# Fixture para casos simples
@pytest.fixture
def test_user():
    return User(email="test@example.com", name="Test User")

# Factory para casos complejos
@pytest.fixture
def user_factory():
    def _create_user(**kwargs):
        defaults = {"email": "test@example.com", "name": "Test User"}
        defaults.update(kwargs)
        return User(**defaults)
    return _create_user
```

### **Testing Async Code**

#### **Async Tests con pytest-asyncio**

```python
import pytest

@pytest.mark.asyncio
async def test_async_endpoint(client):
    async with client:
        response = await client.get("/async-endpoint")
        assert response.status_code == 200
```

#### **Testing Background Tasks**

```python
def test_background_task_execution(client, mocker):
    mock_task = mocker.patch("app.tasks.send_email.delay")

    response = client.post("/send-notification", json={"email": "test@example.com"})

    assert response.status_code == 200
    mock_task.assert_called_once_with("test@example.com")
```

---

## 🎯 Ejemplos de Tests por Tipo

### **Unit Tests**

#### **Test de Modelo**

```python
def test_user_model_creation():
    """Test creación básica de usuario."""
    user = User(
        email="test@example.com",
        full_name="Test User",
        hashed_password="hashed_password_here"
    )

    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.is_active is True  # Default value
    assert user.is_admin is False  # Default value
```

#### **Test de Servicio**

```python
def test_create_user_service(db_session):
    """Test servicio de creación de usuario."""
    user_data = {
        "email": "service@example.com",
        "password": "securepass123",
        "full_name": "Service User"
    }

    user = UserService.create_user(db_session, user_data)

    assert user.email == user_data["email"]
    assert user.full_name == user_data["full_name"]
    assert verify_password(user_data["password"], user.hashed_password)
```

### **Integration Tests**

#### **Test de Workflow Completo**

```python
def test_user_registration_and_login_flow(client):
    """Test flujo completo: registro → login → acceso protegido."""

    # 1. Registro
    user_data = {
        "email": "flow@example.com",
        "password": "flowpass123",
        "full_name": "Flow User"
    }
    register_response = client.post("/auth/register", json=user_data)
    assert register_response.status_code == 201

    # 2. Login
    login_data = {"username": user_data["email"], "password": user_data["password"]}
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Acceso a endpoint protegido
    profile_response = client.get("/users/me", headers=headers)
    assert profile_response.status_code == 200

    profile = profile_response.json()
    assert profile["email"] == user_data["email"]
```

### **Performance Tests**

#### **Test de Performance Básico**

```python
import time
import pytest

@pytest.mark.slow
def test_bulk_operations_performance(client, auth_headers):
    """Test que operaciones en lote no excedan tiempo límite."""

    start_time = time.time()

    # Crear 100 tareas
    for i in range(100):
        task_data = {"title": f"Task {i}", "description": f"Description {i}"}
        response = client.post("/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == 201

    creation_time = time.time() - start_time

    # Verificar que no toma más de 10 segundos
    assert creation_time < 10.0, f"Creation took {creation_time:.2f}s, expected <10s"

    # Test de consulta
    start_time = time.time()
    response = client.get("/tasks/", headers=auth_headers)
    query_time = time.time() - start_time

    assert response.status_code == 200
    assert len(response.json()) >= 100
    assert query_time < 2.0, f"Query took {query_time:.2f}s, expected <2s"
```

---

## 🚨 Troubleshooting Común

### **Errores de Database**

#### **"Database locked"**

```python
# Solución: Usar StaticPool para SQLite
from sqlalchemy.pool import StaticPool

engine = create_engine(
    "sqlite:///./test.db",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # ← Esto resuelve el problema
)
```

#### **"Table doesn't exist"**

```python
# En conftest.py, asegurar creación de tablas
@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)  # ← Crear tablas
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # ← Limpiar tablas
```

### **Errores de Autenticación**

#### **"Token has expired"**

```python
# Crear tokens con tiempo suficiente para tests
@pytest.fixture
def auth_headers(test_user):
    token = create_access_token(
        {"sub": test_user.email},
        expires_delta=timedelta(hours=1)  # ← Tiempo suficiente
    )
    return {"Authorization": f"Bearer {token}"}
```

#### **"Invalid token format"**

```python
# Verificar formato correcto
headers = {"Authorization": f"Bearer {token}"}  # ← "Bearer " es requerido
```

### **Errores de Coverage**

#### **"No coverage data found"**

```bash
# Verificar que pytest-cov esté instalado
pip install pytest-cov

# Ejecutar con coverage explícitamente
pytest --cov=app
```

#### **"Files not found in coverage"**

```ini
# En .coveragerc, verificar [run] source
[run]
source = app  # ← Debe apuntar al directorio correcto
```

---

## 📚 Recursos Adicionales

### **Libros Recomendados**

1. **"Effective Python"** by Brett Slatkin

   - Capítulos sobre testing y debugging
   - Mejores prácticas de Python

2. **"Test-Driven Development with Python"** by Harry Percival

   - TDD completo con Django/Flask
   - Principios aplicables a FastAPI

3. **"Clean Code"** by Robert C. Martin
   - Principios de código limpio
   - Aplicable a tests también

### **Cursos Online**

1. **"FastAPI Testing Masterclass"** (Udemy)

   - Enfoque específico en FastAPI
   - Casos prácticos avanzados

2. **"pytest Complete Guide"** (Pluralsight)

   - Coverage completo de pytest
   - Fixtures avanzadas

3. **"API Testing with Python"** (Test Automation University)
   - Testing de APIs en general
   - Buenas prácticas

### **Blogs y Artículos**

1. **FastAPI Official Blog**

   - [Testing FastAPI Applications](https://fastapi.tiangolo.com/tutorial/testing/)
   - Casos de uso reales

2. **Real Python**

   - [Testing Your Code](https://realpython.com/python-testing/)
   - [pytest: How to Write Better Tests](https://realpython.com/pytest-python-testing/)

3. **Martin Fowler**
   - [Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html)
   - [Mocks Aren't Stubs](https://martinfowler.com/articles/mocksArentStubs.html)

### **Herramientas Complementarias**

#### **Postman/Insomnia** (Testing Manual)

- Testing manual de APIs
- Creación de collections
- Automation básica

#### **Newman** (Postman CLI)

```bash
npm install -g newman
newman run collection.json
```

#### **Locust** (Load Testing)

```bash
pip install locust
```

- Load testing de APIs
- Performance testing avanzado

#### **Faker** (Datos de Testing)

```bash
pip install faker
```

- Generación de datos realistas
- Útil para factories

---

## 🎯 Checklist Final de Recursos

### **Herramientas Instaladas**

- [ ] pytest + plugins esenciales
- [ ] Coverage tools (pytest-cov)
- [ ] Quality tools (black, flake8, mypy)
- [ ] Database testing tools
- [ ] HTTP testing client (httpx)

### **Documentación Guardada**

- [ ] FastAPI testing docs bookmarked
- [ ] pytest documentation accessible
- [ ] Coverage.py docs saved
- [ ] Este recurso guardado localmente

### **Templates Preparados**

- [ ] conftest.py template
- [ ] pytest.ini template
- [ ] .coveragerc template
- [ ] CI/CD workflow template
- [ ] Test structure templates

### **Conocimientos Clave**

- [ ] Fixtures vs factories
- [ ] Unit vs integration vs e2e tests
- [ ] Coverage interpretation
- [ ] Mocking strategies
- [ ] Performance testing basics

---

¡Con estos recursos tienes todo lo necesario para implementar testing profesional en tus proyectos FastAPI! 📚✨

**Próximos pasos**: Guarda estos recursos, implementa los ejemplos en tu proyecto, y úsalos como referencia durante el desarrollo.
