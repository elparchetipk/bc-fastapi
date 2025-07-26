# Week 4: Query Parameters and Data Validation

⏰ **TOTAL DURATION: 6 HOURS EXACTLY**  
📚 **LEVEL: Intermediate (builds on Week 3)**

## 🚨 **IMPORTANT: Natural Progression**

This week is designed for students who **already have a complete CRUD API working** (Week 3). We'll learn query parameters, advanced validation, and data filtering.

- ✅ **Completely achievable in 6 hours**
- ✅ **Gradual progression from Week 3**
- ✅ **Focus on practical and functional concepts**

## 🎯 Week Objectives (Fundamental)

By the end of this 6-hour week (includes 30-min break), students will:

1. ✅ **Implement query parameters for filtering**
2. ✅ **Add data validation with Pydantic Field**
3. ✅ **Create search endpoints with multiple filters**
4. ✅ **Handle optional parameters and defaults**
5. ✅ **Be ready for more advanced API features**

### ❌ **What is NOT expected to master this week**

- Database integration (SQLAlchemy)
- Complex migrations or ORM concepts
- Advanced authentication
- File uploads or complex media handling
- Production deployment

## ⏱️ **6-Hour Structure (Includes 30-min Break)**

### **Block 1: Query Parameters Basics (75 min)**

- **10-query-parameters.md**
- Basic filtering with query params
- Optional parameters with defaults
- Type conversion and validation

### **☕ MANDATORY BREAK (30 min)**

- Rest to absorb query parameter concepts
- Time to resolve doubts about filtering
- Mental preparation for validation

### **Block 2: Advanced Validation (120 min)**

- **11-pydantic-validation.md**
- Field validation with constraints
- Custom validators
- Error handling for invalid data

### **Block 3: Search and Filtering (90 min)**

- **12-search-endpoints.md**
- Multiple filter combinations
- Search by text and ranges
- Pagination basics

### **Block 4: Data Processing (45 min)**

- Integration of all concepts
- Complete API with advanced features
- Deliverable preparation

## 📚 Week Content (Only Essentials)

### **🧭 Ordered Navigation (Follow this order)**

1. **[🧭 1-teoria/](./1-teoria/)** - Query parameters and validation concepts
2. **[💻 2-practica/](./2-practica/)** - Step-by-step implementation
3. **[🎯 3-ejercicios/](./3-ejercicios/)** - Practical reinforcement
4. **[🚀 4-proyecto/](./4-proyecto/)** - Advanced API with filtering
5. **[📚 5-recursos/](./5-recursos/)** - Basic references

### 🛠️ **Practices (Week Core)**

1. **[10-query-parameters.md](./2-practica/10-query-parameters.md)** - Basic filtering
2. **[11-pydantic-validation.md](./2-practica/11-pydantic-validation.md)** - Data validation
3. **[12-search-endpoints.md](./2-practica/12-search-endpoints.md)** - Search functionality

### 📖 **Theory (Minimal)**

- Query parameters fundamentals
- Pydantic Field validation
- Basic filtering concepts

### 🏋️ **Exercises (Consolidation)**

- 2 exercises on filtering and validation
- Functionality verification

## 🚀 **Prerequisites (From Week 3)**

- ✅ Complete CRUD API working
- ✅ Error handling with HTTPException
- ✅ Pydantic models implemented
- ✅ All HTTP methods functioning

## 🎯 Week Success Criteria

### ✅ **Success Criteria (Pass/Fail)**

- [ ] At least 2 query parameters working for filtering
- [ ] Field validation with Pydantic Field implemented
- [ ] Search endpoint with text filtering
- [ ] Proper handling of optional parameters

### 🌟 **Optional Bonus (No pressure)**

- [ ] Pagination implementation
- [ ] Range filtering (dates, numbers)
- [ ] Multiple search criteria combination

---

## 📋 Week Deliverables

### 🔧 **Main Deliverable (Only Required)**

**API with Advanced Query Features**

- ✅ Week 3 API + new query features
- ✅ At least 2 query parameters for filtering
- ✅ Field validation with constraints
- ✅ Search endpoint with text filtering
- ✅ Proper error handling for invalid queries

### 📄 **Documentation Deliverable (Minimum)**

**Updated README.md**

- ✅ Description of all query parameters
- ✅ Examples of filtering and search usage
- ✅ 2-3 sentence reflection on progress

### 🎯 **Delivery Format**

1. **Updated GitHub repository** with:

   - main.py with query parameters
   - Updated requirements.txt
   - README.md with all filtering options

2. **No video required**

### ⏰ **Delivery Date**

- **At the end of the 6-hour session**
- **Immediate delivery, no homework**

## 📊 Simplified Evaluation

