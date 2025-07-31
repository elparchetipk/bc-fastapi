# RÚBRICA DE EVALUACIÓN - SEMANA 1

## FastAPI Fundamentals

### INFORMACIÓN GENERAL

- **Semana**: 1
- **Tema**: FastAPI Fundamentals - Environment Setup & First API
- **Duración**: 6 horas (incluye break de 30 min)
- **Modalidad**: Evaluación automática por IA + revisión manual

### CRITERIOS DE EVALUACIÓN

#### 1. SETUP DEL ENTORNO (25 puntos)

**Evidencia requerida**: Archivo `requirements.txt` y entorno funcional

| Criterio                 | Excelente (5pts)                                | Bueno (4pts)                      | Suficiente (3pts)                   | Insuficiente (0pts)            |
| ------------------------ | ----------------------------------------------- | --------------------------------- | ----------------------------------- | ------------------------------ |
| **Virtual Environment**  | Entorno virtual creado y activado correctamente | Entorno creado con documentación  | Entorno funcional básico            | No hay entorno virtual         |
| **Dependencies**         | requirements.txt completo con versiones         | requirements.txt básico           | Dependencias instaladas sin archivo | No hay gestión de dependencias |
| **FastAPI Installation** | FastAPI + uvicorn instalados y funcionando      | FastAPI instalado correctamente   | Instalación básica funcional        | FastAPI no instalado           |
| **Testing Tools**        | Postman/Thunder Client configurado              | Herramienta de testing disponible | Browser testing únicamente          | No hay herramientas de testing |
| **Documentation**        | README con setup detallado                      | README básico con instrucciones   | Documentación mínima                | Sin documentación              |

#### 2. HELLO WORLD API (25 puntos)

**Evidencia requerida**: Archivo `main.py` con API básica funcionando

| Criterio                 | Excelente (5pts)                     | Bueno (4pts)                   | Suficiente (3pts)             | Insuficiente (0pts)       |
| ------------------------ | ------------------------------------ | ------------------------------ | ----------------------------- | ------------------------- |
| **FastAPI App Creation** | App inicializada con configuraciones | App inicializada correctamente | App básica funcional          | App no inicializada       |
| **Hello World Endpoint** | GET / con respuesta personalizada    | GET / funcional                | Endpoint básico funcional     | Endpoint no funciona      |
| **Additional Endpoint**  | GET /hello/{name} implementado       | Endpoint adicional funcional   | Intento de endpoint adicional | Sin endpoints adicionales |
| **Server Startup**       | uvicorn corriendo sin errores        | Servidor funcional             | Servidor inicia con warnings  | Servidor no inicia        |
| **Response Format**      | JSON bien formateado y consistente   | Respuestas JSON válidas        | Respuestas básicas            | Respuestas malformadas    |

#### 3. TESTING Y VERIFICACIÓN (25 puntos)

**Evidencia requerida**: Capturas de pantalla o documentación de testing

| Criterio                 | Excelente (5pts)                    | Bueno (4pts)                       | Suficiente (3pts)          | Insuficiente (0pts)         |
| ------------------------ | ----------------------------------- | ---------------------------------- | -------------------------- | --------------------------- |
| **Manual Testing**       | Múltiples endpoints testeados       | Endpoints principales testeados    | Testing básico realizado   | No hay evidencia de testing |
| **Documentation Access** | /docs y /redoc funcionando          | Documentación automática accesible | Docs básicamente funcional | Documentación no accesible  |
| **Error Handling**       | Manejo básico de errores 404        | Algunos errores manejados          | Errores reconocidos        | Sin manejo de errores       |
| **Response Validation**  | Respuestas validadas y documentadas | Respuestas verificadas             | Verificación básica        | Sin validación              |
| **Browser Testing**      | Testing en browser documentado      | Browser testing realizado          | Acceso básico por browser  | Sin testing en browser      |

#### 4. ENTREGABLES (15 puntos)

**Evidencia requerida**: Repositorio GitHub con código y documentación

