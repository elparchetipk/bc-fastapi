# Práctica 15: JWT y Hashing de Passwords

**⏱️ Tiempo estimado:** 90 minutos  
**🎯 Objetivo:** Implementar autenticación JWT con hashing seguro de passwords

## 📋 En esta práctica aprenderás

- Configurar librerías de seguridad (passlib, python-jose)
- Implementar hashing seguro de passwords con bcrypt
- Crear y validar JSON Web Tokens (JWT)
- Configurar variables de entorno para secrets
- Estructurar módulos de seguridad en FastAPI

## 🗂️ Estructura del Proyecto

```text
auth_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── security.py    # ← NUEVO: Funciones de seguridad
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py        # ← ACTUALIZADO: Con password hash
│   └── schemas/
│       ├── __init__.py
│       └── auth.py        # ← NUEVO: Schemas de autenticación
├── .env                   # ← NUEVO: Variables de entorno
├── .env.example          # ← NUEVO: Ejemplo de configuración
└── requirements.txt       # ← ACTUALIZADO: Nuevas dependencias
```

## 🔧 Paso 1: Instalar Dependencias

### Actualizar requirements.txt

```text
# Dependencias existentes
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pydantic==2.5.0
alembic==1.13.0

# NUEVAS: Dependencias de seguridad
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

### Instalar nuevas dependencias

```bash
# Instalar las nuevas librerías
pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# O instalar desde requirements.txt
pip install -r requirements.txt
```

### ¿Qué hace cada librería?

- **`python-jose`**: Creación y validación de JWT tokens
- **`passlib[bcrypt]`**: Hashing seguro de passwords con bcrypt
- **`python-multipart`**: Para manejar formularios con FastAPI OAuth2

## 🔧 Paso 2: Configuración de Entorno

### Crear archivo `.env`

```bash
# Configuración de seguridad
SECRET_KEY=tu-clave-super-secreta-aqui-cambiar-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Configuración de base de datos
DATABASE_URL=sqlite:///./auth_app.db

# Configuración de desarrollo
DEBUG=True
```

### Crear archivo `.env.example`

```bash
# COPY THIS FILE TO .env AND FILL WITH REAL VALUES

# Security Settings
SECRET_KEY=your-secret-key-here-minimum-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Settings
DATABASE_URL=sqlite:///./app.db

# Development Settings
DEBUG=True
```

### Generar SECRET_KEY segura

```python
# Script para generar clave secreta
import secrets

# Generar clave aleatoria de 32 bytes (256 bits)
secret_key = secrets.token_urlsafe(32)
print(f"SECRET_KEY={secret_key}")

# Ejemplo de output:
# SECRET_KEY=dGhpc19pc19hX3Zlcnlfc2VjdXJlX2tleV90aGF0X2lzXzI1Nl9iaXRz
```

## 🔧 Paso 3: Configuración Central

### Crear `app/core/config.py`

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Security settings
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database settings
    DATABASE_URL: str = "sqlite:///./app.db"

    # App settings
    DEBUG: bool = False
    APP_NAME: str = "Auth API"
    VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia global de configuración
settings = Settings()

# Validación básica
if len(settings.SECRET_KEY) < 32:
    raise ValueError("SECRET_KEY debe tener al menos 32 caracteres")

print(f"🔧 Configuración cargada: {settings.APP_NAME} v{settings.VERSION}")
print(f"🔒 Algorithm: {settings.ALGORITHM}")
print(f"⏰ Token expiration: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes")
```

### ¿Por qué usar pydantic_settings?

- **Validación automática** de tipos y valores
- **Carga desde .env** automáticamente
- **Documentación** de configuración centralizada
- **Type hints** para mejor IDE support

## 🔧 Paso 4: Módulo de Seguridad

### Crear `app/core/security.py`