Evaluation focuses on **query functionality**:

- **Query Parameters (50%)**: Do filtering parameters work?
- **Validation (30%)**: Is Field validation implemented?
- **Search (15%)**: Does text search work?
- **Delivery (5%)**: Is it updated on GitHub?

### 🏆 Pass Criteria

- **✅ Passed**: Query parameters + validation working + code on GitHub
- **❌ Pending**: Additional support in next session

## 🎁 Bonus Opportunities (Only if extra time)

- **Pagination implementation**: +5 points
- **Range filtering**: +3 points
- **Advanced search combinations**: +2 points

## 📅 6-Hour Session Schedule

| Time        | Activity                 | Duration | Cumulative |
| ----------- | ------------------------ | -------- | ---------- |
| 9:00-10:15  | Query parameters basics  | 75 min   | 75 min     |
| 10:15-10:45 | **☕ MANDATORY BREAK**   | 30 min   | 105 min    |
| 10:45-12:45 | Advanced validation      | 120 min  | 225 min    |
| 12:45-14:15 | Search endpoints         | 90 min   | 315 min    |
| 14:15-15:00 | Integration and delivery | 45 min   | 360 min    |

**Total**: Exactly 6 hours (360 minutes)

## 🔍 Delivery Structure

### 📁 Expected Structure

```
lastname-firstname-week4/
├── README.md               # With query parameters documentation
├── requirements.txt        # FastAPI + pydantic + uvicorn
└── main.py                # API with query parameters and validation
```

### 🚀 Simple Delivery Process

1. **Evolve existing repository**

   - Add query parameters to main.py
   - Update README with filtering examples
   - Commit with descriptive message

2. **Class Demonstration**

   - Show filtering working
   - Demonstrate validation errors
   - Show updated /docs with query params

3. **Deadline**
   - **At the end of the 6-hour class**
   - **No extensions**

## 🤝 Support Resources

### 👥 Help During Class

- **Instructor**: Available throughout the session
- **Classmates**: Collaborative work allowed
- **Documentation**: FastAPI docs + Pydantic Field docs

### 🔧 Basic Tools

- **Same tools from Week 3**
- **Postman/Thunder Client**: To test query parameters
- **Browser**: To see updated /docs with filters

## 🎯 Preparation for Week 5

With this advanced API working, in Week 5 you'll learn:

- **File handling**: Upload and download files
- **Response formatting**: Custom response models
- **Basic middleware**: Request/response processing

## 📞 Contact (Emergencies Only)

- **During class**: Raise hand or chat
- **Outside hours**: Not required, everything resolved in class

---

## 🌟 Final Motivation Message

This fourth week completes your **fundamental API knowledge**. With query parameters and validation, you'll have a professional-grade API foundation.

**Remember**:

- ✅ You build on the solid progress from Weeks 1-3
- ✅ The 30-min break is mandatory to absorb concepts
- ✅ Query parameters are used in most real-world APIs
- ✅ These concepts will apply in all following weeks

**Your API is now smart and flexible! 🚀**

### **📚 Recursos**

- [🔗 Enlaces y Referencias](./5-recursos/recursos-apoyo.md)

## 📚 Contenido de la Semana

### **🧭 Teoría**

- [📖 Bases de Datos y ORMs](./teoria/databases-orm-concepts.md)

### **💻 Prácticas**

1. [🔧 SQLAlchemy Setup](./practica/11-sqlalchemy-setup.md) _(90 min)_
2. [💾 CRUD con Base de Datos](./practica/12-crud-database.md) _(90 min)_
3. [🔗 Relaciones y Consultas](./practica/13-relaciones-consultas.md) _(90 min)_
4. [⚙️ Migraciones y Testing](./practica/14-migraciones-testing.md) _(90 min)_

### **💪 Ejercicios**

- [🎯 Ejercicios de Base de Datos](./ejercicios/ejercicios-practica.md)

### **🚀 Proyecto**

- [📋 Sistema de Biblioteca](./proyecto/especificacion-proyecto.md)

### **📚 Recursos**

- [🔗 Enlaces y Referencias](./5-recursos/recursos-apoyo.md)

## 🎯 Objetivos Específicos

### **Conocimientos**

- ✅ Conceptos de ORM y SQLAlchemy
- ✅ Modelos de datos relacionales
- ✅ Migraciones de base de datos
- ✅ Testing con bases de datos

### **Habilidades**

- ✅ Configurar SQLAlchemy con FastAPI
- ✅ Crear modelos de base de datos
- ✅ Implementar CRUD persistente
- ✅ Escribir consultas eficientes
- ✅ Manejar relaciones entre tablas
- ✅ Testing de endpoints con BD

### **Actitudes**

