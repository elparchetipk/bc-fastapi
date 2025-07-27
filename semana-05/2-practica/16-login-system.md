# Práctica 16: Sistema de Login y Register

**⏱️ Tiempo estimado:** 90 minutos  
**🎯 Objetivo:** Crear endpoints completos de autenticación con registro y login de usuarios

## 📋 En esta práctica aprenderás

- Implementar endpoint de registro de usuarios
- Crear endpoint de login con validación de credenciales
- Generar y retornar tokens JWT al login
- Manejar errores de autenticación apropiadamente
- Validar datos de entrada con Pydantic

## 🔧 Paso 1: Schemas de Autenticación Extendidos

Actualizar `app/schemas/auth.py`:

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    email: EmailStr = Field(..., description="Email válido del usuario")
    full_name: str = Field(..., min_length=2, max_length=100, description="Nombre completo")
    password: str = Field(..., min_length=8, description="Password debe tener al menos 8 caracteres")

    @validator('username')
    def validate_username(cls, v):
        if not v.isalnum():
            raise ValueError('Username solo puede contener letras y números')
        return v.lower()

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password debe contener al menos una mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Password debe contener al menos una minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password debe contener al menos un número')
        return v

class UserLogin(BaseModel):
    username: str = Field(..., description="Username o email")
    password: str = Field(..., description="Password del usuario")

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # segundos
    user: "UserResponse"

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    username: str
    email: str
    full_name: str
    is_active: bool
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True

class PasswordChange(BaseModel):
    current_password: str = Field(..., description="Password actual")
    new_password: str = Field(..., min_length=8, description="Nuevo password")
    confirm_password: str = Field(..., description="Confirmación del nuevo password")

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('Los passwords no coinciden')
        return v

    @validator('new_password')
    def validate_new_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password debe contener al menos una mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Password debe contener al menos una minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password debe contener al menos un número')
        return v
```

## 🔧 Paso 2: Actualizar Modelo de Usuario

Actualizar `app/models/user.py` para incluir campos de autenticación:

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"
```

## 🔧 Paso 3: CRUD de Usuarios con Autenticación

Crear `app/crud/user.py`:

```python
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from datetime import datetime

from app.models.user import User
from app.schemas.auth import UserRegister, UserResponse
from app.core.security import get_password_hash, verify_password

class UserCRUD:

    def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        """Obtener usuario por username"""
        return db.query(User).filter(User.username == username).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return db.query(User).filter(User.email == email).first()

    def get_user_by_username_or_email(self, db: Session, identifier: str) -> Optional[User]:
        """Obtener usuario por username o email"""
        return db.query(User).filter(
            or_(User.username == identifier, User.email == identifier)
        ).first()

    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        return db.query(User).filter(User.id == user_id).first()

    def create_user(self, db: Session, user_data: UserRegister) -> User:
        """Crear nuevo usuario con password hasheado"""

        # Verificar que username no existe
        if self.get_user_by_username(db, user_data.username):
            raise ValueError("Username ya está en uso")

        # Verificar que email no existe
        if self.get_user_by_email(db, user_data.email):
            raise ValueError("Email ya está registrado")

        # Crear usuario con password hasheado
        hashed_password = get_password_hash(user_data.password)

        db_user = User(
            username=user_data.username,
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hashed_password
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    def authenticate_user(self, db: Session, identifier: str, password: str) -> Optional[User]:
        """Autenticar usuario con username/email y password"""
        user = self.get_user_by_username_or_email(db, identifier)

        if not user:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        # Actualizar último login
        user.last_login = datetime.utcnow()
        db.commit()

        return user

    def update_password(self, db: Session, user: User, new_password: str) -> User:
        """Actualizar password del usuario"""
        user.hashed_password = get_password_hash(new_password)
        db.commit()
        db.refresh(user)
        return user

    def deactivate_user(self, db: Session, user: User) -> User:
        """Desactivar usuario"""
        user.is_active = False
        db.commit()
        db.refresh(user)
        return user

    def activate_user(self, db: Session, user: User) -> User:
        """Activar usuario"""
        user.is_active = True
        db.commit()
        db.refresh(user)
        return user

# Instancia global del CRUD
user_crud = UserCRUD()
```

## 🔧 Paso 4: Endpoints de Autenticación

Crear `app/api/auth.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta

from app.database import get_db
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse, PasswordChange
from app.crud.user import user_crud
from app.core.security import create_access_token, get_current_user
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])
security = HTTPBearer()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Registrar nuevo usuario

    - **username**: Nombre de usuario único (3-50 caracteres, solo letras y números)
    - **email**: Email válido del usuario
    - **full_name**: Nombre completo (2-100 caracteres)
    - **password**: Password seguro (mínimo 8 caracteres, mayúscula, minúscula, número)
    """
    try:
        user = user_crud.create_user(db=db, user_data=user_data)
        return UserResponse.model_validate(user)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )

@router.post("/login", response_model=Token)
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Iniciar sesión

    - **username**: Username o email del usuario
    - **password**: Password del usuario

    Retorna un token JWT válido por el tiempo configurado
    """
    # Autenticar usuario
    user = user_crud.authenticate_user(
        db=db,
        identifier=credentials.username,
        password=credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token de acceso
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id},
        expires_delta=access_token_expires
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # en segundos
        user=UserResponse.model_validate(user)
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Obtener perfil del usuario autenticado

    Requiere token JWT válido en el header Authorization
    """
    return UserResponse.model_validate(current_user)

@router.put("/change-password", response_model=dict)
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Cambiar password del usuario autenticado

    - **current_password**: Password actual del usuario
    - **new_password**: Nuevo password (debe cumplir requisitos de seguridad)
    - **confirm_password**: Confirmación del nuevo password
    """
    # Verificar password actual
    if not verify_password(password_data.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password actual incorrecto"
        )

    # Actualizar password
    user_crud.update_password(db=db, user=current_user, new_password=password_data.new_password)

    return {"message": "Password actualizado exitosamente"}

@router.post("/logout", response_model=dict)
def logout_user(
    current_user: User = Depends(get_current_user)
):
    """
    Cerrar sesión (logout)

    En una implementación real, aquí se invalidaría el token
    o se agregaría a una blacklist. Por ahora solo confirmamos la acción.
    """
    return {
        "message": f"Usuario {current_user.username} ha cerrado sesión exitosamente",
        "logged_out_at": datetime.utcnow().isoformat()
    }

@router.get("/validate-token", response_model=dict)
def validate_token(
    current_user: User = Depends(get_current_user)
):
    """
    Validar si el token actual es válido

    Útil para verificar la validez del token desde el frontend
    """
    return {
        "valid": True,
        "user_id": current_user.id,
        "username": current_user.username,
        "message": "Token válido"
    }
```

