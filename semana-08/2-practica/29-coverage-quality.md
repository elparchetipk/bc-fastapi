# Práctica 29: Cobertura de Código y Calidad

## 🎯 Objetivo

Implementar medición de cobertura de código, establecer métricas de calidad y crear documentación automática de tests en 90 minutos.

## ⏱️ Tiempo: 90 minutos

### 📋 Distribución del tiempo

- **Configuración de cobertura** (20 min)
- **Análisis y mejora de cobertura** (30 min)
- **Herramientas de calidad** (25 min)
- **Documentación de tests** (15 min)

## 📋 Pre-requisitos

- ✅ Práctica 28 completada (testing avanzado)
- ✅ Suite de tests funcionando
- ✅ Conocimientos de pytest y FastAPI
- ✅ API con múltiples endpoints

## 🚀 Desarrollo Paso a Paso

### Paso 1: Configuración de Cobertura (20 min)

#### 1.1 Instalar herramientas de cobertura

```bash
pip install coverage pytest-cov
```

#### 1.2 Configurar coverage en pyproject.toml

```toml
# pyproject.toml (crear si no existe)
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "--cov=.",
    "--cov-report=html",
    "--cov-report=term-missing",
    "--cov-fail-under=80"
]

[tool.coverage.run]
source = ["."]
omit = [
    "tests/*",
    "venv/*",
    "*.venv/*",
    "__pycache__/*",
    "*.pyc"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:"
]
```

#### 1.3 Ejecutar tests con cobertura

```bash
# Ejecutar con cobertura
pytest --cov

# Generar reporte HTML
pytest --cov --cov-report=html

# Ver reporte detallado
coverage report --show-missing
```

#### 1.4 Interpretar resultados de cobertura

```text
Name        Stmts   Miss  Cover   Missing
-----------------------------------------
main.py        45      5    89%   23-24, 45-47
auth.py        32      3    91%   67-69
models.py      28      0   100%
-----------------------------------------
TOTAL         105      8    92%
```

**Qué significan las métricas:**

- **Stmts**: Líneas de código total
- **Miss**: Líneas no cubiertas por tests
- **Cover**: Porcentaje de cobertura
- **Missing**: Números de línea específicos sin cobertura

---

### Paso 2: Análisis y Mejora de Cobertura (30 min)

#### 2.1 Identificar código sin cobertura

```bash
# Abrir reporte HTML
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
```

#### 2.2 Crear tests para mejorar cobertura

```python
# tests/test_coverage_improvement.py
import pytest

class TestErrorHandling:
    """Tests para mejorar cobertura de manejo de errores"""

    def test_database_connection_error(self, client, mocker):
        """Test error de conexión a BD"""
        # Mock para simular error de BD
        mocker.patch('sqlalchemy.orm.session.Session.query',
                    side_effect=Exception("Database connection failed"))

        response = client.get("/users")
        assert response.status_code == 500
        assert "database error" in response.json()["detail"].lower()

    def test_validation_error_details(self, client):
        """Test detalles específicos de errores de validación"""
        invalid_data = {
            "name": "",  # Nombre vacío
            "email": "invalid",  # Email sin @
            "age": -1  # Edad negativa
        }

        response = client.post("/users", json=invalid_data)
        assert response.status_code == 422

        errors = response.json()["detail"]
        assert len(errors) >= 3  # Debería haber 3 errores

class TestEdgeCases:
    """Tests para casos límite"""

    def test_extremely_long_name(self, client):
        """Test con nombre extremadamente largo"""
        long_name = "a" * 1000
        user_data = {
            "name": long_name,
            "email": "test@example.com",
            "age": 25
        }

        response = client.post("/users", json=user_data)
        # Dependiendo de tu validación, podría ser 422 o 201
        assert response.status_code in [201, 422]

    def test_special_characters_in_name(self, client):
        """Test con caracteres especiales"""
        user_data = {
            "name": "José María Ñoño",
            "email": "jose@example.com",
            "age": 30
        }

        response = client.post("/users", json=user_data)
        assert response.status_code == 201
        assert response.json()["name"] == user_data["name"]

    def test_boundary_age_values(self, client):
        """Test valores límite de edad"""
        # Edad mínima
        response = client.post("/users", json={
            "name": "Young User",
            "email": "young@example.com",
            "age": 0
        })
        # Dependiendo de tu validación
        assert response.status_code in [201, 422]

        # Edad máxima
        response = client.post("/users", json={
            "name": "Old User",
            "email": "old@example.com",
            "age": 150
        })
        assert response.status_code in [201, 422]
```

#### 2.3 Tests para funciones de utilidad

```python
# tests/test_utils.py
import pytest
from utils import format_email, calculate_age  # Ajustar según tu código

class TestUtilityFunctions:
    """Tests para funciones de utilidad"""

    def test_format_email_lowercase(self):
        """Test formateo de email a minúsculas"""
        result = format_email("TEST@EXAMPLE.COM")
        assert result == "test@example.com"

    def test_format_email_strip_spaces(self):
        """Test eliminación de espacios en email"""
        result = format_email("  test@example.com  ")
        assert result == "test@example.com"

    def test_calculate_age_current_year(self):
        """Test cálculo de edad"""
        from datetime import datetime
        current_year = datetime.now().year
        birth_year = current_year - 25

        age = calculate_age(birth_year)
        assert age == 25

    def test_calculate_age_edge_case(self):
        """Test caso límite de cálculo de edad"""
        age = calculate_age(2025)  # Año futuro
        assert age >= 0  # No debería ser negativo
```

