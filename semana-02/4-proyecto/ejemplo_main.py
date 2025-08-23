# Ejemplo básico para Proyecto Semana 2: API de Biblioteca Personal
# Este archivo muestra la estructura básica y algunos endpoints de ejemplo

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict
import asyncio

# ==================== MODELOS PYDANTIC ====================

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

    # Validación simplificada compatible con Pydantic 1.x
    class Config:
        use_enum_values = True

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

# ==================== CONFIGURACIÓN FASTAPI ====================

app = FastAPI(
    title="API de Biblioteca Personal - Semana 2",
    description="Una API simple para gestión de libros personales",
    version="1.0.0"
)

# Base de datos en memoria
books_db: Dict[int, dict] = {}
next_id: int = 1

# ==================== FUNCIONES AUXILIARES ====================

def get_current_time() -> datetime:
    return datetime.now()

def create_book_record(book_data: BookCreate) -> dict:
    global next_id
    book_dict = book_data.dict()
    book_dict.update({
        "id": next_id,
        "created_at": get_current_time(),
        "updated_at": get_current_time()
    })
    books_db[next_id] = book_dict
    next_id += 1
    return book_dict

# ==================== FUNCIONES ASYNC ====================

async def validate_isbn_external(isbn: str) -> bool:
    """Simula validación de ISBN en base de datos externa"""
    await asyncio.sleep(0.5)  # Simular latencia de API externa
    clean_isbn = isbn.replace('-', '').replace(' ', '')
    return len(clean_isbn) in [10, 13] and clean_isbn.isdigit()

async def get_book_metadata(title: str, author: str) -> dict:
    """Simula obtención de metadata adicional del libro"""
    await asyncio.sleep(0.4)  # Simular consulta a API externa
    return {
        "goodreads_rating": 4.2,
        "amazon_price": 15.99,
        "availability": "in_stock",
        "cover_url": f"https://covers.openlibrary.org/b/title/{title.replace(' ', '+')}-M.jpg"
    }

# ==================== ENDPOINTS ====================

@app.get("/")
def read_root():
    """Endpoint de bienvenida"""
    return {
        "message": "Bienvenido a la API de Biblioteca Personal",
        "version": "1.0.0",
        "docs": "/docs",
        "total_books": len(books_db)
    }

# ==================== CRUD BÁSICO ====================

@app.post("/books", response_model=BookResponse, status_code=201)
async def create_book(book: BookCreate):
    """Crear un nuevo libro (ASYNC)"""
    # Validar ISBN externamente si está presente
    if book.isbn:
        isbn_valid = await validate_isbn_external(book.isbn)
        if not isbn_valid:
            raise HTTPException(status_code=400, detail="ISBN inválido según validación externa")
    
    # Crear el libro
    book_record = create_book_record(book)
    return BookResponse(**book_record)

@app.get("/books", response_model=List[BookResponse])
def get_books(
    status: Optional[BookStatus] = None,
    genre: Optional[BookGenre] = None,
    limit: int = Query(default=100, le=100, ge=1)
):
    """Listar todos los libros con filtros opcionales"""
    books = list(books_db.values())
    
    # Aplicar filtros
    if status:
        books = [book for book in books if book["status"] == status]
    if genre:
        books = [book for book in books if book["genre"] == genre]
    
    # Limitar resultados
    books = books[:limit]
    
    return [BookResponse(**book) for book in books]

@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    """Obtener un libro específico por ID"""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    return BookResponse(**books_db[book_id])

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book_complete(book_id: int, book: BookCreate):
    """Actualizar un libro completamente"""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    # Actualizar con todos los datos nuevos
    updated_data = book.dict()
    updated_data.update({
        "id": book_id,
        "created_at": books_db[book_id]["created_at"],
        "updated_at": get_current_time()
    })
    
    books_db[book_id] = updated_data
    return BookResponse(**updated_data)

@app.patch("/books/{book_id}", response_model=BookResponse)
def update_book_partial(book_id: int, book: BookUpdate):
    """Actualizar un libro parcialmente"""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    # Actualizar solo los campos proporcionados
    current_book = books_db[book_id].copy()
    update_data = book.dict(exclude_unset=True)
    
    current_book.update(update_data)
    current_book["updated_at"] = get_current_time()
    
    books_db[book_id] = current_book
    return BookResponse(**current_book)

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    """Eliminar un libro"""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    deleted_book = books_db.pop(book_id)
    return {"message": f"Libro '{deleted_book['title']}' eliminado correctamente"}

# ==================== BÚSQUEDAS ====================

@app.get("/books/search/title", response_model=List[BookResponse])
def search_books_by_title(
    title: str = Query(..., min_length=1, description="Título a buscar"),
    limit: int = Query(10, ge=1, le=50, description="Número máximo de resultados")
):
    """Buscar libros por título (case insensitive)"""
    matching_books = []
    search_title = title.lower()
    
    for book in books_db.values():
        if search_title in book["title"].lower():
            matching_books.append(book)
            if len(matching_books) >= limit:
                break
    
    return [BookResponse(**book) for book in matching_books]

@app.get("/books/search/author", response_model=List[BookResponse])
def search_books_by_author(
    author: str = Query(..., min_length=1, description="Autor a buscar"),
    limit: int = Query(10, ge=1, le=50, description="Número máximo de resultados")
):
    """Buscar libros por autor (case insensitive)"""
    matching_books = []
    search_author = author.lower()
    
    for book in books_db.values():
        if search_author in book["author"].lower():
            matching_books.append(book)
            if len(matching_books) >= limit:
                break
    
    return [BookResponse(**book) for book in matching_books]

# ==================== ENDPOINT ASYNC ADICIONAL ====================

@app.get("/books/{book_id}/metadata")
async def get_book_metadata_async(book_id: int):
    """Obtener metadata adicional del libro (ASYNC)"""
    if book_id not in books_db:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    book = books_db[book_id]
    metadata = await get_book_metadata(book["title"], book["author"])
    
    return {
        "book_info": {
            "id": book["id"],
            "title": book["title"],
            "author": book["author"]
        },
        "external_metadata": metadata
    }

# ==================== DATOS DE EJEMPLO ====================

# Función para agregar datos de ejemplo al iniciar
def add_sample_data():
    sample_books = [
        {
            "title": "Don Quijote de la Mancha",
            "author": "Miguel de Cervantes",
            "isbn": "9788437610405",
            "genre": BookGenre.fiction,
            "pages": 863,
            "publication_year": 1605,
            "status": BookStatus.finished,
            "rating": 5,
            "notes": "Una obra maestra de la literatura"
        },
        {
            "title": "Sapiens",
            "author": "Yuval Noah Harari", 
            "genre": BookGenre.non_fiction,
            "pages": 498,
            "publication_year": 2011,
            "status": BookStatus.reading,
            "rating": 4
        },
        {
            "title": "Clean Code",
            "author": "Robert C. Martin",
            "isbn": "9780132350884",
            "genre": BookGenre.technology,
            "pages": 464,
            "publication_year": 2008,
            "status": BookStatus.to_read,
            "notes": "Recomendado para desarrollo de software"
        }
    ]
    
    for book_data in sample_books:
        book_create = BookCreate(**book_data)
        create_book_record(book_create)

# Agregar datos de ejemplo al iniciar la aplicación
add_sample_data()

# ==================== PUNTO DE ENTRADA ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
