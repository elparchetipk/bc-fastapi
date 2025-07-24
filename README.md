# Bootcamp bc-fastapi

<div align="center">
  
![Bootcamp FastAPI Logo](./assets/logo-bootcamp-fastapi.png)

</div>

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## 📋 Descripción del Proyecto

Bootcamp intensivo de desarrollo de **APIs REST con FastAPI** dirigido a aprendices de Tecnólogo en Desarrollo de Software (III trimestre). El programa tiene una duración de **12 semanas** con sesiones semanales de 6 horas, enfocado en la aplicación de mejores prácticas y desarrollo de software de **calidad total**.

### 🎯 Objetivos del Bootcamp

- Desarrollar APIs REST robustas y escalables con FastAPI
- Implementar arquitectura limpia y patrones de microservicios
- Aplicar mejores prácticas de desarrollo profesional
- Dominar el stack tecnológico moderno para backend
- Crear aplicaciones con estándares de calidad industrial

## 🛠️ Stack Tecnológico

### Backend Core

- **FastAPI** - Framework principal para APIs REST
- **Python 3.11+** - Lenguaje de programación
- **Pydantic** - Validación y serialización de datos
- **SQLAlchemy** - ORM para base de datos
- **Alembic** - Migraciones de base de datos

### Base de Datos

- **PostgreSQL** - Base de datos principal
- **SQLite** - Base de datos para desarrollo/testing

### Containerización y DevOps

- **Docker** - Containerización de aplicaciones
- **Docker Compose** - Orquestación de servicios
- **GitHub Actions** - CI/CD pipelines

### Frontend (cuando se requiera)

- **React 18** - Biblioteca de interfaces de usuario
- **Vite** - Build tool y dev server
- **Tailwind CSS** - Framework de CSS utility-first
- **pnpm** - Gestor de paquetes

### Herramientas de Desarrollo

- **Postman** - Testing de APIs
- **Swagger/OpenAPI** - Documentación automática
- **SonarQube** - Análisis de calidad de código
- **pytest** - Framework de testing

## 📁 Estructura del Proyecto

