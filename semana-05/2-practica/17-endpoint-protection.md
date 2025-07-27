# Práctica 17: Protección de Endpoints

**⏱️ Tiempo estimado:** 90 minutos  
**🎯 Objetivo:** Implementar middleware y dependencies para proteger endpoints con autenticación

## 📋 En esta práctica aprenderás

- Crear middleware de autenticación personalizado
- Proteger endpoints individuales con dependencies
- Implementar diferentes niveles de protección
- Manejar excepciones de autorización
- Crear decoradores para simplificar la protección

## 🔧 Paso 1: Middleware de Autenticación

Crear `app/middleware/auth.py`:

```python
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from jose import JWTError, jwt
import time
from typing import List, Optional

from app.core.config import settings
from app.core.security import SECRET_KEY, ALGORITHM

class AuthenticationMiddleware(BaseHTTPMiddleware):
    """
    Middleware para verificar autenticación en rutas protegidas
    """

    def __init__(self, app: ASGIApp, protected_paths: List[str] = None):
        super().__init__(app)
        # Rutas que requieren autenticación
        self.protected_paths = protected_paths or [
            "/api/v1/protected",
            "/api/v1/admin",
            "/api/v1/users/me"
        ]
        # Rutas públicas (excluidas de autenticación)
        self.public_paths = [
            "/",
            "/health",
            "/docs",
            "/openapi.json",
            "/api/v1/auth/register",
            "/api/v1/auth/login",
        ]

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Verificar si la ruta requiere autenticación
        path = request.url.path
        requires_auth = any(path.startswith(protected) for protected in self.protected_paths)
        is_public = any(path.startswith(public) for public in self.public_paths)

        if requires_auth and not is_public:
            # Extraer token del header
            authorization = request.headers.get("Authorization")

            if not authorization:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Token de autenticación requerido"}
                )

            try:
                # Verificar formato del token
                scheme, token = authorization.split()
                if scheme.lower() != "bearer":
                    raise ValueError("Esquema de autenticación inválido")

                # Decodificar y validar token
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

                # Agregar información del usuario al request
                request.state.user_id = payload.get("user_id")
                request.state.username = payload.get("sub")

            except (ValueError, JWTError, AttributeError):
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"detail": "Token inválido o expirado"}
                )

        # Continuar con el request
        response = await call_next(request)

        # Agregar headers de tiempo de procesamiento
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware para rate limiting básico
    """

    def __init__(self, app: ASGIApp, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}  # En producción usar Redis

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        # Limpiar requests antiguos
        if client_ip in self.requests:
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if current_time - req_time < self.window_seconds
            ]

        # Verificar límite
        if client_ip not in self.requests:
            self.requests[client_ip] = []

        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": f"Demasiadas requests. Límite: {self.max_requests} por {self.window_seconds} segundos"
                }
            )

        # Registrar request
        self.requests[client_ip].append(current_time)

        response = await call_next(request)
        return response
```

## 🔧 Paso 2: Dependencies de Autorización

Crear `app/dependencies/auth.py`:

```python
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency para obtener usuario actual activo
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user

def get_current_superuser(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Dependency para verificar que el usuario es superusuario
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes. Se requieren privilegios de administrador"
        )
    return current_user

def require_permissions(*required_permissions: str):
    """
    Factory para crear dependency que requiere permisos específicos

    Uso:
    @app.get("/admin/users")
    def get_users(user = Depends(require_permissions("read_users", "admin"))):
        pass
    """
    def permission_dependency(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> User:
        # En una implementación real, verificarías permisos en BD
        # Por ahora, solo verificamos si es superuser
        user_permissions = []
        if current_user.is_superuser:
            user_permissions = ["admin", "read_users", "write_users", "delete_users"]

        for permission in required_permissions:
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permiso requerido: {permission}"
                )

        return current_user

    return permission_dependency

def optional_authentication(
    request: Request,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency para autenticación opcional
    Retorna el usuario si está autenticado, None si no
    """
    try:
        user = get_current_user(request, db)
        return user
    except HTTPException:
        return None

class RequireOwnership:
    """
    Dependency class para verificar que el usuario es propietario del recurso
    """

    def __init__(self, resource_id_param: str = "resource_id"):
        self.resource_id_param = resource_id_param

    def __call__(
        self,
        request: Request,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
    ) -> User:
        # Obtener ID del recurso de los path parameters
        resource_id = request.path_params.get(self.resource_id_param)

        if not resource_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Parámetro {self.resource_id_param} requerido"
            )

        # Verificar ownership (implementación específica según el recurso)
        # Ejemplo: verificar que user_id == current_user.id
        if str(resource_id) != str(current_user.id) and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso"
            )

        return current_user
```

