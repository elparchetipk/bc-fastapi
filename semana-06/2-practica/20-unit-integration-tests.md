# 🧪 Práctica 20: Unit e Integration Tests

**Duración estimada: 90 minutos**

## 🎯 Objetivos

- Implementar tests unitarios completos para servicios y utils
- Crear tests de integración para endpoints FastAPI
- Aplicar mocking strategies para dependencias externas
- Establecer patterns de testing reutilizables

---

## 📋 Prerequisitos

- Práctica 19 completada (pytest setup)
- Proyecto FastAPI con auth y database funcionando
- Fixtures básicas configuradas

---

## 🧪 Parte 1: Tests Unitarios Avanzados (30 min)

### **Paso 1: Tests para User Service**

Crear `tests/unit/test_user_service.py`:

```python
# tests/unit/test_user_service.py
import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session

from app.services.user_service import UserService
from app.models import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.exceptions import UserNotFoundError, EmailAlreadyExistsError


class TestUserService:
    """Tests unitarios para UserService."""

    @pytest.fixture
    def mock_db(self):
        """Mock de la sesión de base de datos."""
        return Mock(spec=Session)

    @pytest.fixture
    def user_service(self, mock_db):
        """Instancia de UserService con mock DB."""
        return UserService(db=mock_db)

    def test_create_user_success(self, user_service, mock_db):
        """Test creación exitosa de usuario."""
        # Arrange
        user_data = UserCreate(
            email="test@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            password="password123"
        )

        # Mock que no existe usuario con ese email
        mock_db.query().filter().first.return_value = None

        # Mock del usuario creado
        created_user = User(
            id=1,
            email=user_data.email,
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=UserRole.CUSTOMER
        )
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None

        with patch.object(user_service, '_create_user_instance', return_value=created_user):
            # Act
            result = user_service.create_user(user_data)

            # Assert
            assert result.email == user_data.email
            assert result.username == user_data.username
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()

    def test_create_user_email_exists(self, user_service, mock_db):
        """Test error cuando email ya existe."""
        # Arrange
        user_data = UserCreate(
            email="existing@example.com",
            username="testuser",
            first_name="Test",
            last_name="User",
            password="password123"
        )

        # Mock que ya existe usuario con ese email
        existing_user = User(id=1, email=user_data.email)
        mock_db.query().filter().first.return_value = existing_user

        # Act & Assert
        with pytest.raises(EmailAlreadyExistsError):
            user_service.create_user(user_data)

        # Verificar que no se intentó crear
        mock_db.add.assert_not_called()
        mock_db.commit.assert_not_called()

    def test_get_user_by_id_success(self, user_service, mock_db):
        """Test obtener usuario por ID exitoso."""
        # Arrange
        user_id = 1
        expected_user = User(id=user_id, email="test@example.com")
        mock_db.query().filter().first.return_value = expected_user

        # Act
        result = user_service.get_user_by_id(user_id)

        # Assert
        assert result == expected_user
        mock_db.query().filter().first.assert_called_once()

    def test_get_user_by_id_not_found(self, user_service, mock_db):
        """Test error cuando usuario no existe."""
        # Arrange
        user_id = 999
        mock_db.query().filter().first.return_value = None

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            user_service.get_user_by_id(user_id)

    def test_update_user_success(self, user_service, mock_db):
        """Test actualización exitosa de usuario."""
        # Arrange
        user_id = 1
        existing_user = User(
            id=user_id,
            email="old@example.com",
            first_name="Old",
            last_name="Name"
        )

        update_data = UserUpdate(
            first_name="New",
            last_name="Name"
        )

        mock_db.query().filter().first.return_value = existing_user

        # Act
        result = user_service.update_user(user_id, update_data)

        # Assert
        assert result.first_name == "New"
        assert result.last_name == "Name"
        assert result.email == "old@example.com"  # No cambió
        mock_db.commit.assert_called_once()

    @pytest.mark.parametrize("role,expected", [
        (UserRole.ADMIN, True),
        (UserRole.MANAGER, True),
        (UserRole.EMPLOYEE, False),
        (UserRole.CUSTOMER, False),
    ])
    def test_user_has_admin_privileges(self, user_service, role, expected):
        """Test verificación de privilegios admin con parametrización."""
        # Arrange
        user = User(id=1, role=role)

        # Act
        result = user_service.user_has_admin_privileges(user)

        # Assert
        assert result == expected
```

