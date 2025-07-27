# Rúbrica de Evaluación - Semana 5: Autenticación y Autorización

## 📊 Información General

**Tema:** Implementación de sistemas de autenticación y autorización seguros con FastAPI  
**Duración:** 6 horas de contenido principal  
**Modalidad:** Prácticas guiadas + proyecto integrador  
**Peso en curso:** 15% de la calificación total del bootcamp

---

## 🎯 Objetivos de Evaluación

### Competencias Centrales Evaluadas

1. **Implementación JWT** - Creación y validación de tokens seguros
2. **Sistema de Autenticación** - Login/logout funcional
3. **Protección de Endpoints** - Middleware y dependency injection
4. **Autorización Básica** - Roles y permisos de usuarios
5. **Buenas Prácticas** - Seguridad y manejo de errores

---

## 📋 Criterios de Evaluación

### 🔐 1. Fundamentos de Autenticación (25% - 25 puntos)

#### **Excelente (23-25 puntos)**

- ✅ Implementa JWT correctamente con todas las configuraciones necesarias
- ✅ Utiliza password hashing con bcrypt de forma segura
- ✅ Configura variables de entorno para secrets apropiadamente
- ✅ Entiende y explica claramente la diferencia entre auth y authorization
- ✅ Maneja expiración de tokens y refresh tokens básico

#### **Proficiente (18-22 puntos)**

- ✅ Implementa JWT con configuración básica funcional
- ✅ Usa password hashing correctamente
- ✅ Configura secrets de forma básica pero segura
- ✅ Comprende conceptos de autenticación vs autorización
- ⚠️ Manejo básico de expiración de tokens

#### **En Desarrollo (13-17 puntos)**

- ⚠️ JWT implementado pero con configuración incompleta
- ⚠️ Password hashing básico pero sin todas las mejores prácticas
- ⚠️ Configuración de secrets mejorable
- ⚠️ Comprensión conceptual básica
- ❌ Manejo limitado de expiración de tokens

#### **Necesita Mejora (0-12 puntos)**

- ❌ JWT mal implementado o no funcional
- ❌ Passwords sin hash o hash inseguro
- ❌ Secrets hardcodeados o mal manejados
- ❌ Confusión entre conceptos básicos
- ❌ No maneja expiración de tokens

---

### 🚪 2. Sistema de Login/Register (25% - 25 puntos)

#### **Excelente (23-25 puntos)**

- ✅ Endpoints de register y login completamente funcionales
- ✅ Validación robusta de datos de entrada (email, password strength)
- ✅ Manejo apropiado de errores (usuario existente, credenciales inválidas)
- ✅ Response models seguros (no expone passwords)
- ✅ Implementa logout o token blacklisting

#### **Proficiente (18-22 puntos)**

- ✅ Endpoints básicos de register y login funcionando
- ✅ Validación básica de datos de entrada
- ✅ Manejo básico de errores comunes
- ✅ Response models apropiados
- ⚠️ Logout básico o no implementado

#### **En Desarrollo (13-17 puntos)**

- ⚠️ Endpoints funcionan pero con validación limitada
- ⚠️ Algunos errores manejados, otros no
- ⚠️ Response models mejorables
- ❌ Sin implementación de logout

#### **Necesita Mejora (0-12 puntos)**

- ❌ Endpoints no funcionan correctamente
- ❌ Validación ausente o muy básica
- ❌ Manejo de errores deficiente
- ❌ Expone información sensible en responses

---

### 🛡️ 3. Protección de Endpoints (25% - 25 puntos)

#### **Excelente (23-25 puntos)**

- ✅ Implementa OAuth2PasswordBearer correctamente
- ✅ Dependency injection para get_current_user funcional
- ✅ Protege múltiples endpoints de forma consistente
- ✅ Maneja tokens inválidos/expirados apropiadamente
- ✅ Implementa diferentes niveles de protección

#### **Proficiente (18-22 puntos)**

- ✅ OAuth2 scheme básico implementado
- ✅ get_current_user funciona correctamente
- ✅ Protege endpoints principales
- ✅ Manejo básico de tokens inválidos
- ⚠️ Niveles de protección limitados

#### **En Desarrollo (13-17 puntos)**

- ⚠️ Protección básica pero inconsistente
- ⚠️ get_current_user con limitaciones
- ⚠️ Algunos endpoints protegidos, otros no
- ⚠️ Manejo de errores básico

#### **Necesita Mejora (0-12 puntos)**

