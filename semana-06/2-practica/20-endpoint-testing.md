# Práctica 20: Testing de Endpoints

## 🎯 Objetivo

Implementar **testing completo de endpoints** CRUD y validaciones en 90 minutos, cubriendo casos de éxito y error de forma sistemática.

## ⏱️ Tiempo: 90 minutos

## 📋 Pre-requisitos

- ✅ Práctica 19 completada (pytest configurado)
- ✅ API con endpoints CRUD funcionando
- ✅ TestClient y fixtures básicas configuradas
- ✅ Base de datos de testing funcionando

## 🚀 Desarrollo Paso a Paso

### Paso 1: Testing de Endpoints GET (25 min)

#### Test de listado de recursos

```python
# tests/test_users.py
import pytest
from fastapi import status

def test_get_users_empty_list(client):
    """Test de lista vacía de usuarios"""
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_users_with_data(client, sample_users):
    """Test de lista con usuarios existentes"""
    # Primero crear algunos usuarios
    for user in sample_users:
        client.post("/auth/register", json=user)

    # Verificar que aparecen en la lista
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    users_list = response.json()
    assert len(users_list) == len(sample_users)
    assert isinstance(users_list, list)

def test_get_user_by_id_success(client, test_user):
    """Test de obtener usuario por ID existente"""
    # Crear usuario primero
    create_response = client.post("/auth/register", json=test_user)
    assert create_response.status_code == status.HTTP_201_CREATED
    user_id = create_response.json()["id"]

    # Obtener usuario por ID
    response = client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    user_data = response.json()
    assert user_data["id"] == user_id
    assert user_data["email"] == test_user["email"]
    assert "password" not in user_data  # No debe devolver password

def test_get_user_by_id_not_found(client):
    """Test de usuario no encontrado"""
    response = client.get("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "not found" in response.json()["detail"].lower()
```

#### Test de endpoints de recursos relacionados

```python
# tests/test_items.py (si tienes items en tu API)
def test_get_user_items_empty(client, test_user):
    """Test de items de usuario vacío"""
    # Crear usuario
    create_response = client.post("/auth/register", json=test_user)
    user_id = create_response.json()["id"]

    # Verificar items vacíos
    response = client.get(f"/users/{user_id}/items")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_items_list(client):
    """Test de listado general de items"""
    response = client.get("/items/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
```

---

### Paso 2: Testing de Endpoints POST (25 min)

#### Test de creación exitosa

```python
# tests/test_users.py (continuar)
def test_create_user_success(client, test_user):
    """Test de creación exitosa de usuario"""
    response = client.post("/auth/register", json=test_user)
    assert response.status_code == status.HTTP_201_CREATED

    user_data = response.json()
    assert user_data["email"] == test_user["email"]
    assert user_data["name"] == test_user["name"]
    assert "id" in user_data
    assert "password" not in user_data  # Password no debe retornarse
    assert "created_at" in user_data  # Si tienes timestamps

def test_create_user_duplicate_email(client, test_user):
    """Test de email duplicado"""
    # Crear usuario primera vez
    response1 = client.post("/auth/register", json=test_user)
    assert response1.status_code == status.HTTP_201_CREATED

    # Intentar crear mismo email
    response2 = client.post("/auth/register", json=test_user)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response2.json()["detail"].lower()

def test_create_user_invalid_email(client):
    """Test de email inválido"""
    invalid_user = {
        "email": "not-an-email",
        "password": "password123",
        "name": "Test User"
    }
    response = client.post("/auth/register", json=invalid_user)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    errors = response.json()["detail"]
    assert any("email" in str(error).lower() for error in errors)
```

#### Test de validaciones de datos

```python
def test_create_user_missing_fields(client):
    """Test de campos requeridos faltantes"""
    # Email faltante
    response = client.post("/auth/register", json={
        "password": "password123",
        "name": "Test User"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Password faltante
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "name": "Test User"
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_user_empty_fields(client):
    """Test de campos vacíos"""
    response = client.post("/auth/register", json={
        "email": "",
        "password": "",
        "name": ""
    })
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_create_user_password_too_short(client):
    """Test de password muy corta"""
    response = client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "123",  # Muy corta
        "name": "Test User"
    })
    # Dependiendo de tu validación, podría ser 422 o 400
    assert response.status_code in [status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_400_BAD_REQUEST]
```

