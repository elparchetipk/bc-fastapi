# RÚBRICA DE EVALUACIÓN - SEMANA 2

## Data Validation & POST Endpoints

### INFORMACIÓN GENERAL

- **Semana**: 2
- **Tema**: Python Type Hints, Pydantic Models & POST Endpoints
- **Duración**: 6 horas (incluye break de 30 min)
- **Prerequisitos**: Semana 1 aprobada (API básica funcionando)
- **Modalidad**: Evaluación automática por IA + revisión manual

### CRITERIOS DE EVALUACIÓN

#### 1. PYTHON TYPE HINTS (20 puntos)

**Evidencia requerida**: Código con type hints implementados correctamente

| Criterio                 | Excelente (4pts)                            | Bueno (3pts)                   | Suficiente (2pts)          | Insuficiente (0pts)          |
| ------------------------ | ------------------------------------------- | ------------------------------ | -------------------------- | ---------------------------- |
| **Function Parameters**  | Todos los parámetros con tipos correctos    | Mayoría de parámetros tipados  | Algunos parámetros tipados | Sin type hints en parámetros |
| **Return Types**         | Tipos de retorno especificados y correctos  | Mayoría de returns tipados     | Algunos returns tipados    | Sin tipos de retorno         |
| **Variable Annotations** | Variables complejas anotadas apropiadamente | Variables principales anotadas | Anotaciones básicas        | Sin anotaciones de variables |
| **Complex Types**        | Uso correcto de List, Dict, Optional        | Algunos tipos complejos usados | Tipos básicos únicamente   | Solo tipos primitivos        |
| **Consistency**          | Uso consistente en todo el código           | Uso mayormente consistente     | Uso irregular              | Sin consistencia             |

#### 2. PYDANTIC MODELS (25 puntos)

**Evidencia requerida**: Modelos Pydantic funcionales para validación de datos

| Criterio             | Excelente (5pts)                          | Bueno (4pts)                   | Suficiente (3pts)       | Insuficiente (0pts)  |
| -------------------- | ----------------------------------------- | ------------------------------ | ----------------------- | -------------------- |
| **Model Definition** | Modelos bien estructurados con BaseModel  | Modelos básicos funcionales    | Modelos simples creados | Modelos no funcionan |
| **Field Types**      | Tipos de campos apropiados y precisos     | Tipos básicos correctos        | Algunos tipos correctos | Tipos incorrectos    |
| **Validation Rules** | Validaciones básicas implementadas        | Algunas validaciones presentes | Validación mínima       | Sin validaciones     |
| **Model Usage**      | Modelos usados correctamente en endpoints | Uso básico en endpoints        | Integración parcial     | Sin integración      |
| **Data Structure**   | Estructura de datos lógica y eficiente    | Estructura básica adecuada     | Estructura simple       | Estructura confusa   |

#### 3. POST ENDPOINTS (25 puntos)

**Evidencia requerida**: Endpoints POST funcionales que reciben y procesan datos

| Criterio                    | Excelente (5pts)                             | Bueno (4pts)                    | Suficiente (3pts)             | Insuficiente (0pts)        |
| --------------------------- | -------------------------------------------- | ------------------------------- | ----------------------------- | -------------------------- |
| **Endpoint Implementation** | POST endpoints bien implementados            | Endpoints básicos funcionales   | Endpoints simples creados     | Endpoints no funcionan     |
| **Request Body Handling**   | Manejo correcto de request body con Pydantic | Request body básico procesado   | Datos recibidos parcialmente  | Sin procesamiento de body  |
| **Response Format**         | Respuestas JSON consistentes y útiles        | Respuestas básicas correctas    | Respuestas simples            | Respuestas malformadas     |
| **Data Persistence**        | Datos almacenados en memoria correctamente   | Almacenamiento básico funcional | Datos guardados temporalmente | Sin persistencia           |
| **HTTP Status Codes**       | Uso correcto de 201 para creación            | Status codes básicos usados     | Códigos por defecto           | Sin manejo de status codes |

#### 4. TESTING Y VALIDACIÓN (20 puntos)

**Evidencia requerida**: Pruebas documentadas de funcionalidad completa

| Criterio                    | Excelente (4pts)                            | Bueno (3pts)                    | Suficiente (2pts)                  | Insuficiente (0pts)          |
| --------------------------- | ------------------------------------------- | ------------------------------- | ---------------------------------- | ---------------------------- |
| **POST Request Testing**    | Múltiples pruebas POST documentadas         | Pruebas POST básicas realizadas | Testing POST mínimo                | Sin pruebas POST             |
| **Data Validation Testing** | Pruebas de validación exitosas y fallidas   | Algunas pruebas de validación   | Validación básica probada          | Sin pruebas de validación    |
| **Error Scenarios**         | Escenarios de error probados y documentados | Algunos errores probados        | Errores básicos identificados      | Sin testing de errores       |
| **Integration Testing**     | GET y POST funcionando juntos               | Integración básica probada      | Endpoints independientes funcionan | Sin integración              |
| **Documentation**           | Pruebas documentadas con capturas/ejemplos  | Documentación básica de pruebas | Testing mencionado                 | Sin documentación de pruebas |

