# Ejercicios Prácticos - Semana 3 (Consolidación)

## 🎯 Objetivo Básico

Consolidar conceptos de **validación avanzada + manejo de errores + estructura del proyecto** en el Bloque 4 (45 minutos) a través de ejercicios simples.

## ⏱️ Tiempo: 45 minutos (Bloque 4 - Consolidación)

## 📋 Pre-requisitos

- ✅ API de los Bloques 1-3 funcionando
- ✅ Validación avanzada implementada
- ✅ Manejo de errores básico funcionando
- ✅ Estructura de proyecto organizada

---

## 🏋️ Ejercicio 1: Verificación Completa (20 min)

**Objetivo**: Asegurar que todo lo aprendido funciona

### 📝 Checklist de Verificación

**Revisa tu proyecto actual y marca:**

- [ ] **Validación avanzada**: ¿Tienes validadores custom con `@validator`?
- [ ] **Manejo de errores**: ¿Tus endpoints manejan errores con `HTTPException`?
- [ ] **Estructura organizada**: ¿Tienes archivos separados (models, routers, services)?
- [ ] **API funcionando**: ¿Todos los endpoints CRUD funcionan correctamente?
- [ ] **Logs básicos**: ¿Se registran errores en la consola?
- [ ] **Documentación**: ¿Se ve bien en http://127.0.0.1:8000/docs?

### 🔧 **Si algo no funciona**:

1. **Problema con validadores**:

   ```python
   from pydantic import BaseModel, validator

   class Product(BaseModel):
       name: str
       price: float

       @validator('name')
       def validate_name(cls, v):
           if not v.strip():
               raise ValueError('El nombre no puede estar vacío')
           return v.title()
   ```

2. **Problema con errores**: Usa el patrón más simple:

   ```python
   from fastapi import HTTPException, status

   @app.get("/products/{product_id}")
   def get_product(product_id: int):
       if product_id not in products_db:
           raise HTTPException(
               status_code=status.HTTP_404_NOT_FOUND,
               detail="Producto no encontrado"
           )
       return products_db[product_id]
   ```

3. **Problema con estructura**: Verifica que tienes:

   ```
   mi-proyecto/
   ├── main.py
   ├── models/
   │   └── product.py
   ├── routers/
   │   └── products.py
   └── services/
       └── product_service.py
   ```

### ✅ Criterio de Éxito

- Todos los checkboxes marcados
- API ejecutándose sin errores
- Documentación automática funcional

---

## 🏋️ Ejercicio 2: Endpoint de Búsqueda Simple (25 min)

**Objetivo**: Agregar un endpoint de búsqueda básico que use todo lo aprendido

### 📝 Instrucciones

1. **Abrir tu archivo de productos** (donde tienes los endpoints)

2. **Agregar este endpoint de búsqueda**:

```python
from typing import List, Optional

@app.get("/products/search")
def search_products(
    name: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> List[dict]:
    """Buscar productos por nombre y rango de precio"""
    try:
        # Obtener todos los productos
        results = products_db.copy()

        # Filtrar por nombre si se proporciona
        if name:
            name_lower = name.lower().strip()
            if len(name_lower) < 2:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El término de búsqueda debe tener al menos 2 caracteres"
                )
            results = [p for p in results if name_lower in p["name"].lower()]

        # Filtrar por precio mínimo
        if min_price is not None:
            if min_price < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El precio mínimo no puede ser negativo"
                )
            results = [p for p in results if p["price"] >= min_price]

        # Filtrar por precio máximo
        if max_price is not None:
            if max_price < 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El precio máximo no puede ser negativo"
                )
            results = [p for p in results if p["price"] <= max_price]

        # Validar rango de precios
        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El precio mínimo no puede ser mayor al máximo"
                )

        return results

    except HTTPException:
        raise
    except Exception as e:
        # Log del error (opcional)
        print(f"Error en búsqueda: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )
```

3. **Probar el endpoint**:

```bash
# Buscar por nombre
curl "http://localhost:8000/products/search?name=laptop"

# Buscar por rango de precio
curl "http://localhost:8000/products/search?min_price=100&max_price=500"

# Buscar combinando filtros
curl "http://localhost:8000/products/search?name=mouse&min_price=20&max_price=100"

# Probar errores
curl "http://localhost:8000/products/search?name=a"  # Error: muy corto
curl "http://localhost:8000/products/search?min_price=500&max_price=100"  # Error: rango inválido
```

4. **Verificar en documentación**:
   - Ve a http://127.0.0.1:8000/docs
   - Busca el endpoint `/products/search`
   - Prueba los filtros desde la interfaz

### ✅ Criterio de Éxito

- Endpoint de búsqueda funciona con todos los filtros
- Maneja errores apropiadamente
- Valida datos correctamente
- Aparece en documentación automática

---

## 💻 Ejemplos de Testing

### **Testing manual rápido**:

```bash
# 1. Verificar que la API funciona
curl http://localhost:8000/products/

# 2. Probar búsqueda básica
curl "http://localhost:8000/products/search?name=laptop"

# 3. Probar validación de errores
curl "http://localhost:8000/products/search?name=x"

# 4. Verificar documentación
# Ir a http://localhost:8000/docs
```

### **¿Qué has logrado?**

✅ **Validación robusta**: Tu API valida datos y maneja errores  
✅ **Búsqueda funcional**: Los usuarios pueden filtrar productos  
✅ **Código organizado**: Tienes una estructura profesional  
✅ **Manejo de errores**: Tu API es resiliente  
✅ **Documentación**: Todo está auto-documentado

---

_Ejercicios diseñados para Semana 3 - Bootcamp FastAPI_  
_Tiempo total: 45 minutos de consolidación práctica_
is_available: bool = Field(True)
is_bestseller: bool = Field(False)

    # Validadores custom requeridos:
    # 1. El título debe capitalizar correctamente
    # 2. El author no puede ser solo números
    # 3. Los libros bestseller deben tener rating >= 4.0
    # 4. Los tags no pueden tener duplicados
    # 5. Los libros muy antiguos (< 1900) deben tener precio especial

````

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
````

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
