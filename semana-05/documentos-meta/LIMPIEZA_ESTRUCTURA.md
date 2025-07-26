# LIMPIEZA DE ESTRUCTURA - SEMANA 5

## Archivos Eliminados

### Prácticas Complejas Eliminadas

- `15-jwt-setup.md` (865 líneas) - JWT complejo con librerías externas
- `16-login-system.md` - Sistema complejo con SQLAlchemy
- `17-endpoint-protection.md` - Middleware avanzado
- `18-roles-authorization.md` - RBAC complejo

### Contenido Complejo Removido

- JWT (JSON Web Tokens) implementation
- SQLAlchemy user management
- OAuth2 authentication flows
- Advanced middleware patterns
- Complex password hashing (bcrypt, passlib)
- Database-based session management

## Archivos Simplificados Creados

### Prácticas Ultra-Simplificadas

- `14-security-basics.md` - API keys & concepts (75 min)
- `15-simple-users.md` - Basic user management (90 min)
- `16-endpoint-protection.md` - Simple protection patterns (90 min)

### Teoría Simplificada

- `auth-concepts.md` - Authentication vs authorization basics only

### Ejercicios Simplificados

- `ejercicios-seguridad.md` - 2 simple security exercises (60 min total)

### Proyecto Simplificado

- `especificacion-auth.md` - Note-taking API with basic security (3 horas)

### Recursos Simplificados

- `recursos-apoyo.md` - Basic security references only

## Nuevo Enfoque: Seguridad Básica

### ANTES (Demasiado Complejo):

- JWT implementation con python-jose
- Password hashing con bcrypt
- OAuth2 flows
- Database user management
- Middleware avanzado
- Testing de seguridad complejo

### DESPUÉS (Ultra-Simplificado):

- API key authentication
- In-memory user storage
- Basic role concepts (user/admin)
- Simple dependency injection
- Conceptual understanding de security
- HTTP status codes para security

## Estructura Final Limpia

```
semana-05/
├── 1-teoria/
│   └── auth-concepts.md           # Conceptos básicos únicamente
├── 2-practica/
│   ├── 14-security-basics.md      # API keys (75 min)
│   ├── 15-simple-users.md         # User basics (90 min)
│   └── 16-endpoint-protection.md  # Simple protection (90 min)
├── 3-ejercicios/
│   └── ejercicios-seguridad.md    # 2 ejercicios básicos (60 min)
├── 4-proyecto/
│   └── especificacion-auth.md     # Note-taking API (180 min)
├── 5-recursos/
│   └── recursos-apoyo.md          # Referencias básicas
├── README.md                      # Planificación 6h + break 30min
└── documentos-meta/
    └── LIMPIEZA_ESTRUCTURA.md
```

## Principios Aplicados

1. **Máximo 6 horas semanales** - Contenido ajustado a security básico
2. **Ultra-simplificación** - Sin JWT, sin bases de datos complejas
3. **Nomenclatura en inglés** - Todos los archivos de contenido
4. **Estructura numerada** - Carpetas 1-5 con contenido esencial
5. **Sin referencias a ajustes** - Documentación limpia para estudiantes
6. **Break de 30 min explícito** - Incluido en planificación
7. **Progresión natural** - Desde query parameters de Semana 4 a security básico

## Tiempo Total Estimado: 6 horas

- Teoría: 60 min
- Prácticas: 255 min (3 prácticas)
- Ejercicios: 60 min
- Proyecto: 180 min
- **Break: 30 min incluido**

**NOTA:** Esta limpieza transforma la Semana 5 de "Autenticación JWT compleja" a "Conceptos básicos de seguridad", manteniendo progresión lógica desde funcionalidades avanzadas de API hacia conceptos de seguridad fundamentales.
