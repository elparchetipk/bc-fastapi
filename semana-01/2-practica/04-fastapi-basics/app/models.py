from pydantic import BaseModel, Field, EmailStr, ConfigDict
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
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Juan Pérez",
                "email": "juan@email.com",
                "age": 25,
                "interests": ["technology", "science"]
            }
        }
    )
    
    name: str = Field(min_length=2, max_length=50, description="Nombre completo del usuario")
    email: EmailStr = Field(description="Email válido del usuario")
    age: int = Field(ge=18, le=120, description="Edad del usuario")
    interests: Optional[List[Category]] = Field(default=None, description="Intereses del usuario")

class User(UserCreate, TimestampMixin):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Juan Pérez",
                "email": "juan@email.com",
                "age": 25,
                "interests": ["technology", "science"],
                "is_active": True,
                "created_at": "2025-01-01T10:00:00Z"
            }
        }
    )
    
    id: int = Field(description="ID único del usuario")
    is_active: bool = Field(default=True, description="Estado activo del usuario")

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    interests: Optional[List[Category]]
    is_active: bool
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(default=None, ge=18, le=120)
    interests: Optional[List[Category]] = None
    is_active: Optional[bool] = None

# Modelo para artículos
class ArticleCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Introducción a FastAPI",
                "content": "FastAPI es un framework moderno para crear APIs con Python...",
                "category": "technology",
                "tags": ["python", "api", "web"]
            }
        }
    )
    
    title: str = Field(min_length=5, max_length=200, description="Título del artículo")
    content: str = Field(min_length=10, description="Contenido del artículo")
    category: Category = Field(description="Categoría del artículo")
    tags: Optional[List[str]] = Field(default=None, description="Tags del artículo")

class Article(ArticleCreate, TimestampMixin):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Introducción a FastAPI",
                "content": "FastAPI es un framework moderno...",
                "category": "technology",
                "tags": ["python", "api", "web"],
                "author_id": 1,
                "views": 0,
                "created_at": "2025-01-01T10:00:00Z"
            }
        }
    )
    
    id: int = Field(description="ID único del artículo")
    author_id: int = Field(description="ID del autor")
    views: int = Field(default=0, description="Número de visualizaciones")

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
