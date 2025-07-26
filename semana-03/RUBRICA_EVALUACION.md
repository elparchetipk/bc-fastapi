# RÚBRICA DE EVALUACIÓN - SEMANA 3

## Complete CRUD Operations & Error Handling

### INFORMACIÓN GENERAL

- **Semana**: 3
- **Tema**: PUT/DELETE Endpoints, Error Handling & Complete CRUD
- **Duración**: 6 horas (incluye break de 30 min)
- **Prerequisitos**: Semana 2 aprobada (POST endpoints y Pydantic funcionando)
- **Modalidad**: Evaluación automática por IA + revisión manual

### CRITERIOS DE EVALUACIÓN

#### 1. PUT ENDPOINTS (20 puntos)

**Evidencia requerida**: Endpoints PUT funcionales para actualización de datos

| Criterio               | Excelente (4pts)                            | Bueno (3pts)                   | Suficiente (2pts)            | Insuficiente (0pts)         |
| ---------------------- | ------------------------------------------- | ------------------------------ | ---------------------------- | --------------------------- |
| **PUT Implementation** | PUT endpoint correctamente implementado     | Endpoint PUT básico funcional  | PUT simple creado            | PUT no funciona             |
| **Path Parameters**    | ID en ruta manejado correctamente           | Parámetros de ruta básicos     | Algunos parámetros usados    | Sin parámetros de ruta      |
| **Request Body**       | Body de request procesado con Pydantic      | Request body básico procesado  | Datos recibidos parcialmente | Sin procesamiento de body   |
| **Update Logic**       | Lógica de actualización completa y correcta | Actualización básica funcional | Actualización simple         | Sin lógica de actualización |
| **Response Format**    | Respuesta con objeto actualizado            | Respuesta básica correcta      | Respuesta simple             | Respuesta incorrecta        |

#### 2. DELETE ENDPOINTS (20 puntos)

**Evidencia requerida**: Endpoints DELETE funcionales para eliminación de datos

| Criterio                  | Excelente (4pts)                           | Bueno (3pts)                     | Suficiente (2pts)                | Insuficiente (0pts)              |
| ------------------------- | ------------------------------------------ | -------------------------------- | -------------------------------- | -------------------------------- |
| **DELETE Implementation** | DELETE endpoint correctamente implementado | Endpoint DELETE básico funcional | DELETE simple creado             | DELETE no funciona               |
| **Item Identification**   | Identificación correcta de item por ID     | ID básico usado para identificar | Algunos IDs manejados            | Sin identificación por ID        |
| **Deletion Logic**        | Elemento removido correctamente de lista   | Eliminación básica funcional     | Eliminación simple               | Sin eliminación real             |
| **Response Message**      | Mensaje de confirmación claro y útil       | Mensaje básico de confirmación   | Respuesta simple                 | Sin mensaje de confirmación      |
| **Data Integrity**        | Lista/datos mantienen integridad después   | Datos básicamente consistentes   | Datos funcionan post-eliminación | Datos corruptos post-eliminación |

#### 3. ERROR HANDLING (25 puntos)

**Evidencia requerida**: Manejo apropiado de errores con HTTPException

| Criterio                    | Excelente (5pts)                               | Bueno (4pts)                    | Suficiente (3pts)             | Insuficiente (0pts)            |
| --------------------------- | ---------------------------------------------- | ------------------------------- | ----------------------------- | ------------------------------ |
| **HTTPException Usage**     | HTTPException usada correctamente              | Uso básico de HTTPException     | Algunas excepciones manejadas | Sin manejo de excepciones      |
| **404 Not Found**           | Error 404 implementado en endpoints relevantes | 404 básico en algunos endpoints | 404 en al menos un endpoint   | Sin manejo de 404              |
| **400 Bad Request**         | Error 400 para datos inválidos                 | 400 básico implementado         | Algunos errores 400           | Sin manejo de 400              |
| **Error Messages**          | Mensajes de error claros y descriptivos        | Mensajes básicos útiles         | Mensajes simples              | Sin mensajes descriptivos      |
| **Status Code Consistency** | Uso consistente de códigos HTTP apropiados     | Códigos básicos correctos       | Algunos códigos correctos     | Códigos incorrectos o ausentes |

#### 4. CRUD COMPLETO (25 puntos)

**Evidencia requerida**: Operaciones CRUD integradas funcionando juntas

| Criterio          | Excelente (5pts)                                      | Bueno (4pts)              | Suficiente (3pts)                  | Insuficiente (0pts)       |
| ----------------- | ----------------------------------------------------- | ------------------------- | ---------------------------------- | ------------------------- |
| **CREATE (POST)** | POST endpoints robustos de Semana 2                   | POST básico funcionando   | POST simple operativo              | POST no funciona          |
| **READ (GET)**    | GET endpoints completos (lista + individual)          | GET básicos funcionando   | Al menos un GET operativo          | GET no funciona           |
| **UPDATE (PUT)**  | PUT endpoints completos y funcionales                 | PUT básico funcionando    | PUT simple operativo               | PUT no funciona           |
| **DELETE**        | DELETE endpoints completos y funcionales              | DELETE básico funcionando | DELETE simple operativo            | DELETE no funciona        |
| **Integration**   | Todas las operaciones funcionan juntas sin conflictos | CRUD básico integrado     | Operaciones mayormente compatibles | Operaciones no integradas |