### **Paso 2: Tests para Product Service con Mocking**

```python
# tests/unit/test_product_service.py
import pytest
from unittest.mock import Mock, patch
from decimal import Decimal

from app.services.product_service import ProductService
from app.models import Product, ProductCategory, User
from app.schemas.product import ProductCreate, ProductUpdate
from app.exceptions import ProductNotFoundError, InsufficientStockError


class TestProductService:
    """Tests unitarios para ProductService."""

    @pytest.fixture
    def mock_db(self):
        return Mock()

    @pytest.fixture
    def product_service(self, mock_db):
        return ProductService(db=mock_db)

    @pytest.fixture
    def sample_product(self):
        return Product(
            id=1,
            name="Test Product",
            description="A test product",
            price=Decimal("99.99"),
            category=ProductCategory.ELECTRONICS,
            stock_quantity=10,
            created_by=1
        )

    def test_create_product_success(self, product_service, mock_db):
        """Test creación exitosa de producto."""
        # Arrange
        product_data = ProductCreate(
            name="New Product",
            description="A new product",
            price=Decimal("49.99"),
            category=ProductCategory.BOOKS,
            stock_quantity=5
        )
        user_id = 1

        created_product = Product(
            id=1,
            **product_data.dict(),
            created_by=user_id
        )

        with patch.object(product_service, '_create_product_instance', return_value=created_product):
            # Act
            result = product_service.create_product(product_data, user_id)

            # Assert
            assert result.name == product_data.name
            assert result.price == product_data.price
            assert result.created_by == user_id
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()

    def test_reduce_stock_success(self, product_service, mock_db, sample_product):
        """Test reducción exitosa de stock."""
        # Arrange
        initial_stock = sample_product.stock_quantity
        reduce_quantity = 3
        mock_db.query().filter().first.return_value = sample_product

        # Act
        result = product_service.reduce_stock(sample_product.id, reduce_quantity)

        # Assert
        assert result.stock_quantity == initial_stock - reduce_quantity
        mock_db.commit.assert_called_once()

    def test_reduce_stock_insufficient(self, product_service, mock_db, sample_product):
        """Test error por stock insuficiente."""
        # Arrange
        sample_product.stock_quantity = 2
        reduce_quantity = 5
        mock_db.query().filter().first.return_value = sample_product

        # Act & Assert
        with pytest.raises(InsufficientStockError):
            product_service.reduce_stock(sample_product.id, reduce_quantity)

        # Verificar que no se hizo commit
        mock_db.commit.assert_not_called()

    @patch('app.services.product_service.send_low_stock_alert')
    def test_reduce_stock_triggers_alert(self, mock_alert, product_service, mock_db, sample_product):
        """Test que se envía alerta cuando stock es bajo."""
        # Arrange
        sample_product.stock_quantity = 5
        reduce_quantity = 3  # Quedará en 2, por debajo del threshold
        mock_db.query().filter().first.return_value = sample_product

        # Act
        product_service.reduce_stock(sample_product.id, reduce_quantity)

        # Assert
        mock_alert.assert_called_once_with(sample_product)

    def test_search_products_by_category(self, product_service, mock_db):
        """Test búsqueda de productos por categoría."""
        # Arrange
        category = ProductCategory.ELECTRONICS
        expected_products = [
            Product(id=1, name="Laptop", category=category),
            Product(id=2, name="Phone", category=category)
        ]

        mock_query = mock_db.query.return_value
        mock_query.filter.return_value.all.return_value = expected_products

        # Act
        result = product_service.search_by_category(category)

        # Assert
        assert len(result) == 2
        assert all(p.category == category for p in result)
        mock_query.filter.assert_called_once()
```