## 🔧 Paso 3: Decoradores de Protección

Crear `app/decorators/auth.py`:

```python
from functools import wraps
from fastapi import HTTPException, status
from typing import Callable, List
import asyncio

def require_auth(func: Callable) -> Callable:
    """
    Decorador para requerir autenticación en endpoints
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # El usuario debe ser pasado como dependency
        current_user = kwargs.get('current_user')
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Autenticación requerida"
            )

        if asyncio.iscoroutinefunction(func):
            return await func(*args, **kwargs)
        return func(*args, **kwargs)

    return wrapper

def require_roles(*roles: str):
    """
    Decorador para requerir roles específicos
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Autenticación requerida"
                )

            # Verificar roles (implementación básica)
            user_roles = []
            if current_user.is_superuser:
                user_roles = ["admin", "user"]
            else:
                user_roles = ["user"]

            for role in roles:
                if role not in user_roles:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Rol requerido: {role}"
                    )

            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper
    return decorator

def api_key_required(api_key_header: str = "X-API-Key"):
    """
    Decorador para requerir API key
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get('request')
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Request object not found"
                )

            api_key = request.headers.get(api_key_header)
            if not api_key:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=f"API key requerida en header {api_key_header}"
                )

            # Verificar API key (implementación básica)
            valid_api_keys = ["test-api-key-123", "prod-api-key-456"]
            if api_key not in valid_api_keys:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="API key inválida"
                )

            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)

        return wrapper
    return decorator
```

## 🔧 Paso 4: Endpoints Protegidos de Ejemplo

Crear `app/api/protected.py`:

```python
from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.schemas.auth import UserResponse
from app.dependencies.auth import (
    get_current_active_user,
    get_current_superuser,
    require_permissions,
    optional_authentication,
    RequireOwnership
)
from app.decorators.auth import require_auth, require_roles, api_key_required

router = APIRouter(prefix="/protected", tags=["Protected Routes"])

@router.get("/profile", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_active_user)
):
    """
    Obtener perfil del usuario autenticado
    Requiere: Token JWT válido
    """
    return UserResponse.model_validate(current_user)

@router.get("/admin-only")
def admin_only_endpoint(
    current_user: User = Depends(get_current_superuser)
):
    """
    Endpoint solo para administradores
    Requiere: Token JWT + privilegios de admin
    """
    return {
        "message": "¡Acceso permitido! Eres administrador",
        "user": current_user.username,
        "admin": True
    }

@router.get("/users-management")
def manage_users(
    current_user: User = Depends(require_permissions("read_users", "admin")),
    db: Session = Depends(get_db)
):
    """
    Gestión de usuarios
    Requiere: Permisos específicos
    """
    # Simular obtener todos los usuarios
    return {
        "message": "Lista de usuarios (solo para admins)",
        "authorized_by": current_user.username,
        "permissions": ["read_users", "admin"]
    }

@router.get("/user/{user_id}")
def get_user_data(
    user_id: int,
    current_user: User = Depends(RequireOwnership("user_id"))
):
    """
    Obtener datos de usuario específico
    Requiere: Ser propietario del recurso o admin
    """
    return {
        "message": f"Datos del usuario {user_id}",
        "accessed_by": current_user.username,
        "authorized": True
    }

@router.get("/public-or-private")
def flexible_endpoint(
    current_user: User = Depends(optional_authentication)
):
    """
    Endpoint que cambia comportamiento según autenticación
    """
    if current_user:
        return {
            "message": "Contenido personalizado para usuario autenticado",
            "user": current_user.username,
            "authenticated": True
        }
    else:
        return {
            "message": "Contenido público para usuarios anónimos",
            "authenticated": False
        }

@router.get("/with-api-key")
@api_key_required()
def api_key_endpoint(request: Request):
    """
    Endpoint que requiere API key
    Requiere: X-API-Key header
    """
    return {
        "message": "Acceso autorizado con API key",
        "api_key": request.headers.get("X-API-Key")
    }

@router.get("/decorated-admin")
@require_roles("admin")
def decorated_admin_endpoint(current_user: User = Depends(get_current_active_user)):
    """
    Endpoint usando decorador de roles
    """
    return {
        "message": "Acceso con decorador de roles",
        "user": current_user.username,
        "roles": ["admin"]
    }

@router.post("/sensitive-action")
def sensitive_action(
    request: Request,
    current_user: User = Depends(get_current_superuser)
):
    """
    Acción sensible que requiere máximos privilegios
    """
    return {
        "message": "Acción sensible ejecutada",
        "executed_by": current_user.username,
        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent")
    }
```