#### 5. ENTREGABLES Y ORGANIZACIÓN (10 puntos)

**Evidencia requerida**: Proyecto completo y bien organizado

| Criterio                    | Excelente (2pts)                           | Bueno (1.5pts)                 | Suficiente (1pt)             | Insuficiente (0pts)         |
| --------------------------- | ------------------------------------------ | ------------------------------ | ---------------------------- | --------------------------- |
| **Code Organization**       | Código limpio, modular y bien comentado    | Código organizado y claro      | Código funcional básico      | Código desorganizado        |
| **GitHub Repository**       | Commits descriptivos y progresión clara    | Repo actualizado regularmente  | Código subido al final       | Sin repo o incompleto       |
| **README Updates**          | README completo con nuevos endpoints       | README actualizado básicamente | README mínimo actualizado    | README no actualizado       |
| **Requirements Management** | requirements.txt actualizado correctamente | Dependencias gestionadas       | Lista básica de dependencias | Sin gestión de dependencias |
| **Delivery Quality**        | Entrega completa y a tiempo                | Entrega a tiempo con calidad   | Entrega básica completa      | Entrega incompleta o tardía |

### ESCALA DE CALIFICACIÓN

- **Excelente (90-100 pts)**: Dominio sólido de validación de datos y endpoints POST
- **Bueno (80-89 pts)**: Comprensión correcta con implementación funcional
- **Suficiente (70-79 pts)**: Conceptos básicos logrados, necesita práctica adicional
- **Insuficiente (0-69 pts)**: Requiere refuerzo en conceptos fundamentales

### CRITERIOS DE APROBACIÓN

- **Mínimo para aprobar**: 70 puntos (70%)
- **Entregables obligatorios**:
  - Al menos 1 modelo Pydantic funcional
  - Al menos 1 endpoint POST que acepte datos
  - Código con type hints básicos
  - API integrada (GET + POST funcionando juntos)

### RETROALIMENTACIÓN AUTOMÁTICA

**Para el agente evaluador de IA:**

#### Puntos de verificación automática:

1. **Type Hints**: Verificar presencia de anotaciones de tipo en funciones principales
2. **Pydantic Import**: Confirmar que BaseModel está importado y usado
3. **POST Endpoints**: Identificar al menos un endpoint con decorador @app.post
4. **Model Usage**: Verificar que modelos Pydantic se usan en endpoints
5. **Syntax Validation**: Confirmar que el código es sintácticamente correcto

#### Indicadores de calidad:

- Nombres descriptivos para modelos y campos
- Uso apropiado de tipos de datos (str, int, bool, etc.)
- Estructura lógica en respuestas de endpoints
- Comentarios explicativos en modelos complejos
- Consistencia en formato de respuestas

#### Señales de alarma para revisión manual:

- Modelos excesivamente complejos para el nivel
- Uso de validaciones avanzadas no enseñadas
- Endpoints POST sin validación de datos
- Errores de sintaxis en type hints
- Falta de integración entre GET y POST

#### Patrones de código esperados:

```python
# Esperado: Modelo Pydantic básico
class User(BaseModel):
    name: str
    age: int

# Esperado: Endpoint POST con modelo
@app.post("/users")
def create_user(user: User):
    return {"message": "User created", "user": user}
```

### FEEDBACK PERSONALIZADO POR NIVEL

#### Para estudiantes destacados (90-100 pts):

- Reconocer implementación sólida
- Sugerir exploraciones adicionales (validaciones opcionales)
- Preparar para conceptos avanzados de Semana 3

#### Para estudiantes en nivel esperado (80-89 pts):

- Confirmar comprensión correcta
- Señalar áreas de mejora menores
- Reforzar confianza en progreso

#### Para estudiantes en nivel mínimo (70-79 pts):

- Identificar conceptos que necesitan refuerzo
- Proporcionar ejercicios adicionales específicos
- Programar seguimiento antes de Semana 3

#### Para estudiantes por debajo del mínimo (0-69 pts):

- Análisis detallado de gaps conceptuales
- Plan de recuperación específico
- Sesión de apoyo adicional requerida

### RECURSOS PARA ESTUDIANTES

- Documentación Pydantic: https://docs.pydantic.dev/
- FastAPI Tutorial sobre Request Body: https://fastapi.tiangolo.com/tutorial/body/
- Python Type Hints Guide: https://docs.python.org/3/library/typing.html
- Ejemplos de código de las prácticas de la semana

**Fecha de creación**: 25 de julio de 2025  
**Versión**: 1.0  
**Próxima revisión**: Al finalizar implementación del bootcamp
