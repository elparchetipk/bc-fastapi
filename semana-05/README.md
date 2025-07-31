# Semana 5: Autenticación y Autorización

⏰ **DURACIÓN TOTAL: 6 HORAS EXACTAS**  
📚 **NIVEL: Intermedio (construye sobre Semanas 1-4)**

## 🚨 **IMPORTANTE: Aplicando Bases de Datos**

Esta semana está diseñada para estudiantes que **ya tienen una API completa con SQLAlchemy** (Semanas 1-4). Implementaremos autenticación y autorización básica.

- ✅ **Completamente realizable en 6 horas**
- ✅ **Enfoque práctico en seguridad básica**
- ✅ **Preparación para APIs con usuarios**

## 🎯 Objetivos de la Semana (Fundamentales)

Al finalizar esta semana de 6 horas (incluye break de 30 min), los estudiantes:

1. ✅ **Implementarán autenticación JWT básica** con FastAPI
2. ✅ **Crearán endpoints de login/registro** seguros
3. ✅ **Protegerán rutas** con dependencias de autenticación
4. ✅ **Manejarán roles básicos** de usuario
5. ✅ **Aplicarán buenas prácticas** de seguridad en APIs

### ❌ **Lo que NO se espera dominar esta semana**

- OAuth2 con proveedores externos
- Sistemas de permisos complejos
- Refresh tokens avanzados
- Middleware personalizado complejo
- Audit logs y monitoring

## ⏱️ Distribución de Tiempo (6 horas total)

| Bloque | Actividad                   | Tiempo | Descripción                     |
| ------ | --------------------------- | ------ | ------------------------------- |
| **1**  | JWT y Hashing Básico        | 90 min | JWT, passwords, setup inicial   |
| **2**  | Sistema de Login            | 90 min | Endpoints de autenticación      |
| **3**  | Protección de Endpoints     | 90 min | Dependencies, rutas protegidas  |
| **4**  | Roles y Autorización Básica | 90 min | Permisos simples, admin vs user |

## 📚 Contenido de la Semana

### **📋 Navegación Ordenada (Seguir este orden)**

1. **[🧭 1-teoria/](./1-teoria/)** - Conceptos de autenticación y seguridad
2. **[💻 2-practica/](./2-practica/)** - Implementación JWT y protección
3. **[🎯 3-ejercicios/](./3-ejercicios/)** - Ejercicios de seguridad
4. **[🚀 4-proyecto/](./4-proyecto/)** - Sistema de autenticación completo
5. **[📚 5-recursos/](./5-recursos/)** - Referencias y herramientas

### **🧭 Teoría**

- [🔐 Autenticación vs Autorización](./1-teoria/auth-concepts.md)

### **💻 Prácticas**

1. [🔧 JWT y Hashing de Passwords](./2-practica/15-jwt-setup.md) _(90 min)_
2. [🚪 Sistema de Login y Registro](./2-practica/16-login-system.md) _(90 min)_
3. [🛡️ Protección de Endpoints](./2-practica/17-endpoint-protection.md) _(90 min)_
4. [👥 Roles y Autorización](./2-practica/18-roles-authorization.md) _(90 min)_

### **💪 Ejercicios**

- [🔒 Ejercicios de Seguridad](./3-ejercicios/ejercicios-seguridad.md)

### **🚀 Proyecto**

- [🏪 E-commerce con Autenticación](./4-proyecto/especificacion-auth.md)

### **📚 Recursos**

- [📖 Recursos de Apoyo](./5-recursos/recursos-apoyo.md)

---

## 🔐 Tecnologías de la Semana

### **Stack de Autenticación**

- **JWT**: `python-jose[cryptography]` - Tokens de autenticación
- **Hashing**: `passlib[bcrypt]` - Encriptación de passwords
- **OAuth2**: FastAPI OAuth2PasswordBearer - Estándar de autenticación
- **SQLAlchemy**: Gestión de usuarios en base de datos

### **Herramientas de Testing**

- **Postman/Thunder Client**: Testing manual de endpoints con JWT
- **pytest**: Testing automatizado de autenticación
- **httpx**: Cliente HTTP para tests

---

## ⏱️ **Estructura de 6 Horas (Incluye Break de 30 min)**

### **Bloque 1: JWT y Hashing (75 min)**

- **15-jwt-setup.md**
- Configuración de librerías de autenticación
- Implementación de hashing de passwords
- Generación y verificación de tokens JWT

### **☕ BREAK OBLIGATORIO (30 min)**

- Descanso para asimilar conceptos de seguridad
- Tiempo para resolver dudas sobre JWT
- Preparación mental para sistema de login

