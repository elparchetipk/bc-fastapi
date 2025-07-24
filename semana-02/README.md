# Semana 2: Python Moderno para APIs

⏰ **DURACIÓN TOTAL: 6 HORAS EXACTAS**  
📚 **NIVEL: Intermedio (construye sobre Semana 1)**  
🔄 **INCLUYE**: Contenido avanzado movido desde Semana 1

## 🎯 Objetivos de la Semana

Con la base sólida de la Semana 1 (API funcionando), ahora profundizaremos en Python moderno y conceptos esenciales para APIs profesionales.

Al finalizar esta semana de 6 horas, los estudiantes:

1. ✅ **Dominarán type hints esenciales** para APIs robustas
2. ✅ **Comprenderán fundamentos de Pydantic** para validación de datos
3. ✅ **Manejarán conceptos básicos de async/await** en FastAPI
4. ✅ **Implementarán validación avanzada** en sus APIs
5. ✅ **Tendrán una API más robusta y profesional**

## ⏱️ **Estructura de 6 Horas**

### **Bloque 1: Python Fundamentals Modernos (120 min)**

- **03-python-fundamentals.md** (movido de Semana 1)
- Type hints esenciales
- Funciones avanzadas y decoradores
- Manejo de errores Python

### **Bloque 2: Fundamentos Pydantic (120 min)**

- **05-pydantic-essentials.md** (nuevo)
- Modelos de datos básicos
- Validación automática
- Serialización/deserialización

### **Bloque 3: FastAPI Intermedio (90 min)**

- **04-fastapi-basics.md** (movido y adaptado de Semana 1)
- Múltiples métodos HTTP
- Parámetros de consulta avanzados
- Response models

### **Bloque 4: Async y Consolidación (90 min)**

- **06-async-basics.md** (nuevo)
- Conceptos async/await básicos
- Cuándo usar sync vs async
- Práctica consolidada

## 🚀 **Prerrequisitos (De Semana 1)**

- ✅ Entorno FastAPI funcionando
- ✅ API Hello World completada
- ✅ Familiaridad con endpoints básicos
- ✅ Git configurado y funcionando

## 📋 **Entregables de la Semana**

### **🔧 Entregable Principal: API Mejorada**

**Archivo**: `main.py` (evolución de Semana 1)

**Nuevas características esperadas**:

- ✅ **Modelos Pydantic** para validación de datos
- ✅ **Type hints** en todas las funciones
- ✅ **Validación avanzada** con mensajes de error claros
- ✅ **Al menos 8-10 endpoints** con diferentes métodos HTTP
- ✅ **Response models** definidos
- ✅ **Manejo de errores** robusto

### **📄 Entregable de Documentación**

**README.md actualizado** con:

- ✅ Descripción de nuevos endpoints
- ✅ Ejemplos de uso con curl/requests
- ✅ Documentación de modelos de datos
- ✅ Instrucciones de testing

### **🧪 Entregable de Testing (Opcional)**

**tests/test_api.py** básico:

- ✅ Tests para endpoints principales
- ✅ Validación de modelos Pydantic
- ✅ Casos de error esperados

## ⏰ **Cronograma Detallado**

| Tiempo      | Actividad                    | Archivo/Recurso                 |
| ----------- | ---------------------------- | ------------------------------- |
| 0-120 min   | Python Fundamentals Modernos | `03-python-fundamentals.md`     |
| 120-240 min | Fundamentos Pydantic         | `05-pydantic-essentials.md`     |
| 240-330 min | FastAPI Intermedio           | `04-fastapi-basics.md`          |
| 330-420 min | Async Basics + Consolidación | `06-async-basics.md` + Práctica |

## 🎯 **Criterios de Éxito**

### **Mínimo Aceptable (70/100)**:

- ✅ Al menos 5 modelos Pydantic funcionando
- ✅ Type hints en 80% de las funciones
- ✅ API con 8+ endpoints operativos
- ✅ Validación básica implementada

### **Logro Esperado (85/100)**:

- ✅ Todo lo anterior +
- ✅ Manejo de errores con mensajes personalizados
- ✅ Response models bien definidos
- ✅ Documentación clara y completa
- ✅ Al menos 1 endpoint async funcionando

### **Excelencia (95/100)**:

