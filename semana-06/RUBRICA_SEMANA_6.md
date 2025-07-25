# Rúbrica de Evaluación - Semana 6: Testing y Quality Assurance

## 📊 Información General

**Tema:** Implementación de testing comprehensivo y quality assurance en proyectos FastAPI  
**Duración:** 6 horas de contenido principal  
**Modalidad:** Teoría + prácticas guiadas + proyecto de testing completo  
**Peso en curso:** 15% de la calificación total del bootcamp

---

## 🎯 Objetivos de Evaluación

### Competencias Centrales Evaluadas

1. **Testing Implementation** - Tests unitarios e integración funcionales
2. **Quality Assurance** - Herramientas y procesos de QA configurados
3. **Coverage Analysis** - Medición y optimización del coverage
4. **Test Design** - Estructura y patterns apropiados de testing
5. **Automation** - CI/CD y quality gates implementados

---

## 📋 Criterios de Evaluación

### 🧪 1. Testing Implementation (30% - 30 puntos)

#### **Excelente (27-30 puntos)**

- ✅ Tests unitarios completos para todas las funciones críticas
- ✅ Tests de integración para todos los endpoints principales
- ✅ Tests de autenticación y autorización implementados
- ✅ Tests de base de datos con fixtures apropiadas
- ✅ Tests asíncronos correctamente implementados
- ✅ Estructura de tests clara y mantenible

#### **Proficiente (21-26 puntos)**

- ✅ Tests unitarios para funciones principales
- ✅ Tests de integración para endpoints básicos
- ✅ Tests de autenticación básicos
- ✅ Tests de database con setup correcto
- ⚠️ Tests asíncronos con configuración básica
- ✅ Estructura de tests organizada

#### **En Desarrollo (15-20 puntos)**

- ⚠️ Tests unitarios básicos implementados
- ⚠️ Algunos tests de integración funcionales
- ⚠️ Tests de auth con cobertura limitada
- ⚠️ Tests de database básicos
- ❌ Tests asíncronos limitados o incorrectos
- ⚠️ Estructura de tests mejorable

#### **Insuficiente (0-14 puntos)**

- ❌ Tests unitarios insuficientes o no funcionales
- ❌ Tests de integración ausentes o fallidos
- ❌ Sin tests de autenticación
- ❌ Tests de database incorrectos o ausentes
- ❌ No maneja testing asíncrono
- ❌ Estructura de tests confusa o inexistente

### 📊 2. Coverage Analysis (25% - 25 puntos)

#### **Excelente (23-25 puntos)**

- ✅ Coverage overall ≥85% con calidad
- ✅ Coverage de líneas críticas al 100%
- ✅ Coverage reports configurados y legibles
- ✅ Exclusiones de coverage justificadas
- ✅ Branch coverage implementado
- ✅ Coverage integrado en CI/CD

#### **Proficiente (18-22 puntos)**

- ✅ Coverage overall ≥75%
- ✅ Coverage de funciones principales completo
- ✅ Coverage reports básicos configurados
- ✅ Algunas exclusiones apropriadas
- ⚠️ Branch coverage parcial
- ✅ Coverage measurement automatizado

#### **En Desarrollo (13-17 puntos)**

- ⚠️ Coverage overall ≥60%
- ⚠️ Coverage de funciones básicas
- ⚠️ Coverage reports básicos
- ⚠️ Exclusiones no siempre justificadas
- ❌ Sin branch coverage
- ⚠️ Measurement manual o incompleto

#### **Insuficiente (0-12 puntos)**

- ❌ Coverage <60% o no medido
- ❌ Coverage de funciones críticas insuficiente
- ❌ Sin coverage reports configurados
- ❌ Exclusiones inadecuadas o excesivas
- ❌ No comprende branch coverage
- ❌ Sin automation de measurement

### 🔧 3. Quality Assurance Setup (20% - 20 puntos)

#### **Excelente (18-20 puntos)**

- ✅ Pre-commit hooks completamente configurados
- ✅ Linting (flake8/pylint) sin errores
- ✅ Formatting (black) aplicado consistentemente
- ✅ Type checking (mypy) configurado y pasando
- ✅ Import sorting (isort) configurado
- ✅ Quality gates en CI/CD funcionando

#### **Proficiente (14-17 puntos)**

- ✅ Pre-commit hooks básicos configurados
- ✅ Linting con pocos errores menores
- ✅ Formatting aplicado en su mayoría
- ✅ Type checking básico configurado
- ✅ Import sorting funcional
- ⚠️ Quality gates parciales en CI

#### **En Desarrollo (10-13 puntos)**

