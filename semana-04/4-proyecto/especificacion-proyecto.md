# Proyecto Final Semana 4: API de Biblioteca con Base de Datos

## 🎯 Objetivo del Proyecto

Crear una API REST para un sistema de gestión de biblioteca que integre los conceptos fundamentales de la Semana 4: bases de datos, relaciones básicas, CRUD y testing.

**⏱️ Tiempo estimado:** 5.5 horas  
**📅 Fecha de entrega:** Final de la Semana 4  
**🏆 Peso en la evaluación:** 40% de la calificación semanal

---

## 📋 Descripción del Proyecto

### Contexto del Negocio

Desarrollar el backend para un sistema de biblioteca que permita:

- Gestión de libros (CRUD completo)
- Registro de usuarios de la biblioteca
- Sistema de préstamos y devoluciones
- Consultas básicas con relaciones entre entidades
- Validaciones de reglas de negocio simples

### Tecnologías Requeridas

- **Framework:** FastAPI
- **Base de Datos:** SQLite con SQLAlchemy ORM
- **Testing:** pytest básico
- **Validación:** Pydantic v2

---

## 🏗️ Arquitectura del Sistema

### Estructura del Proyecto (Simplificada)

```text
library_api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Aplicación principal
│   ├── database.py             # Configuración BD
│   ├── models.py               # Todos los modelos SQLAlchemy
│   ├── schemas.py              # Todos los schemas Pydantic
│   ├── crud.py                 # Operaciones CRUD
│   └── dependencies.py         # Dependencias compartidas
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_books.py
│   ├── test_users.py
│   └── test_loans.py
├── requirements.txt
├── README.md
└── .env.example
```

### Modelo de Datos (Simplificado)

#### Entidades Principales

1. **Book** (Libro)

   - id (Primary Key)
   - title (string, required)
   - author (string, required)
   - isbn (string, unique, optional)
   - publication_year (integer, optional)
   - is_available (boolean, default=True)
   - created_at (datetime)

2. **User** (Usuario)

   - id (Primary Key)
   - name (string, required)
   - email (string, unique, required)
   - phone (string, optional)
   - is_active (boolean, default=True)
   - created_at (datetime)

3. **Loan** (Préstamo)
   - id (Primary Key)
   - user_id (Foreign Key → User)
   - book_id (Foreign Key → Book)
   - loan_date (datetime, required)
   - return_date (datetime, optional)
   - is_returned (boolean, default=False)
   - created_at (datetime)

#### Relaciones Simples

- User 1:N Loans (un usuario puede tener múltiples préstamos)
- Book 1:N Loans (un libro puede ser prestado múltiples veces)
- Constraint: Un libro solo puede ser prestado si está disponible

---

## 🎯 Funcionalidades Requeridas

### Módulo de Libros

#### Endpoints Mínimos

```python
POST   /api/v1/books/                    # Crear libro
GET    /api/v1/books/                    # Listar libros (con paginación)
GET    /api/v1/books/{book_id}           # Obtener libro por ID
PUT    /api/v1/books/{book_id}           # Actualizar libro
DELETE /api/v1/books/{book_id}           # Eliminar libro
GET    /api/v1/books/search/{title}      # Buscar por título
```

#### Validaciones

- Título requerido (máximo 200 caracteres)
- Autor requerido (máximo 100 caracteres)
- ISBN único si se proporciona (formato básico)
- Año de publicación debe ser razonable (1500-2025)

### Módulo de Usuarios

#### Endpoints Mínimos

```python
POST   /api/v1/users/                    # Crear usuario
GET    /api/v1/users/                    # Listar usuarios
GET    /api/v1/users/{user_id}           # Obtener usuario por ID
PUT    /api/v1/users/{user_id}           # Actualizar usuario
DELETE /api/v1/users/{user_id}           # Eliminar usuario (solo si no tiene préstamos activos)
```

#### Validaciones

- Email único y válido
- Nombre requerido (máximo 100 caracteres)
- No se puede eliminar usuario con préstamos activos

### Módulo de Préstamos

#### Endpoints Mínimos

```python
POST   /api/v1/loans/                    # Crear préstamo
GET    /api/v1/loans/                    # Listar préstamos
GET    /api/v1/loans/{loan_id}           # Obtener préstamo por ID
PUT    /api/v1/loans/{loan_id}/return    # Marcar préstamo como devuelto
GET    /api/v1/loans/user/{user_id}      # Préstamos de un usuario
GET    /api/v1/loans/book/{book_id}      # Historial de préstamos de un libro
GET    /api/v1/loans/active             # Préstamos activos
```

#### Reglas de Negocio

- Solo se puede prestar un libro si está disponible (`is_available = True`)
- Al crear un préstamo, el libro debe marcarse como no disponible
- Al devolver un libro, debe marcarse como disponible nuevamente
- Un usuario no puede tener más de 3 préstamos activos simultáneamente

### Endpoints de Consultas

#### Reportes Básicos

