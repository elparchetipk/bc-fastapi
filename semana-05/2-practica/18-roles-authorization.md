# Práctica 18: Roles y Autorización

**⏱️ Tiempo estimado:** 90 minutos  
**🎯 Objetivo:** Implementar un sistema completo de roles y permisos con RBAC (Role-Based Access Control)

## 📋 En esta práctica aprenderás

- Diseñar sistema de roles y permisos en base de datos
- Implementar RBAC (Role-Based Access Control)
- Crear middleware de autorización por roles
- Gestionar permisos granulares por recurso
- Implementar jerarquías de roles

## 🗂️ Estructura del Proyecto

```text
auth_api/
├── app/
│   ├── models/
│   │   ├── user.py        # ← ACTUALIZADO: Con relaciones a roles
│   │   ├── role.py        # ← NUEVO: Modelo de roles
│   │   └── permission.py  # ← NUEVO: Modelo de permisos
│   ├── schemas/
│   │   ├── role.py        # ← NUEVO: Schemas de roles
│   │   └── permission.py  # ← NUEVO: Schemas de permisos
│   ├── crud/
│   │   ├── role.py        # ← NUEVO: CRUD de roles
│   │   └── permission.py  # ← NUEVO: CRUD de permisos
│   ├── api/
│   │   ├── roles.py       # ← NUEVO: Endpoints de roles
│   │   └── admin.py       # ← NUEVO: Endpoints de admin
│   └── core/
│       └── rbac.py        # ← NUEVO: Sistema RBAC
```

## 🔧 Paso 1: Modelos de Roles y Permisos

### Crear `app/models/role.py`:

```python
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Tabla intermedia para relación Many-to-Many entre roles y permisos
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True),
    Column('granted_at', DateTime(timezone=True), server_default=func.now())
)

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_system_role = Column(Boolean, default=False)  # Roles del sistema no editables
    hierarchy_level = Column(Integer, default=0)  # 0 = más bajo, mayor número = más privilegios
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relaciones
    users = relationship("User", back_populates="role")
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )

    def __repr__(self):
        return f"<Role(name='{self.name}', level={self.hierarchy_level})>"
```

### Crear `app/models/permission.py`:

```python
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.models.role import role_permissions

class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    resource = Column(String(50), nullable=False)  # users, products, orders, etc.
    action = Column(String(20), nullable=False)    # create, read, update, delete, admin
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    roles = relationship(
        "Role",
        secondary=role_permissions,
        back_populates="permissions"
    )

    def __repr__(self):
        return f"<Permission(name='{self.name}', resource='{self.resource}', action='{self.action}')>"

    @property
    def full_name(self):
        """Nombre completo del permiso: resource.action"""
        return f"{self.resource}.{self.action}"
```

### Actualizar `app/models/user.py`:

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
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

    # Relación con roles
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    role = relationship("Role", back_populates="users")

    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role.name if self.role else None}')>"

    def has_permission(self, permission_name: str) -> bool:
        """Verificar si el usuario tiene un permiso específico"""
        if self.is_superuser:
            return True

        if not self.role or not self.role.is_active:
            return False

        return any(
            perm.name == permission_name and perm.is_active
            for perm in self.role.permissions
        )

    def has_resource_permission(self, resource: str, action: str) -> bool:
        """Verificar permiso por recurso y acción"""
        permission_name = f"{resource}.{action}"
        return self.has_permission(permission_name)

    def get_all_permissions(self) -> list:
        """Obtener todos los permisos del usuario"""
        if self.is_superuser:
            return ["*"]  # Superusuario tiene todos los permisos

        if not self.role or not self.role.is_active:
            return []

        return [
            perm.name for perm in self.role.permissions
            if perm.is_active
        ]
```

## 🔧 Paso 2: Schemas para Roles y Permisos

### Crear `app/schemas/role.py`:

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

from app.schemas.permission import PermissionResponse

class RoleBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Nombre del rol")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del rol")
    hierarchy_level: int = Field(default=0, ge=0, le=100, description="Nivel jerárquico (0-100)")

class RoleCreate(RoleBase):
    permission_ids: Optional[List[int]] = Field(default=[], description="IDs de permisos a asignar")

class RoleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    hierarchy_level: Optional[int] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None
    permission_ids: Optional[List[int]] = None

class RoleResponse(RoleBase):
    id: int
    is_active: bool
    is_system_role: bool
    created_at: datetime
    updated_at: Optional[datetime]
    permissions: List[PermissionResponse] = []
    user_count: Optional[int] = None

    class Config:
        from_attributes = True

class RoleWithUsers(RoleResponse):
    users: List["UserBasic"] = []

class UserBasic(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool

    class Config:
        from_attributes = True

# Prevenir import circular
RoleWithUsers.model_rebuild()
```