- ⚠️ Pre-commit hooks parcialmente configurados
- ⚠️ Linting con varios errores
- ⚠️ Formatting inconsistente
- ⚠️ Type checking limitado
- ⚠️ Import sorting no configurado
- ❌ Sin quality gates en CI

#### **Insuficiente (0-9 puntos)**

- ❌ Sin pre-commit hooks o no funcionan
- ❌ Muchos errores de linting
- ❌ Sin formatting consistency
- ❌ Sin type checking
- ❌ Imports desorganizados
- ❌ Sin automation de quality

### 🎭 4. Test Design y Patterns (15% - 15 puntos)

#### **Excelente (14-15 puntos)**

- ✅ Uso apropiado de fixtures y factory patterns
- ✅ Mocking estratégico y efectivo
- ✅ Parametrized tests donde apropiado
- ✅ Test isolation bien implementado
- ✅ Arrange-Act-Assert pattern consistente
- ✅ Tests descriptivos y mantenibles

#### **Proficiente (11-13 puntos)**

- ✅ Fixtures básicas bien implementadas
- ✅ Mocking utilizado correctamente
- ✅ Algunos parametrized tests
- ✅ Test isolation general
- ✅ AAA pattern principalmente seguido
- ✅ Tests generalmente claros

#### **En Desarrollo (8-10 puntos)**

- ⚠️ Fixtures básicas con algunos problemas
- ⚠️ Mocking limitado o incorrecto
- ⚠️ Pocos parametrized tests
- ⚠️ Isolation ocasionalmente comprometido
- ⚠️ AAA pattern inconsistente
- ⚠️ Tests no siempre claros

#### **Insuficiente (0-7 puntos)**

- ❌ Fixtures mal implementadas o ausentes
- ❌ Mocking incorrecto o ausente
- ❌ Sin parametrized tests
- ❌ Tests interdependientes
- ❌ Sin estructura clara en tests
- ❌ Tests confusos o sin sentido

### 🔄 5. CI/CD Integration y Automation (10% - 10 puntos)

#### **Excelente (9-10 puntos)**

- ✅ GitHub Actions configurado correctamente
- ✅ Tests automatizados en multiple Python versions
- ✅ Quality checks automatizados
- ✅ Coverage reports automatizados
- ✅ Failure notifications configuradas
- ✅ Branch protection con status checks

#### **Proficiente (7-8 puntos)**

- ✅ GitHub Actions básico funcionando
- ✅ Tests automatizados en una versión Python
- ✅ Algunos quality checks automatizados
- ✅ Coverage measurement automatizado
- ⚠️ Notifications básicas
- ✅ Branch protection básico

#### **En Desarrollo (5-6 puntos)**

- ⚠️ GitHub Actions con configuración incompleta
- ⚠️ Tests parcialmente automatizados
- ⚠️ Quality checks limitados
- ⚠️ Coverage manual o inconsistente
- ❌ Sin notifications
- ⚠️ Branch protection limitado

#### **Insuficiente (0-4 puntos)**

- ❌ Sin CI/CD configurado o no funcional
- ❌ Tests no automatizados
- ❌ Sin quality automation
- ❌ Sin coverage automation
- ❌ Sin configuración de repository
- ❌ No comprende CI/CD concepts

---

## 🏆 Niveles de Logro General

### **Excelente (90-100 puntos) - Grade A**

**Características:**

- Suite de tests comprehensiva y bien diseñada
- Quality assurance completamente automatizado
- Coverage alto con tests de calidad
- CI/CD pipeline robusto y confiable
- Código que sirve como ejemplo para otros

**Indicadores:**

- ≥85% test coverage con alta calidad
- 0 errores de linting, formatting perfecto
- Tests ejecutan en <30 segundos
- CI/CD pipeline completamente funcional
- Documentación de testing clara y completa

### **Proficiente (75-89 puntos) - Grade B**

**Características:**

- Tests funcionales cubriendo casos principales
- QA tools configurados y funcionando
- Coverage adecuado con buena calidad
- CI básico configurado correctamente
- Código mantenible y bien organizado

**Indicadores:**

- ≥75% test coverage
- Pocos errores de linting menores
- Tests ejecutan en tiempo razonable
- CI básico funcional
- Documentación de testing adecuada

### **En Desarrollo (60-74 puntos) - Grade C**

**Características:**

- Tests básicos implementados
- Algunas herramientas de QA configuradas
- Coverage aceptable pero mejorable
- Automation parcial implementada
- Necesita refinamiento en varios aspectos

**Indicadores:**

- ≥60% test coverage
- Varios errores de linting
- Tests con performance mejorable
- CI parcialmente configurado
- Documentación básica presente

### **Insuficiente (< 60 puntos) - Grade F**

**Características:**

- Tests insuficientes o no funcionales
- QA tools ausentes o mal configurados
- Coverage bajo o no medido
- Sin automation o no funcional
- Requiere trabajo significativo

