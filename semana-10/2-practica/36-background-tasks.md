# Práctica 36: Background Tasks y Procesamiento Asíncrono

⏰ **Tiempo estimado**: 75 minutos _(optimizado)_  
🎯 **Objetivo**: Implementar Background Tasks esenciales para procesamiento asíncrono

## Objetivos

- Implementar tareas en segundo plano básicas con FastAPI
- Configurar Redis básico para colas de tareas
- Crear sistema de notificaciones esencial
- Implementar logging básico de tareas

## Duración: 75 minutos

**OPTIMIZADO PARA 75MIN:**

- ✅ FastAPI Background Tasks fundamentals
- ✅ Redis integration esencial
- ✅ Email notifications básico pero funcional
- ⬇️ Simplificado: Celery setup, monitoring avanzado

## Prerrequisitos

- ✅ FastAPI instalado y configurado
- ✅ Redis instalado y corriendo
- ✅ Conocimiento de async/await
- ✅ Práctica 35 (WebSockets) completada

## 1. Introducción a Background Tasks (15 min)

### Conceptos Clave

Las Background Tasks en FastAPI permiten ejecutar operaciones que no requieren que el cliente espere la respuesta, mejorando la experiencia del usuario y el rendimiento de la API.

**Casos de uso comunes:**

- Envío de emails
- Procesamiento de imágenes
- Generación de reportes
- Limpieza de datos
- Notificaciones push

### Configuración Inicial

```python
# requirements.txt adicionales
redis==5.0.1
celery==5.3.4
flower==2.0.1
aioredis==2.0.1
httpx==0.26.0
```

## 2. Background Tasks Básicas de FastAPI (20 min)

### Estructura del Proyecto

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── background/
│   │   ├── __init__.py
│   │   ├── tasks.py
│   │   └── email_service.py
│   ├── models/
│   │   └── task_models.py
│   └── api/
│       └── task_routes.py
├── static/
│   └── dashboard.html
└── requirements.txt
```

### Implementación Básica

```python
# app/background/tasks.py
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any
import httpx

logger = logging.getLogger(__name__)

async def send_email_task(email: str, subject: str, body: str):
    """Simula envío de email en background"""
    logger.info(f"Enviando email a {email}")

    # Simular procesamiento
    await asyncio.sleep(2)

    # Aquí iría la lógica real de envío
    logger.info(f"Email enviado exitosamente a {email}")
    return {"status": "sent", "email": email, "timestamp": datetime.now()}

async def process_file_task(file_path: str, user_id: int):
    """Procesa archivo en background"""
    logger.info(f"Procesando archivo {file_path} para usuario {user_id}")

    try:
        # Simular procesamiento pesado
        await asyncio.sleep(5)

        # Simular éxito/fallo
        import random
        if random.random() > 0.2:  # 80% éxito
            result = {
                "status": "completed",
                "file_path": file_path,
                "user_id": user_id,
                "processed_at": datetime.now(),
                "records_processed": random.randint(100, 1000)
            }
        else:
            raise Exception("Error simulado en procesamiento")

        logger.info(f"Archivo procesado exitosamente: {file_path}")
        return result

    except Exception as e:
        logger.error(f"Error procesando archivo {file_path}: {str(e)}")
        return {
            "status": "failed",
            "file_path": file_path,
            "user_id": user_id,
            "error": str(e),
            "failed_at": datetime.now()
        }

async def cleanup_old_data_task():
    """Limpieza periódica de datos antiguos"""
    logger.info("Iniciando limpieza de datos antiguos")

    # Simular limpieza
    await asyncio.sleep(3)

    deleted_count = 42  # Simular conteo
    logger.info(f"Limpieza completada: {deleted_count} registros eliminados")

    return {"deleted_count": deleted_count, "timestamp": datetime.now()}
```

### Modelos de Datos

```python
# app/models/task_models.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class EmailRequest(BaseModel):
    email: str
    subject: str
    body: str

class FileProcessRequest(BaseModel):
    file_path: str
    user_id: int

class TaskResponse(BaseModel):
    task_id: str
    status: TaskStatus
    created_at: datetime
    message: str

class TaskResult(BaseModel):
    task_id: str
    status: TaskStatus
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
```

## 3. Implementación con Redis y Celery (25 min)

### Configuración de Celery

```python
# app/background/celery_app.py
from celery import Celery
import os

# Configuración de Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Crear instancia de Celery
celery_app = Celery(
    "background_tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.background.celery_tasks"]
)

