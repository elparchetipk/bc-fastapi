# Week 4 Project: Advanced API with Search and Validation

## Objective

Build an enhanced API with search functionality, advanced validation, and file handling.

## Requirements

### Core Features

- Product API with search and filtering
- User management with validation
- File upload/download functionality
- Advanced query parameters

### Technical Specifications

#### Product Model with Validation

```python
from pydantic import BaseModel, Field
from typing import Optional

class Product(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: str = Field(..., max_length=500)
    price: float = Field(..., gt=0, le=999999)
    category: str = Field(..., min_length=1)
    in_stock: bool = True
    tags: Optional[list] = []
```

#### Required Endpoints

1. **Product Management**

   - `GET /products` - List with search/filter
   - `GET /products/{id}` - Get specific product
   - `POST /products` - Create with validation
   - `PUT /products/{id}` - Update with validation
   - `DELETE /products/{id}` - Delete product

2. **Search and Filtering**

   - `GET /products/search?category=electronics&min_price=100&max_price=500`
   - `GET /products/search?name=laptop&in_stock=true`

3. **User Management**

   - `POST /users` - Register with email validation
   - `GET /users/{id}` - Get user profile

4. **File Operations**
   - `POST /upload` - Upload product images
   - `GET /files` - List uploaded files

### Implementation Guidelines

1. Use in-memory storage (simple lists/dictionaries)
2. Implement comprehensive input validation
3. Add proper error handling for all endpoints
4. Include query parameter filtering
5. Test all functionality thoroughly

### Deliverables

- Complete API file (`main.py`)
- Sample data for testing
- Documentation of all endpoints
- Test results and examples

### Evaluation Criteria

- All endpoints work correctly (60%)
- Proper validation and error handling (25%)
- Search/filtering functionality (10%)
- Code quality and documentation (5%)

**Time Limit:** 3 hours maximum
│ │ ├── cart.py
│ │ ├── order.py
│ │ └── review.py
│ ├── schemas/
│ │ ├── **init**.py
│ │ ├── user.py
│ │ ├── category.py
│ │ ├── product.py
│ │ ├── cart.py
│ │ ├── order.py
│ │ └── review.py
│ ├── crud/
│ │ ├── **init**.py
│ │ ├── base.py
│ │ ├── user.py
│ │ ├── category.py
│ │ ├── product.py
│ │ ├── cart.py
│ │ ├── order.py
│ │ └── review.py
│ ├── api/
│ │ ├── **init**.py
│ │ ├── endpoints/
│ │ │ ├── users.py
│ │ │ ├── categories.py
│ │ │ ├── products.py
│ │ │ ├── cart.py
│ │ │ ├── orders.py
│ │ │ ├── reviews.py
│ │ │ └── reports.py
│ │ └── api.py # Router principal
│ └── core/
│ ├── **init**.py
│ ├── config.py
│ └── security.py # Hash de passwords
├── alembic/
│ ├── versions/
│ ├── env.py
│ └── script.py.mako
├── tests/
│ ├── **init**.py
│ ├── conftest.py
│ ├── test_users.py
│ ├── test_products.py
│ ├── test_orders.py
│ ├── test_cart.py
│ └── test_integration.py
├── scripts/
│ ├── init_db.py
│ ├── seed_data.py
│ └── migrate.py
├── alembic.ini
├── requirements.txt
├── README.md
└── .env.example

````

### Modelo de Datos

#### Entidades Principales

1. **User** (Usuario)

   - id, username, email, hashed_password
   - full_name, phone, is_active
   - created_at, updated_at

2. **Category** (Categoría)

   - id, name, description, slug
   - is_active, created_at

3. **Product** (Producto)

   - id, name, description, sku
   - price, cost, stock, is_active
   - category_id (FK), created_at, updated_at

4. **Cart** (Carrito)

   - id, user_id (FK), created_at, updated_at

5. **CartItem** (Item del Carrito)

   - id, cart_id (FK), product_id (FK)
   - quantity, unit_price, created_at

