# Ejercicios de Testing - Semana 6

⏰ **Tiempo estimado:** 90 minutos  
🎯 **Objetivo:** Aplicar testing avanzado en un proyecto personal  
📚 **Prerequisito:** Prácticas 19-22 completadas

## 📋 Instrucciones Generales

1. **Usa tu proyecto actual** de las semanas 1-5
2. **Implementa todos los tests** paso a paso
3. **Alcanza mínimo 85% coverage** en módulos principales
4. **Documenta tus tests** siguiendo buenas prácticas
5. **Sube tu código** con los tests implementados

---

## 🎯 Ejercicio 1: Setup Completo de Testing (20 min)

### **Objetivo**

Configurar ambiente completo de testing para tu proyecto.

### **Tareas**

1. **Instalar dependencias de testing**

   ```bash
   pip install pytest pytest-cov pytest-asyncio httpx
   ```

2. **Crear estructura de testing**

   ```
   tests/
   ├── conftest.py
   ├── test_auth.py
   ├── test_[tu_modulo].py
   └── test_integration.py
   ```

3. **Configurar pytest.ini**

   - Coverage mínimo 80%
   - Marcadores para tests lentos
   - Output verbose

4. **Configurar .coveragerc**
   - Excluir archivos no relevantes
   - Configurar reportes HTML

### **Criterios de Evaluación**

- [ ] Estructura de testing creada
- [ ] Configuración de pytest completa
- [ ] Dependencias instaladas correctamente
- [ ] Coverage configurado

---

## 🎯 Ejercicio 2: Tests de Autenticación (25 min)

### **Objetivo**

Implementar tests completos para tu sistema de autenticación.

### **Tareas**

1. **Tests de registro de usuario**

   - Registro exitoso
   - Email duplicado
   - Validaciones de campos
   - Password débil

2. **Tests de login**

   - Login exitoso
   - Credenciales incorrectas
   - Usuario inexistente
   - Formato de respuesta correcto

3. **Tests de JWT**

   - Generación de token
   - Verificación de token
   - Token expirado
   - Token inválido

4. **Fixtures para autenticación**
   - Usuario de testing
   - Headers de autorización
   - Factory de usuarios

### **Ejemplo esperado**

```python
def test_register_success(client):
    user_data = {
        "email": "test@example.com",
        "password": "securepass123",
        "full_name": "Test User"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]

def test_login_success(client, test_user):
    login_data = {
        "username": test_user.email,
        "password": "testpassword123"
    }
    response = client.post("/auth/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### **Criterios de Evaluación**

- [ ] Mínimo 8 tests de autenticación
- [ ] Casos exitosos y fallidos cubiertos
- [ ] Fixtures correctamente implementadas
- [ ] Parametrización usada apropiadamente

---

## 🎯 Ejercicio 3: Tests de Endpoints CRUD (30 min)

### **Objetivo**

Crear tests completos para tus endpoints principales (tasks, posts, etc.).

### **Tareas**

1. **Tests de CREATE**

   - Creación exitosa con autenticación
   - Creación sin autenticación (401)
   - Validaciones de campos requeridos
   - Límites de caracteres

2. **Tests de READ**

   - Obtener elemento por ID
   - Obtener lista paginada
   - Filtros y búsqueda
   - Elemento inexistente (404)

3. **Tests de UPDATE**

   - Actualización exitosa
   - Actualización parcial
   - Sin permisos (403)
   - Validaciones

4. **Tests de DELETE**
   - Eliminación exitosa
   - Sin permisos
   - Elemento inexistente
   - Verificar eliminación real

### **Ejemplo esperado**

```python
class TestTasksCRUD:
    def test_create_task_success(self, client, auth_headers):
        task_data = {
            "title": "New Task",
            "description": "Task description",
            "priority": "high"
        }
        response = client.post("/tasks/", json=task_data, headers=auth_headers)
        assert response.status_code == 201

        created_task = response.json()
        assert created_task["title"] == task_data["title"]
        assert created_task["user_id"] is not None

    def test_get_task_by_id(self, client, auth_headers, task_factory):
        task = task_factory(title="Test Task")

        response = client.get(f"/tasks/{task.id}", headers=auth_headers)
        assert response.status_code == 200

        retrieved_task = response.json()
        assert retrieved_task["id"] == task.id
        assert retrieved_task["title"] == "Test Task"
```

### **Criterios de Evaluación**

- [ ] Tests para todos los endpoints CRUD
- [ ] Casos de éxito y error cubiertos
- [ ] Autenticación y autorización probadas
- [ ] Validaciones de datos verificadas

---

## 🎯 Ejercicio 4: Tests de Aislamiento y Seguridad (15 min)

### **Objetivo**

Verificar que la seguridad y aislamiento entre usuarios funciona correctamente.

### **Tareas**

1. **Tests de aislamiento entre usuarios**

   - Usuarios solo ven sus propios datos
   - No pueden modificar datos de otros
   - Búsquedas no muestran datos de otros

2. **Tests de autorización**

   - Endpoints protegidos requieren auth
   - Roles y permisos funcionan correctamente
   - Admin puede acceder a recursos restringidos

3. **Tests de validación de tokens**
   - Token válido permite acceso
   - Token inválido rechaza acceso
   - Token expirado rechaza acceso

### **Ejemplo esperado**

```python
def test_user_isolation(self, client, auth_headers, second_user_headers):
    # Usuario 1 crea una task
    task_data = {"title": "Private Task", "description": "Only for user 1"}
    response1 = client.post("/tasks/", json=task_data, headers=auth_headers)
    task_id = response1.json()["id"]

    # Usuario 2 no puede ver la task del usuario 1
    response2 = client.get(f"/tasks/{task_id}", headers=second_user_headers)
    assert response2.status_code == 404
