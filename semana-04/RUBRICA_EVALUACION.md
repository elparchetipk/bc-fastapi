# RÚBRICA DE EVALUACIÓN - SEMANA 4

## Bases de Datos con FastAPI

### INFORMACIÓN GENERAL

- **Semana**: 4
- **Tema**: SQLAlchemy, CRUD con Base de Datos y Testing Básico
- **Duración**: 6 horas (incluye break de 30 min)
- **Prerequisitos**: Semana 3 aprobada (Validación y manejo de errores funcionando)
- **Modalidad**: Evaluación automática por IA + revisión manual

### CRITERIOS DE EVALUACIÓN

#### 1. CONFIGURACIÓN DE BASE DE DATOS (25 puntos)

**Evidencia requerida**: SQLAlchemy configurado y funcionando con SQLite

| Criterio                | Excelente (5pts)                       | Bueno (4pts)                 | Suficiente (3pts)           | Insuficiente (0pts)       |
| ----------------------- | -------------------------------------- | ---------------------------- | --------------------------- | ------------------------- |
| **SQLAlchemy Setup**    | Configuración completa con database.py | Setup básico funcional       | Conexión simple funcionando | SQLAlchemy no configurado |
| **Database Connection** | Conexión estable sin errores           | Conexión funcional           | Conexión básica             | No hay conexión           |
| **Base Model**          | Base declarativa configurada           | Base model creado            | Modelo base simple          | Sin modelo base           |
| **Session Management**  | get_db() dependency funcionando        | Gestión básica de sesiones   | Sesión manual               | Sin gestión de sesiones   |
| **Table Creation**      | Tablas creadas automáticamente         | Comando de creación funciona | Tablas creadas manualmente  | Sin creación de tablas    |

#### 2. MODELOS DE DATOS (25 puntos)

**Evidencia requerida**: Modelos SQLAlchemy y schemas Pydantic funcionales

| Criterio              | Excelente (5pts)                                   | Bueno (4pts)                  | Suficiente (3pts)       | Insuficiente (0pts)  |
| --------------------- | -------------------------------------------------- | ----------------------------- | ----------------------- | -------------------- |
| **SQLAlchemy Models** | Modelos con campos y tipos apropiados              | Modelos básicos funcionales   | Modelos simples creados | Modelos no funcionan |
| **Pydantic Schemas**  | Schemas para Create/Response definidos             | Schemas básicos implementados | Algunos schemas creados | Sin schemas          |
| **Relationships**     | Relación One-to-Many implementada                  | Relación simple funcionando   | Foreign key básico      | Sin relaciones       |
| **Field Types**       | Tipos de datos apropiados (String, Integer, Float) | Tipos básicos correctos       | Algunos tipos correctos | Tipos incorrectos    |
| **Model Integration** | Modelos integrados correctamente                   | Integración básica funcional  | Integración parcial     | Sin integración      |

#### 3. OPERACIONES CRUD (30 puntos)

**Evidencia requerida**: Endpoints CRUD funcionando con base de datos

| Criterio             | Excelente (6pts)                | Bueno (5pts)                  | Suficiente (3pts)            | Insuficiente (0pts)   |
| -------------------- | ------------------------------- | ----------------------------- | ---------------------------- | --------------------- |
| **Create Operation** | POST endpoint creando en BD     | Create básico funcional       | Endpoint POST simple         | Create no funciona    |
| **Read Operations**  | GET list y GET by ID desde BD   | Read básico desde BD          | Endpoint GET simple          | Read no funciona      |
| **Update Operation** | PUT/PATCH actualizando BD       | Update básico funcional       | Intento de update            | Update no funciona    |
| **Delete Operation** | DELETE removiendo de BD         | Delete básico funcional       | Delete simple                | Delete no funciona    |
| **Data Persistence** | Datos persistidos correctamente | Persistencia básica funcional | Datos guardados parcialmente | Sin persistencia real |