```python
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# Configuración de hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verificar si una password en texto plano coincide con el hash

    Args:
        plain_password: Password en texto plano
        hashed_password: Password hasheada

    Returns:
        bool: True si coinciden, False si no
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Generar hash seguro de una password

    Args:
        password: Password en texto plano

    Returns:
        str: Password hasheada con bcrypt
    """
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crear JWT token de acceso

    Args:
        data: Datos a incluir en el token (claims)
        expires_delta: Tiempo de expiración personalizado

    Returns:
        str: JWT token codificado
    """
    to_encode = data.copy()

    # Calcular tiempo de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Añadir claims estándar
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })

    # Codificar token
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodificar y validar JWT token

    Args:
        token: JWT token codificado

    Returns:
        dict: Payload del token si es válido, None si no
    """
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        # Verificar que sea un token de acceso
        if payload.get("type") != "access":
            return None

        return payload

    except JWTError:
        return None

def verify_token_signature(token: str) -> bool:
    """
    Verificar solo la firma del token (sin validar expiración)

    Args:
        token: JWT token codificado

    Returns:
        bool: True si la firma es válida
    """
    try:
        jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": False}  # No verificar expiración
        )
        return True
    except JWTError:
        return False

# Funciones de utilidad para testing y debugging
def decode_token_unsafe(token: str) -> dict:
    """
    Decodificar token SIN verificar firma (solo para debugging)

    ⚠️ NUNCA usar en producción
    """
    import json
    import base64

    # Dividir token en partes
    header, payload, signature = token.split('.')

    # Decodificar payload (añadir padding si necesario)
    payload += '=' * (4 - len(payload) % 4)
    decoded_payload = base64.urlsafe_b64decode(payload)

    return json.loads(decoded_payload)

def get_token_info(token: str) -> dict:
    """
    Obtener información del token para debugging
    """
    try:
        # Decodificar sin verificar
        payload = decode_token_unsafe(token)

        # Verificar firma
        signature_valid = verify_token_signature(token)

        # Verificar expiración
        exp = payload.get('exp', 0)
        now = datetime.utcnow().timestamp()
        is_expired = now > exp

        return {
            "signature_valid": signature_valid,
            "is_expired": is_expired,
            "expires_at": datetime.fromtimestamp(exp).isoformat() if exp else None,
            "issued_at": datetime.fromtimestamp(payload.get('iat', 0)).isoformat() if payload.get('iat') else None,
            "subject": payload.get('sub'),
            "type": payload.get('type'),
            "payload": payload
        }
    except Exception as e:
        return {"error": str(e), "token_invalid": True}
```

## 🔧 Paso 5: Esquemas de Autenticación

### Crear `app/schemas/auth.py`

```python
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Schema base para usuario"""
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    email: EmailStr = Field(..., description="Email válido del usuario")
    full_name: Optional[str] = Field(None, max_length=100, description="Nombre completo del usuario")
    is_active: bool = Field(True, description="Si el usuario está activo")

class UserCreate(UserBase):
    """Schema para crear usuario"""
    password: str = Field(..., min_length=8, max_length=100, description="Password del usuario")

    @validator('password')
    def validate_password(cls, v):
        """Validar fortaleza de password"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password debe contener al menos una mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Password debe contener al menos una minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password debe contener al menos un número')
        return v

    @validator('username')
    def validate_username(cls, v):
        """Validar formato de username"""
        if not v.isalnum():
            raise ValueError('Username debe ser alfanumérico')
        return v.lower()  # Convertir a minúsculas

class UserResponse(UserBase):
    """Schema para respuesta de usuario (sin password)"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserInDB(UserBase):
    """Schema para usuario en base de datos"""
    id: int
    hashed_password: str
    created_at: datetime

    class Config:
        from_attributes = True

# Schemas de autenticación
class LoginRequest(BaseModel):
    """Schema para request de login"""
    username: str = Field(..., description="Username o email")
    password: str = Field(..., description="Password del usuario")

class Token(BaseModel):
    """Schema para response de token"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Tipo de token")
    expires_in: int = Field(..., description="Segundos hasta expiración")

class TokenData(BaseModel):
    """Schema para datos dentro del token"""
    username: Optional[str] = None
    user_id: Optional[int] = None

# Schemas para cambio de password
class PasswordChange(BaseModel):
    """Schema para cambiar password"""
    current_password: str = Field(..., description="Password actual")
    new_password: str = Field(..., min_length=8, description="Nueva password")

    @validator('new_password')
    def validate_new_password(cls, v):
        """Validar nueva password"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password debe contener al menos una mayúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Password debe contener al menos una minúscula')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password debe contener al menos un número')
        return v

class PasswordReset(BaseModel):
    """Schema para reset de password"""
    email: EmailStr = Field(..., description="Email del usuario")
```

## 🔧 Paso 6: Modelo de Usuario con Password

