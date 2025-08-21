# Proyecto Semana 3: API de Productos con Validaciones

## 🎯 Objetivo del Proyecto

Desarrollar una **API REST simple** que demuestre los conceptos aprendidos en la Semana 3: validación de datos con Pydantic, manejo básico de errores, y organización de código.

## 📋 Especificaciones Funcionales

### **Entidad Principal:**

- **Product**: Gestión de productos de una tienda simple

### **Funcionalidades Requeridas:**

- ✅ CRUD básico para productos (5 endpoints)
- ✅ Validación de datos con Pydantic
- ✅ Manejo básico de errores con HTTPException
- ✅ Filtros simples por precio
- ✅ Organización básica del código

## 🏗️ Especificación Técnica

### **1. Modelo Pydantic Requerido**

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
from enum import Enum

class ProductStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    out_of_stock = "out_of_stock"

class ProductCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    home = "home"
    sports = "sports"
    other = "other"

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del producto")
    price: float = Field(..., gt=0, description="Precio debe ser mayor que 0")
    stock: int = Field(..., ge=0, description="Stock no puede ser negativo")
    category: ProductCategory = Field(default=ProductCategory.other)
    status: ProductStatus = Field(default=ProductStatus.active)

    @validator('name')
    def validate_name(cls, v):
        # Capitalizar y limpiar espacios
        cleaned = v.strip().title()
        if len(cleaned) < 2:
            raise ValueError('Nombre debe tener al menos 2 caracteres después de limpiar')
        return cleaned

    @validator('price')
    def validate_price(cls, v):
        # Redondear a 2 decimales
        return round(v, 2)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[ProductCategory] = None
    status: Optional[ProductStatus] = None

    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            cleaned = v.strip().title()
            if len(cleaned) < 2:
                raise ValueError('Nombre debe tener al menos 2 caracteres')
            return cleaned
        return v

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
```

### **2. Endpoints Requeridos (5 endpoints principales)**

#### **Productos CRUD**

```python
# CRUD básico (5 endpoints principales)
POST   /products                    # Crear producto
GET    /products                    # Listar productos
GET    /products/{product_id}       # Obtener producto específico
PUT    /products/{product_id}       # Actualizar producto completo
DELETE /products/{product_id}       # Eliminar producto

# Filtros simples (dentro del GET /products)
GET    /products?min_price=10&max_price=100&category=electronics&status=active
```

### **3. Validaciones y Manejo de Errores**

#### **Validaciones Automáticas con Pydantic**

- Nombre: mínimo 2 caracteres, máximo 100, se capitaliza automáticamente
- Precio: mayor que 0, se redondea a 2 decimales
- Stock: no negativo
- Descripción: máximo 500 caracteres

#### **Manejo de Errores Básico**

```python
from fastapi import HTTPException

# Funciones helper para errores comunes
def product_not_found(product_id: int):
    raise HTTPException(
        status_code=404,
        detail=f"Producto con ID {product_id} no encontrado"
    )

def validation_error(message: str):
    raise HTTPException(
        status_code=400,
        detail=message
    )

# Ejemplo de uso en endpoints
@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    if product_id not in products_db:
        product_not_found(product_id)
    return ProductResponse(**products_db[product_id])
```

### **4. Filtros Simples**

```python
from fastapi import Query

@app.get("/products", response_model=List[ProductResponse])
def get_products(
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    category: Optional[ProductCategory] = Query(None, description="Filtrar por categoría"),
    status: Optional[ProductStatus] = Query(None, description="Filtrar por estado"),
    limit: int = Query(20, ge=1, le=100, description="Límite de resultados")
):
    # Implementar lógica de filtrado simple
    pass
```

## 📊 Datos de Ejemplo

### **Productos Iniciales**

```python
sample_products = [
    {
        "id": 1,
        "name": "Laptop Gamer",
        "description": "Laptop para gaming con RTX 4060",
        "price": 899.99,
        "stock": 5,
        "category": "electronics",
        "status": "active"
    },
    {
        "id": 2,
        "name": "Camiseta Básica",
        "description": "Camiseta de algodón 100%",
        "price": 19.99,
        "stock": 25,
        "category": "clothing",
        "status": "active"
    },
    {
        "id": 3,
        "name": "Python Cookbook",
        "description": "Recetas de programación en Python",
        "price": 45.50,
        "stock": 0,
        "category": "books",
        "status": "out_of_stock"
    }
]
```

## 🛠️ Estructura Simplificada del Proyecto

### **Un solo archivo: main.py**

```python
# main.py - Todo en un archivo para simplificar
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

