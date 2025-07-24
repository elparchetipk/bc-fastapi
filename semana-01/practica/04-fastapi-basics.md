# 04 - Fundamentos de FastAPI

## 🎯 Objetivos de Aprendizaje

Al finalizar este módulo, podrás:

- Crear tu primera aplicación FastAPI funcional
- Entender la estructura básica de endpoints
- Implementar diferentes métodos HTTP (GET, POST, PUT, DELETE)
- Usar parámetros de ruta, query y cuerpo de request
- Generar documentación automática con Swagger/OpenAPI

## 📋 Prerrequisitos

- Haber completado [03-python-fundamentals.md](./03-python-fundamentals.md)
- Python 3.8+ con entorno virtual configurado
- FastAPI y Uvicorn instalados

## 🚀 Instalación de Dependencias

Primero, instala las dependencias necesarias:

```bash
pip install fastapi uvicorn[standard] python-multipart
```

## 🏗️ Estructura del Proyecto

```
semana-01/
├── practica/
│   └── 04-fastapi-basics/
│       ├── app/
│       │   ├── __init__.py
│       │   ├── main.py
│       │   ├── models.py
│       │   ├── routes.py
│       │   └── examples/
│       │       ├── basic_endpoints.py
│       │       ├── path_parameters.py
│       │       ├── query_parameters.py
│       │       └── request_body.py
│       ├── requirements.txt
│       └── README.md
```

## 📝 Contenido

### 1. Primera Aplicación FastAPI

Empezamos con lo más básico: una aplicación FastAPI simple.

#### Archivo main.py

Crea el archivo `app/main.py`:

```python
from fastapi import FastAPI
from datetime import datetime

# Crear la instancia de FastAPI
app = FastAPI(
    title="Mi Primera API",
    description="Una API de ejemplo para aprender FastAPI",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # ReDoc
)

# Endpoint básico
@app.get("/")
async def root():
    """Endpoint raíz que devuelve un saludo básico."""
    return {
        "message": "¡Hola, FastAPI!",
        "timestamp": datetime.now().isoformat(),
        "status": "ok"
    }

# Endpoint de salud
@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la API."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Endpoint de información
@app.get("/info")
async def get_info():
    """Endpoint que devuelve información sobre la API."""
    return {
        "name": "Mi Primera API",
        "version": "1.0.0",
        "description": "API de ejemplo para aprender FastAPI",
        "endpoints": [
            "/",
            "/health",
            "/info",
            "/docs",
            "/redoc"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

### 2. Modelos de Datos con Pydantic

Crea el archivo `app/models.py`:

```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enum para categorías
class Category(str, Enum):
    TECHNOLOGY = "technology"
    SCIENCE = "science"
    SPORTS = "sports"
    ENTERTAINMENT = "entertainment"

# Modelo base para timestamps
class TimestampMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

# Modelo para usuario
class UserCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="Juan Pérez")
    email: EmailStr = Field(..., example="juan@email.com")
    age: int = Field(..., ge=18, le=120, example=25)
    interests: Optional[List[Category]] = Field(None, example=["technology", "science"])

class User(UserCreate, TimestampMixin):
    id: int = Field(..., example=1)
    is_active: bool = Field(True, example=True)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    interests: Optional[List[Category]]
    is_active: bool
    created_at: datetime

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=18, le=120)
    interests: Optional[List[Category]] = None
    is_active: Optional[bool] = None

# Modelo para artículos
class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=200, example="Introducción a FastAPI")
    content: str = Field(..., min_length=10, example="FastAPI es un framework moderno...")
    category: Category = Field(..., example="technology")
    tags: Optional[List[str]] = Field(None, example=["python", "api", "web"])

class Article(ArticleCreate, TimestampMixin):
    id: int = Field(..., example=1)
    author_id: int = Field(..., example=1)
    views: int = Field(0, example=0)

class ArticleResponse(BaseModel):
    id: int
    title: str
    content: str
    category: Category
    tags: Optional[List[str]]
    author_id: int
    views: int
    created_at: datetime

