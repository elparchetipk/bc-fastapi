# Security Best Practices - Bootcamp bc-fastapi

## 🔒 Fundamentos de Seguridad en APIs

### Principios OWASP Top 10 API Security

#### 1. Broken Object Level Authorization

```python
# ❌ VULNERABLE
@app.get("/api/users/{user_id}/profile")
async def get_user_profile(user_id: int):
    return database.get_user_profile(user_id)  # No verifica autorización

# ✅ SEGURO
@app.get("/api/users/{user_id}/profile")
async def get_user_profile(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access forbidden")
    return database.get_user_profile(user_id)
```

#### 2. Broken User Authentication

```python
# ✅ JWT Implementation Segura
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

#### 3. Input Validation & Sanitization

```python
from pydantic import BaseModel, validator, EmailStr
from typing import Optional
import re

class UserCreateRequest(BaseModel):
    email: EmailStr
    password: str
    username: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain number')
        return v

    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', v):
            raise ValueError('Username must be 3-20 chars, alphanumeric + underscore')
        return v
```

## 🛡️ Implementación por Semanas

### Semana 3-4: Security Fundamentals

- HTTPS enforcement
- Input validation básica
- Error handling seguro
- Environment variables para secrets

### Semana 5-6: Authentication & Authorization

- JWT implementation
- Password hashing (bcrypt)
- Role-based access control
- Rate limiting básico

### Semana 7-8: Advanced Security

- CORS configuration
- SQL injection prevention
- Security headers (CSRF, XSS)
- Dependency vulnerability scanning

### Semana 9-10: Production Security

- Security logging y monitoring
- Secrets management (HashiCorp Vault)
- Container security
- Security testing automation

## 🔧 Security Tools Integration

### Pre-commit Security Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ['-r', 'src/', '-f', 'json', '-o', 'bandit-report.json']

  - repo: https://github.com/gitguardian/ggshield
    rev: v1.25.0
    hooks:
      - id: ggshield
        language: python
        stages: [commit]
```

### GitHub Actions Security Scanning

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Bandit Security Scan
        run: |
          pip install bandit
          bandit -r src/ -f json -o bandit-report.json

      - name: Run Safety Check
        run: |
          pip install safety
          safety check --json --output safety-report.json

      - name: Upload Security Reports
        uses: actions/upload-artifact@v3
        with:
          name: security-reports
          path: |
            bandit-report.json
            safety-report.json
```

## 📋 Security Checklist por Proyecto

### Básico (Semanas 1-4)

- [ ] HTTPS configurado
- [ ] Environment variables para secrets
- [ ] Input validation en endpoints
- [ ] Error handling que no expone información sensible
- [ ] Logging apropiado (sin passwords/tokens)

### Intermedio (Semanas 5-8)

- [ ] Authentication JWT implementado
- [ ] Password hashing con bcrypt
- [ ] Rate limiting configurado
- [ ] CORS configurado apropiadamente
- [ ] SQL injection prevention
- [ ] Security headers implementados

### Avanzado (Semanas 9-12)

- [ ] Role-based access control
- [ ] Security logging y monitoring
- [ ] Dependency vulnerability scanning
- [ ] Container security best practices
- [ ] Secrets management apropiado
- [ ] Security testing automatizado

## ⚠️ Common Security Mistakes

### 1. Hardcoded Secrets

```python
# ❌ NUNCA HACER ESTO
SECRET_KEY = "super-secret-key-12345"
DATABASE_URL = "postgresql://user:password@localhost/db"

# ✅ USAR ENVIRONMENT VARIABLES
import os
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
```

### 2. SQL Injection Vulnerabilities

```python
# ❌ VULNERABLE
def get_user_by_id(user_id: str):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    return database.execute(query)

# ✅ SEGURO
def get_user_by_id(user_id: int):
    query = "SELECT * FROM users WHERE id = ?"
    return database.execute(query, (user_id,))
```

### 3. Information Disclosure

```python
# ❌ EXPONE INFORMACIÓN SENSIBLE
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}  # Puede exponer stack traces
    )

# ✅ MANEJO SEGURO
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

## 📚 Resources y Referencias

### Essential Reading

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Security Best Practices](https://python.org/dev/security/)

### Tools

- **Bandit**: Python security linter
- **Safety**: Dependency vulnerability scanner
- **GitGuardian**: Secrets detection
- **Semgrep**: Static analysis security testing

### Compliance Frameworks

- **GDPR**: Data protection requirements
- **SOC 2**: Security compliance standard
- **ISO 27001**: Information security management
