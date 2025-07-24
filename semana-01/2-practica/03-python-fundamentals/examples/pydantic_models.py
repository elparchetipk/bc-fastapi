from pydantic import BaseModel, EmailStr, field_validator, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enum para roles
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

# Modelo básico
class User(BaseModel):
    model_config = ConfigDict(
        use_enum_values=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Juan Pérez",
                "email": "juan@email.com",
                "age": 25,
                "role": "user",
                "is_active": True,
                "tags": ["python", "fastapi"]
            }
        }
    )

    id: int
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=18, le=120)  # ge = greater equal, le = less equal
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    tags: Optional[List[str]] = None

    # Validador personalizado usando Pydantic v2
    @field_validator('name')
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if ' ' not in v.strip():
            raise ValueError('El nombre debe contener al menos un espacio')
        return v.title()

# Modelo para respuestas (sin campos sensibles)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

# Modelo para actualización (campos opcionales)
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# Ejemplos de uso
if __name__ == "__main__":
    # Crear usuario válido
    user = User(
        id=1,
        name="juan pérez",
        email="juan@email.com",
        age=25,
        role=UserRole.ADMIN
    )
    
    print("Usuario creado:", user)
    print("JSON:", user.model_dump_json(indent=2))
    print("Dict:", user.model_dump())
    
    # Validación de errores
    try:
        invalid_user = User(
            id=1,
            name="Juan",  # Sin espacio - error
            email="invalid-email",  # Email inválido
            age=15,  # Menor de 18 - error
            role=UserRole.USER  # Usar enum válido para esta prueba
        )
    except Exception as e:
        print("Errores de validación:", e)
