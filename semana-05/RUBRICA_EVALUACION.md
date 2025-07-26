# RÚBRICA DE EVALUACIÓN - SEMANA 5

## Basic Security & Simple Authentication

### INFORMACIÓN GENERAL

- **Semana**: 5
- **Tema**: Basic Security Concepts & Simple Authentication
- **Duración**: 6 horas (incluye break de 30 min)
- **Prerequisitos**: Semana 4 aprobada (Query parameters y validación avanzada)
- **Modalidad**: Evaluación automática por IA + revisión manual

### CRITERIOS DE EVALUACIÓN

#### 1. SECURITY CONCEPTS UNDERSTANDING (20 puntos)

**Evidencia requerida**: Implementación que demuestre comprensión de conceptos básicos

| Criterio                            | Excelente (4pts)                                  | Bueno (3pts)                    | Suficiente (2pts)                   | Insuficiente (0pts)                |
| ----------------------------------- | ------------------------------------------------- | ------------------------------- | ----------------------------------- | ---------------------------------- |
| **Authentication vs Authorization** | Claramente distingue y aplica ambos conceptos     | Comprende diferencias básicas   | Confusión ocasional entre conceptos | No distingue conceptos             |
| **Security Awareness**              | Demuestra comprensión de vulnerabilidades básicas | Entiende riesgos principales    | Conocimiento superficial            | Sin conciencia de seguridad        |
| **HTTP Status Codes**               | Usa 401, 403 apropiadamente                       | Uso correcto de códigos básicos | Algunos códigos correctos           | Códigos incorrectos o ausentes     |
| **Error Messages**                  | Mensajes seguros sin exposición de datos          | Mensajes apropiados básicos     | Algunos mensajes apropiados         | Mensajes que exponen información   |
| **Best Practices**                  | Aplica principios básicos de seguridad            | Algunas buenas prácticas        | Práctica mínima                     | Sin aplicación de buenas prácticas |

#### 2. API KEY AUTHENTICATION (25 puntos)

**Evidencia requerida**: Sistema de API keys funcional

| Criterio                   | Excelente (5pts)                          | Bueno (4pts)                   | Suficiente (3pts)         | Insuficiente (0pts)          |
| -------------------------- | ----------------------------------------- | ------------------------------ | ------------------------- | ---------------------------- |
| **API Key Implementation** | Sistema completo y funcional              | Implementación básica correcta | Sistema simple funcional  | API keys no funcionan        |
| **Header Processing**      | Manejo correcto de headers X-API-Key      | Headers básicos procesados     | Algunos headers manejados | Sin procesamiento de headers |
| **Key Validation**         | Validación robusta con errores apropiados | Validación básica funcional    | Validación simple         | Sin validación               |
| **Public vs Protected**    | Clara distinción entre endpoints          | Distinción básica implementada | Algunas diferencias       | Sin diferenciación           |
| **Error Handling**         | Manejo completo de escenarios de error    | Errores básicos manejados      | Algunos errores manejados | Sin manejo de errores        |

#### 3. SIMPLE USER MANAGEMENT (25 puntos)

**Evidencia requerida**: Sistema básico de usuarios en memoria

| Criterio              | Excelente (5pts)                         | Bueno (4pts)                    | Suficiente (3pts)               | Insuficiente (0pts)     |
| --------------------- | ---------------------------------------- | ------------------------------- | ------------------------------- | ----------------------- |
| **User Model**        | Modelo bien estructurado con roles       | Modelo básico funcional         | Modelo simple creado            | Sin modelo de usuario   |
| **In-Memory Storage** | Gestión eficiente de usuarios            | Almacenamiento básico funcional | Almacenamiento simple           | Sin gestión de usuarios |
| **Login Logic**       | Lógica completa de autenticación         | Login básico funcional          | Login simple implementado       | Login no funciona       |
| **Password Handling** | Manejo conceptual apropiado de passwords | Handling básico de passwords    | Passwords manejados básicamente | Passwords expuestos     |
| **User Sessions**     | Concepto de sesión implementado          | Sesión básica                   | Intento de sesión               | Sin concepto de sesión  |

#### 4. ENDPOINT PROTECTION (20 puntos)

**Evidencia requerida**: Endpoints protegidos con verificación de acceso

| Criterio                 | Excelente (4pts)                    | Bueno (3pts)                | Suficiente (2pts)      | Insuficiente (0pts)      |
| ------------------------ | ----------------------------------- | --------------------------- | ---------------------- | ------------------------ |
| **Dependency Injection** | Uso correcto de Depends para auth   | Depends básico implementado | Algunos Depends usados | Sin dependency injection |
| **Role-Based Access**    | Sistema de roles funcional          | Roles básicos implementados | Intentos de roles      | Sin control de roles     |
| **Resource Ownership**   | Usuarios acceden solo a sus datos   | Separación básica de datos  | Algunos controles      | Sin separación de datos  |
| **Admin Functions**      | Funcionalidades admin protegidas    | Algunos controles admin     | Admin básico           | Sin funciones admin      |
| **Access Control Flow**  | Flujo completo de control de acceso | Flujo básico funcional      | Flujo simple           | Sin flujo de control     |