| Criterio                 | Excelente (3pts)                              | Bueno (2pts)                  | Suficiente (1pt)            | Insuficiente (0pts)         |
| ------------------------ | --------------------------------------------- | ----------------------------- | --------------------------- | --------------------------- |
| **GitHub Repository**    | Repo bien organizado con commits descriptivos | Repo funcional con código     | Código subido básicamente   | Sin repositorio             |
| **README Documentation** | README completo con instrucciones de uso      | README con información básica | README mínimo               | Sin README                  |
| **Code Organization**    | Código limpio y bien comentado                | Código organizado             | Código funcional básico     | Código desorganizado        |
| **Requirements File**    | requirements.txt completo y actualizado       | requirements.txt básico       | Lista de dependencias       | Sin gestión de dependencias |
| **Delivery Timeliness**  | Entregado a tiempo con calidad                | Entregado a tiempo            | Entregado con retraso menor | Entregado fuera de plazo    |

#### 5. COMPRENSIÓN CONCEPTUAL (10 puntos)

**Evidencia requerida**: Reflexión escrita en README o comentarios en código

| Criterio                  | Excelente (2pts)                         | Bueno (1.5pts)                | Suficiente (1pt)         | Insuficiente (0pts)        |
| ------------------------- | ---------------------------------------- | ----------------------------- | ------------------------ | -------------------------- |
| **FastAPI Understanding** | Comprende ventajas y conceptos básicos   | Entiende propósito de FastAPI | Conocimiento básico      | No demuestra comprensión   |
| **API Concepts**          | Explica qué es una API y REST básico     | Comprende concepto de API     | Conocimiento superficial | Sin comprensión conceptual |
| **HTTP Methods**          | Entiende GET y diferencias básicas       | Conoce método GET             | Uso básico de HTTP       | Sin comprensión HTTP       |
| **Development Process**   | Reflexiona sobre proceso de desarrollo   | Documenta pasos seguidos      | Menciona experiencia     | Sin reflexión              |
| **Next Steps**            | Identifica próximos pasos de aprendizaje | Muestra interés en continuar  | Comprende progresión     | Sin visión de continuidad  |

### ESCALA DE CALIFICACIÓN

- **Excelente (90-100 pts)**: Dominio completo de conceptos fundamentales
- **Bueno (80-89 pts)**: Comprensión sólida con implementación correcta
- **Suficiente (70-79 pts)**: Conceptos básicos logrados, necesita refuerzo
- **Insuficiente (0-69 pts)**: Requiere repetir contenidos fundamentales

### CRITERIOS DE APROBACIÓN

- **Mínimo para aprobar**: 70 puntos (70%)
- **Entregables obligatorios**:
  - API funcionando con al menos 1 endpoint
  - Código en GitHub
  - README con instrucciones básicas

### RETROALIMENTACIÓN AUTOMÁTICA

**Para el agente evaluador de IA:**

#### Puntos de verificación automática:

1. **Estructura de archivos**: Verificar existencia de main.py, requirements.txt, README.md
2. **Sintaxis de código**: Validar que el código de Python es sintácticamente correcto
3. **Importaciones**: Verificar que FastAPI está importado correctamente
4. **Endpoints**: Confirmar que existe al menos un endpoint GET funcional
5. **Documentación**: Verificar que README contiene información básica del proyecto

#### Indicadores de calidad:

- Uso de nombres descriptivos en funciones y variables
- Comentarios explicativos en código complejo
- Estructura consistente en respuestas JSON
- Manejo de casos básicos (rutas, parámetros)

#### Señales de alarma para revisión manual:

- Código excesivamente complejo para el nivel
- Uso de librerías no enseñadas en la semana
- Falta de documentación mínima
- Errores de sintaxis o imports faltantes
- Entrega incompleta o fuera de especificaciones

### RECURSOS PARA ESTUDIANTES

- Documentación oficial FastAPI: https://fastapi.tiangolo.com/
- Guía de setup de entorno de la semana
- Ejemplos de código proporcionados en prácticas
- Canal de ayuda para dudas técnicas

**Fecha de creación**: 25 de julio de 2025  
**Versión**: 1.0  
**Próxima revisión**: Al finalizar implementación del bootcamp
