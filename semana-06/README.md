# Semana 6: Testing y Roles de Usuario

⏰ **DURACIÓN TOTAL: 6 HORAS EXACTAS**  
📚 **NIVEL: Intermedio (construye sobre Semanas 1-5)**

## 🚨 **IMPORTANTE: Testing + Roles Básicos**

Esta semana está diseñada para estudiantes que **ya tienen una API completa con autenticación** (Semanas 1-5). Implementaremos testing automatizado y sistema básico de roles.

- ✅ **Completamente realizable en 6 horas**
- ✅ **Enfoque práctico en testing de APIs + roles**
- ✅ **Preparación para desarrollo profesional**

## 🎯 Objetivos de la Semana AJUSTADOS (Fundamentales)

Al finalizar esta semana de 5h 30min efectivos (incluye break de 30 min), los estudiantes:

1. ✅ **Implementarán testing automatizado** con pytest básico
2. ✅ **Crearán tests para endpoints** de autenticación y CRUD
3. ✅ **Implementarán sistema de roles** admin/user básico
4. ✅ **Testing de autorización** con roles y permisos
5. ✅ **Organizarán código** con estructura profesional

### ❌ **Lo que NO se espera dominar esta semana** (MOVIDO A SEMANA 7)

- ~~Cobertura avanzada con coverage~~ → **Semana 7**
- ~~Testing avanzado con mocks complejos~~ → **Semana 7**
- Performance testing avanzado
- Security testing automatizado
- Análisis de código con SonarQube completo

## ⏱️ Distribución de Tiempo AJUSTADA (5h 30min efectivos)

| Bloque | Actividad                 | Tiempo  | Descripción                    |
| ------ | ------------------------- | ------- | ------------------------------ |
| **1**  | Pytest Básico             | 75 min  | Setup, fixtures, tests básicos |
| **2**  | Testing de APIs           | 45 min  | TestClient, endpoints testing  |
| **3**  | Testing con Autenticación | 60 min  | Mocks, usuarios, tokens        |
| **4**  | Roles y Autorización      | 105 min | Sistema roles, admin, testing  |
| **5**  | Consolidación             | 45 min  | Testing completo, debugging    |

**CAMBIOS PRINCIPALES:**

- ✅ **Agregado**: Sistema completo de roles (desde Semana 5)
- ⬇️ **Reducido**: Testing de APIs de 90 a 45 minutos
- ⬇️ **Reducido**: Testing con Auth de 90 a 60 minutos
- ❌ **Eliminado**: Coverage avanzado (se mueve a Semana 7)
- ✅ **Enfocado**: Testing funcional + roles operativos

## 📚 Contenido de la Semana

### **📋 Navegación Ordenada (Seguir este orden)**

1. **[🧭 1-teoria/](./1-teoria/)** - Conceptos de testing y calidad
2. **[💻 2-practica/](./2-practica/)** - Implementación pytest y testing
3. **[🎯 3-ejercicios/](./3-ejercicios/)** - Ejercicios de testing
4. **[🚀 4-proyecto/](./4-proyecto/)** - API con testing completo
5. **[📚 5-recursos/](./5-recursos/)** - Referencias y herramientas

### **🧭 Teoría**

- [🧪 Testing y Calidad en APIs](./1-teoria/testing-concepts.md)

### **💻 Prácticas**

1. [🔧 Pytest Setup y Configuración](./2-practica/19-pytest-setup.md) _(75 min)_
2. [🧪 Testing de Endpoints](./2-practica/20-endpoint-testing.md) _(45 min)_
3. [🔐 Testing con Autenticación](./2-practica/21-auth-testing.md) _(60 min)_
4. [� Roles y Autorización](./2-practica/23-roles-implementation.md) _(105 min)_
5. [🔄 Consolidación y Testing Completo](./2-practica/24-consolidation.md) _(45 min)_

**ELIMINADO/MOVIDO A SEMANA 7:**

- ~~Coverage y Calidad de Código~~ → **Semana 7**

### **💪 Ejercicios**

- [🎯 Ejercicios de Testing](./3-ejercicios/ejercicios-testing.md)

### **🚀 Proyecto**

- [🏪 E-commerce con Testing Completo](./4-proyecto/especificacion-testing.md)

### **📚 Recursos**

- [📖 Recursos de Testing](./5-recursos/recursos-apoyo.md)

---

## 🧪 Tecnologías de la Semana

### **Stack de Testing**

- **pytest**: Framework principal de testing para Python
- **httpx**: Cliente HTTP asíncrono para testing de APIs
- **pytest-asyncio**: Soporte para testing asíncrono
- **coverage**: Medición de cobertura de código

### **Herramientas de Calidad**

- **FastAPI TestClient**: Cliente de testing específico de FastAPI
- **pytest fixtures**: Configuración reutilizable de tests
- **Mock**: Para simular dependencias externas
- **Coverage Report**: Reportes de cobertura en HTML/terminal

---

## ⏱️ **Estructura de 6 Horas (Incluye Break de 30 min)**

### **Bloque 1: Pytest Básico (75 min)**