# Configuración
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutos
    task_soft_time_limit=25 * 60,  # 25 minutos
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
)
```

### Tareas de Celery

```python
# app/background/celery_tasks.py
from .celery_app import celery_app
import asyncio
import logging
from datetime import datetime
import httpx

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def send_notification_email(self, email: str, subject: str, body: str):
    """Tarea Celery para envío de emails"""
    try:
        # Simular envío
        import time
        time.sleep(2)

        result = {
            "task_id": self.request.id,
            "email": email,
            "subject": subject,
            "status": "sent",
            "sent_at": datetime.now().isoformat()
        }

        logger.info(f"Email enviado a {email}")
        return result

    except Exception as exc:
        logger.error(f"Error enviando email: {str(exc)}")
        self.retry(countdown=60, max_retries=3)

@celery_app.task(bind=True)
def process_large_file(self, file_path: str, user_id: int):
    """Procesamiento pesado de archivos"""
    try:
        # Actualizar estado
        self.update_state(
            state="PROCESSING",
            meta={"current": 0, "total": 100, "status": "Iniciando procesamiento..."}
        )

        # Simular procesamiento con progreso
        import time
        for i in range(100):
            time.sleep(0.1)  # Simular trabajo

            # Actualizar progreso
            self.update_state(
                state="PROCESSING",
                meta={
                    "current": i + 1,
                    "total": 100,
                    "status": f"Procesando línea {i + 1}/100"
                }
            )

        result = {
            "task_id": self.request.id,
            "file_path": file_path,
            "user_id": user_id,
            "records_processed": 100,
            "status": "completed",
            "completed_at": datetime.now().isoformat()
        }

        return result

    except Exception as exc:
        logger.error(f"Error procesando archivo: {str(exc)}")
        self.retry(countdown=60, max_retries=3)

@celery_app.task
def generate_report(user_id: int, report_type: str):
    """Generación de reportes"""
    import time
    time.sleep(5)  # Simular generación

    return {
        "user_id": user_id,
        "report_type": report_type,
        "file_url": f"/reports/report_{user_id}_{report_type}.pdf",
        "generated_at": datetime.now().isoformat()
    }
```

## 4. API Endpoints (15 min)

### Rutas de Background Tasks

```python
# app/api/task_routes.py
from fastapi import APIRouter, BackgroundTasks, HTTPException
from ..models.task_models import *
from ..background.tasks import send_email_task, process_file_task
from ..background.celery_tasks import send_notification_email, process_large_file, generate_report
from ..background.celery_app import celery_app
import uuid
from datetime import datetime

router = APIRouter(prefix="/tasks", tags=["background-tasks"])

# Almacén temporal de tareas (en producción usar Redis)
task_storage = {}

@router.post("/email/simple", response_model=TaskResponse)
async def send_email_simple(
    email_request: EmailRequest,
    background_tasks: BackgroundTasks
):
    """Envía email usando BackgroundTasks de FastAPI"""
    task_id = str(uuid.uuid4())

    # Agregar tarea al background
    background_tasks.add_task(
        send_email_task,
        email_request.email,
        email_request.subject,
        email_request.body
    )

    # Guardar info de la tarea
    task_storage[task_id] = {
        "status": TaskStatus.PENDING,
        "created_at": datetime.now(),
        "type": "email"
    }

    return TaskResponse(
        task_id=task_id,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        message="Email programado para envío"
    )

@router.post("/email/celery", response_model=TaskResponse)
async def send_email_celery(email_request: EmailRequest):
    """Envía email usando Celery"""
    task = send_notification_email.delay(
        email_request.email,
        email_request.subject,
        email_request.body
    )

    return TaskResponse(
        task_id=task.id,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        message="Email programado con Celery"
    )

@router.post("/file/process", response_model=TaskResponse)
async def process_file(file_request: FileProcessRequest):
    """Procesa archivo con Celery y seguimiento de progreso"""
    task = process_large_file.delay(
        file_request.file_path,
        file_request.user_id
    )

    return TaskResponse(
        task_id=task.id,
        status=TaskStatus.PENDING,
        created_at=datetime.now(),
        message="Archivo programado para procesamiento"
    )

@router.post("/report/generate")
async def request_report(user_id: int, report_type: str):
    """Genera reporte en background"""
    task = generate_report.delay(user_id, report_type)

    return {
        "task_id": task.id,
        "message": "Reporte programado para generación",
        "status": "pending"
    }

