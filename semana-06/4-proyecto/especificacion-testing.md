# Proyecto Final: API con Testing Completo

⏰ **Tiempo:** 120 minutos  
🎯 **Objetivo:** Desarrollar una API completa con suite de testing profesional  
📚 **Nivel:** Integración de conocimientos de Semanas 1-6

## 🎯 Descripción del Proyecto

Desarrollarás una **API de gestión de tareas avanzada** que incluye autenticación, CRUD completo, y una suite de testing profesional que demuestre todas las técnicas aprendidas en el bootcamp.

### **Características Principales**

1. **Sistema de autenticación completo** (JWT, registro, login)
2. **CRUD avanzado de tareas** con categorías y prioridades
3. **Sistema de usuarios** con perfiles y roles
4. **Testing completo** con coverage >85%
5. **Documentación automatizada** y deployment-ready

---

## 📋 Requisitos Técnicos

### **Backend (FastAPI)**

- ✅ **Autenticación JWT** con refresh tokens
- ✅ **Base de datos SQLAlchemy** con migraciones
- ✅ **Validación Pydantic** completa
- ✅ **Manejo de errores** profesional
- ✅ **Logging** estructurado
- ✅ **Documentación OpenAPI** automática

### **Testing**

- ✅ **pytest** con fixtures profesionales
- ✅ **Coverage >85%** en módulos críticos
- ✅ **Tests de integración** E2E
- ✅ **Tests de autenticación** completos
- ✅ **Tests de autorización** y seguridad
- ✅ **CI/CD básico** con GitHub Actions

### **Calidad de Código**

- ✅ **Linting** con flake8/black
- ✅ **Type hints** completos
- ✅ **Documentación** de API
- ✅ **Estructura** profesional
- ✅ **Environment variables** para configuración

---

## 🏗️ Arquitectura del Proyecto

### **Estructura de Carpetas**

```text
task-api/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py              # Configuración
│   ├── database.py            # Conexión DB
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py     # JWT utilities
│   │   ├── password.py        # Password hashing
│   │   └── dependencies.py    # Auth dependencies
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py           # User model
│   │   ├── task.py           # Task model
│   │   └── category.py       # Category model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py           # User Pydantic models
│   │   ├── task.py           # Task Pydantic models
│   │   └── auth.py           # Auth Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py           # Auth endpoints
│   │   ├── users.py          # User endpoints
│   │   ├── tasks.py          # Task endpoints
│   │   └── categories.py     # Category endpoints
│   └── services/
│       ├── __init__.py
│       ├── user_service.py   # User business logic
│       ├── task_service.py   # Task business logic
│       └── auth_service.py   # Auth business logic
├── tests/
│   ├── conftest.py           # Pytest configuration
│   ├── fixtures/
│   │   ├── auth_fixtures.py
│   │   ├── user_fixtures.py
│   │   └── task_fixtures.py
│   ├── unit/
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   ├── test_tasks.py
│   │   └── test_services.py
│   ├── integration/
│   │   ├── test_auth_flow.py
│   │   ├── test_task_workflow.py
│   │   └── test_user_isolation.py
│   └── helpers/
│       ├── auth_helpers.py
│       └── test_helpers.py
├── migrations/               # Alembic migrations
├── scripts/
│   ├── run_tests.sh
│   ├── setup_dev.py
│   └── deploy.sh
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── .coveragerc
├── .env.example
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 📊 Modelos de Datos

### **User Model**

```python
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    categories = relationship("Category", back_populates="user", cascade="all, delete-orphan")
```

### **Task Model**

```python
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)
    priority = Column(Enum("low", "medium", "high", name="priority_enum"), default="medium")
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    # Relationships
    user = relationship("User", back_populates="tasks")
    category = relationship("Category", back_populates="tasks")
```

### **Category Model**

```python
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    color = Column(String(7), default="#3498db")  # Hex color
    created_at = Column(DateTime, default=datetime.utcnow)

    # Foreign Keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    user = relationship("User", back_populates="categories")
    tasks = relationship("Task", back_populates="category")

    # Constraints
    __table_args__ = (UniqueConstraint('user_id', 'name', name='unique_user_category'),)
