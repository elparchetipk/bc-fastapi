# Rúbrica de Evaluación - Semana 2: Python Moderno para APIs

## 📋 Información General

⏰ **AJUSTADA PARA 6 HORAS DE CLASE**  
**Modalidad**: Evaluación práctica con mayor complejidad que Semana 1  
**Peso en el curso**: 12% de la nota final  
**Método de evaluación**: Revisión de código + demo funcional  
**Escala**: 0-100 puntos

## 🎯 **Objetivos Evaluados**

Esta rúbrica evalúa la evolución desde la API básica de Semana 1 hacia una API más robusta con Python moderno y características intermedias de FastAPI.

---

## 📊 Criterios de Evaluación

### 1. **Evolución desde Semana 1 (25 puntos)**

#### **Excelente (23-25 puntos)**

- ✅ API de Semana 1 exitosamente expandida (no reescrita)
- ✅ Código organizado y bien estructurado
- ✅ Commit history clara mostrando progresión
- ✅ Funcionalidad previa intacta + nuevas características

#### **Competente (18-22 puntos)**

- ✅ API expandida con algunas características nuevas
- ✅ Estructura básica mejorada
- ⚠️ Algunos endpoints de Semana 1 modificados sin necesidad

#### **En Desarrollo (13-17 puntos)**

- ✅ Algunos elementos nuevos implementados
- ⚠️ Organización del código mejorable
- ⚠️ Funcionalidad previa parcialmente afectada

#### **Insuficiente (0-12 puntos)**

- ❌ No demuestra progresión desde Semana 1
- ❌ Código desorganizado o no funcional

### 2. **Implementación de Modelos Pydantic (25 puntos)**

#### **Excelente (23-25 puntos)**

- ✅ Al menos 5 modelos Pydantic bien definidos
- ✅ Validación avanzada con Field() y validators personalizados
- ✅ Response models apropiados para diferentes endpoints
- ✅ Uso correcto de enums y tipos complejos
- ✅ Documentación automática rica y clara

#### **Competente (18-22 puntos)**

- ✅ 3-4 modelos Pydantic implementados
- ✅ Validación básica con Field()
- ✅ Response models para endpoints principales
- ⚠️ Algunos validators o características avanzadas faltantes

#### **En Desarrollo (13-17 puntos)**

- ✅ 2-3 modelos básicos implementados
- ⚠️ Validación mínima o incorrecta
- ⚠️ Response models inconsistentes

#### **Insuficiente (0-12 puntos)**

- ❌ Modelos Pydantic ausentes o no funcionales
- ❌ Sin validación de datos

### 3. **CRUD Completo y Métodos HTTP (20 puntos)**

#### **Excelente (18-20 puntos)**

- ✅ CRUD completo implementado (Create, Read, Update, Delete)
- ✅ Uso correcto de métodos HTTP (GET, POST, PUT, PATCH, DELETE)
- ✅ Status codes apropiados para cada operación
- ✅ Manejo de errores robusto con mensajes claros
- ✅ Operaciones batch o avanzadas implementadas

#### **Competente (14-17 puntos)**

- ✅ CRUD básico funcionando
- ✅ Métodos HTTP principales implementados
- ✅ Status codes mayormente correctos
- ⚠️ Manejo de errores básico

#### **En Desarrollo (10-13 puntos)**

- ✅ Algunas operaciones CRUD funcionando
- ⚠️ Métodos HTTP limitados o incorrectos
- ⚠️ Status codes inconsistentes

#### **Insuficiente (0-9 puntos)**

- ❌ CRUD incompleto o no funcional
- ❌ Métodos HTTP mal implementados

### 4. **Características Avanzadas de FastAPI (15 puntos)**

#### **Excelente (14-15 puntos)**

- ✅ Parámetros de consulta avanzados con validación
- ✅ Búsqueda y filtros implementados
- ✅ Paginación y ordenamiento básicos
- ✅ Middleware custom (timing, CORS, etc.)
- ✅ Headers personalizados y metadata

#### **Competente (11-13 puntos)**

- ✅ Query parameters con validación básica
- ✅ Algunos filtros implementados
- ⚠️ Características avanzadas limitadas

#### **En Desarrollo (8-10 puntos)**

- ✅ Query parameters básicos
- ⚠️ Funcionalidades avanzadas mínimas

#### **Insuficiente (0-7 puntos)**

- ❌ Sin características avanzadas implementadas

### 5. **Type Hints y Async/Await (15 puntos)**

