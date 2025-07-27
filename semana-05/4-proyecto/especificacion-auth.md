# Proyecto Semana 5: API con Autenticación

## 🎯 Objetivo del Proyecto

Crear una **API simple con autenticación completa** que integre todos los conceptos aprendidos en la Semana 5: JWT, hashing, protección de endpoints y roles básicos.

**⏱️ Tiempo estimado:** 4-6 horas  
**📅 Fecha de entrega:** Final de la Semana 5  
**🏆 Peso en la evaluación:** 40% de la calificación semanal

---

## 📋 Descripción del Proyecto

### Contexto del Negocio

Desarrollar el backend para una plataforma simple que permita:

- Registro y autenticación de usuarios
- Sistema de roles (admin/usuario)
- Gestión de productos (solo admins)
- Sistema de favoritos (usuarios autenticados)
- Protección de endpoints con JWT

### Tecnologías Requeridas

- **Framework:** FastAPI
- **Base de Datos:** SQLite con SQLAlchemy
- **Autenticación:** JWT con python-jose
- **Hashing:** bcrypt con passlib
- **Validación:** Pydantic

---

## 🏗️ Estructura del Proyecto

### Organización de Archivos

```text
proyecto-semana5/
├── main.py              # Aplicación principal con todos los endpoints
├── models.py            # Modelos SQLAlchemy
├── schemas.py           # Schemas Pydantic
├── auth.py              # Funciones de autenticación
├── database.py          # Configuración de base de datos
├── requirements.txt     # Dependencias
├── README.md           # Documentación
└── test_api.py         # Testing básico (opcional)
```

---

## 📋 Especificaciones Funcionales

### **Entidades del Sistema:**

1. **User**: Usuarios con autenticación y roles
2. **Product**: Productos del sistema (CRUD solo admin)
3. **Favorite**: Relación usuario-producto favorito

### **Funcionalidades Requeridas:**

- ✅ Registro de usuarios con password hasheado
- ✅ Login con JWT token
- ✅ Protección de endpoints con dependencias
- ✅ Roles: admin (gestiona productos) y user (favoritos)
- ✅ CRUD de productos (solo admins)
- ✅ Sistema de favoritos (usuarios autenticados)

---

## 🏗️ Especificación Técnica

### **1. Modelos de Base de Datos (models.py)**

```python
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # "user" o "admin"
    is_active = Column(Boolean, default=True)

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer)  # En centavos
    created_by = Column(Integer, ForeignKey("users.id"))

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
```

### **2. Schemas Pydantic (schemas.py)**

```python
from pydantic import BaseModel
from typing import Optional

# Schemas de Usuario
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool

# Schemas de Autenticación
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Schemas de Producto
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: int
    created_by: int

# Schemas de Favoritos
class FavoriteResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    product: ProductResponse
```

### **3. Funciones de Autenticación (auth.py)**

```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

SECRET_KEY = "tu-secret-key-super-secreto-cambiar-en-produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    # Implementar decodificación JWT y obtener usuario
    pass

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Se requiere rol de administrador")
    return current_user
```

---

## 📋 Endpoints Requeridos

### **Autenticación**

- `POST /register` - Registrar nuevo usuario
- `POST /login` - Login y obtener JWT token
- `GET /me` - Obtener perfil del usuario autenticado
- `POST /create-admin` - Crear primer administrador

### **Productos (Solo Admin)**

- `POST /products` - Crear producto
- `GET /products` - Listar productos (público)
- `PUT /products/{id}` - Actualizar producto
- `DELETE /products/{id}` - Eliminar producto

### **Favoritos (Usuario Autenticado)**

- `POST /favorites/{product_id}` - Agregar a favoritos
- `GET /favorites` - Ver mis favoritos
- `DELETE /favorites/{product_id}` - Quitar de favoritos

### **Administración (Solo Admin)**