6. **Order** (Orden)

   - id, order_number, user_id (FK)
   - total_amount, status, shipping_address
   - created_at, updated_at

7. **OrderItem** (Item de Orden)

   - id, order_id (FK), product_id (FK)
   - quantity, unit_price, subtotal

8. **Review** (Reseña)
   - id, user_id (FK), product_id (FK)
   - rating, comment, is_verified
   - created_at, updated_at

#### Relaciones

- User 1:1 Cart (un usuario, un carrito activo)
- User 1:N Orders (un usuario, muchas órdenes)
- User 1:N Reviews (un usuario, muchas reseñas)
- Category 1:N Products (una categoría, muchos productos)
- Cart 1:N CartItems (un carrito, muchos items)
- Order 1:N OrderItems (una orden, muchos items)
- Product 1:N CartItems (un producto en muchos carritos)
- Product 1:N OrderItems (un producto en muchas órdenes)
- Product 1:N Reviews (un producto, muchas reseñas)

---

## 🎯 Funcionalidades Requeridas

### Módulo de Usuarios

#### Endpoints Mínimos

```python
POST   /api/v1/users/                    # Crear usuario
GET    /api/v1/users/                    # Listar usuarios
GET    /api/v1/users/{user_id}           # Obtener usuario
PUT    /api/v1/users/{user_id}           # Actualizar usuario
DELETE /api/v1/users/{user_id}           # Eliminar usuario
POST   /api/v1/users/login               # Login (retorna token simple)
````

#### Validaciones

- Email único y válido
- Username único, 3-20 caracteres
- Password mínimo 8 caracteres
- Teléfono formato válido (opcional)

### Módulo de Categorías

#### Endpoints Mínimos

```python
POST   /api/v1/categories/               # Crear categoría
GET    /api/v1/categories/               # Listar categorías
GET    /api/v1/categories/{category_id}  # Obtener categoría
PUT    /api/v1/categories/{category_id}  # Actualizar categoría
DELETE /api/v1/categories/{category_id}  # Eliminar categoría
GET    /api/v1/categories/{category_id}/products  # Productos de categoría
```

#### Validaciones

- Nombre único
- Slug generado automáticamente
- No eliminar categoría con productos activos

### Módulo de Productos

#### Endpoints Mínimos

```python
POST   /api/v1/products/                 # Crear producto
GET    /api/v1/products/                 # Listar productos (con filtros)
GET    /api/v1/products/{product_id}     # Obtener producto
PUT    /api/v1/products/{product_id}     # Actualizar producto
DELETE /api/v1/products/{product_id}     # Eliminar producto
GET    /api/v1/products/search           # Búsqueda avanzada
```

#### Filtros de Búsqueda

- Por nombre/descripción
- Por categoría
- Por rango de precio
- Por disponibilidad (stock > 0)
- Ordenamiento (precio, nombre, fecha)
- Paginación

#### Validaciones

- SKU único
- Precio > 0
- Stock >= 0
- Categoría debe existir

### Módulo de Carrito

#### Endpoints Mínimos

```python
GET    /api/v1/cart/                     # Obtener carrito actual
POST   /api/v1/cart/items                # Agregar item al carrito
PUT    /api/v1/cart/items/{item_id}      # Actualizar cantidad
DELETE /api/v1/cart/items/{item_id}      # Remover item
DELETE /api/v1/cart/                     # Vaciar carrito
```

#### Lógica de Negocio

- Un usuario solo puede tener un carrito activo
- Verificar stock disponible al agregar items
- Calcular total automáticamente
- Precio unitario se toma del producto al momento de agregar

### Módulo de Órdenes

#### Endpoints Mínimos

```python
POST   /api/v1/orders/                   # Crear orden desde carrito
GET    /api/v1/orders/                   # Listar órdenes del usuario
GET    /api/v1/orders/{order_id}         # Obtener orden específica
PUT    /api/v1/orders/{order_id}/status  # Actualizar estado orden
```

#### Estados de Orden

- `pending` - Pendiente
- `confirmed` - Confirmada
- `shipped` - Enviada
- `delivered` - Entregada
- `cancelled` - Cancelada

#### Lógica de Negocio

- Generar número de orden único
- Reducir stock de productos al confirmar
- No permitir cancelar órdenes enviadas
- Vaciar carrito al crear orden exitosa

### Módulo de Reseñas

#### Endpoints Mínimos

```python
POST   /api/v1/reviews/                  # Crear reseña
GET    /api/v1/reviews/                  # Listar reseñas
GET    /api/v1/products/{product_id}/reviews  # Reseñas de producto
PUT    /api/v1/reviews/{review_id}       # Actualizar reseña
DELETE /api/v1/reviews/{review_id}       # Eliminar reseña
```

#### Validaciones

- Usuario solo puede reseñar un producto una vez
- Rating entre 1-5 estrellas
- Comentario máximo 1000 caracteres
- Solo el autor puede modificar su reseña

### Módulo de Reportes

#### Endpoints Mínimos

```python
GET    /api/v1/reports/sales             # Reporte de ventas
GET    /api/v1/reports/products/popular  # Productos más vendidos
GET    /api/v1/reports/categories/stats  # Estadísticas por categoría
GET    /api/v1/reports/users/stats       # Estadísticas de usuarios
```

---

## 🧪 Testing Requerido

### Cobertura Mínima

- **Coverage general:** > 80%
- **Tests unitarios:** CRUD operations
- **Tests de integración:** Endpoints principales
- **Tests de validación:** Reglas de negocio

### Casos de Prueba Críticos

1. **Creación de orden completa:**

   - Agregar productos al carrito
   - Verificar cálculos
   - Crear orden
   - Verificar reducción de stock

2. **Validaciones de negocio:**

   - Stock insuficiente
   - Duplicación de reseñas
   - Eliminación con restricciones

3. **Consultas complejas:**
   - Búsqueda con múltiples filtros
   - Reportes con agregaciones
   - Relaciones correctas

---

## 📊 Datos de Prueba

### Script de Inicialización

Crear `scripts/seed_data.py`:

```python
def create_sample_data():
    """Crear datos de prueba para el sistema"""

    # Categorías
    categories = [
        {"name": "Electronics", "description": "Electronic devices"},
        {"name": "Clothing", "description": "Fashion and apparel"},
        {"name": "Books", "description": "Books and literature"},
        {"name": "Home & Garden", "description": "Home improvement"},
    ]

    # Productos (mínimo 20)
    products = [
        # Electronics
        {"name": "Laptop Pro", "price": 1299.99, "stock": 15, "category": "Electronics"},
        {"name": "Smartphone X", "price": 699.99, "stock": 25, "category": "Electronics"},
        {"name": "Wireless Headphones", "price": 199.99, "stock": 50, "category": "Electronics"},
        # ... más productos
    ]

    # Usuarios (mínimo 5)
    users = [
        {"username": "johndoe", "email": "john@example.com", "full_name": "John Doe"},
        {"username": "janedoe", "email": "jane@example.com", "full_name": "Jane Doe"},
        # ... más usuarios
    ]