#### **Excelente (14-15 puntos)**

- ✅ Type hints en 95%+ de funciones y variables
- ✅ Al menos 2-3 endpoints async implementados correctamente
- ✅ Uso apropiado de async vs sync según el caso
- ✅ Comprensión clara de cuándo usar cada enfoque

#### **Competente (11-13 puntos)**

- ✅ Type hints en 80%+ del código
- ✅ Al menos 1 endpoint async funcionando
- ⚠️ Uso básico pero correcto de async/await

#### **En Desarrollo (8-10 puntos)**

- ✅ Type hints parciales
- ⚠️ Intento de async/await con errores menores

#### **Insuficiente (0-7 puntos)**

- ❌ Type hints ausentes o incorrectos
- ❌ Sin implementación async o mal hecha

---

## 🎯 **Entregables Requeridos**

### **📦 Entregable Principal: API Evolucionada**

- **Archivo**: `main.py` (evolución de Semana 1)
- **Repositorio**: Actualización del repo de Semana 1
- **Rama**: `semana-2-python-moderno` (recomendado)

### **📄 Documentación Actualizada**

- **README.md** con:
  - Descripción de nuevos endpoints
  - Ejemplos de uso actualizados
  - Instrucciones de testing
  - Reflexión sobre lo aprendido (1-2 párrafos)

### **🧪 Testing Básico (Opcional +5 puntos)**

- **Archivo**: `test_api.py` o script de testing
- **Tests**: Para endpoints principales y validación Pydantic

---

## 📊 **Escala de Calificación**

| Rango      | Nivel             | Descripción                                                       |
| ---------- | ----------------- | ----------------------------------------------------------------- |
| **90-100** | **Excelente**     | Supera expectativas, domina conceptos, implementación profesional |
| **75-89**  | **Competente**    | Cumple objetivos, buena comprensión, implementación sólida        |
| **60-74**  | **En Desarrollo** | Comprensión básica, implementación parcial pero funcional         |
| **50-59**  | **Suficiente**    | Mínimo aceptable, necesita mejoras significativas                 |
| **0-49**   | **Insuficiente**  | No cumple objetivos mínimos, requiere repetir                     |

---

## 🎁 **Oportunidades de Bonus (+5-10 puntos cada una)**

- **Testing Automatizado Completo**: Suite de tests con pytest
- **Documentación Avanzada**: Ejemplos de curl, Postman collection
- **Performance Benchmarking**: Medición de rendimiento async vs sync
- **Manejo de Archivos**: Upload/download de archivos
- **Validación Compleja**: Validators custom avanzados
- **API Versioning**: Implementación de versiones de API
- **Logging Estructurado**: Sistema de logs profesional

---

## 🚨 **Criterios de Descalificación**

- **Código copiado** sin comprensión demostrable
- **API no ejecutable** o con errores críticos
- **Sin progresión** observable desde Semana 1
- **Plagio** de implementaciones externas

---

## 📝 **Método de Evaluación**

### **1. Revisión Automática (40%)**

- Ejecución exitosa de la API
- Endpoints respondiendo correctamente
- Documentación automática funcionando

### **2. Revisión de Código (40%)**

- Calidad y organización del código
- Uso correcto de Pydantic y type hints
- Implementación de características requeridas

### **3. Demo/Explicación (20%)**

- Demo de 5-7 minutos mostrando funcionalidades
- Explicación de decisiones técnicas
- Comprensión de conceptos implementados

---

## 📅 **Cronograma de Evaluación**

- **Entrega**: Final de la sesión de 6 horas
- **Revisión**: 48 horas después de la entrega
- **Feedback**: 72 horas después de la entrega
- **Oportunidad de mejora**: 1 semana (solo para notas <60)

---

## 🎯 **Expectativas Realistas para 6 Horas**

### **Se Espera:**

- ✅ Evolución clara desde Semana 1
- ✅ 3-5 modelos Pydantic básicos pero funcionales
- ✅ CRUD básico con validación
- ✅ Al menos 1 endpoint async
- ✅ Type hints en código principal

### **NO Se Espera:**

- ❌ Arquitectura perfecta
- ❌ Validaciones super complejas
- ❌ Manejo de todos los edge cases
- ❌ Performance optimization avanzada
- ❌ Testing exhaustivo

---

**💡 Nota**: Esta semana evalúa **progresión y aplicación de conceptos**, no perfección. El objetivo es construir sobre la base de Semana 1 con herramientas más robustas.
