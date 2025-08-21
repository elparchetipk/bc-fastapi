# Guía Rápida - Semana 3: Validaciones y Manejo de Errores

## 🎯 Objetivo

Construir sobre la semana 2 agregando **validaciones avanzadas** y **manejo de errores** básico.

## 🚀 Inicio Rápido (15 min)

### 1. Setup

```bash
# Usar el proyecto de la semana 2 como base
cp -r ../semana-02/mi-biblioteca-api ./mi-productos-api
cd mi-productos-api

# O crear nuevo proyecto
mkdir mi-productos-api && cd mi-productos-api
python -m venv venv
source venv/bin/activate
pip install fastapi uvicorn
```

### 2. Estructura Base

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, validator
from enum import Enum

app = FastAPI(title="API Productos - Semana 3")

class ProductStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    out_of_stock = "out_of_stock"

class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    status: ProductStatus = ProductStatus.active

    @validator('name')
    def validate_name(cls, v):
        return v.strip().title()  # Capitalizar automáticamente
```

## ✅ Checklist del Proyecto (5.5 horas)

### **Bloque 1: Modelos y Validaciones (90 min)**

- [ ] Crear enums para Status y Category
- [ ] Implementar modelo Product con Field constraints
- [ ] Agregar validators personalizados (@validator)
- [ ] Probar validaciones con datos incorrectos

### **Bloque 2: CRUD con Errores (120 min)**

- [ ] POST /products - con validación de duplicados
- [ ] GET /products - con filtros básicos
- [ ] GET /products/{id} - con HTTPException 404
- [ ] PUT /products/{id} - con validación y 404

### **Bloque 3: Filtros y Manejo de Errores (60 min)**

- [ ] Filtros por precio (min_price, max_price)
- [ ] Filtros por categoría y status
- [ ] HTTPException personalizada para errores
- [ ] Validaciones de lógica de negocio

### **Bloque 4: Testing y Pulido (60 min)**

- [ ] Probar todos los endpoints
- [ ] Verificar manejo de errores
- [ ] Documentar en README
- [ ] Preparar entrega

## 🔧 Conceptos Clave a Implementar

### **1. Validaciones Pydantic**

```python
class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0, description="Precio mayor que 0")

    @validator('name')
    def name_must_be_clean(cls, v):
        cleaned = v.strip().title()
        if len(cleaned) < 2:
            raise ValueError('Nombre muy corto después de limpiar')
        return cleaned

    @validator('price')
    def price_two_decimals(cls, v):
        return round(v, 2)
```

### **2. Manejo de Errores**

```python
from fastapi import HTTPException

def product_not_found(product_id: int):
    raise HTTPException(
        status_code=404,
        detail=f"Producto {product_id} no encontrado"
    )

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products_db:
        product_not_found(product_id)
    return products_db[product_id]
```

### **3. Filtros con Query Parameters**

```python
from fastapi import Query

@app.get("/products")
def get_products(
    min_price: float = Query(None, ge=0),
    max_price: float = Query(None, ge=0),
    category: ProductCategory = Query(None)
):
    # Lógica de filtrado
    pass
```

## 🎯 Puntos de Evaluación

| Concepto                  | Peso | Qué evaluar                   |
| ------------------------- | ---- | ----------------------------- |
| **Validaciones Pydantic** | 30%  | Field constraints, @validator |
| **Manejo de Errores**     | 20%  | HTTPException 404, 422        |
| **CRUD Funcional**        | 40%  | 4-5 endpoints trabajando      |
| **Filtros**               | 10%  | Query parameters básicos      |

## ⚠️ Errores Comunes a Evitar

1. **Validaciones muy complejas** - Mantén simple
2. **Muchos endpoints** - Enfócate en calidad, no cantidad
3. **Estructura compleja** - Un archivo main.py es suficiente
4. **Sobre-ingeniería** - Validaciones básicas son suficientes

## 🏆 Bonus (Opcional)

- **+5 pts**: DELETE endpoint
- **+5 pts**: Validación de nombres únicos
- **+5 pts**: Endpoint de estadísticas básicas
- **+10 pts**: Filtros adicionales

## 🔗 Recursos

- [Pydantic Validators](https://pydantic-docs.helpmanual.io/usage/validators/)
- [FastAPI Error Handling](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- Archivo `ejemplo_main.py` en este directorio

---

**💡 Recuerda**: Esta semana se trata de **calidad** en validaciones y manejo de errores, no de cantidad de features.
