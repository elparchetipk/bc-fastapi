# Proyecto Semana 6: Sistema de Testing y QA para API de Gestión

## 🎯 Objetivo del Proyecto

Implementar un sistema completo de testing y quality assurance para una API de gestión de tareas, aplicando todas las técnicas aprendidas durante la semana.

## 📋 Descripción General

Los estudiantes trabajarán con una API base de gestión de tareas y deberán implementar:

- Suite completa de tests (unitarios, integración, end-to-end)
- Herramientas de quality assurance
- Análisis de cobertura y performance
- Pipeline de CI/CD con testing automatizado

## ⏱️ Tiempo Estimado

**6 horas** (distribuidas durante la semana con apoyo en clase)

---

## 🏗️ Estructura del Proyecto Base

### API Base Proporcionada

```
task_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── schemas/
│   │   ├── user.py
│   │   └── task.py
│   ├── crud/
│   │   ├── user.py
│   │   └── task.py
│   ├── api/
│   │   ├── auth.py
│   │   ├── users.py
│   │   └── tasks.py
│   └── services/
│       ├── email_service.py
│       └── notification_service.py
├── requirements.txt
└── README.md
```

### Funcionalidades de la API Base

1. **Autenticación**: Registro, login, logout
2. **Gestión de usuarios**: CRUD básico
3. **Gestión de tareas**: CRUD con estados (pendiente, en_progreso, completada)
4. **Notificaciones**: Email y sistema interno
5. **Filtros y búsqueda**: Por estado, fecha, usuario

---

## 📝 Especificaciones del Proyecto

### Parte 1: Setup y Configuración (1 hora)

#### 1.1 Estructura de Testing

```
tests/
├── __init__.py
├── conftest.py
├── unit/
│   ├── test_models.py
│   ├── test_schemas.py
│   ├── test_crud.py
│   └── test_services.py
├── integration/
│   ├── test_auth_endpoints.py
│   ├── test_user_endpoints.py
│   ├── test_task_endpoints.py
│   └── test_workflow.py
├── performance/
│   ├── test_load.py
│   └── test_benchmarks.py
├── fixtures/
│   ├── user_fixtures.py
│   └── task_fixtures.py
└── utils/
    └── test_helpers.py
```

#### 1.2 Configuraciones Requeridas

- **pytest.ini**: Configuración básica con markers
- **pyproject.toml**: Black, isort, mypy, coverage
- **.flake8**: Configuración de linting
- **requirements-dev.txt**: Dependencias de desarrollo

### Parte 2: Tests Unitarios (1.5 horas)

#### 2.1 Tests para Modelos

```python
# Ejemplo: tests/unit/test_models.py
class TestTaskModel:
    def test_task_creation(self):
        """Test creación básica de tarea."""

    def test_task_status_transitions(self):
        """Test transiciones válidas de estado."""

    def test_task_validation(self):
        """Test validaciones de campos."""
```

**Requisitos:**

- [ ] Tests para modelo User (5+ tests)
- [ ] Tests para modelo Task (8+ tests)
- [ ] Tests para validaciones de campos
- [ ] Tests para métodos de instancia
- [ ] Tests para propiedades calculadas

#### 2.2 Tests para Schemas

```python
# Ejemplo: tests/unit/test_schemas.py
class TestTaskSchemas:
    def test_task_create_schema(self):
        """Test schema de creación de tarea."""

    def test_task_update_schema(self):
        """Test schema de actualización."""

    def test_schema_validation_errors(self):
        """Test errores de validación."""
```

**Requisitos:**

- [ ] Tests para todos los schemas de entrada
- [ ] Tests para schemas de respuesta
- [ ] Tests para validaciones Pydantic
- [ ] Tests para casos de error

#### 2.3 Tests para CRUD Operations

```python
# Ejemplo: tests/unit/test_crud.py
class TestTaskCRUD:
    def test_create_task(self, db_session, test_user):
        """Test creación de tarea."""

    def test_get_tasks_by_user(self, db_session, test_user, sample_tasks):
        """Test obtener tareas por usuario."""

    def test_update_task_status(self, db_session, sample_task):
        """Test actualización de estado."""
```

**Requisitos:**

- [ ] Tests para todas las operaciones CRUD
- [ ] Tests con fixtures de base de datos
- [ ] Tests para filtros y búsquedas
- [ ] Tests para casos de error

### Parte 3: Tests de Integración (2 horas)

#### 3.1 Tests de Endpoints de Autenticación

```python
class TestAuthEndpoints:
    @pytest.mark.asyncio
    async def test_register_success(self, client):
        """Test registro exitoso."""

    @pytest.mark.asyncio
    async def test_login_success(self, client, test_user):
        """Test login exitoso."""

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_token(self, authenticated_client):
        """Test acceso a endpoint protegido."""
```

**Requisitos:**

- [ ] Tests para registro de usuario
- [ ] Tests para login/logout
- [ ] Tests para refresh de tokens
- [ ] Tests para endpoints protegidos
- [ ] Tests para casos de error de autenticación

