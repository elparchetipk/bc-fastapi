# RÚBRICA DE EVALUACIÓN - SEMANA 4

## Query Parameters, Advanced Validation & File Operations

### INFORMACIÓN GENERAL

- **Semana**: 4
- **Tema**: Query Parameters, Pydantic Advanced Validation & Basic File Operations
- **Duración**: 6 horas (incluye break de 30 min)
- **Prerequisitos**: Semana 3 aprobada (CRUD completo funcionando)
- **Modalidad**: Evaluación automática por IA + revisión manual

### CRITERIOS DE EVALUACIÓN

#### 1. QUERY PARAMETERS (25 puntos)

**Evidencia requerida**: Endpoints con query parameters funcionales para filtrado y búsqueda

| Criterio                   | Excelente (5pts)                                   | Bueno (4pts)                     | Suficiente (3pts)                | Insuficiente (0pts)        |
| -------------------------- | -------------------------------------------------- | -------------------------------- | -------------------------------- | -------------------------- |
| **Basic Query Parameters** | Múltiples query params implementados correctamente | Query params básicos funcionales | Al menos 1 query param funcional | Query params no funcionan  |
| **Optional Parameters**    | Parámetros opcionales con valores por defecto      | Algunos parámetros opcionales    | Parámetros básicos sin defaults  | Sin parámetros opcionales  |
| **Type Annotations**       | Query params con tipos correctos (int, str, bool)  | Tipos básicos especificados      | Algunos tipos especificados      | Sin anotaciones de tipo    |
| **Filtering Logic**        | Lógica de filtrado implementada correctamente      | Filtrado básico funcional        | Filtrado simple implementado     | Sin lógica de filtrado     |
| **Multiple Filters**       | Combinación de múltiples filtros funcionando       | Algunos filtros combinados       | Filtros independientes           | Sin combinación de filtros |

#### 2. ADVANCED PYDANTIC VALIDATION (25 puntos)

**Evidencia requerida**: Modelos con validaciones avanzadas usando Field y validators

| Criterio              | Excelente (5pts)                          | Bueno (4pts)                      | Suficiente (3pts)               | Insuficiente (0pts)         |
| --------------------- | ----------------------------------------- | --------------------------------- | ------------------------------- | --------------------------- |
| **Field Constraints** | Uso correcto de Field con min/max, regex  | Algunos constraints implementados | Field básico usado              | Sin uso de Field            |
| **Optional Fields**   | Campos opcionales correctamente definidos | Algunos campos opcionales         | Intentos de campos opcionales   | Sin campos opcionales       |
| **Custom Validation** | Validaciones personalizadas implementadas | Algunas validaciones custom       | Validación básica personalizada | Sin validaciones custom     |
| **Error Messages**    | Mensajes de error personalizados claros   | Algunos mensajes personalizados   | Mensajes básicos                | Sin mensajes personalizados |
| **Model Composition** | Modelos anidados o composición básica     | Algunos modelos relacionados      | Modelos simples                 | Sin composición de modelos  |

#### 3. SEARCH ENDPOINTS (20 puntos)

**Evidencia requerida**: Endpoints de búsqueda que combinan query parameters con lógica de filtrado

| Criterio                  | Excelente (4pts)                               | Bueno (3pts)                 | Suficiente (2pts)       | Insuficiente (0pts)    |
| ------------------------- | ---------------------------------------------- | ---------------------------- | ----------------------- | ---------------------- |
| **Search Implementation** | Endpoint de búsqueda completo y funcional      | Búsqueda básica implementada | Búsqueda simple creada  | Búsqueda no funciona   |
| **Text Search**           | Búsqueda por texto en múltiples campos         | Búsqueda básica por texto    | Búsqueda en un campo    | Sin búsqueda por texto |
| **Range Filters**         | Filtros por rango (edad, precio, fecha)        | Algunos filtros por rango    | Filtro básico por rango | Sin filtros por rango  |
| **Pagination Basics**     | Conceptos básicos de paginación (limit/offset) | Limit básico implementado    | Intentos de paginación  | Sin paginación         |
| **Response Format**       | Respuestas de búsqueda bien estructuradas      | Respuestas básicas correctas | Respuestas simples      | Respuestas malformadas |

#### 4. FILE OPERATIONS (15 puntos)

**Evidencia requerida**: Operaciones básicas con archivos (upload/download simple)

| Criterio            | Excelente (3pts)                             | Bueno (2pts)              | Suficiente (1pt)                 | Insuficiente (0pts)   |
| ------------------- | -------------------------------------------- | ------------------------- | -------------------------------- | --------------------- |
| **File Upload**     | Upload básico de archivos implementado       | Upload simple funcional   | Intento de upload                | Upload no funciona    |
| **File Validation** | Validación básica de tipo/tamaño de archivo  | Algunas validaciones      | Validación mínima                | Sin validación        |
| **File Storage**    | Archivos guardados correctamente             | Almacenamiento básico     | Archivos guardados temporalmente | Sin almacenamiento    |
| **File Download**   | Download básico implementado                 | Download simple funcional | Intento de download              | Download no funciona  |
| **Error Handling**  | Manejo de errores en operaciones de archivos | Algunos errores manejados | Error handling básico            | Sin manejo de errores |

