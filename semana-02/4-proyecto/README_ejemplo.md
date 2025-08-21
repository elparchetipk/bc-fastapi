# API de Biblioteca Personal - Semana 2

## Descripción

API REST simple para gestión de libros personales desarrollada con FastAPI. Este proyecto demuestra el uso de Pydantic, async/await, y validaciones avanzadas.

## Características

- ✅ CRUD completo para libros (8 endpoints)
- ✅ Validación robusta con Pydantic
- ✅ 2 operaciones asíncronas
- ✅ Búsqueda por título y autor
- ✅ Almacenamiento en memoria
- ✅ Documentación automática con FastAPI

## Requisitos

- Python 3.8+
- FastAPI
- Uvicorn

## Instalación

```bash
# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install -r requirements.txt
```

## Ejecución

```bash
# Ejecutar el servidor
uvicorn main:app --reload

# O ejecutar directamente
python main.py
```

La API estará disponible en: http://localhost:8000

## Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints Principales

### CRUD Básico

- `POST /books` - Crear libro
- `GET /books` - Listar libros (con filtros opcionales)
- `GET /books/{book_id}` - Obtener libro específico
- `PUT /books/{book_id}` - Actualizar libro completo
- `PATCH /books/{book_id}` - Actualizar libro parcial
- `DELETE /books/{book_id}` - Eliminar libro

### Búsquedas

- `GET /books/search/title?title=...` - Buscar por título
- `GET /books/search/author?author=...` - Buscar por autor

### Endpoints Async

- `POST /books` - Validación async de ISBN
- `GET /books/{book_id}/metadata` - Obtener metadata externa

## Ejemplos de Uso

### Crear un libro

```bash
curl -X POST "http://localhost:8000/books" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "El Quijote",
    "author": "Miguel de Cervantes",
    "isbn": "9788437610405",
    "genre": "fiction",
    "pages": 863,
    "publication_year": 1605,
    "status": "finished",
    "rating": 5,
    "notes": "Una obra maestra"
  }'
```

### Listar libros con filtros

```bash
# Todos los libros
curl "http://localhost:8000/books"

# Solo libros de ficción
curl "http://localhost:8000/books?genre=fiction"

# Solo libros que estoy leyendo
curl "http://localhost:8000/books?status=reading"
```

### Buscar libros

```bash
# Buscar por título
curl "http://localhost:8000/books/search/title?title=quijote"

# Buscar por autor
curl "http://localhost:8000/books/search/author?author=cervantes"
```

### Actualizar libro parcialmente

```bash
curl -X PATCH "http://localhost:8000/books/1" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "finished",
    "rating": 5,
    "notes": "Excelente libro, muy recomendado"
  }'
```

## Modelos de Datos

### BookStatus (Enum)
- `to_read` - Por leer
- `reading` - Leyendo
- `finished` - Terminado
- `paused` - Pausado

### BookGenre (Enum)
- `fiction` - Ficción
- `non_fiction` - No ficción
- `science` - Ciencia
- `biography` - Biografía
- `history` - Historia
- `technology` - Tecnología
- `other` - Otro

### Campos del Libro
- `title` (obligatorio): Título del libro
- `author` (obligatorio): Autor del libro
- `isbn` (opcional): ISBN de 10 o 13 dígitos
- `genre`: Género del libro
- `pages` (opcional): Número de páginas
- `publication_year` (opcional): Año de publicación
- `status`: Estado de lectura
- `rating` (opcional): Calificación de 1 a 5
- `notes` (opcional): Notas personales

## Decisiones Técnicas

- **Async/await**: Usado para validación de ISBN y obtención de metadata para simular operaciones I/O
- **Almacenamiento en memoria**: Diccionario Python para simplicidad, fácil de cambiar a base de datos
- **Validación personalizada**: Pydantic validators para ISBN y otros campos
- **Búsqueda case-insensitive**: Para mejor experiencia de usuario
- **Filtros opcionales**: En el listado general para mayor flexibilidad

## Datos de Ejemplo

La aplicación viene con 3 libros de ejemplo:
1. Don Quijote de la Mancha (Cervantes)
2. Sapiens (Yuval Noah Harari)
3. Clean Code (Robert C. Martin)

## Posibles Extensiones

- Agregar paginación
- Implementar autenticación
- Conectar a base de datos real
- Agregar categorías personalizadas
- Sistema de préstamos
- Exportar a CSV/JSON
