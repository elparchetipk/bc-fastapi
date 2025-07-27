# Testing y Calidad en APIs

## 🎯 Objetivos de Aprendizaje

Al finalizar este módulo teórico, comprenderás:

- **¿Qué es el testing automatizado?** y por qué es crucial en APIs
- **Tipos de testing** relevantes para aplicaciones FastAPI
- **pytest framework** y sus características principales
- **Testing de APIs REST** con FastAPI TestClient
- **Cobertura de código** y métricas de calidad

---

## 🧪 ¿Qué es el Testing Automatizado?

### **Definición**

El **testing automatizado** es el proceso de ejecutar pruebas de software de forma automática para verificar que el código funciona como se espera.

### **¿Por qué es importante?**

- ✅ **Detecta errores temprano** - Antes de llegar a producción
- ✅ **Facilita refactoring** - Cambios seguros en el código
- ✅ **Documentación viva** - Los tests explican cómo funciona el código
- ✅ **Confianza en despliegues** - Reduces bugs en producción
- ✅ **Calidad profesional** - Estándar en desarrollo moderno

### **Sin testing vs Con testing**

| Aspecto               | Sin Testing           | Con Testing            |
| --------------------- | --------------------- | ---------------------- |
| **Detección de bugs** | Manual, tardía        | Automática, temprana   |
| **Confianza**         | Baja al hacer cambios | Alta para refactorizar |
| **Tiempo debugging**  | Mucho tiempo perdido  | Problemas localizados  |
| **Mantenimiento**     | Difícil y arriesgado  | Seguro y predecible    |

---

## 🏗️ Tipos de Testing para APIs

### **1. Testing Unitario**

- **¿Qué prueba?** Funciones individuales aisladas
- **Ejemplo**: Una función que valida email
- **Herramienta**: pytest

```python
def test_validate_email():
    assert validate_email("test@example.com") == True
    assert validate_email("invalid-email") == False
```

### **2. Testing de Integración**

- **¿Qué prueba?** Interacción entre componentes
- **Ejemplo**: API + Base de datos
- **Herramienta**: pytest + TestClient

```python
def test_create_user_integration():
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    assert user_in_database(user_data["email"])
```

### **3. Testing de Endpoints (API Testing)**

- **¿Qué prueba?** Endpoints HTTP completos
- **Ejemplo**: POST /users/, GET /users/1
- **Herramienta**: FastAPI TestClient

```python
def test_get_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1
```

### **4. Testing Funcional**

- **¿Qué prueba?** Flujos completos de usuario
- **Ejemplo**: Registro → Login → Acceso a recurso protegido
- **Herramienta**: pytest con múltiples requests

---

## 🐍 pytest Framework

### **¿Por qué pytest?**

- ✅ **Sintaxis simple** - Fácil de leer y escribir
- ✅ **Fixtures poderosas** - Setup y teardown automático
- ✅ **Descubrimiento automático** - Encuentra tests automáticamente
- ✅ **Reporting robusto** - Reportes detallados de fallos
- ✅ **Extensible** - Plugins para FastAPI, coverage, etc.

### **Estructura básica de un test**

```python
def test_something():
    # Arrange - Preparar datos
    data = {"name": "Test"}

    # Act - Ejecutar la acción
    result = process_data(data)

    # Assert - Verificar resultado
    assert result["name"] == "Test"
    assert result["processed"] == True
```

### **Convenciones de pytest**

- **Archivos**: `test_*.py` o `*_test.py`
- **Funciones**: `test_*`
- **Clases**: `Test*`
- **Ubicación**: Carpeta `tests/` en el proyecto

---

## 🚀 Testing de APIs con FastAPI

### **TestClient: Tu mejor amigo**

FastAPI incluye `TestClient` basado en httpx para testing:

```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
```

### **Ventajas del TestClient**

- ✅ **Sin servidor real** - Tests rápidos y aislados
- ✅ **Misma API que httpx** - Familiar y potente
- ✅ **Soporte async** - Compatible con código asíncrono
- ✅ **Integración perfecta** - Diseñado para FastAPI

### **Patrones comunes de testing de APIs**

#### **1. Testing de GET endpoints**

```python
def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
```

#### **2. Testing de POST endpoints**

```python
def test_create_user():
    user_data = {"email": "test@example.com", "name": "Test"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
```

#### **3. Testing de errores**

```python
def test_get_nonexistent_user():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]
```

---

## 🔐 Testing con Autenticación

### **El desafío**

Muchos endpoints requieren autenticación. ¿Cómo testear sin complicar?

### **Estrategias**

#### **1. Fixture para token válido**

```python
@pytest.fixture
def auth_headers():
    # Crear usuario de prueba y obtener token
    token = create_test_token()
    return {"Authorization": f"Bearer {token}"}

def test_protected_endpoint(auth_headers):
    response = client.get("/protected", headers=auth_headers)
    assert response.status_code == 200
```

#### **2. Mock del sistema de auth**

```python
def test_with_mock_user(monkeypatch):
    def mock_get_current_user():
        return {"id": 1, "email": "test@example.com"}

    monkeypatch.setattr("auth.get_current_user", mock_get_current_user)
    response = client.get("/profile")
    assert response.status_code == 200
```

---

## 📊 Cobertura de Código

### **¿Qué es la cobertura?**

La **cobertura de código** mide qué porcentaje de tu código es ejecutado durante los tests.

### **¿Por qué importa?**

