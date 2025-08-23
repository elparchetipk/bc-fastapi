# Práctica 24: Consolidación y Testing Completo

## 🎯 Objetivo

**Consolidar y verificar todo el sistema** de autenticación, roles y testing implementado durante la semana, asegurando funcionamiento completo en 45 minutos.

## ⏱️ Tiempo: 45 minutos

## 📋 Pre-requisitos

- ✅ Testing básico configurado (Prácticas 19-21)
- ✅ Sistema de roles implementado (Práctica 23)
- ✅ Autenticación funcionando (Semana 5)

---

## 🔍 Paso 1: Verificación Completa del Sistema (15 min)

### Checklist de Funcionamiento Integral

**Marca cada elemento que funciona correctamente:**

#### **Autenticación (Semana 5)**

- [ ] **JWT tokens**: Login retorna token válido
- [ ] **Password hashing**: Passwords se guardan hasheados
- [ ] **Token verification**: Endpoints protegidos validan token
- [ ] **User extraction**: Se puede obtener usuario del token

#### **Roles y Autorización (Semana 6)**

- [ ] **Role field**: Campo role en modelo User
- [ ] **Admin creation**: Se puede crear primer admin
- [ ] **Role checking**: require_admin funciona correctamente
- [ ] **Admin endpoints**: Solo admins acceden a /admin/\*

#### **Testing Automatizado (Semana 6)**

- [ ] **Pytest setup**: pytest ejecuta sin errores
- [ ] **Auth tests**: Tests de login/registro pasan
- [ ] **Role tests**: Tests de autorización pasan
- [ ] **CRUD tests**: Tests de endpoints funcionan

### Comando de Verificación Rápida

```bash
# 1. Ejecutar todos los tests
pytest -v

# 2. Verificar estructura de archivos
ls -la app/
ls -la app/routers/
ls -la tests/

# 3. Verificar servidor funciona
uvicorn app.main:app --reload
```

---

## 🧪 Paso 2: Suite de Testing Completa (20 min)

### Ejecutar Testing Integral

#### Test 1: Autenticación Completa (5 min)

```bash
# Ejecutar solo tests de autenticación
pytest tests/test_auth.py -v

# Verificar que pasan:
# ✅ test_register_user_success
# ✅ test_login_user_success
# ✅ test_get_current_user_with_valid_token
# ✅ test_access_protected_endpoint
```

#### Test 2: Roles y Autorización (5 min)

```bash
# Ejecutar solo tests de roles
pytest tests/test_roles.py -v

# Verificar que pasan:
# ✅ test_admin_can_list_users
# ✅ test_regular_user_cannot_access_admin_endpoints
# ✅ test_admin_can_change_user_role
# ✅ test_create_first_admin_success
```

#### Test 3: CRUD con Autenticación (5 min)

```bash
# Ejecutar tests de endpoints CRUD
pytest tests/test_endpoints.py -v

# Verificar que pasan:
# ✅ test_create_resource_authenticated
# ✅ test_get_resource_authenticated
# ✅ test_update_own_resource
# ✅ test_cannot_update_other_user_resource
```

#### Test 4: Coverage Básico (5 min)

```bash
# Instalar coverage si no está
pip install coverage

# Ejecutar con coverage
coverage run -m pytest
coverage report

# Objetivo: >70% coverage en archivos principales
```

---

## 🚀 Paso 3: Testing Manual de Integración (10 min)

### Flujo Completo de Usuario

#### Escenario 1: Usuario Normal (3 min)

```bash
# 1. Registrarse
curl -X POST "http://127.0.0.1:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@test.com",
       "full_name": "Regular User",
       "password": "user123"
     }'

# 2. Login
curl -X POST "http://127.0.0.1:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=user@test.com&password=user123"

# 3. Acceder a perfil (con token)
curl -X GET "http://127.0.0.1:8000/auth/me" \
     -H "Authorization: Bearer YOUR_USER_TOKEN"

# 4. Intentar acceso admin (debe fallar)
curl -X GET "http://127.0.0.1:8000/admin/users" \
     -H "Authorization: Bearer YOUR_USER_TOKEN"
```

#### Escenario 2: Usuario Admin (4 min)

```bash
# 1. Crear primer admin
curl -X POST "http://127.0.0.1:8000/admin/create-first-admin" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "admin@test.com",
       "full_name": "Admin User",
       "password": "admin123"
     }'

# 2. Login como admin
curl -X POST "http://127.0.0.1:8000/auth/login" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin@test.com&password=admin123"

# 3. Listar usuarios
curl -X GET "http://127.0.0.1:8000/admin/users" \
     -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# 4. Cambiar rol de usuario
curl -X PUT "http://127.0.0.1:8000/admin/users/1/role" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
     -d '{"role": "admin"}'
```

