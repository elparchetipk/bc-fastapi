# 🔒 Ejercicios de Seguridad - Semana 5

## 📝 Información General

**Duración estimada:** 90-120 minutos  
**Nivel:** Intermedio  
**Prerequisitos:** Completar prácticas 15-18 de autenticación

---

## 🎯 Objetivos

- Reforzar conceptos de autenticación y autorización
- Practicar implementación de JWT y protección de endpoints
- Desarrollar habilidades de debugging en seguridad
- Aplicar buenas prácticas de seguridad en APIs

---

## 🔥 Ejercicios Prácticos

### **Ejercicio 1: Debugging JWT (20 minutos)**

Un token JWT no está funcionando correctamente. Identifica y corrige los errores:

```python
# ❌ Código con errores
from datetime import datetime, timedelta
import jwt

SECRET_KEY = "mi-secret-super-seguro"  # Error 1
ALGORITHM = "RS256"  # Error 2

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire.timestamp()})  # Error 3

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None
```

**🎯 Tu tarea:**

1. Identifica al menos 3 errores en el código
2. Corrige cada error explicando por qué estaba mal
3. Añade validación adicional para mejores prácticas

**💡 Pistas:**

- ¿Qué algoritmo deberías usar para secretos simétricos?
- ¿Cómo debería manejarse la expiración?
- ¿Es seguro el secret actual?

---

### **Ejercicio 2: Sistema de Roles Avanzado (25 minutos)**

Implementa un sistema de autorización más complejo:

```python
# 📋 Especificaciones
# Roles: admin, manager, employee, customer
# Permisos por endpoint:
# - GET /users -> admin, manager
# - POST /users -> admin
# - GET /products -> todos los roles
# - POST /products -> admin, manager
# - DELETE /products -> admin
# - GET /orders -> admin, manager, employee (solo sus órdenes)
# - POST /orders -> customer, employee
```

**🎯 Tu tarea:**

1. Crea un enum para roles y permisos
2. Implementa un decorador `@require_permission()`
3. Crea una función de verificación de permisos flexible
4. Implementa los endpoints con las restricciones correctas

**📝 Plantilla base:**

```python
from enum import Enum
from functools import wraps
from fastapi import HTTPException, Depends

class Role(Enum):
    # Completa aquí
    pass

class Permission(Enum):
    # Completa aquí
    pass

def require_permission(permission: Permission):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Tu implementación aquí
            pass
        return wrapper
    return decorator

# Ejemplo de uso:
@app.get("/users")
@require_permission(Permission.READ_USERS)
async def get_users():
    pass
```

---

### **Ejercicio 3: Seguridad de Passwords (20 minutos)**

Implementa validaciones robustas de contraseñas:

**🎯 Requisitos:**

- Mínimo 8 caracteres
- Al menos 1 mayúscula
- Al menos 1 minúscula
- Al menos 1 número
- Al menos 1 carácter especial
- No puede contener el username
- No puede ser una contraseña común

```python
from typing import List
import re

# Lista de contraseñas comunes (versión reducida)
COMMON_PASSWORDS = [
    "password", "123456", "password123", "admin", "qwerty",
    "abc123", "Password1", "welcome", "monkey", "dragon"
]

def validate_password(password: str, username: str = None) -> tuple[bool, List[str]]:
    """
    Valida una contraseña según criterios de seguridad.

    Returns:
        tuple: (es_valida, lista_de_errores)
    """
    errors = []

    # Tu implementación aquí

    return len(errors) == 0, errors

# Tests que deben pasar:
# validate_password("weak") -> (False, ["errores..."])
# validate_password("StrongP@ssw0rd") -> (True, [])
# validate_password("password123", "user") -> (False, ["es común"])
# validate_password("user123", "user") -> (False, ["contiene username"])
```

---

### **Ejercicio 4: Rate Limiting y Seguridad (25 minutos)**

Implementa un sistema básico de rate limiting para prevenir ataques:

**🎯 Especificaciones:**

- Máximo 5 intentos de login por IP en 15 minutos
- Máximo 100 requests por usuario autenticado por hora
- Máximo 10 requests por IP no autenticada por minuto

```python
from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
import time

class RateLimiter:
    def __init__(self):
        self.attempts = defaultdict(list)
        self.user_requests = defaultdict(list)
        self.ip_requests = defaultdict(list)

    def check_login_attempts(self, ip: str) -> bool:
        """Verifica si la IP puede intentar login"""
        # Tu implementación aquí
        pass

    def check_user_rate_limit(self, user_id: str) -> bool:
        """Verifica rate limit para usuario autenticado"""
        # Tu implementación aquí
        pass

    def check_ip_rate_limit(self, ip: str) -> bool:
        """Verifica rate limit para IP no autenticada"""
        # Tu implementación aquí
        pass

    def record_login_attempt(self, ip: str):
        """Registra un intento de login"""
        # Tu implementación aquí
        pass

# Middleware de ejemplo
rate_limiter = RateLimiter()

async def rate_limit_middleware(request: Request, call_next):
    # Tu implementación del middleware aquí
    pass
```