#### 5. INTEGRATION & TESTING (10 puntos)

**Evidencia requerida**: Sistema integrado y probado

| Criterio                 | Excelente (2pts)                              | Bueno (1.5pts)               | Suficiente (1pt)           | Insuficiente (0pts)            |
| ------------------------ | --------------------------------------------- | ---------------------------- | -------------------------- | ------------------------------ |
| **Security Integration** | Todas las funciones de seguridad integradas   | Integración básica funcional | Integración parcial        | Sin integración                |
| **Security Testing**     | Múltiples escenarios de seguridad probados    | Testing básico realizado     | Algunas pruebas            | Sin testing de seguridad       |
| **Documentation**        | Documentación clara de funciones de seguridad | Documentación básica         | Documentación mínima       | Sin documentación              |
| **Code Quality**         | Código limpio y organizado                    | Código funcional y claro     | Código básico funcional    | Código desorganizado           |
| **Error Scenarios**      | Manejo completo de casos de error             | Casos básicos manejados      | Algunos casos considerados | Sin manejo de casos especiales |

### ESCALA DE CALIFICACIÓN

- **Excelente (90-100 pts)**: Comprensión sólida de conceptos básicos de seguridad
- **Bueno (80-89 pts)**: Implementación correcta de funcionalidades básicas de seguridad
- **Suficiente (70-79 pts)**: Conceptos básicos de seguridad funcionando
- **Insuficiente (0-69 pts)**: Requiere refuerzo en fundamentos de seguridad

### CRITERIOS DE APROBACIÓN

- **Mínimo para aprobar**: 70 puntos (70%)
- **Entregables obligatorios**:
  - Al menos 1 endpoint protegido con API key funcional
  - Sistema básico de usuarios (in-memory)
  - Diferenciación entre public y protected endpoints
  - Comprensión demostrada de authentication vs authorization

### RETROALIMENTACIÓN AUTOMÁTICA

**Para el agente evaluador de IA:**

#### Puntos de verificación automática:

1. **API Key Headers**: Verificar uso de Header() en funciones de verificación
2. **Depends Usage**: Confirmar que Depends está usado para protección
3. **HTTPException**: Verificar manejo de errores 401 y 403
4. **User Storage**: Buscar diccionarios o listas para gestión de usuarios
5. **Role Differentiation**: Identificar diferentes niveles de acceso

#### Indicadores de calidad:

- Uso apropiado de HTTP status codes para seguridad
- Separación clara entre endpoints públicos y protegidos
- Manejo básico de roles (user/admin)
- Mensajes de error informativos pero seguros
- Implementación de dependency injection para auth

#### Señales de alarma para revisión manual:

- Passwords almacenados en texto plano visible
- Falta de diferenciación entre public/protected endpoints
- API keys hardcodeadas sin gestión
- Ausencia de manejo de errores de seguridad
- Roles implementados sin verificación

#### Patrones de código esperados:

```python
# Esperado: API Key verification
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key not in VALID_KEYS:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return VALID_KEYS[x_api_key]

# Esperado: Protected endpoint
@app.get("/protected")
def protected_endpoint(user=Depends(verify_api_key)):
    return {"message": f"Hello {user['name']}"}

# Esperado: Role checking
def require_admin(user=Depends(verify_api_key)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin required")
    return user
```

### FEEDBACK PERSONALIZADO POR NIVEL

#### Para estudiantes destacados (90-100 pts):

- Reconocer comprensión sólida de conceptos de seguridad
- Destacar implementación apropiada de controles de acceso
- Preparar para conceptos más avanzados (JWT, OAuth2 en proyectos futuros)

#### Para estudiantes en nivel esperado (80-89 pts):

- Confirmar comprensión correcta de authentication vs authorization
- Señalar mejoras menores en implementación de seguridad
- Reforzar progreso hacia APIs seguras

#### Para estudiantes en nivel mínimo (70-79 pts):

- Identificar conceptos de seguridad que necesitan refuerzo
- Proporcionar ejercicios específicos para API keys y roles
- Asegurar base sólida antes de conceptos avanzados

#### Para estudiantes por debajo del mínimo (0-69 pts):

- Análisis detallado de gaps en conceptos de seguridad
- Plan de recuperación enfocado en authentication básico
- Sesión de apoyo para conceptos fundamentales

### CONEXIÓN CON SEMANAS ANTERIORES

- **Semanas 1-4**: Construye sobre API completa con funcionalidades avanzadas
- **Preparación futuras**: Base para conceptos de seguridad más avanzados
- **Progresión**: De funcionalidades a seguridad básica

### RECURSOS PARA ESTUDIANTES

- FastAPI Security: https://fastapi.tiangolo.com/tutorial/security/
- HTTP Authentication: https://developer.mozilla.org/en-US/docs/Web/HTTP/Authentication
- OWASP Security Guide: https://owasp.org/www-community/controls/
- Ejemplos de código de las prácticas de la semana

**Fecha de creación**: 25 de julio de 2025  
**Versión**: 1.0  
**Próxima revisión**: Al finalizar implementación del bootcamp
