# Semana 4: Query Parameters y Validación de Datos

⏰ **DURACIÓN TOTAL: 6 HORAS EXACTAS**  
📚 **NIVEL: Intermedio (construye sobre Semana 3)**

## 🚨 **IMPORTANTE: Progresión Natural**

Esta semana está diseñada para estudiantes que **ya tienen una API CRUD completa funcionando** (Semana 3). Aprenderemos query parameters, validación avanzada y filtrado de datos.

- ✅ **Completamente realizable en 6 horas**
- ✅ **Progresión gradual desde Semana 3**
- ✅ **Enfoque en conceptos prácticos y funcionales**

## 🎯 Objetivos de la Semana (Fundamentales)

Al finalizar esta semana de 6 horas (incluye break de 30 min), los estudiantes:

1. ✅ **Implementarán query parameters para filtrado**
2. ✅ **Agregarán validación de datos con Pydantic Field**
3. ✅ **Crearán endpoints de búsqueda con múltiples filtros**
4. ✅ **Manejarán parámetros opcionales y valores por defecto**
5. ✅ **Estarán preparados para funcionalidades más avanzadas de API**

### ❌ **Lo que NO se espera dominar esta semana**

- Integración con bases de datos (SQLAlchemy)
- Migraciones complejas o conceptos ORM
- Autenticación avanzada
- Subida de archivos o manejo complejo de media
- Despliegue en producción

## ⏱️ **Estructura de 6 Horas (Incluye Break de 30 min)**

### **Bloque 1: Query Parameters Básicos (75 min)**

- **10-query-parameters.md**
- Filtrado básico con query params
- Parámetros opcionales con valores por defecto
- Conversión de tipos y validación

### **☕ BREAK OBLIGATORIO (30 min)**

- Descanso para asimilar conceptos de query parameters
- Tiempo para resolver dudas sobre filtrado
- Preparación mental para validación

### **Bloque 2: Validación Avanzada (120 min)**

- **11-pydantic-validation.md**
- Validación de campos con restricciones
- Validadores personalizados
- Manejo de errores para datos inválidos

### **Bloque 3: Búsqueda y Filtrado (90 min)**

- **12-search-endpoints.md**
- Combinaciones de múltiples filtros
- Búsqueda por texto y rangos
- Conceptos básicos de paginación

### **Bloque 4: Procesamiento de Datos (45 min)**

- Integración de todos los conceptos
- API completa con funcionalidades avanzadas
- Preparación de entregable

## 📚 Contenido de la Semana (Solo lo Esencial)

### **🧭 Navegación Ordenada (Seguir este orden)**

1. **[🧭 1-teoria/](./1-teoria/)** - Conceptos de query parameters y validación
2. **[💻 2-practica/](./2-practica/)** - Implementación paso a paso
3. **[🎯 3-ejercicios/](./3-ejercicios/)** - Refuerzo práctico
4. **[🚀 4-proyecto/](./4-proyecto/)** - API avanzada con filtrado
5. **[📚 5-recursos/](./5-recursos/)** - Referencias básicas

### 🛠️ **Prácticas (Núcleo de la semana)**

1. **[10-query-parameters.md](./2-practica/10-query-parameters.md)** - Filtrado básico
2. **[11-pydantic-validation.md](./2-practica/11-pydantic-validation.md)** - Validación de datos
3. **[12-search-endpoints.md](./2-practica/12-search-endpoints.md)** - Funcionalidad de búsqueda

### 📖 **Teoría (Mínima)**

- Fundamentos de query parameters
- Validación con Pydantic Field
- Conceptos básicos de filtrado

### 🏋️ **Ejercicios (Consolidación)**

- 2 ejercicios sobre filtrado y validación
- Verificación de funcionalidad

## 🚀 **Prerrequisitos (De Semana 3)**

- ✅ API CRUD completa funcionando
- ✅ Manejo de errores con HTTPException
- ✅ Modelos Pydantic implementados
- ✅ Todos los métodos HTTP funcionando

## 🎯 Criterios de Éxito de la Semana

### ✅ **Criterios de Éxito (Aprobatorio)**

- [ ] Al menos 2 query parameters funcionando para filtrado
- [ ] Validación de campos con Pydantic Field implementada
- [ ] Endpoint de búsqueda con filtrado por texto
- [ ] Manejo apropiado de parámetros opcionales

### 🌟 **Bonus Opcional (Sin presión)**

- [ ] Implementación de paginación
- [ ] Filtrado por rangos (fechas, números)
- [ ] Combinación de múltiples criterios de búsqueda

---

## 📋 Entregables de la Semana

### 🔧 **Entregable Principal (Único Obligatorio)**

**API con Funcionalidades Avanzadas de Query**

