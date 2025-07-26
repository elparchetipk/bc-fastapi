# Práctica 14: Testing Básico con Base de Datos

## 🎯 Objetivo

Aprender a escribir tests básicos para tu API con base de datos. Crearás tests simples que verifican que tu API funciona correctamente.

- Configurar testing básico con pytest
- Crear una base de datos de prueba
- Escribir tests para endpoints
- Verificar operaciones CRUD

## ⏱️ Tiempo: 35 minutos

## 📋 Pre-requisitos

- ✅ Práctica 13 completada (Relaciones básicas)
- ✅ API con categorías y productos funcionando
- ✅ Base de datos con relaciones

---

## 🚀 Paso 1: Instalar pytest (5 min)

### Actualizar requirements.txt

```text
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
pytest==7.4.3
httpx==0.25.2
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🧪 Paso 2: Configurar Testing (10 min)

### Crear archivo conftest.py

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from main import app
from database import get_db, Base

# Base de datos de prueba (en memoria)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    # Crear tablas de prueba
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    # Limpiar después de cada test
    Base.metadata.drop_all(bind=engine)
    # Eliminar archivo de base de datos de prueba
    if os.path.exists("test.db"):
        os.remove("test.db")
```

---

## 📝 Paso 3: Tests para Categorías (10 min)

### Crear archivo test_categorias.py

```python
import pytest
from fastapi.testclient import TestClient

def test_crear_categoria(client: TestClient):
    """Test crear una nueva categoría"""
    response = client.post(
        "/categorias/",
        json={"nombre": "Electrónicos", "descripcion": "Dispositivos electrónicos"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Electrónicos"
    assert data["descripcion"] == "Dispositivos electrónicos"
    assert "id" in data

def test_listar_categorias_vacio(client: TestClient):
    """Test listar categorías cuando no hay ninguna"""
    response = client.get("/categorias/")
    assert response.status_code == 200
    assert response.json() == []

def test_listar_categorias_con_datos(client: TestClient):
    """Test listar categorías con datos"""
    # Crear categoría
    client.post(
        "/categorias/",
        json={"nombre": "Libros", "descripcion": "Libros y literatura"}
    )

    # Listar categorías
    response = client.get("/categorias/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["nombre"] == "Libros"

def test_obtener_categoria(client: TestClient):
    """Test obtener categoría específica"""
    # Crear categoría
    create_response = client.post(
        "/categorias/",
        json={"nombre": "Deportes", "descripcion": "Artículos deportivos"}
    )
    categoria_id = create_response.json()["id"]

    # Obtener categoría
    response = client.get(f"/categorias/{categoria_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Deportes"
    assert data["productos"] == []  # Sin productos inicialmente

def test_categoria_no_encontrada(client: TestClient):
    """Test error cuando categoría no existe"""
    response = client.get("/categorias/999")
    assert response.status_code == 404
```

---

## 🛍️ Paso 4: Tests para Productos (10 min)

### Crear archivo test_productos.py

```python
import pytest
from fastapi.testclient import TestClient

def test_crear_producto_sin_categoria(client: TestClient):
    """Test crear producto sin categoría"""
    response = client.post(
        "/productos/",
        json={
            "nombre": "Producto Test",
            "precio": 99.99,
            "descripcion": "Producto de prueba"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Producto Test"
    assert data["precio"] == 99.99

def test_crear_producto_con_categoria(client: TestClient):
    """Test crear producto con categoría"""
    # Crear categoría primero
    categoria_response = client.post(
        "/categorias/",
        json={"nombre": "Tecnología", "descripcion": "Productos tecnológicos"}
    )
    categoria_id = categoria_response.json()["id"]

    # Crear producto con categoría
    response = client.post(
        "/productos/",
        json={
            "nombre": "Smartphone",
            "precio": 599.99,
            "descripcion": "Teléfono inteligente",
            "categoria_id": categoria_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Smartphone"
    assert data["categoria_id"] == categoria_id

def test_listar_productos_con_categoria(client: TestClient):
    """Test listar productos mostrando información de categoría"""
    # Crear categoría
    categoria_response = client.post(
        "/categorias/",
        json={"nombre": "Hogar", "descripcion": "Productos para el hogar"}
    )
    categoria_id = categoria_response.json()["id"]

    # Crear producto
    client.post(
        "/productos/",
        json={
            "nombre": "Aspiradora",
            "precio": 199.99,
            "descripcion": "Aspiradora potente",
            "categoria_id": categoria_id
        }
    )

    # Listar productos
    response = client.get("/productos/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["categoria"]["nombre"] == "Hogar"

def test_productos_por_categoria(client: TestClient):
    """Test filtrar productos por categoría"""
    # Crear categoría
    categoria_response = client.post(
        "/categorias/",
        json={"nombre": "Ropa", "descripcion": "Prendas de vestir"}
    )
    categoria_id = categoria_response.json()["id"]

    # Crear productos
    client.post(
        "/productos/",
        json={
            "nombre": "Camiseta",
            "precio": 25.99,
            "descripcion": "Camiseta de algodón",
            "categoria_id": categoria_id
        }
    )

    client.post(
        "/productos/",
        json={
            "nombre": "Pantalón",
            "precio": 45.99,
            "descripcion": "Pantalón casual",
            "categoria_id": categoria_id
        }
    )

    # Obtener productos de la categoría
    response = client.get(f"/categorias/{categoria_id}/productos/")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["productos"]) == 2

def test_validacion_precio_negativo(client: TestClient):
    """Test validación de precio negativo"""
    response = client.post(
        "/productos/",
        json={
            "nombre": "Producto Inválido",
            "precio": -10.99,
            "descripcion": "Precio negativo"
        }
    )
    assert response.status_code == 400
```