---

### Paso 3: Herramientas de Calidad (25 min)

#### 3.1 Configurar herramientas adicionales

```bash
pip install flake8 black isort mypy
```

#### 3.2 Configurar calidad de código

```toml
# pyproject.toml (agregar)
[tool.black]
line-length = 88
target-version = ['py39']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

#### 3.3 Script de verificación de calidad

```bash
# scripts/quality_check.sh (crear archivo)
#!/bin/bash

echo "🔍 Ejecutando verificaciones de calidad..."

echo "1. Formateando código con Black..."
black . --check --diff

echo "2. Ordenando imports con isort..."
isort . --check-only --diff

echo "3. Verificando estilo con flake8..."
flake8 .

echo "4. Verificando tipos con mypy..."
mypy .

echo "5. Ejecutando tests con cobertura..."
pytest --cov --cov-fail-under=80

echo "✅ Verificaciones completadas!"
```

#### 3.4 Pre-commit hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [--cov, --cov-fail-under=80]
```

#### 3.5 Configurar flake8

```ini
# .flake8
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    venv,
    .venv,
    *.egg-info
```

---

### Paso 4: Documentación de Tests (15 min)

#### 4.1 Generar documentación con pytest-html

```bash
pip install pytest-html
```

#### 4.2 Ejecutar tests con reporte HTML

```bash
pytest --html=reports/report.html --self-contained-html
```

#### 4.3 Crear documentación de tests

```python
# tests/test_documentation.py
"""
Módulo de documentación de tests.

Este módulo contiene tests que sirven como documentación viva
de la funcionalidad de la API.
"""

class TestAPIDocumentation:
    """
    Tests que documentan el comportamiento esperado de la API.

    Estos tests sirven como documentación ejecutable y ejemplos
    de uso para otros desarrolladores.
    """

    def test_user_creation_workflow(self, client):
        """
        Documenta el flujo completo de creación de usuario.

        Pasos:
        1. Enviar datos de usuario válidos
        2. Verificar respuesta exitosa (201)
        3. Confirmar que se devuelve ID único
        4. Validar que los datos se almacenan correctamente

        Ejemplo de uso:
        POST /users
        {
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "age": 30
        }
        """
        user_data = {
            "name": "Juan Pérez",
            "email": "juan@example.com",
            "age": 30
        }

        response = client.post("/users", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["name"] == user_data["name"]
        assert data["email"] == user_data["email"]
        assert data["age"] == user_data["age"]

    def test_authentication_flow(self, client):
        """
        Documenta el flujo de autenticación JWT.

        Demuestra:
        - Cómo registrar un usuario
        - Cómo hacer login
        - Cómo usar el token para acceder a endpoints protegidos
        """
        # Registro
        user_data = {
            "email": "auth@example.com",
            "password": "securepass123"
        }
        client.post("/register", json=user_data)

        # Login
        login_response = client.post("/login", data={
            "username": user_data["email"],
            "password": user_data["password"]
        })

        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # Uso del token
        headers = {"Authorization": f"Bearer {token}"}
        protected_response = client.get("/users/me", headers=headers)
        assert protected_response.status_code == 200
```

#### 4.4 Crear README de tests

````markdown
# Tests Documentation

## Estructura de Tests

```text
tests/
├── conftest.py          # Fixtures compartidas
├── test_main.py         # Tests básicos de la API
├── test_auth.py         # Tests de autenticación
├── test_database.py     # Tests de base de datos
├── test_integration.py  # Tests de integración
└── test_documentation.py # Tests como documentación
```
````

## Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov

# Solo tests específicos
pytest tests/test_auth.py -v

# Generar reporte HTML
pytest --html=reports/report.html
```

## Métricas de Calidad

- **Cobertura mínima**: 80%
- **Tests por funcionalidad**: Mínimo 3 casos
- **Documentación**: Todos los tests documentados

```

## ✅ Entregables

Al finalizar esta práctica debes tener:

1. ✅ **Cobertura de código** configurada y medida
2. ✅ **Cobertura mínima del 80%** alcanzada
3. ✅ **Herramientas de calidad** configuradas
4. ✅ **Scripts de verificación** automatizados
5. ✅ **Documentación de tests** completa

## 📚 Recursos de Apoyo

- [Coverage.py Documentation](https://coverage.readthedocs.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Black Code Formatter](https://black.readthedocs.io/)

## 🔗 Próxima Práctica

En la siguiente práctica trabajaremos con **documentación avanzada** y **automatización de APIs**.

---

💡 **Tip**: La cobertura del 100% no siempre es necesaria. Enfócate en la calidad sobre la cantidad.
```