@router.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """Obtiene el estado de una tarea"""
    # Intentar con Celery primero
    try:
        task = celery_app.AsyncResult(task_id)

        if task.state == "PENDING":
            response = {
                "task_id": task_id,
                "state": task.state,
                "status": "Tarea pendiente..."
            }
        elif task.state == "PROCESSING":
            response = {
                "task_id": task_id,
                "state": task.state,
                "current": task.info.get("current", 0),
                "total": task.info.get("total", 1),
                "status": task.info.get("status", "")
            }
        elif task.state == "SUCCESS":
            response = {
                "task_id": task_id,
                "state": task.state,
                "result": task.result
            }
        else:  # FAILURE
            response = {
                "task_id": task_id,
                "state": task.state,
                "error": str(task.info)
            }

        return response

    except Exception:
        # Fallback a almacén local
        if task_id in task_storage:
            return task_storage[task_id]
        else:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")

@router.get("/active")
async def get_active_tasks():
    """Lista todas las tareas activas"""
    active_tasks = celery_app.control.inspect().active()
    return active_tasks

@router.delete("/cancel/{task_id}")
async def cancel_task(task_id: str):
    """Cancela una tarea"""
    celery_app.control.revoke(task_id, terminate=True)
    return {"message": f"Tarea {task_id} cancelada"}