```

---

## 🔐 Endpoints Principales

### **Authentication (`/auth`)**

| Método | Endpoint                | Descripción                | Auth Required |
| ------ | ----------------------- | -------------------------- | ------------- |
| POST   | `/auth/register`        | Registro de usuario        | ❌            |
| POST   | `/auth/login`           | Login con email/password   | ❌            |
| POST   | `/auth/refresh`         | Refresh token              | ✅            |
| POST   | `/auth/logout`          | Logout (invalidar token)   | ✅            |
| POST   | `/auth/forgot-password` | Recuperación de contraseña | ❌            |

### **Users (`/users`)**

| Método | Endpoint           | Descripción               | Auth Required |
| ------ | ------------------ | ------------------------- | ------------- |
| GET    | `/users/me`        | Perfil del usuario actual | ✅            |
| PUT    | `/users/me`        | Actualizar perfil         | ✅            |
| DELETE | `/users/me`        | Eliminar cuenta           | ✅            |
| POST   | `/users/me/avatar` | Subir avatar              | ✅            |
| GET    | `/users`           | Listar usuarios (admin)   | ✅ Admin      |

### **Tasks (`/tasks`)**

| Método | Endpoint               | Descripción               | Auth Required |
| ------ | ---------------------- | ------------------------- | ------------- |
| GET    | `/tasks`               | Listar tareas del usuario | ✅            |
| POST   | `/tasks`               | Crear nueva tarea         | ✅            |
| GET    | `/tasks/{id}`          | Obtener tarea por ID      | ✅            |
| PUT    | `/tasks/{id}`          | Actualizar tarea          | ✅            |
| DELETE | `/tasks/{id}`          | Eliminar tarea            | ✅            |
| GET    | `/tasks/search`        | Buscar tareas             | ✅            |
| PATCH  | `/tasks/{id}/complete` | Marcar como completada    | ✅            |

### **Categories (`/categories`)**

| Método | Endpoint                 | Descripción                   | Auth Required |
| ------ | ------------------------ | ----------------------------- | ------------- |
| GET    | `/categories`            | Listar categorías del usuario | ✅            |
| POST   | `/categories`            | Crear nueva categoría         | ✅            |
| GET    | `/categories/{id}`       | Obtener categoría por ID      | ✅            |
| PUT    | `/categories/{id}`       | Actualizar categoría          | ✅            |
| DELETE | `/categories/{id}`       | Eliminar categoría            | ✅            |
| GET    | `/categories/{id}/tasks` | Tareas de una categoría       | ✅            |

---

## 🧪 Especificaciones de Testing

### **Cobertura Requerida**

| Módulo      | Coverage Mínimo | Descripción           |
| ----------- | --------------- | --------------------- |
| `auth/`     | 90%             | Autenticación crítica |
| `models/`   | 85%             | Modelos de datos      |
| `routers/`  | 85%             | Endpoints API         |
| `services/` | 90%             | Lógica de negocio     |
| **Total**   | **85%**         | Coverage general      |

### **Types de Tests Requeridos**

1. **Unit Tests** (60% del tiempo)

   - Tests de servicios individuales
   - Tests de funciones utilitarias
   - Tests de validaciones Pydantic
   - Tests de modelos SQLAlchemy

2. **Integration Tests** (30% del tiempo)

   - Tests de workflows completos
   - Tests de endpoints E2E
   - Tests de autenticación completa
   - Tests de aislamiento entre usuarios

3. **Edge Cases Tests** (10% del tiempo)
   - Tests de manejo de errores
   - Tests de límites del sistema
   - Tests de casos maliciosos
   - Tests de performance básica

### **Fixtures Requeridas**

```python
# En conftest.py
@pytest.fixture
def db():
    """Base de datos de testing."""
    pass

@pytest.fixture
def client(db):
    """Cliente FastAPI con DB de testing."""
    pass

@pytest.fixture
def test_user(db):
    """Usuario básico para testing."""
    pass

@pytest.fixture
def admin_user(db):
    """Usuario administrador."""
    pass

@pytest.fixture
def auth_headers(test_user):
    """Headers de autenticación."""
    pass

@pytest.fixture
def task_factory(db):
    """Factory para crear tareas."""
    pass

@pytest.fixture
def category_factory(db):
    """Factory para crear categorías."""
    pass
