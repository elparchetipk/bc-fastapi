# Semana 4: Bases de Datos con FastAPI (Ajustado)

## 🎯 Objetivos de la Semana

Al finalizar esta semana, los estudiantes podrán:

- **Integrar SQLAlchemy** con FastAPI para persistencia básica
- **Diseñar modelos de base de datos** relacionales simples
- **Implementar CRUD completo** con base de datos SQLite
- **Aplicar validaciones** de reglas de negocio básicas
- **Realizar testing** básico con bases de datos

## ⏱️ Distribución de Tiempo (6 horas total)

| Bloque | Actividad                  | Tiempo | Descripción                              |
| ------ | -------------------------- | ------ | ---------------------------------------- |
| **1**  | Configuración BD + Modelos | 90 min | SQLAlchemy setup, modelos básicos        |
| **2**  | CRUD Básico                | 90 min | Operaciones Create, Read, Update, Delete |
| **3**  | Relaciones Simples         | 90 min | Foreign keys, consultas básicas          |
| **4**  | Testing y Validaciones     | 90 min | pytest básico, reglas de negocio         |

## ⚙️ Configuración Previa

> **🔧 VS Code Setup**: Para evitar errores de importación con SQLAlchemy, FastAPI y Pydantic, consulta la [Guía de Configuración de VS Code](../recursos-compartidos/GUIA_CONFIGURACION_VSCODE.md) y la [Configuración Rápida](./CONFIGURACION_VSCODE.md)

## 📚 Contenido de la Semana

### **📋 Navegación Ordenada (Seguir este orden)**

1. **[🧭 1-teoria/](./1-teoria/)** - Conceptos de bases de datos
2. **[💻 2-practica/](./2-practica/)** - Implementación SQLAlchemy
3. **[🎯 3-ejercicios/](./3-ejercicios/)** - Refuerzo y práctica
4. **[🚀 4-proyecto/](./4-proyecto/)** - API completa con BD
5. **[📚 5-recursos/](./5-recursos/)** - Referencias y apoyo

### **🧭 Teoría**

- [📖 Bases de Datos y ORMs](./1-teoria/database-concepts.md)

### **💻 Prácticas**

1. [🔧 SQLAlchemy + FastAPI Setup](./2-practica/11-sqlalchemy-setup.md) _(90 min)_
2. [📊 CRUD con Base de Datos](./2-practica/12-database-crud.md) _(90 min)_
3. [🔗 Relaciones y Consultas](./2-practica/13-relations-queries.md) _(90 min)_
4. [🚀 Migraciones y Testing](./2-practica/14-migrations-testing.md) _(90 min)_

### **💪 Ejercicios**

- [🎯 Ejercicios de BD](./3-ejercicios/ejercicios-practica.md)

### **🚀 Proyecto**

- [📋 API de Biblioteca con BD](./4-proyecto/especificacion-proyecto.md) ⭐ **AJUSTADO**

**Proyecto Simplificado:** Sistema de gestión de biblioteca con 3 entidades (Book, User, Loan), CRUD completo y reglas de negocio básicas. Tiempo estimado: 5.5 horas.

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

## 📅 Cronograma de la Jornada de 6 Horas

| Tiempo      | Actividad                | Duración | Acumulado |
| ----------- | ------------------------ | -------- | --------- |
| 12:00-13:30 | SQLAlchemy Setup         | 90 min   | 90 min    |
| 13:30-14:00 | CRUD con BD (parte 1)    | 30 min   | 120 min   |
| 14:00-14:30 | **☕ BREAK OBLIGATORIO** | 30 min   | 150 min   |
| 14:30-15:30 | CRUD con BD (parte 2)    | 60 min   | 210 min   |
| 15:30-17:00 | Relaciones y Consultas   | 90 min   | 300 min   |
| 17:00-18:00 | Migraciones y Testing    | 60 min   | 360 min   |

**Total**: Exactamente 6 horas (360 minutos)

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
