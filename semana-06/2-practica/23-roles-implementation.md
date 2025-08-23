# Práctica 23: Roles y Autorización

## 🎯 Objetivo

Implementar **sistema completo de roles** (admin/user) con testing, en 105 minutos, construyendo sobre la base de autenticación de la Semana 5.

## ⏱️ Tiempo: 105 minutos

## 📋 Pre-requisitos

- ✅ Autenticación JWT funcionando (Semana 5)
- ✅ Testing básico configurado (Prácticas 19-21)
- ✅ Endpoints protegidos implementados

---

## 🚀 Desarrollo Paso a Paso

### Paso 1: Implementar Modelo de Roles (25 min)

#### Actualizar modelo User en `app/models/user.py`

```python
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # NUEVO: campo role
```

#### Actualizar schemas en `app/schemas/user.py`

```python
from pydantic import BaseModel
from typing import Literal

class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    role: str  # NUEVO: incluir role en respuesta

class UserRoleUpdate(BaseModel):
    role: Literal["user", "admin"]

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
```

#### Migrar base de datos

```bash
# Si usas Alembic (recomendado)
alembic revision --autogenerate -m "Add role field to users"
alembic upgrade head

# Si usas recreación simple
# Eliminar database.db y dejar que se recree
```

---

### Paso 2: Funciones de Autorización (30 min)

#### Actualizar `app/auth/dependencies.py`

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.database import get_db
from app.models.user import User
from app.auth.jwt_handler import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """Obtener usuario actual del token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user

async def require_admin(
    current_user: User = Depends(get_current_user)
):
    """Dependencia que requiere rol de administrador"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: admin role required"
        )
    return current_user

async def require_active_user(
    current_user: User = Depends(get_current_user)
):
    """Dependencia que requiere usuario activo"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: inactive user"
        )
    return current_user
```

---

### Paso 3: Endpoints con Roles (35 min)

#### Crear `app/routers/admin.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserRoleUpdate
from app.auth.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users", response_model=List[UserResponse])
async def list_all_users(
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Listar todos los usuarios (solo admin)"""
    users = db.query(User).all()

    return [UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        role=user.role
    ) for user in users]

