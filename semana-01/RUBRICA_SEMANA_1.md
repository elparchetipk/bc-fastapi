# Rúbrica de Evaluación - Semana 1: Fundamentos de FastAPI

## 📋 Información General

**Modalidad**: Evaluación integral por proyecto  
**Peso en el curso**: 15% de la nota final  
**Método de evaluación**: Automatizada + Revisión por IA  
**Escala**: 0-100 puntos

---

## 🎯 Criterios de Evaluación y Ponderación

### 1. Funcionalidad de la API (40 puntos)

#### 1.1 Endpoints Básicos (15 puntos)

**Excelente (13-15 puntos)**

- ✅ Todos los endpoints CRUD funcionan correctamente
- ✅ Respuestas HTTP con status codes apropiados
- ✅ Manejo de errores 404, 400, 500 implementado
- ✅ Endpoints adicionales (estadísticas, filtros) funcionando

**Competente (10-12 puntos)**

- ✅ Endpoints CRUD básicos funcionando
- ✅ Status codes correctos en casos exitosos
- ✅ Manejo básico de errores 404
- ⚠️ Algunos endpoints avanzados con problemas menores

**En Desarrollo (7-9 puntos)**

- ✅ GET y POST funcionando
- ⚠️ PUT/DELETE con problemas ocasionales
- ⚠️ Status codes inconsistentes
- ❌ Manejo de errores limitado

**Insuficiente (0-6 puntos)**

- ❌ Endpoints principales no funcionan
- ❌ Status codes incorrectos
- ❌ Sin manejo de errores

#### 1.2 Validación de Datos (15 puntos)

**Excelente (13-15 puntos)**

- ✅ Modelos Pydantic completos con validadores personalizados
- ✅ Validación de tipos, rangos y formatos
- ✅ Mensajes de error descriptivos y útiles
- ✅ Validación tanto en request como response models

**Competente (10-12 puntos)**

- ✅ Modelos Pydantic básicos implementados
- ✅ Validación de tipos funcionando
- ✅ Algunos validadores personalizados
- ⚠️ Mensajes de error básicos

**En Desarrollo (7-9 puntos)**

- ✅ Modelos Pydantic básicos
- ⚠️ Validación limitada a tipos básicos
- ❌ Sin validadores personalizados
- ❌ Mensajes de error genéricos

**Insuficiente (0-6 puntos)**

- ❌ Sin modelos Pydantic o incorrectos
- ❌ Sin validación de datos
- ❌ Acepta cualquier input sin validar

#### 1.3 Filtros y Búsqueda (10 puntos)

**Excelente (9-10 puntos)**

- ✅ Múltiples filtros funcionando (categoría, fecha, estado, etc.)
- ✅ Búsqueda por texto en múltiples campos
- ✅ Combinación de filtros funcional
- ✅ Paginación implementada correctamente

**Competente (7-8 puntos)**

- ✅ Filtros básicos funcionando
- ✅ Búsqueda por texto simple
- ✅ Paginación básica
- ⚠️ Algunos filtros avanzados faltantes

**En Desarrollo (5-6 puntos)**

- ✅ Algunos filtros funcionando
- ⚠️ Búsqueda limitada
- ❌ Sin paginación o problemas en implementación

**Insuficiente (0-4 puntos)**

- ❌ Sin filtros implementados
- ❌ Sin funcionalidad de búsqueda
- ❌ Sin paginación

### 2. Calidad del Código (25 puntos)

#### 2.1 Estructura y Organización (10 puntos)

**Excelente (9-10 puntos)**

- ✅ Estructura modular clara (models, routers, services)
- ✅ Separación de responsabilidades evidente
- ✅ Archivos organizados lógicamente
- ✅ Imports organizados y sin circulares

**Competente (7-8 puntos)**

- ✅ Estructura básica apropiada
- ✅ Modelos separados del código de rutas
- ✅ Organización clara de archivos
- ⚠️ Algunas responsabilidades mezcladas

**En Desarrollo (5-6 puntos)**

- ✅ Archivos separados básicamente
- ⚠️ Estructura confusa en algunos lugares
- ⚠️ Responsabilidades no claramente definidas

**Insuficiente (0-4 puntos)**

- ❌ Todo el código en un solo archivo
- ❌ Sin estructura aparente
- ❌ Código muy desorganizado

#### 2.2 Estilo y Mejores Prácticas (8 puntos)

**Excelente (7-8 puntos)**

