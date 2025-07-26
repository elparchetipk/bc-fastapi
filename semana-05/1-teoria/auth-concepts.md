# Week 5 Theory: Basic Security Concepts

## What is Security in APIs?

API security ensures that only authorized users can access your API and that data remains protected.

## Authentication vs Authorization

### Authentication: "Who are you?"

Verifying the identity of a user.

**Example**: Login with username and password

### Authorization: "What can you do?"

Determining what an authenticated user is allowed to access.

**Example**: Only admins can delete users

## Common Authentication Methods

### 1. API Keys

Simple strings that identify API users.

```python
# In request headers:
X-API-Key: user123
```

**Pros**: Simple to implement  
**Cons**: Not very secure for sensitive data

### 2. Username/Password

Traditional method with credentials.

```python
{
  "username": "alice",
  "password": "secret123"
}
```

**Pros**: Familiar to users  
**Cons**: Passwords can be compromised

### 3. Session-Based

Server remembers user after login.

**Pros**: Good for web applications  
**Cons**: Not scalable for APIs

## Basic Security Principles

### 1. Never Store Plain Passwords

Always hash passwords before storing them.

### 2. Use HTTPS

Encrypt data in transit.

### 3. Validate All Input

Check all data from users.

### 4. Principle of Least Privilege

Give users only the permissions they need.

## Simple Protection Patterns

### Dependency Injection

```python
def require_auth(api_key: str = Header(...)):
    if api_key not in valid_keys:
        raise HTTPException(401, "Invalid API key")
    return get_user(api_key)

@app.get("/protected")
def protected_route(user=Depends(require_auth)):
    return {"user": user}
```

### Role-Based Access

```python
def require_admin(user=Depends(require_auth)):
    if user.role != "admin":
        raise HTTPException(403, "Admin required")
    return user
```

## HTTP Status Codes for Security

- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Authenticated but not authorized
- **400 Bad Request**: Invalid credentials format

## Best Practices (Basics)

1. **Always validate input** from users
2. **Use proper HTTP status codes** for security errors
3. **Don't expose sensitive information** in error messages
4. **Keep security simple** when starting out
5. **Log security events** for monitoring

This foundation prepares you for more advanced security concepts in future projects.

**Autorización** es el proceso de **determinar qué puede hacer** un usuario autenticado.

**Pregunta que responde:** _"¿Qué puedes hacer?"_

#### Modelos de Autorización

1. **Role-Based Access Control (RBAC)**

   ```python
   # Ejemplo conceptual
   user.role = "admin"  # Roles: admin, user, moderator
   if user.role == "admin":
       # Puede acceder a endpoints administrativos
   ```

2. **Attribute-Based Access Control (ABAC)**

   ```python
   # Basado en atributos del usuario, recurso y contexto
   if user.department == "HR" and resource.type == "employee_data":
       # Permitir acceso
   ```

3. **Permission-Based**
   ```python
   # Permisos granulares específicos
   user.permissions = ["read_users", "create_posts", "delete_comments"]
   ```

### Flujo Típico: Autenticación → Autorización

```mermaid
sequenceDiagram
    participant U as Usuario
    participant A as API
    participant D as Database

    U->>A: 1. Login (username/password)
    A->>D: 2. Verificar credentials
    D-->>A: 3. Usuario válido
    A-->>U: 4. JWT Token (AUTENTICACIÓN)

    U->>A: 5. Request con Token
    A->>A: 6. Validar Token
    A->>A: 7. Verificar Permisos (AUTORIZACIÓN)
    A-->>U: 8. Response o Error
```

---

## 🎫 JSON Web Tokens (JWT)

### ¿Qué es un JWT?

JWT es un **estándar abierto** (RFC 7519) para transmitir información entre partes de forma **segura** y **compacta**.

### Estructura de un JWT

Un JWT consiste en **tres partes** separadas por puntos (`.`):

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

#### 1. Header (Cabecera)

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

- **alg**: Algoritmo de firmado (HS256, RS256, etc.)
- **typ**: Tipo de token (siempre "JWT")

#### 2. Payload (Carga útil)

```json
{
  "sub": "1234567890", // Subject (ID del usuario)
  "name": "John Doe", // Claim personalizado
  "iat": 1516239022, // Issued At (timestamp)
  "exp": 1516242622 // Expiration (timestamp)
}
```

**Claims estándar:**

- `sub` (subject): Identificador del usuario
- `iat` (issued at): Cuándo se emitió el token
- `exp` (expiration): Cuándo expira el token
- `iss` (issuer): Quién emitió el token
- `aud` (audience): Para quién es el token

#### 3. Signature (Firma)

```javascript
HMACSHA256(base64UrlEncode(header) + '.' + base64UrlEncode(payload), secret);
```

### Ventajas de JWT

1. **Stateless** - No requiere almacenamiento en servidor
2. **Portable** - Funciona entre dominios y servicios
3. **Self-contained** - Toda la información necesaria está en el token
4. **Secure** - Firmado digitalmente
5. **Compact** - Tamaño pequeño para HTTP headers

