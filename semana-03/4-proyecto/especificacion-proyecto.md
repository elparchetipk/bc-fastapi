# Proyecto Semana 3: API de Inventario Simple

## 🎯 Objetivo del Proyecto

Desarrollar una **API REST** que demuestre los conceptos aprendidos en la Semana 3: validación de datos, manejo de errores, y estructura REST básica.

## 📋 Especificaciones Funcionales

### **Entidades del Sistema:**

1. **Product**: Productos del inventario
2. **Category**: Categorías de productos

### **Funcionalidades Requeridas:**

- ✅ CRUD completo para productos
- ✅ Gestión básica de categorías
- ✅ Validación de datos con Pydantic
- ✅ Manejo básico de errores
- ✅ Filtros de búsqueda simple

## 🏗️ Especificación Técnica

### **1. Modelos Pydantic Requeridos**

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from enum import Enum

# Modelo para Categoría
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

# Modelo para Producto
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    price: float = Field(..., gt=0)
    stock: int = Field(0, ge=0)
    category_id: int = Field(..., gt=0)

    @validator('name')
    def validate_name(cls, v):
        return v.strip().title()

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = Field(None, gt=0)

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    category_name: Optional[str] = None
```

### **2. Endpoints Requeridos**

#### **Productos**

| Método | Endpoint         | Descripción         |
| ------ | ---------------- | ------------------- |
| GET    | `/products`      | Listar productos    |
| GET    | `/products/{id}` | Obtener producto    |
| POST   | `/products`      | Crear producto      |
| PUT    | `/products/{id}` | Actualizar producto |
| DELETE | `/products/{id}` | Eliminar producto   |

#### **Categorías**

| Método | Endpoint                    | Descripción             |
| ------ | --------------------------- | ----------------------- |
| GET    | `/categories`               | Listar categorías       |
| POST   | `/categories`               | Crear categoría         |
| GET    | `/categories/{id}/products` | Productos por categoría |

#### **Búsqueda y Filtros**

```python
GET /products?name=laptop&min_price=100&max_price=500&category_id=1
```

### **3. Validaciones Básicas**

#### **Reglas de Negocio**

1. **Nombre único**: No puede haber productos con el mismo nombre en la misma categoría
2. **Stock válido**: El stock no puede ser negativo
3. **Precio válido**: El precio debe ser mayor que 0
4. **Categoría válida**: El producto debe tener una categoría existente

### **4. Manejo de Errores**

#### **Excepciones Custom**

```python
class ProductNotFound(HTTPException):
    def __init__(self, product_id: int):
        super().__init__(
            status_code=404,
            detail=f"Producto con ID {product_id} no encontrado"
        )

class CategoryNotFound(HTTPException):
    def __init__(self, category_id: int):
        super().__init__(
            status_code=404,
            detail=f"Categoría con ID {category_id} no encontrada"
        )
```

## 📊 Datos de Ejemplo

### **Categorías Iniciales**

```python
categories = [
    {"id": 1, "name": "Electrónicos", "description": "Dispositivos electrónicos"},
    {"id": 2, "name": "Ropa", "description": "Vestimenta y accesorios"},
    {"id": 3, "name": "Libros", "description": "Literatura y textos"},
]
```

### **Productos de Ejemplo**

```python
products = [
    {
        "id": 1,
        "name": "Laptop HP",
        "description": "Laptop para oficina",
        "price": 799.99,
        "stock": 10,
        "category_id": 1
    },
    {
        "id": 2,
        "name": "Camiseta Polo",
        "description": "Camiseta casual",
        "price": 25.99,
        "stock": 50,
        "category_id": 2
    }
]
```

## 🛠️ Estructura del Proyecto

### **Estructura Recomendada**

```text
inventory-api/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   └── routers/
│       ├── products.py
│       └── categories.py
├── requirements.txt
└── README.md
```

## 📋 Criterios de Entrega

### **Funcionalidades Mínimas**

- ✅ **CRUD completo** para productos
- ✅ **Gestión básica** de categorías
- ✅ **Validación** con Pydantic
- ✅ **Manejo de errores** básico
- ✅ **Filtros** de búsqueda simple

### **Requisitos Técnicos**

- ✅ **API ejecutable** con `uvicorn`
- ✅ **Documentación** automática en `/docs`
- ✅ **Código organizado** y limpio
- ✅ **README** con instrucciones

## 🎯 Casos de Prueba

### **Casos de Éxito**

```bash
# 1. Crear producto
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 799.99, "stock": 10, "category_id": 1}'

# 2. Buscar productos
curl -X GET "http://localhost:8000/products?min_price=100&max_price=500"

# 3. Obtener producto por ID
curl -X GET "http://localhost:8000/products/1"
```

### **Casos de Error**

```bash
# 1. Producto no encontrado
curl -X GET "http://localhost:8000/products/999"

# 2. Precio inválido
curl -X POST "http://localhost:8000/products" \
  -d '{"name": "Test", "price": -10, "category_id": 1}'
```

## 📊 Evaluación

| Criterio               | Peso | Descripción                   |
| ---------------------- | ---- | ----------------------------- |
| **Funcionalidad CRUD** | 40%  | Operaciones básicas completas |
| **Validación**         | 25%  | Validaciones con Pydantic     |
| **Manejo de Errores**  | 20%  | Excepciones básicas           |
| **Documentación**      | 15%  | README y docs automáticas     |

## ⏰ Tiempo Estimado

### Total: 4-6 horas

### **Día 1 (2-3h)**: Estructura y Modelos

- Configurar proyecto
- Crear modelos Pydantic
- Implementar endpoints básicos

### **Día 2 (2-3h)**: Validación y Errores

- Agregar validaciones
- Implementar manejo de errores
- Crear filtros básicos
- Testing y documentación

## 📝 Entregables

1. **Código fuente** completo
2. **API funcionando**
3. **README.md** con instrucciones
4. **Documentación** automática accesible

---

## 💡 Consejos

- ⏰ **Enfócate en lo básico** antes que en características avanzadas
- 🔄 **Prueba cada endpoint** mientras desarrollas
- 📝 **Documenta el proceso** en el README

---

_Proyecto Semana 3 - Bootcamp FastAPI - EPTI Development_
