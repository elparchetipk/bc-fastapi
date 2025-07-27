# Práctica 22: Coverage y Calidad de Código

⏰ **Tiempo:** 90 minutos  
📚 **Prerequisito:** Prácticas 19-21 completadas  
🎯 **Objetivo:** Implementar análisis de cobertura y mejorar la calidad del código

## 📋 Contenido de la Práctica

### **Parte 1: Coverage Setup y Medición (30 min)**

1. **Instalación de pytest-cov**
2. **Configuración de Coverage**
3. **Reportes de Cobertura**

### **Parte 2: Mejora de Coverage (45 min)**

1. **Identificar Gaps de Coverage**
2. **Tests para Edge Cases**
3. **Tests de Integración**

### **Parte 3: Calidad y Documentación (15 min)**

1. **Organización Final**
2. **Documentación de Tests**
3. **Scripts de Automatización**

---

## 🎯 Parte 1: Coverage Setup y Medición (30 min)

### 1.1 Instalación de pytest-cov

**Paso 1: Actualizar requirements**

**Archivo: `requirements-dev.txt`** (crear/actualizar)

```txt
# Testing dependencies
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
httpx==0.25.2

# Linting y formateo
black==23.11.0
flake8==6.1.0
mypy==1.7.1

# Documentación
mkdocs==1.5.3
mkdocs-material==9.4.8
```

**Paso 2: Instalar dependencias**

```bash
pip install -r requirements-dev.txt
```

### 1.2 Configuración de Coverage

**Archivo: `.coveragerc`** (crear en raíz del proyecto)

```ini
[run]
source = app
omit =
    app/__init__.py
    app/main.py
    */tests/*
    */venv/*
    */env/*
    */__pycache__/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if __name__ == .__main__.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod

show_missing = True
precision = 2
skip_covered = False

[html]
directory = htmlcov
title = FastAPI Testing Coverage Report

[xml]
output = coverage.xml
```

**Archivo: `pytest.ini`** (crear en raíz del proyecto)

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --cov=app
    --cov-report=html
    --cov-report=xml
    --cov-report=term-missing
    --cov-fail-under=85
    -v
    --tb=short
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

### 1.3 Reportes de Cobertura

**Comando básico para coverage:**

```bash
# Ejecutar tests con coverage
pytest --cov=app --cov-report=html --cov-report=term

# Solo mostrar líneas faltantes
pytest --cov=app --cov-report=term-missing

# Generar reporte HTML detallado
pytest --cov=app --cov-report=html
open htmlcov/index.html  # macOS
# xdg-open htmlcov/index.html  # Linux
```

**Script de coverage avanzado**

**Archivo: `scripts/test_coverage.py`** (crear)

```python
#!/usr/bin/env python3
"""Script para ejecutar tests con análisis de coverage detallado."""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Ejecuta un comando y maneja errores."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return None

def main():
    """Función principal."""
    print("🧪 Iniciando análisis completo de coverage...")

    # Limpiar coverage anterior
    run_command("coverage erase", "Limpiando coverage anterior")

    # Ejecutar tests con coverage
    output = run_command(
        "pytest --cov=app --cov-report=html --cov-report=xml --cov-report=term-missing",
        "Ejecutando tests con coverage"
    )

    if output is None:
        print("❌ Error ejecutando tests")
        sys.exit(1)

    # Mostrar resumen
    print("\n📊 RESUMEN DE COVERAGE:")
    lines = output.split('\n')
    for line in lines:
        if 'TOTAL' in line or '%' in line:
            print(f"  {line}")

    # Generar reporte detallado
    run_command("coverage report --show-missing", "Generando reporte detallado")

    # Verificar si se cumple el mínimo
    result = subprocess.run("coverage report --fail-under=85", shell=True)
    if result.returncode == 0:
        print("\n✅ Coverage mínimo (85%) alcanzado!")
    else:
        print("\n⚠️  Coverage por debajo del mínimo (85%)")

    print(f"\n📁 Reporte HTML generado en: {Path('htmlcov/index.html').absolute()}")

if __name__ == "__main__":
    main()
```

---

## 🎯 Parte 2: Mejora de Coverage (45 min)

### 2.1 Identificar Gaps de Coverage

**Análisis de coverage por módulo:**

```bash
# Ver coverage por archivo
coverage report --show-missing

# Ver solo archivos con coverage bajo
coverage report --show-missing --skip-covered
```

**Archivo: `tests/test_coverage_gaps.py`** (crear)