**Indicadores:**

- <60% test coverage o no medido
- Muchos errores de quality
- Tests lentos o fallando
- Sin CI/CD funcional
- Documentación insuficiente o ausente

---

## 📝 Entregables Específicos

### **📤 Entregables Obligatorios**

1. **Test Suite Completo**

   - Tests unitarios para todas las funciones críticas
   - Tests de integración para endpoints principales
   - Tests de autenticación y autorización
   - Tests de base de datos con fixtures

2. **Quality Setup**

   - Pre-commit hooks configurados
   - Linting y formatting automatizados
   - Type checking configurado
   - Coverage measurement automatizado

3. **CI/CD Pipeline**

   - GitHub Actions configurado
   - Tests automatizados en CI
   - Quality checks automatizados
   - Coverage reports automatizados

4. **Documentation**
   - README con instrucciones de testing
   - Documentación de test patterns utilizados
   - Guía de contribution con quality standards

### **📋 Formato de Entrega**

```
proyecto-testing/
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Fixtures globales
│   ├── unit/                    # Tests unitarios
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   └── test_products.py
│   ├── integration/             # Tests de integración
│   │   ├── test_api_endpoints.py
│   │   ├── test_database.py
│   │   └── test_auth_flow.py
│   └── fixtures/                # Test data
│       ├── users.py
│       └── products.py
├── .github/
│   └── workflows/
│       └── tests.yml            # CI/CD pipeline
├── .pre-commit-config.yaml      # Pre-commit hooks
├── pytest.ini                  # Pytest configuration
├── .coverage                   # Coverage configuration
├── mypy.ini                    # Type checking config
└── README.md                   # Testing documentation
```

---

## 📊 Métrica de Evaluación por Semana

### **Milestone Checkpoints**

| Día   | Checkpoint     | Criterios                   | Peso |
| ----- | -------------- | --------------------------- | ---- |
| **2** | Basic Tests    | Unit tests funcionando      | 25%  |
| **3** | Integration    | API tests completos         | 25%  |
| **4** | Quality Setup  | QA tools configurados       | 25%  |
| **6** | Final Delivery | Todo completo y funcionando | 25%  |

### **Feedback Timeline**

- **Día 2:** Feedback sobre estructura de tests
- **Día 4:** Review de quality setup
- **Día 6:** Evaluación final y recomendaciones
- **Día 8:** Calificación final publicada

---

## 🔍 Criteria de Auto-evaluación

### **Antes de Entregar - Checklist**

- [ ] **Tests Pass:** Todos los tests pasan consistentemente
- [ ] **Coverage:** ≥85% coverage overall
- [ ] **Quality:** 0 errores de linting
- [ ] **Performance:** Test suite ejecuta en <30s
- [ ] **CI/CD:** Pipeline completamente funcional
- [ ] **Documentation:** README y docs completos

### **Quality Self-Check**

```bash
# Ejecutar antes de entregar
pytest --cov=app --cov-report=html --cov-report=term-missing
flake8 app/ tests/
black --check app/ tests/
isort --check-only app/ tests/
mypy app/
```

---

## 🆘 Recursos de Apoyo

### **Para Debugging de Tests**

- **pytest -v --tb=short:** Output verboso con tracebacks cortos
- **pytest --pdb:** Debugger automático en failures
- **pytest -k "test_name":** Ejecutar tests específicos
- **pytest --lf:** Solo tests que fallaron la última vez

### **Para Mejorar Coverage**

- **pytest --cov-report=html:** Reporte HTML detallado
- **coverage report --show-missing:** Líneas no cubiertas
- **coverage html:** Reporte interactivo en navegador

### **Para Quality Issues**

- **flake8 --statistics:** Summary de errores
- **black --diff:** Ver cambios propuestos
- **mypy --show-error-codes:** Códigos de error específicos

---

## 📞 Soporte Durante Evaluación

### **Canales de Ayuda**

- **GitHub Issues:** Para problemas técnicos específicos con etiqueta `testing-week6`
- **Office Hours:** Martes y Jueves 6-8 PM para debugging en vivo
- **Peer Support:** Channel Slack #semana-6-testing para ayuda entre estudiantes

### **Criterios de Extensión**

Se consideran extensiones en casos de:

- Problemas técnicos documentados con el CI/CD
- Issues complejos de compatibility entre herramientas
- Blockers relacionados con setup de testing environment

**Máximo:** 2 días de extensión con penalty mínimo en casos justificados.

---

**🎯 Esta rúbrica está diseñada para promover no solo la implementación técnica, sino también la comprensión profunda de testing y quality assurance como disciplinas fundamentales del desarrollo profesional.**