```

### **Criterios de Evaluación**

- [ ] Aislamiento entre usuarios verificado
- [ ] Autorización correctamente probada
- [ ] Tests de seguridad implementados
- [ ] Casos maliciosos considerados

---

## 🎯 Ejercicio 5: Coverage y Optimización (Bonus - 10 min)

### **Objetivo**

Alcanzar coverage alto y optimizar la suite de tests.

### **Tareas**

1. **Medir coverage actual**

   ```bash
   pytest --cov=app --cov-report=html
   ```

2. **Identificar gaps de coverage**

   - Revisar reporte HTML
   - Identificar líneas no cubiertas
   - Priorizar coverage crítico

3. **Crear tests adicionales**

   - Tests para casos edge
   - Tests de manejo de errores
   - Tests de funciones utilitarias

4. **Optimizar suite de tests**
   - Usar marcadores para tests lentos
   - Optimizar fixtures
   - Paralelizar cuando sea posible

### **Meta de Coverage**

- **Mínimo aceptable**: 80%
- **Objetivo**: 85%
- **Excelente**: 90%+

### **Criterios de Evaluación**

- [ ] Coverage mínimo 80% alcanzado
- [ ] Gaps importantes cubiertos
- [ ] Tests bien organizados
- [ ] Performance de tests aceptable

---

## 📊 Rúbrica de Evaluación

| Criterio                | Excelente (4)                      | Bueno (3)                 | Suficiente (2)      | Insuficiente (1) |
| ----------------------- | ---------------------------------- | ------------------------- | ------------------- | ---------------- |
| **Setup Testing**       | Setup completo con config avanzada | Setup básico funcional    | Setup mínimo        | Setup incompleto |
| **Tests Autenticación** | +10 tests, casos complejos         | 6-10 tests, casos básicos | 4-6 tests mínimos   | <4 tests         |
| **Tests CRUD**          | Todos endpoints, casos edge        | Endpoints principales     | Algunos endpoints   | Pocos tests      |
| **Coverage**            | >90% en módulos críticos           | 85-90% general            | 80-85% básico       | <80%             |
| **Organización**        | Estructura profesional             | Buena organización        | Organización básica | Desorganizado    |

## 🚀 Entregables

### **Archivos requeridos:**

1. **`tests/`** - Carpeta completa con todos los tests
2. **`pytest.ini`** - Configuración de pytest
3. **`.coveragerc`** - Configuración de coverage
4. **`requirements-dev.txt`** - Dependencias de desarrollo
5. **`README_TESTING.md`** - Documentación de tus tests

### **Formato de entrega:**

- **Repositorio Git** con commit específico para testing
- **Screenshot** del reporte de coverage
- **Documento breve** explicando decisiones de testing

---

## 💡 Tips para el Éxito

### **Organización**

1. **Empieza simple** - tests básicos primero
2. **Usa fixtures** - evita duplicación
3. **Nombra claramente** - `test_should_return_404_when_task_not_found`
4. **Agrupa por funcionalidad** - usa clases cuando apropiado

### **Coverage Inteligente**

1. **Prioriza módulos críticos** - auth, core business logic
2. **No persiguas 100%** - 85-90% es excelente
3. **Tests de calidad** > cantidad de líneas cubiertas
4. **Enfócate en casos importantes** - edge cases, errores

### **Performance**

1. **Usa marcadores** - separa tests lentos
2. **Fixtures eficientes** - reutiliza cuando sea posible
3. **Base de datos en memoria** - para tests rápidos
4. **Cleanup automático** - evita estado entre tests

### **Debugging**

1. **Tests pequeños** - fáciles de debuggear
2. **Asserts claros** - mensajes descriptivos
3. **Usa `-v`** - para output detallado
4. **Un concepto por test** - facilita identificar problemas

---

## ❓ Preguntas Frecuentes

### **"¿Cómo testear endpoints que requieren admin?"**

```python
@pytest.fixture
def admin_headers(admin_user):
    token = create_access_token({"sub": admin_user.email})
    return {"Authorization": f"Bearer {token}"}
```

### **"¿Cómo testear upload de archivos?"**

```python
def test_upload_file(client, auth_headers):
    files = {"file": ("test.txt", "file content", "text/plain")}
    response = client.post("/upload", files=files, headers=auth_headers)
    assert response.status_code == 200
```

### **"¿Cómo testear envío de emails?"**

```python
# Usa mocks para servicios externos
from unittest.mock import patch

@patch('app.services.email.send_email')
def test_password_reset_sends_email(mock_send_email, client):
    response = client.post("/auth/reset-password", json={"email": "test@example.com"})
    assert response.status_code == 200
    mock_send_email.assert_called_once()
```

---

## 🎯 Objetivos de Aprendizaje Verificados

Al completar estos ejercicios, habrás demostrado:

- ✅ **Configurar** ambiente completo de testing
- ✅ **Implementar** tests para autenticación y seguridad
- ✅ **Crear** tests CRUD completos y robustos
- ✅ **Verificar** aislamiento y autorización
- ✅ **Medir** y optimizar coverage de código
- ✅ **Organizar** tests de manera profesional

¡Éxito en tus tests! 🧪✨
