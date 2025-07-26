# Recursos de Apoyo - Semana 3: FastAPI Intermedio

## 📚 Documentación Oficial

### **FastAPI Core**

- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Documentación oficial completa
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) - Tutorial paso a paso
- [FastAPI Advanced User Guide](https://fastapi.tiangolo.com/advanced/) - Guías avanzadas
- [FastAPI GitHub Repository](https://github.com/tiangolo/fastapi) - Código fuente y ejemplos

### **Pydantic (Validación)**

- [Pydantic Documentation](https://docs.pydantic.dev/) - Documentación v2
- [Pydantic Validators](https://docs.pydantic.dev/latest/concepts/validators/) - Validadores custom
- [Pydantic Field Types](https://docs.pydantic.dev/latest/concepts/types/) - Tipos de campos
- [Pydantic Migration Guide](https://docs.pydantic.dev/latest/migration/) - Migración v1 a v2

### **HTTP y REST**

- [HTTP Status Codes](https://httpstatuses.com/) - Referencia completa de códigos
- [REST API Design](https://restfulapi.net/) - Mejores prácticas REST
- [HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) - MDN Web Docs
- [API Design Patterns](https://microservices.io/patterns/data/api-composition.html) - Patrones de diseño

---

## 🛠️ Herramientas de Desarrollo

### **Testing de APIs**

#### **Postman**

- [Postman Download](https://www.postman.com/downloads/) - Cliente gráfico
- [Postman Learning Center](https://learning.postman.com/) - Tutoriales y documentación
- [Postman Collections](https://learning.postman.com/docs/collections/intro-to-collections/) - Organizar requests

#### **HTTPie**

```bash
# Instalación
pip install httpie

# Ejemplos de uso
http GET localhost:8000/api/v1/products
http POST localhost:8000/api/v1/products name="Test Product" price:=99.99
http PUT localhost:8000/api/v1/products/1 name="Updated Product"
http DELETE localhost:8000/api/v1/products/1
```

#### **curl (Línea de comandos)**

```bash
# GET request
curl -X GET "http://localhost:8000/api/v1/products"

# POST con JSON
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Product", "price": 99.99}'

# PUT con headers
curl -X PUT "http://localhost:8000/api/v1/products/1" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"name": "Updated Product", "price": 129.99}'

# DELETE
curl -X DELETE "http://localhost:8000/api/v1/products/1" -v
```

### **Editores y IDEs**

#### **VS Code (Recomendado)**

```bash
# Extensiones esenciales
code --install-extension ms-python.python
code --install-extension ms-python.pylint
code --install-extension ms-python.black-formatter
code --install-extension humao.rest-client
code --install-extension ms-python.isort
```

**Configuración VS Code para FastAPI:**

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.pylintEnabled": true,
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

#### **PyCharm**

- [PyCharm Professional](https://www.jetbrains.com/pycharm/) - IDE completo para Python
- [FastAPI Plugin](https://plugins.jetbrains.com/plugin/14251-fastapi) - Plugin específico para FastAPI

### **Validación y Linting**

#### **Herramientas de Calidad**

```bash
# Instalar herramientas de desarrollo
pip install black isort mypy flake8 pytest

# Formatear código
black app/
isort app/

# Verificar tipos
mypy app/

# Linting
flake8 app/

# Testing
pytest tests/
```

---

## 📖 Guías y Tutoriales

### **FastAPI Específico**

- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices) - Mejores prácticas comunitarias
- [Full Stack FastAPI Template](https://github.com/tiangolo/full-stack-fastapi-postgresql) - Template completo oficial
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/) - Autenticación y usuarios
- [FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/) - Integración con bases de datos

### **Patrones de Arquitectura**

- [Repository Pattern](https://deviq.com/design-patterns/repository-pattern) - Patrón de acceso a datos
- [Service Layer Pattern](https://martinfowler.com/eaaCatalog/serviceLayer.html) - Capa de servicios
- [Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/) - Inyección de dependencias
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html) - Arquitectura limpia

### **Validación Avanzada**

- [Pydantic Custom Validators](https://docs.pydantic.dev/latest/concepts/validators/) - Validadores personalizados
- [Field Validation](https://docs.pydantic.dev/latest/concepts/field_validator/) - Validación de campos
- [Model Validation](https://docs.pydantic.dev/latest/concepts/model_validator/) - Validación de modelos
- [Custom Types](https://docs.pydantic.dev/latest/concepts/types/) - Tipos personalizados

---

## 🔧 Snippets de Código Útiles

### **Estructura Base de Endpoint**

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from typing import List, Optional

router = APIRouter()

@router.get(
    "/",
    response_model=List[ItemResponse],
    summary="Listar items",
    description="Obtiene una lista paginada de items con filtros opcionales"
)
async def list_items(
    # Query parameters
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Items por página"),
    search: Optional[str] = Query(None, min_length=2, description="Término de búsqueda"),

    # Dependency injection
    service: ItemService = Depends(get_item_service)
) -> List[ItemResponse]:
    """Listar items con paginación y filtros"""
    return await service.list_items(page, page_size, search)
```

### **Validador Custom Típico**

```python
from pydantic import BaseModel, Field, validator
import re

class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    sku: str = Field(..., min_length=6, max_length=20)
    price: float = Field(..., gt=0)

    @validator('name')
    def validate_name(cls, v):
        # Limpiar espacios y capitalizar
        v = ' '.join(v.split()).title()

        # Validaciones específicas
        if v.isdigit():
            raise ValueError('El nombre no puede ser solo números')

        forbidden_chars = ['<', '>', '"', "'"]
        if any(char in v for char in forbidden_chars):
            raise ValueError(f'El nombre no puede contener: {", ".join(forbidden_chars)}')

        return v

    @validator('sku')
    def validate_sku(cls, v):
        pattern = r'^[A-Z]{3}-\d{4}-[A-Z]{2}$'
        v = v.upper().strip()

        if not re.match(pattern, v):
            raise ValueError('SKU debe tener formato ABC-1234-XY')

        return v
```

### **Exception Handler Básico**

```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path),
            "method": request.method
        }
    )
```

### **Service Layer Pattern**

```python
from typing import List, Optional
from repositories.item_repository import ItemRepository
from schemas.item import ItemCreate, ItemUpdate, ItemResponse

class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    async def create_item(self, item_data: ItemCreate) -> ItemResponse:
        # Validaciones de negocio
        if await self.repository.exists_by_field("name", item_data.name):
            raise ConflictError("Item with this name already exists")

        # Crear item
        created_item = await self.repository.create(item_data.dict())
        return ItemResponse(**created_item)

    async def get_item(self, item_id: int) -> ItemResponse:
        item = await self.repository.get_by_id(item_id)
        if not item:
            raise NotFoundError(f"Item {item_id} not found")
        return ItemResponse(**item)
```

---

## 🧪 Templates de Testing

### **Testing con pytest**

```python
# conftest.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_product():
    return {
        "name": "Test Product",
        "sku": "TST-1234-XX",
        "price": 99.99,
        "category_id": 1
    }

# test_products.py
def test_create_product_success(client, sample_product):
    response = client.post("/api/v1/products", json=sample_product)
    assert response.status_code == 201
    assert response.json()["name"] == sample_product["name"]

def test_get_product_not_found(client):
    response = client.get("/api/v1/products/999")
    assert response.status_code == 404
    assert response.json()["error_code"] == "RESOURCE_NOT_FOUND"

def test_create_product_duplicate_sku(client, sample_product):
    # Crear primer producto
    client.post("/api/v1/products", json=sample_product)

    # Intentar crear con mismo SKU
    response = client.post("/api/v1/products", json=sample_product)
    assert response.status_code == 409
    assert "duplicate" in response.json()["message"].lower()
```

### **Collection de Postman**

```json
{
  "info": {
    "name": "FastAPI Inventory API",
    "description": "Collection para testing de API de inventario"
  },
  "item": [
    {
      "name": "Create Product",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"name\": \"Test Product\",\n  \"sku\": \"TST-1234-XX\",\n  \"price\": 99.99,\n  \"category_id\": 1\n}"
        },
        "url": {
          "raw": "{{base_url}}/api/v1/products",
          "host": ["{{base_url}}"],
          "path": ["api", "v1", "products"]
        }
      }
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:8000"
    }
  ]
}
```

---

## 📚 Recursos Adicionales

### **Blogs y Artículos**

- [Real Python - FastAPI Tutorial](https://realpython.com/fastapi-python-web-apis/) - Tutorial completo
- [TestDriven.io FastAPI](https://testdriven.io/blog/fastapi-crud/) - Series de FastAPI
- [FastAPI Tips and Tricks](https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-1-hello-world/) - Tutorial avanzado

### **Videos y Cursos**

- [FastAPI Official YouTube](https://www.youtube.com/c/tiangolo) - Canal oficial del creador
- [Python API Development](https://www.youtube.com/watch?v=0sOvCWFmrtA) - Curso completo gratuito
- [FastAPI Crash Course](https://www.youtube.com/watch?v=7t2alSnE2-I) - Introducción rápida

### **Libros y Referencias**

- [Building Python Web APIs with FastAPI](https://www.amazon.com/Building-Python-Web-APIs-FastAPI/dp/1801077540) - Libro completo
- [FastAPI Modern Python Web Development](https://www.amazon.com/FastAPI-Modern-Python-Web-Development/dp/1098135507) - Libro reciente
- [Effective Python](https://effectivepython.com/) - Mejores prácticas de Python

### **Comunidad y Soporte**

- [FastAPI GitHub Discussions](https://github.com/tiangolo/fastapi/discussions) - Discusiones oficiales
- [FastAPI Reddit](https://www.reddit.com/r/FastAPI/) - Comunidad Reddit
- [Stack Overflow](https://stackoverflow.com/questions/tagged/fastapi) - Preguntas y respuestas
- [Discord FastAPI](https://discord.gg/VQjSZaeJmf) - Chat en tiempo real

---

## 🔍 Debugging y Troubleshooting

### **Problemas Comunes**

#### **Error: "422 Unprocessable Entity"**

```python
# Problema: Validación Pydantic falla
# Solución: Verificar tipos de datos y validaciones

# ❌ Incorrecto
{"price": "99.99"}  # String en lugar de number

# ✅ Correcto
{"price": 99.99}    # Number
```

#### **Error: "404 Not Found" en endpoints**

```python
# Problema: Orden de rutas incorrecta
# ❌ Incorrecto
@router.get("/products/{product_id}")
@router.get("/products/stats")  # Nunca se alcanza

# ✅ Correcto
@router.get("/products/stats")   # Ruta específica primero
@router.get("/products/{product_id}")  # Ruta genérica después
```

#### **Error: "500 Internal Server Error"**

```python
# Problema: Exception no manejada
# Solución: Usar try-catch o exception handlers

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

### **Comandos de Diagnóstico**

```bash
# Verificar sintaxis Python
python -m py_compile app/main.py

# Verificar importaciones
python -c "from app.main import app; print('OK')"

# Ejecutar con logs detallados
uvicorn app.main:app --reload --log-level debug

# Verificar puertos ocupados
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

---

## 💡 Tips de Productividad

### **Shortcuts VS Code**

- `Ctrl+Shift+P`: Command palette
- `Ctrl+Click`: Ir a definición
- `F12`: Ir a definición
- `Shift+F12`: Encontrar referencias
- `Ctrl+.`: Quick fix/refactor
- `F2`: Rename symbol

### **Aliases Útiles**

```bash
# .bashrc o .zshrc
alias fapi="uvicorn app.main:app --reload"
alias fapitest="pytest tests/ -v"
alias fapilint="black app/ && isort app/ && flake8 app/"
```

### **Configuración Git**

```bash
# .gitignore para FastAPI
__pycache__/
*.py[cod]
*$py.class
.env
.venv/
venv/
logs/
.pytest_cache/
.coverage
htmlcov/
```

---

_Recursos compilados para Semana 3 - Bootcamp FastAPI_  
_Última actualización: 24 de julio de 2025_
