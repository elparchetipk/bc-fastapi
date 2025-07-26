# Rúbrica de Evaluación - Semana 4: Bases de Datos con FastAPI

## 📊 Información General

**Proyecto**: API E-commerce con Base de Datos  
**Tiempo asignado**: 6 horas  
**Peso en curso**: 20%  
**Tipo**: Evaluación sumativa

---

## 🎯 Criterios de Evaluación

### **1. Configuración Base de Datos (25 puntos - 25%)**

#### **Excelente (23-25 puntos)**

- ✅ **SQLAlchemy configurado** correctamente con FastAPI
- ✅ **Conexión a BD** funcionando sin errores
- ✅ **Variables de entorno** para configuración de BD
- ✅ **Modelos base** bien estructurados
- ✅ **Alembic configurado** para migraciones
- ✅ **Testing con BD** en memoria funcionando

#### **Bueno (19-22 puntos)**

- ✅ **SQLAlchemy funcional** con configuración básica
- ✅ **Conexión establecida** correctamente
- ✅ **Modelos básicos** creados y funcionales
- ⚠️ **Configuración** hardcodeada (sin variables entorno)
- ⚠️ **Alembic** configurado pero sin usar
- ⚠️ **Testing limitado** o sin BD de prueba

#### **Satisfactorio (15-18 puntos)**

- ✅ **SQLAlchemy conectado** pero con configuración simple
- ✅ **Modelo básico** funcionando
- ❌ **Sin variables de entorno**
- ❌ **Sin Alembic** configurado
- ❌ **Sin testing** con BD

#### **Necesita Mejora (0-14 puntos)**

- ❌ **Errores de conexión** a base de datos
- ❌ **SQLAlchemy mal configurado**
- ❌ **Modelos no funcionan**
- ❌ **No hay evidencia** de setup correcto

---

### **2. Modelos de Datos (25 puntos - 25%)**

#### **Excelente (23-25 puntos)**

- ✅ **Esquema bien diseñado** con relaciones apropiadas
- ✅ **Modelos SQLAlchemy** correctamente definidos
- ✅ **Relaciones FK** implementadas y funcionando
- ✅ **Campos apropiados** con tipos correctos
- ✅ **Constraints y validaciones** en BD
- ✅ **Modelos Pydantic** correspondientes para API

#### **Bueno (19-22 puntos)**

- ✅ **Modelos bien estructurados** con campos apropiados
- ✅ **Algunas relaciones** implementadas correctamente
- ✅ **Tipos de datos** correctos
- ⚠️ **Relaciones básicas** (solo FK simples)
- ⚠️ **Validaciones limitadas**
- ⚠️ **Algunos modelos Pydantic** faltantes

#### **Satisfactorio (15-18 puntos)**

- ✅ **Modelos básicos** funcionando
- ✅ **Campos principales** definidos
- ❌ **Sin relaciones** entre tablas
- ❌ **Tipos de datos** básicos únicamente
- ❌ **Sin validaciones** adicionales

#### **Necesita Mejora (0-14 puntos)**

- ❌ **Errores en definición** de modelos
- ❌ **Campos faltantes** o incorrectos
- ❌ **No funciona** con SQLAlchemy
- ❌ **Diseño de esquema** deficiente

---

### **3. CRUD Funcional (30 puntos - 30%)**

#### **Excelente (27-30 puntos)**

- ✅ **Todos los endpoints CRUD** implementados y funcionales
- ✅ **Create, Read, Update, Delete** trabajando perfectamente
- ✅ **Relaciones manejadas** en operaciones
- ✅ **Paginación** implementada en GET
- ✅ **Filtros y búsqueda** funcionando
- ✅ **Manejo de errores** de BD apropiado
- ✅ **Transacciones** manejadas correctamente

#### **Bueno (22-26 puntos)**

- ✅ **CRUD básico completo** y funcional
- ✅ **Operaciones principales** trabajando bien
- ✅ **Algunas relaciones** manejadas
- ⚠️ **Paginación básica** o sin implementar
- ⚠️ **Filtros limitados**
- ⚠️ **Manejo de errores** básico

#### **Satisfactorio (17-21 puntos)**

- ✅ **Operaciones básicas** (Create, Read) funcionando
- ✅ **GET y POST** implementados
- ❌ **Update/Delete** faltantes o con errores
- ❌ **Sin manejo** de relaciones
- ❌ **Errores de BD** no manejados

#### **Necesita Mejora (0-16 puntos)**

- ❌ **CRUD no funcional** o con errores graves
- ❌ **Operaciones básicas** fallan
- ❌ **Endpoints** devuelven errores
- ❌ **No persiste** datos correctamente

---

### **4. Testing y Calidad (20 puntos - 20%)**

#### **Excelente (18-20 puntos)**

- ✅ **Tests completos** para todos los endpoints
- ✅ **BD de prueba** configurada y funcionando
- ✅ **Setup/teardown** de tests correcto
- ✅ **Test cases** comprehensivos (happy path + edge cases)
- ✅ **Fixtures** bien organizadas
- ✅ **Código limpio** y bien organizado
- ✅ **Documentación** de API completa

#### **Bueno (15-17 puntos)**

- ✅ **Tests básicos** para endpoints principales
- ✅ **BD de prueba** funcionando
- ✅ **Happy path** cubierto en tests
- ⚠️ **Setup de tests** básico
- ⚠️ **Edge cases** limitados
- ⚠️ **Organización** mejorable

#### **Satisfactorio (11-14 puntos)**

