# Práctica 16: Endpoints de Login y Register

## 🎯 Objetivo

Crear **endpoints básicos de registro y login** en 90 minutos, aplicando JWT y hashing de passwords de forma simple.

## ⏱️ Tiempo: 90 minutos

## 📋 Pre-requisitos

- ✅ JWT y hashing configurados (Práctica 15 completada)
- ✅ Base de datos funcionando
- ✅ Archivo `auth.py` con funciones básicas

## 🚀 Desarrollo Paso a Paso

### Paso 1: Modelo de Usuario Simple (20 min)

#### Crear `models.py` para usuarios

```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
```

#### Schemas básicos

```python
from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
```

---

### Paso 2: Funciones CRUD Básicas (25 min)

#### Ampliar `auth.py` con funciones de usuario

```python
# Agregar al archivo auth.py existente
from sqlalchemy.orm import Session
from .models import User

def create_user(db: Session, username: str, email: str, password: str):
    """Crear usuario con password hasheado"""
    hashed_password = get_password_hash(password)

    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    """Obtener usuario por username"""
    return db.query(User).filter(User.username == username).first()

def authenticate_user(db: Session, username: str, password: str):
    """Verificar usuario y password"""
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
```

---

### Paso 3: Endpoints de Registro y Login (30 min)

#### Crear endpoints en `main.py`

```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from . import auth, models
from .database import SessionLocal, engine

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependencia de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=UserResponse)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""

    # Verificar si usuario ya existe
    if auth.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=400,
            detail="Username ya está registrado"
        )

    # Crear usuario
    user = auth.create_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active
    )

@app.post("/login", response_model=Token)
def login_user(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login y obtener token"""

    # Autenticar usuario
    user = auth.authenticate_user(db, user_data.username, user_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o password incorrecto",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token
    access_token_expires = timedelta(minutes=30)
    access_token = auth.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(auth.get_current_user)):
    """Obtener usuario actual"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active
    )
```

---

### Paso 4: Testing Manual Básico (15 min)

#### Probar registro

```bash
# Registrar usuario
curl -X POST "http://127.0.0.1:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "juan",
       "email": "juan@test.com",
       "password": "mi_password"
     }'
```

**Resultado esperado:**

```json
{
  "id": 1,
  "username": "juan",
  "email": "juan@test.com",
  "is_active": true
}
```

#### Probar login

```bash
# Hacer login
curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "juan",
       "password": "mi_password"
     }'
```

**Resultado esperado:**

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Probar acceso protegido

```bash
# Usar el token obtenido
curl -X GET "http://127.0.0.1:8000/users/me" \
     -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**Resultado esperado:**

```json
{
  "id": 1,
  "username": "juan",
  "email": "juan@test.com",
  "is_active": true
}
```

---

## ✅ Checklist de Completado

### Funcionalidad Básica

- [ ] Modelo User creado y migraciones aplicadas
- [ ] Esquemas Pydantic definidos
- [ ] Funciones CRUD básicas implementadas
- [ ] Endpoint `/register` funcionando
- [ ] Endpoint `/login` retornando JWT
- [ ] Endpoint `/users/me` protegido funcionando

### Testing Manual

- [ ] Registro de usuario exitoso
- [ ] Login exitoso con token válido
- [ ] Acceso a ruta protegida con token
- [ ] Error 401 sin token
- [ ] Error 400 con usuario duplicado

### Comprensión

- [ ] Entiendes el flujo registro → login → token → acceso
- [ ] Sabes cómo hashear y verificar passwords
- [ ] Comprendes la validación de JWT

---

## 🎯 Objetivo Alcanzado

**Has implementado un sistema básico de autenticación** con:

1. **Registro de usuarios** con password hasheado
2. **Login** que retorna JWT válido
3. **Protección de rutas** usando tokens
4. **Testing manual** para verificar funcionalidad

**🚀 Siguiente:** En el proyecto de la semana integrarás todo lo aprendido en un sistema completo.

---

## 📚 Conceptos Aplicados

- **Hashing seguro** de passwords con bcrypt
- **JWT tokens** para autenticación stateless
- **Protección de endpoints** con dependencias
- **Manejo de errores** HTTP apropiados
- **CRUD básico** para usuarios

**¡Sistema de autenticación completado exitosamente!** 🎉