```python
"""Tests específicos para cubrir gaps de coverage."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import IntegrityError

class TestErrorHandling:
    """Tests para manejo de errores y casos edge."""

    def test_database_connection_error(self, client):
        """Test manejo de error de conexión a DB."""
        # Este test simula un error de DB
        with pytest.raises(Exception):
            # Aquí simularías un error de DB real
            pass

    def test_invalid_json_request(self, client):
        """Test request con JSON inválido."""
        response = client.post(
            "/tasks/",
            data="invalid json",  # No es JSON válido
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422

    def test_missing_required_fields(self, client, auth_headers):
        """Test crear task sin campos requeridos."""
        incomplete_data = {"description": "Missing title"}
        response = client.post("/tasks/", json=incomplete_data, headers=auth_headers)
        assert response.status_code == 422

        errors = response.json()["detail"]
        assert any("title" in str(error) for error in errors)

    def test_field_validation_limits(self, client, auth_headers):
        """Test validaciones de límites de campos."""
        # Título muy largo
        long_title = "x" * 1000
        task_data = {"title": long_title, "description": "Test"}
        response = client.post("/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == 422

        # Descripción vacía
        empty_desc_data = {"title": "Test", "description": ""}
        response = client.post("/tasks/", json=empty_desc_data, headers=auth_headers)
        # Dependiendo de tu validación, puede ser 422 o aceptado
        assert response.status_code in [201, 422]

class TestModelValidations:
    """Tests para validaciones a nivel de modelo."""

    def test_user_email_uniqueness(self, db):
        """Test que email de usuario es único."""
        from app.models.user import User
        from app.auth.password import get_password_hash

        user1_data = {
            "email": "duplicate@example.com",
            "full_name": "User 1",
            "hashed_password": get_password_hash("password123")
        }
        user2_data = {
            "email": "duplicate@example.com",  # Mismo email
            "full_name": "User 2",
            "hashed_password": get_password_hash("password456")
        }

        # Crear primer usuario
        user1 = User(**user1_data)
        db.add(user1)
        db.commit()

        # Intentar crear segundo usuario con mismo email
        user2 = User(**user2_data)
        db.add(user2)

        with pytest.raises(IntegrityError):
            db.commit()

    def test_task_user_relationship(self, db, test_user):
        """Test relación entre task y usuario."""
        from app.models.task import Task

        task_data = {
            "title": "Test Task",
            "description": "Test Description",
            "user_id": test_user.id
        }

        task = Task(**task_data)
        db.add(task)
        db.commit()
        db.refresh(task)

        # Verificar relación
        assert task.user_id == test_user.id
        assert task.user.email == test_user.email

class TestUtilityFunctions:
    """Tests para funciones utilitarias."""

    def test_password_hashing(self):
        """Test funciones de hashing de passwords."""
        from app.auth.password import get_password_hash, verify_password

        password = "test_password_123"
        hashed = get_password_hash(password)

        # Verificar que el hash es diferente al password original
        assert hashed != password
        assert len(hashed) > 20  # Hash debe ser largo

        # Verificar que la verificación funciona
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False

    def test_jwt_token_creation(self):
        """Test creación y verificación de JWT tokens."""
        from app.auth.jwt_handler import create_access_token, verify_token
        from datetime import timedelta

        data = {"sub": "test@example.com"}
        token = create_access_token(data, expires_delta=timedelta(hours=1))

        # Verificar que se creó un token
        assert isinstance(token, str)
        assert len(token) > 20

        # Verificar que se puede decodificar
        decoded = verify_token(token)
        assert decoded["sub"] == "test@example.com"

    def test_jwt_token_expiration(self):
        """Test expiración de JWT tokens."""
        from app.auth.jwt_handler import create_access_token, verify_token
        from datetime import timedelta

        # Crear token que expira inmediatamente
        data = {"sub": "test@example.com"}
        token = create_access_token(data, expires_delta=timedelta(seconds=-1))

        # Verificar que el token expirado no es válido
        decoded = verify_token(token)
        assert decoded is None  # o lanza excepción, según implementación
```

### 2.2 Tests para Edge Cases

**Archivo: `tests/test_edge_cases.py`** (crear)

