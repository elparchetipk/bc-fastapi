# Práctica 37: Server-Sent Events (SSE) y Streaming de Datos

## Objetivos

- Implementar Server-Sent Events con FastAPI
- Crear streams de datos en tiempo real
- Desarrollar dashboard con actualizaciones automáticas
- Integrar SSE con WebSockets y Background Tasks

## Duración: 90 minutos

## Prerrequisitos

- ✅ FastAPI instalado y configurado
- ✅ Conocimiento de async/await
- ✅ Práctica 35 (WebSockets) completada
- ✅ Práctica 36 (Background Tasks) completada

## 1. Introducción a Server-Sent Events (15 min)

### Conceptos Clave

Server-Sent Events (SSE) es una tecnología que permite al servidor enviar datos al cliente de forma unidireccional en tiempo real, ideal para notificaciones, actualizaciones de estado y streaming de datos.

**Ventajas de SSE:**

- Más simple que WebSockets para comunicación unidireccional
- Reconexión automática
- Soporte nativo en navegadores
- Funciona sobre HTTP/HTTPS estándar

**Casos de uso:**

- Dashboards en tiempo real
- Notificaciones push
- Feeds de noticias
- Monitoreo de sistemas
- Actualizaciones de progreso

### Comparación: SSE vs WebSockets vs Polling

```python
# comparison_example.py

"""
POLLING (Tradicional):
- Cliente consulta cada X segundos
- Mayor uso de recursos
- Latencia alta
- Simple de implementar

SSE (Server-Sent Events):
- Servidor envía cuando hay datos
- Unidireccional (servidor → cliente)
- Reconexión automática
- Ideal para notificaciones

WEBSOCKETS:
- Bidireccional en tiempo real
- Más complejo
- Ideal para chat, juegos
- Mayor overhead
"""
```

## 2. Implementación Básica de SSE (20 min)

### Estructura del Proyecto

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── sse/
│   │   ├── __init__.py
│   │   ├── events.py
│   │   ├── streams.py
│   │   └── managers.py
│   ├── models/
│   │   └── sse_models.py
│   └── api/
│       └── sse_routes.py
├── static/
│   ├── sse_dashboard.html
│   ├── notifications.html
│   └── monitoring.html
└── requirements.txt
```

### Modelos Base

```python
# app/models/sse_models.py
from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict, Optional
from enum import Enum

class EventType(str, Enum):
    NOTIFICATION = "notification"
    TASK_UPDATE = "task_update"
    SYSTEM_ALERT = "system_alert"
    USER_ACTION = "user_action"
    METRIC_UPDATE = "metric_update"

class SSEEvent(BaseModel):
    id: str
    event: EventType
    data: Dict[str, Any]
    timestamp: datetime
    user_id: Optional[int] = None
    channel: Optional[str] = None

class NotificationEvent(BaseModel):
    title: str
    message: str
    level: str = "info"  # info, warning, error, success
    action_url: Optional[str] = None

class TaskProgressEvent(BaseModel):
    task_id: str
    progress: int  # 0-100
    status: str
    message: str

class MetricEvent(BaseModel):
    metric_name: str
    value: float
    unit: str
    timestamp: datetime
```

### SSE Event Manager

```python
# app/sse/managers.py
import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, Set, AsyncGenerator, Optional
from fastapi import Request
import logging

logger = logging.getLogger(__name__)

