# Proyecto Semana 2: API de Biblioteca Personal

## 🎯 Objetivo del Proyecto

Desarrollar una **API simple para gestión de libros** que demuestre los conceptos aprendidos en la Semana 2: type hints, Pydantic, async/await básico, y endpoints FastAPI con validaciones.

## 📋 Especificaciones Funcionales

### **Entidad Principal:**

- **Book**: Gestión de libros personales con información básica

### **Funcionalidades Requeridas:**

- ✅ CRUD básico para libros (6 endpoints)
- ✅ Búsqueda simple por título y autor
- ✅ Validación de datos con Pydantic
- ✅ 2-3 operaciones asíncronas simuladas
- ✅ Almacenamiento en memoria (lista/diccionario)

## 🏗️ Especificación Técnica

### **1. Modelo Pydantic Requerido**

```python
from pydantic import BaseModel, Field, validator
from datetime import datetime, date
from enum import Enum
from typing import Optional, List

class BookStatus(str, Enum):
    to_read = "to_read"
    reading = "reading"
    finished = "finished"
    paused = "paused"

class BookGenre(str, Enum):
    fiction = "fiction"
    non_fiction = "non_fiction"
    science = "science"
    biography = "biography"
    history = "history"
    technology = "technology"
    other = "other"

# Modelo base para Book
class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Título del libro")
    author: str = Field(..., min_length=1, max_length=100, description="Autor del libro")
    isbn: Optional[str] = Field(None, min_length=10, max_length=17, description="ISBN del libro")
    genre: BookGenre = Field(default=BookGenre.other)
    pages: Optional[int] = Field(None, ge=1, le=10000, description="Número de páginas")
    publication_year: Optional[int] = Field(None, ge=1000, le=2024, description="Año de publicación")
    status: BookStatus = Field(default=BookStatus.to_read)
    rating: Optional[int] = Field(None, ge=1, le=5, description="Calificación de 1 a 5")
    notes: Optional[str] = Field(None, max_length=1000, description="Notas personales")

    @validator('isbn')
    def validate_isbn(cls, v):
        if v is not None:
            # Remover guiones y espacios
            clean_isbn = v.replace('-', '').replace(' ', '')
            if len(clean_isbn) not in [10, 13]:
                raise ValueError('ISBN debe tener 10 o 13 dígitos')
            if not clean_isbn.isdigit():
                raise ValueError('ISBN debe contener solo números')
        return v

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    isbn: Optional[str] = Field(None, min_length=10, max_length=17)
    genre: Optional[BookGenre] = None
    pages: Optional[int] = Field(None, ge=1, le=10000)
    publication_year: Optional[int] = Field(None, ge=1000, le=2024)
    status: Optional[BookStatus] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = Field(None, max_length=1000)

class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### **2. Endpoints Requeridos**

#### **Books (`/books`)**

```python
# CRUD básico (6 endpoints principales)
POST   /books                    # Crear libro
GET    /books                    # Listar todos los libros
GET    /books/{book_id}          # Obtener libro específico
PUT    /books/{book_id}          # Actualizar libro completo
PATCH  /books/{book_id}          # Actualizar libro parcial
DELETE /books/{book_id}          # Eliminar libro

# Endpoints adicionales (2 endpoints de búsqueda)
GET    /books/search/title       # Buscar por título
GET    /books/search/author      # Buscar por autor

# Total: 8 endpoints
```

### **3. Funcionalidades Async Requeridas (2-3 operaciones)**

Implementar estos endpoints como **async** para simular operaciones lentas:

```python
import asyncio
from datetime import datetime

# Simular validación de ISBN en base de datos externa
async def validate_isbn_external(isbn: str) -> bool:
    await asyncio.sleep(0.5)  # Simular latencia de API externa
    # Validación simple para demo
    return len(isbn.replace('-', '').replace(' ', '')) in [10, 13]

# Simular backup de datos cuando se crea un libro
async def backup_book_data(book_data: dict) -> dict:
    await asyncio.sleep(0.3)  # Simular proceso de backup
    return {
        "backup_id": f"bk_{datetime.now().timestamp()}",
        "status": "success"
    }

# Simular obtención de información adicional del libro
async def get_book_metadata(title: str, author: str) -> dict:
    await asyncio.sleep(0.4)  # Simular consulta a API externa
    return {
        "goodreads_rating": 4.2,
        "amazon_price": 15.99,
        "availability": "in_stock"
    }

# Endpoints async requeridos (2-3 endpoints):
@app.post("/books", response_model=BookResponse)
async def create_book_async(book: BookCreate):
    # Validar ISBN externamente si está presente
    if book.isbn:
        isbn_valid = await validate_isbn_external(book.isbn)
        if not isbn_valid:
            raise HTTPException(status_code=400, detail="ISBN inválido")

    # Crear libro y hacer backup en paralelo
    pass

@app.get("/books/{book_id}/metadata")
async def get_book_metadata_async(book_id: int):
    # Obtener metadata adicional del libro
    pass
```

### **4. Búsquedas Simples**

```python
from fastapi import Query

# Búsqueda por título
@app.get("/books/search/title", response_model=List[BookResponse])
def search_books_by_title(
    title: str = Query(..., min_length=1, description="Título a buscar"),
    limit: int = Query(10, ge=1, le=50, description="Número máximo de resultados")
):
    # Buscar libros que contengan el título (case insensitive)
    pass