### Desventajas de JWT

1. **No se puede revocar** fácilmente
2. **Tamaño** puede ser grande con muchos claims
3. **Vulnerable** si se compromete el secret
4. **Stateless** = no puede tracked del lado del servidor

### Mejores Prácticas JWT

```python
# ✅ BUENAS PRÁCTICAS
{
    "exp": 1234567890,        # Siempre incluir expiración
    "iat": 1234567800,        # Timestamp de emisión
    "sub": "user123",         # ID del usuario, no info sensible
    "role": "user",           # Información mínima necesaria
    "permissions": ["read"]   # Permisos específicos si necesario
}

# ❌ MALAS PRÁCTICAS
{
    "password": "123456",     # NUNCA incluir passwords
    "credit_card": "1234",    # NUNCA info sensible
    "admin_secret": "xyz",    # NUNCA secrets
    # Sin expiración = riesgo de seguridad
}
```

---

## 🔒 Password Hashing y Seguridad

### ¿Por qué Hashear Passwords?

**NUNCA** almacenes passwords en texto plano. Siempre usa **hashing** criptográfico.

#### Problemas del Texto Plano:

- Empleados pueden ver passwords de usuarios
- Breaches exponen todas las passwords
- Vulnerabilidades de base de datos
- Problemas legales y de compliance

### Algoritmos de Hashing

#### ❌ NO usar: MD5, SHA1, SHA256 simples

```python
# INSEGURO - NO HACER
import hashlib
password = "mypassword"
hash = hashlib.md5(password.encode()).hexdigest()
# Vulnerable a rainbow tables y ataques de fuerza bruta
```

#### ✅ SÍ usar: bcrypt, scrypt, Argon2

```python
# SEGURO - bcrypt con salt automático
import bcrypt

# Hashear password
password = "mypassword"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

# Verificar password
bcrypt.checkpw(password.encode('utf-8'), hashed)  # True/False
```

### Conceptos Clave de Hashing

#### 1. Salt (Sal)

- **Valor aleatorio** añadido al password antes del hash
- **Previene rainbow table attacks**
- **Único para cada password**

```python
# Sin salt: password123 → mismo hash siempre
# Con salt: password123 + salt_random → hash único
```

#### 2. Work Factor / Cost

- **Controla la dificultad** del algoritmo
- **Más alto = más seguro pero más lento**
- **Debe ajustarse según hardware disponible**

```python
# bcrypt work factor
salt = bcrypt.gensalt(rounds=12)  # Default: 12, más alto = más seguro
```

#### 3. Timing Attacks

- **Comparaciones deben tomar tiempo constante**
- **Evita revelar información por timing**

```python
# ❌ VULNERABLE a timing attacks
if hash1 == hash2:  # Puede ser más rápido si primeros chars difieren

# ✅ SEGURO - timing constante
import secrets
if secrets.compare_digest(hash1, hash2):  # Siempre toma mismo tiempo
```

---

## 🔑 OAuth2 y OpenID Connect

### OAuth2 Flow Básico

OAuth2 es un **framework de autorización** que permite a aplicaciones obtener acceso limitado a servicios.

#### Authorization Code Flow

```mermaid
sequenceDiagram
    participant U as Usuario
    participant C as Cliente (App)
    participant A as Auth Server
    participant R as Resource Server

    U->>C: 1. Quiere acceder
    C->>A: 2. Redirect para autorización
    U->>A: 3. Login y autoriza
    A->>C: 4. Authorization Code
    C->>A: 5. Intercambia code por token
    A->>C: 6. Access Token
    C->>R: 7. Request con token
    R->>C: 8. Protected resource
```

### Términos Clave OAuth2

- **Resource Owner**: Usuario que posee los datos
- **Client**: Aplicación que quiere acceder a los datos
- **Authorization Server**: Servidor que autentica y autoriza
- **Resource Server**: Servidor que hospeada los recursos protegidos
- **Access Token**: Token para acceder a recursos
- **Refresh Token**: Token para renovar access tokens

### FastAPI OAuth2

FastAPI incluye utilidades para OAuth2:

```python
from fastapi.security import OAuth2PasswordBearer

# Esquema OAuth2 para password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency para obtener token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Validar y decodificar token
    # Retornar usuario actual
    pass
```

---

## 🛡️ Principios de Seguridad en APIs

### 1. Principio de Menor Privilegio

**Dar solo los permisos mínimos necesarios**

```python
# ❌ MAL - demasiados permisos
user.permissions = ["*"]  # Acceso a todo

# ✅ BIEN - permisos específicos
user.permissions = ["read_own_profile", "update_own_profile"]
```

### 2. Defense in Depth

**Múltiples capas de seguridad**

```python
# Capa 1: HTTPS
# Capa 2: Authentication
# Capa 3: Authorization
# Capa 4: Input validation
# Capa 5: Rate limiting
# Capa 6: Logging/Monitoring
```

