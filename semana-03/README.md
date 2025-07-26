# Semana 3: Validación y Estructura REST

⏰ **DURACIÓN TOTAL: 6 HORAS EXACTAS**  
📚 **NIVEL: Intermedio (construye sobre Semanas 1 y 2)**

## 🚨 **IMPORTANTE: Aplicando Conceptos Aprendidos**

Esta semana está diseñada para estudiantes que **ya tienen una API funcional con Pydantic** (Semanas 1-2). Aplicaremos validación de datos y estructura REST básica.

- ✅ **Completamente realizable en 6 horas**
- ✅ **Enfoque práctico en validación y errores**
- ✅ **Preparación para APIs más estructuradas**

## 🎯 Objetivos de la Semana (Fundamentales)

Al finalizar esta semana de 6 horas (incluye break de 30 min), los estudiantes:

1. ✅ **Implementarán validación de datos** con Pydantic de forma efectiva
2. ✅ **Manejarán errores básicos** con HTTPException
3. ✅ **Crearán endpoints CRUD completos** (GET, POST, PUT, DELETE)
4. ✅ **Estructurarán código** de manera organizada
5. ✅ **Aplicarán principios REST básicos**

### ❌ **Lo que NO se espera dominar esta semana**

- Autenticación y autorización
- Bases de datos complejas
- Middleware personalizado
- Testing automatizado avanzado
- Arquitecturas complejas

## ⏱️ **Estructura de 6 Horas (Incluye Break de 30 min)**

### **Bloque 1: Validación con Pydantic (75 min)**

- **08-validacion-avanzada.md**
- Validadores personalizados básicos
- Field constraints simples
- Verificación de funcionamiento

### **☕ BREAK OBLIGATORIO (30 min)**

- Descanso para asimilar validaciones
- Tiempo para resolver dudas sobre Pydantic
- Preparación mental para manejo de errores

### **Bloque 2: Manejo de Errores Básico (120 min)**

- **09-manejo-errores.md**
- HTTPException básica
- Status codes apropiados
- Responses de error consistentes

### **Bloque 3: Estructura REST y CRUD (90 min)**

- **10-estructura-rest.md**
- Endpoints CRUD organizados
- Principios REST básicos
- Organización de código

### **Bloque 4: Consolidación y Proyecto (45 min)**

- Integración de conceptos
- Inicio del proyecto integrador
- Preparación de entregable

## 📚 Contenido de la Semana

### **📋 Navegación Ordenada (Seguir este orden)**

1. **[🧭 1-teoria/](./1-teoria/)** - Conceptos fundamentales
2. **[💻 2-practica/](./2-practica/)** - Implementación guiada
3. **[🎯 3-ejercicios/](./3-ejercicios/)** - Refuerzo y práctica
4. **[🚀 4-proyecto/](./4-proyecto/)** - Aplicación integradora
5. **[📚 5-recursos/](./5-recursos/)** - Referencias y apoyo

### **🧭 Teoría**

- [📖 Conceptos REST y HTTP](./1-teoria/rest-http-concepts.md)

### **💻 Prácticas**

1. [✅ Validación con Pydantic](./2-practica/08-validacion-avanzada.md) _(75 min)_
2. [⚠️ Manejo de Errores Básico](./2-practica/09-manejo-errores.md) _(120 min)_
3. [🏗️ Estructura REST](./2-practica/10-estructura-rest.md) _(90 min)_

### **💪 Ejercicios**

- [🎯 Ejercicios de Refuerzo](./3-ejercicios/ejercicios-practica.md)

### **🚀 Proyecto**

- [📋 API de Inventario Simple](./4-proyecto/especificacion-proyecto.md)

### **📚 Recursos**

- [🔗 Enlaces y Referencias](./5-recursos/recursos-apoyo.md)

## 🎯 Objetivos Específicos

### **Conocimientos**

- ✅ Validación básica con Pydantic
- ✅ Manejo de errores con HTTPException
- ✅ Status codes HTTP apropiados
- ✅ Principios REST básicos

### **Habilidades**

- ✅ Implementar validadores personalizados simples
- ✅ Crear endpoints CRUD organizados
- ✅ Manejar errores de forma consistente
- ✅ Estructurar código de API básica

### **Actitudes**

- ✅ Escritura de código limpio y organizado
- ✅ Atención al detalle en validación
- ✅ Responsabilidad en manejo de errores

## 📋 Prerrequisitos

### **Obligatorios**

- ✅ **Semana 1 completada**: API básica funcionando
- ✅ **Semana 2 completada**: Modelos Pydantic + type hints
- ✅ Python 3.8+ con entorno virtual
- ✅ FastAPI, Uvicorn instalados

### **Recomendados**

- 📖 Comprensión básica de HTTP
- 🌐 Experiencia con APIs simples
- 🧪 Familiaridad con herramientas básicas (curl, Postman)

## 🎯 Entregables de la Semana

### **📤 Entrega Principal**

**API de Inventario Simple** - Due: Final de Semana 3

**Componentes obligatorios:**

- ✅ **CRUD básico** para productos
- ✅ **Validación simple** con Pydantic
- ✅ **Manejo de errores** básico
- ✅ **Documentación automática** funcional
- ✅ **Código organizado** y limpio

### **📁 Estructura de Entrega**

```text
estudiante-nombre/
├── main.py                 # API principal
├── models.py              # Modelos Pydantic
├── routers/
│   └── products.py        # Endpoints organizados
├── requirements.txt        # Dependencias
└── README.md              # Documentación
```

## 📊 Evaluación

### **Rúbrica de Evaluación** → [📋 Ver Rúbrica Completa](./RUBRICA_SEMANA_3.md)

| Criterio               | Peso | Descripción                     |
| ---------------------- | ---- | ------------------------------- |
| **Funcionalidad CRUD** | 30%  | Endpoints básicos y funcionales |
| **Validación**         | 25%  | Validación simple de datos      |
| **Manejo Errores**     | 20%  | Responses apropiados y básicos  |
| **Estructura Código**  | 15%  | Organización y claridad         |
| **Documentación**      | 10%  | README y comentarios            |

## 🔄 Continuidad del Aprendizaje

### **🔗 Conexión con Semanas Anteriores**

- **Semana 1**: Usa la API básica como foundation
- **Semana 2**: Aplica modelos Pydantic y async

### **🚀 Preparación para Semanas Siguientes**

- **Semana 4**: Bases de datos y persistencia
- **Semana 5**: Autenticación básica

## 🆘 Soporte y Recursos

### **Durante la Semana**

- 💬 **Foro del curso**: Preguntas y discusiones
- 🎥 **Office hours**: Martes y jueves 19:00-20:00
- 📧 **Email instructor**: consultas específicas

### **Recursos Adicionales**

- 📖 [FastAPI Documentation](https://fastapi.tiangolo.com/)
- 🌐 [HTTP Status Codes Reference](https://httpstatuses.com/)
- 🔧 [Postman Learning Center](https://learning.postman.com/)

---

## 📝 Notas Importantes

> ⚠️ **Tiempo límite estricto**: 6 horas de trabajo efectivo
>
> ✅ **Enfoque en calidad** sobre cantidad
>
> 🎯 **Cada bloque es independiente** pero se complementan
>
> 📋 **Entrega obligatoria** para continuar a Semana 4

---

_Última actualización: 26 de julio de 2025_  
_Bootcamp FastAPI - EPTI Development_