### Crear `app/schemas/permission.py`:

```python
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class PermissionBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Nombre único del permiso")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del permiso")
    resource: str = Field(..., min_length=2, max_length=50, description="Recurso (users, products, etc.)")
    action: str = Field(..., min_length=2, max_length=20, description="Acción (create, read, update, delete)")

    @validator('name')
    def validate_name_format(cls, v, values):
        """Validar que el nombre siga el formato resource.action"""
        if 'resource' in values and 'action' in values:
            expected = f"{values['resource']}.{values['action']}"
            if v != expected:
                raise ValueError(f"Nombre debe ser '{expected}' para este recurso y acción")
        return v

    @validator('action')
    def validate_action(cls, v):
        """Validar que la acción sea válida"""
        valid_actions = ['create', 'read', 'update', 'delete', 'admin', 'list', 'export']
        if v not in valid_actions:
            raise ValueError(f"Acción debe ser una de: {', '.join(valid_actions)}")
        return v

class PermissionCreate(PermissionBase):
    pass

class PermissionUpdate(BaseModel):
    description: Optional[str] = Field(None, max_length=500)
    is_active: Optional[bool] = None

class PermissionResponse(PermissionBase):
    id: int
    is_active: bool
    created_at: datetime
    full_name: str

    class Config:
        from_attributes = True

class PermissionWithRoles(PermissionResponse):
    roles: List["RoleBasic"] = []

class RoleBasic(BaseModel):
    id: int
    name: str
    description: Optional[str]
    hierarchy_level: int
    is_active: bool

    class Config:
        from_attributes = True

# Prevenir import circular
PermissionWithRoles.model_rebuild()
```

## 🔧 Paso 3: CRUD para Roles y Permisos

### Crear `app/crud/role.py`:

