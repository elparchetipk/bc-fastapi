# Práctica 27: Pytest y Testing Básico - Enfoque Intensivo

⏰ **Tiempo:** 90 minutos  
📚 **Prerequisito:** Semanas 1-7 completadas con API funcionando  
🎯 **Objetivo:** Configurar pytest y crear suite de testing básico pero completo

## 📋 Contenido de la Práctica

### **Parte 1: Setup Rápido de Pytest (25 min)**

1. **Instalación y configuración**
2. **Estructura de testing**
3. **Configuración inicial**

### **Parte 2: Tests Unitarios Básicos (35 min)**

1. **Tests de modelos y funciones**
2. **Fixtures básicas**
3. **Assertions fundamentales**

### **Parte 3: Tests de Endpoints Básicos (30 min)**

1. **TestClient setup**
2. **Tests de endpoints sin autenticación**
3. **Verificación de estructura de respuesta**

## 🚀 Desarrollo Paso a Paso

### Paso 1: Instalación y Configuración (15 min)

#### 1.1 Instalar dependencias de testing

```bash
# En tu directorio del proyecto
pip install pytest httpx pytest-asyncio

# Verificar instalación
pytest --version
```

#### 1.2 Actualizar requirements.txt

```text
# Agregar al final del archivo
pytest==7.4.3
httpx==0.25.2
pytest-asyncio==0.21.1
```

#### 1.3 Crear estructura de testing

```bash
# Desde la raíz del proyecto
mkdir tests
touch tests/__init__.py
touch tests/conftest.py
touch tests/test_main.py
```

#### 1.4 Configurar conftest.py

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    """Cliente de pruebas para la aplicación FastAPI"""
    return TestClient(app)

@pytest.fixture
def sample_user():
    """Datos de usuario de ejemplo para tests"""
    return {
        "name": "Test User",
        "email": "test@example.com",
        "age": 25
    }
```

---

### Paso 2: Primeros Tests Básicos (25 min)

#### 2.1 Test básico de la aplicación

```python
# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from main import app

def test_app_exists():
    """Verifica que la app FastAPI existe"""
    assert app is not None

def test_app_title():
    """Verifica el título de la aplicación"""
    assert app.title == "Mi API FastAPI"  # Ajustar según tu app

class TestHealthCheck:
    """Tests para verificar que la API está funcionando"""

    def test_read_root(self, client):
        """Test del endpoint raíz"""
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

    def test_health_endpoint(self, client):
        """Test del endpoint de salud"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
```

#### 2.2 Ejecutar los primeros tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con más detalle
pytest -v

# Ejecutar un archivo específico
pytest tests/test_main.py -v
```

#### 2.3 Interpretar resultados

```text
✅ PASSED: Test exitoso
❌ FAILED: Test falló
⚠️  SKIPPED: Test omitido
```

---

### Paso 3: Testing de Endpoints (35 min)

#### 3.1 Tests para endpoints GET

```python
# tests/test_main.py (agregar al final)

class TestUsersEndpoints:
    """Tests para endpoints de usuarios"""

    def test_get_users_empty(self, client):
        """Test obtener usuarios cuando la lista está vacía"""
        response = client.get("/users")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_user_not_found(self, client):
        """Test obtener usuario que no existe"""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
```

#### 3.2 Tests para endpoints POST

```python
# Continuar en tests/test_main.py

def test_create_user_success(self, client, sample_user):
    """Test crear usuario exitosamente"""
    response = client.post("/users", json=sample_user)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == sample_user["name"]
    assert data["email"] == sample_user["email"]
    assert "id" in data

def test_create_user_invalid_data(self, client):
    """Test crear usuario con datos inválidos"""
    invalid_user = {"name": ""}  # Email faltante
    response = client.post("/users", json=invalid_user)
    assert response.status_code == 422  # Validation error
```

#### 3.3 Tests para validación de datos

```python
class TestValidation:
    """Tests para validación de datos"""

    def test_user_invalid_email(self, client):
        """Test con email inválido"""
        invalid_user = {
            "name": "Test User",
            "email": "invalid-email",  # Sin @
            "age": 25
        }
        response = client.post("/users", json=invalid_user)
        assert response.status_code == 422

    def test_user_negative_age(self, client):
        """Test con edad negativa"""
        invalid_user = {
            "name": "Test User",
            "email": "test@example.com",
            "age": -5  # Edad inválida
        }
        response = client.post("/users", json=invalid_user)
        assert response.status_code == 422
```

---

### Paso 4: Práctica y Troubleshooting (15 min)

#### 4.1 Comandos útiles de pytest

```bash
# Ejecutar con output detallado
pytest -v -s

# Ejecutar solo tests que fallan
pytest --lf

# Ejecutar solo un test específico
pytest tests/test_main.py::test_create_user_success -v

# Mostrar print statements
pytest -s
```

#### 4.2 Debugging de tests

```python
# Agregar prints para debugging
def test_debug_example(self, client, sample_user):
    """Ejemplo de debugging en tests"""
    print(f"Testing with user: {sample_user}")

    response = client.post("/users", json=sample_user)
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")

    assert response.status_code == 201
```

#### 4.3 Errores comunes y soluciones

| Error                  | Causa                | Solución                                      |
| ---------------------- | -------------------- | --------------------------------------------- |
| `ModuleNotFoundError`  | No encuentra main.py | Verificar que estás en el directorio correcto |
| `404 Not Found`        | Endpoint no existe   | Verificar ruta en tu FastAPI app              |
| `422 Validation Error` | Datos inválidos      | Revisar modelo Pydantic                       |

## 🎯 Ejercicios Rápidos (Opcional)

### Ejercicio 1: Test Personalizado (5 min)

Crea un test para un endpoint específico de tu API.

### Ejercicio 2: Validación Extra (5 min)

Agrega un test para validar un campo específico de tu modelo.

## ✅ Entregables

Al finalizar esta práctica debes tener:

1. ✅ **pytest configurado** y funcionando
2. ✅ **Estructura de tests** creada correctamente
3. ✅ **Mínimo 5 tests básicos** ejecutándose exitosamente
4. ✅ **Tests para GET y POST** implementados
5. ✅ **Tests de validación** funcionando

## 📚 Recursos de Apoyo

- [Documentación oficial de pytest](https://docs.pytest.org/)
- [FastAPI Testing Guide](https://fastapi.tiangolo.com/tutorial/testing/)
- [TestClient Documentation](https://fastapi.tiangolo.com/tutorial/testing/#using-testclient)

## 🔗 Próxima Práctica

En la siguiente práctica aprenderemos sobre **testing avanzado de APIs** y **mocking de dependencias**.

---

💡 **Tip**: Los tests son código también. Manténlos simples, legibles y bien organizados.