- ✅ **Algunos tests** funcionando
- ✅ **Testing manual** documentado
- ❌ **BD de prueba** no configurada
- ❌ **Tests limitados** o básicos
- ❌ **Sin documentación** de API

#### **Necesita Mejora (0-10 puntos)**

- ❌ **Sin tests** automatizados
- ❌ **Solo testing manual** sin documentar
- ❌ **Código desorganizado**
- ❌ **Sin evidencia** de testing

---

## 🎯 Entregables Requeridos

### **📦 Entregable Principal**

**Repositorio GitHub** con:

```
semana-04-proyecto/
├── app/
│   ├── main.py              # FastAPI app principal
│   ├── database.py          # Configuración SQLAlchemy
│   ├── models/              # Modelos SQLAlchemy
│   ├── schemas/             # Modelos Pydantic
│   ├── crud/                # Operaciones de BD
│   └── routers/             # Endpoints organizados
├── alembic/                 # Migraciones
├── tests/                   # Tests automatizados
├── requirements.txt         # Dependencias
├── .env.example            # Variables de entorno
├── README.md               # Documentación
└── database.db             # BD SQLite (si aplica)
```

### **📋 Documentación Requerida**

1. **README.md** con:

   - Instrucciones de instalación
   - Cómo ejecutar la aplicación
   - Endpoints disponibles
   - Ejemplos de uso

2. **Colección Postman** o equivalente con:

   - Todos los endpoints
   - Ejemplos de requests/responses
   - Tests de funcionalidad

3. **Evidencia de Testing**:
   - Screenshots de tests pasando
   - Cobertura de código (opcional)
   - Documentación de casos de prueba

---

## 📊 Cálculo de Calificación

### **Escala de Puntos**

| Criterio          | Peso     | Puntos Máximos |
| ----------------- | -------- | -------------- |
| Configuración BD  | 25%      | 25             |
| Modelos de Datos  | 25%      | 25             |
| CRUD Funcional    | 30%      | 30             |
| Testing y Calidad | 20%      | 20             |
| **TOTAL**         | **100%** | **100**        |

### **Escala de Calificación**

| Puntos | Calificación | Descripción                            |
| ------ | ------------ | -------------------------------------- |
| 90-100 | **A**        | Excelente - Cumple todos los objetivos |
| 80-89  | **B**        | Bueno - Cumple objetivos principales   |
| 70-79  | **C**        | Satisfactorio - Cumple mínimos         |
| 60-69  | **D**        | Necesita mejora - Objetivos parciales  |
| 0-59   | **F**        | Insuficiente - No cumple objetivos     |

---

## ⚠️ Consideraciones Especiales

### **Restricciones de Tiempo (6 horas)**

- ✅ **SQLite únicamente** - No se requiere PostgreSQL/MySQL
- ✅ **Relaciones básicas** - FK simples, no muchos-a-muchos complejos
- ✅ **Testing básico** - BD en memoria es suficiente
- ✅ **Migraciones simples** - Setup básico de Alembic

### **Criterios de Aceptación Mínima**

Para **APROBAR** la semana (70+ puntos) se requiere:

1. ✅ **SQLAlchemy funcionando** con al menos un modelo
2. ✅ **CRUD básico** (Create + Read) implementado
3. ✅ **API funcionando** sin errores graves
4. ✅ **Proyecto ejecutable** siguiendo README

### **Bonus (Puntos Extra)**

- 🌟 **+5 puntos**: Implementar autenticación básica
- 🌟 **+3 puntos**: Usar Docker para BD
- 🌟 **+2 puntos**: Tests con cobertura >80%
- 🌟 **+2 puntos**: Documentación OpenAPI personalizada

---

## 📝 Feedback y Mejora Continua

### **Durante la Evaluación**

- ✅ **Feedback inmediato** en errores críticos
- ✅ **Sugerencias específicas** de mejora
- ✅ **Reconocimiento** de buenas prácticas
- ✅ **Orientación** para correcciones

### **Post-Evaluación**

- 📋 **Informe detallado** por criterio
- 🎯 **Áreas de mejora** identificadas
- 📚 **Recursos adicionales** recomendados
- 🚀 **Preparación** para Semana 5

---

## ✅ Lista de Verificación Final

### **Para Estudiantes - Antes de Entregar**

- [ ] ✅ **Proyecto ejecuta** sin errores
- [ ] ✅ **Todos los endpoints** responden correctamente
- [ ] ✅ **BD se crea** automáticamente al ejecutar
- [ ] ✅ **Tests pasan** (si se implementaron)
- [ ] ✅ **README completo** con instrucciones
- [ ] ✅ **Código limpio** y organizado
- [ ] ✅ **Commit messages** descriptivos
- [ ] ✅ **Variables sensibles** en .env

### **Para Instructores - Durante Evaluación**

- [ ] ✅ **Clonar repositorio** y seguir README
- [ ] ✅ **Verificar instalación** de dependencias
- [ ] ✅ **Probar endpoints** manualmente
- [ ] ✅ **Revisar modelos** y relaciones
- [ ] ✅ **Ejecutar tests** si existen
- [ ] ✅ **Evaluar organización** del código
- [ ] ✅ **Documentar feedback** específico

---

**🎯 Objetivo**: Al completar esta evaluación, los estudiantes habrán demostrado capacidad para desarrollar APIs con persistencia real, preparándolos para proyectos más complejos en las siguientes semanas.

---

_Rúbrica actualizada: 24 de julio de 2025_