#### 4. BÚSQUEDAS Y VALIDACIONES (15 puntos)

**Evidencia requerida**: Búsquedas básicas y validaciones funcionando

| Criterio                 | Excelente (3pts)                       | Bueno (2pts)                 | Suficiente (1pt)   | Insuficiente (0pts)    |
| ------------------------ | -------------------------------------- | ---------------------------- | ------------------ | ---------------------- |
| **Search Functionality** | Búsqueda por título/nombre funcionando | Búsqueda básica implementada | Filtro simple      | Sin búsquedas          |
| **Query Parameters**     | Query params para filtros              | Parámetros básicos usados    | Algunos parámetros | Sin query parameters   |
| **Data Validation**      | Validaciones en schemas funcionando    | Validaciones básicas         | Validación mínima  | Sin validaciones       |
| **Error Handling**       | Errores 404, 422 manejados             | Algunos errores manejados    | Errores básicos    | Sin manejo de errores  |
| **Response Formatting**  | Respuestas bien estructuradas          | Formato básico correcto      | Respuestas simples | Respuestas malformadas |

#### 5. ENTREGABLES Y ORGANIZACIÓN (5 puntos)

**Evidencia requerida**: Proyecto completo y bien organizado

| Criterio                    | Excelente (1pt)                            | Bueno (0.75pts)                | Suficiente (0.5pts)          | Insuficiente (0pts)         |
| --------------------------- | ------------------------------------------ | ------------------------------ | ---------------------------- | --------------------------- |
| **Code Organization**       | Archivos separados (models, schemas, crud) | Código organizado básicamente  | Código funcional simple      | Código desorganizado        |
| **GitHub Repository**       | Commits descriptivos y progresión clara    | Repo actualizado regularmente  | Código subido al final       | Sin repo o incompleto       |
| **README Updates**          | README con instrucciones de BD             | README actualizado básicamente | README mínimo actualizado    | README no actualizado       |
| **Requirements Management** | requirements.txt con SQLAlchemy            | Dependencias gestionadas       | Lista básica de dependencias | Sin gestión de dependencias |
| **Delivery Quality**        | Entrega completa y a tiempo                | Entrega a tiempo con calidad   | Entrega básica completa      | Entrega incompleta o tardía |

### ESCALA DE CALIFICACIÓN

- **Excelente (90-100 pts)**: Dominio sólido de bases de datos con FastAPI
- **Bueno (80-89 pts)**: Comprensión correcta con implementación funcional
- **Suficiente (70-79 pts)**: Conceptos básicos logrados, necesita práctica adicional
- **Insuficiente (0-69 pts)**: Requiere refuerzo en conceptos fundamentales

### ENTREGABLES ESPECÍFICOS

#### Archivos Requeridos

- `main.py` - Aplicación FastAPI con endpoints CRUD
- `database.py` - Configuración de SQLAlchemy
- `models.py` - Modelos SQLAlchemy
- `schemas.py` - Schemas Pydantic
- `crud.py` - Funciones de base de datos (opcional)
- `requirements.txt` - Dependencias incluyendo SQLAlchemy
- `README.md` - Instrucciones actualizadas

#### Funcionalidades Mínimas

- ✅ **Conexión a SQLite** funcionando
- ✅ **Modelo básico** (ej: Producto con id, nombre, precio)
- ✅ **CRUD completo** - Create, Read, Update, Delete
- ✅ **Schemas Pydantic** para validación
- ✅ **Búsqueda básica** por parámetro
- ✅ **Manejo de errores** 404 y 422

#### Testing Básico

- ✅ **Manual testing** de todos los endpoints
- ✅ **Documentación automática** (/docs) funcionando
- ✅ **Datos persistidos** entre reinicios del servidor
- ✅ **Validaciones** funcionando correctamente

---

**Nota**: Esta rúbrica enfatiza funcionalidad básica y sólida comprensión de conceptos fundamentales sobre complejidad avanzada.