- ✅ Nombres de variables/funciones descriptivos
- ✅ Type hints utilizados consistentemente
- ✅ Funciones pequeñas y enfocadas
- ✅ Sin código duplicado
- ✅ Configuración por variables de entorno

**Competente (5-6 puntos)**

- ✅ Nombres de variables apropiados
- ✅ Type hints en funciones principales
- ✅ Funciones razonablemente enfocadas
- ⚠️ Alguna duplicación menor de código

**En Desarrollo (3-4 puntos)**

- ⚠️ Nombres de variables básicos pero aceptables
- ⚠️ Type hints esporádicos
- ⚠️ Algunas funciones muy largas

**Insuficiente (0-2 puntos)**

- ❌ Nombres de variables confusos o genéricos
- ❌ Sin type hints
- ❌ Código muy repetitivo

#### 2.3 Manejo de Errores (7 puntos)

**Excelente (6-7 puntos)**

- ✅ HTTPException utilizadas apropiadamente
- ✅ Custom exception handlers implementados
- ✅ Logging de errores configurado
- ✅ Respuestas de error consistentes y útiles

**Competente (4-5 puntos)**

- ✅ HTTPException básicas implementadas
- ✅ Manejo de casos comunes (404, 400)
- ⚠️ Respuestas de error básicas

**En Desarrollo (2-3 puntos)**

- ✅ Algunos HTTPException utilizados
- ⚠️ Manejo inconsistente de errores

**Insuficiente (0-1 puntos)**

- ❌ Sin manejo de errores apropiado
- ❌ La aplicación se rompe con inputs inválidos

### 3. Documentación y Presentación (20 puntos)

#### 3.1 Documentación Automática (8 puntos)

**Excelente (7-8 puntos)**

- ✅ Swagger/OpenAPI generado correctamente
- ✅ Ejemplos en los modelos Pydantic
- ✅ Descripciones en endpoints y parámetros
- ✅ Tags y organizadores utilizados

**Competente (5-6 puntos)**

- ✅ Documentación automática funcionando
- ✅ Algunos ejemplos en modelos
- ✅ Descripciones básicas en endpoints

**En Desarrollo (3-4 puntos)**

- ✅ Documentación automática básica
- ⚠️ Sin ejemplos o descripciones

**Insuficiente (0-2 puntos)**

- ❌ Documentación automática no funciona
- ❌ Sin configuración de FastAPI apropiada

#### 3.2 README y Documentación Manual (8 puntos)

**Excelente (7-8 puntos)**

- ✅ README completo con instrucciones claras de instalación
- ✅ Ejemplos de uso de la API con curl/postman
- ✅ Descripción de la arquitectura del proyecto
- ✅ Screenshots de la documentación funcionando

**Competente (5-6 puntos)**

- ✅ README con instrucciones básicas de instalación
- ✅ Algunos ejemplos de uso
- ✅ Descripción del proyecto

**En Desarrollo (3-4 puntos)**

- ✅ README básico presente
- ⚠️ Instrucciones incompletas o confusas

**Insuficiente (0-2 puntos)**

- ❌ Sin README o muy básico
- ❌ Sin instrucciones de instalación

#### 3.3 Comentarios y Docstrings (4 puntos)

**Excelente (4 puntos)**

- ✅ Docstrings en todas las funciones importantes
- ✅ Comentarios explicativos donde es necesario
- ✅ Código autodocumentado

**Competente (3 puntos)**

- ✅ Docstrings en funciones principales
- ✅ Algunos comentarios útiles

**En Desarrollo (2 puntos)**

- ⚠️ Pocos docstrings o comentarios

**Insuficiente (0-1 puntos)**

- ❌ Sin documentación en el código

### 4. Completitud y Entrega (15 puntos)

#### 4.1 Ejercicios Completados (5 puntos)

**Excelente (5 puntos)**

- ✅ Todos los ejercicios de python-fundamentals completados
- ✅ Código funcionando correctamente
- ✅ Soluciones elegantes y eficientes

**Competente (4 puntos)**

- ✅ Mayoría de ejercicios completados
- ✅ Código funcionando con problemas menores

**En Desarrollo (2-3 puntos)**

- ⚠️ Algunos ejercicios completados
- ⚠️ Soluciones básicas pero funcionales

**Insuficiente (0-1 puntos)**

- ❌ Pocos o ningún ejercicio completado

#### 4.2 Estructura de Entrega (5 puntos)

**Excelente (5 puntos)**

- ✅ Repositorio GitHub bien organizado
- ✅ Commits frecuentes con mensajes descriptivos
- ✅ requirements.txt completo
- ✅ Estructura de carpetas profesional

