# Week 3 Project: Simple Task API

## Objective

Build a complete CRUD API that manages tasks.

## Requirements

### Core Features

- Create, read, update, and delete tasks
- Basic error handling
- Simple task model

### Technical Specifications

#### Task Model

```python
class Task(BaseModel):
    title: str
    description: str = ""
    completed: bool = False
```

#### Required Endpoints

- `GET /tasks` - List all tasks
- `GET /tasks/{task_id}` - Get specific task
- `POST /tasks` - Create new task
- `PUT /tasks/{task_id}` - Update task
- `DELETE /tasks/{task_id}` - Delete task

### Implementation Guidelines

1. Use in-memory storage (simple list)
2. Add proper error handling (404, 400)
3. Include basic validation
4. Test all endpoints

### Deliverables

- Working API file (`main.py`)
- Test results (screenshots or documentation)
- Brief explanation of your implementation

### Evaluation Criteria

- All CRUD operations work correctly
- Proper error handling
- Clean, readable code
- Documentation of testing

**Time Limit:** 3 hours maximum
weight: Optional[float] = Field(None, gt=0, le=1000) # kg
dimensions: Optional[Dict[str, float]] = None # cm

    # Metadatos
    barcode: Optional[str] = Field(None, min_length=8, max_length=13)
    tags: Optional[List[str]] = Field(None, max_items=10)
    is_active: bool = Field(True)
    is_featured: bool = Field(False)

    # Validadores custom requeridos
    @validator('name')
    def validate_name(cls, v):
        # Capitalizar y limpiar espacios
        pass

    @validator('sku')
    def validate_sku_format(cls, v):
        # Validar formato específico
        pass

    @root_validator
    def validate_cost_vs_price(cls, values):
        # cost_price debe ser menor que price
        pass

````

#### **Categoría**

