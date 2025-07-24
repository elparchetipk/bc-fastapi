# Estructura del Proyecto - Bootcamp bc-fastapi

## 📁 Organización General

```
bc-fastapi/
├── 📄 README.md                           # Documentación principal del proyecto
├── 📄 CHANGELOG.md                        # Registro de cambios y contribuciones
├── 📄 CONTRIBUTING.md                     # Guía de contribución
├── 📄 CODE_OF_CONDUCT.md                  # Código de conducta de la comunidad
├── 📄 LICENSE                             # Licencia MIT
├── 📄 .gitignore                          # Archivos ignorados por Git
├── 📄 plan-trabajo-detallado.md           # Plan completo del bootcamp
│
├── 📁 .github/                            # Configuración de GitHub
│   ├── 📄 .copilot-instructions.md        # Instrucciones para GitHub Copilot
│   ├── 📄 PULL_REQUEST_TEMPLATE.md        # Template para Pull Requests
│   └── 📁 ISSUE_TEMPLATE/                 # Templates para Issues
│       ├── 📄 bug_report.md               # Template para reportar bugs
│       ├── 📄 feature_request.md          # Template para solicitar features
│       ├── 📄 question.md                 # Template para preguntas
│       └── 📄 config.yml                  # Configuración de templates
│
├── 📁 _docs/                              # 📚 Documentación del proyecto
│   ├── 📁 setup/                          # Guías de instalación y configuración
│   ├── 📁 guides/                         # Tutoriales de desarrollo
│   ├── 📁 api/                            # Documentación de APIs
│   ├── 📁 architecture/                   # Documentación de arquitectura
│   └── 📁 troubleshooting/                # Solución de problemas
│
├── 📁 _scripts/                           # 🔧 Scripts de automatización
│   ├── 📁 setup/                          # Scripts de configuración inicial
│   ├── 📁 deployment/                     # Scripts de despliegue
│   ├── 📁 testing/                        # Scripts de testing
│   └── 📁 utilities/                      # Utilidades y herramientas
│
├── 📁 recursos-compartidos/               # 🛠️ Recursos transversales
│   ├── 📁 templates/                      # Templates de código
│   ├── 📁 configs/                        # Configuraciones compartidas
│   ├── 📁 databases/                      # Scripts de base de datos
│   └── 📁 tools/                          # Herramientas de desarrollo
│
├── 📁 semana-01/                          # 🎯 Fundamentos y Configuración
│   ├── 📁 teoria/                         # Material teórico
│   ├── 📁 practica/                       # Ejercicios prácticos
│   ├── 📁 ejercicios/                     # Ejercicios individuales
│   ├── 📁 proyecto/                       # Hello World API
│   └── 📁 recursos/                       # Recursos adicionales
│
├── 📁 semana-02/                          # ⚡ FastAPI Fundamentals
│   ├── 📁 teoria/                         # Pydantic, Type hints
│   ├── 📁 practica/                       # CRUD básico
│   ├── 📁 ejercicios/                     # Validaciones
│   ├── 📁 proyecto/                       # Task Manager API
│   └── 📁 recursos/                       # Referencias FastAPI
│
├── 📁 semana-03/                          # 🗄️ Base de Datos y ORM
│   ├── 📁 teoria/                         # SQLAlchemy, Alembic
│   ├── 📁 practica/                       # Modelos y relaciones
│   ├── 📁 ejercicios/                     # Queries complejas
│   ├── 📁 proyecto/                       # Task Manager con BD
│   └── 📁 recursos/                       # SQL resources
│
├── 📁 semana-04/                          # 🐳 Docker y Containerización
│   ├── 📁 teoria/                         # Docker concepts
│   ├── 📁 practica/                       # Dockerfile creation
│   ├── 📁 ejercicios/                     # Docker Compose
│   ├── 📁 proyecto/                       # Containerized app
│   └── 📁 recursos/                       # Docker references
│
├── 📁 semana-05/                          # 🔒 Autenticación y Autorización
│   ├── 📁 teoria/                         # JWT, OAuth2
│   ├── 📁 practica/                       # Auth implementation
│   ├── 📁 ejercicios/                     # Security patterns
│   ├── 📁 proyecto/                       # Secure Task Manager
│   └── 📁 recursos/                       # Security docs
│
├── 📁 semana-06/                          # 🧪 Testing y Quality Assurance
│   ├── 📁 teoria/                         # Testing strategies
│   ├── 📁 practica/                       # pytest, coverage
│   ├── 📁 ejercicios/                     # Test cases
│   ├── 📁 proyecto/                       # Complete test suite
│   └── 📁 recursos/                       # Testing resources
│
├── 📁 semana-07/                          # 📊 Optimización y Performance
│   ├── 📁 teoria/                         # Performance concepts
│   ├── 📁 practica/                       # Caching, monitoring
│   ├── 📁 ejercicios/                     # Optimization tasks
│   ├── 📁 proyecto/                       # Optimized API
│   └── 📁 recursos/                       # Performance tools
│
├── 📁 semana-08/                          # ⚛️ Frontend Integration
│   ├── 📁 teoria/                         # React, CORS
│   ├── 📁 practica/                       # Frontend setup
│   ├── 📁 ejercicios/                     # Integration tasks
│   ├── 📁 proyecto/                       # Full-stack app
│   └── 📁 recursos/                       # Frontend resources
│
├── 📁 semana-09/                          # 🏗️ Microservices Architecture
│   ├── 📁 teoria/                         # Microservices patterns
│   ├── 📁 practica/                       # Service separation
│   ├── 📁 ejercicios/                     # Communication patterns
│   ├── 📁 proyecto/                       # Microservices system
│   └── 📁 recursos/                       # Architecture docs
│
├── 📁 semana-10/                          # 🚀 DevOps y CI/CD
│   ├── 📁 teoria/                         # DevOps practices
│   ├── 📁 practica/                       # Pipeline setup
│   ├── 📁 ejercicios/                     # Automation tasks
│   ├── 📁 proyecto/                       # Complete pipeline
│   └── 📁 recursos/                       # DevOps tools
│
├── 📁 semana-11/                          # 🎯 Proyecto Final - Desarrollo
│   ├── 📁 teoria/                         # Integration concepts
│   ├── 📁 practica/                       # Project development
│   ├── 📁 ejercicios/                     # Advanced features
│   ├── 📁 proyecto/                       # E-Commerce Platform
│   └── 📁 recursos/                       # Final project resources
│
├── 📁 semana-12/                          # 🏆 Proyecto Final - Presentación
│   ├── 📁 teoria/                         # Presentation skills
│   ├── 📁 practica/                       # Demo preparation
│   ├── 📁 ejercicios/                     # Final touches
│   ├── 📁 proyecto/                       # Complete deliverable
│   └── 📁 recursos/                       # Presentation resources
│
└── 📁 proyecto-final/                     # 🌟 E-Commerce API Platform
    ├── 📁 backend/                        # FastAPI microservices
    ├── 📁 frontend/                       # React application
    ├── 📁 docs/                           # Project documentation
    ├── 📁 deployment/                     # Deployment configs
    └── 📁 tests/                          # Comprehensive testing
```

