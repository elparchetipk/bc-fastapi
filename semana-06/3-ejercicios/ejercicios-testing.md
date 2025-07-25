# Ejercicios de Testing y Quality Assurance

## 🎯 Objetivos

- Aplicar conceptos de testing en proyectos reales
- Implementar herramientas de quality assurance
- Desarrollar suite completo de tests
- Optimizar performance y coverage

## ⏱️ Tiempo Estimado

**120 minutos** (2 horas distribuidas durante la semana)

---

## 📋 Ejercicio 1: Configuración de Testing Framework (30 min)

### Objetivo

Configurar un entorno completo de testing para un proyecto FastAPI existente.

### Tareas

#### 1.1 Setup Inicial

```bash
# Instalar dependencias de testing
pip install pytest pytest-asyncio pytest-cov httpx

# Crear estructura de testing
mkdir -p tests/{unit,integration,fixtures}
touch tests/__init__.py
touch tests/conftest.py
```

#### 1.2 Configurar pytest.ini

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-config
    --strict-markers
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

#### 1.3 Crear Fixtures Básicos

```python
# tests/conftest.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_user_data():
    return {
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "Test User"
    }
```

### Entregable

- [ ] Estructura de testing configurada
- [ ] pytest.ini con configuración básica
- [ ] conftest.py con fixtures esenciales
- [ ] Al menos 3 tests básicos funcionando

---

## 📋 Ejercicio 2: Tests Unitarios y de Integración (40 min)

### Objetivo

Implementar tests unitarios para modelos y tests de integración para endpoints.

### Tareas

#### 2.1 Tests Unitarios - Modelos

```python
# tests/unit/test_models.py
import pytest
from app.models.user import User
from app.core.security import verify_password, get_password_hash

class TestUserModel:
    def test_user_creation(self):
        """Test creación básica de usuario."""
        user = User(
            email="test@example.com",
            hashed_password=get_password_hash("password"),
            full_name="Test User"
        )

        assert user.email == "test@example.com"
        assert user.full_name == "Test User"
        assert user.is_active is True
        assert verify_password("password", user.hashed_password)

    def test_user_email_validation(self):
        """Test validación de email."""
        # Implementar test de validación
        pass
```

#### 2.2 Tests de Integración - Endpoints

```python
# tests/integration/test_auth_endpoints.py
import pytest
from httpx import AsyncClient

class TestAuthEndpoints:
    @pytest.mark.asyncio
    async def test_register_user(self, client: AsyncClient):
        """Test registro de usuario."""
        user_data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "full_name": "New User"
        }

        response = await client.post("/auth/register", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert "id" in data

    @pytest.mark.asyncio
    async def test_login_user(self, client: AsyncClient, sample_user_data):
        """Test login de usuario."""
        # Primero registrar
        await client.post("/auth/register", json=sample_user_data)

        # Luego hacer login
        login_data = {
            "username": sample_user_data["email"],
            "password": sample_user_data["password"]
        }

        response = await client.post("/auth/login", data=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
```

### Entregable

- [ ] 5+ tests unitarios para modelos/schemas
- [ ] 5+ tests de integración para endpoints
- [ ] Tests pasan exitosamente
- [ ] Coverage básico configurado

---

## 📋 Ejercicio 3: Quality Assurance Setup (30 min)

### Objetivo

Configurar herramientas de calidad de código y automatización.

### Tareas

#### 3.1 Configurar Formateo y Linting

```bash
# Instalar herramientas
pip install black isort flake8 mypy

# Configurar pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 88
```

#### 3.2 Script de Quality Check

```bash
# scripts/quality_check.sh
#!/bin/bash

echo "🔍 Ejecutando quality checks..."

echo "1. Formateo con Black..."
black --check app/

echo "2. Ordenando imports..."
isort --check-only app/

echo "3. Linting con Flake8..."
flake8 app/

echo "4. Type checking con MyPy..."
mypy app/

echo "✅ Quality checks completados"
```

#### 3.3 Pre-commit Hooks (Opcional)

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
```

### Entregable

- [ ] Black, isort, flake8, mypy configurados
- [ ] Script de quality check funcionando
- [ ] Código pasa todos los quality checks
- [ ] Pre-commit hooks instalados (opcional)

---

## 📋 Ejercicio 4: Coverage y Reporting (20 min)

### Objetivo

Implementar análisis de cobertura y reportes de testing.

### Tareas

#### 4.1 Configurar Coverage

```bash
# Instalar pytest-cov
pip install pytest-cov

# Ejecutar con coverage
pytest --cov=app --cov-report=html --cov-report=term-missing
```

#### 4.2 Analizar Resultados

```bash
# Generar reporte HTML
pytest --cov=app --cov-report=html