### Actualizar `app/models/user.py`

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)  # ← NUEVO: Password hasheada
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

    @property
    def is_authenticated(self):
        """Siempre True para usuarios válidos"""
        return True

    @property
    def is_anonymous(self):
        """Siempre False para usuarios registrados"""
        return False
```

## 🔧 Paso 7: Testing de Funciones de Seguridad

### Crear script de testing `test_security.py`

```python
#!/usr/bin/env python3
"""
Script para probar funciones de seguridad
Ejecutar: python test_security.py
"""

from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    get_token_info
)
from datetime import timedelta
import time

def test_password_hashing():
    """Probar hashing y verificación de passwords"""
    print("🔐 Testing Password Hashing...")

    # Password de prueba
    password = "MySecurePassword123"

    # Generar hash
    hashed = get_password_hash(password)
    print(f"Password: {password}")
    print(f"Hash: {hashed}")

    # Verificar password correcta
    is_valid = verify_password(password, hashed)
    print(f"✅ Password correcta: {is_valid}")

    # Verificar password incorrecta
    is_invalid = verify_password("WrongPassword", hashed)
    print(f"❌ Password incorrecta: {is_invalid}")

    # Verificar que hash es diferente cada vez
    hash2 = get_password_hash(password)
    print(f"✅ Hashes son diferentes: {hashed != hash2}")
    print()

def test_jwt_tokens():
    """Probar creación y validación de JWT"""
    print("🎫 Testing JWT Tokens...")

    # Datos para el token
    token_data = {
        "sub": "testuser",
        "user_id": 123,
        "username": "testuser"
    }

    # Crear token
    token = create_access_token(token_data)
    print(f"Token creado: {token[:50]}...")

    # Decodificar token
    decoded = decode_access_token(token)
    if decoded:
        print("✅ Token decodificado correctamente:")
        print(f"  - Subject: {decoded.get('sub')}")
        print(f"  - User ID: {decoded.get('user_id')}")
        print(f"  - Expires: {decoded.get('exp')}")
    else:
        print("❌ Error decodificando token")

    # Probar token inválido
    invalid_decoded = decode_access_token("invalid.token.here")
    print(f"❌ Token inválido decodificado: {invalid_decoded}")
    print()

def test_token_expiration():
    """Probar expiración de tokens"""
    print("⏰ Testing Token Expiration...")

    # Crear token con expiración muy corta
    token_data = {"sub": "testuser"}
    short_token = create_access_token(
        token_data,
        expires_delta=timedelta(seconds=2)
    )

    print("Token con expiración de 2 segundos creado")

    # Verificar inmediatamente
    decoded = decode_access_token(short_token)
    print(f"✅ Token válido inmediatamente: {decoded is not None}")

    # Esperar y verificar nuevamente
    print("Esperando 3 segundos...")
    time.sleep(3)

    decoded_expired = decode_access_token(short_token)
    print(f"❌ Token expirado después de 3s: {decoded_expired is None}")
    print()

def test_token_info():
    """Probar función de información de token"""
    print("📊 Testing Token Info...")

    # Crear token
    token_data = {"sub": "testuser", "role": "admin"}
    token = create_access_token(token_data)

    # Obtener información
    info = get_token_info(token)
    print("Información del token:")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print()

if __name__ == "__main__":
    print("🧪 Testing Security Functions\n")
    print("=" * 50)

    try:
        test_password_hashing()
        test_jwt_tokens()
        test_token_expiration()
        test_token_info()

        print("✅ Todos los tests completados exitosamente!")

    except Exception as e:
        print(f"❌ Error en testing: {e}")
        import traceback
        traceback.print_exc()
```

### Ejecutar tests

```bash
# Ejecutar script de testing
python test_security.py

