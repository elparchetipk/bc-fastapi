# Recursos de Apoyo - Semana 3

## 📚 Documentación y Referencias

### **FastAPI**

- [FastAPI Documentation](https://fastapi.tiangolo.com/) - Documentación oficial
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) - Tutorial paso a paso
- [Response Status Codes](https://fastapi.tiangolo.com/tutorial/response-status-code/) - Códigos de estado HTTP

### **Pydantic (Validación)**

- [Pydantic Documentation](https://docs.pydantic.dev/) - Documentación oficial
- [Field Validation](https://docs.pydantic.dev/latest/concepts/validators/) - Validadores básicos
- [Field Types](https://docs.pydantic.dev/latest/concepts/types/) - Tipos de campos

### **HTTP y REST**

- [HTTP Status Codes](https://httpstatuses.com/) - Referencia de códigos HTTP
- [REST API Basics](https://restfulapi.net/) - Principios básicos REST
- [HTTP Methods](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) - Métodos HTTP

## 🛠️ Herramientas de Desarrollo

### **Testing de APIs**

#### **Postman**

- [Postman Download](https://www.postman.com/downloads/) - Cliente para probar APIs
- [Postman Basics](https://learning.postman.com/docs/getting-started/introduction/) - Guía de inicio

#### **curl (Línea de comandos)**

```bash
# GET - Obtener datos
curl -X GET "http://localhost:8000/products"

# POST - Crear datos
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Producto Test", "price": 99.99}'

# PUT - Actualizar datos
curl -X PUT "http://localhost:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Producto Actualizado", "price": 129.99}'

# DELETE - Eliminar datos
curl -X DELETE "http://localhost:8000/products/1"
```

### **Editor Recomendado: VS Code**

```bash
# Extensiones útiles
code --install-extension ms-python.python
code --install-extension ms-python.pylint
code --install-extension humao.rest-client
```

### **Herramientas de Calidad**

```bash
# Instalar herramientas básicas
pip install black isort

# Formatear código
black app/

# Ordenar imports
isort app/
```

## 📖 Ejemplos de Código Útiles

### **Validador Pydantic Básico**

```python
from pydantic import BaseModel, Field, validator

class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    stock: int = Field(0, ge=0)

    @validator('name')
    def validate_name(cls, v):
        # Limpiar espacios y capitalizar
        return v.strip().title()

    @validator('price')
    def validate_price(cls, v):
        # Redondear a 2 decimales
        return round(v, 2)
```

### **Manejo Básico de Errores**

```python
from fastapi import HTTPException

# Función para manejar errores comunes
def product_not_found(product_id: int):
    raise HTTPException(
        status_code=404,
        detail=f"Producto con ID {product_id} no encontrado"
    )

# Uso en endpoint
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    product = database.get(product_id)
    if not product:
        product_not_found(product_id)
    return product
```

### **Filtros de Búsqueda Básicos**

```python
from typing import Optional
from fastapi import Query

@app.get("/products")
async def list_products(
    name: Optional[str] = Query(None, description="Filtrar por nombre"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    category_id: Optional[int] = Query(None, gt=0, description="ID de categoría")
):
    # Lógica de filtrado básica
    products = database.filter_products(
        name=name,
        min_price=min_price,
        max_price=max_price,
        category_id=category_id
    )
    return products
```

## 🧪 Testing Básico

### **Probar API con curl**

```bash
# 1. Listar productos
curl -X GET "http://localhost:8000/products"

# 2. Crear producto
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop HP", "price": 799.99, "category_id": 1}'

# 3. Obtener producto específico
curl -X GET "http://localhost:8000/products/1"

# 4. Buscar con filtros
curl -X GET "http://localhost:8000/products?min_price=100&max_price=500"

# 5. Eliminar producto
curl -X DELETE "http://localhost:8000/products/1"
```

### **Casos de Prueba Básicos**

```bash
# Probar validaciones
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "", "price": -10}'  # Debería dar error 422

# Probar producto no encontrado
curl -X GET "http://localhost:8000/products/999"  # Debería dar error 404
```

## 📚 Recursos Adicionales

### **Tutoriales Recomendados**

- [Real Python - FastAPI Tutorial](https://realpython.com/fastapi-python-web-apis/) - Tutorial completo
- [FastAPI Official Tutorial](https://fastapi.tiangolo.com/tutorial/) - Tutorial oficial paso a paso

### **Videos Útiles**

- [FastAPI Crash Course](https://www.youtube.com/watch?v=7t2alSnE2-I) - Introducción rápida
- [Python API Development](https://www.youtube.com/watch?v=0sOvCWFmrtA) - Curso básico

### **Comunidad y Ayuda**

- [FastAPI GitHub Discussions](https://github.com/tiangolo/fastapi/discussions) - Preguntas oficiales
- [Stack Overflow](https://stackoverflow.com/questions/tagged/fastapi) - Preguntas y respuestas

## 🔍 Problemas Comunes

### **Error 422: Unprocessable Entity**

```python
# Problema: Tipo de dato incorrecto
# ❌ Incorrecto
{"price": "99.99"}  # String en lugar de número

# ✅ Correcto
{"price": 99.99}    # Número
```

### **Error 404: Not Found**

```python
# Problema: Recurso no existe
# Verificar que el ID sea correcto y que el recurso exista en la base de datos
```

### **Error 500: Internal Server Error**

```python
# Problema: Error en el código
# Revisar logs del servidor para ver el error específico
uvicorn app.main:app --reload --log-level debug
```

## 💡 Consejos Útiles

### **Comandos Frecuentes**

```bash
# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload

# Verificar sintaxis
python -m py_compile app/main.py

# Formatear código
black app/
```

### **Organización del Código**

```text
app/
├── main.py          # Aplicación principal
├── models.py        # Modelos Pydantic
├── database.py      # Conexión a datos
└── routers/         # Rutas organizadas
    ├── products.py
    └── categories.py
```

---

_Recursos de Apoyo - Semana 3 - Bootcamp FastAPI - EPTI Development_