# Búsqueda por autor
@app.get("/books/search/author", response_model=List[BookResponse])
def search_books_by_author(
    author: str = Query(..., min_length=1, description="Autor a buscar"),
    limit: int = Query(10, ge=1, le=50, description="Número máximo de resultados")
):
    # Buscar libros por autor (case insensitive)
    pass
```

## 📊 Criterios de Evaluación

### **1. Funcionalidad (40 puntos)**

- ✅ Todos los endpoints implementados y funcionando (8 endpoints)
- ✅ Validación correcta con Pydantic
- ✅ Búsquedas básicas operativas
- ✅ Operaciones CRUD funcionando

### **2. Implementación Técnica (30 puntos)**

- ✅ Type hints en 95% del código
- ✅ Uso correcto de async/await (mínimo 2 endpoints)
- ✅ Modelos Pydantic bien diseñados
- ✅ Status codes HTTP apropiados (200, 201, 404, 422)

### **3. Calidad del Código (20 puntos)**

- ✅ Código limpio y bien estructurado
- ✅ Nombres de variables descriptivos
- ✅ Comentarios donde sea necesario
- ✅ Manejo básico de errores

### **4. Documentación (10 puntos)**

- ✅ README con instrucciones claras
- ✅ Documentación automática rica en `/docs`
- ✅ Ejemplos de uso básicos

## 🚀 Guía de Implementación

### **Paso 1: Setup del Proyecto (20 min)**

```bash
# Crear estructura
mkdir library-api-week2
cd library-api-week2

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install "fastapi[all]" uvicorn

# Crear archivos base
touch main.py README.md requirements.txt
```

### **Paso 2: Modelos Pydantic (45 min)**

- Implementar modelo Book con todos los campos
- Agregar validaciones custom (ISBN, años, rating)
- Probar modelos con datos de ejemplo
- Crear esquemas Create, Update y Response

### **Paso 3: Endpoints Básicos CRUD (90 min)**

- Implementar estructura básica de datos en memoria
- POST /books - Crear libro
- GET /books - Listar todos
- GET /books/{id} - Obtener uno específico
- PUT /books/{id} - Actualizar completo
- PATCH /books/{id} - Actualizar parcial
- DELETE /books/{id} - Eliminar

### **Paso 4: Búsquedas y Async (60 min)**

- GET /books/search/title - Búsqueda por título
- GET /books/search/author - Búsqueda por autor
- Implementar 2 operaciones async (validación ISBN + metadata)
- Probar todas las funcionalidades

### **Paso 5: Testing y Documentación (40 min)**

- Probar todos los endpoints manualmente
- Crear README completo con ejemplos
- Verificar documentación automática
- Crear requirements.txt

### **Cronograma Detallado (5.5 horas total):**

- **0:00-0:20** → Setup inicial y estructura
- **0:20-1:05** → Modelos Pydantic y validaciones
- **1:05-2:35** → Endpoints CRUD básicos
- **2:35-3:35** → Búsquedas y funciones async
- **3:35-4:15** → Testing y debugging
- **4:15-4:55** → Documentación y pulido
- **4:55-5:30** → Review final y entrega

## 📝 Entregables

### **Archivos Requeridos:**

1. **`main.py`** - API principal con todos los endpoints
2. **`README.md`** - Documentación del proyecto
3. **`requirements.txt`** - Dependencias del proyecto

### **Formato de Entrega:**

- **Repositorio GitHub** con código fuente
- **Video demo** (3-5 minutos) mostrando funcionalidades básicas
- **Archivo de pruebas** (collection de requests básicos)

### **Ejemplo de README:**

```markdown
# API de Biblioteca Personal - Semana 2

## Descripción

API REST simple para gestión de libros personales desarrollada con FastAPI.

## Características

- ✅ CRUD completo para libros (8 endpoints)
- ✅ Validación robusta con Pydantic
- ✅ 2 operaciones asíncronas
- ✅ Búsqueda por título y autor

## Instalación

\`\`\`bash
pip install -r requirements.txt
uvicorn main:app --reload
\`\`\`

## Endpoints Principales

- GET /books - Listar libros
- POST /books - Crear libro
- GET /books/search/title - Búsqueda por título

## Ejemplos de Uso

\`\`\`bash

# Crear libro

curl -X POST "http://localhost:8000/books" \
 -H "Content-Type: application/json" \
 -d '{
"title": "El Quijote",
"author": "Miguel de Cervantes",
"genre": "fiction",
"pages": 863,
"publication_year": 1605
}'

# Buscar por título

curl "http://localhost:8000/books/search/title?title=quijote"
\`\`\`

## Decisiones Técnicas

- Async/await para validación de ISBN y obtención de metadata
- Almacenamiento en memoria con diccionario para simplicidad
- Validación personalizada de ISBN con Pydantic validators
```

## 🎯 Consejos para el Éxito

1. **Empieza simple**: Implementa CRUD básico primero
2. **Usa /docs**: Aprovecha la documentación automática para probar
3. **Valida datos**: Usa las validaciones de Pydantic al máximo
4. **Organiza el código**: Mantén todo en main.py pero bien estructurado
5. **Prueba constantemente**: Cada endpoint debe funcionar antes de seguir

## 🏆 Oportunidades de Bonus

- **+5 puntos**: Implementar endpoint para estadísticas básicas (/books/stats)
- **+5 puntos**: Agregar filtro por género en listado general
- **+5 puntos**: Validación avanzada de año (no futuro)
- **+10 puntos**: Export de biblioteca a JSON

---

**🎯 Objetivo**: Consolidar conceptos de Pydantic, async/await y FastAPI en un proyecto manejable y realista.