**Competente (4 puntos)**

- ✅ Repositorio organizado básicamente
- ✅ requirements.txt presente
- ✅ Algunos commits con buenos mensajes

**En Desarrollo (2-3 puntos)**

- ⚠️ Repositorio básico pero funcional
- ⚠️ requirements.txt incompleto

**Insuficiente (0-1 puntos)**

- ❌ Entrega desorganizada o incompleta

#### 4.3 Puntualidad y Formato (5 puntos)

**Excelente (5 puntos)**

- ✅ Entrega a tiempo
- ✅ Todos los formatos solicitados
- ✅ Video demo claro y profesional

**Competente (4 puntos)**

- ✅ Entrega a tiempo
- ✅ Formatos básicos cumplidos
- ⚠️ Video demo básico

**En Desarrollo (2-3 puntos)**

- ⚠️ Entrega con retraso menor (1-2 días)
- ⚠️ Algunos formatos faltantes

**Insuficiente (0-1 puntos)**

- ❌ Entrega tardía significativa (3+ días)
- ❌ Formatos incorrectos o faltantes

---

## 🏆 Puntos Bonus (hasta +15 puntos)

### Testing Automatizado (+5 puntos)

- ✅ Tests básicos con pytest implementados
- ✅ Cobertura mínima de endpoints principales
- ✅ Tests de validación de modelos

### Docker Setup (+5 puntos)

- ✅ Dockerfile funcional
- ✅ docker-compose.yml para desarrollo
- ✅ Instrucciones de uso con Docker

### CI/CD Pipeline (+3 puntos)

- ✅ GitHub Actions configurado
- ✅ Tests ejecutándose automáticamente
- ✅ Linting automático

### Features Avanzadas (+2 puntos cada una)

- ✅ Middleware personalizado
- ✅ Bulk operations
- ✅ Export/Import de datos
- ✅ Configuración avanzada con environment variables

---

## 📊 Escala de Calificación Final

| Puntos  | Calificación      | Descripción                              |
| ------- | ----------------- | ---------------------------------------- |
| 90-100+ | **Excelente**     | Supera expectativas, trabajo profesional |
| 75-89   | **Competente**    | Cumple todos los requerimientos básicos  |
| 60-74   | **En Desarrollo** | Cumple parcialmente, necesita mejoras    |
| 0-59    | **Insuficiente**  | No cumple requerimientos mínimos         |

---

## 🤖 Instrucciones para Evaluación por IA

### Criterios de Verificación Automática

1. **Funcionalidad**:

   - Ejecutar `pip install -r requirements.txt`
   - Ejecutar `uvicorn app.main:app --reload`
   - Verificar que http://localhost:8000/docs carga correctamente
   - Probar endpoints básicos: GET, POST, PUT, DELETE
   - Verificar respuestas JSON válidas

2. **Código**:

   - Verificar presencia de modelos Pydantic
   - Comprobar type hints en funciones
   - Revisar estructura de carpetas
   - Validar que no hay errores de sintaxis

3. **Documentación**:

   - Verificar presencia de README.md
   - Comprobar documentación automática en /docs
   - Revisar comentarios y docstrings

4. **Entrega**:
   - Verificar estructura de repositorio
   - Comprobar presencia de requirements.txt
   - Revisar commits en GitHub

### Puntos de Verificación Críticos

❌ **Automáticamente Insuficiente si**:

- La aplicación no inicia (`uvicorn app.main:app --reload` falla)
- No hay modelos Pydantic implementados
- No hay endpoints CRUD básicos funcionando
- Sin README.md o completamente vacío

✅ **Criterios Mínimos para Aprobar**:

- Aplicación inicia sin errores
- Al menos 3 endpoints funcionando (GET, POST, PUT/DELETE)
- Modelos Pydantic básicos implementados
- README con instrucciones de instalación

---

## 📝 Notas para el Evaluador

1. **Priorizar funcionalidad**: Un proyecto simple que funciona perfectamente es mejor que uno complejo pero roto.

2. **Considerar el contexto**: Es la primera semana, evaluar según el nivel esperado para principiantes en FastAPI.

3. **Valorar la completitud**: Preferir proyectos completos aunque simples, sobre proyectos avanzados pero incompletos.

4. **Documentar feedback**: Proporcionar comentarios específicos para cada criterio evaluado.

5. **Consistencia**: Aplicar los mismos criterios para todos los estudiantes.

---

**Versión**: 1.0  
**Fecha de creación**: Julio 2025  
**Última actualización**: Julio 2025
