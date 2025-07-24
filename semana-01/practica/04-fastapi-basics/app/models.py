from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enum para categorías
class Category(str, Enum):
    TECHNOLOGY = "technology"
    SCIENCE = "science"
    SPORTS = "sports"
    ENTERTAINMENT = "entertainment"

# Modelo base para timestamps
class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

# Modelo para usuario
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="Juan Pérez")
    email: EmailStr = Field(..., example="juan@email.com")
    age: int = Field(..., ge=18, le=120, example=25)
    interests: Optional[List[Category]] = Field(None, example=["technology", "science"])

class User(UserCreate, TimestampMixin):
    id: int = Field(..., example=1)
    is_active: bool = Field(True, example=True)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    interests: Optional[List[Category]]
    is_active: bool
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=18, le=120)
    interests: Optional[List[Category]] = None
    is_active: Optional[bool] = None

# Modelo para artículos
class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200, example="Introducción a FastAPI")
    content: str = Field(..., min_length=10, example="FastAPI es un framework moderno...")
    category: Category = Field(..., example="technology")
    tags: Optional[List[str]] = Field(None, example=["python", "api", "web"])

class Article(ArticleCreate, TimestampMixin):
    id: int = Field(..., example=1)
    author_id: int = Field(..., example=1)
    views: int = Field(0, example=0)

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    category: Category
    tags: Optional[List[str]]
    author_id: int
    views: int
    created_at: datetime

# Modelos de respuesta estándar
class StandardResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[dict] = None