```python
class Category(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    parent_id: Optional[int] = Field(None, gt=0)  # Para subcategorías
    is_active: bool = Field(True)
````

#### **Proveedor**

```python
class Supplier(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    contact_email: str = Field(..., regex=r'^[^@]+@[^@]+\.[^@]+$')
    contact_phone: Optional[str] = Field(None, min_length=10, max_length=15)
    address: Optional[str] = Field(None, max_length=200)
    is_active: bool = Field(True)
```

### **2. Endpoints Obligatorios**

#### **Productos (Recurso Principal)**

| Método | Endpoint                | Descripción                  | Status Code   |
| ------ | ----------------------- | ---------------------------- | ------------- |
| GET    | `/api/v1/products`      | Listar productos con filtros | 200           |
| GET    | `/api/v1/products/{id}` | Obtener producto específico  | 200, 404      |
| POST   | `/api/v1/products`      | Crear nuevo producto         | 201, 422, 409 |
| PUT    | `/api/v1/products/{id}` | Actualizar producto completo | 200, 404, 422 |
| PATCH  | `/api/v1/products/{id}` | Actualización parcial        | 200, 404, 422 |
| DELETE | `/api/v1/products/{id}` | Eliminar producto            | 204, 404, 400 |

#### **Búsqueda y Filtros Avanzados**

```python
GET /api/v1/products?
    category_id=1&
    min_price=10.00&
    max_price=100.00&
    in_stock=true&
    brand=Apple&
    search=laptop&
    tags=gaming&
    is_featured=true&
    page=1&
    page_size=20&
    sort_by=price&
    sort_order=asc
```

#### **Endpoints Adicionales Obligatorios**

```python
# Estadísticas
GET /api/v1/products/stats
GET /api/v1/products/low-stock          # Productos con stock bajo
GET /api/v1/products/featured           # Productos destacados

# Operaciones especiales
POST /api/v1/products/{id}/stock        # Ajustar stock
POST /api/v1/products/bulk-update       # Actualización masiva

# Categorías (mínimo)
GET /api/v1/categories
POST /api/v1/categories
GET /api/v1/categories/{id}/products

# Proveedores (mínimo)
GET /api/v1/suppliers
POST /api/v1/suppliers

# Health check
GET /health
GET /health/detailed
```

### **3. Validaciones de Negocio Obligatorias**

#### **Reglas de Productos**

1. **SKU único**: No puede haber productos con el mismo SKU
2. **Nombre único por categoría**: Productos en la misma categoría no pueden tener el mismo nombre
3. **Stock coherente**: Si `stock_quantity = 0`, automáticamente debería marcar el producto como no disponible
4. **Precio vs costo**: `cost_price` debe ser menor que `price`
5. **Stock mínimo**: Si `stock_quantity < min_stock_level`, generar alerta
6. **Productos destacados**: Máximo 10 productos pueden ser destacados simultáneamente

#### **Reglas de Eliminación**

1. **Categorías con productos**: No se pueden eliminar categorías que tengan productos activos
2. **Proveedores con productos**: No se pueden eliminar proveedores con productos asociados
3. **Productos destacados**: Antes de eliminar, debe removerse el estado destacado

### **4. Sistema de Errores Obligatorio**

#### **Excepciones Custom Requeridas**

```python
class ProductNotFoundError(BaseAPIException)
class DuplicateSKUError(BaseAPIException)
class InvalidStockOperation(BaseAPIException)
class MaxFeaturedProductsExceeded(BaseAPIException)
class CategoryHasProductsError(BaseAPIException)
class SupplierHasProductsError(BaseAPIException)
```

#### **Responses de Error Consistentes**

```python
{
    "success": false,
    "error_code": "PRODUCT_NOT_FOUND",
    "message": "Producto con ID 123 no encontrado",
    "details": {
        "resource_type": "Product",
        "resource_id": 123,
        "suggestions": ["Verificar que el ID sea correcto"]
    },
    "timestamp": "2025-07-24T10:30:00.123456",
    "path": "/api/v1/products/123",
    "method": "GET"
}
```

## 📊 Datos de Prueba Requeridos

### **Categorías Iniciales**

```python
categories = [
    {"id": 1, "name": "Electrónicos", "description": "Dispositivos electrónicos"},
    {"id": 2, "name": "Ropa", "description": "Vestimenta y accesorios"},
    {"id": 3, "name": "Hogar", "description": "Artículos para el hogar"},
    {"id": 4, "name": "Deportes", "description": "Equipamiento deportivo"},
    {"id": 5, "name": "Libros", "description": "Literatura y textos educativos"}
]
```

### **Proveedores Iniciales**

```python
suppliers = [
    {"id": 1, "name": "Tech Distributor", "contact_email": "sales@techdist.com"},
    {"id": 2, "name": "Fashion Wholesale", "contact_email": "orders@fashionwh.com"},
    {"id": 3, "name": "Home & Living", "contact_email": "contact@homeliving.com"}
]
```

### **Productos de Ejemplo (Mínimo 15)**

```python
products = [
    {
        "name": "iPhone 15 Pro",
        "sku": "ELE-1001-AP",
        "price": 1199.99,
        "cost_price": 899.99,
        "stock_quantity": 25,
        "min_stock_level": 5,
        "category_id": 1,
        "supplier_id": 1,
        "brand": "Apple",
        "is_featured": True
    },
    {
        "name": "Camiseta Deportiva",
        "sku": "ROO-2001-NK",
        "price": 29.99,
        "cost_price": 15.00,
        "stock_quantity": 100,
        "min_stock_level": 20,
        "category_id": 2,
        "supplier_id": 2,
        "brand": "Nike"
    },
    # ... 13 productos más
]
```

## 🛠️ Arquitectura y Estructura

### **Estructura de Proyecto Obligatoria**

```text
inventory-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config/
│   │   ├── settings.py
│   │   └── database.py
│   ├── models/
│   │   ├── product.py
│   │   ├── category.py
│   │   └── supplier.py
│   ├── schemas/
│   │   ├── product.py
│   │   ├── category.py
│   │   └── supplier.py
│   ├── api/
│   │   └── v1/
│   │       ├── api.py
│   │       └── endpoints/
│   │           ├── products.py
│   │           ├── categories.py
│   │           └── suppliers.py
│   ├── core/
│   │   ├── exceptions.py
│   │   ├── handlers.py
│   │   └── logging.py
│   ├── services/
│   │   ├── product_service.py
│   │   ├── category_service.py
│   │   └── supplier_service.py
│   └── repositories/
│       ├── product_repository.py
│       ├── category_repository.py
│       └── supplier_repository.py
├── tests/
│   ├── test_products.py
│   ├── test_categories.py
│   └── conftest.py
├── requirements.txt
├── .env.example
└── README.md
```

### **Patrones de Diseño Obligatorios**

1. ✅ **Repository Pattern**: Para acceso a datos
2. ✅ **Service Layer**: Para lógica de negocio
3. ✅ **Dependency Injection**: Para manejo de dependencias
4. ✅ **Exception Handling**: Para manejo centralizado de errores
5. ✅ **Configuration Management**: Para settings centralizados

## 📋 Criterios de Entrega

### **Funcionalidades Mínimas (Obligatorias)**

- ✅ **15+ endpoints** funcionando correctamente
- ✅ **CRUD completo** para productos (mínimo)
- ✅ **Validación robusta** en todos los endpoints
- ✅ **Manejo de errores** profesional
- ✅ **Filtros y búsqueda** avanzados
- ✅ **Paginación** implementada
- ✅ **Datos de prueba** cargados automáticamente

### **Estructura y Calidad**

- ✅ **Arquitectura organizada** según especificación
- ✅ **Código limpio** y bien comentado
- ✅ **Documentación automática** FastAPI completa
- ✅ **README** con instrucciones claras
- ✅ **Requirements.txt** actualizado

### **Testing y Validación**

- ✅ **API ejecutable** con `uvicorn app.main:app --reload`
- ✅ **Documentación accesible** en `/docs`
- ✅ **Todos los endpoints** testeables con curl/Postman
- ✅ **Casos de error** manejados apropiadamente

## 🎯 Casos de Testing Obligatorios

### **Casos de Éxito**

```bash
# 1. Crear producto válido
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -d '{...producto válido...}'

# 2. Buscar productos con filtros
curl -X GET "http://localhost:8000/api/v1/products?category_id=1&min_price=100"

# 3. Obtener estadísticas
curl -X GET "http://localhost:8000/api/v1/products/stats"

# 4. Operación de stock
curl -X POST "http://localhost:8000/api/v1/products/1/stock" \
  -H "Content-Type: application/json" \
  -d '{"quantity": 10, "operation": "add"}'
```

### **Casos de Error (Obligatorios)**

```bash
# 1. Producto no encontrado
curl -X GET "http://localhost:8000/api/v1/products/999"

# 2. SKU duplicado
curl -X POST "http://localhost:8000/api/v1/products" \
  -d '{"sku": "ELE-1001-AP", ...}'  # SKU ya existe

# 3. Validación fallida
curl -X POST "http://localhost:8000/api/v1/products" \
  -d '{"price": -10, ...}'  # Precio inválido

# 4. Eliminar categoría con productos
curl -X DELETE "http://localhost:8000/api/v1/categories/1"
```

## 📊 Evaluación del Proyecto

| Criterio                 | Peso | Descripción                   |
| ------------------------ | ---- | ----------------------------- |
| **Funcionalidad CRUD**   | 25%  | Operaciones básicas completas |
| **Validación y Errores** | 25%  | Sistema robusto implementado  |
| **Estructura REST**      | 20%  | Arquitectura profesional      |
| **Filtros y Búsqueda**   | 15%  | Funcionalidades avanzadas     |
| **Documentación**        | 10%  | README y docs automáticas     |
| **Calidad del Código**   | 5%   | Organización y claridad       |

### **Escala de Calificación**

- **90-100**: Implementación completa y profesional
- **80-89**: Funcionalidad completa con mejoras menores
- **70-79**: Funcionalidad básica con algunas limitaciones
- **60-69**: Implementación parcial, necesita trabajo
- **< 60**: No cumple requisitos mínimos

## ⏰ Cronograma Sugerido

### **Día 1-2: Estructura y Modelos (2h)**

- Configurar proyecto base
- Crear modelos y schemas
- Implementar validaciones

### **Día 3-4: CRUD y Endpoints (2h)**

- Implementar repositories
- Crear services básicos
- Desarrollar endpoints principales

### **Día 5-6: Funcionalidades Avanzadas (1.5h)**

- Filtros y búsqueda
- Manejo de errores
- Operaciones especiales

### **Día 7: Testing y Documentación (0.5h)**

- Validar funcionalidad
- Completar README
- Testing final

## 📝 Entregables Finales

1. **Código fuente** completo en repositorio
2. **API funcionando** en puerto 8000
3. **README.md** con instrucciones completas
4. **Documentación** Swagger/ReDoc accesible
5. **Collection Postman** (opcional, bonus)

---

## 💡 Consejos para el Éxito

### **Gestión del Tiempo**

- ⏰ **Prioriza funcionalidad core** antes que características avanzadas
- 🔄 **Desarrolla incrementalmente** y prueba frecuentemente
- 📝 **Documenta mientras desarrollas**

### **Calidad del Código**

- 📖 **Sigue las prácticas** de las sesiones
- 🧪 **Prueba cada endpoint** antes de continuar
- 🔍 **Usa herramientas** de desarrollo (Postman, curl)

### **Antes de Entregar**

- ✅ **Ejecuta la API** desde cero
- ✅ **Verifica documentación** automática
- ✅ **Prueba casos de error** principales
- ✅ **README** con instrucciones claras

---

_Especificación del Proyecto - Semana 3_  
_Bootcamp FastAPI - EPTI Development_  
_Fecha límite: Final de Semana 3_