```
bc-fastapi/
├── 📄 README.md                          # Documentación principal
├── 📄 LICENSE                            # Licencia MIT del proyecto
├── 📄 CHANGELOG.md                       # Registro de cambios
├── 📄 CODE_OF_CONDUCT.md                 # Código de conducta
├── 📄 CONTRIBUTING.md                    # Guía de contribución
├── 📄 ESTRUCTURA.md                      # Documentación de estructura
├── 📄 .gitignore                         # Archivos ignorados por Git
├── 📄 plan-trabajo-detallado.md          # Plan semanal detallado
├── 📁 assets/                            # 🎨 Recursos gráficos
│   ├── 📄 logo-bootcamp-fastapi.svg      # Logo principal (SVG)
│   ├── 📄 logo-bootcamp-fastapi.png      # Logo principal (PNG)
│   ├── 📄 logo-bootcamp-fastapi-compact.svg # Logo compacto (SVG)
│   ├── 📄 logo-bootcamp-fastapi-compact.png # Logo compacto (PNG)
│   └── 📄 logo-preview.html              # Preview de logos
├── 📁 .github/                           # 🔧 Configuración GitHub
│   ├── 📄 .copilot-instructions.md       # Instrucciones para Copilot
│   ├── 📄 PULL_REQUEST_TEMPLATE.md       # Template para PRs
│   └── 📁 ISSUE_TEMPLATE/                # Templates para issues
│       ├── 📄 bug_report.md              # Reporte de bugs
│       ├── 📄 feature_request.md         # Solicitud de features
│       ├── 📄 question.md                # Preguntas
│       └── 📄 config.yml                 # Configuración templates
├── 📁 _docs/                             # 📚 Documentación del proyecto
│   ├── 📁 setup/                         # Configuración inicial
│   │   ├── 📄 environment-setup.md       # Setup del entorno
│   │   ├── 📄 git-github-strategy.md     # Estrategia Git/GitHub
│   │   ├── 📄 entrega-guidelines.md      # Guías de entrega
│   │   └── 📄 automation-roadmap.md      # Roadmap de automatización
│   ├── 📁 guides/                        # Guías técnicas avanzadas
│   │   ├── 📄 security-best-practices.md # Mejores prácticas seguridad
│   │   ├── 📄 performance-optimization.md# Optimización performance
│   │   ├── 📄 api-design-standards.md    # Estándares diseño API
│   │   ├── 📄 deployment-devops.md       # Deployment y DevOps
│   │   ├── 📄 architecture-patterns.md   # Patrones arquitectura
│   │   ├── 📄 database-modeling.md       # Modelado de BD
│   │   └── 📄 rubricas-evaluacion.md     # Rúbricas evaluación
│   ├── 📁 api/                           # Documentación API
│   ├── 📁 architecture/                  # Diagramas arquitectura
│   └── 📁 troubleshooting/               # Solución problemas
├── 📁 _scripts/                          # 🔧 Scripts de automatización
│   ├── 📁 setup/                         # Scripts configuración
│   ├── 📁 testing/                       # Scripts testing
│   ├── 📁 deployment/                    # Scripts deployment
│   └── 📁 utilities/                     # Utilidades generales
│       └── 📄 generate_week_gitkeeps.sh  # Generador .gitkeep
├── 📁 recursos-compartidos/              # 🗂️ Recursos compartidos
│   ├── 📁 configs/                       # Configuraciones
│   ├── 📁 templates/                     # Plantillas código
│   ├── 📁 databases/                     # Scripts BD
│   └── 📁 tools/                         # Herramientas
├── 📁 semana-01/ ⭐                      # 🎯 Semana 1: Fundamentos
│   ├── 📄 README.md                      # Objetivos y actividades
│   ├── � RUBRICA_SEMANA_1.md           # Rúbrica evaluación
│   ├── �📁 teoria/                        # Conceptos fundamentales
│   │   └── 📄 01-conceptos-fundamentales.md
│   ├── 📁 practica/                      # Tutoriales prácticos
│   │   ├── 📄 01-environment-setup.md    # Setup entorno desarrollo
│   │   ├── 📄 02-hello-world-api.md      # Primera API FastAPI
│   │   ├── 📄 03-python-fundamentals.md  # Fundamentos Python
│   │   ├── 📄 04-fastapi-basics.md       # Básicos FastAPI
│   │   └── 📁 04-fastapi-basics/         # Proyecto práctico
│   ├── 📁 ejercicios/                    # Ejercicios propuestos
│   ├── 📁 proyecto/                      # Especificaciones proyecto
│   └── 📁 recursos/                      # Referencias y diagramas
├── 📁 semana-02/                         # 🎯 Semana 2-12
├── 📁 semana-03/                         # (Estructura similar)
├── ...                                   # Semanas 4-11
├── 📁 semana-12/                         # 🎯 Semana 12: Cierre
└── 📁 proyecto-final/                    # 🏆 Proyecto integrador
    ├── 📁 backend/                       # Backend FastAPI
    ├── 📁 frontend/                      # Frontend React
    ├── 📁 deployment/                    # Configuración deploy
    ├── 📁 docs/                          # Documentación proyecto
    └── 📁 tests/                         # Testing integral
```

### 📂 Estructura de Cada Semana

Cada directorio `semana-XX/` sigue la misma estructura organizacional:

```
semana-XX/
├── 📄 README.md                 # Objetivos y actividades semanales
├── 📄 RUBRICA_SEMANA_X.md      # Rúbrica de evaluación específica
├── 📁 teoria/                  # 📖 Conceptos teóricos
├── 📁 practica/                # 💻 Tutoriales paso a paso
├── 📁 ejercicios/              # 🏋️ Ejercicios propuestos
├── 📁 proyecto/                # 🎯 Especificaciones proyecto semanal
└── 📁 recursos/                # 📚 Referencias y materiales adicionales
```

## 🎓 Metodología de Enseñanza

### Principios Fundamentales

- **Calidad Total**: No hay "errores menores", todo problema es un PROBLEMA
- **Nomenclatura en Inglés**: Obligatorio para todo código técnico
- **Clean Architecture**: Separación clara de responsabilidades
- **Best Practices**: Aplicación constante de mejores prácticas

### Formato Bootcamp

- **12 sesiones semanales** de 6 horas cada una
- **Proyectos progresivos** que construyen sobre conocimientos previos
- **Evaluación continua** con feedback detallado
- **Proyecto final integrador** que demuestra dominio completo

### Criterios de Evaluación

- **Técnica (70%)**: Funcionamiento, calidad, best practices
- **Profesional (20%)**: Nomenclatura, documentación, Git workflow
- **Actitudinal (10%)**: Participación, growth mindset, colaboración

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.11 o superior
- Node.js 18 o superior (para frontend en semanas posteriores)
- Docker y Docker Compose
- Git
- Editor de código (recomendado: VS Code con extensiones Python y Docker)