```python
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func, and_
from typing import List, Optional

from app.models.role import Role
from app.models.permission import Permission
from app.models.user import User
from app.schemas.role import RoleCreate, RoleUpdate

class RoleCRUD:

    def create_role(self, db: Session, role_data: RoleCreate) -> Role:
        """Crear nuevo rol con permisos"""

        # Verificar que el nombre no exista
        existing = db.query(Role).filter(Role.name == role_data.name).first()
        if existing:
            raise ValueError("El nombre del rol ya existe")

        # Crear rol
        db_role = Role(
            name=role_data.name,
            description=role_data.description,
            hierarchy_level=role_data.hierarchy_level
        )

        # Agregar permisos si se especificaron
        if role_data.permission_ids:
            permissions = db.query(Permission).filter(
                Permission.id.in_(role_data.permission_ids)
            ).all()
            db_role.permissions = permissions

        db.add(db_role)
        db.commit()
        db.refresh(db_role)

        return db_role

    def get_role(self, db: Session, role_id: int) -> Optional[Role]:
        """Obtener rol por ID con permisos"""
        return db.query(Role).options(
            selectinload(Role.permissions)
        ).filter(Role.id == role_id).first()

    def get_role_by_name(self, db: Session, name: str) -> Optional[Role]:
        """Obtener rol por nombre"""
        return db.query(Role).filter(Role.name == name).first()

    def get_roles(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True
    ) -> List[Role]:
        """Obtener lista de roles"""
        query = db.query(Role).options(selectinload(Role.permissions))

        if active_only:
            query = query.filter(Role.is_active == True)

        return query.offset(skip).limit(limit).all()

    def update_role(self, db: Session, role_id: int, role_update: RoleUpdate) -> Optional[Role]:
        """Actualizar rol"""
        db_role = db.query(Role).filter(Role.id == role_id).first()
        if not db_role:
            return None

        # No permitir editar roles del sistema
        if db_role.is_system_role:
            raise ValueError("No se pueden editar roles del sistema")

        # Actualizar campos
        update_data = role_update.model_dump(exclude_unset=True)

        if 'permission_ids' in update_data:
            permission_ids = update_data.pop('permission_ids')
            if permission_ids is not None:
                permissions = db.query(Permission).filter(
                    Permission.id.in_(permission_ids)
                ).all()
                db_role.permissions = permissions

        for field, value in update_data.items():
            setattr(db_role, field, value)

        db.commit()
        db.refresh(db_role)

        return db_role

    def delete_role(self, db: Session, role_id: int) -> bool:
        """Eliminar rol (soft delete)"""
        db_role = db.query(Role).filter(Role.id == role_id).first()
        if not db_role:
            return False

        # No permitir eliminar roles del sistema
        if db_role.is_system_role:
            raise ValueError("No se pueden eliminar roles del sistema")

        # Verificar que no tenga usuarios asignados
        user_count = db.query(User).filter(User.role_id == role_id).count()
        if user_count > 0:
            raise ValueError(f"No se puede eliminar el rol. Tiene {user_count} usuarios asignados")

        db_role.is_active = False
        db.commit()

        return True

    def assign_role_to_user(self, db: Session, user_id: int, role_id: int) -> bool:
        """Asignar rol a usuario"""
        user = db.query(User).filter(User.id == user_id).first()
        role = db.query(Role).filter(Role.id == role_id).first()

        if not user or not role:
            return False

        if not role.is_active:
            raise ValueError("No se puede asignar un rol inactivo")

        user.role_id = role_id
        db.commit()

        return True

    def get_roles_hierarchy(self, db: Session) -> List[Role]:
        """Obtener roles ordenados por jerarquía"""
        return db.query(Role).filter(
            Role.is_active == True
        ).order_by(Role.hierarchy_level.desc()).all()

    def get_role_statistics(self, db: Session) -> dict:
        """Obtener estadísticas de roles"""
        total_roles = db.query(Role).count()
        active_roles = db.query(Role).filter(Role.is_active == True).count()
        system_roles = db.query(Role).filter(Role.is_system_role == True).count()

        # Usuarios por rol
        users_by_role = db.query(
            Role.name,
            func.count(User.id).label('user_count')
        ).outerjoin(User).group_by(Role.id, Role.name).all()

        return {
            "total_roles": total_roles,
            "active_roles": active_roles,
            "system_roles": system_roles,
            "users_by_role": dict(users_by_role)
        }

# Instancia global del CRUD
role_crud = RoleCRUD()
```

### Crear `app/crud/permission.py`:

```python
from sqlalchemy.orm import Session, selectinload
from typing import List, Optional

from app.models.permission import Permission
from app.schemas.permission import PermissionCreate, PermissionUpdate

class PermissionCRUD:

    def create_permission(self, db: Session, permission_data: PermissionCreate) -> Permission:
        """Crear nuevo permiso"""

        # Verificar que el nombre no exista
        existing = db.query(Permission).filter(Permission.name == permission_data.name).first()
        if existing:
            raise ValueError("El permiso ya existe")

        db_permission = Permission(**permission_data.model_dump())
        db.add(db_permission)
        db.commit()
        db.refresh(db_permission)

        return db_permission

    def get_permission(self, db: Session, permission_id: int) -> Optional[Permission]:
        """Obtener permiso por ID"""
        return db.query(Permission).options(
            selectinload(Permission.roles)
        ).filter(Permission.id == permission_id).first()

    def get_permission_by_name(self, db: Session, name: str) -> Optional[Permission]:
        """Obtener permiso por nombre"""
        return db.query(Permission).filter(Permission.name == name).first()

    def get_permissions(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        resource: Optional[str] = None,
        active_only: bool = True
    ) -> List[Permission]:
        """Obtener lista de permisos"""
        query = db.query(Permission)

        if active_only:
            query = query.filter(Permission.is_active == True)

        if resource:
            query = query.filter(Permission.resource == resource)

        return query.offset(skip).limit(limit).all()

    def update_permission(
        self,
        db: Session,
        permission_id: int,
        permission_update: PermissionUpdate
    ) -> Optional[Permission]:
        """Actualizar permiso"""
        db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not db_permission:
            return None

        update_data = permission_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_permission, field, value)

        db.commit()
        db.refresh(db_permission)

        return db_permission

    def delete_permission(self, db: Session, permission_id: int) -> bool:
        """Eliminar permiso (soft delete)"""
        db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
        if not db_permission:
            return False

        db_permission.is_active = False
        db.commit()

        return True

    def get_permissions_by_resource(self, db: Session, resource: str) -> List[Permission]:
        """Obtener permisos por recurso"""
        return db.query(Permission).filter(
            and_(Permission.resource == resource, Permission.is_active == True)
        ).all()

    def create_resource_permissions(self, db: Session, resource: str, actions: List[str]) -> List[Permission]:
        """Crear permisos estándar para un recurso"""
        permissions = []

        for action in actions:
            permission_name = f"{resource}.{action}"

            # Verificar si ya existe
            existing = self.get_permission_by_name(db, permission_name)
            if existing:
                permissions.append(existing)
                continue

            permission_data = PermissionCreate(
                name=permission_name,
                description=f"Permiso para {action} en {resource}",
                resource=resource,
                action=action
            )

            permission = self.create_permission(db, permission_data)
            permissions.append(permission)

        return permissions

# Instancia global del CRUD
permission_crud = PermissionCRUD()
```

