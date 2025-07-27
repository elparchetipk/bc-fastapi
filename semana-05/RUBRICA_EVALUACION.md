# RÚBRICA DE EVALUACIÓN - SEMANA 5

## Autenticación y Autorización

### INFORMACIÓN GENERAL

- **Semana**: 5
- **Tema**: JWT, Autenticación, Login System y Roles Básicos
- **Duración**: 6 horas (incluye break de 30 min)
- **Prerequisitos**: Semana 4 aprobada (SQLAlchemy y CRUD funcionando)
- **Modalidad**: Evaluación automática por IA + revisión manual

### CRITERIOS DE EVALUACIÓN

#### 1. CONFIGURACIÓN JWT Y HASHING (25 puntos)

**Evidencia requerida**: JWT y password hashing implementados correctamente

| Criterio               | Excelente (5pts)                      | Bueno (4pts)                   | Suficiente (3pts)            | Insuficiente (0pts)      |
| ---------------------- | ------------------------------------- | ------------------------------ | ---------------------------- | ------------------------ |
| **JWT Setup**          | python-jose configurado y funcionando | JWT básico implementado        | JWT simple funcionando       | JWT no funciona          |
| **Password Hashing**   | bcrypt con passlib configurado        | Hashing básico funcionando     | Hash simple implementado     | Sin hashing de passwords |
| **Secret Management**  | SECRET_KEY en variables de entorno    | Secret configurado básicamente | Secret hardcoded pero seguro | Secrets inseguros        |
| **Token Generation**   | Tokens generados con expiración       | Tokens básicos generados       | Tokens simples               | Tokens no funcionan      |
| **Token Verification** | Verificación completa de tokens       | Verificación básica funcional  | Verificación simple          | Sin verificación         |

#### 2. SISTEMA DE LOGIN (25 puntos)

**Evidencia requerida**: Endpoints de registro y login funcionando

| Criterio              | Excelente (5pts)                    | Bueno (4pts)              | Suficiente (3pts)         | Insuficiente (0pts)   |
| --------------------- | ----------------------------------- | ------------------------- | ------------------------- | --------------------- |
| **Register Endpoint** | POST /register completo y seguro    | Registro básico funcional | Endpoint registro simple  | Registro no funciona  |
| **Login Endpoint**    | POST /login con validación completa | Login básico funcionando  | Login simple implementado | Login no funciona     |
| **User Model**        | Modelo User con campos necesarios   | Modelo básico funcional   | Modelo simple creado      | Sin modelo de usuario |
| **Data Validation**   | Validación robusta con Pydantic     | Validaciones básicas      | Validación mínima         | Sin validaciones      |
| **Error Handling**    | Manejo apropiado de errores de auth | Errores básicos manejados | Algunos errores manejados | Sin manejo de errores |

#### 3. PROTECCIÓN DE ENDPOINTS (25 puntos)

**Evidencia requerida**: Endpoints protegidos con JWT funcionando

| Criterio                 | Excelente (5pts)                      | Bueno (4pts)                     | Suficiente (3pts)            | Insuficiente (0pts)       |
| ------------------------ | ------------------------------------- | -------------------------------- | ---------------------------- | ------------------------- |
| **OAuth2 Scheme**        | OAuth2PasswordBearer configurado      | OAuth2 básico implementado       | Scheme simple funcionando    | Sin OAuth2 scheme         |
| **Get Current User**     | Dependency get_current_user funcional | Función básica funcionando       | Usuario extraído del token   | Sin extracción de usuario |
| **Protected Endpoints**  | Múltiples endpoints protegidos        | Endpoints principales protegidos | Algunos endpoints protegidos | Sin protección            |
| **Token Validation**     | Validación completa de tokens         | Validación básica funcional      | Validación simple            | Sin validación de tokens  |
| **Dependency Injection** | Dependencies usadas correctamente     | Uso básico de dependencies       | Dependencies simples         | Sin dependencies          |

#### 4. ROLES Y AUTORIZACIÓN (15 puntos)

**Evidencia requerida**: Sistema básico de roles implementado

| Criterio              | Excelente (3pts)                | Bueno (2pts)                 | Suficiente (1pts)       | Insuficiente (0pts)     |
| --------------------- | ------------------------------- | ---------------------------- | ----------------------- | ----------------------- |
| **Role Model**        | Campo role en modelo User       | Roles básicos implementados  | Campo role simple       | Sin modelo de roles     |
| **Admin Endpoints**   | Endpoints solo para admin       | Protección admin básica      | Algunos endpoints admin | Sin endpoints admin     |
| **Role Checking**     | Verificación de roles funcional | Checks básicos de roles      | Verificación simple     | Sin verificación        |
| **Authorization**     | Diferenciación clara user/admin | Separación básica de roles   | Roles distinguidos      | Sin autorización        |
| **Permission System** | Sistema básico de permisos      | Permisos simples funcionando | Permisos básicos        | Sin sistema de permisos |

