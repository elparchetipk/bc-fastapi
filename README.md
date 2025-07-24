# Bootcamp bc-fastapi

![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## 📋 Descripción del Proyecto

Bootcamp intensivo de desarrollo de **APIs REST con FastAPI** dirigido a aprendices de tecnólogo en Desarrollo de Software (III trimestre). El programa tiene una duración de **12 semanas** con sesiones semanales de 6 horas, enfocado en la aplicación de mejores prácticas y desarrollo de software de **calidad total**.

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
├── 📄 README.md                    # Documentación principal
├── 📄 .copilot-instructions.md     # Instrucciones para GitHub Copilot
├── 📄 .gitignore                   # Archivos ignorados por Git
├── 📄 plan-trabajo-detallado.md    # Plan semanal del bootcamp
├── 📁 _docs/                       # 📚 Documentación del proyecto
├── 📁 _scripts/                    # 🔧 Scripts de automatización
├── 📁 semana-01/                   # Código y ejercicios semana 1
├── 📁 semana-02/                   # Código y ejercicios semana 2
├── ...                             # Semanas 3-11
└── 📁 proyecto-final/              # Proyecto integrador final
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
- Node.js 18 o superior
- Docker y Docker Compose
- Git
- Editor de código (recomendado: VS Code)

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

### Primer Proyecto

```bash
# Navegar a la primera semana
cd semana-01

# Seguir las instrucciones específicas de cada semana
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

Toda la documentación detallada se encuentra en la carpeta `_docs/`:

- **Guías de instalación y configuración**
- **Tutoriales paso a paso**
- **Referencias técnicas**
- **Mejores prácticas específicas**
- **Solución de problemas comunes**

## 🤝 Contribución

### Convenciones de Código

- **Nomenclatura**: Obligatorio en inglés para todo elemento técnico
- **Python**: snake_case para funciones y variables
- **JavaScript/React**: camelCase
- **Documentación**: Español para explicaciones, inglés para código

### Flujo de Trabajo Git

```bash
# Crear rama para nueva característica
git checkout -b feature/nombre-descriptivo

# Commits descriptivos en presente
git commit -m "Add user authentication endpoint"

# Push y pull request
git push origin feature/nombre-descriptivo
```

## 📞 Soporte

- **Instructor**: [Información de contacto]
- **Repositorio**: [URL del repositorio]
- **Documentación**: `/bc-fastapi/_docs/`
- **Issues**: Usar GitHub Issues para reportar problemas

## 📄 Licencia

Este proyecto es parte del programa educativo de [Institución] y está destinado únicamente para fines académicos.

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