---

### **Ejercicio 5: Audit Trail (30 minutos)**

Crea un sistema de auditoría para eventos de seguridad:

**🎯 Funcionalidades:**

- Registrar logins exitosos/fallidos
- Registrar cambios de permisos
- Registrar accesos a datos sensibles
- Generar reportes de actividad

```python
from datetime import datetime
from enum import Enum
from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base

class AuditEventType(Enum):
    LOGIN_SUCCESS = "login_success"
    LOGIN_FAILURE = "login_failure"
    PERMISSION_CHANGE = "permission_change"
    DATA_ACCESS = "data_access"
    PASSWORD_CHANGE = "password_change"

class AuditLog(Base):
    __tablename__ = "audit_logs"

    # Completa la definición de la tabla
    pass

class AuditService:
    @staticmethod
    def log_event(
        event_type: AuditEventType,
        user_id: Optional[int] = None,
        ip_address: str = None,
        details: dict = None
    ):
        """Registra un evento de auditoría"""
        # Tu implementación aquí
        pass

    @staticmethod
    def get_user_activity(user_id: int, days: int = 30):
        """Obtiene actividad de un usuario"""
        # Tu implementación aquí
        pass

    @staticmethod
    def get_security_alerts(hours: int = 24):
        """Obtiene alertas de seguridad recientes"""
        # Tu implementación aquí
        pass

# Decorator para auditoría automática
def audit_action(event_type: AuditEventType):
    def decorator(func):
        # Tu implementación del decorator aquí
        pass
    return decorator
```

---

## 🧪 Ejercicios de Testing

### **Ejercicio 6: Testing de Autenticación (20 minutos)**

Crea tests completos para tu sistema de autenticación:

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

class TestAuth:
    def test_register_success(self):
        """Test registro exitoso"""
        # Tu implementación aquí
        pass

    def test_register_duplicate_email(self):
        """Test registro con email duplicado"""
        # Tu implementación aquí
        pass

    def test_login_success(self):
        """Test login exitoso"""
        # Tu implementación aquí
        pass

    def test_login_invalid_credentials(self):
        """Test login con credenciales inválidas"""
        # Tu implementación aquí
        pass

    def test_protected_endpoint_without_token(self):
        """Test acceso sin token"""
        # Tu implementación aquí
        pass

    def test_protected_endpoint_with_token(self):
        """Test acceso con token válido"""
        # Tu implementación aquí
        pass

    def test_protected_endpoint_expired_token(self):
        """Test acceso con token expirado"""
        # Tu implementación aquí
        pass

# Ejecutar tests: pytest ejercicios-seguridad.py::TestAuth -v
```

---

## 🎯 Desafíos Bonus

### **🏆 Desafío 1: OAuth2 Simplificado**

Implementa un flujo OAuth2 básico con Google (solo simulación, sin API real).

### **🏆 Desafío 2: Two-Factor Authentication**

Añade autenticación de dos factores usando TOTP (códigos de tiempo).

### **🏆 Desafío 3: Session Management**

Implementa un sistema de gestión de sesiones activas con logout remoto.

---

## 📝 Entregables

### **🔄 Durante la Práctica**

1. **Código corregido** del Ejercicio 1 con explicaciones
2. **Sistema de roles** funcionando del Ejercicio 2
3. **Validador de passwords** completo del Ejercicio 3
4. **Rate limiter** básico del Ejercicio 4
5. **Sistema de auditoría** del Ejercicio 5
6. **Suite de tests** del Ejercicio 6

### **📤 Al Final de la Semana**

- **Repository actualizado** con todos los ejercicios resueltos
- **Tests passing** documentados con screenshots
- **README** explicando las implementaciones de seguridad
- **Documentación** de APIs con ejemplos de autenticación

---

## 🔍 Criterios de Evaluación

| Aspecto           | Peso | Criterios                      |
| ----------------- | ---- | ------------------------------ |
| **Funcionalidad** | 40%  | Código funciona correctamente  |
| **Seguridad**     | 30%  | Buenas prácticas aplicadas     |
| **Testing**       | 20%  | Tests completos y documentados |
| **Documentación** | 10%  | Código bien documentado        |

---

## 📚 Recursos Adicionales

- [JWT Best Practices](https://auth0.com/blog/a-look-at-the-latest-draft-for-jwt-bcp/)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [Python bcrypt Documentation](https://pypi.org/project/bcrypt/)

---

## 🆘 Ayuda y Soporte

- **Dudas técnicas:** Utilizar issues en GitHub con label `security`
- **Conceptos:** Revisar material teórico de la semana
- **Debugging:** Activar logs detallados y usar debugger

---

**⚡ Nota:** Estos ejercicios son fundamentales para entender seguridad en APIs. Tómate el tiempo necesario para comprenderlos completamente antes de avanzar al proyecto final.