### **Bloque 2: Sistema de Login (120 min)**

- **16-login-system.md**
- Endpoints de registro y login
- Validación de credenciales
- Respuesta con tokens

### **Bloque 3: Protección de Rutas (90 min)**

- **17-endpoint-protection.md**
- Dependencies de autenticación
- Protección de endpoints sensibles
- Manejo de usuarios autenticados

### **Bloque 4: Roles Básicos (45 min)**

- **18-roles-authorization.md**
- Sistema básico de roles (admin/user)
- Restricciones por rol
- Endpoints administrativos

---

## 📋 Pre-requisitos Esenciales

### **✅ Conocimientos Requeridos**

- [x] **FastAPI básico** (Semanas 1-3)
- [x] **SQLAlchemy y bases de datos** (Semana 4)
- [x] **Pydantic models** (Semanas 2-4)
- [x] **CRUD operations** (Semana 4)

### **⚠️ Si no tienes estos conocimientos**

- Completar semanas anteriores primero
- Revisar ejercicios de refuerzo
- Consultar con instructores antes de continuar

---

## 🎯 Competencias que Desarrollarás

**Al inicio de la semana ya sabes:**

- Crear APIs REST completas
- Trabajar con bases de datos
- Implementar CRUD operations
- Usar Pydantic para validación

**Al final de la semana dominarás:**

- ✅ **Autenticación JWT** - Login y tokens seguros
- ✅ **Hashing de passwords** - Almacenamiento seguro
- ✅ **Protección de rutas** - Endpoints que requieren login
- ✅ **Roles básicos** - Diferencias entre admin y usuario
- ✅ **Buenas prácticas** - Seguridad básica en APIs

---

## 🚀 Quick Start

```bash
# 1. Instalar dependencias de autenticación
pip install python-jose[cryptography] passlib[bcrypt] python-multipart

# 2. Actualizar requirements.txt
pip freeze > requirements.txt

# 3. Crear variables de entorno
echo "SECRET_KEY=tu-clave-secreta-muy-larga-aqui" > .env
echo "ALGORITHM=HS256" >> .env
echo "ACCESS_TOKEN_EXPIRE_MINUTES=30" >> .env

# 4. ¡Listo para empezar con autenticación!
```

## � Cronograma de la Jornada de 6 Horas

| Tiempo      | Actividad                     | Duración | Acumulado |
| ----------- | ----------------------------- | -------- | --------- |
| 12:00-13:15 | JWT y Hashing                 | 75 min   | 75 min    |
| 13:15-14:00 | Sistema de Login (parte 1)    | 45 min   | 120 min   |
| 14:00-14:30 | **☕ BREAK OBLIGATORIO**      | 30 min   | 150 min   |
| 14:30-15:45 | Sistema de Login (parte 2)    | 75 min   | 225 min   |
| 15:45-17:15 | Protección de Rutas           | 90 min   | 315 min   |
| 17:15-18:00 | Roles básicos y consolidación | 45 min   | 360 min   |

**Total**: Exactamente 6 horas (360 minutos)

### **📖 Orden de Estudio Recomendado**

1. **JWT y hashing** - Fundamentos de seguridad
2. **Sistema de login** - Registro y autenticación
3. **Protección de rutas** - Endpoints seguros
4. **Roles básicos** - Control de acceso
5. **Ejercicios y proyecto** - Para reforzar conceptos

---

## 💡 Tips para el Éxito

1. **🔒 Seguridad primero**: Nunca almacenar passwords en texto plano
2. **🔑 Variables de entorno**: Usar .env para datos sensibles
3. **🧪 Testing manual**: Probar login y acceso con Postman
4. **� Leer errores**: Los mensajes de autenticación son específicos
5. **⚠️ Manejo de errores**: Respuestas seguras sin revelar información

---

## 📊 Evaluación Final

### **Al completar la semana debes poder:**

- [x] Explicar diferencia entre autenticación y autorización
- [x] Implementar sistema de login con JWT
- [x] Proteger endpoints que requieren autenticación
- [x] Manejar roles básicos (admin vs usuario)
- [x] Testing manual de autenticación con herramientas

### **📦 Entregables**

1. **API con autenticación funcionando**
2. **Sistema de roles implementado**
3. **Endpoints protegidos correctamente**
4. **Testing manual exitoso**

---

## 🆘 Soporte

- **📚 Documentación**: FastAPI Security docs
- **� Instructor**: Consultas durante clases
- **� Compañeros**: Colaboración en ejercicios
- **📞 Slack**: Canal del bootcamp para dudas

---

## 🎉 ¡Prepárate para crear APIs seguras! 🔐✨