- ❌ Protección no funciona correctamente
- ❌ Dependency injection mal implementado
- ❌ Endpoints importantes sin proteger
- ❌ No maneja tokens inválidos

---

### 👥 4. Roles y Autorización (15% - 15 puntos)

#### **Excelente (14-15 puntos)**

- ✅ Sistema de roles bien diseñado y funcional
- ✅ Endpoints administrativos protegidos correctamente
- ✅ Permissions checking robusto
- ✅ Separation clara entre user/admin capabilities
- ✅ Manejo de unauthorized access

#### **Proficiente (11-13 puntos)**

- ✅ Roles básicos implementados (user/admin)
- ✅ Protección básica de endpoints admin
- ✅ Permission checking funcional
- ⚠️ Separation básica de capabilities

#### **En Desarrollo (8-10 puntos)**

- ⚠️ Roles implementados pero limitados
- ⚠️ Protección básica de algunos endpoints
- ⚠️ Permission checking inconsistente

#### **Necesita Mejora (0-7 puntos)**

- ❌ Sin sistema de roles o mal implementado
- ❌ Endpoints admin sin protección adecuada
- ❌ No verifica permisos correctamente

---

### 🧪 5. Testing y Calidad (10% - 10 puntos)

#### **Excelente (9-10 puntos)**

- ✅ Tests comprehensivos para todos los endpoints de auth
- ✅ Testa scenarios de success y failure
- ✅ Mock authentication en tests
- ✅ Código limpio y bien documentado
- ✅ Manejo de errores robusto

#### **Proficiente (7-8 puntos)**

- ✅ Tests básicos para endpoints principales
- ✅ Algunos scenarios de error tested
- ✅ Código mayormente limpio
- ⚠️ Documentación básica

#### **En Desarrollo (5-6 puntos)**

- ⚠️ Tests limitados o básicos
- ⚠️ Código funcional pero mejorable
- ⚠️ Documentación mínima

#### **Necesita Mejora (0-4 puntos)**

- ❌ Sin tests o tests no funcionan
- ❌ Código desorganizado o confuso
- ❌ Sin documentación

---

## 📊 Escala de Calificación Final

| Puntuación Total  | Calificación            | Equivalencia | Descripción                                                  |
| ----------------- | ----------------------- | ------------ | ------------------------------------------------------------ |
| **90-100 puntos** | **A (Excelente)**       | 4.0          | Dominio completo de autenticación y autorización             |
| **80-89 puntos**  | **B (Proficiente)**     | 3.0          | Implementación sólida con pequeñas áreas de mejora           |
| **70-79 puntos**  | **C (En Desarrollo)**   | 2.0          | Funcionalidad básica, necesita refuerzo en algunos conceptos |
| **60-69 puntos**  | **D (Necesita Mejora)** | 1.0          | Comprensión limitada, requiere revisión significativa        |
| **< 60 puntos**   | **F (No Aprobado)**     | 0.0          | No cumple con los objetivos mínimos                          |

---

## 🎯 Entregables Específicos

### 📦 Proyecto Principal (70% del peso)

**API E-commerce con Sistema de Autenticación Completo**

#### **Funcionalidades Mínimas Requeridas:**

1. **Endpoints de Autenticación:**

   - `POST /auth/register` - Registro de usuarios
   - `POST /auth/login` - Login y generación de JWT
   - `POST /auth/logout` - Logout (opcional: token blacklist)
   - `GET /auth/me` - Obtener usuario actual

2. **Endpoints Protegidos:**

   - `GET /users/profile` - Perfil del usuario autenticado
   - `PUT /users/profile` - Actualizar perfil propio
   - `GET /admin/users` - Listar usuarios (solo admin)
   - `DELETE /admin/users/{id}` - Eliminar usuario (solo admin)

3. **Características Técnicas:**
   - JWT con expiración configurable
   - Password hashing con bcrypt
   - Middleware de autenticación
   - Sistema de roles (user/admin)
   - Validación de datos robusta
   - Manejo de errores apropiado

#### **Estructura de Archivos Esperada:**

```text
proyecto_auth/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   └── auth.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── user.py
│   ├── crud/
│   │   ├── __init__.py
│   │   └── user.py
│   └── api/
│       ├── __init__.py
│       ├── auth.py
│       ├── users.py
│       └── admin.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_users.py
├── .env.example
├── requirements.txt
└── README.md
```

### 📝 Documentación (20% del peso)

#### **README.md Completo:**

- Instrucciones de instalación y setup
- Configuración de variables de entorno
- Ejemplos de uso de endpoints
- Documentación de autenticación
- Guía de testing