# Abrir htmlcov/index.html
# Identificar líneas no cubiertas
# Agregar tests para mejorar coverage
```

#### 4.3 Configurar Objetivos

```ini
# pytest.ini - agregar
addopts =
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-fail-under=80
```

### Entregable

- [ ] Coverage configurado correctamente
- [ ] Reporte HTML generado
- [ ] Coverage objetivo definido (80%+)
- [ ] Plan para mejorar coverage implementado

---

## 🎯 Ejercicios Adicionales (Avanzados)

### Ejercicio 5: Mocking y Testing Avanzado

**Objetivo:** Implementar mocking para servicios externos

```python
# Ejemplo: Mock de servicio de email
@patch('app.services.email_service.send_email')
async def test_welcome_email(mock_send_email, client):
    mock_send_email.return_value = True

    response = await client.post("/auth/register", json=user_data)

    assert response.status_code == 201
    mock_send_email.assert_called_once()
```

### Ejercicio 6: Performance Testing

**Objetivo:** Implementar tests de performance básicos

```python
import time

async def test_endpoint_performance(client):
    start_time = time.time()

    response = await client.get("/users/")

    end_time = time.time()
    response_time = end_time - start_time

    assert response.status_code == 200
    assert response_time < 1.0  # Menos de 1 segundo
```

### Ejercicio 7: CI/CD Integration

**Objetivo:** Configurar GitHub Actions para testing

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run tests
        run: |
          pytest --cov=app --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

---

## 🏆 Desafíos de Nivel

### Nivel Principiante

- [ ] Configurar testing básico
- [ ] Escribir 10+ tests simples
- [ ] Ejecutar quality checks
- [ ] Alcanzar 60%+ coverage

### Nivel Intermedio

- [ ] Implementar fixtures complejos
- [ ] Usar mocking básico
- [ ] Configurar CI/CD
- [ ] Alcanzar 80%+ coverage

### Nivel Avanzado

- [ ] Implementar testing avanzado
- [ ] Performance testing
- [ ] Load testing básico
- [ ] Alcanzar 90%+ coverage

---

## 🔍 Checklist de Verificación

### Setup y Configuración

- [ ] pytest configurado correctamente
- [ ] Estructura de tests organizada
- [ ] Fixtures básicos implementados
- [ ] Requirements actualizados

### Tests Implementados

- [ ] Tests unitarios para modelos
- [ ] Tests de integración para endpoints
- [ ] Tests de autenticación/autorización
- [ ] Tests de casos de error

### Quality Assurance

- [ ] Black para formateo configurado
- [ ] isort para imports configurado
- [ ] flake8 para linting configurado
- [ ] mypy para type checking configurado

### Coverage y Reporting

- [ ] pytest-cov configurado
- [ ] Reporte HTML generado
- [ ] Coverage objetivo establecido
- [ ] Plan de mejora definido

### Automatización

- [ ] Scripts de quality check
- [ ] Pre-commit hooks (opcional)
- [ ] CI/CD configurado (opcional)
- [ ] Documentación actualizada

---

## 📊 Métricas de Éxito

| Métrica             | Objetivo Mínimo | Objetivo Ideal |
| ------------------- | --------------- | -------------- |
| Coverage de código  | 70%             | 85%            |
| Tests implementados | 15              | 25+            |
| Quality checks      | Passing         | All passing    |
| Tiempo de ejecución | < 30s           | < 15s          |

---

## 📚 Recursos de Apoyo

### Documentación

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [Coverage.py](https://coverage.readthedocs.io/)

### Tutoriales

- [Testing FastAPI Applications](https://fastapi.tiangolo.com/tutorial/testing/)
- [Python Testing 101](https://realpython.com/python-testing/)

### Herramientas

- **pytest**: Framework de testing
- **httpx**: Cliente HTTP para testing
- **black**: Formateo de código
- **coverage**: Análisis de cobertura

---

## 🎯 Entrega Final

### Requisitos Mínimos

1. **Suite de tests** funcionando con 15+ tests
2. **Quality checks** configurados y pasando
3. **Coverage report** generado con 70%+ coverage
4. **Documentación** básica de testing

### Estructura de Entrega

```
proyecto/
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/
│   └── quality_check.sh
├── pytest.ini
├── pyproject.toml
└── README_TESTING.md
```

### Criterios de Evaluación

- **Funcionalidad** (40%): Tests funcionan correctamente
- **Cobertura** (25%): Coverage objetivo alcanzado
- **Calidad** (20%): Quality checks pasando
- **Organización** (15%): Estructura clara y documentada

---

_Estos ejercicios consolidan los conocimientos de testing y quality assurance, preparando a los estudiantes para mantener código de alta calidad en proyectos reales._
