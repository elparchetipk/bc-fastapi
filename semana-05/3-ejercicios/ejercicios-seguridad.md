# Ejercicios Prácticos - Semana 5 (Consolidación)

## 🎯 Objetivo Básico

Consolidar conceptos de **autenticación JWT + protección de endpoints + roles** en el Bloque 4 (45 minutos) a través de ejercicios simples.

## ⏱️ Tiempo: 45 minutos (Bloque 4 - Consolidación)

## 📋 Pre-requisitos

- ✅ API de los Bloques 1-3 funcionando
- ✅ JWT y hashing implementados
- ✅ Sistema de login básico funcionando
- ✅ Endpoints protegidos implementados

---

## 🏋️ Ejercicio 1: Verificación Completa (20 min)

**Objetivo**: Asegurar que todo lo aprendido funciona

### 📝 Checklist de Verificación

**Revisa tu proyecto actual y marca:**

- [ ] **Hashing de passwords**: ¿Los passwords se guardan hasheados en la DB?
- [ ] **JWT tokens**: ¿El login retorna un token JWT válido?
- [ ] **Endpoints protegidos**: ¿Algunos endpoints requieren token para acceder?
- [ ] **Roles básicos**: ¿Tienes usuarios normales y admins?
- [ ] **Autorización**: ¿Los admins pueden hacer cosas que usuarios normales no?
- [ ] **Documentación**: ¿Se ve bien en <http://127.0.0.1:8000/docs>?

### 🔧 **Si algo no funciona**

1. **Problema con JWT**:

   ```python
   from jose import jwt
   from datetime import datetime, timedelta

   SECRET_KEY = "tu-secret-key"
   ALGORITHM = "HS256"

   def create_access_token(data: dict):
       to_encode = data.copy()
       expire = datetime.utcnow() + timedelta(minutes=30)
       to_encode.update({"exp": expire})
       return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   ```

2. **Problema con hashing**:

   ```python
   from passlib.context import CryptContext

   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

   def get_password_hash(password):
       return pwd_context.hash(password)

   def verify_password(plain_password, hashed_password):
       return pwd_context.verify(plain_password, hashed_password)
   ```

---

## 🏋️ Ejercicio 2: Mini Sistema de Posts (15 min)

**Objetivo**: Crear un sistema simple que use autenticación

### 📝 Instrucciones

1. **Crear modelo Post** (5 min):

   ```python
   # En tu models.py o main.py
   class Post(BaseModel):
       title: str
       content: str

   # Lista global simple (en producción usarías DB)
   posts = []
   ```

2. **Crear endpoint protegido** (5 min):

   ```python
   @app.post("/posts")
   def create_post(
       post: Post,
       current_user = Depends(get_current_user)  # Requiere login
   ):
       new_post = {
           "id": len(posts) + 1,
           "title": post.title,
           "content": post.content,
           "author": current_user.username
       }
       posts.append(new_post)
       return new_post
   ```

3. **Probar con curl** (5 min):

   ```bash
   # 1. Login para obtener token
   curl -X POST "http://127.0.0.1:8000/login" \
        -H "Content-Type: application/json" \
        -d '{"username": "tu_usuario", "password": "tu_password"}'

   # 2. Crear post usando el token
   curl -X POST "http://127.0.0.1:8000/posts" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer TU_TOKEN_AQUI" \
        -d '{"title": "Mi Post", "content": "Contenido del post"}'
   ```

### ✅ **Resultado esperado**

- [ ] El endpoint `/posts` requiere autenticación
- [ ] Sin token retorna error 401
- [ ] Con token válido crea el post exitosamente

---

## 🏋️ Ejercicio 3: Testing de Seguridad (10 min)

**Objetivo**: Verificar que la seguridad funciona correctamente

### 📝 Pruebas a realizar

1. **Test sin token** (3 min):

   ```bash
   # Intentar acceder a endpoint protegido sin token
   curl -X GET "http://127.0.0.1:8000/users/me"
   ```

   **Resultado esperado**: Error 401 "Not authenticated"

2. **Test con token inválido** (3 min):

   ```bash
   # Usar un token falso
   curl -X GET "http://127.0.0.1:8000/users/me" \
        -H "Authorization: Bearer token_falso_123"
   ```

   **Resultado esperado**: Error 401 "Could not validate credentials"

3. **Test de roles** (4 min):

   ```bash
   # Si tienes endpoints de admin, probar con usuario normal
   curl -X GET "http://127.0.0.1:8000/admin/users" \
        -H "Authorization: Bearer TOKEN_DE_USUARIO_NORMAL"
   ```

   **Resultado esperado**: Error 403 "Insufficient permissions"

### ✅ **Checklist de Testing**

- [ ] Error 401 sin token ✅
- [ ] Error 401 con token inválido ✅
- [ ] Error 403 sin permisos de admin ✅
- [ ] Acceso exitoso con token válido ✅

---

## 🎯 **Completado Exitosamente**

### **Has consolidado:**

1. **Autenticación básica** con JWT
2. **Protección de endpoints** usando dependencias
3. **Sistema de roles** básico
4. **Testing de seguridad** manual

### **Checklist Final**

- [ ] Sistema de autenticación funcionando
- [ ] Endpoints protegidos implementados
- [ ] Testing de seguridad realizado
- [ ] Todo funciona sin errores

---

## 📚 **Conceptos Dominados**

- **JWT tokens** para autenticación stateless
- **Password hashing** con bcrypt
- **Dependencias** para protección de endpoints
- **Roles básicos** para autorización
- **HTTP status codes** (401, 403) apropiados

**¡Autenticación y autorización dominadas!** 🔒

---

## 💡 **Si necesitas ayuda**

### **Errores comunes**

1. **"Invalid token"**: Verifica que SECRET_KEY sea la misma
2. **"Not authenticated"**: Asegúrate de enviar el header Authorization
3. **"Insufficient permissions"**: Verifica que el usuario tenga el rol correcto

### **Recursos**

- Documentación FastAPI: `/docs`
- Logs en la terminal donde ejecutas uvicorn
- Prácticas 15-18 como referencia