class SSEManager:
    def __init__(self):
        # Conexiones activas por canal
        self.connections: Dict[str, Set[asyncio.Queue]] = {}
        # Conexiones por usuario
        self.user_connections: Dict[int, Set[asyncio.Queue]] = {}

    async def connect(
        self,
        channel: str = "general",
        user_id: Optional[int] = None,
        request: Optional[Request] = None
    ) -> AsyncGenerator[str, None]:
        """Conecta un cliente a un canal SSE"""
        queue = asyncio.Queue()

        # Añadir a canal
        if channel not in self.connections:
            self.connections[channel] = set()
        self.connections[channel].add(queue)

        # Añadir a usuario
        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            self.user_connections[user_id].add(queue)

        logger.info(f"Cliente conectado al canal '{channel}' (user_id: {user_id})")

        try:
            # Enviar evento de conexión
            await self.send_to_queue(queue, {
                "event": "connected",
                "data": {
                    "channel": channel,
                    "timestamp": datetime.now().isoformat(),
                    "message": f"Conectado al canal {channel}"
                }
            })

            # Loop principal de eventos
            while True:
                try:
                    # Esperar por eventos (con timeout para heartbeat)
                    event_data = await asyncio.wait_for(queue.get(), timeout=30)
                    yield f"data: {json.dumps(event_data)}\n\n"

                except asyncio.TimeoutError:
                    # Enviar heartbeat
                    yield f"data: {json.dumps({'event': 'heartbeat', 'timestamp': datetime.now().isoformat()})}\n\n"

        except asyncio.CancelledError:
            logger.info("Conexión SSE cancelada")
        finally:
            # Limpiar conexiones
            await self.disconnect(queue, channel, user_id)

    async def disconnect(
        self,
        queue: asyncio.Queue,
        channel: str,
        user_id: Optional[int] = None
    ):
        """Desconecta un cliente"""
        # Remover de canal
        if channel in self.connections:
            self.connections[channel].discard(queue)
            if not self.connections[channel]:
                del self.connections[channel]

        # Remover de usuario
        if user_id and user_id in self.user_connections:
            self.user_connections[user_id].discard(queue)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

        logger.info(f"Cliente desconectado del canal '{channel}' (user_id: {user_id})")

    async def send_to_queue(self, queue: asyncio.Queue, data: dict):
        """Envía datos a una cola específica"""
        try:
            await queue.put(data)
        except Exception as e:
            logger.error(f"Error enviando a cola: {e}")

    async def broadcast_to_channel(self, channel: str, event_data: dict):
        """Envía evento a todos los clientes de un canal"""
        if channel in self.connections:
            logger.info(f"Broadcasting a canal '{channel}': {len(self.connections[channel])} clientes")

            # Crear lista de tareas para envío concurrente
            tasks = []
            for queue in self.connections[channel].copy():  # Usar copia para evitar modificaciones concurrentes
                tasks.append(self.send_to_queue(queue, event_data))

            # Ejecutar todas las tareas
            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    async def send_to_user(self, user_id: int, event_data: dict):
        """Envía evento a un usuario específico"""
        if user_id in self.user_connections:
            logger.info(f"Enviando evento a usuario {user_id}")

            tasks = []
            for queue in self.user_connections[user_id].copy():
                tasks.append(self.send_to_queue(queue, event_data))

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

    def get_stats(self) -> dict:
        """Obtiene estadísticas de conexiones"""
        total_connections = sum(len(queues) for queues in self.connections.values())

        return {
            "total_connections": total_connections,
            "channels": {
                channel: len(queues)
                for channel, queues in self.connections.items()
            },
            "users_connected": len(self.user_connections),
            "timestamp": datetime.now().isoformat()
        }

# Instancia global del manager
sse_manager = SSEManager()
```

### Streams de Datos Específicos

```python
# app/sse/streams.py
import asyncio
import random
from datetime import datetime, timedelta
from typing import AsyncGenerator
import psutil  # Para métricas del sistema
import json

async def system_metrics_stream() -> AsyncGenerator[dict, None]:
    """Stream de métricas del sistema"""
    while True:
        try:
            # Obtener métricas reales del sistema
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            metrics = {
                "event": "system_metrics",
                "data": {
                    "cpu_percent": round(cpu_percent, 2),
                    "memory_percent": round(memory.percent, 2),
                    "memory_used_gb": round(memory.used / (1024**3), 2),
                    "memory_total_gb": round(memory.total / (1024**3), 2),
                    "disk_percent": round((disk.used / disk.total) * 100, 2),
                    "disk_free_gb": round(disk.free / (1024**3), 2),
                    "timestamp": datetime.now().isoformat()
                }
            }

            yield metrics
            await asyncio.sleep(5)  # Actualizar cada 5 segundos

        except Exception as e:
            print(f"Error en métricas del sistema: {e}")
            await asyncio.sleep(10)

async def fake_trading_stream() -> AsyncGenerator[dict, None]:
    """Stream simulado de datos de trading"""
    symbols = ["BTC/USD", "ETH/USD", "ADA/USD", "DOT/USD", "SOL/USD"]
    prices = {symbol: random.uniform(100, 50000) for symbol in symbols}

    while True:
        # Simular cambios de precio
        symbol = random.choice(symbols)
        change_percent = random.uniform(-5, 5)
        old_price = prices[symbol]
        new_price = old_price * (1 + change_percent / 100)
        prices[symbol] = new_price

        event = {
            "event": "price_update",
            "data": {
                "symbol": symbol,
                "price": round(new_price, 2),
                "change": round(new_price - old_price, 2),
                "change_percent": round(change_percent, 2),
                "volume": random.randint(1000, 100000),
                "timestamp": datetime.now().isoformat()
            }
        }

        yield event
        await asyncio.sleep(random.uniform(0.5, 3))  # Frecuencia variable

async def log_stream() -> AsyncGenerator[dict, None]:
    """Stream simulado de logs del sistema"""
    log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    services = ["api", "database", "auth", "cache", "worker"]

    while True:
        level = random.choice(log_levels)
        service = random.choice(services)

        # Simular diferentes tipos de mensajes
        if level == "ERROR":
            messages = [
                f"Connection timeout to database",
                f"Failed to process request: invalid token",
                f"Service {service} is not responding"
            ]
        elif level == "WARNING":
            messages = [
                f"High memory usage detected: 85%",
                f"Slow query detected: 2.5s",
                f"Rate limit approaching for user"
            ]
        else:
            messages = [
                f"User logged in successfully",
                f"Cache hit ratio: 95%",
                f"Background task completed"
            ]

        event = {
            "event": "log_entry",
            "data": {
                "level": level,
                "service": service,
                "message": random.choice(messages),
                "timestamp": datetime.now().isoformat(),
                "request_id": f"req_{random.randint(10000, 99999)}"
            }
        }

        yield event
        await asyncio.sleep(random.uniform(1, 5))