#### **Código Documentado:**

- Docstrings en funciones principales
- Comentarios en lógica compleja
- Type hints consistentes

### 🧪 Testing (10% del peso)

#### **Test Suite Mínima:**

- Tests de registro de usuarios
- Tests de login (success/failure)
- Tests de acceso a endpoints protegidos
- Tests de autorización (roles)
- Tests de tokens inválidos/expirados

---

## 📅 Cronograma de Evaluación

### **Durante la Semana**

- **Día 1-2**: Evaluación formativa de ejercicios prácticos
- **Día 3-4**: Revisión de implementación JWT y login
- **Día 5-6**: Evaluación de protección de endpoints
- **Día 7**: Entrega y presentación del proyecto final

### **Metodología de Evaluación**

1. **Evaluación Continua (40%)**

   - Participación en prácticas guiadas
   - Completion de ejercicios incrementales
   - Code reviews de compañeros

2. **Proyecto Final (50%)**

   - Funcionalidad completa
   - Calidad de código
   - Testing coverage

3. **Evaluación Conceptual (10%)**
   - Quiz breve sobre conceptos de seguridad
   - Explicación de decisiones de diseño

---

## 🔍 Casos de Evaluación Específicos

### **Scenario 1: Sistema Básico Funcional**

**Situación:** Estudiante implementa JWT básico y login simple  
**Calificación Esperada:** C (En Desarrollo)  
**Feedback:** "Funcionalidad base correcta, mejorar validaciones y error handling"

### **Scenario 2: Implementación Robusta**

**Situación:** JWT completo, roles funcionales, tests comprehensivos  
**Calificación Esperada:** A (Excelente)  
**Feedback:** "Implementación profesional, excelente manejo de seguridad"

### **Scenario 3: Implementación Insegura**

**Situación:** Passwords sin hash, secrets hardcodeados  
**Calificación Esperada:** D/F (Necesita Mejora/No Aprobado)  
**Feedback:** "Vulnerabilidades críticas de seguridad, requiere rehacer"

---

## 🎯 Objetivos de Aprendizaje vs Evaluación

| Objetivo de Aprendizaje | Método de Evaluación              | Peso |
| ----------------------- | --------------------------------- | ---- |
| **Implementar JWT**     | Código funcional + tests          | 25%  |
| **Sistema de Login**    | Endpoints working + validation    | 25%  |
| **Proteger Endpoints**  | Middleware + dependency injection | 25%  |
| **Gestionar Roles**     | Admin endpoints + authorization   | 15%  |
| **Buenas Prácticas**    | Code quality + security           | 10%  |

---

## 📝 Feedback y Rubrica de Mejora

### **Para Calificación C o Inferior**

#### **Plan de Mejora Requerido:**

1. **Identificar gaps** específicos en implementación
2. **Revisar material** de la semana
3. **Implementar fixes** basados en feedback
4. **Re-submit** proyecto mejorado (dentro de 1 semana)

#### **Recursos de Apoyo:**

- Office hours con instructor
- Pair programming sessions
- Material complementario de seguridad
- Code review sessions

### **Para Todas las Calificaciones**

#### **Feedback Constructivo Incluye:**

- ✅ **Aspectos positivos** específicos
- 🔄 **Áreas de mejora** concretas
- 🎯 **Próximos pasos** recomendados
- 📚 **Recursos adicionales** para profundizar

---

## 🌟 Criterios de Excelencia

### **Para Obtener Calificación A**

**El proyecto debe demostrar:**

- Comprensión profunda de principios de seguridad
- Implementación técnica robusta y profesional
- Código limpio, bien documentado y testeado
- Manejo apropiado de casos edge y errores
- Aplicación consistent de best practices

### **Indicadores de Mastery**

- [ ] **Security-first mindset** en todas las decisiones
- [ ] **Error handling** robusto y user-friendly
- [ ] **Code organization** clara y mantenible
- [ ] **Testing coverage** > 80% en componentes críticos
- [ ] **Documentation** completa y útil
- [ ] **Performance considerations** básicas aplicadas

---

## 🚀 Preparación para Semana 6

### **Skills que se Evalúan como Preparación**

- **Testing avanzado** con authentication mocking
- **Error handling** profesional
- **Code organization** escalable
- **Security consciousness** aplicada consistentemente

### **Conceptos que se Refuerzan**

- Dependency injection patterns
- Middleware design
- Configuration management
- API design principles

---

**¡Esta rúbrica asegura que desarrolles skills de seguridad esenciales para APIs profesionales! 🔐🎯**