- ✅ Todo lo anterior +
- ✅ Testing básico implementado
- ✅ Código limpio y bien estructurado
- ✅ Uso avanzado de Pydantic (validators, aliases)
- ✅ Performance considerada en endpoints async

## 🚫 **Lo que NO se evalúa esta semana**

Para mantener el enfoque:

- ❌ **Bases de datos** → Semana 5-6
- ❌ **Autenticación** → Semana 7
- ❌ **Deployment** → Semana 9-10
- ❌ **Testing avanzado** → Semana 8
- ❌ **Middleware personalizado** → Semana 11-12

## 📚 **Recursos de Apoyo**

### **Documentación Esencial**

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [FastAPI Advanced Tutorial](https://fastapi.tiangolo.com/advanced/)
- [Python Async/Await](https://docs.python.org/3/library/asyncio.html)

### **Comandos de Referencia**

```bash
# Ejecutar con recarga automática
uvicorn main:app --reload

# Testing básico (si implementado)
python -m pytest tests/ -v

# Verificar tipos (si instalado mypy)
mypy main.py

# Instalar dependencias adicionales
pip install "pydantic[email]" pytest httpx
```

## 🔄 **Conexión con Semana 3**

Esta semana prepara el camino para:

- ✅ **Endpoints más complejos** (CRUD completo)
- ✅ **Integración con bases de datos** (usando modelos Pydantic)
- ✅ **APIs más robustas** (con validación sólida)
- ✅ **Mejor arquitectura** (separación de concerns)

## 🆘 **Problemas Comunes y Soluciones**

### **Error: "Type hints not working"**

```bash
# Verificar versión de Python
python --version  # Debe ser 3.8+

# Instalar mypy para verificación
pip install mypy
mypy main.py
```

### **Error: "Pydantic validation failing"**

```python
# Debug de validación
from pydantic import ValidationError

try:
    model = MiModelo(**datos)
except ValidationError as e:
    print(e.json())
```

### **Error: "Async function not working"**

```python
# Verificar que uvicorn soporta async
# Usar async solo cuando sea necesario
# Mantener funciones simples como sync
```

## 📝 **Método de Entrega**

1. **Actualizar repositorio de Semana 1**
2. **Crear nueva rama**: `semana-2-python-moderno`
3. **Evolucionar el código existente** (no empezar de cero)
4. **Documentar los cambios** en commit messages claros
5. **Crear PR** con descripción de mejoras implementadas

## 🏆 **Celebración del Progreso**

Al final de esta semana, habrás:

- 🎯 **Duplicado la funcionalidad** de tu API
- 🛡️ **Añadido validación robusta** con Pydantic
- 🔧 **Implementado mejores prácticas** de Python moderno
- 🚀 **Preparado la base** para características avanzadas

**¡Estás construyendo una API de calidad profesional paso a paso!**

---

## 📋 **Checklist de Preparación**

Antes de comenzar la Semana 2, verifica:

- [ ] ✅ Semana 1 completada exitosamente
- [ ] ✅ API básica funcionando desde Semana 1
- [ ] ✅ Entorno virtual activo y configurado
- [ ] ✅ Git repository con código de Semana 1
- [ ] ✅ FastAPI y dependencias actualizadas

**¡Listo para llevar tu API al siguiente nivel! 🚀**

## 📚 Contenido de la Semana

### **📋 Navegación Ordenada (Seguir este orden)**

1. **[🧭 1-teoria/](./1-teoria/)** - Conceptos fundamentales
2. **[💻 2-practica/](./2-practica/)** - Implementación guiada
3. **[🎯 3-ejercicios/](./3-ejercicios/)** - Refuerzo y práctica
4. **[🚀 4-proyecto/](./4-proyecto/)** - Aplicación integradora
5. **[📚 5-recursos/](./5-recursos/)** - Referencias y apoyo

### 🛠️ **Prácticas Principales**

1. **[03-python-fundamentals.md](./2-practica/03-python-fundamentals.md)** - Python moderno (120 min)
2. **[05-pydantic-essentials.md](./2-practica/05-pydantic-essentials.md)** - Validación de datos (120 min)
3. **[04-fastapi-intermedio.md](./2-practica/04-fastapi-intermedio.md)** - APIs avanzadas (90 min)
4. **[06-async-basics.md](./2-practica/06-async-basics.md)** - Async/await básico (90 min)