```

---

## 🎯 Entregables

### 1. Código Fuente

- [ ] Estructura de proyecto completa
- [ ] Todos los modelos implementados
- [ ] CRUD completo para todas las entidades
- [ ] Endpoints funcionales con validaciones
- [ ] Manejo de errores apropiado

### 2. Base de Datos

- [ ] Migraciones de Alembic funcionando
- [ ] Esquema de BD correctamente definido
- [ ] Relaciones implementadas correctamente
- [ ] Datos de prueba cargados

### 3. Testing

- [ ] Suite de tests completa
- [ ] Coverage > 80%
- [ ] Tests de integración funcionando
- [ ] Casos edge cubiertos

### 4. Documentación

- [ ] README.md con instrucciones de instalación
- [ ] Documentación de API (automática con FastAPI)
- [ ] Comentarios en código complejo
- [ ] Archivo de configuración de ejemplo

### 5. Scripts y Utilidades

- [ ] Script de inicialización de BD
- [ ] Script de datos de prueba
- [ ] Script de migraciones
- [ ] Archivo de dependencias actualizado

---

## 📏 Criterios de Evaluación

### Funcionalidad (40%)

| Aspecto           | Puntos | Criterios                                   |
| ----------------- | ------ | ------------------------------------------- |
| **CRUD Completo** | 15     | Todas las operaciones funcionando           |
| **Relaciones BD** | 15     | Relaciones correctas y consultas eficientes |
| **Validaciones**  | 10     | Reglas de negocio implementadas             |

### Calidad de Código (30%)

| Aspecto               | Puntos | Criterios                                |
| --------------------- | ------ | ---------------------------------------- |
| **Estructura**        | 10     | Organización clara y consistente         |
| **Buenas Prácticas**  | 10     | PEP 8, naming conventions, DRY           |
| **Manejo de Errores** | 10     | Excepciones apropiadas y mensajes claros |

### Testing (20%)

| Aspecto              | Puntos | Criterios                               |
| -------------------- | ------ | --------------------------------------- |
| **Cobertura**        | 10     | Coverage > 80%                          |
| **Calidad de Tests** | 10     | Casos relevantes y assertions correctas |

### Documentación (10%)

| Aspecto         | Puntos | Criterios                                 |
| --------------- | ------ | ----------------------------------------- |
| **README**      | 5      | Instrucciones claras de instalación y uso |
| **Comentarios** | 5      | Código documentado apropiadamente         |

---

## 🚀 Instrucciones de Entrega

### Formato de Entrega

1. **Repositorio GitHub:**

   - Crear repositorio público: `bc-fastapi-semana4-[tu-nombre]`
   - Incluir todos los archivos del proyecto
   - README.md completo con instrucciones

2. **Estructura del Commit:**

   ```bash
   git add .
   git commit -m "feat: Proyecto final Semana 4 - API E-commerce completa"
   git push origin main
   ```

3. **Archivo de Entrega:**
   - Crear `ENTREGA.md` con:
     - Link al repositorio
     - Instrucciones de instalación
     - Comandos para ejecutar tests
     - Decisiones de diseño importantes

### Fecha Límite

**📅 Entrega:** Domingo 23:59 de la Semana 4

### Presentación (Opcional)

**📺 Demo de 5 minutos** mostrando:

- Funcionalidad principal
- Tests ejecutándose
- Consulta compleja funcionando

---

## 🆘 Recursos de Apoyo

### Documentación Oficial

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Pydantic v2](https://docs.pydantic.dev/latest/)
- [pytest Documentation](https://docs.pytest.org/)

### Ejemplos de Referencia

- Prácticas de la Semana 4
- [FastAPI SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Testing FastAPI](https://fastapi.tiangolo.com/tutorial/testing/)

### Ayuda y Soporte

- **Foro del curso:** Para preguntas técnicas
- **Office hours:** Martes y jueves 18:00-19:00
- **Slack del bootcamp:** Canal #semana-4

---

## 🏆 Proyecto Destacado

El mejor proyecto de la semana será:

- Presentado en la siguiente sesión
- Incluido como ejemplo de referencia
- Reconocido en el hall of fame del bootcamp

---

## 💡 Tips para el Éxito

1. **Planifica primero:** Diseña el modelo de datos antes de programar
2. **Desarrolla incrementalmente:** Una funcionalidad a la vez
3. **Prueba frecuentemente:** Ejecuta tests después de cada feature
4. **Documenta mientras codificas:** No dejes la documentación para el final
5. **Usa Git apropiadamente:** Commits frecuentes con mensajes descriptivos

---

¡Demuestra todo lo que has aprendido en esta semana y crea una API robusta y profesional! 🚀
