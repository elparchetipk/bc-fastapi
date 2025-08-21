# Mi Primera API con FastAPI - Ejemplo Base

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Crear la aplicación FastAPI
app = FastAPI(
    title="Mi API de Tareas",
    description="Una API simple para gestión de tareas - Semana 1",
    version="1.0.0"
)

# Modelo de datos usando Pydantic
class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = ""
    completed: bool = False
    created_at: Optional[str] = None

# Base de datos en memoria (lista simple)
tasks_db: List[Task] = []
next_id = 1

@app.get("/")
def read_root():
    """Endpoint de bienvenida"""
    return {
        "message": "¡Bienvenido a mi primera API con FastAPI!",
        "version": "1.0.0",
        "endpoints": {
            "crear_tarea": "POST /tasks",
            "listar_tareas": "GET /tasks", 
            "obtener_tarea": "GET /tasks/{task_id}",
            "completar_tarea": "PUT /tasks/{task_id}/complete"
        }
    }

@app.post("/tasks", response_model=Task)
def create_task(task: Task):
    """Crear una nueva tarea"""
    global next_id
    
    # Asignar ID y timestamp
    task.id = next_id
    task.created_at = datetime.now().isoformat()
    next_id += 1
    
    # Agregar a la "base de datos"
    tasks_db.append(task)
    
    return task

@app.get("/tasks", response_model=List[Task])
def get_tasks(completed: Optional[bool] = None):
    """Listar todas las tareas, opcionalmente filtrar por estado"""
    if completed is None:
        return tasks_db
    
    # Filtrar por estado completado
    return [task for task in tasks_db if task.completed == completed]

@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Obtener una tarea específica por ID"""
    for task in tasks_db:
        if task.id == task_id:
            return task
    
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

@app.put("/tasks/{task_id}/complete", response_model=Task)
def complete_task(task_id: int):
    """Marcar una tarea como completada"""
    for task in tasks_db:
        if task.id == task_id:
            task.completed = True
            return task
    
    raise HTTPException(status_code=404, detail="Tarea no encontrada")

# Para ejecutar: uvicorn main:app --reload