#### 3.2 Tests de Endpoints de Tareas

```python
class TestTaskEndpoints:
    @pytest.mark.asyncio
    async def test_create_task(self, authenticated_client):
        """Test creación de tarea."""

    @pytest.mark.asyncio
    async def test_get_user_tasks(self, authenticated_client, user_with_tasks):
        """Test obtener tareas de usuario."""

    @pytest.mark.asyncio
    async def test_update_task_status(self, authenticated_client, sample_task):
        """Test actualización de estado de tarea."""
```

**Requisitos:**

- [ ] Tests para CRUD completo de tareas
- [ ] Tests para filtros y paginación
- [ ] Tests para autorización (solo propias tareas)
- [ ] Tests para validaciones de entrada
- [ ] Tests para casos de error HTTP

#### 3.3 Tests de Workflow Completo

```python
class TestCompleteWorkflow:
    @pytest.mark.asyncio
    async def test_user_task_lifecycle(self, client):
        """Test ciclo completo: registro -> login -> crear tarea -> completar."""
```

**Requisitos:**

- [ ] Test de journey completo de usuario
- [ ] Test de workflow de tareas (crear -> actualizar -> completar)
- [ ] Test de colaboración entre usuarios
- [ ] Test de casos de error en workflows

### Parte 4: Mocking y Testing Avanzado (1 hora)

#### 4.1 Mocking de Servicios Externos

```python
class TestEmailService:
    @patch('app.services.email_service.smtp_client.send')
    async def test_send_task_notification(self, mock_send):
        """Test envío de notificación por email."""

    @patch('app.services.notification_service.push_notification')
    async def test_push_notification_failure(self, mock_push):
        """Test manejo de falla en notificación push."""
```

**Requisitos:**

- [ ] Mock del servicio de email
- [ ] Mock del servicio de notificaciones
- [ ] Tests para manejo de errores de servicios externos
- [ ] Tests para timeouts y retry logic

#### 4.2 Tests de Performance

```python
class TestPerformance:
    @pytest.mark.asyncio
    async def test_get_tasks_performance(self, authenticated_client):
        """Test performance de endpoint de tareas."""

    @pytest.mark.asyncio
    async def test_concurrent_task_creation(self, authenticated_client):
        """Test creación concurrente de tareas."""
```

**Requisitos:**

- [ ] Tests de tiempo de respuesta
- [ ] Tests de carga concurrente
- [ ] Tests de performance de consultas DB
- [ ] Benchmarks básicos

### Parte 5: Quality Assurance (30 minutos)

#### 5.1 Configuración de Herramientas

**Requisitos:**

- [ ] Black configurado para formateo automático
- [ ] isort configurado para ordenar imports
- [ ] flake8 configurado para linting
- [ ] mypy configurado para type checking
- [ ] Scripts de quality check automatizados

#### 5.2 Coverage Analysis

**Requisitos:**

- [ ] pytest-cov configurado
- [ ] Reporte HTML de coverage generado
- [ ] Coverage objetivo de 85% alcanzado
- [ ] Análisis de líneas no cubiertas

---

## 🎯 Entregables

### Entregable Principal

**Repositorio con testing completo** que incluye:

1. **Suite de Tests** (40 puntos)

   - 20+ tests unitarios
   - 15+ tests de integración
   - 5+ tests de performance
   - Tests para casos de error

2. **Quality Assurance** (25 puntos)

   - Todas las herramientas de QA configuradas
   - Código pasa todos los quality checks
   - Scripts de automatización

3. **Coverage y Documentación** (25 puntos)

   - Coverage ≥ 85%
   - Reporte HTML generado
   - README con instrucciones de testing

4. **CI/CD Integration** (10 puntos)
   - GitHub Actions configurado
   - Tests ejecutándose automáticamente
   - Quality checks en pipeline

### Estructura de Entrega

```
proyecto-testing/
├── app/                     # Código base (proporcionado)
├── tests/                   # Suite completa de tests
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   ├── performance/
│   └── fixtures/
├── scripts/
│   ├── quality_check.sh
│   ├── run_tests.sh
│   └── coverage_report.sh
├── .github/workflows/
│   └── ci.yml
├── pytest.ini
├── pyproject.toml
├── .flake8
├── requirements-dev.txt
├── README_TESTING.md
└── TESTING_REPORT.md
```

---

## 📊 Criterios de Evaluación

### Rúbrica Detallada

