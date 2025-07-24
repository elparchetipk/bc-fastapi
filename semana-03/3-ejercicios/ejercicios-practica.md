# Ejercicios - Semana 3: FastAPI Intermedio

## 🎯 Objetivo

Reforzar los conceptos de FastAPI intermedio con ejercicios prácticos que complementan las prácticas principales de la semana.

---

## 📋 Ejercicio 1: Endpoints HTTP Básicos (20 min)

### **Contexto**

Crear una mini-API para gestionar una biblioteca de libros aplicando los conceptos REST.

### **Instrucciones**

Implementa los siguientes endpoints:

```python
# Modelo básico
class Book(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: str = Field(..., regex=r'^\d{3}-\d{10}$')
    pages: int = Field(..., gt=0, le=10000)
    published_year: int = Field(..., ge=1500, le=2025)
    genre: str = Field(..., min_length=1, max_length=50)
    is_available: bool = Field(True)

# Endpoints requeridos:
# GET /books - Listar todos los libros
# GET /books/{book_id} - Obtener libro específico
# POST /books - Crear nuevo libro
# PUT /books/{book_id} - Actualizar libro
# DELETE /books/{book_id} - Eliminar libro
```

### **Tareas Específicas**

1. **Crear el modelo Book** con validaciones apropiadas
2. **Implementar storage en memoria** (lista o diccionario)
3. **Crear los 5 endpoints** con responses correctos
4. **Aplicar status codes apropiados** (200, 201, 204, 404)
5. **Manejar errores básicos** (libro no encontrado, ISBN duplicado)

### **Criterios de Evaluación**

- ✅ Todos los endpoints funcionan correctamente
- ✅ Validación de datos apropiada
- ✅ Status codes correctos
- ✅ Manejo básico de errores
- ✅ Documentación automática funcional

### **Testing Sugerido**

```bash
# Crear libro
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "FastAPI for Beginners",
    "author": "Tech Writer",
    "isbn": "978-1234567890",
    "pages": 350,
    "published_year": 2024,
    "genre": "Technology",
    "is_available": true
  }'

# Listar libros
curl -X GET "http://localhost:8000/books"

# Obtener libro específico
curl -X GET "http://localhost:8000/books/1"
```

---

## 📋 Ejercicio 2: Validación Avanzada con Pydantic (25 min)

### **Contexto**

Expandir el modelo Book con validadores custom y lógica de negocio compleja.

### **Instrucciones**

Modifica el modelo Book para incluir:

```python
class BookAdvanced(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    isbn: str = Field(..., regex=r'^\d{3}-\d{10}$')
    pages: int = Field(..., gt=0, le=10000)
    published_year: int = Field(..., ge=1500, le=2025)
    genre: Literal["Fiction", "Non-Fiction", "Technology", "Science", "Biography"]
    language: str = Field(..., min_length=2, max_length=3)  # Código de idioma
    price: Decimal = Field(..., gt=0, le=9999.99, decimal_places=2)
    rating: Optional[float] = Field(None, ge=1.0, le=5.0)
    tags: Optional[List[str]] = Field(None, max_items=5)
    is_available: bool = Field(True)
    is_bestseller: bool = Field(False)

    # Validadores custom requeridos:
    # 1. El título debe capitalizar correctamente
    # 2. El author no puede ser solo números
    # 3. Los libros bestseller deben tener rating >= 4.0
    # 4. Los tags no pueden tener duplicados
    # 5. Los libros muy antiguos (< 1900) deben tener precio especial
```

### **Tareas Específicas**

1. **Implementar todos los validadores custom** usando `@validator`
2. **Crear validación cross-field** usando `@root_validator`
3. **Manejar casos edge** (valores None, strings vacíos, etc.)
4. **Probar validaciones** con datos incorrectos
5. **Documentar las reglas** de validación

### **Casos de Test Requeridos**

```python
# Test 1: Título mal capitalizado
{
    "title": "fastapi for beginners",  # Debe corregirse a "Fastapi For Beginners"
    "author": "Tech Writer",
    "isbn": "978-1234567890",
    # ... resto de campos
}

# Test 2: Autor inválido (solo números)
{
    "title": "Valid Title",
    "author": "12345",  # Debe fallar
    # ... resto de campos
}

# Test 3: Bestseller sin rating alto
{
    "title": "Great Book",
    "author": "Famous Author",
    "rating": 3.5,
    "is_bestseller": true,  # Debe fallar (rating < 4.0)
    # ... resto de campos
}
```

---

## 📋 Ejercicio 3: Manejo de Errores Profesional (25 min)

### **Contexto**

Implementar un sistema robusto de manejo de errores para la API de libros.

### **Instrucciones**

Crear excepciones custom y handlers para manejar:

```python
# Excepciones requeridas:
class BookNotFoundError(Exception)
class DuplicateISBNError(Exception)
class InvalidBookDataError(Exception)
class BookNotAvailableError(Exception)
class LibraryFullError(Exception)

# Endpoints con manejo de errores:
# - POST /books/{book_id}/borrow - Prestar libro
# - POST /books/{book_id}/return - Devolver libro
# - GET /books/search?q=query - Buscar libros
```

### **Tareas Específicas**

1. **Crear excepciones custom** con mensajes descriptivos
2. **Implementar exception handlers globales**
3. **Agregar logging** para diferentes tipos de errores
4. **Crear responses de error consistentes**
5. **Implementar lógica de préstamo** con validaciones