---

## 🏃 Paso 5: Ejecutar Tests

### Ejecutar todos los tests

```bash
# Ejecutar todos los tests
pytest

# Ejecutar con más detalles
pytest -v

# Ejecutar solo tests de categorías
pytest test_categorias.py

# Ejecutar un test específico
pytest test_productos.py::test_crear_producto_sin_categoria
```

### Salida esperada

```text
========================= test session starts =========================
collected 8 items

test_categorias.py ....                                        [ 50%]
test_productos.py ....                                         [100%]

========================= 8 passed in 2.34s =========================
```

---

## ✅ Verificación

### Tests que Deben Pasar

- [ ] **test_crear_categoria** - Crear categorías funciona
- [ ] **test_listar_categorias** - Listar funciona con y sin datos
- [ ] **test_obtener_categoria** - Obtener categoría específica
- [ ] **test_crear_producto_con_categoria** - Relaciones funcionan
- [ ] **test_productos_por_categoria** - Filtros funcionan
- [ ] **test_validacion_precio_negativo** - Validaciones funcionan

### Estructura Final

```text
semana-04-practica/
├── main.py               # ✅ API principal
├── crud.py               # ✅ Funciones CRUD
├── database.py           # ✅ Configuración BD
├── models.py             # ✅ Modelos con relaciones
├── schemas.py            # ✅ Schemas con validaciones
├── conftest.py           # ✅ Configuración de tests
├── test_categorias.py    # ✅ Tests de categorías
├── test_productos.py     # ✅ Tests de productos
├── requirements.txt      # ✅ Con pytest y httpx
├── productos.db          # ✅ BD de desarrollo
└── test.db              # ✅ BD de prueba (temporal)
```

---

## 🎯 Resumen

### Lo que Aprendiste

- ✅ **Testing básico** - pytest para verificar tu API
- ✅ **Base de datos de prueba** - Tests aislados e independientes
- ✅ **TestClient** - Simular requests HTTP en tests
- ✅ **Fixtures** - Configuración reutilizable para tests
- ✅ **Assertions** - Verificar que el código funciona correctamente

### Conceptos Clave

1. **pytest** - Framework de testing para Python
2. **TestClient** - Cliente HTTP para testing de FastAPI
3. **Fixtures** - Configuración compartida entre tests
4. **Base de datos temporal** - SQLite en memoria para tests
5. **Assertions** - `assert` para verificar resultados

### Ventajas del Testing

- 🐛 **Detectar errores** antes de production
- 🔒 **Confianza** en que tu código funciona
- 🚀 **Refactoring seguro** - cambios sin miedo
- 📝 **Documentación** viva de cómo funciona la API

### Próximo Paso

¡Tu API ahora tiene tests! Esto te da confianza para hacer cambios y mejoras sabiendo que todo sigue funcionando correctamente.

---

## 🔗 Enlaces Útiles

- [pytest Documentación](https://docs.pytest.org/en/7.4.x/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [TestClient Guide](https://fastapi.tiangolo.com/tutorial/testing/#testclient)

