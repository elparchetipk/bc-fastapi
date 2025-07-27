# Semana 6: Testing y Calidad de Código

⏰ **DURACIÓN TOTAL: 6 HORAS EXACTAS**  
📚 **NIVEL: Intermedio (construye sobre Semanas 1-5)**

## 🚨 **IMPORTANTE: Consolidando Conocimientos**

Esta semana está diseñada para estudiantes que **ya tienen una API completa con autenticación** (Semanas 1-5). Implementaremos testing automatizado y mejorará la calidad del código.

- ✅ **Completamente realizable en 6 horas**
- ✅ **Enfoque práctico en testing de APIs**
- ✅ **Preparación para desarrollo profesional**

## 🎯 Objetivos de la Semana (Fundamentales)

Al finalizar esta semana de 6 horas (incluye break de 30 min), los estudiantes:

1. ✅ **Implementarán testing automatizado** con pytest básico
2. ✅ **Crearán tests para endpoints** de autenticación y CRUD
3. ✅ **Medirán cobertura de código** con coverage básico
4. ✅ **Aplicarán buenas prácticas** de testing en APIs
5. ✅ **Organizarán código** con estructura profesional

### ❌ **Lo que NO se espera dominar esta semana**

- Testing avanzado con mocks complejos
- Integración con CI/CD completa
- Performance testing avanzado
- Security testing automatizado
- Análisis de código con SonarQube completo

## ⏱️ Distribución de Tiempo (6 horas total)

| Bloque | Actividad                 | Tiempo | Descripción                       |
| ------ | ------------------------- | ------ | --------------------------------- |
| **1**  | Pytest Básico             | 90 min | Setup, fixtures, tests básicos    |
| **2**  | Testing de APIs           | 90 min | TestClient, endpoints testing     |
| **3**  | Testing con Autenticación | 90 min | Mocks, usuarios, tokens           |
| **4**  | Cobertura y Calidad       | 90 min | Coverage, organización, documenta |

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

1. [🔧 Pytest Setup y Configuración](./2-practica/19-pytest-setup.md) _(90 min)_
2. [🧪 Testing de Endpoints](./2-practica/20-endpoint-testing.md) _(90 min)_
3. [🔐 Testing con Autenticación](./2-practica/21-auth-testing.md) _(90 min)_
4. [📊 Coverage y Calidad de Código](./2-practica/22-coverage-quality.md) _(90 min)_

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
- ✅ **Cobertura de código** - Coverage y reportes
- ✅ **Calidad de código** - Organización y documentación

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

### **📖 Orden de Estudio Recomendado**

1. **Leer teoría** (30 min) - Conceptos de testing
2. **Práctica 19** (75 min) - Pytest setup
3. **Break** (30 min) - Descanso obligatorio
4. **Práctica 20** (120 min) - Testing de endpoints
5. **Práctica 21** (90 min) - Testing con autenticación
6. **Práctica 22** (45 min) - Cobertura y calidad
7. **Ejercicios y proyecto** - Para reforzar conceptos

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