## 🔧 Paso 5: Actualizar Funciones de Seguridad

Actualizar `app/core/security.py` para incluir función de obtener usuario actual:

```python
# ...código existente...

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database import get_db
from app.models.user import User
from app.schemas.auth import TokenData

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Obtener usuario actual a partir del token JWT
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificar token
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username: str = payload.get("sub")
        user_id: int = payload.get("user_id")

        if username is None or user_id is None:
            raise credentials_exception

        token_data = TokenData(username=username, user_id=user_id)

    except JWTError:
        raise credentials_exception

    # Obtener usuario de la base de datos
    from app.crud.user import user_crud
    user = user_crud.get_user_by_username(db, username=token_data.username)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Obtener usuario actual activo
    (Wrapper para mayor claridad semántica)
    """
    return current_user
```

## 🔧 Paso 6: Integrar en la Aplicación Principal

Actualizar `app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import auth
# ...otros imports...

app = FastAPI(
    title="API con Autenticación JWT",
    description="API REST con sistema de autenticación completo",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "message": "API con Autenticación JWT",
        "version": "1.0.0",
        "endpoints": {
            "register": "/api/v1/auth/register",
            "login": "/api/v1/auth/login",
            "profile": "/api/v1/auth/me",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API funcionando correctamente"}
```

## 🧪 Paso 7: Probar el Sistema de Autenticación

### Crear datos de prueba

Crear `scripts/test_auth.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

def test_authentication_flow():
    """Probar flujo completo de autenticación"""

    # 1. Registrar usuario
    print("1. Registrando usuario...")
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Usuario de Prueba",
        "password": "TestPass123"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    # 2. Login
    print("\n2. Iniciando sesión...")
    login_data = {
        "username": "testuser",
        "password": "TestPass123"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        print(f"Token obtenido: {access_token[:50]}...")

        # 3. Obtener perfil
        print("\n3. Obteniendo perfil...")
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Profile: {response.json()}")

        # 4. Validar token
        print("\n4. Validando token...")
        response = requests.get(f"{BASE_URL}/auth/validate-token", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Validation: {response.json()}")

    else:
        print(f"Error en login: {response.json()}")

if __name__ == "__main__":
    test_authentication_flow()
```

### Probar con curl

```bash
# 1. Registrar usuario
curl -X POST "http://localhost:8000/api/v1/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "johndoe",
       "email": "john@example.com",
       "full_name": "John Doe",
       "password": "SecurePass123"
     }'

# 2. Login (guardar el token)
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "johndoe",
       "password": "SecurePass123"
     }' | jq -r '.access_token')

# 3. Obtener perfil
curl -X GET "http://localhost:8000/api/v1/auth/me" \
     -H "Authorization: Bearer $TOKEN"

# 4. Cambiar password
curl -X PUT "http://localhost:8000/api/v1/auth/change-password" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "current_password": "SecurePass123",
       "new_password": "NewSecurePass456",
       "confirm_password": "NewSecurePass456"
     }'
```

## ✅ Ejercicios de Práctica

1. **Validaciones adicionales**: Agregar validación de email único en tiempo real
2. **Rate limiting**: Implementar límite de intentos de login
3. **Password reset**: Crear flujo de recuperación de password
4. **Refresh tokens**: Implementar tokens de refresh

## 🎯 Entregables

- [ ] Endpoints de registro y login funcionando
- [ ] Validación de tokens JWT
- [ ] Manejo de errores apropiado
- [ ] Tests de autenticación pasando
- [ ] Documentación de API actualizada

## 📚 Conceptos Clave Aprendidos

- **JWT Tokens**: Generación y validación
- **Password Hashing**: Seguridad de credenciales
- **Dependency Injection**: Obtener usuario actual
- **Error Handling**: Manejo de errores de autenticación
- **API Security**: Mejores prácticas de seguridad

---

## 🚨 Problemas Comunes

### Token inválido o expirado

```python
# Verificar configuración de SECRET_KEY y tiempo de expiración
# Generar nuevo token si es necesario
```

### Usuario no encontrado

```python
# Verificar que el usuario esté activo
# Confirmar que username/email existen en BD
```

### Password incorrecto

```python
# Verificar que el password hasheado coincide
# Confirmar que el usuario está usando el password correcto
```

¡Continúa con la [Práctica 17: Protección de Endpoints](./17-endpoint-protection.md)!