# Output esperado:
# 🧪 Testing Security Functions
# ==================================================
# 🔐 Testing Password Hashing...
# Password: MySecurePassword123
# Hash: $2b$12$...
# ✅ Password correcta: True
# ❌ Password incorrecta: False
# ✅ Hashes son diferentes: True
# ...
```

## 🔧 Paso 8: Endpoint Básico de Testing

### Actualizar `app/main.py`

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    decode_access_token,
    get_token_info
)
from app.schemas.auth import Token
from pydantic import BaseModel

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas para testing
class PasswordTest(BaseModel):
    password: str

class TokenTest(BaseModel):
    username: str
    user_id: int = 1

class TokenValidation(BaseModel):
    token: str

@app.get("/")
async def root():
    """Endpoint raíz"""
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.VERSION,
        "docs": "/docs"
    }

@app.post("/test/hash-password")
async def test_hash_password(data: PasswordTest):
    """Testing: Generar hash de password"""
    hashed = get_password_hash(data.password)
    return {
        "original": data.password,
        "hashed": hashed,
        "verify": verify_password(data.password, hashed)
    }

@app.post("/test/create-token", response_model=Token)
async def test_create_token(data: TokenTest):
    """Testing: Crear JWT token"""
    token_data = {
        "sub": data.username,
        "user_id": data.user_id
    }

    access_token = create_access_token(token_data)

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )

@app.post("/test/validate-token")
async def test_validate_token(data: TokenValidation):
    """Testing: Validar JWT token"""
    decoded = decode_access_token(data.token)

    if not decoded:
        raise HTTPException(status_code=401, detail="Token inválido")

    info = get_token_info(data.token)

    return {
        "valid": True,
        "decoded": decoded,
        "info": info
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": settings.VERSION
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
```

### Probar los endpoints

```bash
# Ejecutar servidor
uvicorn app.main:app --reload

# Ir a http://localhost:8000/docs para probar endpoints
```

### Ejemplos de testing con curl

```bash
# 1. Test hash password
curl -X POST "http://localhost:8000/test/hash-password" \
     -H "Content-Type: application/json" \
     -d '{"password": "MySecurePassword123"}'

# 2. Test create token
curl -X POST "http://localhost:8000/test/create-token" \
     -H "Content-Type: application/json" \
     -d '{"username": "testuser", "user_id": 123}'

# 3. Test validate token (usar token del paso anterior)
curl -X POST "http://localhost:8000/test/validate-token" \
     -H "Content-Type: application/json" \
     -d '{"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."}'
```

## ✅ Ejercicios de Práctica

### Ejercicio 1: Fortaleza de Passwords

Implementa una función que valide la fortaleza de passwords:

```python
def validate_password_strength(password: str) -> dict:
    """
    Validar fortaleza de password

    Returns:
        dict: Score y recomendaciones
    """
    score = 0
    issues = []

    # Implementar validaciones:
    # - Longitud mínima 8 caracteres
    # - Al menos una mayúscula
    # - Al menos una minúscula
    # - Al menos un número
    # - Al menos un carácter especial
    # - No passwords comunes (123456, password, etc.)

    return {
        "score": score,
        "strength": "weak|medium|strong",
        "issues": issues
    }
```

### Ejercicio 2: Token Claims Personalizados

Extiende la creación de tokens para incluir claims personalizados:

```python
def create_access_token_with_permissions(
    username: str,
    user_id: int,
    permissions: list,
    role: str = "user"
) -> str:
    """Crear token con permisos y role"""
    # Implementar
    pass
```

### Ejercicio 3: Blacklist de Tokens

Implementa un sistema básico de blacklist para tokens:

```python
# In-memory blacklist (en producción usar Redis)
token_blacklist = set()

def blacklist_token(token: str):
    """Añadir token a blacklist"""
    # Implementar
    pass

def is_token_blacklisted(token: str) -> bool:
    """Verificar si token está en blacklist"""
    # Implementar
    pass
```

## 🎯 Entregables

- [ ] Configuración de seguridad funcionando
- [ ] Functions de hashing y JWT implementadas
- [ ] Tests de seguridad pasando
- [ ] Endpoints de testing funcionando
- [ ] Variables de entorno configuradas
- [ ] Ejercicios completados

## 📚 Conceptos Clave Aprendidos

- **bcrypt**: Hashing seguro con salt automático
- **JWT**: Estructura, claims, firma digital
- **Variables de entorno**: Configuración segura
- **Pydantic Settings**: Configuración tipada
- **Validación**: Fortaleza de passwords

---

## 🚨 Problemas Comunes

### Error: "ModuleNotFoundError: No module named 'jose'"

```bash
# Solución: Instalar con extras
pip install python-jose[cryptography]
```

### Error: "bcrypt not found"

```bash
# Solución: Instalar bcrypt
pip install passlib[bcrypt]
```

### Error: "SECRET_KEY too short"

```python
# Generar clave más larga
import secrets
print(secrets.token_urlsafe(32))
```

¡Continúa con la [Práctica 16: Sistema de Login y Register](./16-login-system.md)!