## 🔧 Paso 4: Sistema RBAC

Crear `app/core/rbac.py`:

```python
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status

from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user

class RBACSystem:
    """Sistema de Control de Acceso Basado en Roles"""

    @staticmethod
    def check_permission(user: User, permission: str) -> bool:
        """Verificar si el usuario tiene el permiso específico"""
        return user.has_permission(permission)

    @staticmethod
    def check_resource_permission(user: User, resource: str, action: str) -> bool:
        """Verificar permiso por recurso y acción"""
        return user.has_resource_permission(resource, action)

    @staticmethod
    def check_hierarchy_level(user: User, min_level: int) -> bool:
        """Verificar si el usuario tiene el nivel jerárquico mínimo"""
        if user.is_superuser:
            return True

        if not user.role:
            return False

        return user.role.hierarchy_level >= min_level

    @staticmethod
    def can_manage_user(manager: User, target_user: User) -> bool:
        """Verificar si un usuario puede gestionar a otro"""
        if manager.is_superuser:
            return True

        if not manager.role or not target_user.role:
            return False

        # Solo puede gestionar usuarios de nivel inferior
        return manager.role.hierarchy_level > target_user.role.hierarchy_level

def require_permission(permission: str):
    """Dependency para requerir permiso específico"""
    def permission_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if not RBACSystem.check_permission(current_user, permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso requerido: {permission}"
            )
        return current_user

    return permission_checker

def require_resource_permission(resource: str, action: str):
    """Dependency para requerir permiso de recurso"""
    def resource_permission_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if not RBACSystem.check_resource_permission(current_user, resource, action):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso requerido: {resource}.{action}"
            )
        return current_user

    return resource_permission_checker

def require_hierarchy_level(min_level: int):
    """Dependency para requerir nivel jerárquico mínimo"""
    def hierarchy_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if not RBACSystem.check_hierarchy_level(current_user, min_level):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Nivel jerárquico insuficiente. Mínimo requerido: {min_level}"
            )
        return current_user

    return hierarchy_checker

def require_role(role_name: str):
    """Dependency para requerir rol específico"""
    def role_checker(
        current_user: User = Depends(get_current_user)
    ) -> User:
        if current_user.is_superuser:
            return current_user

        if not current_user.role or current_user.role.name != role_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Rol requerido: {role_name}"
            )
        return current_user

    return role_checker

class ResourceAccessControl:
    """Control de acceso granular por recurso"""

    @staticmethod
    def can_access_user_data(current_user: User, target_user_id: int) -> bool:
        """Verificar si puede acceder a datos de usuario específico"""
        # Propio usuario
        if current_user.id == target_user_id:
            return True

        # Admin puede acceder a todos
        if current_user.has_resource_permission("users", "admin"):
            return True

        # Manager puede acceder a usuarios de nivel inferior
        if current_user.has_resource_permission("users", "read"):
            # Aquí se implementaría lógica específica de jerarquía
            return True

        return False

    @staticmethod
    def can_modify_user(current_user: User, target_user: User) -> bool:
        """Verificar si puede modificar usuario específico"""
        # No puede modificarse a sí mismo en ciertos aspectos
        if current_user.id == target_user.id:
            return current_user.has_resource_permission("users", "update")

        # Admin puede modificar todos
        if current_user.has_resource_permission("users", "admin"):
            return True

        # Manager puede modificar usuarios de nivel inferior
        return RBACSystem.can_manage_user(current_user, target_user)

def require_resource_access(resource_id_param: str = "resource_id"):
    """Dependency para verificar acceso a recurso específico"""
    def access_checker(
        request,
        current_user: User = Depends(get_current_user)
    ) -> User:
        resource_id = request.path_params.get(resource_id_param)

        if not resource_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Parámetro {resource_id_param} requerido"
            )

        # Lógica específica según el tipo de recurso
        # Esto se implementaría según las necesidades del negocio

        return current_user

    return access_checker
```

