# Week 5 Support Resources

## Official Documentation

### FastAPI Security

- [FastAPI Security Tutorial](https://fastapi.tiangolo.com/tutorial/security/) - Basic security concepts
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) - Dependency injection for auth

### HTTP Authentication

- [HTTP Authentication](https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication) - MDN guide
- [HTTP Status Codes](https://httpstatuses.com/) - Security-related status codes

## Simple Authentication Patterns

### API Key Resources

- [API Key Best Practices](https://cloud.google.com/docs/authentication/api-keys) - Google Cloud guide
- [HTTP Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers) - Header-based auth

### Basic Auth Resources

- [HTTP Basic Authentication](https://tools.ietf.org/html/rfc7617) - RFC specification
- [Session Management](https://owasp.org/www-community/controls/Session_Management_Cheat_Sheet) - OWASP guide

## Security Best Practices

### General Security

- [OWASP Top 10](https://owasp.org/www-project-top-ten/) - Common security vulnerabilities
- [Security Headers](https://securityheaders.com/) - HTTP security headers

### Password Security

- [Password Storage](https://owasp.org/www-community/password-special-characters) - OWASP guide
- [Hashing vs Encryption](https://www.ssl2buy.com/wiki/difference-between-hashing-and-encryption) - Understanding the difference

## Testing Tools

### API Testing

- [Postman](https://www.postman.com/) - API testing with authentication
- [curl Examples](https://curl.se/docs/httpscripting.html) - Command line testing

### Development Tools

- [VSCode REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) - Testing in editor
- [Thunder Client](https://www.thunderclient.com/) - Lightweight API client

## Useful Examples

### Common Authentication Headers

```
# API Key in header
X-API-Key: user123

# Basic Authentication
Authorization: Basic dXNlcjpwYXNzd29yZA==

# Custom token
Authorization: Bearer custom-token-123
```

### Status Code Reference

- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Authenticated but not authorized
- `400 Bad Request` - Invalid credentials format

Remember: Start simple, focus on understanding concepts before complexity.

- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html) - Mejores prácticas

#### **Herramientas Online**

- [Password Strength Checker](https://www.passwordmonster.com/) - Verificar fortaleza
- [bcrypt Calculator](https://bcrypt-generator.com/) - Generar y verificar hashes

### **🛡️ Autorización y Permisos**

#### **Conceptos y Patrones**

- [RBAC (Role-Based Access Control)](https://en.wikipedia.org/wiki/Role-based_access_control) - Modelo de roles
- [ABAC (Attribute-Based Access Control)](https://en.wikipedia.org/wiki/Attribute-based_access_control) - Control por atributos
- [OAuth 2.0 RFC](https://tools.ietf.org/html/rfc6749) - Estándar de autorización

#### **Implementaciones**

- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) - Dependency injection
- [Starlette Middleware](https://www.starlette.io/middleware/) - Middleware customizado
- [Casbin](https://casbin.org/) - Framework de autorización avanzado

### **🔧 Rate Limiting y Seguridad**

#### **Implementaciones**

- [slowapi](https://github.com/laurentS/slowapi) - Rate limiting para FastAPI
- [redis-py](https://redis-py.readthedocs.io/) - Cliente Redis para caching
- [OWASP API Security](https://owasp.org/www-project-api-security/) - Top 10 vulnerabilidades

#### **Herramientas de Testing**

- [OWASP ZAP](https://www.zaproxy.org/) - Scanner de seguridad
- [Burp Suite Community](https://portswigger.net/burp/communitydownload) - Testing de APIs

---

## 📖 Guías de Referencia Rápida

### **🔑 JWT Token Structure**

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "1234567890",
    "name": "John Doe",
    "role": "admin",
    "iat": 1516239022,
    "exp": 1516242622
  },
  "signature": "SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

### **🔐 bcrypt Usage Patterns**

```python
from passlib.context import CryptContext

# Setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("my_password")

# Verify password
is_valid = pwd_context.verify("my_password", hashed)
```

### **🛡️ Common Security Headers**

```python
# FastAPI Middleware para headers de seguridad
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)
```

### **⚡ Rate Limiting Example**

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(request: Request, user_credentials: UserLogin):
    # Login logic here
    pass
```

---

## 🧪 Testing Resources

### **Testing Frameworks**

- [pytest](https://docs.pytest.org/) - Framework de testing principal
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/) - Testing asíncrono
- [httpx](https://www.python-httpx.org/) - Cliente HTTP para tests
- [Factory Boy](https://factoryboy.readthedocs.io/) - Creación de datos de prueba

### **Testing Security**

```python
# Ejemplo de test de autenticación
def test_login_with_valid_credentials():
    response = client.post("/auth/login", json={
        "username": "testuser",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_endpoint_without_token():
    response = client.get("/protected")
    assert response.status_code == 401

def test_protected_endpoint_with_token():
    token = get_valid_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected", headers=headers)
    assert response.status_code == 200
```

### **Coverage Tools**

```bash
# Instalar coverage
pip install coverage pytest-cov

# Ejecutar tests con coverage
pytest --cov=app --cov-report=html --cov-report=term

# Ver reporte HTML
open htmlcov/index.html
```

---

## 🛠️ Herramientas de Desarrollo

### **Database Tools**

- [Alembic](https://alembic.sqlalchemy.org/) - Migraciones de base de datos
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM principal
- [pgAdmin](https://www.pgadmin.org/) - Administrador PostgreSQL
- [DBeaver](https://dbeaver.io/) - Cliente universal de base de datos

### **API Development**

- [Postman](https://www.postman.com/) - Testing de APIs
- [Insomnia](https://insomnia.rest/) - Cliente REST alternativo
- [HTTPie](https://httpie.io/) - Cliente HTTP por línea de comandos

### **Monitoring & Logging**

- [Sentry](https://sentry.io/) - Error tracking
- [Loguru](https://loguru.readthedocs.io/) - Logging avanzado
- [Prometheus](https://prometheus.io/) - Métricas y monitoring

---

## 📚 Libros y Recursos Avanzados

### **Libros Recomendados**

1. **"Web Application Security"** by Andrew Hoffman

   - Conceptos fundamentales de seguridad web
   - Vulnerabilidades comunes y mitigaciones

2. **"OAuth 2.0 Simplified"** by Aaron Parecki

   - Guía completa del protocolo OAuth 2.0
   - Implementaciones prácticas

3. **"High Performance Python"** by Micha Gorelick
   - Optimización de aplicaciones Python
   - Profiling y mejoras de rendimiento

### **Cursos Online**

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Coursera: Cybersecurity Specialization](https://www.coursera.org/specializations/cyber-security)
- [Pluralsight: FastAPI Path](https://www.pluralsight.com/paths/fastapi)

---

## 🔧 Snippets de Código Útiles

### **Custom Dependency para Roles**

```python
from functools import wraps
from typing import List
from fastapi import HTTPException, Depends, status

def require_roles(allowed_roles: List[str]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user
    return role_checker

# Usage
@app.get("/admin-only")
async def admin_endpoint(user: User = Depends(require_roles(["admin"]))):
    return {"message": "Admin access granted"}
```

### **Middleware de Logging de Requests**

```python
import time
import logging
from fastapi import Request

logger = logging.getLogger("api_requests")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time
    logger.info(
        f"{request.method} {request.url.path} - "
        f"{response.status_code} - {process_time:.3f}s"
    )

    return response
```

### **Health Check Endpoint**

```python
from sqlalchemy import text

@app.get("/health")
async def health_check():
    try:
        # Check database connection
        result = await database.fetch_one(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {str(e)}"
        )
```

---

## 🚀 Deployment Resources

### **Docker & Containerization**

```dockerfile
# Dockerfile ejemplo
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Environment Configuration**

```python
# config.py con pydantic settings
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    database_url: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

### **CI/CD with GitHub Actions**

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov

      - name: Run tests
        run: pytest --cov=app
```

---

## 🎓 Ejercicios de Práctica Extra

### **Ejercicio 1: Implementar 2FA**

```python
# Implementa autenticación de dos factores usando pyotp
import pyotp
import qrcode

def generate_secret():
    return pyotp.random_base32()

def generate_qr_code(user_email: str, secret: str):
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user_email,
        issuer_name="Your App Name"
    )
    # Generar QR code para Google Authenticator
    pass

def verify_totp(secret: str, token: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(token)
```

### **Ejercicio 2: Session Management**

```python
# Implementa gestión de sesiones activas
class SessionManager:
    def __init__(self):
        self.active_sessions = {}  # En producción usar Redis

    def create_session(self, user_id: int, token: str, device_info: dict):
        # Crear nueva sesión
        pass

    def revoke_session(self, session_id: str):
        # Revocar sesión específica
        pass

    def revoke_all_sessions(self, user_id: int):
        # Revocar todas las sesiones del usuario
        pass

    def get_active_sessions(self, user_id: int):
        # Obtener sesiones activas
        pass
```

### **Ejercicio 3: Audit Trail Avanzado**

```python
# Sistema de auditoría completo
from enum import Enum
from contextlib import asynccontextmanager

class AuditAction(Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"

@asynccontextmanager
async def audit_context(action: AuditAction, resource: str, user_id: int):
    start_time = time.time()
    try:
        yield
        # Log successful action
        await log_audit(action, resource, user_id, "success", time.time() - start_time)
    except Exception as e:
        # Log failed action
        await log_audit(action, resource, user_id, "failure", time.time() - start_time, str(e))
        raise

# Usage
async def update_user(user_id: int, data: dict):
    async with audit_context(AuditAction.UPDATE, "user", user_id):
        # Update logic here
        pass
```

---

## 🆘 Troubleshooting Common Issues

### **JWT Issues**

```python
# Debug JWT tokens
import jwt

def debug_token(token: str, secret: str):
    try:
        # Decode without verification to see payload
        unverified = jwt.decode(token, options={"verify_signature": False})
        print("Unverified payload:", unverified)

        # Try to decode with verification
        verified = jwt.decode(token, secret, algorithms=["HS256"])
        print("Verified payload:", verified)

    except jwt.ExpiredSignatureError:
        print("Token has expired")
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
```

### **Database Connection Issues**

```python
# Test database connectivity
async def test_db_connection():
    try:
        result = await database.fetch_one("SELECT version()")
        print(f"Database connected: {result}")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False
```

### **CORS Issues**

```python
# Proper CORS setup
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📞 Contacto y Soporte

### **Canales de Ayuda**

- **GitHub Issues**: Para problemas técnicos específicos
- **Discussions**: Para preguntas generales y discusión
- **Office Hours**: Martes y jueves 6-8 PM
- **Email**: bootcamp-support@epti.dev

### **Código de Conducta**

Recuerda seguir el [Código de Conducta](../../CODE_OF_CONDUCT.md) del bootcamp en todas las interacciones.

---

**💡 Tip**: Guarda esta página en favoritos, será tu compañera durante toda la semana de autenticación y autorización.