@router.put("/users/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    """Actualizar rol de un usuario (solo admin)"""

    # No permitir que el admin se cambie su propio rol
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.role = role_data.role
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        role=user.role
    )

@router.post("/create-first-admin", response_model=UserResponse)
async def create_first_admin(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """Crear primer administrador (solo si no existe ningún admin)"""

    # Verificar si ya existe un admin
    existing_admin = db.query(User).filter(User.role == "admin").first()
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin user already exists"
        )

    # Verificar si email ya existe
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Crear admin
    from app.auth.password import get_password_hash

    admin_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        role="admin"
    )

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)

    return UserResponse(
        id=admin_user.id,
        email=admin_user.email,
        full_name=admin_user.full_name,
        is_active=admin_user.is_active,
        role=admin_user.role
    )
```

#### Actualizar `app/main.py`

```python
from fastapi import FastAPI
from app.routers import auth, admin  # NUEVO: importar admin

app = FastAPI(title="API with Authentication and Roles")

# Incluir routers
app.include_router(auth.router)
app.include_router(admin.router)  # NUEVO: incluir admin router

@app.get("/")
async def root():
    return {"message": "API with Authentication and Roles"}
```

---

### Paso 4: Testing de Roles (15 min)

#### Crear `tests/test_roles.py`

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth.jwt_handler import create_access_token

def test_admin_can_list_users(client, admin_user, admin_headers):
    """Test que admin puede listar usuarios"""
    response = client.get("/admin/users", headers=admin_headers)

    assert response.status_code == 200
    users = response.json()
    assert len(users) >= 1
    assert any(user["role"] == "admin" for user in users)

def test_regular_user_cannot_access_admin_endpoints(client, test_user, auth_headers):
    """Test que usuario normal no puede acceder a endpoints de admin"""
    response = client.get("/admin/users", headers=auth_headers)

    assert response.status_code == 403
    assert "admin role required" in response.json()["detail"]

def test_admin_can_change_user_role(client, admin_user, test_user, admin_headers):
    """Test que admin puede cambiar rol de usuario"""
    response = client.put(
        f"/admin/users/{test_user.id}/role",
        json={"role": "admin"},
        headers=admin_headers
    )

    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["role"] == "admin"

def test_admin_cannot_change_own_role(client, admin_user, admin_headers):
    """Test que admin no puede cambiar su propio rol"""
    response = client.put(
        f"/admin/users/{admin_user.id}/role",
        json={"role": "user"},
        headers=admin_headers
    )

    assert response.status_code == 400
    assert "Cannot change your own role" in response.json()["detail"]

def test_create_first_admin_success(client):
    """Test crear primer admin cuando no existe ninguno"""
    admin_data = {
        "email": "newadmin@example.com",
        "full_name": "New Admin",
        "password": "adminpass123"
    }

    response = client.post("/admin/create-first-admin", json=admin_data)

    assert response.status_code == 200
    admin = response.json()
    assert admin["role"] == "admin"
    assert admin["email"] == admin_data["email"]

def test_cannot_create_admin_when_exists(client, admin_user):
    """Test que no se puede crear admin cuando ya existe uno"""
    admin_data = {
        "email": "another@example.com",
        "full_name": "Another Admin",
        "password": "adminpass123"
    }

    response = client.post("/admin/create-first-admin", json=admin_data)

    assert response.status_code == 400
    assert "Admin user already exists" in response.json()["detail"]
```

#### Actualizar `tests/conftest.py` para incluir admin fixtures

```python
@pytest.fixture
def admin_user(db):
    """Fixture para usuario administrador."""
    from app.models.user import User
    from app.auth.password import get_password_hash

    admin_data = {
        "email": "admin@example.com",
        "full_name": "Admin User",
        "hashed_password": get_password_hash("adminpass123"),
        "role": "admin"
    }
    admin = User(**admin_data)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin

@pytest.fixture
def admin_headers(admin_user):
    """Fixture para headers de administrador."""
    token = create_access_token({"sub": admin_user.email})
    return {"Authorization": f"Bearer {token}"}
```

---

## ✅ Testing Manual Rápido

### 1. Crear primer admin

```bash
curl -X POST "http://127.0.0.1:8000/admin/create-first-admin" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@test.com",
       "full_name": "Admin User",
       "password": "admin123"
     }'
```

### 2. Login como admin

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@test.com&password=admin123"
```

### 3. Listar usuarios (con token de admin)

```bash
curl -X GET "http://127.0.0.1:8000/admin/users" \
     -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

---

## ✅ Checklist de Completado

### Funcionalidad Básica

- [ ] Campo `role` agregado al modelo User
- [ ] Función `require_admin` implementada y funcionando
- [ ] Endpoint `/admin/create-first-admin` funcionando
- [ ] Endpoint `/admin/users` listando usuarios
- [ ] Endpoint `/admin/users/{id}/role` cambiando roles

### Testing Automatizado

- [ ] Tests de autorización funcionando
- [ ] Tests de endpoints admin implementados
- [ ] Fixtures para admin y usuarios normales
- [ ] Tests de casos de error funcionando

### Testing Manual

- [ ] Creación de admin exitosa
- [ ] Login de admin funcionando
- [ ] Acceso a endpoints de admin exitoso
- [ ] Error 403 para usuarios sin permisos

### Comprensión

- [ ] Entiendes la diferencia entre autenticación y autorización
- [ ] Comprendes cómo funcionan las dependencias para roles
- [ ] Sabes crear endpoints específicos por rol

---

## 🎯 Objetivo Alcanzado

**Has implementado un sistema completo de roles** con:

1. **Modelo de roles** en base de datos
2. **Dependencias de autorización** funcionales
3. **Endpoints administrativos** protegidos
4. **Testing automatizado** de autorización
5. **Testing manual** verificado

**🚀 Siguiente:** En la consolidación integrarás todo el sistema completo.

---

## 📚 Conceptos Aplicados

- **Role-based Access Control (RBAC)** básico
- **Dependencias anidadas** para verificación de roles
- **HTTP 403 Forbidden** para autorización denegada
- **Admin endpoints** para gestión de usuarios
- **Testing de autorización** automatizado

**¡Sistema de roles completamente implementado y probado!** 👑