## 🎯 Convenciones de Estructura

### 📚 Documentación (`_docs/`)

- **NUNCA** guardar documentación fuera de esta carpeta (excepto README.md)
- Estructura jerárquica por categorías
- Documentación en español, código en inglés

### 🔧 Scripts (`_scripts/`)

- **NUNCA** guardar scripts fuera de esta carpeta
- Scripts ejecutables con documentación clara
- Nombres descriptivos en inglés

### 📅 Semanas (`semana-XX/`)

- Estructura consistente en todas las semanas
- Progresión lógica de dificultad
- Proyectos que construyen sobre conocimientos previos

### 🎓 Estructura por Semana

Cada semana sigue la misma organización:

```
semana-XX/
├── teoria/          # 📖 Conceptos fundamentales
├── practica/        # 💻 Ejercicios guiados
├── ejercicios/      # 🎯 Tareas individuales
├── proyecto/        # 🚀 Proyecto semanal
└── recursos/        # 📚 Referencias adicionales
```

### 🏗️ Proyecto Final

Integra todos los conocimientos del bootcamp:

```
proyecto-final/
├── backend/         # 🔧 APIs y microservicios
├── frontend/        # 🎨 Aplicación React
├── docs/           # 📄 Documentación técnica
├── deployment/     # 🚀 Configuración despliegue
└── tests/          # ✅ Suite completa de tests
```

## 📋 Archivos .gitkeep

Cada carpeta incluye un archivo `.gitkeep` que:

- **Garantiza trazabilidad** en Git
- **Documenta el propósito** de la carpeta
- **Proporciona contexto** sobre el contenido esperado
- **Mantiene estructura** visible en repositorio vacío

## 🎯 Beneficios de esta Estructura

### Para Aprendices

- **Navegación intuitiva** - Fácil encontrar recursos
- **Progresión clara** - Estructura que refleja el aprendizaje
- **Recursos organizados** - Todo en su lugar apropiado

### Para Instructores

- **Mantenimiento sencillo** - Estructura predecible
- **Escalabilidad** - Fácil agregar nuevo contenido
- **Reutilización** - Recursos compartidos accesibles

### Para Contributors

- **Convenciones claras** - Dónde colocar qué tipo de contenido
- **Trazabilidad completa** - Historial visible en Git
- **Colaboración eficiente** - Estructura conocida por todos

## 🔄 Evolución de la Estructura

Esta estructura puede evolucionar basada en:

- Feedback de aprendices
- Necesidades emergentes del curriculum
- Mejores prácticas identificadas
- Contribuciones de la comunidad

Cualquier cambio será documentado en el CHANGELOG.md y comunicado a todos los participantes.
