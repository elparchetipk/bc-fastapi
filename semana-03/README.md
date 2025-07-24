# Semana 3: FastAPI Intermedio

## 🎯 Objetivos de la Semana

Al finalizar esta semana, los estudiantes podrán:

- **Implementar endpoints HTTP completos** (GET, POST, PUT, DELETE) con FastAPI
- **Manejar parámetros** de ruta, query y cuerpo de manera profesional
- **Aplicar validación robusta** en todos los endpoints
- **Gestionar errores** de manera consistente y profesional
- **Estructurar APIs** siguiendo mejores prácticas REST

## ⏱️ Distribución de Tiempo (6 horas total)

| Bloque | Actividad                | Tiempo | Descripción                            |
| ------ | ------------------------ | ------ | -------------------------------------- |
| **1**  | Endpoints HTTP Completos | 90 min | GET, POST, PUT, DELETE + parámetros    |
| **2**  | Validación Avanzada      | 90 min | Path, Query, Body validation           |
| **3**  | Manejo de Errores        | 90 min | HTTPException, status codes, responses |
| **4**  | Estructura REST          | 90 min | Best practices, organización código    |

## 📚 Contenido de la Semana

### **🧭 Teoría**

- [📖 Conceptos REST y HTTP](./teoria/rest-http-concepts.md)

### **💻 Prácticas**

1. [🔧 Endpoints HTTP Completos](./practica/07-endpoints-http-completos.md) _(90 min)_
2. [✅ Validación Avanzada](./practica/08-validacion-avanzada.md) _(90 min)_
3. [⚠️ Manejo de Errores](./practica/09-manejo-errores.md) _(90 min)_
4. [🏗️ Estructura REST](./practica/10-estructura-rest.md) _(90 min)_

### **💪 Ejercicios**

- [🎯 Ejercicios de Refuerzo](./ejercicios/ejercicios-practica.md)

### **🚀 Proyecto**

- [📋 API de Inventario Simple](./proyecto/especificacion-proyecto.md)

### **📚 Recursos**

- [🔗 Enlaces y Referencias](./recursos/recursos-apoyo.md)

## 🎯 Objetivos Específicos

### **Conocimientos**

- ✅ Métodos HTTP y cuándo usarlos
- ✅ Tipos de parámetros en FastAPI
- ✅ Status codes HTTP apropiados
- ✅ Principios REST básicos

### **Habilidades**

- ✅ Implementar CRUD completo
- ✅ Validar datos de entrada robustamente
- ✅ Manejar errores consistentemente
- ✅ Estructurar código de manera profesional

### **Actitudes**

- ✅ Escritura de código limpio y mantenible
- ✅ Atención al detalle en validación
- ✅ Responsabilidad en manejo de errores

## 📋 Prerrequisitos

### **Obligatorios**

- ✅ **Semana 1 completada**: API básica funcionando
- ✅ **Semana 2 completada**: Modelos Pydantic + async
- ✅ Python 3.8+ con entorno virtual
- ✅ FastAPI, Uvicorn instalados

### **Recomendados**

- 📖 Conocimiento básico de REST
- 🌐 Experiencia con APIs web
- 🧪 Familiaridad con herramientas de testing (Postman, curl)

## 🎯 Entregables de la Semana

### **📤 Entrega Principal**

**API de Inventario Simple** - Due: Final de Semana 3

**Componentes obligatorios:**

- ✅ **CRUD completo** para productos
- ✅ **Validación robusta** en todos endpoints
- ✅ **Manejo de errores** consistente
- ✅ **Documentación automática** funcional
- ✅ **Código estructurado** profesionalmente

### **📁 Estructura de Entrega**

```
estudiante-nombre/
├── main.py                 # API principal
├── models/
│   └── product_models.py   # Modelos Pydantic
├── routes/
│   └── product_routes.py   # Endpoints organizados
├── utils/
│   └── error_handlers.py   # Manejo de errores
├── requirements.txt        # Dependencias
└── README.md              # Documentación
```

## 📊 Evaluación

### **Rúbrica de Evaluación** → [📋 Ver Rúbrica Completa](./RUBRICA_SEMANA_3.md)

| Criterio               | Peso | Descripción                         |
| ---------------------- | ---- | ----------------------------------- |
| **Funcionalidad CRUD** | 30%  | Endpoints completos y funcionales   |
| **Validación**         | 25%  | Validación robusta de datos         |
| **Manejo Errores**     | 20%  | Responses apropiados y consistentes |
| **Estructura Código**  | 15%  | Organización y claridad             |
| **Documentación**      | 10%  | README y comentarios                |

## 🔄 Continuidad del Aprendizaje

### **🔗 Conexión con Semanas Anteriores**

- **Semana 1**: Usa la API básica como foundation
- **Semana 2**: Aplica modelos Pydantic y async

### **🚀 Preparación para Semanas Siguientes**

- **Semana 4**: Modelos y validación avanzada
- **Semana 5**: Integración con base de datos

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

_Última actualización: 24 de julio de 2025_  
_Bootcamp FastAPI - EPTI Development_
