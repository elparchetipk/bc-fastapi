# Práctica 15: JWT y Hashing Básico

## 🎯 Objetivo

Implementar **autenticación básica** con JWT y hashing de passwords en 90 minutos, usando conceptos simples y funcionales.

## ⏱️ Tiempo: 90 minutos

## 📋 Pre-requisitos

- ✅ SQLAlchemy funcionando (Semana 4 completada)
- ✅ Modelos y CRUD básicos implementados
- ✅ Conceptos de autenticación de la teoría

## 🚀 Desarrollo Paso a Paso

### Paso 1: Instalar Dependencias (15 min)

#### Actualizar requirements.txt

```text
# Dependencias existentes
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23

# NUEVAS: Para autenticación
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

#### Instalar

```bash
pip install python-jose[cryptography] passlib[bcrypt] python-multipart
```

#### ¿Para qué sirve cada una?

- **`python-jose`**: Crear y verificar tokens JWT
- **`passlib[bcrypt]`**: Hash seguro de passwords
- **`python-multipart`**: Para formularios de login

---

### Paso 2: Configurar Hashing de Passwords (25 min)

#### Crear archivo `auth.py`

```python
# auth.py
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

# Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración JWT (en producción usar variables de entorno)
SECRET_KEY = "mi-clave-super-secreta-cambiar-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def hash_password(password: str) -> str:
    """Convertir password a hash seguro"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar si password coincide con el hash"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(username: str) -> str:
    """Crear JWT token para un usuario"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": username,  # subject = usuario
        "exp": expire     # expiration = cuándo expira
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> str:
    """Verificar token y obtener username"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
```

#### Probar funciones básicas

```python
# Crear archivo test_auth.py para probar
from auth import hash_password, verify_password, create_access_token, verify_token

def test_password_hashing():
    password = "mi_password_123"

    # Hashear password
    hashed = hash_password(password)
    print(f"Password original: {password}")
    print(f"Password hasheado: {hashed}")

    # Verificar password
    is_valid = verify_password(password, hashed)
    print(f"Password es válido: {is_valid}")

    # Verificar password incorrecto
    is_invalid = verify_password("password_incorrecto", hashed)
    print(f"Password incorrecto es válido: {is_invalid}")

def test_jwt_tokens():
    username = "juan123"

    # Crear token
    token = create_access_token(username)
    print(f"Token creado: {token}")

    # Verificar token
    decoded_username = verify_token(token)
    print(f"Username desde token: {decoded_username}")

if __name__ == "__main__":
    print("=== Test Password Hashing ===")
    test_password_hashing()

    print("\n=== Test JWT Tokens ===")
    test_jwt_tokens()
```

**Ejecutar test:**

```bash
python test_auth.py
```

---

### Paso 3: Actualizar Modelo de Usuario (20 min)

#### Modificar models.py

```python
# models.py
from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)  # Guardamos el hash, NO el password
    is_active = Column(Boolean, default=True)
```

#### Crear schemas para autenticación

```python
# schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Recibimos password plano, lo hashearemos

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str

class LoginRequest(BaseModel):
    username: str
    password: str
```

#### Crear las tablas

```python
# Ejecutar para crear tabla actualizada
from database import engine
from models import Base

Base.metadata.create_all(bind=engine)
```

---

### Paso 4: Implementar Endpoints de Autenticación (30 min)

#### Añadir a main.py

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserResponse, Token, LoginRequest
from auth import hash_password, verify_password, create_access_token, verify_token

app = FastAPI(title="API con Autenticación Básica")
security = HTTPBearer()

# Endpoint de registro
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si usuario ya existe
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    # Verificar si email ya existe
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # Crear usuario con password hasheado
    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

# Endpoint de login
@app.post("/login", response_model=Token)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    # Buscar usuario
    user = db.query(User).filter(User.username == login_data.username).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Verificar password
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    # Crear token
    access_token = create_access_token(username=user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }

# Dependency para obtener usuario actual
def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    username = verify_token(token.credentials)
    if username is None:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user

# Endpoint protegido de ejemplo
@app.get("/profile", response_model=UserResponse)
def get_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Endpoint público para comparar
@app.get("/")
def read_root():
    return {"message": "API pública sin autenticación"}
```

---

## 🧪 Testing Manual

### 1. Iniciar servidor

```bash
uvicorn main:app --reload
```

### 2. Probar registro

```bash
# POST http://localhost:8000/register
{
    "username": "juan123",
    "email": "juan@email.com",
    "password": "password123"
}
```

### 3. Probar login

```bash
# POST http://localhost:8000/login
{
    "username": "juan123",
    "password": "password123"
}

# Response:
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer",
    "username": "juan123"
}
```

### 4. Probar endpoint protegido

```bash
# GET http://localhost:8000/profile
# Header: Authorization: Bearer [tu_token_aqui]
```

### 5. Verificar en Swagger

- Ir a `http://localhost:8000/docs`
- Hacer login y copiar el token
- Usar el botón "Authorize" en Swagger
- Probar endpoint `/profile`

---

## ✅ Checklist de Completado

- [ ] Dependencias instaladas
- [ ] Funciones de hashing funcionando
- [ ] Funciones JWT funcionando
- [ ] Modelo User actualizado
- [ ] Schemas de autenticación creados
- [ ] Endpoint de registro funcional
- [ ] Endpoint de login funcional
- [ ] Endpoint protegido funcional
- [ ] Testing manual completado
- [ ] Swagger funcionando con autenticación

---

## 🚨 Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'jose'"

```bash
# Instalar con la versión correcta
pip install python-jose[cryptography]
```

### Error: "password_hash not found"

- Verificar que creaste las tablas después de actualizar el modelo
- Ejecutar: `Base.metadata.create_all(bind=engine)`

### Error: "401 Unauthorized"

- Verificar que el token esté en el header correcto
- Formato: `Authorization: Bearer [token]`

### Token no funciona

- Verificar que la SECRET_KEY sea la misma para crear y verificar
- Verificar que el token no haya expirado (30 min por defecto)

---

## 📋 Resumen

### Lo que implementamos

- ✅ **Hashing seguro** de passwords con bcrypt
- ✅ **JWT básico** para autenticación
- ✅ **Registro de usuarios** con validación
- ✅ **Login con credenciales**
- ✅ **Protección de endpoints**

### Próximos pasos

1. Añadir más validaciones de password
2. Implementar roles de usuario
3. Mejorar manejo de errores
4. Añadir testing automatizado

¡Ya tienes autenticación básica funcionando! 🔐✨