# Modelos de respuesta estándar
class StandardResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    error_code: Optional[str] = None
    details: Optional[dict] = None
```

### 3. Endpoints Básicos

Crea el archivo `app/examples/basic_endpoints.py`:

```python
from fastapi import FastAPI, HTTPException
from datetime import datetime
import random

app = FastAPI(title="Endpoints Básicos")

# Base de datos simulada
fake_users_db = [
    {"id": 1, "name": "Juan Pérez", "email": "juan@email.com"},
    {"id": 2, "name": "María García", "email": "maria@email.com"},
    {"id": 3, "name": "Pedro López", "email": "pedro@email.com"}
]

# GET - Obtener todos los usuarios
@app.get("/users")
async def get_users():
    """Obtiene todos los usuarios."""
    return {
        "users": fake_users_db,
        "total": len(fake_users_db),
        "timestamp": datetime.now().isoformat()
    }

# GET - Obtener un usuario específico
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    """Obtiene un usuario por su ID."""
    user = next((u for u in fake_users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

# POST - Crear un nuevo usuario
@app.post("/users")
async def create_user(user_data: dict):
    """Crea un nuevo usuario."""
    new_id = max([u["id"] for u in fake_users_db]) + 1 if fake_users_db else 1
    new_user = {
        "id": new_id,
        "name": user_data.get("name"),
        "email": user_data.get("email"),
        "created_at": datetime.now().isoformat()
    }
    fake_users_db.append(new_user)
    return {
        "message": "Usuario creado exitosamente",
        "user": new_user
    }

# PUT - Actualizar un usuario
@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: dict):
    """Actualiza un usuario existente."""
    user_index = next((i for i, u in enumerate(fake_users_db) if u["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar campos
    if "name" in user_data:
        fake_users_db[user_index]["name"] = user_data["name"]
    if "email" in user_data:
        fake_users_db[user_index]["email"] = user_data["email"]

    fake_users_db[user_index]["updated_at"] = datetime.now().isoformat()

    return {
        "message": "Usuario actualizado exitosamente",
        "user": fake_users_db[user_index]
    }

# DELETE - Eliminar un usuario
@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Elimina un usuario."""
    user_index = next((i for i, u in enumerate(fake_users_db) if u["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    deleted_user = fake_users_db.pop(user_index)
    return {
        "message": "Usuario eliminado exitosamente",
        "deleted_user": deleted_user
    }

# Endpoint que simula error
@app.get("/random-error")
async def random_error():
    """Endpoint que genera errores aleatorios para pruebas."""
    if random.random() < 0.5:
        raise HTTPException(status_code=500, detail="Error interno del servidor simulado")
    return {"message": "¡Todo salió bien esta vez!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("basic_endpoints:app", host="0.0.0.0", port=8001, reload=True)
```

### 4. Parámetros de Ruta

Crea el archivo `app/examples/path_parameters.py`:

```python
from fastapi import FastAPI, HTTPException, Path
from typing import Union
from enum import Enum

app = FastAPI(title="Parámetros de Ruta")

# Enum para tipos de contenido
class ContentType(str, Enum):
    ARTICLE = "article"
    VIDEO = "video"
    PODCAST = "podcast"

# Base de datos simulada
content_db = {
    "articles": [
        {"id": 1, "title": "FastAPI Basics", "author": "Juan"},
        {"id": 2, "title": "Python Advanced", "author": "María"}
    ],
    "videos": [
        {"id": 1, "title": "FastAPI Tutorial", "duration": "30min"},
        {"id": 2, "title": "Python Tips", "duration": "15min"}
    ],
    "podcasts": [
        {"id": 1, "title": "Tech Talk", "host": "Pedro"},
        {"id": 2, "title": "Python Weekly", "host": "Ana"}
    ]
}

# Parámetro de ruta simple
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    """Obtiene un elemento por ID."""
    return {"item_id": item_id, "message": f"Obteniendo elemento {item_id}"}

# Parámetro de ruta con validación
@app.get("/items/{item_id}/details")
async def get_item_details(
    item_id: int = Path(..., title="ID del elemento", ge=1, le=1000)
):
    """Obtiene detalles de un elemento con validación de ID."""
    return {
        "item_id": item_id,
        "details": f"Detalles del elemento {item_id}",
        "valid_range": "1-1000"
    }

# Parámetro de ruta con enum
@app.get("/content/{content_type}")
async def get_content_by_type(content_type: ContentType):
    """Obtiene contenido por tipo usando enum."""
    content_map = {
        ContentType.ARTICLE: content_db["articles"],
        ContentType.VIDEO: content_db["videos"],
        ContentType.PODCAST: content_db["podcasts"]
    }
    return {
        "content_type": content_type,
        "items": content_map[content_type],
        "count": len(content_map[content_type])
    }

# Múltiples parámetros de ruta
@app.get("/content/{content_type}/{content_id}")
async def get_specific_content(
    content_type: ContentType,
    content_id: int = Path(..., title="ID del contenido", ge=1)
):
    """Obtiene contenido específico por tipo e ID."""
    content_map = {
        ContentType.ARTICLE: content_db["articles"],
        ContentType.VIDEO: content_db["videos"],
        ContentType.PODCAST: content_db["podcasts"]
    }

    items = content_map[content_type]
    item = next((item for item in items if item["id"] == content_id), None)

    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"{content_type.value} con ID {content_id} no encontrado"
        )

    return {
        "content_type": content_type,
        "content_id": content_id,
        "item": item
    }

# Parámetro de ruta con string
@app.get("/users/{username}")
async def get_user_profile(
    username: str = Path(..., title="Nombre de usuario", min_length=3, max_length=20)
):
    """Obtiene perfil de usuario por nombre de usuario."""
    return {
        "username": username,
        "profile_url": f"/profiles/{username}",
        "message": f"Perfil de {username}"
    }

# Parámetro opcional vs requerido
@app.get("/files/{file_path:path}")
async def get_file(file_path: str):
    """Obtiene archivo por ruta completa (permite / en el parámetro)."""
    return {
        "file_path": file_path,
        "message": f"Accediendo al archivo: {file_path}"
    }

# Union de tipos en parámetros
@app.get("/search/{query}")
async def search_content(query: Union[str, int]):
    """Busca contenido por query (string o número)."""
    if isinstance(query, int):
        # Búsqueda por ID
        return {
            "search_type": "id",
            "query": query,
            "message": f"Buscando por ID: {query}"
        }
    else:
        # Búsqueda por texto
        return {
            "search_type": "text",
            "query": query,
            "message": f"Buscando por texto: {query}"
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("path_parameters:app", host="0.0.0.0", port=8002, reload=True)
```

### 5. Parámetros de Query

Crea el archivo `app/examples/query_parameters.py`:

```python
from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List
from enum import Enum

app = FastAPI(title="Parámetros de Query")

# Enum para ordenamiento
class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"

# Base de datos simulada de productos
products_db = [
    {"id": 1, "name": "Laptop", "price": 1200, "category": "electronics", "rating": 4.5},
    {"id": 2, "name": "Mouse", "price": 25, "category": "electronics", "rating": 4.2},
    {"id": 3, "name": "Book", "price": 15, "category": "books", "rating": 4.8},
    {"id": 4, "name": "Shirt", "price": 30, "category": "clothing", "rating": 4.0},
    {"id": 5, "name": "Phone", "price": 800, "category": "electronics", "rating": 4.7},
    {"id": 6, "name": "Jeans", "price": 60, "category": "clothing", "rating": 4.3}
]

# Query parameters básicos
@app.get("/products")
async def get_products(
    page: int = Query(1, title="Número de página", ge=1),
    page_size: int = Query(10, title="Elementos por página", ge=1, le=100),
    search: Optional[str] = Query(None, title="Término de búsqueda", min_length=1)
):
    """Obtiene productos con paginación y búsqueda opcional."""
    filtered_products = products_db

    # Aplicar búsqueda si se proporciona
    if search:
        filtered_products = [
            p for p in filtered_products
            if search.lower() in p["name"].lower()
        ]

    # Aplicar paginación
    start = (page - 1) * page_size
    end = start + page_size
    paginated_products = filtered_products[start:end]

    return {
        "products": paginated_products,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total_items": len(filtered_products),
            "total_pages": (len(filtered_products) + page_size - 1) // page_size
        },
        "search_term": search
    }

# Query parameters con filtros múltiples
@app.get("/products/filter")
async def filter_products(
    category: Optional[str] = Query(None, title="Categoría"),
    min_price: Optional[float] = Query(None, title="Precio mínimo", ge=0),
    max_price: Optional[float] = Query(None, title="Precio máximo", ge=0),
    min_rating: Optional[float] = Query(None, title="Rating mínimo", ge=0, le=5),
    sort_by: Optional[str] = Query("name", title="Campo de ordenamiento"),
    sort_order: SortOrder = Query(SortOrder.ASC, title="Orden de clasificación")
):
    """Filtra productos con múltiples criterios."""
    filtered_products = products_db.copy()

    # Aplicar filtros
    if category:
        filtered_products = [p for p in filtered_products if p["category"] == category]

    if min_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] >= min_price]

    if max_price is not None:
        filtered_products = [p for p in filtered_products if p["price"] <= max_price]

    if min_rating is not None:
        filtered_products = [p for p in filtered_products if p["rating"] >= min_rating]

    # Aplicar ordenamiento
    if sort_by in ["name", "price", "rating"]:
        reverse = sort_order == SortOrder.DESC
        filtered_products.sort(key=lambda x: x[sort_by], reverse=reverse)

    return {
        "products": filtered_products,
        "filters_applied": {
            "category": category,
            "min_price": min_price,
            "max_price": max_price,
            "min_rating": min_rating,
            "sort_by": sort_by,
            "sort_order": sort_order
        },
        "total_results": len(filtered_products)
    }

# Query parameters con listas
@app.get("/products/bulk")
async def get_products_by_ids(
    ids: List[int] = Query(..., title="Lista de IDs de productos"),
    include_details: bool = Query(False, title="Incluir detalles adicionales")
):
    """Obtiene múltiples productos por sus IDs."""
    found_products = [p for p in products_db if p["id"] in ids]
    not_found_ids = [id for id in ids if id not in [p["id"] for p in found_products]]

    result = {
        "products": found_products,
        "found_count": len(found_products),
        "requested_count": len(ids)
    }

    if include_details:
        result["details"] = {
            "not_found_ids": not_found_ids,
            "success_rate": len(found_products) / len(ids) if ids else 0
        }

    return result

# Query parameters con validación avanzada
@app.get("/analytics")
async def get_analytics(
    start_date: Optional[str] = Query(
        None,
        title="Fecha de inicio",
        description="Formato: YYYY-MM-DD",
        regex=r"^\d{4}-\d{2}-\d{2}$"
    ),
    end_date: Optional[str] = Query(
        None,
        title="Fecha de fin",
        description="Formato: YYYY-MM-DD",
        regex=r"^\d{4}-\d{2}-\d{2}$"
    ),
    metrics: List[str] = Query(
        ["sales", "views"],
        title="Métricas a incluir",
        description="Lista de métricas disponibles: sales, views, clicks, conversions"
    )
):
    """Obtiene datos de analítica con validación de fechas."""
    available_metrics = ["sales", "views", "clicks", "conversions"]
    valid_metrics = [m for m in metrics if m in available_metrics]
    invalid_metrics = [m for m in metrics if m not in available_metrics]

    if invalid_metrics:
        raise HTTPException(
            status_code=400,
            detail=f"Métricas inválidas: {invalid_metrics}. Disponibles: {available_metrics}"
        )

    # Simular datos de analítica
    analytics_data = {
        "period": {
            "start_date": start_date,
            "end_date": end_date
        },
        "metrics": {
            metric: {"value": 1000 + hash(metric) % 5000, "unit": "count"}
            for metric in valid_metrics
        }
    }

    return analytics_data

# Query parameters opcionales con valores por defecto
@app.get("/recommendations")
async def get_recommendations(
    user_id: Optional[int] = Query(None, title="ID del usuario"),
    limit: int = Query(5, title="Número de recomendaciones", ge=1, le=20),
    category_filter: Optional[List[str]] = Query(None, title="Filtrar por categorías"),
    exclude_purchased: bool = Query(True, title="Excluir productos ya comprados")
):
    """Obtiene recomendaciones de productos personalizadas."""
    recommendations = products_db.copy()

    # Aplicar filtros si se proporcionan
    if category_filter:
        recommendations = [p for p in recommendations if p["category"] in category_filter]

    # Simular exclusión de productos comprados
    if exclude_purchased and user_id:
        # En un caso real, consultarías las compras del usuario
        purchased_ids = [1, 3]  # IDs simulados de productos comprados
        recommendations = [p for p in recommendations if p["id"] not in purchased_ids]

    # Limitar resultados
    recommendations = recommendations[:limit]

    return {
        "user_id": user_id,
        "recommendations": recommendations,
        "total_recommendations": len(recommendations),
        "filters": {
            "category_filter": category_filter,
            "exclude_purchased": exclude_purchased,
            "limit": limit
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("query_parameters:app", host="0.0.0.0", port=8003, reload=True)
```

### 6. Cuerpo de Request

Crea el archivo `app/examples/request_body.py`:

```python
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

app = FastAPI(title="Cuerpo de Request")

# Modelos para el cuerpo de las requests
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, example="Completar proyecto")
    description: Optional[str] = Field(None, max_length=1000, example="Descripción detallada de la tarea")
    priority: Priority = Field(Priority.MEDIUM, example="high")
    due_date: Optional[str] = Field(None, example="2024-12-31")
    tags: Optional[List[str]] = Field(None, example=["trabajo", "urgente"])

    @validator('due_date')
    def validate_due_date(cls, v):
        if v:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('due_date debe tener formato YYYY-MM-DD')
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    priority: Optional[Priority] = None
    due_date: Optional[str] = None
    completed: Optional[bool] = None
    tags: Optional[List[str]] = None

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, example="usuario123")
    email: EmailStr = Field(..., example="usuario@email.com")
    password: str = Field(..., min_length=8, example="password123")
    full_name: str = Field(..., min_length=2, max_length=100, example="Juan Pérez")
    age: int = Field(..., ge=18, le=120, example=25)
    interests: Optional[List[str]] = Field(None, example=["tecnología", "deportes"])

    @validator('password')
    def validate_password(cls, v):
        if not any(c.isdigit() for c in v):
            raise ValueError('La contraseña debe contener al menos un número')
        if not any(c.isalpha() for c in v):
            raise ValueError('La contraseña debe contener al menos una letra')
        return v

# Base de datos simulada
tasks_db = []
users_db = []

# POST con modelo Pydantic
@app.post("/tasks")
async def create_task(task: TaskCreate):
    """Crea una nueva tarea."""
    new_task = {
        "id": len(tasks_db) + 1,
        "created_at": datetime.now().isoformat(),
        "completed": False,
        **task.dict()
    }
    tasks_db.append(new_task)

    return {
        "message": "Tarea creada exitosamente",
        "task": new_task
    }

# PUT con modelo Pydantic
@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_update: TaskUpdate):
    """Actualiza una tarea existente."""
    task_index = next((i for i, t in enumerate(tasks_db) if t["id"] == task_id), None)
    if task_index is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    # Actualizar solo los campos proporcionados
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        tasks_db[task_index][field] = value

    tasks_db[task_index]["updated_at"] = datetime.now().isoformat()

    return {
        "message": "Tarea actualizada exitosamente",
        "task": tasks_db[task_index]
    }

# POST con múltiples modelos
@app.post("/users/register")
async def register_user(user: UserRegistration):
    """Registra un nuevo usuario."""
    # Verificar si el usuario ya existe
    if any(u["username"] == user.username for u in users_db):
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    new_user = {
        "id": len(users_db) + 1,
        "created_at": datetime.now().isoformat(),
        "is_active": True,
        **user.dict(exclude={"password"})  # No incluir la contraseña en la respuesta
    }
    users_db.append(new_user)

    return {
        "message": "Usuario registrado exitosamente",
        "user": new_user
    }

# POST con cuerpo anidado
@app.post("/projects")
async def create_project(
    project_data: Dict[str, Any] = Body(
        ...,
        example={
            "name": "Mi Proyecto",
            "description": "Descripción del proyecto",
            "team": {
                "leader": "Juan Pérez",
                "members": ["María", "Pedro", "Ana"],
                "roles": {
                    "frontend": ["María"],
                    "backend": ["Pedro", "Ana"],
                    "design": ["Juan Pérez"]
                }
            },
            "timeline": {
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
                "milestones": [
                    {"name": "Diseño", "date": "2024-03-01"},
                    {"name": "Desarrollo", "date": "2024-09-01"},
                    {"name": "Testing", "date": "2024-11-01"}
                ]
            },
            "budget": 50000,
            "technologies": ["Python", "FastAPI", "React", "PostgreSQL"]
        }
    )
):
    """Crea un proyecto con estructura compleja."""
    # Validaciones básicas
    required_fields = ["name", "description", "team", "timeline"]
    for field in required_fields:
        if field not in project_data:
            raise HTTPException(status_code=400, detail=f"Campo requerido: {field}")

    new_project = {
        "id": len(tasks_db) + len(users_db) + 1,  # ID simple
        "created_at": datetime.now().isoformat(),
        "status": "planning",
        **project_data
    }

    return {
        "message": "Proyecto creado exitosamente",
        "project": new_project
    }

# POST con múltiples elementos
@app.post("/tasks/bulk")
async def create_multiple_tasks(tasks: List[TaskCreate]):
    """Crea múltiples tareas de una vez."""
    if len(tasks) > 50:
        raise HTTPException(status_code=400, detail="Máximo 50 tareas por request")

    created_tasks = []
    for task in tasks:
        new_task = {
            "id": len(tasks_db) + len(created_tasks) + 1,
            "created_at": datetime.now().isoformat(),
            "completed": False,
            **task.dict()
        }
        created_tasks.append(new_task)

    tasks_db.extend(created_tasks)

    return {
        "message": f"{len(created_tasks)} tareas creadas exitosamente",
        "tasks": created_tasks,
        "total_tasks": len(tasks_db)
    }

# POST con Body personalizado
@app.post("/feedback")
async def submit_feedback(
    rating: int = Body(..., ge=1, le=5, embed=True),
    comment: str = Body(..., min_length=10, max_length=1000, embed=True),
    category: str = Body(..., embed=True),
    anonymous: bool = Body(False, embed=True),
    user_id: Optional[int] = Body(None, embed=True)
):
    """Envía feedback con parámetros individuales en el cuerpo."""
    if not anonymous and not user_id:
        raise HTTPException(status_code=400, detail="user_id requerido para feedback no anónimo")

    feedback = {
        "id": len(tasks_db) + len(users_db) + 100,  # ID simple
        "rating": rating,
        "comment": comment,
        "category": category,
        "anonymous": anonymous,
        "user_id": user_id,
        "submitted_at": datetime.now().isoformat()
    }

    return {
        "message": "Feedback enviado exitosamente",
        "feedback": feedback
    }

# GET para ver datos creados
@app.get("/tasks")
async def get_tasks():
    """Obtiene todas las tareas creadas."""
    return {"tasks": tasks_db, "total": len(tasks_db)}

@app.get("/users")
async def get_users():
    """Obtiene todos los usuarios registrados."""
    return {"users": users_db, "total": len(users_db)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("request_body:app", host="0.0.0.0", port=8004, reload=True)
```

### 7. Aplicación Principal Integrada

Actualiza el archivo `app/main.py` para incluir todas las funcionalidades:

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from .models import (
    UserCreate, UserResponse, UserUpdate,
    ArticleCreate, ArticleResponse,
    StandardResponse, ErrorResponse
)

# Crear la aplicación principal
app = FastAPI(
    title="FastAPI Bootcamp - Semana 1",
    description="API completa con todos los conceptos básicos de FastAPI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especifica los orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de datos simulada
users_db = []
articles_db = []

# Endpoints de usuario
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    """Crea un nuevo usuario."""
    # Verificar email único
    if any(u["email"] == user.email for u in users_db):
        raise HTTPException(status_code=400, detail="Email ya registrado")

    new_user = {
        "id": len(users_db) + 1,
        "created_at": datetime.now(),
        "is_active": True,
        **user.dict()
    }
    users_db.append(new_user)
    return new_user

@app.get("/users", response_model=List[UserResponse])
async def get_users(skip: int = 0, limit: int = 10):
    """Obtiene lista de usuarios con paginación."""
    return users_db[skip:skip + limit]

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """Obtiene un usuario por ID."""
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_update: UserUpdate):
    """Actualiza un usuario."""
    user_index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        users_db[user_index][field] = value

    users_db[user_index]["updated_at"] = datetime.now()
    return users_db[user_index]

@app.delete("/users/{user_id}", response_model=StandardResponse)
async def delete_user(user_id: int):
    """Elimina un usuario."""
    user_index = next((i for i, u in enumerate(users_db) if u["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    deleted_user = users_db.pop(user_index)
    return StandardResponse(
        message=f"Usuario {deleted_user['name']} eliminado exitosamente"
    )

# Endpoint de información
@app.get("/", response_model=StandardResponse)
async def root():
    """Endpoint raíz con información de la API."""
    return StandardResponse(
        message="¡Bienvenido a FastAPI Bootcamp!",
        data={
            "version": "1.0.0",
            "total_users": len(users_db),
            "total_articles": len(articles_db),
            "endpoints": [
                "/docs",
                "/users",
                "/articles",
                "/health"
            ]
        }
    )

@app.get("/health")
async def health_check():
    """Endpoint de salud."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "uptime": "running"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```

## 🚀 Ejecutar la Aplicación

Para ejecutar los diferentes ejemplos:

```bash
# Aplicación principal
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Ejemplos individuales
uvicorn app.examples.basic_endpoints:app --reload --port 8001
uvicorn app.examples.path_parameters:app --reload --port 8002
uvicorn app.examples.query_parameters:app --reload --port 8003
uvicorn app.examples.request_body:app --reload --port 8004
```

## 📖 Documentación Automática

Una vez ejecutada la aplicación, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🧪 Pruebas con curl

Aquí tienes algunos ejemplos para probar la API:

```bash
# GET básico
curl http://localhost:8000/

# POST crear usuario
curl -X POST "http://localhost:8000/users" \
     -H "Content-Type: application/json" \
     -d '{"name":"Juan Pérez","email":"juan@email.com","age":25}'

# GET usuario
curl http://localhost:8000/users/1

# PUT actualizar usuario
curl -X PUT "http://localhost:8000/users/1" \
     -H "Content-Type: application/json" \
     -d '{"name":"Juan Carlos Pérez"}'

# DELETE usuario
curl -X DELETE http://localhost:8000/users/1
```

## 🎯 Próximos Pasos

Una vez completado este módulo:

1. Practica creando tus propios endpoints
2. Experimenta con diferentes tipos de parámetros
3. Revisa la documentación automática generada
4. Continúa con los ejercicios de la semana
5. Prepárate para conceptos más avanzados en la Semana 2

¡Felicidades! Ya dominas los fundamentos básicos de FastAPI 🎉