---

## 🌐 Parte 2: Tests de Integración para Endpoints (40 min)

### **Paso 1: Tests de Endpoints de Autenticación**

Crear `tests/integration/test_api_auth.py`:

```python
# tests/integration/test_api_auth.py
import pytest
from fastapi.testclient import TestClient

class TestAuthEndpoints:
    """Tests de integración para endpoints de autenticación."""

    def test_register_user_success(self, client: TestClient):
        """Test registro exitoso de usuario."""
        # Arrange
        user_data = {
            "email": "newuser@example.com",
            "username": "newuser",
            "first_name": "New",
            "last_name": "User",
            "password": "securepassword123"
        }

        # Act
        response = client.post("/auth/register", json=user_data)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["username"] == user_data["username"]
        assert "password" not in data
        assert "id" in data
        assert data["role"] == "customer"

    def test_register_duplicate_email(self, client: TestClient, test_user):
        """Test error al registrar email duplicado."""
        # Arrange
        user_data = {
            "email": test_user.email,  # Email ya existe
            "username": "differentuser",
            "first_name": "Different",
            "last_name": "User",
            "password": "password123"
        }

        # Act
        response = client.post("/auth/register", json=user_data)

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "email" in data["detail"].lower()

    def test_login_success(self, client: TestClient, test_user, test_password):
        """Test login exitoso."""
        # Arrange
        login_data = {
            "username": test_user.email,
            "password": test_password
        }

        # Act
        response = client.post("/auth/login", data=login_data)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == test_user.email

    def test_login_invalid_credentials(self, client: TestClient, test_user):
        """Test error con credenciales inválidas."""
        # Arrange
        login_data = {
            "username": test_user.email,
            "password": "wrongpassword"
        }

        # Act
        response = client.post("/auth/login", data=login_data)

        # Assert
        assert response.status_code == 401
        data = response.json()
        assert "incorrect" in data["detail"].lower()

    def test_login_user_not_found(self, client: TestClient):
        """Test error con usuario inexistente."""
        # Arrange
        login_data = {
            "username": "nonexistent@example.com",
            "password": "password123"
        }

        # Act
        response = client.post("/auth/login", data=login_data)

        # Assert
        assert response.status_code == 401

    def test_get_current_user_success(self, client: TestClient, auth_headers, test_user):
        """Test obtener usuario actual con token válido."""
        # Act
        response = client.get("/auth/me", headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == test_user.email
        assert data["username"] == test_user.username
        assert "password" not in data

    def test_get_current_user_no_token(self, client: TestClient):
        """Test error sin token de autenticación."""
        # Act
        response = client.get("/auth/me")

        # Assert
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test error con token inválido."""
        # Arrange
        headers = {"Authorization": "Bearer invalid.token.here"}

        # Act
        response = client.get("/auth/me", headers=headers)

        # Assert
        assert response.status_code == 401

    def test_refresh_token_success(self, client: TestClient, test_user, test_password):
        """Test renovación exitosa de token."""
        # Arrange - Obtener refresh token
        login_response = client.post("/auth/login", data={
            "username": test_user.email,
            "password": test_password
        })
        refresh_token = login_response.json()["refresh_token"]

        # Act
        response = client.post("/auth/refresh", json={
            "refresh_token": refresh_token
        })

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_logout_success(self, client: TestClient, auth_headers):
        """Test logout exitoso."""
        # Act
        response = client.post("/auth/logout", headers=auth_headers)

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "logged out" in data["message"].lower()
```

### **Paso 2: Tests de Endpoints de Productos**