| Criterio              | Excelente (90-100%)                           | Bueno (70-89%)                | Satisfactorio (60-69%)        | Insuficiente (<60%)      |
| --------------------- | --------------------------------------------- | ----------------------------- | ----------------------------- | ------------------------ |
| **Tests Unitarios**   | 25+ tests, alta calidad, edge cases cubiertos | 20+ tests, buena calidad      | 15+ tests, calidad básica     | <15 tests o baja calidad |
| **Tests Integración** | 20+ tests, workflows completos                | 15+ tests, casos principales  | 10+ tests, casos básicos      | <10 tests                |
| **Mocking**           | Uso avanzado, servicios externos              | Uso intermedio, casos básicos | Uso básico, algunos mocks     | Sin mocking o mal uso    |
| **Coverage**          | ≥90%, análisis detallado                      | ≥85%, análisis básico         | ≥80%, reporte simple          | <80%                     |
| **Quality Assurance** | Todas herramientas, automatizado              | Herramientas principales      | Configuración básica          | Sin QA o mal configurado |
| **Performance Tests** | Tests avanzados, benchmarks                   | Tests básicos, métricas       | Tests simples                 | Sin performance tests    |
| **CI/CD**             | Pipeline completo, optimizado                 | Pipeline básico funcional     | Configuración simple          | Sin CI/CD                |
| **Documentación**     | Completa, ejemplos, guías                     | Buena, instrucciones claras   | Básica, instrucciones mínimas | Insuficiente             |

### Criterios de Calidad

#### Testing Excellence

- [ ] Tests independientes y determinísticos
- [ ] Fixtures reutilizables y bien organizados
- [ ] Nombres descriptivos y auto-documentados
- [ ] Cobertura de casos edge y errores
- [ ] Performance tests con métricas claras

#### Code Quality

- [ ] Código pasa todas las herramientas de QA
- [ ] Type hints en todas las funciones
- [ ] Documentación en funciones complejas
- [ ] Estructura clara y modular
- [ ] Sin código duplicado

#### Professional Standards

- [ ] README completo con instrucciones
- [ ] Requirements actualizado
- [ ] Git history limpio
- [ ] CI/CD funcionando correctamente
- [ ] Reporte de testing detallado

---

## 🚀 Extensiones Opcionales (Puntos Extra)

### Nivel Avanzado (5-10 puntos extra)

1. **Load Testing con Locust**

   ```python
   # locustfile.py
   from locust import HttpUser, task

   class TaskAPIUser(HttpUser):
       @task
       def get_tasks(self):
           self.client.get("/tasks/")
   ```

2. **Property-based Testing con Hypothesis**

   ```python
   from hypothesis import given, strategies as st

   @given(st.text(min_size=1, max_size=100))
   def test_task_title_validation(self, title):
       # Test con datos generados automáticamente
   ```

3. **Mutation Testing**

   ```bash
   pip install mutmut
   mutmut run --paths-to-mutate=app/
   ```

4. **Security Testing**

   ```python
   def test_sql_injection_protection(self, client):
       # Tests para vulnerabilidades comunes
   ```

5. **Contract Testing**
   ```python
   # Tests para contratos de API
   def test_api_schema_compliance(self, client):
       # Verificar que responses cumplen el schema
   ```

---

## 📚 Recursos de Apoyo

### Documentación Técnica

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py Guide](https://coverage.readthedocs.io/)

### Ejemplos de Referencia

- [FastAPI Testing Examples](https://github.com/tiangolo/fastapi/tree/master/tests)
- [pytest Best Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)

### Herramientas Recomendadas

- **pytest**: Framework principal
- **httpx**: Cliente HTTP asíncrono
- **factory-boy**: Generación de datos de test
- **freezegun**: Control de tiempo en tests
- **pytest-mock**: Facilita el uso de mocks

---

## 🎯 Objetivos de Aprendizaje Verificables

Al completar este proyecto, los estudiantes habrán demostrado:

1. **Testing Fundamentals**

   - [ ] Diferencia entre tests unitarios, integración y e2e
   - [ ] Uso efectivo de fixtures y mocks
   - [ ] Organización de suite de tests

2. **Quality Assurance**

   - [ ] Configuración de herramientas de QA
   - [ ] Interpretación de métricas de coverage
   - [ ] Automatización de quality checks

3. **Professional Practices**

   - [ ] CI/CD para testing
   - [ ] Documentación de testing
   - [ ] Performance testing básico

4. **FastAPI Specific**
   - [ ] Testing de endpoints asíncronos
   - [ ] Testing de autenticación/autorización
   - [ ] Testing de base de datos

---

## 📅 Cronograma Sugerido

### Durante la Semana (Distribución de 6 horas)

**Sesión 1 (2 horas)**: Setup y Tests Unitarios

- Configuración del entorno
- Implementación de tests unitarios básicos

**Sesión 2 (2 horas)**: Tests de Integración

- Tests de endpoints
- Implementación de fixtures complejos

**Sesión 3 (1 hora)**: QA y Performance

- Configuración de herramientas de QA
- Tests de performance básicos

**Sesión 4 (1 hora)**: CI/CD y Documentación

- Configuración de GitHub Actions
- Documentación final y entrega

### Hitos de Verificación

- **Día 2**: Tests unitarios funcionando
- **Día 4**: Tests de integración completos
- **Día 6**: QA configurado y CI/CD funcionando

---

_Este proyecto integra todos los conceptos de testing y quality assurance aprendidos durante la semana, proporcionando experiencia práctica con herramientas y técnicas profesionales de desarrollo._
