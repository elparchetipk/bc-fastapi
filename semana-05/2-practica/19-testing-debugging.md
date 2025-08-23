# Práctica 19: Consolidación y Testing

## 🎯 Objetivo

**Consolidar y probar todo el sistema de autenticación** implementado en los bloques anteriores, asegurando que funciona correctamente y resolviendo problemas comunes.

## ⏱️ Tiempo: 75 minutos

## 📋 Pre-requisitos

- ✅ JWT y hashing implementados (Práctica 15)
- ✅ Sistema de login funcionando (Práctica 16)
- ✅ Endpoints protegidos (Práctica 17)

---

## 🔍 Paso 1: Verificación Completa del Sistema (20 min)

### Checklist de Funcionamiento

**Marca cada elemento que funciona correctamente:**

- [ ] **Dependencies instaladas**: python-jose, passlib, python-multipart
- [ ] **Variables de entorno**: SECRET_KEY, ALGORITHM configurados
- [ ] **Hashing**: Passwords se guardan hasheados (no en texto plano)
- [ ] **JWT tokens**: Login retorna token válido
- [ ] **Token verification**: Endpoints protegidos validan token
- [ ] **User extraction**: Se puede obtener usuario del token
- [ ] **Error handling**: Mensajes apropiados para errores

### Verificación Rápida en Código

```python
# Verifica estos archivos en tu proyecto:

# 1. auth.py - debe tener estas funciones
def create_access_token(data: dict)  # ✅
def verify_password(plain_password, hashed_password)  # ✅
def get_password_hash(password)  # ✅
def get_current_user(token: str = Depends(oauth2_scheme))  # ✅

# 2. main.py - debe tener estos endpoints
@app.post("/auth/register")  # ✅
@app.post("/auth/login")     # ✅
@app.get("/auth/me")         # ✅ (protegido)

# 3. models.py - User model debe tener
class User(Base):
    email: str        # ✅
    hashed_password: str  # ✅ (NO password plano)
```

---

## 🧪 Paso 2: Testing Manual Completo (25 min)

### Testing con Postman/Thunder Client

#### Test 1: Registro de Usuario (5 min)

```json
POST http://127.0.0.1:8000/auth/register
Content-Type: application/json

{
  "email": "test@example.com",
  "password": "password123"
}

// ✅ Respuesta esperada: 201 Created
{
  "id": 1,
  "email": "test@example.com"
}
```

#### Test 2: Login (5 min)

```json
POST http://127.0.0.1:8000/auth/login
Content-Type: application/x-www-form-urlencoded

username=test@example.com&password=password123

// ✅ Respuesta esperada: 200 OK
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Test 3: Acceso Protegido (5 min)

```json
GET http://127.0.0.1:8000/auth/me
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...

// ✅ Respuesta esperada: 200 OK
{
  "id": 1,
  "email": "test@example.com"
}
```

#### Test 4: Acceso Sin Token (5 min)

```json
GET http://127.0.0.1:8000/auth/me
// SIN Authorization header

// ✅ Respuesta esperada: 401 Unauthorized
{
  "detail": "Not authenticated"
}
```

#### Test 5: Token Inválido (5 min)

```json
GET http://127.0.0.1:8000/auth/me
Authorization: Bearer token-invalido

// ✅ Respuesta esperada: 401 Unauthorized
{
  "detail": "Could not validate credentials"
}
```

---

## 🐛 Paso 3: Resolución de Problemas Comunes (20 min)

### Problema 1: Error de JWT

**Síntoma**: `JWTError` o token no válido

**Solución**:
```python
# Verificar que SECRET_KEY y ALGORITHM estén bien
SECRET_KEY = "tu-clave-secreta-muy-larga-y-segura-aqui"
ALGORITHM = "HS256"

# Verificar función de creación de token
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

### Problema 2: Password no hasheado

**Síntoma**: Passwords en texto plano en la base de datos

**Solución**:
```python
# En el endpoint de registro
@app.post("/auth/register")
async def register(user: UserCreate, db: Session = Depends(get_db)):
    # ❌ MALO: password en texto plano
    # db_user = User(email=user.email, password=user.password)
    
    # ✅ BUENO: password hasheado
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    
    db.add(db_user)
    db.commit()
    return db_user
```

### Problema 3: Dependency no funciona

**Síntoma**: `get_current_user` no funciona

**Solución**:
```python
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
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Buscar usuario en la base de datos
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
```

---

## 📊 Paso 4: Testing con FastAPI Docs (10 min)

### Verificar en Swagger UI

1. **Abrir**: `http://127.0.0.1:8000/docs`

2. **Probar registro**:
   - Expandir `POST /auth/register`
   - Click "Try it out"
   - Agregar datos de usuario
   - Click "Execute"

3. **Probar login**:
   - Expandir `POST /auth/login`
   - Usar `username` (no email) y `password`
   - Copiar el `access_token`

4. **Autorizar**:
   - Click botón "Authorize" (🔐) arriba
   - Pegar token: `Bearer tu-token-aqui`
   - Click "Authorize"

5. **Probar endpoint protegido**:
   - Expandir `GET /auth/me`
   - Click "Try it out"
   - Click "Execute"
   - Debe retornar tus datos de usuario

---

## ✅ Checklist Final

**Al completar esta práctica debes tener:**

- [ ] Sistema de autenticación completo funcionando
- [ ] Testing manual exitoso con Postman/Thunder Client
- [ ] Swagger UI funcionando con autenticación
- [ ] Passwords hasheados en la base de datos
- [ ] Manejo apropiado de errores
- [ ] Documentación clara de endpoints

**Si algún item no funciona:**
1. Revisar logs de errores
2. Verificar configuración de variables
3. Comprobar imports y dependencies
4. Consultar con instructor si es necesario

---

## 🎯 Resultado Esperado

**API de autenticación básica pero completa:**
- Registro seguro de usuarios
- Login con JWT tokens
- Protección de endpoints
- Manejo adecuado de errores
- Base sólida para agregar funcionalidades

## 📚 Próximos Pasos

**En la siguiente semana agregarás:**
- Sistema de roles (admin/user)
- Permisos granulares
- Refresh tokens
- Middleware personalizado