### 3. Fail Secure

**En caso de error, fallar de forma segura**

```python
def check_permission(user, resource):
    try:
        return user.can_access(resource)
    except Exception:
        # ✅ En caso de error, denegar acceso
        return False  # Fail secure

        # ❌ NUNCA hacer esto
        # return True  # Fail open - INSEGURO
```

### 4. Input Validation

**Validar y sanitizar toda entrada**

```python
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    username: str
    email: str

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username muy corto')
        if not v.isalnum():
            raise ValueError('Username debe ser alfanumérico')
        return v
```

### 5. Error Handling Seguro

**No revelar información sensible en errores**

```python
# ❌ INSEGURO - revela info del sistema
raise HTTPException(
    status_code=500,
    detail="Database connection failed: host=192.168.1.100"
)

# ✅ SEGURO - mensaje genérico
raise HTTPException(
    status_code=500,
    detail="Internal server error"
)
```

---

## 🔍 Vulnerabilidades Comunes

### 1. Injection Attacks

#### SQL Injection

```python
# ❌ VULNERABLE
query = f"SELECT * FROM users WHERE id = {user_id}"

# ✅ SEGURO - usar ORM o prepared statements
user = db.query(User).filter(User.id == user_id).first()
```

#### NoSQL Injection

```python
# ❌ VULNERABLE
query = {"username": username, "password": password}

# ✅ SEGURO - validar tipos
if not isinstance(username, str) or not isinstance(password, str):
    raise ValueError("Invalid input types")
```

### 2. Authentication Bypass

```python
# ❌ VULNERABLE - lógica incorrecta
if username == "admin" or password == "":
    return True  # Siempre true para admin!

# ✅ CORRECTO
if username == "admin" and verify_password(password, admin_hash):
    return True
```

### 3. Session Management

```python
# ❌ INSEGURO - tokens predecibles
token = f"{username}_{timestamp}"

# ✅ SEGURO - tokens aleatorios
import secrets
token = secrets.token_urlsafe(32)
```

### 4. Information Disclosure

```python
# ❌ REVELA INFO SENSIBLE
return {"users": [
    {"id": 1, "username": "john", "password_hash": "abc123"},
    {"id": 2, "username": "jane", "credit_card": "1234-5678"}
]}

# ✅ SOLO INFO NECESARIA
return {"users": [
    {"id": 1, "username": "john"},
    {"id": 2, "username": "jane"}
]}
```

---

## 🚀 Implementación en FastAPI

### Estructura Típica de Autenticación

```python
# core/security.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
```

### Dependency Injection para Autenticación

```python
# core/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

### Protección de Endpoints

```python
# api/users.py
@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/admin/users", response_model=List[UserResponse])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_admin_user)  # Solo admin
):
    users = get_users(skip=skip, limit=limit)
    return users
```

---

## 📚 Mejores Prácticas Resumidas

### ✅ DO (Hacer)

1. **Usar HTTPS** siempre en producción
2. **Hashear passwords** con bcrypt/scrypt/Argon2
3. **Implementar rate limiting** en endpoints de auth
4. **Usar JWT con expiración** apropiada
5. **Validar toda entrada** de usuarios
6. **Implementar logging** de eventos de seguridad
7. **Usar variables de entorno** para secrets
8. **Implementar CORS** apropiadamente
9. **Mantener dependencias actualizadas**
10. **Documentar endpoints de seguridad**

### ❌ DON'T (No hacer)

1. **Almacenar passwords** en texto plano
2. **Hardcodear secrets** en código
3. **Usar algoritmos débiles** (MD5, SHA1)
4. **Exponer información sensible** en errors
5. **Implementar autenticación personalizada** sin experiencia
6. **Usar tokens sin expiración**
7. **Confiar en client-side validation** únicamente
8. **Ignorar actualizaciones de seguridad**
9. **Usar HTTP** en producción
10. **Implementar sistemas complejos** sin testing

---

## 🎯 Próximos Pasos

Después de dominar estos conceptos:

1. **Implementar JWT** básico con FastAPI
2. **Crear sistema de login/register**
3. **Proteger endpoints** con middleware
4. **Añadir roles y permisos**
5. **Implementar testing** de seguridad
6. **Considerar OAuth2** para social login
7. **Aprender sobre refresh tokens**
8. **Explorar security headers**
9. **Implementar audit logging**
10. **Estudiar penetration testing**

---

## 📖 Lecturas Recomendadas

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [RFC 7519 - JWT](https://tools.ietf.org/html/rfc7519)
- [FastAPI Security Documentation](https://fastapi.tiangolo.com/tutorial/security/)
- [OAuth2 RFC 6749](https://tools.ietf.org/html/rfc6749)
- [bcrypt Documentation](https://pypi.org/project/bcrypt/)

---

**¡Ahora estás listo para implementar sistemas de autenticación y autorización seguros! 🔐✨**