```python
"""Tests para casos edge y límites del sistema."""
import pytest
from fastapi.testclient import TestClient

class TestAPILimits:
    """Tests para límites de la API."""

    def test_pagination_edge_cases(self, client, auth_headers):
        """Test casos edge de paginación."""
        # Crear varias tasks para testing
        for i in range(25):
            task_data = {"title": f"Task {i}", "description": f"Description {i}"}
            client.post("/tasks/", json=task_data, headers=auth_headers)

        # Test página que no existe
        response = client.get("/tasks?page=999&size=10", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 0

        # Test tamaño de página muy grande
        response = client.get("/tasks?page=1&size=1000", headers=auth_headers)
        assert response.status_code == 200
        # Debe estar limitado a un máximo razonable

        # Test tamaño de página negativo
        response = client.get("/tasks?page=1&size=-1", headers=auth_headers)
        assert response.status_code == 422

    def test_search_edge_cases(self, client, auth_headers):
        """Test casos edge de búsqueda."""
        # Crear task para búsqueda
        task_data = {"title": "Searchable Task", "description": "Find me"}
        client.post("/tasks/", json=task_data, headers=auth_headers)

        # Búsqueda con caracteres especiales
        response = client.get("/tasks/search?q=%@#$", headers=auth_headers)
        assert response.status_code == 200

        # Búsqueda muy larga
        long_query = "x" * 1000
        response = client.get(f"/tasks/search?q={long_query}", headers=auth_headers)
        assert response.status_code in [200, 422]

        # Búsqueda vacía
        response = client.get("/tasks/search?q=", headers=auth_headers)
        assert response.status_code == 200

class TestConcurrency:
    """Tests para escenarios de concurrencia."""

    def test_concurrent_user_creation(self, client):
        """Test creación concurrente de usuarios."""
        import threading
        import time

        results = []

        def create_user(user_id):
            user_data = {
                "email": f"concurrent{user_id}@example.com",
                "password": "password123",
                "full_name": f"Concurrent User {user_id}"
            }
            response = client.post("/auth/register", json=user_data)
            results.append(response.status_code)

        # Crear múltiples usuarios concurrentemente
        threads = []
        for i in range(5):
            thread = threading.Thread(target=create_user, args=(i,))
            threads.append(thread)
            thread.start()

        # Esperar a que terminen todos
        for thread in threads:
            thread.join()

        # Todos deben haberse creado exitosamente
        assert all(status == 201 for status in results)

class TestPerformance:
    """Tests básicos de performance."""

    @pytest.mark.slow
    def test_bulk_operations_performance(self, client, auth_headers):
        """Test performance con operaciones en lote."""
        import time

        start_time = time.time()

        # Crear 100 tasks
        for i in range(100):
            task_data = {
                "title": f"Bulk Task {i}",
                "description": f"Bulk Description {i}",
                "priority": "low"
            }
            response = client.post("/tasks/", json=task_data, headers=auth_headers)
            assert response.status_code == 201

        creation_time = time.time() - start_time

        # Obtener todas las tasks
        start_time = time.time()
        response = client.get("/tasks/me", headers=auth_headers)
        retrieval_time = time.time() - start_time

        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) >= 100

        # Verificar que las operaciones no toman demasiado tiempo
        assert creation_time < 30.0  # Máximo 30 segundos para crear 100 tasks
        assert retrieval_time < 5.0   # Máximo 5 segundos para obtener tasks

        print(f"⏱️  Tiempo creación: {creation_time:.2f}s")
        print(f"⏱️  Tiempo consulta: {retrieval_time:.2f}s")
```

### 2.3 Tests de Integración

**Archivo: `tests/test_integration.py`** (crear)