```python
# tests/integration/test_api_products.py
import pytest
from fastapi.testclient import TestClient

class TestProductEndpoints:
    """Tests de integración para endpoints de productos."""

    def test_get_products_public(self, client: TestClient, multiple_products):
        """Test obtener productos sin autenticación."""
        # Act
        response = client.get("/products")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert len(data) == len(multiple_products)
        assert all("id" in product for product in data)
        assert all("name" in product for product in data)
        assert all("price" in product for product in data)

    def test_get_product_by_id(self, client: TestClient, test_product):
        """Test obtener producto específico por ID."""
        # Act
        response = client.get(f"/products/{test_product.id}")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_product.id
        assert data["name"] == test_product.name
        assert data["price"] == str(test_product.price)

    def test_get_product_not_found(self, client: TestClient):
        """Test error producto no encontrado."""
        # Act
        response = client.get("/products/999")

        # Assert
        assert response.status_code == 404

    def test_create_product_success(self, client: TestClient, auth_headers):
        """Test creación exitosa de producto."""
        # Arrange
        product_data = {
            "name": "New Product",
            "description": "A brand new product",
            "price": 79.99,
            "category": "ELECTRONICS",
            "stock_quantity": 15
        }

        # Act
        response = client.post("/products", json=product_data, headers=auth_headers)

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == product_data["name"]
        assert data["price"] == str(product_data["price"])
        assert data["category"] == product_data["category"]
        assert "id" in data

    def test_create_product_unauthorized(self, client: TestClient):
        """Test error crear producto sin autenticación."""
        # Arrange
        product_data = {
            "name": "Unauthorized Product",
            "price": 50.0,
            "category": "BOOKS"
        }

        # Act
        response = client.post("/products", json=product_data)

        # Assert
        assert response.status_code == 401

    def test_create_product_invalid_data(self, client: TestClient, auth_headers):
        """Test error crear producto con datos inválidos."""
        # Arrange
        invalid_data = {
            "name": "",  # Nombre vacío
            "price": -10,  # Precio negativo
            "category": "INVALID_CATEGORY"
        }

        # Act
        response = client.post("/products", json=invalid_data, headers=auth_headers)

        # Assert
        assert response.status_code == 422

    def test_update_product_success(self, client: TestClient, test_product, auth_headers):
        """Test actualización exitosa de producto."""
        # Arrange
        update_data = {
            "name": "Updated Product Name",
            "price": 129.99
        }

        # Act
        response = client.put(
            f"/products/{test_product.id}",
            json=update_data,
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == update_data["name"]
        assert data["price"] == str(update_data["price"])

    def test_delete_product_admin_only(self, client: TestClient, test_product, admin_auth_headers):
        """Test eliminación de producto (solo admin)."""
        # Act
        response = client.delete(f"/products/{test_product.id}", headers=admin_auth_headers)

        # Assert
        assert response.status_code == 200

        # Verificar que el producto ya no existe
        get_response = client.get(f"/products/{test_product.id}")
        assert get_response.status_code == 404

    def test_delete_product_insufficient_permissions(self, client: TestClient, test_product, auth_headers):
        """Test error eliminación sin permisos admin."""
        # Act
        response = client.delete(f"/products/{test_product.id}", headers=auth_headers)

        # Assert
        assert response.status_code == 403

    def test_search_products_by_category(self, client: TestClient, multiple_products):
        """Test búsqueda de productos por categoría."""
        # Act
        response = client.get("/products?category=ELECTRONICS")

        # Assert
        assert response.status_code == 200
        data = response.json()
        electronics_count = sum(1 for p in multiple_products if p.category.value == "ELECTRONICS")
        assert len(data) == electronics_count
        assert all(product["category"] == "ELECTRONICS" for product in data)

    def test_search_products_by_price_range(self, client: TestClient, multiple_products):
        """Test búsqueda de productos por rango de precio."""
        # Act
        response = client.get("/products?min_price=20&max_price=100")

        # Assert
        assert response.status_code == 200
        data = response.json()
        for product in data:
            price = float(product["price"])
            assert 20 <= price <= 100
```