```python
GET    /api/v1/stats/books              # Estadísticas de libros
GET    /api/v1/stats/users              # Estadísticas de usuarios
GET    /api/v1/stats/loans              # Estadísticas de préstamos
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

- **Coverage general:** > 60%
- **Tests unitarios:** CRUD operations básicas
- **Tests de validación:** Reglas de negocio principales

### Casos de Prueba Básicos

1. **CRUD de Libros:**

   - Crear, leer, actualizar, eliminar libros
   - Validaciones de campos requeridos

2. **CRUD de Usuarios:**

   - Crear, leer, actualizar, eliminar usuarios
   - Validación de email único

3. **Sistema de Préstamos:**

   - Crear préstamo (libro disponible)
   - Rechazar préstamo (libro no disponible)
   - Devolver libro y marcar como disponible

4. **Validaciones de Negocio:**
   - Máximo 3 préstamos por usuario
   - No eliminar usuario con préstamos activos

---

## ⏱️ Cronograma Detallado (5.5 horas)

### Sesión 1: Setup y Modelos (90 minutos)

- **[0-30 min]** Configuración inicial del proyecto
- **[30-60 min]** Modelos SQLAlchemy básicos (Book, User, Loan)
- **[60-90 min]** Configuración de base de datos y conexión

### Sesión 2: CRUD Básico (90 minutos)

- **[90-120 min]** CRUD completo para libros
- **[120-150 min]** CRUD completo para usuarios
- **[150-180 min]** Testing básico de CRUD

### Sesión 3: Sistema de Préstamos (90 minutos)

- **[180-210 min]** Modelos y endpoints de préstamos
- **[210-240 min]** Lógica de negocio (disponibilidad)
- **[240-270 min]** Validaciones y reglas

### Sesión 4: Testing y Finalización (90 minutos)

- **[270-300 min]** Tests de integración
- **[300-320 min]** Documentación y README
- **[320-330 min]** Buffer y ajustes finales

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

---

## 📋 Entregables

### Código Requerido

- [ ] **Archivo principal:** `app/main.py`
- [ ] **Modelos:** `app/models.py` con las 3 entidades
- [ ] **Schemas:** `app/schemas.py` con validaciones Pydantic
- [ ] **CRUD:** `app/crud.py` con operaciones básicas
- [ ] **Base de datos:** `app/database.py` con configuración SQLAlchemy
- [ ] **Dependencias:** `requirements.txt` actualizado

### Testing

- [ ] **Tests básicos:** Al menos 10 tests que pasen
- [ ] **Test CRUD:** Para cada entidad (libros, usuarios, préstamos)
- [ ] **Test validaciones:** Reglas de negocio principales
- [ ] **Coverage:** Mínimo 60%

### Documentación

- [ ] **README.md** con instrucciones de instalación y uso
- [ ] **Comentarios** en funciones complejas
- [ ] **Documentación automática** de FastAPI funcionando

---

## 📏 Criterios de Evaluación (Simplificados)

### Funcionalidad (50%)

| Aspecto               | Puntos | Criterios                              |
| --------------------- | ------ | -------------------------------------- |
| **CRUD Libros**       | 15     | Create, Read, Update, Delete funcional |
| **CRUD Usuarios**     | 15     | Create, Read, Update, Delete funcional |
| **Sistema Préstamos** | 20     | Lógica de préstamo/devolución correcta |

### Calidad de Código (30%)

| Aspecto              | Puntos | Criterios                            |
| -------------------- | ------ | ------------------------------------ |
| **Estructura**       | 15     | Archivos organizados según plantilla |
| **Buenas Prácticas** | 15     | Código limpio, nombres descriptivos  |

### Testing (20%)

| Aspecto           | Puntos | Criterios                                 |
| ----------------- | ------ | ----------------------------------------- |
| **Tests Básicos** | 20     | Al menos 10 tests que pasen correctamente |

---

## 📚 Recursos de Apoyo

### Documentación Oficial

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [pytest Getting Started](https://docs.pytest.org/en/stable/getting-started.html)

### Ejemplos de Referencia

- Prácticas de la Semana 4
- [FastAPI SQL Databases Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- Semanas anteriores del bootcamp (1-3)

---

## 💡 Tips para el Éxito

1. **Sigue el cronograma:** 90 minutos por sesión, respeta los tiempos
2. **Desarrolla incrementalmente:** Una entidad completa antes de seguir
3. **Prueba frecuentemente:** Usa la documentación automática de FastAPI
4. **Simplifica:** Enfócate en que funcione, no en optimizaciones
5. **Usa los ejemplos:** Basate en las prácticas de la semana

---

## 🎯 Funcionalidades Mínimas vs Opcionales

### ✅ **Mínimo Viable (Para aprobar)**

- CRUD completo de libros y usuarios
- Sistema básico de préstamos
- Al menos 8 tests que pasen
- README con instrucciones

### 🌟 **Extensiones Opcionales (Bonus)**

- [ ] Búsqueda avanzada de libros
- [ ] Estadísticas y reportes
- [ ] Validaciones adicionales (ISBN, fechas)
- [ ] API de renovación de préstamos
- [ ] Sistema de multas por retraso

---

¡Enfócate en completar el MVP primero, luego agrega las extensiones si tienes tiempo! 🚀
| --------------- | ------ | ----------------------------------------- |
| **README** | 5 | Instrucciones claras de instalación y uso |
| **Comentarios** | 5 | Código documentado apropiadamente |

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
