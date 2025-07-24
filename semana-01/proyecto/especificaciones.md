# Proyecto de la Semana 1: Sistema de Gestión de Tareas

## 🎯 Descripción del Proyecto

Desarrollar una API completa para gestión de tareas personales, aplicando todos los conceptos aprendidos en la Semana 1.

## 🏗️ Funcionalidades Requeridas

### Core Features

1. **Gestión de Usuarios**

   - Registro de usuarios
   - Perfil de usuario
   - Preferencias personales

2. **Gestión de Tareas**

   - Crear, leer, actualizar, eliminar tareas
   - Categorización de tareas
   - Prioridades y estados
   - Fechas de vencimiento

3. **Organización**
   - Etiquetas (tags)
   - Categorías
   - Filtros y búsqueda
   - Ordenamiento

### Features Adicionales

4. **Estadísticas Básicas**

   - Conteo de tareas por estado
   - Tareas vencidas
   - Productividad semanal

5. **API Features**
   - Documentación automática
   - Validación robusta
   - Manejo de errores
   - Responses consistentes

## 📋 Especificaciones Técnicas

### Modelos de Datos

#### User

```python
{
    "id": int,
    "username": str,
    "email": str,
    "full_name": str,
    "created_at": datetime,
    "preferences": {
        "theme": str,
        "language": str,
        "timezone": str
    }
}
```

#### Task

```python
{
    "id": int,
    "title": str,
    "description": str,
    "priority": "low" | "medium" | "high" | "urgent",
    "status": "pending" | "in_progress" | "completed" | "cancelled",
    "category_id": int,
    "user_id": int,
    "due_date": date,
    "created_at": datetime,
    "updated_at": datetime,
    "tags": [str]
}
```

#### Category

```python
{
    "id": int,
    "name": str,
    "description": str,
    "color": str,
    "user_id": int
}
```

### Endpoints Requeridos

#### Users

- `POST /users` - Registrar usuario
- `GET /users/me` - Obtener perfil actual
- `PUT /users/me` - Actualizar perfil
- `DELETE /users/me` - Eliminar cuenta

#### Tasks

- `POST /tasks` - Crear tarea
- `GET /tasks` - Listar tareas (con filtros)
- `GET /tasks/{task_id}` - Obtener tarea específica
- `PUT /tasks/{task_id}` - Actualizar tarea
- `DELETE /tasks/{task_id}` - Eliminar tarea
- `PATCH /tasks/{task_id}/status` - Cambiar estado

#### Categories

- `POST /categories` - Crear categoría
- `GET /categories` - Listar categorías
- `PUT /categories/{category_id}` - Actualizar categoría
- `DELETE /categories/{category_id}` - Eliminar categoría

#### Statistics

- `GET /stats/summary` - Resumen general
- `GET /stats/productivity` - Estadísticas de productividad

### Parámetros de Filtrado

Para `GET /tasks`:

- `status`: Filtrar por estado
- `priority`: Filtrar por prioridad
- `category_id`: Filtrar por categoría
- `due_date_from` / `due_date_to`: Rango de fechas
- `search`: Búsqueda en título/descripción
- `tags`: Filtrar por etiquetas
- `page` / `page_size`: Paginación
- `sort_by` / `sort_order`: Ordenamiento

## 🎨 Estructura del Proyecto

```
semana-01/
├── proyecto/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   └── category.py
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── tasks.py
│   │   │   ├── categories.py
│   │   │   └── stats.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── task_service.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   └── database/
│   │       ├── __init__.py
│   │       └── fake_db.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_users.py
│   │   ├── test_tasks.py
│   │   └── test_categories.py
│   ├── docs/
│   │   ├── api_examples.md
│   │   └── postman_collection.json
│   ├── requirements.txt
│   ├── README.md
│   └── .env.example
```

## 🚀 Implementación por Fases

### Fase 1: Setup Básico (Día 1-2)

- Configuración del proyecto
- Modelos Pydantic básicos
- Endpoints de usuarios
- Documentación automática

### Fase 2: Core Features (Día 3-4)

- CRUD completo de tareas
- Sistema de categorías
- Validaciones robustas
- Manejo de errores

### Fase 3: Features Avanzadas (Día 5)

- Filtros y búsqueda
- Estadísticas básicas
- Tests básicos
- Documentación de API

### Fase 4: Polish (Día 6-7)

- Refinamiento de código
- Optimizaciones
- Documentación completa
- Preparación para entrega

## 📝 Criterios de Evaluación

### Funcionalidad (40%)

- ✅ Todos los endpoints funcionando
- ✅ Validaciones implementadas
- ✅ Filtros y búsqueda operativos
- ✅ Manejo correcto de errores

### Código (25%)

- ✅ Estructura clara del proyecto
- ✅ Modelos Pydantic bien definidos
- ✅ Separación de responsabilidades
- ✅ Código limpio y legible

### API Design (20%)

- ✅ Endpoints RESTful apropiados
- ✅ Responses consistentes
- ✅ Status codes correctos
- ✅ Documentación automática clara

### Documentación (15%)

- ✅ README completo
- ✅ Ejemplos de uso
- ✅ Instrucciones de instalación
- ✅ Documentación de endpoints

## 🧪 Testing Manual

### Escenarios de Prueba

1. **Flujo básico de usuario**:

   - Registrar usuario
   - Crear categorías
   - Crear tareas
   - Filtrar y buscar
   - Actualizar estados
   - Ver estadísticas

2. **Validaciones**:

   - Datos inválidos
   - Campos requeridos
   - Formatos incorrectos
   - Rangos de valores

3. **Edge cases**:
   - Listas vacías
   - Recursos no encontrados
   - Duplicados
   - Límites de paginación

## 📦 Entregables

1. **Código fuente completo**
2. **README con instrucciones**
3. **Collection de Postman** (opcional)
4. **Screenshots de la documentación**
5. **Video demo** (3-5 minutos)

## 🎁 Bonus Features

- **Bulk operations** (+5 puntos)
- **Export/Import** de tareas (+5 puntos)
- **Configuración por variables de entorno** (+3 puntos)
- **Middleware de logging** (+3 puntos)
- **Tests automatizados** (+10 puntos)
- **Docker setup** (+5 puntos)

## 📅 Cronograma Sugerido

| Día | Actividades           | Entregables        |
| --- | --------------------- | ------------------ |
| 1   | Setup + Modelos       | Estructura básica  |
| 2   | Usuarios + Categorías | CRUD básico        |
| 3   | Tareas principales    | Core functionality |
| 4   | Filtros + Búsqueda    | Features avanzadas |
| 5   | Estadísticas + Polish | API completa       |
| 6   | Testing + Docs        | Documentación      |
| 7   | Entrega final         | Proyecto completo  |

## 🤝 Colaboración

- **Revisión por pares**: Intercambio de feedback
- **Daily standups**: 15min de check-in diario
- **Code reviews**: Comentarios constructivos
- **Discord channels**: #proyecto-semana1

## 📚 Recursos de Apoyo

- Todos los tutoriales de práctica
- Documentación oficial de FastAPI
- Ejemplos en el repositorio
- Office hours con instructores

¡Mucho éxito en tu proyecto! 🚀✨
