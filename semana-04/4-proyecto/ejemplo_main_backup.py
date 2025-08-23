# API de Biblioteca - Ejemplo Funcional LTS
# Semana 4: Bases de Datos con class UserBase(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    
    @validator('email')
    def validate_email(cls, v):
        # Validación básica de email compatible con Pydantic 1.x
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Email format is invalid')
        return v

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True  # Pydantic 1.x compatibletible con Python 3.8+ y versiones LTS

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from pydantic import BaseModel, validator
from typing import List, Optional
from datetime import datetime
import re

# ============================
# CONFIGURACIÓN DE BASE DE DATOS
# ============================

SQLALCHEMY_DATABASE_URL = "sqlite:///./library.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ============================
# MODELOS SQLAlchemy
# ============================

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación con préstamos
    loans = relationship("Loan", back_populates="user")

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(100), nullable=False)
    isbn = Column(String(20), unique=True, nullable=True)
    publication_year = Column(Integer, nullable=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relación con préstamos
    loans = relationship("Loan", back_populates="book")

class Loan(Base):
    __tablename__ = "loans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    loan_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relaciones
    user = relationship("User", back_populates="loans")
    book = relationship("Book", back_populates="loans")

# Crear tablas
Base.metadata.create_all(bind=engine)

# ============================
# SCHEMAS PYDANTIC
# ============================

class UserBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    author: str
    isbn: Optional[str] = None
    publication_year: Optional[int] = None

class BookCreate(BookBase):
    pass

class BookResponse(BookBase):
    id: int
    is_available: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoanBase(BaseModel):
    user_id: int
    book_id: int

class LoanCreate(LoanBase):
    pass

class LoanResponse(LoanBase):
    id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    is_returned: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================
# DEPENDENCIAS
# ============================

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================
# APLICACIÓN FASTAPI
# ============================

app = FastAPI(
    title="API de Biblioteca",
    description="Sistema de gestión de biblioteca con FastAPI y SQLAlchemy",
    version="1.0.0"
)

# ============================
# ENDPOINTS DE USUARIOS
# ============================

@app.post("/api/v1/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar email único
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email ya registrado"
        )
    
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/api/v1/users/", response_model=List[UserResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.put("/api/v1/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    for key, value in user_update.model_dump().items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user

@app.delete("/api/v1/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar que no tenga préstamos activos
    active_loans = db.query(Loan).filter(Loan.user_id == user_id, Loan.is_returned == False).count()
    if active_loans > 0:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar usuario con préstamos activos"
        )
    
    db.delete(user)
    db.commit()
    return {"message": "Usuario eliminado correctamente"}

# ============================
# ENDPOINTS DE LIBROS
# ============================

@app.post("/api/v1/books/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # Verificar ISBN único si se proporciona
    if book.isbn:
        db_book = db.query(Book).filter(Book.isbn == book.isbn).first()
        if db_book:
            raise HTTPException(
                status_code=400,
                detail="ISBN ya registrado"
            )
    
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@app.get("/api/v1/books/", response_model=List[BookResponse])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = db.query(Book).offset(skip).limit(limit).all()
    return books

@app.get("/api/v1/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return book

@app.get("/api/v1/books/search/{title}", response_model=List[BookResponse])
def search_books(title: str, db: Session = Depends(get_db)):
    books = db.query(Book).filter(Book.title.contains(title)).all()
    return books

@app.put("/api/v1/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_update: BookCreate, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    for key, value in book_update.model_dump().items():
        setattr(book, key, value)
    
    db.commit()
    db.refresh(book)
    return book

@app.delete("/api/v1/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    db.delete(book)
    db.commit()
    return {"message": "Libro eliminado correctamente"}

# ============================
# ENDPOINTS DE PRÉSTAMOS
# ============================

@app.post("/api/v1/loans/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    # Verificar que el libro existe y está disponible
    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if book is None:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    if book.is_available == False:
        raise HTTPException(status_code=400, detail="Libro no disponible")
    
    # Verificar que el usuario existe
    user = db.query(User).filter(User.id == loan.user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar límite de préstamos por usuario (máximo 3)
    active_loans = db.query(Loan).filter(
        Loan.user_id == loan.user_id, 
        Loan.is_returned == False
    ).count()
    if active_loans >= 3:
        raise HTTPException(
            status_code=400,
            detail="Usuario ya tiene el máximo de préstamos permitidos (3)"
        )
    
    # Crear préstamo
    db_loan = Loan(**loan.model_dump())
    db.add(db_loan)
    
    # Marcar libro como no disponible usando update
    db.query(Book).filter(Book.id == loan.book_id).update({"is_available": False})
    
    db.commit()
    db.refresh(db_loan)
    return db_loan

@app.get("/api/v1/loans/", response_model=List[LoanResponse])
def list_loans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    loans = db.query(Loan).offset(skip).limit(limit).all()
    return loans

@app.get("/api/v1/loans/{loan_id}", response_model=LoanResponse)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    return loan

@app.put("/api/v1/loans/{loan_id}/return", response_model=LoanResponse)
def return_book(loan_id: int, db: Session = Depends(get_db)):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if loan is None:
        raise HTTPException(status_code=404, detail="Préstamo no encontrado")
    
    if loan.is_returned == True:
        raise HTTPException(status_code=400, detail="Libro ya fue devuelto")
    
    # Marcar préstamo como devuelto usando update
    db.query(Loan).filter(Loan.id == loan_id).update({
        "is_returned": True,
        "return_date": datetime.utcnow()
    })
    
    # Marcar libro como disponible usando update
    db.query(Book).filter(Book.id == loan.book_id).update({"is_available": True})
    
    db.commit()
    db.refresh(loan)
    return loan

@app.get("/api/v1/loans/user/{user_id}", response_model=List[LoanResponse])
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    loans = db.query(Loan).filter(Loan.user_id == user_id).all()
    return loans

@app.get("/api/v1/loans/active", response_model=List[LoanResponse])
def get_active_loans(db: Session = Depends(get_db)):
    loans = db.query(Loan).filter(Loan.is_returned == False).all()
    return loans

# ============================
# ENDPOINTS DE ESTADÍSTICAS
# ============================

@app.get("/api/v1/stats/books")
def get_books_stats(db: Session = Depends(get_db)):
    total_books = db.query(Book).count()
    available_books = db.query(Book).filter(Book.is_available == True).count()
    borrowed_books = total_books - available_books
    
    return {
        "total_books": total_books,
        "available_books": available_books,
        "borrowed_books": borrowed_books
    }

@app.get("/api/v1/stats/users")
def get_users_stats(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    
    return {
        "total_users": total_users,
        "active_users": active_users
    }

@app.get("/api/v1/stats/loans")
def get_loans_stats(db: Session = Depends(get_db)):
    total_loans = db.query(Loan).count()
    active_loans = db.query(Loan).filter(Loan.is_returned == False).count()
    returned_loans = db.query(Loan).filter(Loan.is_returned == True).count()
    
    return {
        "total_loans": total_loans,
        "active_loans": active_loans,
        "returned_loans": returned_loans
    }

# ============================
# ENDPOINT RAÍZ
# ============================

@app.get("/")
def read_root():
    return {
        "message": "API de Biblioteca - Semana 4",
        "documentation": "/docs",
        "status": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