```

## 5. Dashboard de Monitoreo (10 min)

### Cliente HTML para Monitoreo

```html
<!-- static/task_dashboard.html -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0" />
    <title>Dashboard de Tareas en Background</title>
    <style>
      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        margin: 0;
        padding: 20px;
        background-color: #f5f5f5;
      }

      .container {
        max-width: 1200px;
        margin: 0 auto;
        background: white;
        border-radius: 10px;
        padding: 30px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
      }

      .header {
        text-align: center;
        margin-bottom: 30px;
        padding-bottom: 20px;
        border-bottom: 2px solid #e0e0e0;
      }

      .task-form {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 30px;
      }

      .form-row {
        display: flex;
        gap: 10px;
        margin-bottom: 15px;
        align-items: end;
      }

      .form-group {
        flex: 1;
      }

      label {
        display: block;
        margin-bottom: 5px;
        font-weight: bold;
      }

      input,
      textarea,
      select {
        width: 100%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        box-sizing: border-box;
      }

      button {
        background: #007bff;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 4px;
        cursor: pointer;
        transition: background-color 0.3s;
      }

      button:hover {
        background: #0056b3;
      }

      button:disabled {
        background: #6c757d;
        cursor: not-allowed;
      }

      .tasks-list {
        margin-top: 30px;
      }

      .task-item {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
        transition: box-shadow 0.3s;
      }

      .task-item:hover {
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
      }

      .task-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 10px;
      }

      .task-id {
        font-family: monospace;
        background: #f8f9fa;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 0.9em;
      }

      .task-status {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
        text-transform: uppercase;
      }

      .status-pending {
        background: #fff3cd;
        color: #856404;
      }
      .status-processing {
        background: #cce5ff;
        color: #004085;
      }
      .status-success {
        background: #d4edda;
        color: #155724;
      }
      .status-failure {
        background: #f8d7da;
        color: #721c24;
      }

      .progress-bar {
        width: 100%;
        height: 20px;
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 10px;
      }

      .progress-fill {
        height: 100%;
        background: linear-gradient(45deg, #007bff, #0056b3);
        transition: width 0.3s ease;
        border-radius: 10px;
      }

      .task-actions {
        margin-top: 10px;
      }

      .btn-small {
        padding: 5px 10px;
        font-size: 0.8em;
        margin-right: 5px;
      }

      .btn-danger {
        background: #dc3545;
      }

      .btn-danger:hover {
        background: #c82333;
      }

      .stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
      }

      .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 8px;
        text-align: center;
      }

      .stat-number {
        font-size: 2em;
        font-weight: bold;
        margin-bottom: 5px;
      }

      .loading {
        text-align: center;
        padding: 20px;
        color: #666;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="header">
        <h1>🚀 Dashboard de Tareas en Background</h1>
        <p>Monitoreo y gestión de tareas asíncronas</p>
      </div>

      <!-- Estadísticas -->
      <div class="stats">
        <div class="stat-card">
          <div
            class="stat-number"
            id="totalTasks">
            0
          </div>
          <div>Tareas Totales</div>
        </div>
        <div class="stat-card">
          <div
            class="stat-number"
            id="activeTasks">
            0
          </div>
          <div>Tareas Activas</div>
        </div>
        <div class="stat-card">
          <div
            class="stat-number"
            id="completedTasks">
            0
          </div>
          <div>Completadas</div>
        </div>
        <div class="stat-card">
          <div
            class="stat-number"
            id="failedTasks">
            0
          </div>
          <div>Fallidas</div>
        </div>
      </div>

      <!-- Formulario para crear tareas -->
      <div class="task-form">
        <h3>Crear Nueva Tarea</h3>

        <div class="form-row">
          <div class="form-group">
            <label for="taskType">Tipo de Tarea:</label>
            <select id="taskType">
              <option value="email">Enviar Email</option>
              <option value="file">Procesar Archivo</option>
              <option value="report">Generar Reporte</option>
            </select>
          </div>
          <button onclick="createTask()">Crear Tarea</button>
        </div>

        <!-- Campos dinámicos según tipo -->
        <div
          id="emailFields"
          style="display: none;">
          <div class="form-row">
            <div class="form-group">
              <label for="email">Email:</label>
              <input
                type="email"
                id="email"
                placeholder="usuario@ejemplo.com" />
            </div>
            <div class="form-group">
              <label for="subject">Asunto:</label>
              <input
                type="text"
                id="subject"
                placeholder="Asunto del email" />
            </div>
          </div>
          <div class="form-group">
            <label for="body">Mensaje:</label>
            <textarea
              id="body"
              rows="3"
              placeholder="Contenido del email..."></textarea>
          </div>
        </div>

        <div
          id="fileFields"
          style="display: none;">
          <div class="form-row">
            <div class="form-group">
              <label for="filePath">Ruta del Archivo:</label>
              <input
                type="text"
                id="filePath"
                placeholder="/path/to/file.csv" />
            </div>
            <div class="form-group">
              <label for="userId">ID Usuario:</label>
              <input
                type="number"
                id="userId"
                placeholder="123" />
            </div>
          </div>
        </div>

        <div
          id="reportFields"
          style="display: none;">
          <div class="form-row">
            <div class="form-group">
              <label for="reportUserId">ID Usuario:</label>
              <input
                type="number"
                id="reportUserId"
                placeholder="123" />
            </div>
            <div class="form-group">
              <label for="reportType">Tipo de Reporte:</label>
              <select id="reportType">
                <option value="sales">Ventas</option>
                <option value="analytics">Analytics</option>
                <option value="users">Usuarios</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      <!-- Lista de tareas -->
      <div class="tasks-list">
        <h3>Tareas Activas</h3>
        <div
          id="tasksList"
          class="loading">
          Cargando tareas...
        </div>
      </div>
    </div>

    <script>
      let tasks = new Map();

      // Cambiar campos según tipo de tarea
      document
        .getElementById('taskType')
        .addEventListener('change', function () {
          const type = this.value;
          document.getElementById('emailFields').style.display =
            type === 'email' ? 'block' : 'none';
          document.getElementById('fileFields').style.display =
            type === 'file' ? 'block' : 'none';
          document.getElementById('reportFields').style.display =
            type === 'report' ? 'block' : 'none';
        });

      // Crear nueva tarea
      async function createTask() {
        const type = document.getElementById('taskType').value;
        let endpoint, data;

        switch (type) {
          case 'email':
            endpoint = '/tasks/email/celery';
            data = {
              email: document.getElementById('email').value,
              subject: document.getElementById('subject').value,
              body: document.getElementById('body').value,
            };
            break;
          case 'file':
            endpoint = '/tasks/file/process';
            data = {
              file_path: document.getElementById('filePath').value,
              user_id: parseInt(document.getElementById('userId').value),
            };
            break;
          case 'report':
            endpoint = `/tasks/report/generate?user_id=${
              document.getElementById('reportUserId').value
            }&report_type=${document.getElementById('reportType').value}`;
            data = null;
            break;
        }

        try {
          const response = await fetch(endpoint, {
            method: 'POST',
            headers: data ? { 'Content-Type': 'application/json' } : {},
            body: data ? JSON.stringify(data) : null,
          });

          const result = await response.json();

          if (response.ok) {
            // Añadir tarea a la lista
            tasks.set(result.task_id, {
              ...result,
              type: type,
              created_at: new Date(),
            });

            // Limpiar formulario
            clearForm();

            // Actualizar vista
            renderTasks();
            updateStats();

            // Mostrar notificación
            alert('Tarea creada exitosamente!');
          } else {
            alert(
              'Error al crear tarea: ' + (result.detail || 'Error desconocido')
            );
          }
        } catch (error) {
          console.error('Error:', error);
          alert('Error al comunicarse con el servidor');
        }
      }

      // Limpiar formulario
      function clearForm() {
        document.getElementById('email').value = '';
        document.getElementById('subject').value = '';
        document.getElementById('body').value = '';
        document.getElementById('filePath').value = '';
        document.getElementById('userId').value = '';
        document.getElementById('reportUserId').value = '';
      }

      // Obtener estado de tarea
      async function getTaskStatus(taskId) {
        try {
          const response = await fetch(`/tasks/status/${taskId}`);
          if (response.ok) {
            return await response.json();
          }
        } catch (error) {
          console.error('Error obteniendo estado:', error);
        }
        return null;
      }

      // Cancelar tarea
      async function cancelTask(taskId) {
        if (!confirm('¿Estás seguro de que quieres cancelar esta tarea?')) {
          return;
        }

        try {
          const response = await fetch(`/tasks/cancel/${taskId}`, {
            method: 'DELETE',
          });

          if (response.ok) {
            // Actualizar estado local
            const task = tasks.get(taskId);
            if (task) {
              task.status = 'REVOKED';
              tasks.set(taskId, task);
            }

            renderTasks();
            updateStats();
            alert('Tarea cancelada');
          } else {
            alert('Error al cancelar tarea');
          }
        } catch (error) {
          console.error('Error:', error);
          alert('Error al comunicarse con el servidor');
        }
      }

      // Renderizar lista de tareas
      function renderTasks() {
        const container = document.getElementById('tasksList');

        if (tasks.size === 0) {
          container.innerHTML = '<div class="loading">No hay tareas</div>';
          return;
        }

        const tasksArray = Array.from(tasks.values()).sort(
          (a, b) => new Date(b.created_at) - new Date(a.created_at)
        );

        container.innerHTML = tasksArray
          .map(
            (task) => `
                <div class="task-item">
                    <div class="task-header">
                        <span class="task-id">${task.task_id}</span>
                        <span class="task-status status-${(
                          task.state ||
                          task.status ||
                          'pending'
                        ).toLowerCase()}">
                            ${task.state || task.status || 'PENDING'}
                        </span>
                    </div>
                    
                    <div><strong>Tipo:</strong> ${task.type || 'N/A'}</div>
                    <div><strong>Creada:</strong> ${new Date(
                      task.created_at
                    ).toLocaleString()}</div>
                    
                    ${
                      task.current !== undefined
                        ? `
                        <div class="progress-bar">
                            <div class="progress-fill" style="width: ${
                              (task.current / task.total) * 100
                            }%"></div>
                        </div>
                        <div>Progreso: ${task.current}/${task.total} - ${
                            task.status || ''
                          }</div>
                    `
                        : ''
                    }
                    
                    ${
                      task.result
                        ? `
                        <div><strong>Resultado:</strong> <pre>${JSON.stringify(
                          task.result,
                          null,
                          2
                        )}</pre></div>
                    `
                        : ''
                    }
                    
                    ${
                      task.error
                        ? `
                        <div style="color: red;"><strong>Error:</strong> ${task.error}</div>
                    `
                        : ''
                    }
                    
                    <div class="task-actions">
                        <button class="btn-small" onclick="refreshTask('${
                          task.task_id
                        }')">Actualizar</button>
                        <button class="btn-small btn-danger" onclick="cancelTask('${
                          task.task_id
                        }')">Cancelar</button>
                    </div>
                </div>
            `
          )
          .join('');
      }

      // Actualizar estado de tarea específica
      async function refreshTask(taskId) {
        const status = await getTaskStatus(taskId);
        if (status) {
          const task = tasks.get(taskId);
          if (task) {
            Object.assign(task, status);
            tasks.set(taskId, task);
            renderTasks();
            updateStats();
          }
        }
      }

      // Actualizar todas las tareas
      async function refreshAllTasks() {
        for (const taskId of tasks.keys()) {
          await refreshTask(taskId);
        }
      }

      // Actualizar estadísticas
      function updateStats() {
        const total = tasks.size;
        let active = 0,
          completed = 0,
          failed = 0;

        for (const task of tasks.values()) {
          const state = (task.state || task.status || 'PENDING').toUpperCase();

          if (state === 'PENDING' || state === 'PROCESSING') {
            active++;
          } else if (state === 'SUCCESS') {
            completed++;
          } else if (state === 'FAILURE' || state === 'REVOKED') {
            failed++;
          }
        }

        document.getElementById('totalTasks').textContent = total;
        document.getElementById('activeTasks').textContent = active;
        document.getElementById('completedTasks').textContent = completed;
        document.getElementById('failedTasks').textContent = failed;
      }

      // Inicializar
      document.addEventListener('DOMContentLoaded', function () {
        // Mostrar campos de email por defecto
        document.getElementById('emailFields').style.display = 'block';

        // Actualizar cada 5 segundos
        setInterval(refreshAllTasks, 5000);

        // Cargar tareas iniciales
        renderTasks();
        updateStats();
      });
    </script>
  </body>
