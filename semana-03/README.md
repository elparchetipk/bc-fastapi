# Semana 3: Más Métodos HTTP y Manejo de Errores

⏰ **DURACIÓN TOTAL: 6 HORAS EXACTAS**  
📚 **NIVEL: Intermedio (construye sobre Semana 2)**

## 🚨 **IMPORTANTE: Progresión Natural**

Esta semana está diseñada para estudiantes que **ya tienen una API con Pydantic funcionando** (Semana 2). Aprenderemos métodos HTTP adicionales y manejo básico de errores.

- ✅ **Completamente realizable en 6 horas**
- ✅ **Progresión gradual desde Semana 2**
- ✅ **Enfoque en lo práctico y funcional**

## 🎯 Objetivos de la Semana (Fundamentales)

Al finalizar esta semana de 6 horas (incluye break de 30 min), los estudiantes:

1. ✅ **Implementarán endpoints PUT y DELETE básicos**
2. ✅ **Manejarán errores HTTP simples** (404, 400)
3. ✅ **Comprenderán status codes básicos** (200, 201, 404, 400)
4. ✅ **Tendrán CRUD básico funcionando** (Create, Read, Update, Delete)
5. ✅ **Estarán preparados para APIs más robustas**

### ❌ **Lo que NO se espera dominar esta semana**

- REST avanzado y teoría compleja
- Múltiples status codes (solo los básicos)
- Validación compleja con múltiples niveles
- Estructura de proyecto compleja
- Middleware o interceptores

## ⏱️ **Estructura de 6 Horas (Incluye Break de 30 min)**

### **Bloque 1: Endpoints PUT (Actualizar) (75 min)**

- **06-put-endpoints.md**
- Actualizar datos existentes
- Parámetros de ruta + body
- Verificación básica

### **☕ BREAK OBLIGATORIO (30 min)**

- Descanso para asimilar conceptos
- Tiempo para resolver dudas sobre PUT
- Preparación mental para DELETE

### **Bloque 2: Endpoints DELETE (120 min)**

- **07-delete-endpoints.md**
- Eliminar datos
- Manejo de "no encontrado"
- CRUD básico completo

### **Bloque 3: Manejo de Errores Básico (90 min)**

- **08-error-handling.md**
- HTTPException básica
- Status codes esenciales (200, 404, 400)
- Mensajes de error claros

### **Bloque 4: Consolidación CRUD (45 min)**

- Integración de todos los métodos
- Verificación completa
- Preparación de entregable

## 📚 Contenido de la Semana (Solo lo Esencial)

### **🧭 Navegación Ordenada (Seguir este orden)**

1. **[🧭 1-teoria/](./1-teoria/)** - Conceptos HTTP básicos
2. **[💻 2-practica/](./2-practica/)** - Implementación paso a paso
3. **[🎯 3-ejercicios/](./3-ejercicios/)** - Refuerzo práctico
4. **[🚀 4-proyecto/](./4-proyecto/)** - CRUD integrado
5. **[📚 5-recursos/](./5-recursos/)** - Referencias básicas

### 🛠️ **Prácticas (Núcleo de la semana)**

1. **[06-put-endpoints.md](./2-practica/06-put-endpoints.md)** - Actualizar datos
2. **[07-delete-endpoints.md](./2-practica/07-delete-endpoints.md)** - Eliminar datos
3. **[08-error-handling.md](./2-practica/08-error-handling.md)** - Errores básicos

### 📖 **Teoría (Mínima)**

- Métodos HTTP básicos (GET, POST, PUT, DELETE)
- Status codes esenciales
- Conceptos de CRUD

### 🏋️ **Ejercicios (Consolidación)**

- 2 ejercicios de integración CRUD
- Verificación de funcionamiento

## 🚀 **Prerrequisitos (De Semana 2)**

- ✅ API con endpoints POST funcionando
- ✅ Modelos Pydantic básicos implementados
- ✅ Type hints en uso
- ✅ Validación básica funcionando

## 🎯 Criterios de Éxito de la Semana

### ✅ **Criterios de Éxito (Aprobatorio)**

- [ ] Al menos 1 endpoint PUT funcionando
- [ ] Al menos 1 endpoint DELETE funcionando
- [ ] Manejo básico de error 404 (no encontrado)
- [ ] CRUD básico completo (Create, Read, Update, Delete)

### 🌟 **Bonus Opcional (Sin presión)**

- [ ] Múltiples entidades con CRUD
- [ ] Mensajes de error personalizados
- [ ] Status codes adicionales (201, 400)

---

## 📋 Entregables de la Semana

### 🔧 **Entregable Principal (Único Obligatorio)**

**API con CRUD Básico Funcionando**