#### 5. INTEGRATION & TESTING (15 puntos)

**Evidencia requerida**: Integración de todas las funcionalidades y testing completo

| Criterio                  | Excelente (3pts)                                   | Bueno (2pts)                 | Suficiente (1pt)                       | Insuficiente (0pts)  |
| ------------------------- | -------------------------------------------------- | ---------------------------- | -------------------------------------- | -------------------- |
| **API Integration**       | Todas las funcionalidades integradas correctamente | Integración básica funcional | Funcionalidades mayormente compatibles | Sin integración      |
| **Comprehensive Testing** | Pruebas completas de query params y validación     | Testing básico realizado     | Algunas pruebas realizadas             | Sin testing          |
| **Documentation**         | Documentación clara de nuevas funcionalidades      | Documentación básica         | Documentación mínima                   | Sin documentación    |
| **Code Organization**     | Código bien organizado y modular                   | Organización básica adecuada | Código funcional                       | Código desorganizado |
| **Performance Awareness** | Consideraciones básicas de performance             | Algunas optimizaciones       | Código funcional básico                | Sin consideraciones  |

### ESCALA DE CALIFICACIÓN

- **Excelente (90-100 pts)**: Dominio sólido de query parameters y validación avanzada
- **Bueno (80-89 pts)**: Implementación correcta de funcionalidades principales
- **Suficiente (70-79 pts)**: Funcionalidades básicas implementadas
- **Insuficiente (0-69 pts)**: Requiere refuerzo en conceptos avanzados

### CRITERIOS DE APROBACIÓN

- **Mínimo para aprobar**: 70 puntos (70%)
- **Entregables obligatorios**:
  - Al menos 2 endpoints con query parameters funcionales
  - Al menos 1 modelo con validación avanzada (Field)
  - Endpoint de búsqueda básico funcionando
  - Operación de archivo básica (upload o download)

### RETROALIMENTACIÓN AUTOMÁTICA

**Para el agente evaluador de IA:**

#### Puntos de verificación automática:

1. **Query Parameters**: Verificar funciones con parámetros de query anotados
2. **Field Import**: Confirmar que Field de Pydantic está importado y usado
3. **Search Endpoints**: Identificar endpoints que procesan múltiples parámetros
4. **File Operations**: Buscar imports relacionados con archivos (UploadFile, etc.)
5. **Validation**: Verificar uso de validaciones más allá de tipos básicos

#### Indicadores de calidad:

- Uso apropiado de Query() para parámetros de consulta
- Implementación de validaciones con Field()
- Lógica de filtrado que mantiene performance
- Manejo de casos donde no se encuentran resultados
- Documentación automática rica en /docs

#### Señales de alarma para revisión manual:

- Query parameters sin validación de tipos
- Validaciones excesivamente complejas para el nivel
- Operaciones de archivo sin validación de seguridad
- Endpoints de búsqueda sin optimización básica
- Falta de integración con funcionalidades previas

#### Patrones de código esperados:

```python
# Esperado: Query parameters básicos
@app.get("/users")
def get_users(
    name: Optional[str] = None,
    min_age: Optional[int] = None,
    limit: int = 10
):
    # Lógica de filtrado

# Esperado: Validación avanzada
class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    age: Optional[int] = Field(None, ge=0, le=120)
```

### FEEDBACK PERSONALIZADO POR NIVEL

#### Para estudiantes destacados (90-100 pts):

- Reconocer implementación sólida de funcionalidades avanzadas
- Destacar uso apropiado de validaciones y query parameters
- Preparar para conceptos de bases de datos en semanas siguientes

#### Para estudiantes en nivel esperado (80-89 pts):

- Confirmar comprensión correcta de conceptos avanzados
- Señalar áreas de mejora en validaciones o búsquedas
- Reforzar progreso hacia APIs más sofisticadas

#### Para estudiantes en nivel mínimo (70-79 pts):

- Identificar funcionalidades que necesitan práctica adicional
- Proporcionar ejercicios específicos para query parameters
- Asegurar comprensión antes de avanzar a bases de datos

#### Para estudiantes por debajo del mínimo (0-69 pts):

- Análisis detallado de gaps en funcionalidades avanzadas
- Plan de recuperación enfocado en query parameters básicos
- Sesión de apoyo para validaciones de Pydantic

### CONEXIÓN CON SEMANAS ANTERIORES

- **Semanas 1-3**: Construye sobre CRUD completo establecido
- **Preparación Semana 5**: Base para conceptos de bases de datos
- **Progresión**: De operaciones básicas a funcionalidades avanzadas

### PROYECCIÓN A SEMANAS FUTURAS

Esta semana prepara para:

- Bases de datos relacionales (Semana 5)
- Autenticación y autorización (Semana 6)
- APIs de producción (Semanas 7-8)

### RECURSOS PARA ESTUDIANTES

- FastAPI Query Parameters: https://fastapi.tiangolo.com/tutorial/query-params/
- Pydantic Field: https://docs.pydantic.dev/latest/concepts/fields/
- FastAPI File Upload: https://fastapi.tiangolo.com/tutorial/request-files/
- Ejemplos de código de las prácticas de la semana

**Fecha de creación**: 25 de julio de 2025  
**Versión**: 1.0  
**Próxima revisión**: Al finalizar implementación del bootcamp