- ✅ **Identifica código sin testear** - Posibles bugs ocultos
- ✅ **Guía para escribir más tests** - ¿Qué falta?
- ✅ **Métrica de calidad** - Aunque no es la única importante

### **Interpretando la cobertura**

| Cobertura  | Interpretación        | Acción                    |
| ---------- | --------------------- | ------------------------- |
| **< 50%**  | Muy baja              | Escribir muchos más tests |
| **50-70%** | Aceptable para inicio | Mejorar gradualmente      |
| **70-85%** | Buena                 | Enfocarse en lo crítico   |
| **> 85%**  | Excelente             | Mantener y refinar        |

### **Usando coverage con pytest**

```bash
# Instalar coverage
pip install coverage

# Ejecutar tests con cobertura
coverage run -m pytest

# Ver reporte en terminal
coverage report

# Generar reporte HTML
coverage html
```

---

## 🏗️ Fixtures: La Base del Testing

### **¿Qué son las fixtures?**

Las **fixtures** son funciones que preparan datos o estado para tus tests.

### **Ventajas**

- ✅ **Reutilización** - Mismo setup para múltiples tests
- ✅ **Limpieza automática** - Setup y teardown
- ✅ **Inyección de dependencias** - pytest las inyecta automáticamente

### **Ejemplo básico**

```python
@pytest.fixture
def sample_user():
    return {"email": "test@example.com", "name": "Test User"}

def test_user_creation(sample_user):
    response = client.post("/users/", json=sample_user)
    assert response.status_code == 201
```

### **Fixture de base de datos**

```python
@pytest.fixture
def db_session():
    # Setup: crear sesión de BD de prueba
    session = create_test_db_session()
    yield session
    # Teardown: limpiar después del test
    session.rollback()
    session.close()
```

---

## 🎯 Buenas Prácticas de Testing

### **1. Tests independientes**

- ❌ **Malo**: Tests que dependen del orden de ejecución
- ✅ **Bueno**: Cada test puede ejecutarse solo

### **2. Nombres descriptivos**

```python
# ❌ Malo
def test_user():
    pass

# ✅ Bueno
def test_create_user_returns_201_with_valid_data():
    pass
```

### **3. Un concepto por test**

```python
# ❌ Malo: test muy largo que prueba muchas cosas
def test_user_everything():
    # crear usuario
    # actualizar usuario
    # eliminar usuario
    pass

# ✅ Bueno: tests separados
def test_create_user():
    pass

def test_update_user():
    pass

def test_delete_user():
    pass
```

### **4. Arrange, Act, Assert**

```python
def test_create_user():
    # Arrange - Preparar
    user_data = {"email": "test@example.com"}

    # Act - Ejecutar
    response = client.post("/users/", json=user_data)

    # Assert - Verificar
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]
```

---

## ⚡ Tests Rápidos vs Tests Lentos

### **Tests rápidos (preferibles)**

- ✅ **Sin I/O**: No tocan disco, red, BD real
- ✅ **En memoria**: Todo en RAM
- ✅ **Aislados**: No dependen de estado externo
- ⏱️ **< 1 segundo** por test

### **Tests lentos (usar con moderación)**

- ⚠️ **Con I/O**: BD real, APIs externas
- ⚠️ **Integración completa**: Todo el sistema
- ⚠️ **Setup complejo**: Datos reales
- ⏱️ **> 1 segundo** por test

### **Estrategia balanceada**

- **80% tests rápidos** - Feedback inmediato
- **20% tests lentos** - Confianza en integración

---

## 🔧 Herramientas del Ecosistema

### **Core Testing**

- **pytest** - Framework principal
- **httpx** - Cliente HTTP para tests
- **coverage** - Medición de cobertura

### **Específicas de FastAPI**

- **TestClient** - Cliente de testing de FastAPI
- **pytest-asyncio** - Soporte async/await

### **Utilidades Adicionales**

- **factoryboy** - Generación de datos de prueba
- **freezegun** - Mock de fechas/tiempo
- **responses** - Mock de requests HTTP

---

## 📋 Checklist de Testing

### **Setup inicial**

- [ ] pytest instalado y configurado
- [ ] Estructura de carpeta `tests/`
- [ ] `conftest.py` con fixtures básicas
- [ ] TestClient configurado

### **Tests básicos**

- [ ] Test de endpoint raíz (`/`)
- [ ] Tests de endpoints CRUD principales
- [ ] Tests de validación de datos
- [ ] Tests de casos de error (404, 422)

### **Tests avanzados**

- [ ] Tests de autenticación (login/registro)
- [ ] Tests de endpoints protegidos
- [ ] Tests de roles y permisos
- [ ] Tests de integración con BD

### **Calidad**

- [ ] Cobertura > 70%
- [ ] Tests con nombres descriptivos
- [ ] Fixtures reutilizables
- [ ] Tests rápidos (< 1s cada uno)

---

## 🚀 ¿Qué Sigue?

Después de dominar estos conceptos, estarás listo para:

1. **Implementar pytest** en tu proyecto FastAPI
2. **Crear tests para todos tus endpoints**
3. **Medir y mejorar la cobertura**
4. **Establecer buenas prácticas** en tu equipo

El testing no es opcional en desarrollo profesional. ¡Es tu red de seguridad para crear software confiable!

---

## 🎉 ¡Prepárate para transformar tu desarrollo con testing automatizado! 🧪🚀