- `GET /admin/users` - Listar todos los usuarios
- `PUT /admin/users/{id}/role` - Cambiar rol de usuario

---

## 📋 Criterios de Evaluación

### **Funcionalidad (60%)**

- [ ] Sistema de registro funcionando (10%)
- [ ] Login con JWT funcionando (10%)
- [ ] Endpoints protegidos correctamente (15%)
- [ ] CRUD de productos (admin only) (15%)
- [ ] Sistema de favoritos funcionando (10%)

### **Seguridad (25%)**

- [ ] Passwords hasheados correctamente (10%)
- [ ] JWT tokens válidos y seguros (10%)
- [ ] Autorización por roles funcionando (5%)

### **Código y Documentación (15%)**

- [ ] Código limpio y organizado (5%)
- [ ] README con instrucciones claras (5%)
- [ ] Comentarios donde sea necesario (5%)

---

## 🚀 Instrucciones de Entrega

### **1. Requisitos Técnicos**

```text
requirements.txt:
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

### **2. Testing Manual Obligatorio**

Probar todos los endpoints usando curl:

```bash
# 1. Crear admin inicial
curl -X POST "http://127.0.0.1:8000/create-admin" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "email": "admin@test.com", "password": "admin123"}'

# 2. Login como admin
curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'

# 3. Crear producto (solo admin)
curl -X POST "http://127.0.0.1:8000/products" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer TOKEN_ADMIN" \
     -d '{"name": "Laptop", "description": "Gaming laptop", "price": 150000}'

# 4. Registrar usuario normal
curl -X POST "http://127.0.0.1:8000/register" \
     -H "Content-Type: application/json" \
     -d '{"username": "usuario", "email": "user@test.com", "password": "user123"}'

# 5. Login como usuario y probar favoritos
curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "usuario", "password": "user123"}'

curl -X POST "http://127.0.0.1:8000/favorites/1" \
     -H "Authorization: Bearer TOKEN_USUARIO"
```

### **3. Documentación Requerida (README.md)**

````markdown
# Proyecto Semana 5 - API con Autenticación

## Descripción

API REST con autenticación JWT, roles y sistema de favoritos.

## Instalación

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
````

## Endpoints

### Autenticación

- POST /register - Registro de usuarios
- POST /login - Login con JWT
- GET /me - Perfil del usuario

### Productos (Admin)

- POST /products - Crear producto
- GET /products - Listar productos
- DELETE /products/{id} - Eliminar producto

### Favoritos (Usuario)

- POST /favorites/{id} - Agregar favorito
- GET /favorites - Ver favoritos

## Testing

[Incluir ejemplos de curl usados para probar]

## Usuarios de prueba

- Admin: admin/admin123
- Usuario: usuario/user123

---

## ✅ Checklist de Entrega

### **Antes de entregar, verificar:**

- [ ] Todos los endpoints funcionan correctamente
- [ ] Sistema de autenticación JWT implementado
- [ ] Roles admin/user funcionando
- [ ] Passwords se guardan hasheados
- [ ] README.md completo con instrucciones
- [ ] Testing manual documentado
- [ ] Código limpio y comentado

### **Archivos a entregar:**

- [ ] `main.py` - Aplicación principal
- [ ] `models.py` - Modelos de base de datos
- [ ] `schemas.py` - Schemas Pydantic
- [ ] `auth.py` - Funciones de autenticación
- [ ] `database.py` - Configuración de DB
- [ ] `requirements.txt` - Dependencias
- [ ] `README.md` - Documentación

---

## 🎯 Objetivo Alcanzado

Al completar este proyecto habrás demostrado:

1. **Dominio de autenticación** con JWT y hashing
2. **Implementación de autorización** por roles
3. **Protección de endpoints** con dependencias
4. **Desarrollo de API REST** completa y funcional
5. **Buenas prácticas** de seguridad en APIs

**¡Proyecto de autenticación completado exitosamente!** 🔐
