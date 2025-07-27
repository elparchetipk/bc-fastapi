# Práctica 18: Roles Básicos

## 🎯 Objetivo

Implementar **roles de usuario básicos** (admin/user) en 90 minutos, usando un enfoque simple y funcional.

## ⏱️ Tiempo: 90 minutos

## 📋 Pre-requisitos

- ✅ Protección de endpoints funcionando (Práctica 17 completada)
- ✅ Sistema de autenticación completo
- ✅ Base de datos y modelos básicos

## 🚀 Desarrollo Paso a Paso

### Paso 1: Agregar Campo Role al Usuario (20 min)

#### Actualizar modelo User en `models.py`

```python
from sqlalchemy import Column, Integer, String, Boolean

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")  # NUEVO: campo role
```

#### Actualizar schemas

```python
from pydantic import BaseModel
from typing import Literal

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
    is_active: bool
    role: str  # NUEVO: incluir role en respuesta

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# NUEVO: Schema para actualizar roles (solo admin)
class UserRoleUpdate(BaseModel):
    role: Literal["user", "admin"]
```

#### Actualizar función create_user en `auth.py`

```python
def create_user(db: Session, username: str, email: str, password: str, role: str = "user"):
    """Crear usuario con password hasheado y role"""
    hashed_password = get_password_hash(password)

    db_user = User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        role=role  # NUEVO: asignar role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

---

### Paso 2: Funciones de Verificación de Roles (25 min)

#### Agregar funciones de roles en `auth.py`

```python
def require_admin(current_user: User = Depends(get_current_user)):
    """Dependencia que requiere rol de admin"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: se requiere rol de administrador"
        )
    return current_user

def get_all_users(db: Session):
    """Obtener todos los usuarios (solo admin)"""
    return db.query(User).all()

def update_user_role(db: Session, user_id: int, new_role: str):
    """Actualizar role de un usuario (solo admin)"""
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        return None

    user.role = new_role
    db.commit()
    db.refresh(user)
    return user

def create_admin_user(db: Session, username: str, email: str, password: str):
    """Crear usuario administrador"""
    return create_user(db, username, email, password, role="admin")
```

---

### Paso 3: Endpoints con Roles (30 min)

#### Actualizar endpoints en `main.py`

```python
# Importar las nuevas funciones y schemas
from . import auth

# Endpoint para crear primer admin (solo si no existe ningún admin)
@app.post("/create-admin", response_model=UserResponse)
def create_first_admin(user_data: UserRegister, db: Session = Depends(get_db)):
    """Crear primer usuario administrador"""

    # Verificar si ya existe un admin
    existing_admin = db.query(User).filter(User.role == "admin").first()

    if existing_admin:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un administrador en el sistema"
        )

    # Verificar si username ya existe
    if auth.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=400,
            detail="Username ya está registrado"
        )

    # Crear admin
    admin_user = auth.create_admin_user(
        db=db,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )

    return UserResponse(
        id=admin_user.id,
        username=admin_user.username,
        email=admin_user.email,
        is_active=admin_user.is_active,
        role=admin_user.role
    )

# Endpoint solo para admins: ver todos los usuarios
@app.get("/admin/users", response_model=List[UserResponse])
def list_all_users(
    admin_user: User = Depends(auth.require_admin),
    db: Session = Depends(get_db)
):
    """Listar todos los usuarios (solo admin)"""

    users = auth.get_all_users(db)

    return [UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
        role=user.role
    ) for user in users]

# Endpoint solo para admins: cambiar role de usuario
@app.put("/admin/users/{user_id}/role", response_model=UserResponse)
def update_user_role(
    user_id: int,
    role_data: UserRoleUpdate,
    admin_user: User = Depends(auth.require_admin),
    db: Session = Depends(get_db)
):
    """Actualizar role de un usuario (solo admin)"""

    # No permitir que el admin se cambie su propio rol
    if user_id == admin_user.id:
        raise HTTPException(
            status_code=400,
            detail="No puedes cambiar tu propio rol"
        )

    # Actualizar role
    updated_user = auth.update_user_role(db, user_id, role_data.role)

    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return UserResponse(
        id=updated_user.id,
        username=updated_user.username,
        email=updated_user.email,
        is_active=updated_user.is_active,
        role=updated_user.role
    )

# Actualizar endpoint de registro para incluir role en respuesta
@app.post("/register", response_model=UserResponse)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """Registrar nuevo usuario"""

    if auth.get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=400,
            detail="Username ya está registrado"
        )

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
        is_active=user.is_active,
        role=user.role  # NUEVO: incluir role
    )
```

---

### Paso 4: Testing Manual de Roles (15 min)

#### Paso 1: Crear primer admin

```bash
# Crear usuario administrador
curl -X POST "http://127.0.0.1:8000/create-admin" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "admin",
       "email": "admin@test.com",
       "password": "admin123"
     }'
```

**Resultado esperado:**

```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@test.com",
  "is_active": true,
  "role": "admin"
}
```

#### Paso 2: Login como admin y usar endpoints protegidos

```bash
# 1. Login como admin
curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin123"}'

# 2. Ver todos los usuarios (solo admin)
curl -X GET "http://127.0.0.1:8000/admin/users" \
     -H "Authorization: Bearer TOKEN_DEL_ADMIN"

# 3. Cambiar role de usuario (solo admin)
curl -X PUT "http://127.0.0.1:8000/admin/users/2/role" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer TOKEN_DEL_ADMIN" \
     -d '{"role": "admin"}'
```

#### Paso 3: Probar acceso denegado

```bash
# Registrar usuario normal
curl -X POST "http://127.0.0.1:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "usuario",
       "email": "user@test.com",
       "password": "user123"
     }'

# Login como usuario normal
curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "usuario", "password": "user123"}'

# Intentar acceder a endpoint de admin (debe fallar)
curl -X GET "http://127.0.0.1:8000/admin/users" \
     -H "Authorization: Bearer TOKEN_DEL_USUARIO"
```

**Resultado esperado (error 403):**

```json
{
  "detail": "Acceso denegado: se requiere rol de administrador"
}
```

---

## ✅ Checklist de Completado

### Funcionalidad Básica

- [ ] Campo `role` agregado al modelo User
- [ ] Función `require_admin` implementada
- [ ] Endpoint `/create-admin` funcionando
- [ ] Endpoints `/admin/*` protegidos por rol

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

**Has implementado un sistema básico de roles** con:

1. **Roles de usuario** (user/admin) en la base de datos
2. **Protección por rol** usando dependencias
3. **Endpoints de administración** solo para admins
4. **Testing completo** del sistema de roles

**🚀 Siguiente:** En el proyecto final integrarás todo el sistema de autenticación y autorización.

---

## 📚 Conceptos Aplicados

- **Role-based access control** básico
- **Dependencias anidadas** para verificación de roles
- **HTTP 403 Forbidden** para autorización
- **Admin endpoints** para gestión de usuarios
- **Primera ejecución** para crear admin inicial

**¡Sistema de roles implementado exitosamente!** 👑