```python
"""Tests de integración end-to-end."""
import pytest
from fastapi.testclient import TestClient

@pytest.mark.integration
class TestUserWorkflow:
    """Test del workflow completo de usuario."""

    def test_complete_user_journey(self, client):
        """Test journey completo: registro → login → crear task → actualizar → eliminar."""

        # 1. Registro
        user_data = {
            "email": "journey@example.com",
            "password": "journey123",
            "full_name": "Journey User"
        }
        register_response = client.post("/auth/register", json=user_data)
        assert register_response.status_code == 201
        user = register_response.json()

        # 2. Login
        login_data = {"username": user_data["email"], "password": user_data["password"]}
        login_response = client.post("/auth/login", data=login_data)
        assert login_response.status_code == 200
        token_data = login_response.json()
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}

        # 3. Crear task
        task_data = {
            "title": "Journey Task",
            "description": "Task for complete journey",
            "priority": "high"
        }
        create_response = client.post("/tasks/", json=task_data, headers=headers)
        assert create_response.status_code == 201
        task = create_response.json()

        # 4. Obtener task
        get_response = client.get(f"/tasks/{task['id']}", headers=headers)
        assert get_response.status_code == 200
        retrieved_task = get_response.json()
        assert retrieved_task["title"] == task_data["title"]

        # 5. Actualizar task
        update_data = {"title": "Updated Journey Task", "completed": True}
        update_response = client.put(f"/tasks/{task['id']}", json=update_data, headers=headers)
        assert update_response.status_code == 200
        updated_task = update_response.json()
        assert updated_task["title"] == update_data["title"]
        assert updated_task["completed"] is True

        # 6. Obtener todas las tasks del usuario
        list_response = client.get("/tasks/me", headers=headers)
        assert list_response.status_code == 200
        user_tasks = list_response.json()
        assert len(user_tasks) >= 1
        assert any(t["id"] == task["id"] for t in user_tasks)

        # 7. Eliminar task
        delete_response = client.delete(f"/tasks/{task['id']}", headers=headers)
        assert delete_response.status_code == 204

        # 8. Verificar que fue eliminada
        get_deleted_response = client.get(f"/tasks/{task['id']}", headers=headers)
        assert get_deleted_response.status_code == 404

@pytest.mark.integration
class TestMultiUserScenarios:
    """Tests con múltiples usuarios."""

    def test_multiple_users_isolation(self, client):
        """Test que múltiples usuarios no interfieren entre sí."""

        # Crear dos usuarios
        users_data = [
            {"email": "user1@example.com", "password": "pass1", "full_name": "User 1"},
            {"email": "user2@example.com", "password": "pass2", "full_name": "User 2"}
        ]

        headers_list = []

        for user_data in users_data:
            # Registro
            client.post("/auth/register", json=user_data)

            # Login
            login_data = {"username": user_data["email"], "password": user_data["password"]}
            login_response = client.post("/auth/login", data=login_data)
            token = login_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            headers_list.append(headers)

        # Cada usuario crea tasks
        for i, headers in enumerate(headers_list):
            for j in range(3):
                task_data = {
                    "title": f"User {i+1} Task {j+1}",
                    "description": f"Task by user {i+1}"
                }
                response = client.post("/tasks/", json=task_data, headers=headers)
                assert response.status_code == 201

        # Verificar que cada usuario ve solo sus tasks
        for i, headers in enumerate(headers_list):
            response = client.get("/tasks/me", headers=headers)
            user_tasks = response.json()
            assert len(user_tasks) == 3

            # Todas las tasks deben pertenecer al usuario correcto
            for task in user_tasks:
                assert f"User {i+1}" in task["title"]
```

---

## 🎯 Parte 3: Calidad y Documentación (15 min)

### 3.1 Script de Automatización

**Archivo: `scripts/run_tests.sh`** (crear)

```bash
#!/bin/bash

# Script completo para ejecutar todos los tests y análisis

echo "🧪 Iniciando suite completa de testing..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para mostrar resultados
show_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2 completado exitosamente${NC}"
    else
        echo -e "${RED}❌ $2 falló${NC}"
        exit 1
    fi
}

# 1. Linting
echo -e "${YELLOW}📋 Ejecutando linting...${NC}"
flake8 app tests
show_result $? "Linting"

# 2. Type checking
echo -e "${YELLOW}🔍 Ejecutando type checking...${NC}"
mypy app
show_result $? "Type checking"

# 3. Tests unitarios
echo -e "${YELLOW}🧪 Ejecutando tests unitarios...${NC}"
pytest tests/ -m "not slow and not integration" -v
show_result $? "Tests unitarios"

# 4. Tests de integración
echo -e "${YELLOW}🔗 Ejecutando tests de integración...${NC}"
pytest tests/ -m "integration" -v
show_result $? "Tests de integración"

# 5. Coverage completo
echo -e "${YELLOW}📊 Analizando coverage...${NC}"
pytest --cov=app --cov-report=html --cov-report=term-missing --cov-fail-under=85
show_result $? "Coverage analysis"

# 6. Tests de performance (opcional)
echo -e "${YELLOW}⚡ Ejecutando tests de performance...${NC}"
pytest tests/ -m "slow" -v --tb=short
show_result $? "Tests de performance"

echo -e "${GREEN}🎉 Todos los tests completados exitosamente!${NC}"
echo -e "${YELLOW}📁 Ver reporte de coverage en: htmlcov/index.html${NC}"
```

### 3.2 Documentación de Tests

**Archivo: `tests/README.md`** (crear)

```markdown
# Documentación de Testing

## 📁 Estructura de Tests
```

tests/
├── conftest.py # Configuración y fixtures globales
├── fixtures/ # Fixtures organizadas por módulo
│ └── auth_fixtures.py # Fixtures de autenticación
├── helpers/ # Funciones helper para tests
│ └── auth_helpers.py # Helpers de autenticación
├── test_auth.py # Tests de autenticación
├── test_tasks.py # Tests de endpoints de tasks
├── test_protected_endpoints.py # Tests de endpoints protegidos
├── test_user_isolation.py # Tests de aislamiento entre usuarios
├── test_coverage_gaps.py # Tests para gaps de coverage
├── test_edge_cases.py # Tests de casos edge
└── test_integration.py # Tests de integración E2E