### Configuración del Entorno

```bash
# Clonar el repositorio
git clone <repository-url>
cd bc-fastapi

# Crear entorno virtual de Python
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias base
pip install fastapi uvicorn

# Verificar instalación
python -c "import fastapi; print('FastAPI:', fastapi.__version__)"
```

### Comenzar con Semana 1

```bash
# Navegar a la primera semana
cd semana-01

# Revisar objetivos y estructura
cat README.md

# Seguir tutoriales en orden:
# 1. practica/01-environment-setup.md
# 2. practica/02-hello-world-api.md
# 3. practica/03-python-fundamentals.md
# 4. practica/04-fastapi-basics.md
```

### Verificar Configuración

```bash
# Desde semana-01/practica/04-fastapi-basics/
cd app
pip install -r requirements.txt
uvicorn main:app --reload

# Verificar en: http://localhost:8000/docs
```

## 📋 Cronograma del Bootcamp

| Semana | Tema Principal                | Tecnologías                         |
| ------ | ----------------------------- | ----------------------------------- |
| 1      | Fundamentos y Configuración   | Python, FastAPI, Git, Docker        |
| 2      | FastAPI Fundamentals          | Pydantic, Swagger, Validation       |
| 3      | Base de Datos y ORM           | SQLAlchemy, Alembic, PostgreSQL     |
| 4      | Containerización              | Docker, Docker Compose              |
| 5      | Autenticación y Seguridad     | JWT, OAuth2, Security               |
| 6      | Testing y Calidad             | pytest, SonarQube, Coverage         |
| 7      | Optimización y Performance    | Caching, Monitoring, Redis          |
| 8      | Frontend Integration          | React, Vite, CORS                   |
| 9      | Microservicios                | Architecture, Service Communication |
| 10     | DevOps y CI/CD                | GitHub Actions, Deployment          |
| 11     | Proyecto Final - Desarrollo   | Integración completa                |
| 12     | Proyecto Final - Presentación | Evaluación y cierre                 |

## 📚 Documentación Adicional

La documentación completa está organizada en `_docs/` con las siguientes secciones:

### 🚀 Setup y Configuración (`_docs/setup/`)

- **`environment-setup.md`** - Configuración completa del entorno de desarrollo
- **`git-github-strategy.md`** - Estrategias Git/GitHub y flujos de trabajo
- **`entrega-guidelines.md`** - Guías para entregas y evaluaciones
- **`automation-roadmap.md`** - Roadmap de automatización y CI/CD

### 📖 Guías Técnicas Avanzadas (`_docs/guides/`)

- **`security-best-practices.md`** - Mejores prácticas de seguridad
- **`performance-optimization.md`** - Optimización de rendimiento
- **`api-design-standards.md`** - Estándares de diseño de APIs
- **`deployment-devops.md`** - Deployment y prácticas DevOps
- **`architecture-patterns.md`** - Patrones de arquitectura
- **`database-modeling.md`** - Modelado de bases de datos
- **`rubricas-evaluacion.md`** - Sistema de rúbricas y evaluación

### 📊 Otras Secciones

- **`_docs/api/`** - Documentación específica de APIs
- **`_docs/architecture/`** - Diagramas y documentación arquitectural
- **`_docs/troubleshooting/`** - Solución de problemas comunes

## 📋 Archivos Principales del Proyecto

### 🔧 Configuración y Gestión

- **`CHANGELOG.md`** - Registro detallado de cambios del proyecto
- **`CODE_OF_CONDUCT.md`** - Código de conducta para colaboradores
- **`CONTRIBUTING.md`** - Guía completa de contribución
- **`ESTRUCTURA.md`** - Documentación detallada de la estructura
- **`plan-trabajo-detallado.md`** - Plan semanal completo del bootcamp

### ⚙️ GitHub y Colaboración

- **`.github/.copilot-instructions.md`** - Instrucciones para GitHub Copilot
- **`.github/PULL_REQUEST_TEMPLATE.md`** - Template para Pull Requests
- **`.github/ISSUE_TEMPLATE/`** - Templates para issues (bugs, features, preguntas)

### 🛠️ Scripts y Automatización

- **`_scripts/utilities/generate_week_gitkeeps.sh`** - Generador automático de .gitkeep
- **`_scripts/setup/`** - Scripts de configuración inicial
- **`_scripts/testing/`** - Scripts para testing automatizado
- **`_scripts/deployment/`** - Scripts de deployment