async def notification_stream() -> AsyncGenerator[dict, None]:
    """Stream de notificaciones del sistema"""
    notification_types = [
        {"type": "info", "title": "Nueva función disponible", "message": "Hemos añadido notificaciones en tiempo real"},
        {"type": "warning", "title": "Mantenimiento programado", "message": "El sistema estará en mantenimiento mañana a las 2 AM"},
        {"type": "success", "title": "Backup completado", "message": "El backup diario se ha completado exitosamente"},
        {"type": "error", "title": "Error de conexión", "message": "Problemas temporales con la base de datos"},
    ]

    while True:
        # Enviar notificación cada 30-60 segundos
        await asyncio.sleep(random.uniform(30, 60))

        notification = random.choice(notification_types)
        event = {
            "event": "notification",
            "data": {
                **notification,
                "id": f"notif_{random.randint(1000, 9999)}",
                "timestamp": datetime.now().isoformat(),
                "read": False
            }
        }

        yield event
```

## 3. API Endpoints para SSE (15 min)

### Rutas principales

```python
# app/api/sse_routes.py
from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import StreamingResponse
from ..sse.managers import sse_manager
from ..sse.streams import system_metrics_stream, fake_trading_stream, log_stream, notification_stream
from ..models.sse_models import *
from datetime import datetime
import asyncio
import json
from typing import Optional

router = APIRouter(prefix="/sse", tags=["server-sent-events"])

@router.get("/events")
async def sse_endpoint(
    request: Request,
    channel: str = Query("general", description="Canal al que conectarse"),
    user_id: Optional[int] = Query(None, description="ID del usuario")
):
    """Endpoint principal para Server-Sent Events"""

    async def event_generator():
        async for event in sse_manager.connect(channel=channel, user_id=user_id, request=request):
            yield event

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )

@router.get("/metrics")
async def system_metrics_endpoint(request: Request):
    """Stream de métricas del sistema"""

    async def metrics_generator():
        async for metric in system_metrics_stream():
            # Enviar también al canal general
            await sse_manager.broadcast_to_channel("metrics", metric)
            yield f"data: {json.dumps(metric)}\n\n"

    return StreamingResponse(
        metrics_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@router.get("/trading")
async def trading_stream_endpoint(request: Request):
    """Stream de datos de trading simulados"""

    async def trading_generator():
        async for trade_data in fake_trading_stream():
            await sse_manager.broadcast_to_channel("trading", trade_data)
            yield f"data: {json.dumps(trade_data)}\n\n"

    return StreamingResponse(
        trading_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@router.get("/logs")
async def logs_stream_endpoint(request: Request):
    """Stream de logs del sistema"""

    async def logs_generator():
        async for log_entry in log_stream():
            await sse_manager.broadcast_to_channel("logs", log_entry)
            yield f"data: {json.dumps(log_entry)}\n\n"

    return StreamingResponse(
        logs_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@router.get("/notifications/{user_id}")
async def user_notifications_endpoint(request: Request, user_id: int):
    """Stream de notificaciones para usuario específico"""

    async def notifications_generator():
        async for notification in notification_stream():
            # Enviar a usuario específico
            await sse_manager.send_to_user(user_id, notification)
            yield f"data: {json.dumps(notification)}\n\n"

    return StreamingResponse(
        notifications_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

@router.post("/broadcast/{channel}")
async def broadcast_message(
    channel: str,
    message: dict,
    user_id: Optional[int] = None
):
    """Envía un mensaje a todos los clientes de un canal"""

    event_data = {
        "event": "broadcast",
        "data": {
            **message,
            "channel": channel,
            "timestamp": datetime.now().isoformat(),
            "sender": user_id
        }
    }

    await sse_manager.broadcast_to_channel(channel, event_data)

    return {
        "status": "sent",
        "channel": channel,
        "message": "Mensaje enviado exitosamente"
    }

@router.post("/notify/{user_id}")
async def send_user_notification(
    user_id: int,
    notification: NotificationEvent
):
    """Envía notificación a usuario específico"""

    event_data = {
        "event": "notification",
        "data": {
            **notification.dict(),
            "timestamp": datetime.now().isoformat(),
            "id": f"notif_{datetime.now().timestamp()}"
        }
    }

    await sse_manager.send_to_user(user_id, event_data)

    return {
        "status": "sent",
        "user_id": user_id,
        "message": "Notificación enviada"
    }

@router.get("/stats")
async def get_sse_stats():
    """Obtiene estadísticas de conexiones SSE"""
    return sse_manager.get_stats()

@router.post("/task-update")
async def broadcast_task_update(task_update: TaskProgressEvent):
    """Actualización de progreso de tarea"""

    event_data = {
        "event": "task_update",
        "data": {
            **task_update.dict(),
            "timestamp": datetime.now().isoformat()
        }
    }

    # Enviar a canal de tareas
    await sse_manager.broadcast_to_channel("tasks", event_data)

    return {"status": "broadcasted", "task_id": task_update.task_id}
```

## 4. Dashboard Interactivo (25 min)

### Dashboard Principal con SSE

```html
<!-- static/sse_dashboard.html -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0" />
    <title>Dashboard SSE en Tiempo Real</title>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 20px;
      }

      .dashboard {
        max-width: 1400px;
        margin: 0 auto;
        display: grid;
        gap: 20px;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      }

      .card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: transform 0.3s ease;
      }

      .card:hover {
        transform: translateY(-5px);
      }

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid #e0e0e0;
      }

      .card-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #333;
      }

      .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        animation: pulse 2s infinite;
      }

      .status-connected {
        background: #28a745;
      }
      .status-disconnected {
        background: #dc3545;
      }
      .status-connecting {
        background: #ffc107;
      }

      @keyframes pulse {
        0% {
          opacity: 1;
        }
        50% {
          opacity: 0.5;
        }
        100% {
          opacity: 1;
        }
      }

      .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 15px;
      }

      .metric-item {
        text-align: center;
        padding: 15px;
        background: linear-gradient(135deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        transition: all 0.3s ease;
      }

      .metric-item:hover {
        transform: scale(1.05);
      }

      .metric-value {
        font-size: 1.8em;
        font-weight: bold;
        color: #007bff;
      }

      .metric-label {
        font-size: 0.9em;
        color: #666;
        margin-top: 5px;
      }

      .trading-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        margin: 5px 0;
        border-radius: 8px;
        transition: all 0.3s ease;
      }

      .price-up {
        background: rgba(40, 167, 69, 0.1);
        border-left: 4px solid #28a745;
      }

      .price-down {
        background: rgba(220, 53, 69, 0.1);
        border-left: 4px solid #dc3545;
      }

      .price-neutral {
        background: rgba(108, 117, 125, 0.1);
        border-left: 4px solid #6c757d;
      }

      .symbol {
        font-weight: bold;
      }

      .price {
        font-size: 1.1em;
      }

      .change {
        font-size: 0.9em;
        font-weight: bold;
      }

      .change-positive {
        color: #28a745;
      }
      .change-negative {
        color: #dc3545;
      }

      .log-entry {
        padding: 8px 12px;
        margin: 5px 0;
        border-radius: 6px;
        font-family: 'Courier New', monospace;
        font-size: 0.9em;
        border-left: 4px solid;
      }

      .log-info {
        background: rgba(23, 162, 184, 0.1);
        border-left-color: #17a2b8;
      }

      .log-warning {
        background: rgba(255, 193, 7, 0.1);
        border-left-color: #ffc107;
      }

      .log-error {
        background: rgba(220, 53, 69, 0.1);
        border-left-color: #dc3545;
      }

      .log-debug {
        background: rgba(108, 117, 125, 0.1);
        border-left-color: #6c757d;
      }

      .notification {
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        border-left: 4px solid;
        animation: slideIn 0.5s ease;
      }

      @keyframes slideIn {
        from {
          transform: translateX(-100%);
          opacity: 0;
        }
        to {
          transform: translateX(0);
          opacity: 1;
        }
      }

      .notification-info {
        background: rgba(23, 162, 184, 0.1);
        border-left-color: #17a2b8;
      }

      .notification-warning {
        background: rgba(255, 193, 7, 0.1);
        border-left-color: #ffc107;
      }

      .notification-success {
        background: rgba(40, 167, 69, 0.1);
        border-left-color: #28a745;
      }

      .notification-error {
        background: rgba(220, 53, 69, 0.1);
        border-left-color: #dc3545;
      }

      .notification-title {
        font-weight: bold;
        margin-bottom: 5px;
      }

      .notification-message {
        color: #666;
      }

      .notification-time {
        font-size: 0.8em;
        color: #999;
        margin-top: 5px;
      }

      .controls {
        display: flex;
        gap: 10px;
        margin-bottom: 20px;
        flex-wrap: wrap;
      }

      button {
        padding: 8px 16px;
        border: none;
        border-radius: 6px;
        background: #007bff;
        color: white;
        cursor: pointer;
        transition: background 0.3s ease;
      }

      button:hover {
        background: #0056b3;
      }

      button:disabled {
        background: #6c757d;
        cursor: not-allowed;
      }

      .btn-success {
        background: #28a745;
      }
      .btn-success:hover {
        background: #1e7e34;
      }

      .btn-warning {
        background: #ffc107;
        color: #212529;
      }
      .btn-warning:hover {
        background: #e0a800;
      }

      .btn-danger {
        background: #dc3545;
      }
      .btn-danger:hover {
        background: #c82333;
      }

      .scrollable {
        max-height: 300px;
        overflow-y: auto;
        scrollbar-width: thin;
      }

      .scrollable::-webkit-scrollbar {
        width: 6px;
      }

      .scrollable::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 3px;
      }

      .scrollable::-webkit-scrollbar-thumb {
        background: #c1c1c1;
        border-radius: 3px;
      }

      .scrollable::-webkit-scrollbar-thumb:hover {
        background: #a8a8a8;
      }

      .header {
        text-align: center;
        margin-bottom: 30px;
        color: white;
      }

      .header h1 {
        font-size: 2.5em;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
      }

      .connection-status {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 0.9em;
      }
    </style>
  </head>
  <body>
    <div class="header">
      <h1>🚀 Dashboard SSE en Tiempo Real</h1>
      <p>Monitoreo avanzado con Server-Sent Events</p>
    </div>

    <div class="dashboard">
      <!-- Métricas del Sistema -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">📊 Métricas del Sistema</h3>
          <div class="connection-status">
            <span id="metricsStatus">Conectando...</span>
            <div
              id="metricsIndicator"
              class="status-indicator status-connecting"></div>
          </div>
        </div>
        <div
          class="metrics-grid"
          id="systemMetrics">
          <div class="metric-item">
            <div
              class="metric-value"
              id="cpuValue">
              --
            </div>
            <div class="metric-label">CPU %</div>
          </div>
          <div class="metric-item">
            <div
              class="metric-value"
              id="memoryValue">
              --
            </div>
            <div class="metric-label">Memoria %</div>
          </div>
          <div class="metric-item">
            <div
              class="metric-value"
              id="diskValue">
              --
            </div>
            <div class="metric-label">Disco %</div>
          </div>
        </div>
      </div>

      <!-- Trading en Tiempo Real -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">💹 Trading en Vivo</h3>
          <div class="connection-status">
            <span id="tradingStatus">Conectando...</span>
            <div
              id="tradingIndicator"
              class="status-indicator status-connecting"></div>
          </div>
        </div>
        <div
          class="scrollable"
          id="tradingData">
          <div style="text-align: center; color: #666;">
            Esperando datos de trading...
          </div>
        </div>
      </div>

      <!-- Logs del Sistema -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">📝 Logs del Sistema</h3>
          <div class="connection-status">
            <span id="logsStatus">Conectando...</span>
            <div
              id="logsIndicator"
              class="status-indicator status-connecting"></div>
          </div>
        </div>
        <div class="controls">
          <button onclick="clearLogs()">Limpiar Logs</button>
          <button
            onclick="toggleLogLevel('error')"
            id="errorBtn">
            Errores
          </button>
          <button
            onclick="toggleLogLevel('warning')"
            id="warningBtn">
            Warnings
          </button>
          <button
            onclick="toggleLogLevel('info')"
            id="infoBtn">
            Info
          </button>
        </div>
        <div
          class="scrollable"
          id="systemLogs">
          <div style="text-align: center; color: #666;">Esperando logs...</div>
        </div>
      </div>

      <!-- Notificaciones -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">🔔 Notificaciones</h3>
          <div class="connection-status">
            <span id="notificationsStatus">Conectando...</span>
            <div
              id="notificationsIndicator"
              class="status-indicator status-connecting"></div>
          </div>
        </div>
        <div class="controls">
          <button
            onclick="sendTestNotification()"
            class="btn-success">
            Enviar Test
          </button>
          <button
            onclick="clearNotifications()"
            class="btn-warning">
            Limpiar
          </button>
        </div>
        <div
          class="scrollable"
          id="notifications">
          <div style="text-align: center; color: #666;">Sin notificaciones</div>
        </div>
      </div>

      <!-- Estadísticas de Conexiones -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">🌐 Estadísticas SSE</h3>
          <button
            onclick="refreshStats()"
            class="btn-success">
            Actualizar
          </button>
        </div>
        <div id="sseStats">
          <div style="text-align: center; color: #666;">
            Cargando estadísticas...
          </div>
        </div>
      </div>

      <!-- Control de Conexiones -->
      <div class="card">
        <div class="card-header">
          <h3 class="card-title">⚙️ Control de Conexiones</h3>
        </div>
        <div class="controls">
          <button
            onclick="connectAll()"
            class="btn-success">
            Conectar Todo
          </button>
          <button
            onclick="disconnectAll()"
            class="btn-danger">
            Desconectar Todo
          </button>
          <button
            onclick="reconnectAll()"
            class="btn-warning">
            Reconectar
          </button>
        </div>
        <div>
          <p><strong>Estado de Conexiones:</strong></p>
          <ul id="connectionsList">
            <li>
              Métricas: <span id="metricsConnectionStatus">Desconectado</span>
            </li>
            <li>
              Trading: <span id="tradingConnectionStatus">Desconectado</span>
            </li>
            <li>Logs: <span id="logsConnectionStatus">Desconectado</span></li>
            <li>
              Notificaciones:
              <span id="notificationsConnectionStatus">Desconectado</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <script>
      class SSEDashboard {
        constructor() {
          this.connections = {
            metrics: null,
            trading: null,
            logs: null,
            notifications: null,
          };

          this.logFilters = {
            error: true,
            warning: true,
            info: true,
            debug: true,
          };

          this.tradingData = new Map();
          this.init();
        }

        init() {
          this.connectAll();
          this.refreshStats();

          // Actualizar estadísticas cada 30 segundos
          setInterval(() => this.refreshStats(), 30000);
        }

        // Conexión a métricas del sistema
        connectMetrics() {
          this.updateConnectionStatus('metrics', 'connecting');

          this.connections.metrics = new EventSource('/sse/metrics');

          this.connections.metrics.onopen = () => {
            this.updateConnectionStatus('metrics', 'connected');
          };

          this.connections.metrics.onmessage = (event) => {
            try {
              const data = JSON.parse(event.data);
              if (data.event === 'system_metrics') {
                this.updateSystemMetrics(data.data);
              }
            } catch (error) {
              console.error('Error parseando métricas:', error);
            }
          };

          this.connections.metrics.onerror = () => {
            this.updateConnectionStatus('metrics', 'disconnected');
          };
        }

        // Conexión a trading
        connectTrading() {
          this.updateConnectionStatus('trading', 'connecting');

          this.connections.trading = new EventSource('/sse/trading');

          this.connections.trading.onopen = () => {
            this.updateConnectionStatus('trading', 'connected');
          };

          this.connections.trading.onmessage = (event) => {
            try {
              const data = JSON.parse(event.data);
              if (data.event === 'price_update') {
                this.updateTradingData(data.data);
              }
            } catch (error) {
              console.error('Error parseando trading:', error);
            }
          };

          this.connections.trading.onerror = () => {
            this.updateConnectionStatus('trading', 'disconnected');
          };
        }

        // Conexión a logs
        connectLogs() {
          this.updateConnectionStatus('logs', 'connecting');

          this.connections.logs = new EventSource('/sse/logs');

          this.connections.logs.onopen = () => {
            this.updateConnectionStatus('logs', 'connected');
          };

          this.connections.logs.onmessage = (event) => {
            try {
              const data = JSON.parse(event.data);
              if (data.event === 'log_entry') {
                this.addLogEntry(data.data);
              }
            } catch (error) {
              console.error('Error parseando logs:', error);
            }
          };

          this.connections.logs.onerror = () => {
            this.updateConnectionStatus('logs', 'disconnected');
          };
        }

        // Conexión a notificaciones (usuario demo: ID 1)
        connectNotifications() {
          this.updateConnectionStatus('notifications', 'connecting');

          this.connections.notifications = new EventSource(
            '/sse/notifications/1'
          );

          this.connections.notifications.onopen = () => {
            this.updateConnectionStatus('notifications', 'connected');
          };

          this.connections.notifications.onmessage = (event) => {
            try {
              const data = JSON.parse(event.data);
              if (data.event === 'notification') {
                this.addNotification(data.data);
              }
            } catch (error) {
              console.error('Error parseando notificación:', error);
            }
          };

          this.connections.notifications.onerror = () => {
            this.updateConnectionStatus('notifications', 'disconnected');
          };
        }

        updateConnectionStatus(type, status) {
          const statusElement = document.getElementById(`${type}Status`);
          const indicatorElement = document.getElementById(`${type}Indicator`);
          const connectionStatusElement = document.getElementById(
            `${type}ConnectionStatus`
          );

          if (statusElement) {
            statusElement.textContent =
              status === 'connected'
                ? 'Conectado'
                : status === 'connecting'
                ? 'Conectando...'
                : 'Desconectado';
          }

          if (indicatorElement) {
            indicatorElement.className = `status-indicator status-${status}`;
          }

          if (connectionStatusElement) {
            connectionStatusElement.textContent =
              status === 'connected'
                ? 'Conectado'
                : status === 'connecting'
                ? 'Conectando...'
                : 'Desconectado';
            connectionStatusElement.style.color =
              status === 'connected'
                ? '#28a745'
                : status === 'connecting'
                ? '#ffc107'
                : '#dc3545';
          }
        }

        updateSystemMetrics(metrics) {
          document.getElementById('cpuValue').textContent =
            metrics.cpu_percent + '%';
          document.getElementById('memoryValue').textContent =
            metrics.memory_percent + '%';
          document.getElementById('diskValue').textContent =
            metrics.disk_percent + '%';
        }

        updateTradingData(data) {
          // Actualizar datos en memoria
          this.tradingData.set(data.symbol, data);

          // Renderizar tabla de trading
          const container = document.getElementById('tradingData');
          const sortedData = Array.from(this.tradingData.values()).sort(
            (a, b) => a.symbol.localeCompare(b.symbol)
          );

          container.innerHTML = sortedData
            .map((item) => {
              const changeClass =
                item.change > 0
                  ? 'price-up'
                  : item.change < 0
                  ? 'price-down'
                  : 'price-neutral';
              const changeTextClass =
                item.change > 0 ? 'change-positive' : 'change-negative';

              return `
                        <div class="trading-item ${changeClass}">
                            <div class="symbol">${item.symbol}</div>
                            <div class="price">$${item.price.toFixed(2)}</div>
                            <div class="change ${changeTextClass}">
                                ${
                                  item.change > 0 ? '+' : ''
                                }${item.change.toFixed(2)} 
                                (${
                                  item.change_percent > 0 ? '+' : ''
                                }${item.change_percent.toFixed(2)}%)
                            </div>
                        </div>
                    `;
            })
            .join('');
        }

        addLogEntry(log) {
          if (!this.logFilters[log.level.toLowerCase()]) {
            return; // Filtrado
          }

          const container = document.getElementById('systemLogs');
          const logElement = document.createElement('div');
          logElement.className = `log-entry log-${log.level.toLowerCase()}`;
          logElement.innerHTML = `
                    <strong>[${log.level}]</strong> 
                    <span style="color: #666;">${new Date(
                      log.timestamp
                    ).toLocaleTimeString()}</span> 
                    <strong>${log.service}:</strong> ${log.message}
                    <small style="float: right; color: #999;">${
                      log.request_id
                    }</small>
                `;

          container.appendChild(logElement);

          // Mantener solo últimas 50 entradas
          while (container.children.length > 50) {
            container.removeChild(container.firstChild);
          }

          // Scroll automático
          container.scrollTop = container.scrollHeight;
        }

        addNotification(notification) {
          const container = document.getElementById('notifications');

          // Crear elemento de notificación
          const notifElement = document.createElement('div');
          notifElement.className = `notification notification-${notification.type}`;
          notifElement.innerHTML = `
                    <div class="notification-title">${notification.title}</div>
                    <div class="notification-message">${
                      notification.message
                    }</div>
                    <div class="notification-time">${new Date(
                      notification.timestamp
                    ).toLocaleString()}</div>
                `;

          // Insertar al principio
          container.insertBefore(notifElement, container.firstChild);

          // Mantener solo últimas 10 notificaciones
          while (container.children.length > 10) {
            container.removeChild(container.lastChild);
          }
        }

        async refreshStats() {
          try {
            const response = await fetch('/sse/stats');
            const stats = await response.json();

            const container = document.getElementById('sseStats');
            container.innerHTML = `
                        <div class="metrics-grid">
                            <div class="metric-item">
                                <div class="metric-value">${
                                  stats.total_connections
                                }</div>
                                <div class="metric-label">Conexiones Totales</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-value">${
                                  stats.users_connected
                                }</div>
                                <div class="metric-label">Usuarios Conectados</div>
                            </div>
                            <div class="metric-item">
                                <div class="metric-value">${
                                  Object.keys(stats.channels).length
                                }</div>
                                <div class="metric-label">Canales Activos</div>
                            </div>
                        </div>
                        <div style="margin-top: 15px;">
                            <strong>Canales:</strong>
                            <ul style="margin-left: 20px; margin-top: 5px;">
                                ${Object.entries(stats.channels)
                                  .map(
                                    ([channel, count]) =>
                                      `<li>${channel}: ${count} conexiones</li>`
                                  )
                                  .join('')}
                            </ul>
                        </div>
                    `;
          } catch (error) {
            console.error('Error obteniendo estadísticas:', error);
          }
        }

        connectAll() {
          this.connectMetrics();
          this.connectTrading();
          this.connectLogs();
          this.connectNotifications();
        }

        disconnectAll() {
          Object.values(this.connections).forEach((connection) => {
            if (connection) {
              connection.close();
            }
          });

          Object.keys(this.connections).forEach((type) => {
            this.updateConnectionStatus(type, 'disconnected');
          });
        }

        reconnectAll() {
          this.disconnectAll();
          setTimeout(() => this.connectAll(), 1000);
        }

        toggleLogLevel(level) {
          this.logFilters[level] = !this.logFilters[level];
          const btn = document.getElementById(`${level}Btn`);
          btn.style.opacity = this.logFilters[level] ? '1' : '0.5';
        }

        async sendTestNotification() {
          try {
            await fetch('/sse/notify/1', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                title: 'Notificación de Prueba',
                message: 'Esta es una notificación de prueba del dashboard',
                level: 'info',
              }),
            });
          } catch (error) {
            console.error('Error enviando notificación de prueba:', error);
          }
        }
      }

      // Funciones globales para los botones
      let dashboard;

      function connectAll() {
        dashboard.connectAll();
      }
      function disconnectAll() {
        dashboard.disconnectAll();
      }
      function reconnectAll() {
        dashboard.reconnectAll();
      }
      function refreshStats() {
        dashboard.refreshStats();
      }
      function toggleLogLevel(level) {
        dashboard.toggleLogLevel(level);
      }
      function sendTestNotification() {
        dashboard.sendTestNotification();
      }

      function clearLogs() {
        document.getElementById('systemLogs').innerHTML = '';
      }

      function clearNotifications() {
        document.getElementById('notifications').innerHTML =
          '<div style="text-align: center; color: #666;">Sin notificaciones</div>';
      }

      // Inicializar dashboard cuando la página esté lista
      document.addEventListener('DOMContentLoaded', () => {
        dashboard = new SSEDashboard();
      });
    </script>
  </body>
