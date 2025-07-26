# Rúbrica de Evaluación - Semana 3: FastAPI Intermedio

## 📊 Información General

**Proyecto**: API de Inventario Simple  
**Tiempo asignado**: 6 horas  
**Peso en curso**: 15%  
**Tipo**: Evaluación sumativa

---

## 🎯 Criterios de Evaluación

### **1. Funcionalidad CRUD (30 puntos - 30%)**

#### **Excelente (26-30 puntos)**

- ✅ **Todos los endpoints implementados** y funcionales
- ✅ **GET, POST, PUT, DELETE** trabajando correctamente
- ✅ **Operaciones complejas** (búsqueda, filtros) implementadas
- ✅ **Responses consistentes** en todos los endpoints
- ✅ **Edge cases manejados** apropiadamente

#### **Bueno (21-25 puntos)**

- ✅ **Endpoints principales** implementados y funcionales
- ✅ **CRUD básico** working completamente
- ✅ **Mayoría de operaciones** funcionan correctamente
- ⚠️ **Algunos edge cases** no manejados
- ⚠️ **Responses** mayormente consistentes

#### **Satisfactorio (16-20 puntos)**

- ✅ **Endpoints básicos** implementados
- ✅ **Operaciones principales** funcionan
- ⚠️ **Algunas funcionalidades** incompletas o con errores
- ⚠️ **Responses** parcialmente consistentes
- ❌ **Edge cases** no considerados

#### **Necesita Mejora (0-15 puntos)**

- ❌ **Endpoints incompletos** o no funcionales
- ❌ **Errores frecuentes** en operaciones
- ❌ **Funcionalidad básica** no implementada
- ❌ **Responses inconsistentes** o incorrectas

---

### **2. Validación de Datos (25 puntos - 25%)**

#### **Excelente (23-25 puntos)**

- ✅ **Validación robusta** en todos los endpoints
- ✅ **Path, Query, Body** parámetros validados correctamente
- ✅ **Mensajes de error** claros y específicos
- ✅ **Tipos de datos** apropiados y consistentes
- ✅ **Validaciones custom** cuando corresponde

#### **Bueno (19-22 puntos)**

- ✅ **Validación presente** en endpoints principales
- ✅ **Tipos básicos** validados correctamente
- ✅ **Mensajes de error** informativos
- ⚠️ **Algunas validaciones** pueden ser más específicas
- ⚠️ **Validaciones custom** limitadas

#### **Satisfactorio (15-18 puntos)**

- ✅ **Validación básica** implementada
- ⚠️ **Algunos endpoints** sin validación completa
- ⚠️ **Mensajes de error** genéricos
- ⚠️ **Tipos de datos** apropiados pero básicos

#### **Necesita Mejora (0-14 puntos)**

- ❌ **Validación insuficiente** o ausente
- ❌ **Tipos de datos** incorrectos o inconsistentes
- ❌ **Sin manejo** de datos inválidos
- ❌ **Mensajes de error** ausentes o confusos

---

### **3. Manejo de Errores (20 puntos - 20%)**

#### **Excelente (18-20 puntos)**

- ✅ **HTTPException** usado apropiadamente
- ✅ **Status codes** correctos en todas las situaciones
- ✅ **Mensajes de error** informativos y consistentes
- ✅ **Error handling** proactivo
- ✅ **Logging** básico implementado

#### **Bueno (15-17 puntos)**

- ✅ **Status codes** correctos en mayoría de casos
- ✅ **HTTPException** usado generalmente bien
- ✅ **Mensajes de error** informativos
- ⚠️ **Algunos casos** sin manejo específico
- ⚠️ **Consistencia** puede mejorar

#### **Satisfactorio (12-14 puntos)**

- ✅ **Manejo básico** de errores implementado
- ⚠️ **Status codes** apropiados pero limitados
- ⚠️ **Mensajes de error** genéricos
- ⚠️ **Algunos errores** no manejados

#### **Necesita Mejora (0-11 puntos)**

- ❌ **Sin manejo** de errores apropiado
- ❌ **Status codes** incorrectos o ausentes
- ❌ **Errores causan crashes** o responses incorrectos
- ❌ **Mensajes** confusos o ausentes

---

### **4. Estructura y Organización (15 puntos - 15%)**

#### **Excelente (14-15 puntos)**

- ✅ **Código bien organizado** en módulos
- ✅ **Separación clara** de responsabilidades
- ✅ **Naming conventions** consistentes
- ✅ **Imports** organizados y limpios
- ✅ **Estructura profesional** del proyecto

#### **Bueno (12-13 puntos)**

- ✅ **Organización clara** del código
- ✅ **Funciones bien estructuradas**
- ✅ **Naming** generalmente consistente
- ⚠️ **Algunas mejoras** en organización posibles
- ⚠️ **Imports** mayormente ordenados

#### **Satisfactorio (9-11 puntos)**