### 🎯 Estado Actual: Semana 1 Completada

La **Semana 1** está completamente implementada con:

- ✅ **Objetivos y rúbrica definidos** (`README.md`, `RUBRICA_SEMANA_1.md`)
- ✅ **Tutoriales prácticos completos** (4 tutoriales paso a paso)
- ✅ **Teoría fundamental** (conceptos base documentados)
- ✅ **Proyecto práctico funcional** (API Hello World con estructura profesional)
- ✅ **Diagramas visuales** (SVG para reforzar conceptos)
- ✅ **Ejercicios propuestos** y especificaciones proyecto
- ✅ **Referencias y recursos** organizados

## 🤝 Contribución

### Filosofía: "Manual Primero, Luego Altamente Productivo"

- **Primero**: Entender y hacer manualmente cada proceso
- **Segundo**: Automatizar solo cuando se domina el proceso manual
- **Siempre**: Mantener calidad total en cada entrega

### Convenciones de Código

- **Nomenclatura**: Obligatorio en inglés para todo elemento técnico
- **Python**: snake_case para funciones y variables, PascalCase para clases
- **JavaScript/React**: camelCase para variables, PascalCase para componentes
- **Documentación**: Español para explicaciones, inglés para código
- **Commits**: Mensajes descriptivos en inglés, formato present tense

### Flujo de Trabajo Git

```bash
# Crear rama para nueva característica
git checkout -b feature/descriptive-name

# Commits atómicos y descriptivos
git commit -m "Add user authentication endpoint"
git commit -m "Implement JWT token validation"

# Push y pull request
git push origin feature/descriptive-name
```

### Entrega de Proyectos

- **📍 GitHub Only**: Todas las entregas deben ser via GitHub
- **🔍 CI/CD**: Usar GitHub Actions desde día 1
- **📋 PR Templates**: Usar templates para Pull Requests
- **✅ Reviews**: Code review obligatorio para merge
- **📊 Quality Gates**: SonarQube y testing antes de deploy

Para más detalles, ver `_docs/setup/git-github-strategy.md` y `CONTRIBUTING.md`.

## 📞 Soporte y Recursos

### 📋 Documentación Principal

- **`README.md`** - Este archivo (información general)
- **`ESTRUCTURA.md`** - Documentación detallada de estructura
- **`plan-trabajo-detallado.md`** - Plan completo semana a semana
- **`CONTRIBUTING.md`** - Guía completa de contribución

### 🔧 Setup y Configuración

- **`_docs/setup/environment-setup.md`** - Configuración entorno desarrollo
- **`_docs/setup/git-github-strategy.md`** - Estrategias Git/GitHub
- **`_docs/setup/entrega-guidelines.md`** - Guías de entrega

### 📖 Guías Técnicas

- **`_docs/guides/`** - Guías avanzadas (seguridad, performance, arquitectura)
- **`semana-01/README.md`** - Ejemplo de estructura semanal

### 🐛 Reportar Problemas

- **GitHub Issues**: Usar templates en `.github/ISSUE_TEMPLATE/`
- **Bug Reports**: `bug_report.md`
- **Feature Requests**: `feature_request.md`
- **Preguntas**: `question.md`

### 📞 Contacto

- **Instructor**: [Información de contacto]
- **Repositorio**: [URL del repositorio]
- **Documentación**: `/bc-fastapi/_docs/`

## 📄 Licencia

Este proyecto es parte del programa educativo del Centro de Gestión de Mercados Logística y Tecnologías de la Información CGMLTI de la Regional Distrito Capital del Servicio Nacional de Aprendizaje SENA - Colombia y está destinado únicamente para fines académicos.

---

## 🏆 Objetivos de Aprendizaje

Al completar este bootcamp, los aprendices serán capaces de:

✅ **Desarrollar APIs REST** profesionales con FastAPI  
✅ **Implementar arquitectura limpia** y patrones de diseño  
✅ **Gestionar bases de datos** con ORMs y migraciones  
✅ **Containerizar aplicaciones** con Docker  
✅ **Aplicar testing** comprehensivo y análisis de calidad  
✅ **Integrar frontend** con React y tecnologías modernas  
✅ **Desplegar aplicaciones** con pipelines CI/CD  
✅ **Trabajar en equipo** con herramientas profesionales

---

<div align="center">

**¡Bienvenidos al Bootcamp bc-fastapi!**  
_Donde la calidad es total y la excelencia es el estándar._

</div>
