# RÚBRICA DE EVALUACIÓN - SEMANA 3

## Data Validation & Error Handling

### INFORMACIÓN GENERAL

- **Semana**: 3
- **Tema**: Validación de Datos, Manejo de Errores y Estructura REST Básica
- **Duración**: 6 horas (incluye break de 30 min)
- **Prerequisitos**: Semana 2 aprobada (API con Pydantic funcionando)
- **Modalidad**: Evaluación automática por IA + revisión manual

### CRITERIOS DE EVALUACIÓN

#### 1. PYDANTIC VALIDATION (25 puntos)

**Evidencia requerida**: Modelos Pydantic con validaciones implementadas

| Criterio              | Excelente (5pts)                     | Bueno (4pts)                     | Suficiente (3pts)       | Insuficiente (0pts)     |
| --------------------- | ------------------------------------ | -------------------------------- | ----------------------- | ----------------------- |
| **Field Constraints** | Field() con múltiples validaciones   | Field() con validaciones básicas | Algunos Field() usados  | Sin Field() constraints |
| **Custom Validators** | Al menos 1 validador personalizado   | Intento de validador custom      | Validaciones simples    | Sin validadores custom  |
| **Type Validation**   | Tipos de datos apropiados y precisos | Tipos básicos correctos          | Algunos tipos correctos | Tipos incorrectos       |
| **Error Messages**    | Mensajes de error informativos       | Algunos mensajes personalizados  | Mensajes por defecto    | Sin manejo de errores   |
| **Model Structure**   | Modelos bien estructurados           | Estructura básica adecuada       | Modelos simples         | Modelos confusos        |

#### 2. CRUD FUNCTIONALITY (25 puntos)

**Evidencia requerida**: Endpoints CRUD básicos funcionando

| Criterio               | Excelente (5pts)                       | Bueno (4pts)                     | Suficiente (3pts)             | Insuficiente (0pts) |
| ---------------------- | -------------------------------------- | -------------------------------- | ----------------------------- | ------------------- |
| **GET Endpoints**      | GET list y GET by ID funcionando       | GET básico implementado          | Endpoint GET simple           | GET no funciona     |
| **POST Endpoint**      | POST con validación completa           | POST básico funcional            | POST simple implementado      | POST no funciona    |
| **PUT/PATCH Endpoint** | PUT o PATCH implementado correctamente | Endpoint de actualización básico | Intento de actualización      | Sin actualización   |
| **DELETE Endpoint**    | DELETE con manejo de errores           | DELETE básico funcional          | DELETE simple                 | DELETE no funciona  |
| **Data Persistence**   | Datos almacenados consistentemente     | Almacenamiento básico funcional  | Datos guardados temporalmente | Sin persistencia    |

#### 3. MANEJO DE ERRORES (20 puntos)

**Evidencia requerida**: HTTPException y manejo básico de errores

| Criterio                | Excelente (4pts)                   | Bueno (3pts)               | Suficiente (2pts)      | Insuficiente (0pts)     |
| ----------------------- | ---------------------------------- | -------------------------- | ---------------------- | ----------------------- |
| **HTTPException Usage** | HTTPException usado apropiadamente | HTTPException implementado | Excepciones básicas    | Sin manejo de errores   |
| **Status Codes**        | Códigos HTTP correctos (404, 422)  | Algunos códigos correctos  | Códigos básicos usados | Códigos incorrectos     |
| **Error Messages**      | Mensajes claros y útiles           | Mensajes informativos      | Mensajes básicos       | Mensajes confusos       |
| **Error Scenarios**     | Varios escenarios manejados        | Errores principales        | Errores básicos        | Sin escenarios de error |
| **Consistency**         | Manejo consistente en toda la API  | Manejo mayormente presente | Manejo parcial         | Sin consistencia        |

#### 4. TESTING Y VERIFICACIÓN (15 puntos)

**Evidencia requerida**: Pruebas documentadas de funcionalidad