- **19-pytest-setup.md**
- Instalación y configuración de pytest
- Fixtures básicas y estructura de tests
- Primeros tests unitarios

### **☕ BREAK OBLIGATORIO (30 min)**

- Descanso para asimilar conceptos de testing
- Tiempo para resolver dudas sobre pytest
- Preparación mental para testing de APIs

### **Bloque 2: Testing de APIs (120 min)**

- **20-endpoint-testing.md**
- FastAPI TestClient setup
- Testing de endpoints CRUD
- Validación de respuestas y errores

### **Bloque 3: Testing con Autenticación (90 min)**

- **21-auth-testing.md**
- Testing de login y registro
- Mocking de JWT tokens
- Testing de endpoints protegidos

### **Bloque 4: Cobertura y Calidad (45 min)**

- **22-coverage-quality.md**
- Medición de cobertura de código
- Reportes y análisis
- Organización y documentación

---

## 📋 Pre-requisitos Esenciales

### **✅ Conocimientos Requeridos**

- [x] **FastAPI completo** (Semanas 1-3)
- [x] **SQLAlchemy y bases de datos** (Semana 4)
- [x] **Autenticación JWT** (Semana 5)
- [x] **Endpoints CRUD funcionando** (Semanas 3-4)

### **⚠️ Si no tienes estos conocimientos**

- Completar semanas anteriores primero
- Tener una API funcional con autenticación
- Consultar con instructores antes de continuar

---

## 🎯 Competencias que Desarrollarás

**Al inicio de la semana ya sabes:**

- Crear APIs REST completas con autenticación
- Trabajar con bases de datos y JWT
- Implementar CRUD operations
- Proteger endpoints con roles

**Al final de la semana dominarás:**

- ✅ **Testing automatizado** - Pytest y fixtures básicas
- ✅ **Testing de APIs** - TestClient y validaciones
- ✅ **Testing con autenticación** - Mocks y tokens
- ✅ **Sistema de roles** - Admin/user con autorización
- ✅ **Organización de código** - Estructura profesional

### **ELIMINADO/MOVIDO A SEMANA 7:**

- ~~Cobertura avanzada~~ → **Semana 7**
- ~~Testing avanzado con mocks complejos~~ → **Semana 7**
- ~~Análisis de calidad completo~~ → **Semana 7**

---

## 🚀 Quick Start

```bash
# 1. Instalar dependencias de testing
pip install pytest httpx pytest-asyncio coverage

# 2. Actualizar requirements.txt
pip freeze > requirements.txt

# 3. Crear estructura de tests
mkdir tests
touch tests/__init__.py
touch tests/conftest.py

# 4. ¡Listo para empezar con testing!
```

## 📅 Cronograma AJUSTADO de la Jornada (5h 30min efectivos)

| Tiempo      | Actividad                 | Duración | Acumulado |
| ----------- | ------------------------- | -------- | --------- |
| 12:00-13:15 | Pytest Básico             | 75 min   | 75 min    |
| 13:15-14:00 | Testing de APIs           | 45 min   | 120 min   |
| 14:00-14:30 | **☕ BREAK OBLIGATORIO**  | 30 min   | 150 min   |
| 14:30-15:30 | Testing con Autenticación | 60 min   | 210 min   |
| 15:30-17:15 | Roles y Autorización      | 105 min  | 315 min   |
| 17:15-18:00 | Consolidación y Testing   | 45 min   | 360 min   |

**Total**: Exactamente 5h 30min efectivos (330 minutos + 30min break)

### **📖 Orden de Estudio Recomendado**

1. **Pytest setup** - Fundamentos de testing
2. **Testing de endpoints** - Validación de APIs
3. **Testing con autenticación** - Seguridad en tests
4. **Cobertura y calidad** - Métricas de calidad
5. **Ejercicios y proyecto** - Para reforzar conceptos

---

## 💡 Tips para el Éxito

1. **🧪 Test first**: Escribir tests antes de arreglar bugs
2. **📊 Cobertura != Calidad**: 80% de cobertura es buena meta inicial
3. **🔧 Fixtures reutilizables**: Evitar duplicación en tests
4. **📝 Tests descriptivos**: Nombres claros de lo que se prueba
5. **⚡ Tests rápidos**: Tests unitarios deben ser muy rápidos

---

## 📊 Evaluación Final

### **Al completar la semana debes poder:**

- [x] Configurar pytest para un proyecto FastAPI
- [x] Crear tests para endpoints CRUD básicos
- [x] Testing de autenticación y endpoints protegidos
- [x] Medir y reportar cobertura de código
- [x] Organizar código con buenas prácticas

### **📦 Entregables**

1. **API con tests automatizados funcionando**
2. **Suite de tests cubriendo funcionalidad principal**
3. **Reporte de cobertura > 70%**
4. **Código organizado y documentado**

---

## 🆘 Soporte

- **📚 Documentación**: pytest docs, FastAPI testing
- **🎓 Instructor**: Consultas durante clases
- **👥 Compañeros**: Pair programming en tests
- **📞 Slack**: Canal del bootcamp para dudas

---

## 🎉 ¡Prepárate para crear APIs de calidad profesional! 🧪✨