- ✅ API de Semana 3 + nuevas funcionalidades de query
- ✅ Al menos 2 query parameters para filtrado
- ✅ Validación de campos con restricciones
- ✅ Endpoint de búsqueda con filtrado por texto
- ✅ Manejo apropiado de errores para queries inválidas

### 📄 **Entregable de Documentación (Mínimo)**

**README.md Actualizado**

- ✅ Descripción de todos los query parameters
- ✅ Ejemplos de uso de filtrado y búsqueda
- ✅ Reflexión de 2-3 oraciones sobre el progreso

### 🎯 **Formato de Entrega**

1. **Repositorio GitHub actualizado** con:

   - main.py con query parameters
   - requirements.txt actualizado
   - README.md con todas las opciones de filtrado

2. **Sin video requerido**

### ⏰ **Fecha de Entrega**

- **Al final de la sesión de 6 horas**
- **Entrega inmediata, sin trabajo en casa**

## 📊 Evaluación Simplificada

La evaluación se enfoca en **funcionalidad de query**:

- **Query Parameters (50%)**: ¿Funcionan los parámetros de filtrado?
- **Validación (30%)**: ¿Está implementada la validación Field?
- **Búsqueda (15%)**: ¿Funciona la búsqueda por texto?
- **Entrega (5%)**: ¿Está actualizado en GitHub?

### 🏆 Criterio de Aprobación

- **✅ Aprobado**: Query parameters + validación funcionando + código en GitHub
- **❌ Pendiente**: Apoyo adicional en próxima sesión

## 🎁 Oportunidades de Bonus (Solo si hay tiempo extra)

- **Implementación de paginación**: +5 puntos
- **Filtrado por rangos**: +3 puntos
- **Combinaciones avanzadas de búsqueda**: +2 puntos

## 📅 Cronograma de la Jornada de 6 Horas

| Tiempo      | Actividad                | Duración | Acumulado |
| ----------- | ------------------------ | -------- | --------- |
| 9:00-10:15  | Query parameters básicos | 75 min   | 75 min    |
| 10:15-10:45 | **☕ BREAK OBLIGATORIO** | 30 min   | 105 min   |
| 10:45-12:45 | Validación avanzada      | 120 min  | 225 min   |
| 12:45-14:15 | Endpoints de búsqueda    | 90 min   | 315 min   |
| 14:15-15:00 | Integración y entrega    | 45 min   | 360 min   |

**Total**: Exactamente 6 horas (360 minutos)

## 🔍 Estructura de Entrega

### 📁 Estructura Esperada

```
apellido-nombre-semana4/
├── README.md               # Con documentación de query parameters
├── requirements.txt        # FastAPI + pydantic + uvicorn
└── main.py                # API con query parameters y validación
```

### 🚀 Proceso de Entrega Simple

1. **Evolucionar repositorio existente**

   - Agregar query parameters a main.py
   - Actualizar README con ejemplos de filtrado
   - Commit con mensaje descriptivo

2. **Demostración en Clase**

   - Mostrar filtrado funcionando
   - Demostrar errores de validación
   - Mostrar /docs actualizado con query params

3. **Fecha Límite**
   - **Al final de la clase de 6 horas**
   - **Sin extensiones**

## 🤝 Recursos de Apoyo

### 👥 Ayuda Durante la Clase

- **Instructor**: Disponible durante toda la jornada
- **Compañeros**: Trabajo colaborativo permitido
- **Documentación**: FastAPI docs + Pydantic Field docs

### 🔧 Herramientas Básicas

- **Mismas herramientas de Semana 3**
- **Postman/Thunder Client**: Para probar query parameters
- **Browser**: Para ver /docs actualizado con filtros

## 🎯 Preparación para Semana 5

Con esta API avanzada funcionando, en la Semana 5 aprenderás:

- **Conceptos básicos de seguridad**: Autenticación simple
- **Protección de endpoints**: API keys básicas
- **Manejo de usuarios**: Conceptos fundamentales

## 📞 Contacto (Solo Emergencias)

- **Durante la clase**: Levantar la mano o chat
- **Fuera de horario**: No se requiere, todo se resuelve en clase

---

## 🌟 Mensaje de Motivación Final

Esta cuarta semana completa tu **conocimiento fundamental de APIs**. Con query parameters y validación, tendrás una base de API de nivel profesional.

**Recuerda**:

- ✅ Construyes sobre el sólido progreso de Semanas 1-3
- ✅ El break de 30 min es obligatorio para asimilar conceptos
- ✅ Los query parameters se usan en la mayoría de APIs del mundo real
- ✅ Estos conceptos se aplicarán en todas las semanas siguientes

**¡Tu API ahora es inteligente y flexible! 🚀**