```

---

## 📝 Criterios de Evaluación

### **Funcionalidad (40%)**

| Criterio           | Excelente (4)              | Bueno (3)                 | Suficiente (2)              | Insuficiente (1) |
| ------------------ | -------------------------- | ------------------------- | --------------------------- | ---------------- |
| **Autenticación**  | JWT completo con refresh   | JWT básico funcional      | Login/registro básico       | Auth incompleto  |
| **CRUD Endpoints** | Todos funcionando + extras | CRUD básico completo      | CRUD parcialmente funcional | CRUD muy básico  |
| **Validaciones**   | Validaciones robustas      | Validaciones básicas      | Algunas validaciones        | Sin validaciones |
| **Manejo Errores** | Manejo profesional         | Errores básicos manejados | Manejo mínimo               | Sin manejo       |

### **Testing (35%)**

| Criterio           | Excelente (4)             | Bueno (3)          | Suficiente (2)      | Insuficiente (1) |
| ------------------ | ------------------------- | ------------------ | ------------------- | ---------------- |
| **Coverage**       | >90% en críticos          | 85-90% general     | 80-85% básico       | <80%             |
| **Tipos de Tests** | Unit + Integration + Edge | Unit + Integration | Solo Unit tests     | Tests básicos    |
| **Organización**   | Estructura profesional    | Buena organización | Organización básica | Desorganizado    |
| **Calidad Tests**  | Tests robustos y claros   | Tests funcionales  | Tests básicos       | Tests pobres     |

### **Calidad Código (25%)**

| Criterio          | Excelente (4)            | Bueno (3)        | Suficiente (2)       | Insuficiente (1)   |
| ----------------- | ------------------------ | ---------------- | -------------------- | ------------------ |
| **Estructura**    | Arquitectura profesional | Estructura clara | Estructura básica    | Mal estructurado   |
| **Documentación** | Docs completas + OpenAPI | Docs básicas     | Docs mínimas         | Sin documentación  |
| **Code Style**    | Linting + formatting     | Código limpio    | Estilo inconsistente | Código desordenado |
| **Type Hints**    | Type hints completos     | Parciales        | Básicos              | Sin type hints     |

---

## 🚀 Entregables

### **1. Repositorio GitHub**

- **Código fuente completo** con estructura profesional
- **README.md detallado** con instrucciones de setup
- **Tests implementados** con coverage report
- **CI/CD configurado** con GitHub Actions
- **Documentation** de API automática

### **2. Documentos**

- **`TESTING.md`** - Documentación de estrategia de testing
- **`API_DOCS.md`** - Documentación de endpoints
- **`SETUP.md`** - Instrucciones de desarrollo
- **`DEPLOYMENT.md`** - Guía de deployment

### **3. Demos**

- **Video/screenshots** de API funcionando
- **Reporte de coverage** HTML
- **Postman/Thunder collection** para testing manual
- **Docker setup** funcional (bonus)

---

## 💡 Tips para el Éxito

### **Planificación (15 min)**

1. **Revisa el scope completo** antes de empezar
2. **Prioriza funcionalidad core** primero
3. **Planifica tiempo para testing** (30% del proyecto)
4. **Deja buffer para debugging** y pulimiento

### **Desarrollo (60 min)**

1. **Estructura base** - modelos, auth, endpoints básicos
2. **Testing setup** - conftest.py, fixtures básicas
3. **CRUD completo** - un módulo a la vez
4. **Tests por módulo** - testa mientras desarrollas

### **Testing (30 min)**

1. **Tests de auth** primero (críticos)
2. **Tests de CRUD** por endpoint
3. **Tests de integración** para workflows
4. **Coverage check** y gaps de testing

### **Pulimiento (15 min)**

1. **Documentation** - README, docstrings
2. **Code cleanup** - linting, formatting
3. **Final testing** - suite completa
4. **Demo preparation** - screenshots, videos

---

## 🔧 Setup Técnico

### **Environment Setup**

```bash
# 1. Crear proyecto
mkdir task-api
cd task-api

# 2. Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install fastapi uvicorn sqlalchemy alembic python-jose[cryptography] passlib[bcrypt] python-multipart

# 4. Dev dependencies
pip install pytest pytest-cov pytest-asyncio httpx black flake8 mypy

# 5. Save requirements
pip freeze > requirements.txt
```

### **Database Setup**

```bash
# Initialize Alembic
alembic init migrations

# Create first migration
alembic revision --autogenerate -m "Initial tables"

# Apply migration
alembic upgrade head
```

### **Testing Setup**

```bash
# Run tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Only unit tests
pytest tests/unit/

# With verbose output
pytest -v --tb=short
```

---

## 🎯 Objetivos de Aprendizaje

Al completar este proyecto, habrás demostrado dominio de:

- ✅ **Desarrollo de APIs** profesionales con FastAPI
- ✅ **Testing automatizado** completo y robusto
- ✅ **Autenticación y seguridad** en APIs
- ✅ **Organización de código** y buenas prácticas
- ✅ **Coverage analysis** y calidad de código
- ✅ **Integration testing** y workflows E2E
- ✅ **Documentation** técnica y de usuario
- ✅ **Deployment** y entrega profesional

¡Este es tu proyecto capstone que demuestra todo lo aprendido en el bootcamp! 🏆