````

## 🎯 Tipos de Tests

### Tests Unitarios
- **Ubicación**: `test_*.py` con mark `@pytest.mark.unit`
- **Propósito**: Verificar funcionalidad individual
- **Ejecución**: `pytest -m unit`

### Tests de Integración
- **Ubicación**: `test_integration.py` con mark `@pytest.mark.integration`
- **Propósito**: Verificar workflows completos
- **Ejecución**: `pytest -m integration`

### Tests de Performance
- **Ubicación**: Tests con mark `@pytest.mark.slow`
- **Propósito**: Verificar performance básica
- **Ejecución**: `pytest -m slow`

## 🔧 Comandos Útiles

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con coverage
pytest --cov=app

# Ejecutar solo tests rápidos
pytest -m "not slow"

# Ejecutar tests específicos
pytest tests/test_auth.py

# Modo verbose con detalles
pytest -v --tb=short

# Detener en primer fallo
pytest -x

# Ejecutar tests en paralelo (con pytest-xdist)
pytest -n auto
````

## 📊 Coverage Goals

- **Mínimo aceptable**: 85%
- **Objetivo**: 90%+
- **Crítico**: 95%+ para módulos de auth y core

## 🎭 Fixtures Principales

- `client`: Cliente de testing configurado
- `db`: Sesión de base de datos de testing
- `test_user`: Usuario de testing básico
- `auth_headers`: Headers de autenticación
- `admin_user`: Usuario administrador
- `user_factory`: Factory para crear usuarios

## 🚨 Troubleshooting

### Error: "Database locked"

```bash
# Eliminar base de datos de testing
rm test.db
```

### Error: "Token expired"

```python
# Aumentar tiempo de expiración en fixtures
expires_delta=timedelta(hours=1)
```

### Coverage bajo

```bash
# Ver líneas no cubiertas
pytest --cov=app --cov-report=term-missing
```

````

### 3.3 GitHub Actions CI

**Archivo: `.github/workflows/tests.yml`** (crear)

```yaml
name: Tests and Coverage

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Lint with flake8
      run: |
        flake8 app tests --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 app tests --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

    - name: Type check with mypy
      run: mypy app

    - name: Test with pytest
      run: |
        pytest --cov=app --cov-report=xml --cov-report=term-missing

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        flags: unittests
        name: codecov-umbrella
````

---

## ✅ Checklist Final de Coverage y Calidad

### **Coverage Setup**

- [ ] pytest-cov instalado y configurado
- [ ] .coveragerc configurado con exclusiones apropiadas
- [ ] pytest.ini configurado con opciones de coverage
- [ ] Scripts de automatización creados

### **Tests de Coverage**

- [ ] Coverage mínimo 85% alcanzado
- [ ] Tests para manejo de errores
- [ ] Tests para validaciones de modelos
- [ ] Tests para funciones utilitarias
- [ ] Tests para casos edge y límites

### **Organización y Calidad**

- [ ] Estructura de tests clara y documentada
- [ ] Fixtures organizadas y reutilizables
- [ ] Helpers para operaciones comunes
- [ ] Documentación de tests completa
- [ ] CI/CD configurado (opcional)

---

## 🚨 Troubleshooting Común

### **Coverage no detecta algunos archivos**

```ini
# En .coveragerc, verificar [run] source
[run]
source = app
```

### **Tests muy lentos**

```python
# Usar marcadores para separar tests
@pytest.mark.slow
def test_performance_heavy():
    pass

# Ejecutar solo tests rápidos
pytest -m "not slow"
```

### **Base de datos no se limpia entre tests**

```python
# En conftest.py, usar autouse=True
@pytest.fixture(autouse=True)
def cleanup_database(db):
    yield
    db.execute("DELETE FROM tasks")
    db.execute("DELETE FROM users")
    db.commit()
```

---

## 🎯 Puntos Clave

1. **Coverage no es todo** - calidad > cantidad
2. **Tests de edge cases** son fundamentales
3. **Automatización** facilita el mantenimiento
4. **Documentación** hace tests mantenibles
5. **CI/CD** asegura calidad continua

¡Has completado el **módulo de Testing y Calidad**! 🎉

**Próximos pasos**: Implementar estos tests en tu proyecto final y mantener el coverage alto durante el desarrollo.