</html>
```

## 5. Integración con Background Tasks (10 min)

### Notificaciones de Progreso de Tareas

```python
# app/integrations/task_notifications.py
from ..sse.managers import sse_manager
from ..background.celery_app import celery_app
from datetime import datetime
import asyncio

class TaskNotificationService:
    """Servicio para enviar notificaciones de progreso de tareas via SSE"""

    @staticmethod
    async def notify_task_started(task_id: str, task_type: str, user_id: int = None):
        """Notifica que una tarea ha comenzado"""
        event_data = {
            "event": "task_started",
            "data": {
                "task_id": task_id,
                "task_type": task_type,
                "status": "started",
                "message": f"Tarea {task_type} iniciada",
                "timestamp": datetime.now().isoformat()
            }
        }

        # Enviar a canal de tareas
        await sse_manager.broadcast_to_channel("tasks", event_data)

        # Enviar a usuario específico si está especificado
        if user_id:
            await sse_manager.send_to_user(user_id, event_data)

    @staticmethod
    async def notify_task_progress(
        task_id: str,
        progress: int,
        message: str,
        user_id: int = None
    ):
        """Notifica progreso de tarea"""
        event_data = {
            "event": "task_progress",
            "data": {
                "task_id": task_id,
                "progress": progress,
                "message": message,
                "timestamp": datetime.now().isoformat()
            }
        }

        await sse_manager.broadcast_to_channel("tasks", event_data)

        if user_id:
            await sse_manager.send_to_user(user_id, event_data)

    @staticmethod
    async def notify_task_completed(
        task_id: str,
        result: dict,
        user_id: int = None
    ):
        """Notifica que una tarea se ha completado"""
        event_data = {
            "event": "task_completed",
            "data": {
                "task_id": task_id,
                "status": "completed",
                "result": result,
                "message": "Tarea completada exitosamente",
                "timestamp": datetime.now().isoformat()
            }
        }

        await sse_manager.broadcast_to_channel("tasks", event_data)

        if user_id:
            await sse_manager.send_to_user(user_id, event_data)

    @staticmethod
    async def notify_task_failed(
        task_id: str,
        error: str,
        user_id: int = None
    ):
        """Notifica que una tarea ha fallado"""
        event_data = {
            "event": "task_failed",
            "data": {
                "task_id": task_id,
                "status": "failed",
                "error": error,
                "message": "Tarea falló",
                "timestamp": datetime.now().isoformat()
            }
        }

        await sse_manager.broadcast_to_channel("tasks", event_data)

        if user_id:
            await sse_manager.send_to_user(user_id, event_data)