| Criterio                   | Excelente (3pts)                          | Bueno (2pts)                      | Suficiente (1pt)              | Insuficiente (0pts)          |
| -------------------------- | ----------------------------------------- | --------------------------------- | ----------------------------- | ---------------------------- |
| **CRUD Testing**           | Todos los endpoints CRUD probados         | Endpoints principales probados    | Testing básico realizado      | Sin pruebas CRUD             |
| **Validation Testing**     | Pruebas de validación exitosas y fallidas | Algunas pruebas de validación     | Validación básica probada     | Sin pruebas de validación    |
| **Error Handling Testing** | Escenarios de error probados              | Algunos errores probados          | Errores básicos identificados | Sin testing de errores       |
| **Documentation Testing**  | /docs accesible y funcional               | Documentación automática funciona | Docs básicamente accesible    | Documentación no funciona    |
| **Response Validation**    | Respuestas verificadas y documentadas     | Respuestas básicas verificadas    | Verificación mínima           | Sin validación de respuestas |

#### 5. ENTREGABLES Y ORGANIZACIÓN (10 puntos)

**Evidencia requerida**: Proyecto completo y bien organizado

| Criterio                    | Excelente (2pts)                           | Bueno (1.5pts)                 | Suficiente (1pt)             | Insuficiente (0pts)         |
| --------------------------- | ------------------------------------------ | ------------------------------ | ---------------------------- | --------------------------- |
| **Code Organization**       | Código limpio, modular y bien comentado    | Código organizado y claro      | Código funcional básico      | Código desorganizado        |
| **GitHub Repository**       | Commits descriptivos y progresión clara    | Repo actualizado regularmente  | Código subido al final       | Sin repo o incompleto       |
| **README Quality**          | README completo con instrucciones claras   | README actualizado básicamente | README mínimo actualizado    | README no actualizado       |
| **Requirements Management** | requirements.txt actualizado correctamente | Dependencias gestionadas       | Lista básica de dependencias | Sin gestión de dependencias |
| **Delivery Quality**        | Entrega completa y a tiempo                | Entrega a tiempo con calidad   | Entrega básica completa      | Entrega incompleta o tardía |

### ESCALA DE CALIFICACIÓN

- **Excelente (90-100 pts)**: Dominio sólido de validación y manejo de errores
- **Bueno (80-89 pts)**: Comprensión correcta con implementación funcional
- **Suficiente (70-79 pts)**: Conceptos básicos logrados, necesita práctica adicional
- **Insuficiente (0-69 pts)**: Requiere refuerzo en conceptos fundamentales

### CRITERIOS DE APROBACIÓN

- **Mínimo para aprobar**: 70 puntos (70%)
- **Entregables obligatorios**:
  - Al menos 1 validador personalizado funcionando
  - Endpoints CRUD básicos implementados
  - Manejo básico de errores con HTTPException
  - API documentada automáticamente funcional

### RETROALIMENTACIÓN AUTOMÁTICA

**Para el agente evaluador de IA:**

#### Puntos de verificación automática

1. **Pydantic Field Usage**: Verificar uso de Field() con constraints (min_length, max_length, gt, etc.)
2. **Custom Validators**: Identificar al menos un @validator personalizado en modelos
3. **HTTPException Usage**: Confirmar que HTTPException se usa para manejo de errores
4. **CRUD Endpoints**: Verificar presencia de GET, POST, PUT/PATCH, DELETE endpoints
5. **Status Codes**: Validar uso apropiado de códigos HTTP (200, 201, 404, 422)
6. **Documentation**: Confirmar que /docs es accesible y muestra endpoints correctamente
7. **Error Responses**: Verificar que errores retornan respuestas JSON apropiadas
8. **Model Integration**: Confirmar que modelos Pydantic se usan en todos los endpoints principales

#### Patrones de código a verificar

```python
# Validación Field()
name: str = Field(..., min_length=1, max_length=100)

# Validador personalizado
@validator('field_name')
def validate_field(cls, v):
    # validation logic
    return v

# Manejo de errores
raise HTTPException(status_code=404, detail="Item not found")

# Endpoint con modelo
@app.post("/items/", response_model=ItemResponse)
async def create_item(item: ItemCreate):
```

#### Estructura de archivos esperada

```text
├── main.py              # API principal con endpoints
├── models.py            # Modelos Pydantic con validaciones
├── requirements.txt     # FastAPI, uvicorn, pydantic
└── README.md           # Instrucciones de uso
```

---

_Rúbrica actualizada: 26 de julio de 2025_  
_Bootcamp FastAPI - EPTI Development_