# ... modelos y lógica aquí ...

app = FastAPI(title="API de Productos - Semana 3")

# Base de datos en memoria
products_db: Dict[int, dict] = {}
next_id: int = 1

# ... endpoints aquí ...
```

## 📋 Criterios de Evaluación

### **Funcionalidades Mínimas (Total: 100 puntos)**

#### **Funcionalidad CRUD (40 puntos)**

- ✅ POST /products - Crear producto (10 pts)
- ✅ GET /products - Listar productos (10 pts)
- ✅ GET /products/{id} - Obtener producto (10 pts)
- ✅ PUT /products/{id} - Actualizar producto (10 pts)

#### **Validación con Pydantic (30 puntos)**

- ✅ Validaciones de campos con Field (10 pts)
- ✅ Validators personalizados (10 pts)
- ✅ Enums funcionando (10 pts)

#### **Manejo de Errores (20 puntos)**

- ✅ HTTPException para 404 (10 pts)
- ✅ Responses de error apropiados (10 pts)

#### **Filtros y Calidad (10 puntos)**

- ✅ Filtros básicos por precio (5 pts)
- ✅ Código limpio y organizado (5 pts)

## ⏰ Cronograma Realista (5.5 horas)

### **Paso 1: Setup y Modelos (90 min)**

- Crear estructura básica del proyecto
- Implementar modelos Pydantic con validaciones
- Probar modelos con datos de ejemplo

### **Paso 2: CRUD Básico (120 min)**

- POST /products - Crear producto
- GET /products - Listar productos
- GET /products/{id} - Obtener producto específico
- PUT /products/{id} - Actualizar producto

### **Paso 3: Manejo de Errores (60 min)**

- Implementar HTTPException para casos básicos
- Manejar errores de validación
- Probar casos de error

### **Paso 4: Filtros y Pulido (60 min)**

- Agregar filtros simples por precio y categoría
- Testing manual de todos los endpoints
- Documentación básica

### **Total: 5.5 horas (330 minutos)**

## 🎯 Casos de Prueba Básicos

### **Casos de Éxito**

```bash
# 1. Crear producto
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "laptop gaming",
    "description": "Laptop para juegos",
    "price": 899.99,
    "stock": 5,
    "category": "electronics"
  }'

# 2. Listar productos con filtros
curl "http://localhost:8000/products?min_price=100&max_price=500&category=electronics"

# 3. Obtener producto específico
curl "http://localhost:8000/products/1"

# 4. Actualizar producto
curl -X PUT "http://localhost:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop Gaming Pro",
    "price": 999.99,
    "stock": 3
  }'
```

### **Casos de Error**

```bash
# 1. Producto no encontrado
curl "http://localhost:8000/products/999"
# Esperado: 404 Not Found

# 2. Precio inválido
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "price": -10, "stock": 5}'
# Esperado: 422 Validation Error

# 3. Nombre muy corto
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{"name": "A", "price": 10, "stock": 5}'
# Esperado: 422 Validation Error
```

## 📝 Entregables

### **Archivos Requeridos:**

1. **`main.py`** - API principal con todos los endpoints
2. **`requirements.txt`** - Dependencias del proyecto
3. **`README.md`** - Documentación básica

### **README Ejemplo:**

```markdown
# API de Productos - Semana 3

## Descripción

API REST para gestión de productos con validaciones Pydantic.

## Instalación

\`\`\`bash
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

## Endpoints

- POST /products - Crear producto
- GET /products - Listar productos
- GET /products/{id} - Obtener producto
- PUT /products/{id} - Actualizar producto

## Validaciones Implementadas

- Nombre: se capitaliza automáticamente
- Precio: debe ser positivo, se redondea a 2 decimales
- Stock: no puede ser negativo
```

## 🎯 Consejos para el Éxito

1. **Empieza simple**: Implementa CRUD básico primero
2. **Prueba constantemente**: Usa /docs para verificar endpoints
3. **Validaciones graduales**: Agrega una validación a la vez
4. **Manejo de errores básico**: Solo 404 y 422 son suficientes
5. **Un archivo es suficiente**: No compliques la estructura

## 🏆 Oportunidades de Bonus

- **+5 puntos**: Endpoint DELETE /products/{id}
- **+5 puntos**: Filtro adicional por status
- **+5 puntos**: Contador de productos por categoría
- **+10 puntos**: Validación de nombre único (no duplicados)

---

**🎯 Objetivo**: Consolidar validaciones Pydantic y manejo básico de errores en un proyecto práctico y realista.