## 🔧 Paso 5: Endpoints de Gestión de Roles

Crear `app/api/roles.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.role import RoleCreate, RoleUpdate, RoleResponse, RoleWithUsers
from app.crud.role import role_crud
from app.core.rbac import require_permission, require_resource_permission

router = APIRouter(prefix="/roles", tags=["Roles Management"])

@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("roles.create"))
):
    """
    Crear nuevo rol
    Requiere: permiso roles.create
    """
    try:
        role = role_crud.create_role(db=db, role_data=role_data)
        return RoleResponse.model_validate(role)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[RoleResponse])
def list_roles(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    active_only: bool = Query(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("roles.read"))
):
    """
    Listar roles
    Requiere: permiso roles.read
    """
    roles = role_crud.get_roles(db=db, skip=skip, limit=limit, active_only=active_only)
    return [RoleResponse.model_validate(role) for role in roles]

@router.get("/{role_id}", response_model=RoleWithUsers)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("roles.read"))
):
    """
    Obtener rol por ID
    Requiere: permiso roles.read
    """
    role = role_crud.get_role(db=db, role_id=role_id)
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return RoleWithUsers.model_validate(role)

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("roles.update"))
):
    """
    Actualizar rol
    Requiere: permiso roles.update
    """
    try:
        role = role_crud.update_role(db=db, role_id=role_id, role_update=role_update)
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        return RoleResponse.model_validate(role)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{role_id}")
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("roles.delete"))
):
    """
    Eliminar rol (soft delete)
    Requiere: permiso roles.delete
    """
    try:
        success = role_crud.delete_role(db=db, role_id=role_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado"
            )
        return {"message": "Rol eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/{role_id}/assign/{user_id}")
def assign_role_to_user(
    role_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("users.update"))
):
    """
    Asignar rol a usuario
    Requiere: permiso users.update
    """
    try:
        success = role_crud.assign_role_to_user(db=db, user_id=user_id, role_id=role_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario o rol no encontrado"
            )
        return {"message": f"Rol {role_id} asignado al usuario {user_id}"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/hierarchy/list", response_model=List[RoleResponse])
def get_roles_hierarchy(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("roles.read"))
):
    """
    Obtener roles ordenados por jerarquía
    Requiere: permiso roles.read
    """
    roles = role_crud.get_roles_hierarchy(db=db)
    return [RoleResponse.model_validate(role) for role in roles]

@router.get("/stats/summary")
def get_role_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("roles.admin"))
):
    """
    Obtener estadísticas de roles
    Requiere: permiso roles.admin
    """
    return role_crud.get_role_statistics(db=db)
```

## 🔧 Paso 6: Inicializar Roles y Permisos del Sistema

Crear `scripts/init_rbac.py`:

```python
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.crud.role import role_crud
from app.crud.permission import permission_crud
from app.schemas.role import RoleCreate
from app.schemas.permission import PermissionCreate

def init_system_permissions(db: Session):
    """Crear permisos básicos del sistema"""

    # Definir recursos y acciones
    resources_actions = {
        "users": ["create", "read", "update", "delete", "admin"],
        "roles": ["create", "read", "update", "delete", "admin"],
        "permissions": ["read", "admin"],
        "products": ["create", "read", "update", "delete", "list"],
        "orders": ["create", "read", "update", "delete", "list"],
        "reports": ["read", "export"]
    }

    permissions = []

    for resource, actions in resources_actions.items():
        print(f"Creando permisos para {resource}...")
        resource_permissions = permission_crud.create_resource_permissions(
            db=db, resource=resource, actions=actions
        )
        permissions.extend(resource_permissions)
        print(f"  ✅ Creados {len(resource_permissions)} permisos")

    return permissions

def init_system_roles(db: Session, permissions):
    """Crear roles básicos del sistema"""

    # Mapear permisos por nombre para fácil acceso
    perms_by_name = {perm.name: perm.id for perm in permissions}

    # Definir roles del sistema
    system_roles = [
        {
            "name": "superadmin",
            "description": "Administrador con todos los permisos",
            "hierarchy_level": 100,
            "permissions": list(perms_by_name.values())  # Todos los permisos
        },
        {
            "name": "admin",
            "description": "Administrador con permisos de gestión",
            "hierarchy_level": 80,
            "permissions": [
                perms_by_name["users.read"],
                perms_by_name["users.update"],
                perms_by_name["roles.read"],
                perms_by_name["products.admin"],
                perms_by_name["orders.admin"],
                perms_by_name["reports.read"],
            ]
        },
        {
            "name": "manager",
            "description": "Manager con permisos limitados",
            "hierarchy_level": 50,
            "permissions": [
                perms_by_name["users.read"],
                perms_by_name["products.read"],
                perms_by_name["products.update"],
                perms_by_name["orders.read"],
                perms_by_name["orders.update"],
                perms_by_name["reports.read"],
            ]
        },
        {
            "name": "employee",
            "description": "Empleado con permisos básicos",
            "hierarchy_level": 20,
            "permissions": [
                perms_by_name["products.read"],
                perms_by_name["orders.read"],
                perms_by_name["orders.create"],
                perms_by_name["orders.update"],
            ]
        },
        {
            "name": "customer",
            "description": "Cliente con acceso limitado",
            "hierarchy_level": 10,
            "permissions": [
                perms_by_name["products.read"],
                perms_by_name["orders.create"],
                perms_by_name["orders.read"],  # Solo sus propias órdenes
            ]
        }
    ]

    created_roles = []

    for role_data in system_roles:
        try:
            print(f"Creando rol: {role_data['name']}...")

            role_create = RoleCreate(
                name=role_data["name"],
                description=role_data["description"],
                hierarchy_level=role_data["hierarchy_level"],
                permission_ids=role_data["permissions"]
            )

            role = role_crud.create_role(db=db, role_data=role_create)

            # Marcar como rol del sistema
            role.is_system_role = True
            db.commit()

            created_roles.append(role)
            print(f"  ✅ Rol '{role.name}' creado con {len(role.permissions)} permisos")

        except ValueError as e:
            print(f"  ⚠️  Rol '{role_data['name']}' ya existe: {e}")

    return created_roles

def main():
    """Inicializar RBAC completo"""
    db = Session(bind=engine)

    try:
        print("🔧 Inicializando Sistema RBAC...")
        print("=" * 50)

        # 1. Crear permisos
        print("\n📋 Creando permisos del sistema...")
        permissions = init_system_permissions(db)
        print(f"✅ Total de permisos: {len(permissions)}")

        # 2. Crear roles
        print("\n👥 Creando roles del sistema...")
        roles = init_system_roles(db, permissions)
        print(f"✅ Total de roles: {len(roles)}")

        print("\n🎉 Inicialización RBAC completada exitosamente!")
        print("\nRoles creados:")
        for role in roles:
            print(f"  - {role.name} (nivel {role.hierarchy_level}): {len(role.permissions)} permisos")

    except Exception as e:
        print(f"❌ Error durante inicialización: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
```

## ✅ Ejercicios de Práctica

1. **Roles dinámicos**: Permitir crear roles personalizados por los admins
2. **Permisos temporales**: Implementar permisos con fecha de expiración
3. **Audit log**: Registrar cambios en roles y permisos
4. **Delegación**: Permitir que usuarios deleguen permisos temporalmente

## 🎯 Entregables

- [ ] Modelos de roles y permisos implementados
- [ ] Sistema RBAC funcionando
- [ ] Dependencies de autorización por roles
- [ ] Endpoints de gestión de roles
- [ ] Script de inicialización ejecutado

## 📚 Conceptos Clave Aprendidos

- **RBAC**: Role-Based Access Control
- **Jerarquías**: Niveles de acceso por roles
- **Permisos granulares**: Control fino por recurso/acción
- **Dependencies**: Inyección de autorización
- **Sistema escalable**: Roles y permisos configurables

---

¡Continúa con los [Ejercicios de Seguridad](../3-ejercicios/ejercicios-seguridad.md)!