- ✅ API de Semana 2 + mejoras nuevas
- ✅ Al menos 1 endpoint PUT (actualizar)
- ✅ Al menos 1 endpoint DELETE (eliminar)
- ✅ Manejo básico de errores (404 mínimo)
- ✅ CRUD completo funcionando

### 📄 **Entregable de Documentación (Mínimo)**

**README.md Actualizado**

- ✅ Descripción de todos los endpoints CRUD
- ✅ Ejemplo de uso de PUT y DELETE
- ✅ Reflexión de 2-3 oraciones sobre el progreso

### 🎯 **Formato de Entrega**

1. **Repositorio GitHub actualizado** con:

   - main.py con CRUD completo
   - requirements.txt actualizado
   - README.md con todos los endpoints

2. **Sin video requerido**

### ⏰ **Fecha de Entrega**

- **Al final de la sesión de 6 horas**
- **Entrega inmediata, sin trabajo en casa**

## 📊 Evaluación Simplificada

La evaluación se enfoca en **CRUD funcionando**:

- **Funcionalidad CRUD (80%)**: ¿Funcionan todos los métodos HTTP?
- **Manejo de errores (15%)**: ¿Se maneja al menos el 404?
- **Entrega (5%)**: ¿Está actualizado en GitHub?

### 🏆 Criterio de Aprobación

- **✅ Aprobado**: CRUD completo funcionando + código en GitHub
- **❌ Pendiente**: Apoyo adicional en próxima sesión

## 🎁 Oportunidades de Bonus (Solo si hay tiempo extra)

- **CRUD para múltiples entidades**: +5 puntos
- **Mensajes de error personalizados**: +3 puntos
- **Status codes adicionales**: +2 puntos

## 📅 Cronograma de la Jornada de 6 Horas

| Tiempo      | Actividad                    | Duración | Acumulado |
| ----------- | ---------------------------- | -------- | --------- |
| 9:00-10:15  | Endpoints PUT (actualizar)   | 75 min   | 75 min    |
| 10:15-10:45 | **☕ BREAK OBLIGATORIO**     | 30 min   | 105 min   |
| 10:45-12:45 | Endpoints DELETE + CRUD      | 120 min  | 225 min   |
| 12:45-14:15 | Manejo de errores básico     | 90 min   | 315 min   |
| 14:15-15:00 | Consolidación CRUD y entrega | 45 min   | 360 min   |

**Total**: Exactamente 6 horas (360 minutos)

## 🔍 Estructura de Entrega

### 📁 Estructura Esperada

```
apellido-nombre-semana3/
├── README.md               # Con endpoints CRUD completos
├── requirements.txt        # FastAPI + pydantic + uvicorn
└── main.py                # API con CRUD completo
```

### 🚀 Proceso de Entrega Simple

1. **Evolucionar repositorio existente**

   - Agregar PUT y DELETE a main.py
   - Actualizar README con nuevos endpoints
   - Commit con mensaje descriptivo

2. **Demostración en Clase**

   - Mostrar CRUD completo funcionando
   - Demostrar manejo de error 404
   - Mostrar documentación /docs actualizada

3. **Fecha Límite**
   - **Al final de la clase de 6 horas**
   - **Sin extensiones**

## 🤝 Recursos de Apoyo

### 👥 Ayuda Durante la Clase

- **Instructor**: Disponible durante toda la jornada
- **Compañeros**: Trabajo colaborativo permitido
- **Documentación**: FastAPI docs + HTTP status codes

### 🔧 Herramientas Básicas

- **Mismas herramientas de Semana 2**
- **Postman/Thunder Client**: Para probar PUT y DELETE
- **Browser**: Para ver /docs actualizado con CRUD

## 🎯 Preparación para Semana 4

Con este CRUD básico funcionando, en la Semana 4 aprenderás:

- **Modelos de datos más complejos**: Relaciones básicas
- **Validación avanzada**: Campos opcionales y reglas
- **Filtros y búsquedas**: Query parameters más sofisticados

## 📞 Contacto (Solo Emergencias)

- **Durante la clase**: Levantar la mano o chat
- **Fuera de horario**: No se requiere, todo se resuelve en clase

---

## 🌟 Mensaje de Motivación Final

Esta tercera semana completa tu **conocimiento fundamental de HTTP**. Con CRUD funcionando, tendrás una base sólida para cualquier API más compleja.

**Recuerda**:

- ✅ Construyes sobre el sólido progreso de Semanas 1-2
- ✅ El break de 30 min es obligatorio para asimilar conceptos
- ✅ CRUD es el fundamento de la mayoría de APIs
- ✅ Los conceptos se aplicarán en todas las semanas siguientes

**¡Tu API ya puede hacer todo lo básico! 🚀**