</html>
```

## 6. Testing (5 min)

### Tests para Background Tasks

```python
# tests/test_background_tasks.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.background.celery_app import celery_app

client = TestClient(app)

class TestBackgroundTasks:

    def test_simple_email_task(self):
        """Test de envío de email simple"""
        response = client.post("/tasks/email/simple", json={
            "email": "test@example.com",
            "subject": "Test Subject",
            "body": "Test body"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "pending"
        assert "task_id" in data

    def test_celery_email_task(self):
        """Test de envío de email con Celery"""
        response = client.post("/tasks/email/celery", json={
            "email": "test@example.com",
            "subject": "Test Subject",
            "body": "Test body"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "pending"
        assert "task_id" in data

    def test_file_processing_task(self):
        """Test de procesamiento de archivo"""
        response = client.post("/tasks/file/process", json={
            "file_path": "/tmp/test.csv",
            "user_id": 123
        })

        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data

    def test_task_status(self):
        """Test de consulta de estado de tarea"""
        # Crear tarea
        response = client.post("/tasks/email/celery", json={
            "email": "test@example.com",
            "subject": "Test",
            "body": "Test"
        })

        task_id = response.json()["task_id"]

        # Consultar estado
        status_response = client.get(f"/tasks/status/{task_id}")
        assert status_response.status_code == 200

        status_data = status_response.json()
        assert "task_id" in status_data
        assert "state" in status_data

    def test_nonexistent_task_status(self):
        """Test de consulta de tarea inexistente"""
        response = client.get("/tasks/status/nonexistent-id")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_background_task_execution(self):
        """Test de ejecución real de tarea"""
        from app.background.tasks import send_email_task

        result = await send_email_task(
            "test@example.com",
            "Test Subject",
            "Test Body"
        )

        assert result["status"] == "sent"
        assert result["email"] == "test@example.com"
```

## 7. Monitoreo con Flower (5 min)

### Configuración de Flower

```python
# flower_config.py
from celery import Celery

# Configuración para Flower
flower_app = Celery('flower_monitor')
flower_app.config_from_object('app.background.celery_app')

# Comando para ejecutar Flower:
# flower -A app.background.celery_app --port=5555
```

### Script de Monitoreo

```python
# monitor_tasks.py
import requests
import time
from datetime import datetime

def monitor_celery_workers():
    """Monitorea el estado de los workers de Celery"""
    try:
        # Conectar a Flower API
        response = requests.get("http://localhost:5555/api/workers")

        if response.status_code == 200:
            workers = response.json()
            print(f"[{datetime.now()}] Workers activos: {len(workers)}")

            for worker_name, worker_info in workers.items():
                print(f"  - {worker_name}: {worker_info.get('status', 'unknown')}")
        else:
            print("Error conectando a Flower")

    except Exception as e:
        print(f"Error en monitoreo: {e}")

if __name__ == "__main__":
    while True:
        monitor_celery_workers()
        time.sleep(30)  # Monitorear cada 30 segundos
```

## Resumen y Próximos Pasos

### Lo que has aprendido:

1. ✅ **Background Tasks básicas** con FastAPI
2. ✅ **Celery y Redis** para tareas avanzadas
3. ✅ **Monitoreo y tracking** de progreso
4. ✅ **APIs RESTful** para gestión de tareas
5. ✅ **Dashboard interactivo** para visualización

### Tareas para consolidar:

- [ ] Implementar notificaciones por WebSocket cuando las tareas terminen
- [ ] Añadir autenticación a las rutas de tareas
- [ ] Configurar logging avanzado
- [ ] Implementar retry policies personalizadas
- [ ] Crear métricas de rendimiento

### Conexión con la siguiente práctica:

En la **Práctica 37** integraremos **Server-Sent Events (SSE)** para notificaciones en tiempo real sobre el estado de estas tareas en background.

---

**💡 Tip Profesional:** Las background tasks son esenciales para crear aplicaciones escalables. Combínalas con WebSockets (Práctica 35) para una experiencia de usuario excepcional.
