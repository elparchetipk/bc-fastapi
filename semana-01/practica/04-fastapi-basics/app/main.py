from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List
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
