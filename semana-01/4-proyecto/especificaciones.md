# Proyecto de la Semana 1: Mi Primera API con FastAPI

## 🎯 Descripción del Proyecto

Crear una API básica de gestión de tareas personales que demuestre los conceptos fundamentales de FastAPI aprendidos en las 5.5 horas efectivas de clase.

**⏰ TIEMPO ESTIMADO: 2-3 horas máximo (incluido en las 6 horas de clase)**

## 🚨 **ALCANCE REALISTA PARA 5.5 HORAS**

Este proyecto está diseñado para ser **completamente realizable** en el tiempo de clase disponible. NO es un proyecto complejo, sino una demostración de conceptos básicos.

## 🏗️ Funcionalidades Requeridas (MÍNIMAS)

### ✅ **Core Features (OBLIGATORIAS)**

1. **API Básica Funcionando**
   - Servidor FastAPI ejecutándose
   - Documentación automática accesible
   - Al menos 4 endpoints funcionando

2. **Gestión Simple de Tareas**
   - Crear una tarea
   - Listar todas las tareas
   - Obtener una tarea por ID
   - Marcar tarea como completada

### 🎁 **Features Opcionales (BONUS)**

3. **Validación Básica**
   - Modelos Pydantic simples
   - Validación de entrada de datos

4. **Organización**
   - Filtro simple por estado (completada/pendiente)

## 📋 Especificaciones Técnicas SIMPLIFICADAS

### Modelo de Datos (UNO SOLO)

#### Task (Modelo Único)

```python
{
    "id": int,
    "title": str,
    "description": str (opcional),
    "completed": bool (default: False),
    "created_at": str (ISO format)
}
```

### Endpoints Requeridos (SOLO 4)

#### Tasks Básicos

- `GET /` - Hello World + información de la API
- `POST /tasks` - Crear tarea nueva
- `GET /tasks` - Listar todas las tareas
- `GET /tasks/{task_id}` - Obtener tarea específica
- `PUT /tasks/{task_id}/complete` - Marcar como completada

### Almacenamiento

**Lista en memoria (NO base de datos)**
```python
# Variable global simple
tasks_db = []
```
```python
# Variable global simple
tasks_db = []
```

## 🎨 Estructura del Proyecto SIMPLE

```text
proyecto/
├── main.py              # TODO en un solo archivo
├── requirements.txt     # Solo FastAPI y uvicorn
├── README.md           # Instrucciones básicas
└── .gitignore          # Opcional
```

**NO necesitas carpetas complejas ni múltiples archivos para esta semana.**

## 🚀 Implementación REALISTA (5.5 horas)

### ⏱️ Tiempo en Clase (Durante las 6 horas)

- **Setup (30 min)**: Entorno + FastAPI instalado
- **Hello World (45 min)**: Primer endpoint funcionando
- **Modelo Básico (30 min)**: Clase Task con Pydantic
- **CRUD Básico (90 min)**: 4 endpoints principales
- **Testing Manual (30 min)**: Probar endpoints
- **Documentación (15 min)**: README básico

### ⏱️ Tiempo Fuera de Clase (Opcional)

- **Mejoras**: Validaciones adicionales
- **Cleanup**: Código más limpio
- **Bonus**: Filtros simples

## 📝 Criterios de Evaluación SIMPLIFICADOS

### ✅ Funcionalidad Básica (50%)

- API se ejecuta sin errores
- 4 endpoints funcionan correctamente
- Documentación automática accesible
- Respuestas JSON válidas

### ✅ Código (30%)

- Archivo main.py limpio y legible
- Modelo Pydantic básico implementado
- Comentarios mínimos explicativos

### ✅ Documentación (20%)

- README con instrucciones de ejecución
- Capturas de pantalla de /docs
- Ejemplos de uso básicos

## 🧪 Testing Manual SIMPLE

### Pruebas Básicas

1. **Verificar servidor**: `uvicorn main:app --reload`
2. **Acceder a docs**: `http://localhost:8000/docs`
3. **Crear tarea**: POST con título
4. **Listar tareas**: GET para ver la lista
5. **Obtener tarea**: GET por ID específico
6. **Completar tarea**: PUT para marcar como completada

## 📦 Entregables MÍNIMOS

1. ✅ **Archivo main.py funcionando**
2. ✅ **requirements.txt con dependencias**
3. ✅ **README.md con instrucciones**
4. ✅ **Screenshot de /docs funcionando**

### 🎁 Entregables Bonus (Opcionales)

- Video demo de 2 minutos máximo
- Ejemplo de uso con curl/Postman
- Filtro por estado completado

## 📅 Cronograma REALISTA

| Tiempo | Actividad                    | Resultado                |
| ------ | ---------------------------- | ------------------------ |
| 30min  | Setup + instalación         | FastAPI funcionando      |
| 45min  | Hello World + estructura     | Primer endpoint          |
| 30min  | Modelo Task básico           | Pydantic funcionando     |
| 90min  | 4 endpoints CRUD             | API básica completa      |
| 30min  | Testing manual               | Endpoints verificados    |
| 15min  | README + documentación       | Proyecto documentado     |

**Total: 4 horas de las 5.5 disponibles + 1.5h buffer para problemas**

## 🎯 Expectativas REALISTAS

### ✅ Lo que SÍ vas a lograr:
- API funcionando localmente
- Comprensión básica de FastAPI
- Documentación automática
- CRUD básico en memoria

### ❌ Lo que NO se espera:
- Base de datos real
- Autenticación/autorización
- Validaciones complejas
- Arquitectura avanzada
- Testing automatizado
- Deploy en producción

## 🤝 Apoyo Durante el Desarrollo

- **Discord**: Canal #semana1-help
- **Office Hours**: Horarios específicos para dudas
- **Peer Programming**: Trabajo en parejas permitido
- **Code Review**: Revisión opcional pre-entrega

## 📚 Recursos de Apoyo ESPECÍFICOS

- [FastAPI Tutorial Básico](https://fastapi.tiangolo.com/tutorial/)
- [Documentación Pydantic](https://docs.pydantic.dev/)
- Ejemplos de código en `semana-01/2-practica/`
- Template básico en repositorio

## 🎉 Criterio de Éxito

**Si tu API arranca, muestra documentación y permite crear/listar tareas, ¡HAS TENIDO ÉXITO!**

Este es tu primer contacto con FastAPI. El objetivo es sentirte cómodo y motivado para continuar, no crear una aplicación de producción.

¡Enfócate en los fundamentos y disfruta el proceso! 🚀✨