---

### Paso 3: Testing de Endpoints PUT/PATCH (20 min)

#### Test de actualización exitosa

```python
def test_update_user_success(client, test_user):
    """Test de actualización exitosa"""
    # Crear usuario
    create_response = client.post("/auth/register", json=test_user)
    user_id = create_response.json()["id"]

    # Datos para actualizar
    update_data = {
        "name": "Updated Name",
        "email": test_user["email"]  # Mantener email
    }

    # Actualizar usuario
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK

    updated_user = response.json()
    assert updated_user["name"] == "Updated Name"
    assert updated_user["email"] == test_user["email"]
    assert updated_user["id"] == user_id

def test_update_user_not_found(client):
    """Test de actualización de usuario inexistente"""
    update_data = {"name": "New Name"}
    response = client.put("/users/999", json=update_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_partial_update_user(client, test_user):
    """Test de actualización parcial (PATCH)"""
    # Crear usuario
    create_response = client.post("/auth/register", json=test_user)
    user_id = create_response.json()["id"]

    # Solo actualizar nombre
    response = client.patch(f"/users/{user_id}", json={"name": "Partial Update"})
    assert response.status_code == status.HTTP_200_OK

    updated_user = response.json()
    assert updated_user["name"] == "Partial Update"
    assert updated_user["email"] == test_user["email"]  # No cambió
```

---

### Paso 4: Testing de Endpoints DELETE (20 min)

#### Test de eliminación exitosa

```python
def test_delete_user_success(client, test_user):
    """Test de eliminación exitosa"""
    # Crear usuario
    create_response = client.post("/auth/register", json=test_user)
    user_id = create_response.json()["id"]

    # Eliminar usuario
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verificar que ya no existe
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_user_not_found(client):
    """Test de eliminación de usuario inexistente"""
    response = client.delete("/users/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_user_cascade_items(client, test_user):
    """Test de eliminación en cascada (si tienes relaciones)"""
    # Crear usuario
    create_response = client.post("/auth/register", json=test_user)
    user_id = create_response.json()["id"]

    # Crear item del usuario (si aplicable)
    item_data = {
        "title": "Test Item",
        "description": "Test Description",
        "owner_id": user_id
    }
    item_response = client.post("/items/", json=item_data)
    assert item_response.status_code == status.HTTP_201_CREATED

    # Eliminar usuario
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == status.HTTP_204_NO_CONTENT

    # Verificar que items del usuario también se eliminaron
    items_response = client.get("/items/")
    items = items_response.json()
    user_items = [item for item in items if item.get("owner_id") == user_id]
    assert len(user_items) == 0
```

---

### Paso 5: Testing de Validaciones y Errores (20 min)

#### Fixture para errores comunes

```python
# Agregar a tests/conftest.py
@pytest.fixture
def invalid_user_data():
    """Datos inválidos para testing de errores"""
    return [
        # Email inválido
        {"email": "invalid-email", "password": "validpass123", "name": "Test"},
        # Password muy corta
        {"email": "test@example.com", "password": "123", "name": "Test"},
        # Nombre vacío
        {"email": "test@example.com", "password": "validpass123", "name": ""},
        # Email muy largo
        {"email": "a" * 300 + "@example.com", "password": "validpass123", "name": "Test"},
    ]
```

#### Tests parametrizados para validaciones