- ✅ Responsabilidad con la persistencia de datos
- ✅ Atención al diseño de esquemas
- ✅ Disciplina en testing de bases de datos

## 🛠️ Tecnologías Utilizadas

### **Principales**

- **SQLAlchemy** - ORM para Python
- **Alembic** - Migraciones de BD
- **SQLite** - Base de datos de desarrollo
- **FastAPI** - Framework web

### **Testing y Desarrollo**

- **pytest** - Framework de testing
- **pytest-asyncio** - Testing asíncrono
- **SQLite in-memory** - BD de prueba

## 📋 Pre-requisitos

### **Conocimientos Técnicos**

- ✅ **Semana 3 completada** - APIs REST con validación
- ✅ **Modelos Pydantic** - Response/Request models
- ✅ **FastAPI intermedio** - Endpoints HTTP completos
- ✅ **Python básico** - POO y conceptos de BD

### **Herramientas**

- ✅ **Python 3.8+** instalado y configurado
- ✅ **FastAPI** y dependencias funcionando
- ✅ **IDE** con soporte SQLAlchemy (VS Code recomendado)
- ✅ **Git** para control de versiones

## 🎯 Entregables de la Semana

### **📦 Proyecto Principal: API E-commerce con BD**

- **API completa** con persistencia en base de datos
- **Modelos**: Productos, Categorías, Inventario
- **CRUD completo** para todas las entidades
- **Relaciones** entre tablas implementadas
- **Migraciones** documentadas y funcionales
- **Testing** de endpoints con base de datos

### **📋 Criterios de Evaluación**

1. **Configuración BD (25%)** - SQLAlchemy setup correcto
2. **Modelos de Datos (25%)** - Esquema bien diseñado
3. **CRUD Funcional (30%)** - Operaciones completas
4. **Testing (20%)** - Pruebas con BD de prueba

## 🔗 Conexión con Otras Semanas

### **Desde Semana 3**

- **APIs REST** → Se persisten en base de datos
- **Validación robusta** → Se aplica a modelos de BD
- **Manejo de errores** → Se extiende a errores de BD
- **Estructura código** → Se organiza con capas de persistencia

### **Hacia Semana 5**

- **Base de datos sólida** → APIs más complejas
- **Relaciones** → Consultas avanzadas y optimización
- **Testing patterns** → CI/CD con bases de datos
- **Migraciones** → Deployment y versionado de esquemas

## ⚠️ Consideraciones Importantes

### **Scope de 6 Horas**

- ✅ **SQLite únicamente** - No PostgreSQL/MySQL en esta semana
- ✅ **Relaciones básicas** - FK simples, no muchos-a-muchos complejos
- ✅ **Migraciones básicas** - Alembic setup, no advanced features
- ✅ **Testing simple** - BD en memoria, no complex fixtures

### **Enfoque Práctico**

- ✅ **Hands-on desde minuto 1** - Menos teoría, más código
- ✅ **Proyecto incremental** - Build up durante las 4 prácticas
- ✅ **Validación inmediata** - Testing después de cada feature
- ✅ **Debugging incluido** - Cómo resolver errores comunes

## 📊 Cronograma Detallado

### **🕐 Bloque 1: SQLAlchemy Setup (90 min)**

- **0-15 min**: Introducción y objetivos
- **15-45 min**: Instalación y configuración básica
- **45-75 min**: Primer modelo y conexión
- **75-90 min**: Testing de configuración

### **🕑 Bloque 2: CRUD con BD (90 min)**

- **0-20 min**: Revisión y setup
- **20-50 min**: Implementar operaciones Create/Read
- **50-80 min**: Implementar Update/Delete
- **80-90 min**: Testing de CRUD completo

### **🕒 Bloque 3: Relaciones y Consultas (90 min)**

- **0-15 min**: Conceptos de relaciones
- **15-50 min**: Implementar Foreign Keys
- **50-80 min**: Consultas con joins básicos
- **80-90 min**: Testing de relaciones

### **🕓 Bloque 4: Migraciones y Testing (90 min)**

- **0-20 min**: Setup de Alembic
- **20-45 min**: Primera migración
- **45-75 min**: Testing con BD de prueba
- **75-90 min**: Review final y deployment

## 🎉 Resultado Esperado

Al completar esta semana, tendrás una **API REST completa** con:

- ✅ **Persistencia real** en SQLite
- ✅ **Modelos relacionales** bien diseñados
- ✅ **CRUD funcional** para múltiples entidades
- ✅ **Testing robusto** con bases de datos
- ✅ **Migraciones** documentadas y reproducibles

🚀 **Preparado para APIs de producción con bases de datos robustas**

---

_Última actualización: 24 de julio de 2025_