#### 5. TESTING Y VALIDACIÓN (10 puntos)

**Evidencia requerida**: Pruebas documentadas de todas las operaciones CRUD

| Criterio             | Excelente (2pts)                                 | Bueno (1.5pts)                    | Suficiente (1pt)                    | Insuficiente (0pts)               |
| -------------------- | ------------------------------------------------ | --------------------------------- | ----------------------------------- | --------------------------------- |
| **CRUD Testing**     | Todas las operaciones CRUD probadas              | Operaciones principales probadas  | Algunas operaciones probadas        | Sin testing CRUD                  |
| **Error Testing**    | Escenarios de error probados y documentados      | Algunos errores probados          | Errores básicos identificados       | Sin testing de errores            |
| **Integration Flow** | Flujo completo CREATE→READ→UPDATE→DELETE probado | Flujo básico probado              | Operaciones independientes probadas | Sin flujo integrado               |
| **Documentation**    | Testing documentado con ejemplos claros          | Documentación básica de pruebas   | Testing básico mencionado           | Sin documentación                 |
| **Edge Cases**       | Casos límite identificados y probados            | Algunos casos límite considerados | Casos básicos únicamente            | Sin consideración de casos límite |

### ESCALA DE CALIFICACIÓN

- **Excelente (90-100 pts)**: Dominio completo de CRUD y manejo de errores
- **Bueno (80-89 pts)**: CRUD funcional con error handling básico
- **Suficiente (70-79 pts)**: Operaciones CRUD básicas funcionando
- **Insuficiente (0-69 pts)**: CRUD incompleto, requiere refuerzo

### CRITERIOS DE APROBACIÓN

- **Mínimo para aprobar**: 70 puntos (70%)
- **Entregables obligatorios**:
  - Al menos 1 endpoint PUT funcional
  - Al menos 1 endpoint DELETE funcional
  - Manejo básico de error 404
  - CRUD completo operativo (todas las operaciones funcionando)

### RETROALIMENTACIÓN AUTOMÁTICA

**Para el agente evaluador de IA:**

#### Puntos de verificación automática:

1. **PUT Endpoints**: Verificar presencia de @app.put() con parámetros de ruta
2. **DELETE Endpoints**: Verificar presencia de @app.delete() con parámetros de ruta
3. **HTTPException Import**: Confirmar que HTTPException está importado
4. **Error Handling**: Buscar raise HTTPException en el código
5. **CRUD Integration**: Verificar que todos los métodos HTTP están presentes

#### Indicadores de calidad:

- Uso consistente de códigos de estado HTTP
- Mensajes de error descriptivos en HTTPException
- Lógica de actualización que mantiene estructura de datos
- Validación de existencia antes de actualizar/eliminar
- Respuestas JSON consistentes en todos los endpoints

#### Señales de alarma para revisión manual:

- Operaciones CRUD que no mantienen integridad de datos
- Endpoints PUT/DELETE sin validación de existencia
- Manejo de errores excesivamente complejo
- Código que no sigue patrones establecidos en semanas anteriores
- Falta de integración entre operaciones

#### Patrones de código esperados:

```python
# Esperado: PUT endpoint básico
@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    for i, existing_user in enumerate(users):
        if existing_user["id"] == user_id:
            users[i] = {"id": user_id, **user.dict()}
            return users[i]
    raise HTTPException(status_code=404, detail="User not found")

# Esperado: DELETE endpoint básico
@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users):
        if user["id"] == user_id:
            deleted_user = users.pop(i)
            return {"message": f"User {deleted_user['name']} deleted"}
    raise HTTPException(status_code=404, detail="User not found")
```

### FEEDBACK PERSONALIZADO POR NIVEL

#### Para estudiantes destacados (90-100 pts):

- Reconocer implementación completa de CRUD
- Destacar manejo apropiado de errores
- Preparar para conceptos más avanzados (query parameters, validación)

#### Para estudiantes en nivel esperado (80-89 pts):

- Confirmar comprensión sólida de operaciones HTTP
- Señalar mejoras menores en error handling
- Reforzar progreso hacia API completa

#### Para estudiantes en nivel mínimo (70-79 pts):

- Identificar operaciones CRUD que necesitan refuerzo
- Proporcionar ejercicios específicos para error handling
- Asegurar base sólida antes de Semana 4

#### Para estudiantes por debajo del mínimo (0-69 pts):

- Análisis detallado de gaps en CRUD operations
- Plan de recuperación enfocado en operaciones faltantes
- Sesión de apoyo para completar CRUD básico

### CONEXIÓN CON SEMANAS ANTERIORES

- **Semana 1**: Usa conceptos de endpoints GET básicos
- **Semana 2**: Construye sobre POST endpoints y modelos Pydantic
- **Preparación Semana 4**: Base para query parameters y validación avanzada

### RECURSOS PARA ESTUDIANTES

- FastAPI HTTP Methods: https://fastapi.tiangolo.com/tutorial/first-steps/
- HTTP Status Codes: https://httpstatuses.com/
- FastAPI Exception Handling: https://fastapi.tiangolo.com/tutorial/handling-errors/
- Ejemplos CRUD de las prácticas de la semana

**Fecha de creación**: 25 de julio de 2025  
**Versión**: 1.0  
**Próxima revisión**: Al finalizar implementación del bootcamp