---

## 🧪 Parte 3: Tests con Async Client (20 min)

### **Paso 1: Tests Asíncronos para Endpoints Complejos**

```python
# tests/integration/test_async_endpoints.py
import pytest
import httpx
from app.main import app

class TestAsyncEndpoints:
    """Tests asíncronos para endpoints que requieren operaciones complejas."""

    @pytest.mark.asyncio
    async def test_bulk_product_creation(self, async_client: httpx.AsyncClient, auth_headers):
        """Test creación masiva de productos."""
        # Arrange
        products_data = [
            {
                "name": f"Product {i}",
                "description": f"Description {i}",
                "price": 10.00 + i,
                "category": "ELECTRONICS",
                "stock_quantity": 5
            }
            for i in range(5)
        ]

        # Act
        response = await async_client.post(
            "/products/bulk",
            json={"products": products_data},
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 201
        data = response.json()
        assert len(data["created_products"]) == 5

    @pytest.mark.asyncio
    async def test_export_products_csv(self, async_client: httpx.AsyncClient, multiple_products, admin_auth_headers):
        """Test exportación de productos a CSV."""
        # Act
        response = await async_client.get("/products/export/csv", headers=admin_auth_headers)

        # Assert
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/csv"
        assert "attachment" in response.headers["content-disposition"]

    @pytest.mark.asyncio
    async def test_concurrent_stock_updates(self, async_client: httpx.AsyncClient, test_product, auth_headers):
        """Test actualizaciones concurrentes de stock."""
        # Arrange
        product_id = test_product.id
        initial_stock = test_product.stock_quantity

        # Act - Múltiples requests concurrentes
        tasks = []
        for i in range(3):
            task = async_client.patch(
                f"/products/{product_id}/stock",
                json={"operation": "reduce", "quantity": 1},
                headers=auth_headers
            )
            tasks.append(task)

        responses = await asyncio.gather(*tasks)

        # Assert
        for response in responses:
            assert response.status_code in [200, 409]  # Success o conflict

        # Verificar estado final
        final_response = await async_client.get(f"/products/{product_id}")
        final_stock = final_response.json()["stock_quantity"]
        assert final_stock <= initial_stock
```

---

## ✅ Verificación y Debugging

### **Comandos de Testing**

```bash
# Ejecutar todos los tests unitarios
pytest tests/unit/ -v

# Ejecutar tests de integración
pytest tests/integration/ -v

# Ejecutar con coverage detallado
pytest --cov=app --cov-report=html --cov-branch

# Ejecutar tests específicos con debugging
pytest tests/unit/test_user_service.py::TestUserService::test_create_user_success -v -s

# Ejecutar solo tests lentos
pytest -m slow

# Ejecutar tests en paralelo
pytest -n auto
```

### **Debugging Tips**

```python
# En tests, usar pdb para debugging
def test_complex_scenario(self, client):
    response = client.post("/complex-endpoint", json=data)
    import pdb; pdb.set_trace()  # Pausa aquí
    assert response.status_code == 200

# Mostrar logs durante testing
pytest -s --log-cli-level=INFO

# Ejecutar hasta el primer fallo
pytest -x

# Usar fixtures para debugging
@pytest.fixture
def debug_user(test_user):
    print(f"Debug: Using user {test_user.email}")
    return test_user
```

---

## 🎯 Entregables

1. **Tests unitarios** completos para servicios principales
2. **Tests de integración** para todos los endpoints críticos
3. **Mocking strategies** implementadas apropiadamente
4. **Tests asíncronos** para operaciones complejas
5. **Coverage ≥80%** en servicios y endpoints

---

## 📚 Próximos Pasos

En la siguiente práctica cubriremos:

- Quality assurance automation
- Coverage analysis avanzado
- Performance testing básico
- CI/CD integration

---

**🎯 Estos tests son tu red de seguridad. Cada test que escribes es una inversión en la confiabilidad de tu aplicación.**