### **Lógica de Negocio Requerida**

- Un libro solo puede prestarse si `is_available = true`
- No se pueden prestar más de 10 libros simultáneamente (límite global)
- Los libros bestseller tienen reglas especiales
- Búsqueda debe manejar queries vacíos o muy cortos

### **Testing de Errores**

```bash
# Intentar prestar libro no disponible
curl -X POST "http://localhost:8000/books/1/borrow"

# Buscar con query muy corto
curl -X GET "http://localhost:8000/books/search?q=a"

# Crear libro con ISBN duplicado
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{"isbn": "978-1234567890", ...}'  # ISBN ya existe
```

---

## 📋 Ejercicio 4: API REST Completa (30 min)

### **Contexto**

Integrar todos los conceptos en una API de gestión de biblioteca completa.

### **Instrucciones**

Crear una API con la siguiente estructura:

```text
/api/v1/books/                  # CRUD de libros
/api/v1/books/search           # Búsqueda avanzada
/api/v1/books/stats            # Estadísticas
/api/v1/borrowing/             # Gestión de préstamos
/api/v1/categories/            # Gestión de categorías
/health                        # Health check
```

### **Endpoints Específicos Requeridos**

```python
# Búsqueda avanzada
GET /api/v1/books/search?title=&author=&genre=&year_from=&year_to=&available_only=

# Estadísticas
GET /api/v1/books/stats
# Response: {total_books, available_count, borrowed_count, by_genre, avg_rating}

# Préstamos
POST /api/v1/borrowing/borrow/{book_id}
POST /api/v1/borrowing/return/{book_id}
GET /api/v1/borrowing/active    # Préstamos activos

# Categorías
GET /api/v1/categories/         # Listar géneros únicos
GET /api/v1/categories/{genre}/books  # Libros por género
```

### **Características Avanzadas**

1. **Paginación** en todos los endpoints de listado
2. **Filtros múltiples** combinables
3. **Ordenamiento** por diferentes campos
4. **Validación cruzada** entre modelos
5. **Logging estructurado** de todas las operaciones

### **Estructura de Response Consistente**

```python
# Response de éxito
{
    "success": true,
    "data": {...},
    "message": "Operation completed successfully",
    "timestamp": "2025-07-24T10:30:00"
}

# Response de error
{
    "success": false,
    "error_code": "BOOK_NOT_FOUND",
    "message": "Book with ID 123 not found",
    "details": {...},
    "timestamp": "2025-07-24T10:30:00"
}
```

---

## 📋 Ejercicio 5: Testing y Documentación (15 min)

### **Contexto**

Completar la API con testing automatizado y documentación profesional.

### **Instrucciones**

1. **Crear test suite** usando pytest para:

   - Todos los endpoints CRUD
   - Validaciones de datos
   - Manejo de errores
   - Casos edge

2. **Documentar la API** con:

   - README completo con instalación
   - Ejemplos de uso para cada endpoint
   - Guía de desarrollo
   - Esquemas de base de datos

3. **Optimizar documentación automática**:
   - Descriptions detalladas en todos los endpoints
   - Ejemplos en esquemas Pydantic
   - Tags organizados por funcionalidad
   - Responses documentation completa

### **Testing Automatizado Mínimo**

```python
# test_books.py
def test_create_book_success():
    # Test creación exitosa
    pass

def test_create_book_duplicate_isbn():
    # Test ISBN duplicado
    pass

def test_get_book_not_found():
    # Test libro no encontrado
    pass

def test_borrow_book_not_available():
    # Test prestar libro no disponible
    pass

def test_search_books_with_filters():
    # Test búsqueda con filtros
    pass
```

### **Documentación README Requerida**

```markdown
# Library Management API

## Installation

[Instrucciones paso a paso]

## Quick Start

[Ejemplos básicos]

## API Endpoints

[Documentación detallada de cada endpoint]

## Examples

[Casos de uso completos]

## Development

[Guía para desarrolladores]
```

---

## 🎯 Entrega Final

### **Estructura de Proyecto Esperada**

```text
ejercicio-biblioteca/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── exceptions.py
│   ├── handlers.py
│   └── utils.py
├── tests/
│   ├── test_books.py
│   ├── test_borrowing.py
│   └── conftest.py
├── requirements.txt
└── README.md
```

### **Criterios de Evaluación**

| Aspecto            | Puntos | Descripción                         |
| ------------------ | ------ | ----------------------------------- |
| **Funcionalidad**  | 40%    | Todos los endpoints funcionan       |
| **Validación**     | 25%    | Validaciones robustas implementadas |
| **Manejo Errores** | 20%    | Sistema de errores profesional      |
| **Documentación**  | 10%    | README y docs automáticas           |
| **Testing**        | 5%     | Tests básicos implementados         |

### **Tiempo Total Estimado: 115 minutos**

### **Entregables**

1. ✅ **Código fuente** completo y funcional
2. ✅ **API funcionando** en puerto 8000
3. ✅ **Documentación** Swagger accesible
4. ✅ **README** con instrucciones
5. ✅ **Tests básicos** ejecutables

---

_Ejercicios diseñados para Semana 3 - Bootcamp FastAPI_  
_Tiempo total: ~2 horas de trabajo práctico_