## 🔧 Paso 5: Integrar Middleware en la Aplicación

Actualizar `app/main.py`:

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.middleware.auth import AuthenticationMiddleware, RateLimitMiddleware
from app.api import auth, protected

app = FastAPI(
    title="API con Protección de Endpoints",
    description="API con múltiples niveles de autenticación y autorización",
    version="1.0.0"
)

# Agregar middleware personalizado
app.add_middleware(RateLimitMiddleware, max_requests=100, window_seconds=60)
app.add_middleware(
    AuthenticationMiddleware,
    protected_paths=["/api/v1/protected", "/api/v1/admin"]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(protected.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {
        "message": "API con Protección de Endpoints",
        "authentication": "JWT Bearer Token",
        "endpoints": {
            "auth": "/api/v1/auth/",
            "protected": "/api/v1/protected/",
            "docs": "/docs"
        }
    }

@app.get("/public")
def public_endpoint():
    """Endpoint público sin protección"""
    return {
        "message": "Este es un endpoint público",
        "accessible": "sin autenticación"
    }
```

## 🧪 Paso 6: Testing de Protección

Crear `tests/test_protection.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_public_endpoint():
    """Test endpoint público"""
    response = client.get("/public")
    assert response.status_code == 200
    assert "público" in response.json()["message"]

def test_protected_endpoint_without_token():
    """Test endpoint protegido sin token"""
    response = client.get("/api/v1/protected/profile")
    assert response.status_code == 401
    assert "Token de autenticación requerido" in response.json()["detail"]

def test_protected_endpoint_with_invalid_token():
    """Test endpoint protegido con token inválido"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/protected/profile", headers=headers)
    assert response.status_code == 401
    assert "Token inválido" in response.json()["detail"]

def test_authentication_flow():
    """Test flujo completo de autenticación"""
    # 1. Registrar usuario
    register_data = {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "TestPass123"
    }

    response = client.post("/api/v1/auth/register", json=register_data)
    assert response.status_code == 201

    # 2. Login
    login_data = {
        "username": "testuser",
        "password": "TestPass123"
    }

    response = client.post("/api/v1/auth/login", json=login_data)
    assert response.status_code == 200

    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Acceder a endpoint protegido
    response = client.get("/api/v1/protected/profile", headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

def test_admin_endpoint_as_regular_user():
    """Test endpoint de admin con usuario regular"""
    # Aquí necesitarías crear un usuario regular y obtener token
    # Luego intentar acceder a endpoint de admin
    pass

def test_rate_limiting():
    """Test rate limiting middleware"""
    # Hacer muchas requests rápidas
    for i in range(110):  # Más del límite de 100
        response = client.get("/public")
        if i < 100:
            assert response.status_code == 200
        else:
            assert response.status_code == 429
```

## 🔧 Paso 7: Script de Prueba Manual

Crear `scripts/test_protection.py`:

```python
import requests
import time

BASE_URL = "http://localhost:8000/api/v1"

def test_protection_levels():
    """Probar diferentes niveles de protección"""

    print("=== Testing Protection Levels ===\n")

    # 1. Endpoint público
    print("1. Testing public endpoint...")
    response = requests.get("http://localhost:8000/public")
    print(f"Public endpoint: {response.status_code} - {response.json()['message']}")

    # 2. Endpoint protegido sin token
    print("\n2. Testing protected endpoint without token...")
    response = requests.get(f"{BASE_URL}/protected/profile")
    print(f"Protected without token: {response.status_code} - {response.json()['detail']}")

    # 3. Registrar y hacer login
    print("\n3. Registering and logging in...")

    register_data = {
        "username": "protectiontest",
        "email": "protection@test.com",
        "full_name": "Protection Test",
        "password": "SecurePass123"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    if response.status_code == 201:
        print("✅ User registered successfully")
    else:
        print(f"❌ Registration failed: {response.status_code}")
        return

    login_data = {
        "username": "protectiontest",
        "password": "SecurePass123"
    }

    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✅ Login successful, token obtained")
        headers = {"Authorization": f"Bearer {token}"}
    else:
        print(f"❌ Login failed: {response.status_code}")
        return

    # 4. Acceder a endpoints protegidos
    print("\n4. Testing protected endpoints with valid token...")

    endpoints = [
        "/protected/profile",
        "/protected/public-or-private",
        "/protected/admin-only",  # Este debería fallar
    ]

    for endpoint in endpoints:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        print(f"{endpoint}: {response.status_code}")
        if response.status_code == 200:
            print(f"  ✅ {response.json().get('message', 'Success')}")
        else:
            print(f"  ❌ {response.json().get('detail', 'Error')}")

    # 5. Test con API key
    print("\n5. Testing API key endpoint...")

    api_headers = {"X-API-Key": "test-api-key-123"}
    response = requests.get(f"{BASE_URL}/protected/with-api-key", headers=api_headers)
    print(f"API key endpoint: {response.status_code}")
    if response.status_code == 200:
        print(f"  ✅ {response.json()['message']}")
    else:
        print(f"  ❌ {response.json()['detail']}")

def test_rate_limiting():
    """Probar rate limiting"""
    print("\n=== Testing Rate Limiting ===\n")

    success_count = 0
    rate_limited = False

    for i in range(105):  # Intentar más del límite
        response = requests.get("http://localhost:8000/public")

        if response.status_code == 200:
            success_count += 1
        elif response.status_code == 429:
            print(f"Rate limited at request {i + 1}")
            rate_limited = True
            break

        if i % 20 == 0:
            print(f"Completed {i + 1} requests...")

    print(f"Successful requests: {success_count}")
    print(f"Rate limiting triggered: {rate_limited}")

if __name__ == "__main__":
    test_protection_levels()
    time.sleep(1)
    test_rate_limiting()
```

## ✅ Ejercicios de Práctica

1. **IP Whitelist**: Crear middleware que solo permita IPs específicas
2. **Session-based Auth**: Implementar autenticación basada en sesiones
3. **Two-Factor Auth**: Agregar autenticación de dos factores básica
4. **Resource Permissions**: Sistema granular de permisos por recurso

## 🎯 Entregables

- [ ] Middleware de autenticación funcionando
- [ ] Dependencies de autorización implementadas
- [ ] Endpoints protegidos con diferentes niveles
- [ ] Rate limiting básico funcionando
- [ ] Tests de protección pasando

## 📚 Conceptos Clave Aprendidos

- **Middleware**: Procesamiento de requests global
- **Dependencies**: Inyección de dependencias para auth
- **Decoradores**: Simplificación de protección
- **Rate Limiting**: Prevención de abuso
- **Levels of Protection**: Diferentes niveles de seguridad

---

## 🚨 Problemas Comunes

### Middleware no se ejecuta

```python
# Verificar orden de middleware en main.py
# Los middleware se ejecutan en orden inverso al registrado
```

### Dependencies circulares

```python
# Evitar imports circulares entre módulos
# Usar forward references cuando sea necesario
```

### Rate limiting no funciona

```python
# Verificar que el middleware esté antes que CORS
# En producción usar Redis para storage distribuido
```

¡Continúa con la [Práctica 18: Roles y Autorización](./18-roles-authorization.md)!