#### 5. TESTING Y CALIDAD (10 puntos)

**Evidencia requerida**: Testing manual y código organizado

| Criterio              | Excelente (2pts)                     | Bueno (1.5pts)              | Suficiente (1pts)        | Insuficiente (0pts)  |
| --------------------- | ------------------------------------ | --------------------------- | ------------------------ | -------------------- |
| **Manual Testing**    | Testing completo con Postman         | Testing básico realizado    | Algunas pruebas manuales | Sin testing manual   |
| **Code Organization** | Código bien estructurado en archivos | Organización básica         | Estructura simple        | Código desorganizado |
| **Documentation**     | README con instrucciones claras      | Documentación básica        | Documentación mínima     | Sin documentación    |
| **Error Messages**    | Mensajes de error informativos       | Mensajes básicos útiles     | Mensajes simples         | Mensajes confusos    |
| **Best Practices**    | Buenas prácticas de seguridad        | Prácticas básicas aplicadas | Algunas buenas prácticas | Sin buenas prácticas |

### CRITERIOS DE APROBACIÓN

| Puntuación Total | Calificación        | Equivalencia | Estado                |
| ---------------- | ------------------- | ------------ | --------------------- |
| **90-100 pts**   | **A (Excelente)**   | 4.0          | Dominio completo      |
| **80-89 pts**    | **B (Proficiente)** | 3.0          | Implementación sólida |
| **70-79 pts**    | **C (Suficiente)**  | 2.0          | Funcionalidad básica  |
| **60-69 pts**    | **D (Deficiente)**  | 1.0          | Necesita mejoras      |
| **< 60 pts**     | **F (Reprobado)**   | 0.0          | No cumple objetivos   |

### ENTREGABLES REQUERIDOS

#### PROYECTO PRINCIPAL (80% del peso)

##### API con Sistema de Autenticación Básico

**Funcionalidades Mínimas:**

1. **Endpoints de Autenticación:**

   - `POST /auth/register` - Registro de usuarios
   - `POST /auth/login` - Login con JWT
   - `GET /auth/me` - Usuario actual

2. **Endpoints Protegidos:**

   - `GET /users/profile` - Perfil del usuario
   - `PUT /users/profile` - Actualizar perfil
   - `GET /admin/users` - Listar usuarios (solo admin)

3. **Características Técnicas:**
   - JWT con expiración
   - Password hashing con bcrypt
   - Sistema básico de roles (user/admin)
   - Validación con Pydantic
   - Manejo de errores HTTP

#### ESTRUCTURA DE ARCHIVOS BÁSICA

```text
proyecto_auth/
├── main.py
├── auth.py
├── models.py
├── schemas.py
├── database.py
├── requirements.txt
├── .env.example
└── README.md
```

#### DOCUMENTACIÓN (15% del peso)

- README.md con instrucciones de setup
- Ejemplos de uso de endpoints
- Variables de entorno documentadas

#### TESTING MANUAL (5% del peso)

- Evidencia de testing con Postman/Thunder Client
- Screenshots o documentación de pruebas realizadas
- Verificación de login y acceso a rutas protegidas

### METODOLOGÍA DE EVALUACIÓN

#### Durante la Semana

- **Día 1-2**: Ejercicios de JWT y hashing
- **Día 3-4**: Sistema de login
- **Día 5**: Protección de endpoints y roles
- **Día 6**: Entrega del proyecto final

#### Distribución de Evaluación

- **Ejercicios Prácticos (30%)**: Ejercicios incrementales durante la semana
- **Proyecto Final (60%)**: API completa con autenticación
- **Participación (10%)**: Participación en clases y code reviews

### CASOS DE EVALUACIÓN COMUNES

#### Escenario 1: Implementación Básica

- JWT funcionando, login simple
- **Calificación Esperada:** C (Suficiente)
- **Feedback:** "Funcionalidad base correcta, mejorar validaciones"

#### Escenario 2: Implementación Completa

- JWT robusto, roles funcionando, testing completo
- **Calificación Esperada:** A (Excelente)
- **Feedback:** "Implementación profesional y segura"

#### Escenario 3: Problemas de Seguridad

- Passwords sin hash, secrets expuestos
- **Calificación Esperada:** F (Reprobado)
- **Feedback:** "Vulnerabilidades críticas, requiere rehacer"

### RECURSOS DE APOYO

#### Para Calificación C o Inferior

- Office hours con instructor
- Material complementario de seguridad
- Sesiones de code review
- Re-entrega permitida (1 semana adicional)

---

## 🎯 ¡Evalúa tu progreso en autenticación y autorización! 🔐