```python
@pytest.mark.parametrize("invalid_data", [
    {"email": "invalid-email", "password": "validpass123", "name": "Test"},
    {"email": "test@example.com", "password": "123", "name": "Test"},
    {"email": "test@example.com", "password": "validpass123", "name": ""},
])
def test_create_user_validation_errors(client, invalid_data):
    """Test parametrizado de errores de validación"""
    response = client.post("/auth/register", json=invalid_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()

def test_request_with_invalid_json(client):
    """Test de JSON malformado"""
    response = client.post(
        "/auth/register",
        data="invalid json",
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_request_with_extra_fields(client):
    """Test de campos adicionales no permitidos"""
    data_with_extra = {
        "email": "test@example.com",
        "password": "validpass123",
        "name": "Test User",
        "extra_field": "should be ignored"
    }
    response = client.post("/auth/register", json=data_with_extra)
    # Debería funcionar, FastAPI ignora campos extra por defecto
    assert response.status_code == status.HTTP_201_CREATED

    # Verificar que campo extra no se guarda
    user_data = response.json()
    assert "extra_field" not in user_data
```

---

## 🧪 Testing Manual

### Ejecutar Tests por Categoría

#### 1. Tests de endpoints GET

```bash
pytest tests/test_users.py -k "test_get" -v
```

#### 2. Tests de endpoints POST

```bash
pytest tests/test_users.py -k "test_create" -v
```

#### 3. Tests de validaciones

```bash
pytest tests/test_users.py -k "validation" -v
```

#### 4. Todos los tests de usuarios

```bash
pytest tests/test_users.py -v
```

---

## 📊 Checklist de Verificación

### ✅ Tests GET

- [ ] Lista vacía retorna 200 y array vacío
- [ ] Lista con datos retorna 200 y array con objetos
- [ ] GET por ID existente retorna 200 y objeto correcto
- [ ] GET por ID inexistente retorna 404

### ✅ Tests POST

- [ ] Creación exitosa retorna 201 y objeto creado
- [ ] Email duplicado retorna 400/422
- [ ] Datos inválidos retornan 422
- [ ] Campos faltantes retornan 422

### ✅ Tests PUT/PATCH

- [ ] Actualización exitosa retorna 200 y objeto actualizado
- [ ] Actualización de inexistente retorna 404
- [ ] Actualización parcial funciona correctamente

### ✅ Tests DELETE

- [ ] Eliminación exitosa retorna 204
- [ ] Eliminación de inexistente retorna 404
- [ ] Objeto eliminado ya no es accesible

### ✅ Tests de Validación

- [ ] Emails inválidos son rechazados
- [ ] Passwords cortas son rechazadas
- [ ] Campos requeridos faltantes son detectados
- [ ] JSON malformado es manejado correctamente

---

## 🔧 Troubleshooting

### ❌ Error: "AssertionError en test_create_user"

```python
# Verificar estructura de respuesta
def test_debug_create_response(client, test_user):
    response = client.post("/auth/register", json=test_user)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    # Ajustar assertions basado en la salida real
```

### ❌ Error: "Tests fallan por BD no limpia"

```python
# En conftest.py, agregar cleanup automático
@pytest.fixture(autouse=True)
def cleanup_db():
    """Limpiar BD antes y después de cada test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
```

### ❌ Error: "Tests muy lentos"

```bash
# Ejecutar tests en paralelo
pip install pytest-xdist
pytest -n auto
```

---

## 📚 Recursos Adicionales

### Comandos Útiles

```bash
# Ejecutar solo tests que fallaron la última vez
pytest --lf

# Ejecutar hasta el primer fallo
pytest -x

# Mostrar output de print statements
pytest -s

# Coverage de endpoints específicos
pytest tests/test_users.py --cov=main --cov-report=html
```

### Extensiones Útiles

```bash
# Para mejor output de fallos
pip install pytest-sugar

# Para tests parametrizados avanzados
pip install pytest-cases

# Para mocking más fácil
pip install pytest-mock
```

---

## 🎯 Próximos Pasos

En la siguiente práctica aprenderás:

1. **Testing con autenticación** - Headers JWT, login flows
2. **Mocking de dependencias** - Usuarios autenticados, roles
3. **Tests de autorización** - Permisos y restricciones
4. **Tests de integración** - Flujos completos end-to-end

¡Has dominado el testing básico de endpoints! 🧪🚀