- ✅ **Estructura básica** presente
- ⚠️ **Organización** puede mejorar
- ⚠️ **Naming** inconsistente en algunos casos
- ⚠️ **Código funcional** pero no optimizado

#### **Necesita Mejora (0-8 puntos)**

- ❌ **Código desorganizado** o confuso
- ❌ **Sin estructura** clara
- ❌ **Naming** inconsistente o confuso
- ❌ **Difícil de leer** o mantener

---

### **5. Documentación (10 puntos - 10%)**

#### **Excelente (9-10 puntos)**

- ✅ **README completo** con instalación y uso
- ✅ **Documentación automática** FastAPI funcional
- ✅ **Comentarios útiles** en código complejo
- ✅ **Ejemplos de uso** incluidos
- ✅ **Docstrings** en funciones principales

#### **Bueno (7-8 puntos)**

- ✅ **README presente** con información básica
- ✅ **Documentación automática** funcional
- ✅ **Algunos comentarios** útiles
- ⚠️ **Ejemplos limitados** o ausentes
- ⚠️ **Docstrings** parciales

#### **Satisfactorio (5-6 puntos)**

- ✅ **README básico** presente
- ⚠️ **Documentación automática** funcional pero básica
- ⚠️ **Comentarios mínimos** o ausentes
- ⚠️ **Sin ejemplos** de uso

#### **Necesita Mejora (0-4 puntos)**

- ❌ **Sin README** o inadecuado
- ❌ **Documentación automática** no funcional
- ❌ **Sin comentarios** explicativos
- ❌ **Código sin documentar**

---

## 📋 Entregables Obligatorios

### **📁 Estructura Mínima Requerida**

```
estudiante-nombre/
├── main.py                 # ✅ API principal
├── models/
│   └── product_models.py   # ✅ Modelos Pydantic
├── requirements.txt        # ✅ Dependencias
└── README.md              # ✅ Documentación
```

### **📁 Estructura Recomendada (Bonus)**

```
estudiante-nombre/
├── main.py
├── models/
│   └── product_models.py
├── routes/
│   └── product_routes.py   # 🌟 Endpoints organizados
├── utils/
│   └── error_handlers.py   # 🌟 Manejo de errores
├── requirements.txt
└── README.md
```

---

## 🎯 Funcionalidades Obligatorias

### **Endpoints Mínimos Requeridos**

| Método | Endpoint         | Descripción         | Status         |
| ------ | ---------------- | ------------------- | -------------- |
| GET    | `/products`      | Listar productos    | ✅ Obligatorio |
| GET    | `/products/{id}` | Obtener producto    | ✅ Obligatorio |
| POST   | `/products`      | Crear producto      | ✅ Obligatorio |
| PUT    | `/products/{id}` | Actualizar producto | ✅ Obligatorio |
| DELETE | `/products/{id}` | Eliminar producto   | ✅ Obligatorio |

### **Campos Mínimos del Modelo**

```python
class Product(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)
    in_stock: bool = Field(True)
    category: str = Field(..., min_length=1, max_length=50)
```

---

## 📊 Escala de Calificación

| Rango  | Calificación | Descripción                                     |
| ------ | ------------ | ----------------------------------------------- |
| 90-100 | A            | Excelente trabajo, supera expectativas          |
| 80-89  | B            | Buen trabajo, cumple expectativas               |
| 70-79  | C            | Trabajo satisfactorio, necesita mejoras menores |
| 60-69  | D            | Trabajo básico, necesita mejoras significativas |
| 0-59   | F            | No cumple con los requisitos mínimos            |

---

## 🔄 Proceso de Evaluación

### **Entrega**

- 📅 **Deadline**: Final de Semana 3
- 📁 **Método**: GitHub repository
- 🏷️ **Tag**: `semana-03-submission`
- 📋 **Include**: README con instrucciones de ejecución

### **Evaluación**

1. **Revisión automática** (funcionalidad básica)
2. **Revisión manual** (calidad código y documentación)
3. **Feedback específico** dentro de 48 horas
4. **Oportunidad de mejora** si es necesario

---

## 💡 Consejos para el Éxito

### **⚡ Gestión del Tiempo**

- 🎯 **Prioriza funcionalidad** sobre perfección
- ⏰ **Dedica 30 min** por bloque de práctica
- 🔄 **Itera incrementalmente**
- 📝 **Documenta mientras desarrollas**

### **🏆 Calidad del Código**

- 📖 **Lee la documentación** FastAPI official
- 🧪 **Prueba cada endpoint** mientras desarrollas
- 🔍 **Usa herramientas** de desarrollo (Postman, curl)
- 💡 **Sigue ejemplos** de las prácticas

### **📋 Antes de Entregar**

- ✅ **Todos los endpoints** funcionan
- ✅ **Documentación automática** accesible
- ✅ **README** con instrucciones claras
- ✅ **Código** comentado apropiadamente

---

_Rúbrica creada: 24 de julio de 2025_  
_Bootcamp FastAPI - EPTI Development_