# Instancia global del servicio
task_notification_service = TaskNotificationService()
```

## 6. Testing de SSE (5 min)

### Tests para Server-Sent Events

```python
# tests/test_sse.py
import pytest
import asyncio
from fastapi.testclient import TestClient
from app.main import app
from app.sse.managers import sse_manager

client = TestClient(app)

class TestSSE:

    def test_sse_endpoint_exists(self):
        """Test que el endpoint SSE existe"""
        # No podemos hacer una llamada completa en tests síncronos
        # pero podemos verificar que la ruta existe
        response = client.get("/sse/stats")
        assert response.status_code == 200

    def test_broadcast_message(self):
        """Test de envío de mensaje broadcast"""
        response = client.post("/sse/broadcast/test", json={
            "message": "Test message",
            "type": "info"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "sent"
        assert data["channel"] == "test"

    def test_user_notification(self):
        """Test de notificación a usuario"""
        response = client.post("/sse/notify/123", json={
            "title": "Test Notification",
            "message": "This is a test",
            "level": "info"
        })

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "sent"
        assert data["user_id"] == 123

    def test_sse_stats(self):
        """Test de estadísticas SSE"""
        response = client.get("/sse/stats")
        assert response.status_code == 200

        data = response.json()
        assert "total_connections" in data
        assert "channels" in data
        assert "users_connected" in data

    @pytest.mark.asyncio
    async def test_sse_manager_broadcast(self):
        """Test del manager SSE"""
        # Simular broadcast
        await sse_manager.broadcast_to_channel("test", {
            "event": "test",
            "data": {"message": "test"}
        })

        # Verificar estadísticas
        stats = sse_manager.get_stats()
        assert isinstance(stats["total_connections"], int)
        assert isinstance(stats["channels"], dict)
```

## Resumen y Próximos Pasos

### Lo que has aprendido:

1. ✅ **Server-Sent Events** con FastAPI
2. ✅ **Streaming de datos** en tiempo real
3. ✅ **Dashboard interactivo** con múltiples fuentes
4. ✅ **Gestión de conexiones** y canales
5. ✅ **Integración** con Background Tasks

### Tareas para consolidar:

- [ ] Implementar autenticación en streams SSE
- [ ] Añadir persistencia de eventos importantes
- [ ] Crear filtros avanzados en el dashboard
- [ ] Implementar rate limiting para eventos
- [ ] Añadir métricas de rendimiento

### Conexión con la siguiente práctica:

En la **Práctica 38** integraremos todos los conceptos (WebSockets, Background Tasks y SSE) en una aplicación completa de chat con notificaciones y dashboard en tiempo real.

---

**💡 Tip Profesional:** SSE es perfecto para dashboards y notificaciones unidireccionales. Combínalo con WebSockets para comunicación bidireccional completa.