#### Escenario 3: Swagger UI (3 min)

```bash
# 1. Abrir Swagger UI
# http://127.0.0.1:8000/docs

# 2. Probar login desde Swagger
# 3. Autorizar con token en Swagger
# 4. Probar endpoints protegidos desde Swagger
```

---

## 🐛 Paso 4: Troubleshooting y Optimización (10 min)

### Problemas Comunes y Soluciones

#### Error 1: Tests fallan por DB

**Síntoma**: `database is locked` o `table already exists`

**Solución**:

```bash
# Limpiar base de datos de test
rm -f test.db
rm -f test_*.db

# Re-ejecutar tests
pytest -v
```

#### Error 2: Import errors

**Síntoma**: `ModuleNotFoundError` en tests

**Solución**:

```python
# Verificar PYTHONPATH en conftest.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
```

#### Error 3: Admin endpoints no funcionan

**Síntoma**: `404 Not Found` en /admin/\*

**Solución**:

```python
# Verificar que router está incluido en main.py
from app.routers import admin
app.include_router(admin.router)
```

#### Error 4: Roles no se asignan

**Síntoma**: Todos los usuarios tienen role="user"

**Solución**:

```python
# Verificar migración de DB
# Si usas SQLite simple, eliminar y recrear
rm database.db
# Iniciar servidor para recrear con nuevo schema
```

### Optimización Final

```python
# Verificar que todos los endpoints están documentados
# en Swagger UI con ejemplos claros

# app/main.py
app = FastAPI(
    title="API with Auth and Roles",
    description="Complete API with JWT authentication and role-based authorization",
    version="1.0.0"
)
```

---

## ✅ Checklist de Sistema Completo

### **Funcionalidad Core**

- [ ] **Registro de usuarios** funcionando
- [ ] **Login con JWT** funcionando
- [ ] **Endpoints protegidos** requieren autenticación
- [ ] **Sistema de roles** admin/user operativo
- [ ] **Endpoints administrativos** solo para admins

### **Testing Automatizado**

- [ ] **Suite de tests** ejecuta sin errores
- [ ] **Coverage >70%** en archivos principales
- [ ] **Tests de auth** cubren casos principales
- [ ] **Tests de roles** verifican autorización
- [ ] **CI/CD ready** (tests preparados para automatización)

### **Documentation & Quality**

- [ ] **Swagger UI** funcionando con autenticación
- [ ] **README** con instrucciones claras
- [ ] **Code organization** clara y profesional
- [ ] **Error handling** apropiado
- [ ] **Security practices** implementadas

### **Manual Testing**

- [ ] **User journey** completo funciona
- [ ] **Admin journey** completo funciona
- [ ] **Error cases** manejados apropiadamente
- [ ] **UI/UX** en Swagger clara y funcional

---

## 🎯 Resultado Final

**Al completar esta consolidación tienes:**

### **API Production-Ready con:**

1. **Autenticación JWT** completa y segura
2. **Sistema de roles** admin/user funcional
3. **Testing automatizado** con buena cobertura
4. **Documentación API** clara en Swagger
5. **Error handling** robusto
6. **Security best practices** implementadas

### **Skills Desarrollados:**

- ✅ **FastAPI avanzado** con autenticación
- ✅ **Testing de APIs** con pytest
- ✅ **Role-based authorization** (RBAC)
- ✅ **JWT tokens** y seguridad
- ✅ **API documentation** profesional
- ✅ **Code organization** y best practices

### **Preparación para:**

- APIs en producción
- Sistemas multi-usuario
- Arquitecturas escalables
- Testing automatizado en CI/CD
- Desarrollo profesional en equipo

---

## 📚 Conceptos Aplicados Esta Semana

- **Test-Driven Development** básico
- **Authentication vs Authorization** en práctica
- **JWT tokens** seguros y escalables
- **Role-Based Access Control** (RBAC)
- **API testing** automatizado
- **FastAPI dependencies** avanzadas
- **Database migrations** básicas
- **API documentation** profesional

## 🚀 Próximos Pasos

**En la siguiente semana agregarás:**

- Coverage avanzado y reportes detallados
- Testing con mocks complejos
- CI/CD básico con GitHub Actions
- Performance testing
- Security testing automatizado

**¡Sistema completo de autenticación y roles con testing exitosamente implementado!** 🎉👑🧪
