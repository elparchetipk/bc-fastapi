# 🤝 Guía de Contribución - Bootcamp bc-fastapi

¡Bienvenido/a al bootcamp bc-fastapi! 🚀 Esta guía te ayudará a contribuir de manera efectiva al proyecto.

## 📋 Tabla de Contenidos

- [🎯 Filosofía del Proyecto](#-filosofía-del-proyecto)
- [🚀 Inicio Rápido](#-inicio-rápido)
- [📝 Tipos de Contribución](#-tipos-de-contribución)
- [🔧 Configuración del Entorno](#-configuración-del-entorno)
- [📋 Proceso de Contribución](#-proceso-de-contribución)
- [📏 Estándares de Código](#-estándares-de-código)
- [🧪 Testing](#-testing)
- [📚 Documentación](#-documentación)
- [🏆 Reconocimiento](#-reconocimiento)

## 🎯 Filosofía del Proyecto

### Principios Fundamentales

**Calidad Total** 💎

- No hay "errores menores" - Todo problema es un PROBLEMA
- Aplicamos siempre las mejores prácticas
- El código debe ser limpio, documentado y mantenible

**Nomenclatura Profesional** 🌐

- **OBLIGATORIO**: Todos los nombres técnicos en INGLÉS
- Python: `snake_case` para funciones y variables
- JavaScript/React: `camelCase`
- Clases: `PascalCase`

**Arquitectura Limpia** 🏗️

- Clean Architecture como preferencia
- Separación clara de responsabilidades
- Microservices cuando sea apropiado

## 🚀 Inicio Rápido

### Para Aprendices del Bootcamp

1. **Haz Fork del Repositorio** 🍴

   ```bash
   # Clona tu fork
   git clone https://github.com/TU-USUARIO/bc-fastapi.git
   cd bc-fastapi
   ```

2. **Configura el Repositorio Original** 🔗

   ```bash
   git remote add upstream https://github.com/REPO-ORIGINAL/bc-fastapi.git
   git fetch upstream
   ```

3. **Crea tu Entorno de Desarrollo** 🛠️

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

4. **¡Empieza a Contribuir!** 🎉

## 📝 Tipos de Contribución

### 🐛 Reportar Bugs

- Usa el template de [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md)
- Incluye pasos para reproducir
- Proporciona información del entorno
- Sugiere una posible solución si la tienes

### 💡 Sugerir Funcionalidades

- Usa el template de [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md)
- Explica el problema que resuelve
- Describe la solución propuesta
- Considera alternativas

### ❓ Hacer Preguntas

- Usa el template de [Pregunta/Duda](.github/ISSUE_TEMPLATE/question.md)
- Sé específico sobre tu duda
- Incluye contexto relevante
- Muestra qué has intentado

### 📚 Mejorar Documentación

- Corregir typos o errores
- Agregar ejemplos clarificadores
- Traducir comentarios técnicos
- Mejorar explicaciones existentes

### 💻 Contribuir Código

- Implementar nuevas funcionalidades
- Corregir bugs reportados
- Optimizar código existente
- Agregar tests

## 🔧 Configuración del Entorno

### Herramientas Requeridas

```bash
# Python 3.11+
python --version

# Node.js 18+ (para frontend)
node --version
npm --version

# Docker (para containerización)
docker --version
docker compose version

# Git
git --version
```

### Dependencias del Proyecto

```bash
# Backend
pip install fastapi uvicorn sqlalchemy alembic pytest

# Frontend (cuando aplique)
cd frontend/
npm install

# Herramientas de desarrollo
pip install black flake8 pytest-cov
```

### Variables de Entorno

```bash
# Copia el template de configuración
cp .env.template .env

# Edita las variables según tu entorno
# DATABASE_URL=postgresql://user:password@localhost/bootcamp_db
# SECRET_KEY=your-secret-key-here
```

## 📋 Proceso de Contribución

### 1. Preparación 🎯

```bash
# Sincroniza con el repositorio original
git checkout main
git pull upstream main

# Crea una nueva rama descriptiva
git checkout -b feature/user-authentication
# o
git checkout -b fix/database-connection-error
# o
git checkout -b docs/improve-setup-guide
```

### 2. Desarrollo 💻

**Commits Atómicos** ⚡

- Un commit = una funcionalidad/fix específico
- Mensajes en inglés, tiempo presente
- Formato: `Add user authentication endpoint`

**Nombres de Rama** 🌿

- `feature/` - nuevas funcionalidades
- `fix/` - corrección de bugs
- `docs/` - cambios en documentación
- `refactor/` - refactoring de código
- `test/` - agregar o mejorar tests

### 3. Testing 🧪

```bash
# Ejecuta todos los tests
pytest

# Tests con coverage
pytest --cov=src/ --cov-report=html

# Linting
flake8 src/
black src/ --check
```

### 4. Pull Request 📨

**Título Descriptivo**

```
[FEATURE] Add JWT authentication for user endpoints
[FIX] Resolve database connection timeout issue
[DOCS] Improve installation instructions for Windows
```

**Descripción Completa**

- ¿Qué cambia este PR?
- ¿Por qué es necesario?
- ¿Cómo se puede probar?
- Screenshots (si aplica)
- Links a issues relacionados

**Checklist**

- [ ] ✅ Tests pasan
- [ ] 📋 Documentación actualizada
- [ ] 🏷️ Commits tienen mensajes descriptivos
- [ ] 🌐 Nomenclatura en inglés
- [ ] 🧪 Coverage mantenido/mejorado

## 📏 Estándares de Código

### Python/FastAPI

```python
# ✅ CORRECTO
class UserService:
    """Service for handling user operations."""

    def create_user(self, user_data: dict) -> User:
        """Create a new user with validation."""
        return self._validate_and_save(user_data)

    def _validate_and_save(self, data: dict) -> User:
        # Private method implementation
        pass

# ❌ INCORRECTO
class ServicioUsuario:  # Español no permitido
    def crearUsuario(self, datos):  # Sin type hints
        pass
```

### JavaScript/React

```javascript
// ✅ CORRECTO
const UserDashboard = ({ userData }) => {
  const [isLoading, setIsLoading] = useState(false);

  const handleUserUpdate = async (updatedData) => {
    setIsLoading(true);
    // Implementation
  };

  return <div className="user-dashboard">...</div>;
};

// ❌ INCORRECTO
const panel_usuario = ({ datos_usuario }) => {
  // snake_case en JS
  // Implementation
};
```

### Documentación de APIs

```python
@app.post("/users/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    Create a new user account.

    Args:
        user: User creation data with email and password
        db: Database session dependency

    Returns:
        UserResponse: Created user information

    Raises:
        HTTPException: If email already exists (409)
        HTTPException: If validation fails (400)
    """
    # Implementation
```

## 🧪 Testing

### Estructura de Tests

```
tests/
├── unit/
│   ├── test_user_service.py
│   ├── test_auth_utils.py
│   └── test_database_models.py
├── integration/
│   ├── test_user_endpoints.py
│   └── test_database_operations.py
└── e2e/
    └── test_complete_user_flow.py
```

### Ejemplos de Tests

```python
# tests/unit/test_user_service.py
import pytest
from src.services.user_service import UserService

class TestUserService:
    """Test suite for UserService class."""

    @pytest.fixture
    def user_service(self):
        return UserService()

    def test_create_user_success(self, user_service):
        """Test successful user creation."""
        user_data = {
            "email": "test@example.com",
            "password": "secure_password123"
        }

        result = user_service.create_user(user_data)

        assert result.email == user_data["email"]
        assert result.id is not None

    def test_create_user_duplicate_email_raises_error(self, user_service):
        """Test that duplicate email raises appropriate error."""
        # Implementation
```

### Coverage Mínimo

- **Unit Tests**: 90%+ coverage
- **Integration Tests**: Endpoints críticos cubiertos
- **E2E Tests**: Flujos principales funcionando

## 📚 Documentación

### Estructura de Documentación

```
_docs/
├── setup/
│   ├── installation.md
│   ├── environment-setup.md
│   └── troubleshooting.md
├── guides/
│   ├── beginner-guide.md
│   ├── fastapi-fundamentals.md
│   └── best-practices.md
├── api/
│   ├── authentication.md
│   ├── user-endpoints.md
│   └── error-handling.md
└── architecture/
    ├── project-structure.md
    ├── database-design.md
    └── deployment.md
```

### Estándares de Documentación

**Markdown Formatting** 📝

- Usa headers jerárquicos (H1, H2, H3...)
- Code blocks con syntax highlighting
- Links descriptivos
- Listas ordenadas/desordenadas apropiadas

**Ejemplos Completos** 💡

- Incluye ejemplos de código funcionales
- Muestra tanto request como response
- Explica parámetros y return values
- Proporciona context de cuándo usar

**Idioma** 🌐

- Documentación de usuario: **Español**
- Comentarios en código: **Inglés**
- Nombres técnicos: **Inglés**

## 🏆 Reconocimiento

### Sistema de Badges 🏅

**🌟 First Contributor**

- Tu primera contribución aceptada

**🐛 Bug Hunter**

- Reportar y/o solucionar bugs

**💡 Feature Creator**

- Implementar nuevas funcionalidades

**📚 Documentation Hero**

- Mejoras significativas en documentación

**🧪 Testing Champion**

- Contribuciones en testing y quality assurance

**🏗️ Architecture Advisor**

- Propuestas de mejoras arquitecturales

**🤝 Community Helper**

- Ayudar a otros contributors

### Hall of Fame 🏛️

Los contributors destacados aparecen en:

- README principal del proyecto
- CHANGELOG con menciones específicas
- GitHub Discussions como featured contributors
- Recomendaciones LinkedIn (para estudiantes destacados)

### Beneficios para Aprendices 🎓

**Portfolio Development** 💼

- Experiencia real en proyecto open source
- Contribuciones visibles en GitHub profile
- Referencias técnicas para futuros empleos

**Skill Building** 🚀

- Code review profesional
- Trabajo en equipo remoto
- Process de desarrollo ágil
- Communication en contexto técnico

**Networking** 🌐

- Conexión con comunidad de desarrolladores
- Mentoring de profesionales experimentados
- Participación en discusiones técnicas

## 📞 Canales de Comunicación

### GitHub Issues 🐛

- Bug reports
- Feature requests
- Preguntas técnicas específicas

### GitHub Discussions 💬

- Discusiones generales
- Ideas y propuestas
- Show and tell
- Q&A community

### Code Reviews 👀

- Feedback constructivo
- Learning opportunities
- Pair programming virtual

## ❓ FAQ para Contributors

### ¿Cómo empiezo si soy principiante?

1. **Busca issues etiquetados como "good first issue"**
2. **Lee la documentación completa**
3. **Configura tu entorno de desarrollo**
4. **Haz una contribución pequeña primero** (ej. fix de typo)
5. **Pide ayuda cuando la necesites**

### ¿Qué pasa si mi PR es rechazado?

- **Es parte del proceso de aprendizaje** 📚
- **Recibirás feedback constructivo** 💡
- **Puedes hacer las correcciones necesarias** 🔧
- **Cada iteración te hace mejor developer** 🚀

### ¿Puedo trabajar en múltiples issues al mismo tiempo?

- **Principiantes**: Un issue a la vez
- **Contributors experimentados**: Máximo 2-3 issues
- **Comunica tu progreso** regularmente

### ¿Cómo mantengo mi fork actualizado?

```bash
# Sincroniza con upstream regularmente
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

---

## 🎉 ¡Bienvenido/a a la Comunidad!

Contribuir a bc-fastapi no solo mejora el proyecto, sino que **acelera tu crecimiento como developer profesional**.

Cada línea de código, cada bug report, cada mejora en documentación te acerca más a ser el developer que quieres ser.

**¡Tu contribución cuenta! 🌟**

---

_¿Tienes preguntas sobre esta guía? ¡Abre un issue con el label "question"!_
