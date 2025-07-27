# Práctica 17: Protección de Endpoints Básica

## 🎯 Objetivo

Aprender a **proteger endpoints** con autenticación JWT en 90 minutos, usando dependencias simples.

## ⏱️ Tiempo: 90 minutos

## 📋 Pre-requisitos

- ✅ Sistema de login funcionando (Práctica 16 completada)
- ✅ JWT setup básico implementado
- ✅ Endpoints de registro y login funcionando

## 🚀 Desarrollo Paso a Paso

### Paso 1: Dependencia de Autenticación (25 min)

#### Completar función `get_current_user` en `auth.py`

```python
# Agregar al archivo auth.py existente
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

security = HTTPBearer()

def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
    """Obtener usuario actual desde JWT token"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodificar token
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    # Obtener usuario de la base de datos
    user = get_user_by_username(db, username=username)

    if user is None:
        raise credentials_exception

    return user
```

#### ¿Qué hace esta función?

1. **Extrae el token** del header Authorization
2. **Decodifica el JWT** usando la clave secreta
3. **Obtiene el username** del payload del token
4. **Busca el usuario** en la base de datos
5. **Retorna el usuario** si todo está correcto

---

### Paso 2: Proteger Endpoints Existentes (20 min)

#### Actualizar endpoints en `main.py`

```python
# Modificar endpoints existentes para usar autenticación

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(auth.get_current_user)):
    """Obtener perfil del usuario autenticado"""
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active
    )

# Agregar nuevos endpoints protegidos
@app.get("/protected")
def protected_endpoint(current_user: User = Depends(auth.get_current_user)):
    """Endpoint protegido básico"""
    return {
        "message": f"Hola {current_user.username}, tienes acceso!",
        "user_id": current_user.id,
        "status": "authenticated"
    }

@app.get("/public")
def public_endpoint():
    """Endpoint público sin protección"""
    return {
        "message": "Este endpoint es público",
        "status": "no authentication required"
    }
```

---

### Paso 3: Endpoints CRUD Protegidos (30 min)

#### Ejemplo: Gestión de posts protegida

```python
# Agregar a main.py
from typing import List

# Lista simple para ejemplos (en producción usarías la base de datos)
posts = []

class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    author: str

@app.post("/posts", response_model=PostResponse)
def create_post(
    post_data: PostCreate,
    current_user: User = Depends(auth.get_current_user)
):
    """Crear nuevo post (requiere autenticación)"""

    new_post = {
        "id": len(posts) + 1,
        "title": post_data.title,
        "content": post_data.content,
        "author": current_user.username
    }

    posts.append(new_post)

    return PostResponse(**new_post)

@app.get("/posts", response_model=List[PostResponse])
def get_posts():
    """Listar posts (público)"""
    return [PostResponse(**post) for post in posts]

@app.get("/posts/my", response_model=List[PostResponse])
def get_my_posts(current_user: User = Depends(auth.get_current_user)):
    """Obtener mis posts (requiere autenticación)"""

    my_posts = [post for post in posts if post["author"] == current_user.username]

    return [PostResponse(**post) for post in my_posts]

@app.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    current_user: User = Depends(auth.get_current_user)
):
    """Borrar post (solo el autor)"""

    post = next((p for p in posts if p["id"] == post_id), None)

    if not post:
        raise HTTPException(status_code=404, detail="Post no encontrado")

    if post["author"] != current_user.username:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para borrar este post"
        )

    posts.remove(post)

    return {"message": "Post eliminado exitosamente"}
```

---

### Paso 4: Testing Manual de Protección (15 min)

#### Probar endpoint protegido SIN token

```bash
# Intentar acceder sin token (debe fallar)
curl -X GET "http://127.0.0.1:8000/protected"
```

**Resultado esperado:**

```json
{
  "detail": "Not authenticated"
}
```

#### Probar endpoint protegido CON token

```bash
# 1. Hacer login para obtener token
curl -X POST "http://127.0.0.1:8000/login" \
     -H "Content-Type: application/json" \
     -d '{"username": "juan", "password": "mi_password"}'

# 2. Usar el token en endpoint protegido
curl -X GET "http://127.0.0.1:8000/protected" \
     -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**Resultado esperado:**

```json
{
  "message": "Hola juan, tienes acceso!",
  "user_id": 1,
  "status": "authenticated"
}
```

#### Probar CRUD protegido

```bash
# Crear post (requiere token)
curl -X POST "http://127.0.0.1:8000/posts" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer TU_TOKEN_AQUI" \
     -d '{
       "title": "Mi primer post",
       "content": "Contenido del post"
     }'

# Ver mis posts (requiere token)
curl -X GET "http://127.0.0.1:8000/posts/my" \
     -H "Authorization: Bearer TU_TOKEN_AQUI"

# Ver todos los posts (público)
curl -X GET "http://127.0.0.1:8000/posts"
```

---

## ✅ Checklist de Completado

### Funcionalidad Básica

- [ ] Función `get_current_user` implementada y funcionando
- [ ] Endpoint `/protected` funcionando con autenticación
- [ ] Endpoint `/public` funcionando sin autenticación
- [ ] Endpoints CRUD protegidos implementados

### Testing Manual

- [ ] Error 401 al acceder sin token
- [ ] Acceso exitoso con token válido
- [ ] CRUD protegido funcionando correctamente
- [ ] Autorización por propietario funcionando

### Comprensión

- [ ] Entiendes cómo funciona `Depends()` para protección
- [ ] Comprendes la diferencia entre endpoints públicos y protegidos
- [ ] Sabes implementar autorización básica (solo el propietario)

---

## 🎯 Objetivo Alcanzado

**Has implementado protección básica de endpoints** con:

1. **Dependencias de autenticación** usando JWT
2. **Endpoints protegidos** que requieren login
3. **Endpoints públicos** sin restricciones
4. **Autorización básica** por propietario

**🚀 Siguiente:** En la próxima práctica verás roles y permisos más avanzados.

---

## 📚 Conceptos Aplicados

- **Dependencies** de FastAPI para protección
- **JWT validation** en tiempo real
- **Authorization headers** Bearer token
- **HTTP status codes** para autenticación/autorización
- **Resource ownership** para control de acceso

**¡Endpoints protegidos exitosamente!** 🔒
