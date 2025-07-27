# Teoría - Semana 5: Autenticación Básica

## 📖 Introducción

En las semanas anteriores aprendimos a crear APIs con base de datos. Ahora necesitamos **proteger** nuestra API para que solo **usuarios autorizados** puedan acceder a ciertos datos.

---

## 🎯 Objetivos de Aprendizaje

Al finalizar esta semana podrás:

- Entender qué es autenticación y autorización
- Implementar login básico con username/password
- Crear un sistema simple de tokens
- Proteger endpoints específicos

---

## 🔐 Conceptos Básicos

### ¿Qué es Autenticación?

**Autenticación** = Verificar **quién eres**

```python
# Ejemplo: Usuario envía credenciales
{
    "username": "juan123",
    "password": "mi_password_secreto"
}

# Sistema verifica: ¿Esta persona es realmente juan123?
```

### ¿Qué es Autorización?

**Autorización** = Verificar **qué puedes hacer**

```python
# Ejemplo: Juan está autenticado, pero...
# ¿Puede Juan eliminar productos? → Solo si es admin
# ¿Puede Juan ver sus propios pedidos? → Sí
# ¿Puede Juan ver pedidos de otros? → No
```

### Flujo Simple

```text
1. Usuario envía username + password
2. API verifica en base de datos
3. Si es correcto → Crear token
4. Usuario usa token para acceder
5. API verifica token en cada request
```

---

## 👤 Sistema de Usuarios Básico

### Modelo de Usuario

```python
# models.py
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)  # ¡NUNCA guardar password en texto plano!
    is_active = Column(Boolean, default=True)
```

### Schema de Usuario

```python
# schemas.py
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True
```

---

## 🔒 Hashing de Passwords

### ¿Por qué NO guardar passwords directamente?

```python
# ❌ MUY PELIGROSO
user.password = "123456"  # Si hackean la BD, ven todos los passwords
```

### Usar Hashing

**Hashing** = Convertir password en texto ilegible que **no se puede revertir**

```python
# ✅ SEGURO
password = "123456"
password_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"

# Es imposible obtener "123456" desde el hash
```

### Implementación Simple

```python
# auth.py
from passlib.context import CryptContext

# Configurar hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Convertir password a hash"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verificar si password coincide con hash"""
    return pwd_context.verify(plain_password, hashed_password)
```

---

## 🎫 Tokens Simples

### ¿Qué es un Token?

Un **token** es como una **credencial temporal** que demuestra que ya te autenticaste.

```text
Ejemplo: Token en un evento
1. Compras entrada (autenticación)
2. Te dan una pulsera (token)
3. Usas la pulsera para entrar a diferentes áreas (autorización)
4. La pulsera expira al final del día
```

### Token JWT Básico

```python
# jwt_handler.py
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "tu_clave_super_secreta"  # En producción: variable de entorno
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(username: str) -> str:
    """Crear token para un usuario"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": username,  # subject = usuario
        "exp": expire     # expiration = cuándo expira
    }
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str) -> str:
    """Verificar token y obtener username"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        return username
    except jwt.PyJWTError:
        return None  # Token inválido
```

---

## 🚪 Endpoints de Autenticación

### Registro de Usuario

```python
@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si usuario ya existe
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Crear nuevo usuario
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
```

### Login de Usuario

```python
@app.post("/login")
def login_user(username: str, password: str, db: Session = Depends(get_db)):
    # Buscar usuario en BD
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Verificar password
    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Crear token
    access_token = create_access_token(username=user.username)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "username": user.username
    }
```

---

## 🛡️ Proteger Endpoints

### Dependency para Obtener Usuario Actual

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

security = HTTPBearer()

def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    """Obtener usuario actual desde token"""
    username = verify_token(token.credentials)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
```

### Endpoints Protegidos

```python
# Endpoint público (sin protección)
@app.get("/products")
def get_products():
    return {"products": ["Laptop", "Phone", "Tablet"]}

# Endpoint protegido (necesita autenticación)
@app.get("/profile", response_model=UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

# Endpoint solo para admin
@app.delete("/admin/users/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verificar si es admin (simplificado)
    if current_user.username != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # Eliminar usuario
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()

    return {"message": "User deleted"}
```

---

## 🧪 Cómo Probar

### 1. Registrar Usuario

```bash
POST /register
{
    "username": "juan123",
    "email": "juan@email.com",
    "password": "password123"
}
```

### 2. Hacer Login

```bash
POST /login
{
    "username": "juan123",
    "password": "password123"
}

# Response:
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

### 3. Usar Token

```bash
GET /profile
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

---

## 📋 Resumen de Conceptos

### Lo que aprendimos

- ✅ **Autenticación vs Autorización**
- ✅ **Hashing de passwords** con bcrypt
- ✅ **Tokens JWT básicos**
- ✅ **Endpoints de registro y login**
- ✅ **Protección de endpoints**

### Dependencias necesarias

```bash
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install python-multipart
```

### Próximos pasos

1. Implementar el sistema completo
2. Añadir roles de usuario (admin, user)
3. Mejorar manejo de errores
4. Añadir refresh tokens
5. Implementar testing de autenticación

---

## 🎉 Conclusión

¡Ya estás listo para crear APIs seguras! 🔐✨
