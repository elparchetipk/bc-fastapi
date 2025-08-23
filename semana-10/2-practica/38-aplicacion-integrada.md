# Práctica 38: Aplicación Integrada - Chat Completo

⏰ **Tiempo estimado**: 75 minutos _(optimizado)_  
🎯 **Objetivo**: Integrar WebSockets, Background Tasks y SSE en MVP funcional

---

## 📋 Qué vas a lograr

Al final de esta práctica habrás:

- ✅ Creado un chat funcional con las tres tecnologías
- ✅ Integrado notificaciones básicas con Background Tasks
- ✅ Implementado dashboard básico con SSE
- ✅ Agregado sistema de presencia simple
- ✅ Configurado logging básico y testing

**OPTIMIZADO PARA 75MIN:**

- ✅ MVP funcional con todas las tecnologías integradas
- ✅ Chat operativo con notificaciones
- ✅ Dashboard básico actualizable
- ⬇️ Simplificado: Features avanzadas, UI compleja, testing exhaustivo

---

## 🛠️ Paso 1: Arquitectura Simplificada (15 min)

### **Estructura del proyecto**

```
app/
├── chat/
│   ├── __init__.py
│   ├── models.py         # Modelos de chat
│   ├── websocket.py      # WebSocket endpoints
│   ├── notifications.py  # Background tasks
│   └── dashboard.py      # SSE endpoints
├── core/
│   ├── events.py         # Event system
│   └── presence.py       # Sistema de presencia
└── static/
    ├── chat.html         # Chat interface
    ├── dashboard.html    # Admin dashboard
    └── js/
        ├── chat.js
        └── dashboard.js
```

### **Crear modelos de chat**

```python
# app/chat/models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from typing import Optional
import uuid

class ChatRoom(Base):
    __tablename__ = "chat_rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text, nullable=True)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(Integer, ForeignKey("users.id"))

    # Relaciones
    messages = relationship("ChatMessage", back_populates="room", cascade="all, delete-orphan")
    members = relationship("RoomMember", back_populates="room", cascade="all, delete-orphan")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # text, image, file, system
    room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    edited_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)

    # Relaciones
    room = relationship("ChatRoom", back_populates="messages")
    user = relationship("User")

class RoomMember(Base):
    __tablename__ = "room_members"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("chat_rooms.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String(20), default="member")  # admin, moderator, member
    joined_at = Column(DateTime, default=datetime.utcnow)
    last_seen = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    room = relationship("ChatRoom", back_populates="members")
    user = relationship("User")

class UserPresence(Base):
    __tablename__ = "user_presence"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    status = Column(String(20), default="offline")  # online, away, busy, offline
    last_activity = Column(DateTime, default=datetime.utcnow)
    current_room = Column(Integer, ForeignKey("chat_rooms.id"), nullable=True)

    # Relaciones
    user = relationship("User")
```

### **Sistema de eventos centralizado**

```python
# app/core/events.py
from typing import Dict, List, Any, Callable
from datetime import datetime
import asyncio
import logging

logger = logging.getLogger(__name__)

class EventSystem:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = {}
        self.event_history: List[Dict] = []

    def subscribe(self, event_type: str, callback: Callable):
        """Suscribirse a un tipo de evento"""
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable):
        """Desuscribirse de un evento"""
        if event_type in self.listeners:
            self.listeners[event_type].remove(callback)

    async def emit(self, event_type: str, data: Dict[str, Any]):
        """Emitir un evento"""
        event = {
            "type": event_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat(),
            "id": f"{event_type}_{datetime.utcnow().timestamp()}"
        }

        # Guardar en historial
        self.event_history.append(event)
        if len(self.event_history) > 1000:  # Mantener últimos 1000 eventos
            self.event_history = self.event_history[-1000:]

        # Notificar listeners
        if event_type in self.listeners:
            tasks = []
            for callback in self.listeners[event_type]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        tasks.append(callback(event))
                    else:
                        callback(event)
                except Exception as e:
                    logger.error(f"Error en listener {callback}: {e}")

            if tasks:
                await asyncio.gather(*tasks, return_exceptions=True)

        logger.info(f"Event emitted: {event_type}")

    def get_recent_events(self, event_type: str = None, limit: int = 50):
        """Obtener eventos recientes"""
        events = self.event_history
        if event_type:
            events = [e for e in events if e["type"] == event_type]
        return events[-limit:]

# Instancia global
event_system = EventSystem()
```

---

## 🔄 Paso 2: WebSocket Avanzado (25 min)

### **WebSocket manager integrado**

```python
# app/chat/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from app.websocket_manager import manager
from app.core.events import event_system
from app.core.presence import presence_manager
from app.chat.models import ChatMessage, ChatRoom
from app.database import get_db
from app.auth.dependencies import get_current_user_websocket
import json
import uuid
from datetime import datetime

router = APIRouter()

@router.websocket("/ws/chat/{room_id}")
async def chat_websocket(
    websocket: WebSocket,
    room_id: int,
    token: str = None,
    db = Depends(get_db)
):
    connection_id = str(uuid.uuid4())
    user = None

    try:
        # Autenticación opcional
        if token:
            user = await get_current_user_websocket(token, db)

        # Verificar acceso a la sala
        room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
        if not room:
            await websocket.close(code=4004, reason="Room not found")
            return

        # Conectar
        await manager.connect(connection_id, websocket, user.id if user else None)
        await manager.join_room(connection_id, f"room_{room_id}")

        # Actualizar presencia
        if user:
            await presence_manager.set_user_online(user.id, room_id)

        # Notificar evento
        await event_system.emit("user_joined", {
            "user_id": user.id if user else None,
            "room_id": room_id,
            "connection_id": connection_id
        })

        # Enviar mensajes recientes
        recent_messages = db.query(ChatMessage)\
            .filter(ChatMessage.room_id == room_id)\
            .order_by(ChatMessage.created_at.desc())\
            .limit(50).all()

        for message in reversed(recent_messages):
            await manager.send_personal_message(
                json.dumps({
                    "type": "message",
                    "data": {
                        "id": message.id,
                        "content": message.content,
                        "user_id": message.user_id,
                        "username": message.user.username,
                        "created_at": message.created_at.isoformat()
                    }
                }),
                connection_id
            )

        # Loop principal
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)

            await handle_websocket_message(
                message_data, connection_id, room_id, user, db
            )

    except WebSocketDisconnect:
        manager.disconnect(connection_id, user.id if user else None)
        if user:
            await presence_manager.set_user_offline(user.id)

        await event_system.emit("user_left", {
            "user_id": user.id if user else None,
            "room_id": room_id,
            "connection_id": connection_id
        })

async def handle_websocket_message(message_data, connection_id, room_id, user, db):
    """Manejar diferentes tipos de mensajes WebSocket"""
    message_type = message_data.get("type")

    if message_type == "chat_message":
        await handle_chat_message(message_data, room_id, user, db)

    elif message_type == "typing":
        await handle_typing_indicator(message_data, connection_id, room_id, user)

    elif message_type == "ping":
        await manager.send_personal_message(
            json.dumps({"type": "pong", "timestamp": datetime.utcnow().isoformat()}),
            connection_id
        )

async def handle_chat_message(message_data, room_id, user, db):
    """Manejar mensajes de chat"""
    if not user:
        return

    content = message_data.get("content", "").strip()
    if not content:
        return

    # Guardar mensaje en DB
    message = ChatMessage(
        content=content,
        room_id=room_id,
        user_id=user.id,
        message_type="text"
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    # Broadcast a la sala
    broadcast_data = {
        "type": "message",
        "data": {
            "id": message.id,
            "content": message.content,
            "user_id": message.user_id,
            "username": user.username,
            "created_at": message.created_at.isoformat()
        }
    }

    await manager.send_to_room(
        json.dumps(broadcast_data),
        f"room_{room_id}"
    )

    # Emitir evento para notificaciones
    await event_system.emit("new_message", {
        "message_id": message.id,
        "room_id": room_id,
        "user_id": user.id,
        "content": content
    })

async def handle_typing_indicator(message_data, connection_id, room_id, user):
    """Manejar indicador de escritura"""
    if not user:
        return

    typing_data = {
        "type": "typing",
        "data": {
            "user_id": user.id,
            "username": user.username,
            "is_typing": message_data.get("is_typing", False)
        }
    }

    # Enviar a todos en la sala excepto al remitente
    connections = manager.rooms.get(f"room_{room_id}", set())
    for conn_id in connections:
        if conn_id != connection_id:
            await manager.send_personal_message(
                json.dumps(typing_data),
                conn_id
            )
```

---

## 🔔 Paso 3: Sistema de Notificaciones (25 min)

### **Background tasks para notificaciones**

```python
# app/chat/notifications.py
from fastapi import BackgroundTasks
from app.core.events import event_system
from app.chat.models import ChatMessage, RoomMember
from app.models.user import User
from app.database import SessionLocal
from app.sse_manager import sse_manager
import asyncio
import logging
import json

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.setup_event_listeners()

    def setup_event_listeners(self):
        """Configurar listeners de eventos"""
        event_system.subscribe("new_message", self.handle_new_message)
        event_system.subscribe("user_joined", self.handle_user_joined)
        event_system.subscribe("user_left", self.handle_user_left)

    async def handle_new_message(self, event):
        """Manejar nuevo mensaje para notificaciones"""
        data = event["data"]
        message_id = data["message_id"]
        room_id = data["room_id"]
        sender_id = data["user_id"]

        db = SessionLocal()
        try:
            # Obtener miembros de la sala
            members = db.query(RoomMember)\
                .filter(RoomMember.room_id == room_id)\
                .filter(RoomMember.user_id != sender_id)\
                .all()

            message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
            sender = db.query(User).filter(User.id == sender_id).first()

            # Crear notificaciones
            for member in members:
                await self.create_notification(
                    user_id=member.user_id,
                    title=f"Nuevo mensaje de {sender.username}",
                    content=message.content[:100],
                    data={
                        "type": "chat_message",
                        "room_id": room_id,
                        "message_id": message_id
                    }
                )

            # Actualizar estadísticas en dashboard
            await sse_manager.send_to_all(json.dumps({
                "type": "message_stats",
                "data": {
                    "room_id": room_id,
                    "new_message_count": 1,
                    "last_activity": event["timestamp"]
                }
            }))

        finally:
            db.close()

    async def handle_user_joined(self, event):
        """Manejar usuario que se une a sala"""
        data = event["data"]
        room_id = data["room_id"]
        user_id = data.get("user_id")

        if user_id:
            await sse_manager.send_to_all(json.dumps({
                "type": "user_presence",
                "data": {
                    "room_id": room_id,
                    "user_id": user_id,
                    "status": "joined"
                }
            }))

    async def handle_user_left(self, event):
        """Manejar usuario que deja sala"""
        data = event["data"]
        room_id = data["room_id"]
        user_id = data.get("user_id")

        if user_id:
            await sse_manager.send_to_all(json.dumps({
                "type": "user_presence",
                "data": {
                    "room_id": room_id,
                    "user_id": user_id,
                    "status": "left"
                }
            }))

    async def create_notification(self, user_id: int, title: str, content: str, data: dict = None):
        """Crear notificación para usuario"""
        notification = {
            "id": f"notif_{asyncio.get_event_loop().time()}",
            "user_id": user_id,
            "title": title,
            "content": content,
            "data": data or {},
            "created_at": event_system.event_history[-1]["timestamp"] if event_system.event_history else None,
            "read": False
        }

        # Enviar vía SSE
        await sse_manager.send_to_user(
            user_id,
            json.dumps({
                "type": "notification",
                "data": notification
            })
        )

        logger.info(f"Notification sent to user {user_id}: {title}")

# Instancia global
notification_service = NotificationService()

# Background tasks
async def process_message_notifications(message_id: int):
    """Procesar notificaciones de mensaje en background"""
    await notification_service.handle_new_message({
        "data": {"message_id": message_id}
    })

async def cleanup_old_notifications():
    """Limpiar notificaciones antiguas"""
    # Implementar limpieza de notificaciones de más de 30 días
    logger.info("Cleaning up old notifications...")
```

---

## 📊 Paso 4: Dashboard en Tiempo Real (25 min)

### **SSE endpoints para dashboard**

```python
# app/chat/dashboard.py
from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from app.sse_manager import sse_manager
from app.websocket_manager import manager
from app.core.presence import presence_manager
from app.chat.models import ChatRoom, ChatMessage
from app.database import get_db
from app.auth.dependencies import get_current_user
import asyncio
import json
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/dashboard/stream")
async def dashboard_stream(
    request: Request,
    current_user = Depends(get_current_user)
):
    """Stream SSE para dashboard administrativo"""

    async def event_generator():
        connection_id = f"dashboard_{current_user.id}"

        try:
            # Registrar conexión SSE
            await sse_manager.add_connection(connection_id, current_user.id)

            # Enviar datos iniciales
            initial_data = await get_dashboard_initial_data()
            yield f"data: {json.dumps(initial_data)}\n\n"

            # Loop de eventos
            while True:
                if await request.is_disconnected():
                    break

                # Heartbeat cada 30 segundos
                await asyncio.sleep(30)
                yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': datetime.utcnow().isoformat()})}\n\n"

        except asyncio.CancelledError:
            pass
        finally:
            await sse_manager.remove_connection(connection_id)

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

@router.get("/dashboard/stats")
async def get_dashboard_stats(
    current_user = Depends(get_current_user),
    db = Depends(get_db)
):
    """Obtener estadísticas del dashboard"""

    # Estadísticas de conexiones
    connection_stats = manager.get_stats()

    # Estadísticas de presencia
    presence_stats = await presence_manager.get_stats()

    # Estadísticas de mensajes (últimas 24h)
    yesterday = datetime.utcnow() - timedelta(days=1)
    message_count = db.query(ChatMessage)\
        .filter(ChatMessage.created_at >= yesterday)\
        .count()

    # Salas más activas
    active_rooms = db.query(ChatRoom.id, ChatRoom.name, ChatMessage.room_id)\
        .join(ChatMessage)\
        .filter(ChatMessage.created_at >= yesterday)\
        .group_by(ChatRoom.id, ChatRoom.name, ChatMessage.room_id)\
        .limit(10).all()

    return {
        "connections": connection_stats,
        "presence": presence_stats,
        "messages_24h": message_count,
        "active_rooms": [
            {"id": room.id, "name": room.name, "message_count": len(list(room))}
            for room in active_rooms
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

async def get_dashboard_initial_data():
    """Obtener datos iniciales para dashboard"""
    return {
        "type": "initial_data",
        "data": {
            "websocket_connections": len(manager.active_connections),
            "active_users": len(manager.user_connections),
            "active_rooms": len(manager.rooms),
            "server_start": datetime.utcnow().isoformat()
        }
    }

@router.post("/dashboard/broadcast")
async def broadcast_message(
    message: dict,
    current_user = Depends(get_current_user)
):
    """Enviar mensaje broadcast a todos los usuarios conectados"""

    broadcast_data = {
        "type": "admin_broadcast",
        "data": {
            "message": message.get("content", ""),
            "from": "Administrador",
            "timestamp": datetime.utcnow().isoformat()
        }
    }

    # Enviar vía WebSocket a todas las conexiones
    success_count = 0
    for connection_id in manager.active_connections:
        if await manager.send_personal_message(
            json.dumps(broadcast_data),
            connection_id
        ):
            success_count += 1

    return {
        "message": "Broadcast sent",
        "sent_to": success_count,
        "total_connections": len(manager.active_connections)
    }
```

---

## 🎨 Paso 5: Frontend Integrado (20 min)

### **Chat interface completo**

```html
<!-- app/static/chat.html -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0" />
    <title>Chat en Tiempo Real</title>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        height: 100vh;
        display: flex;
      }

      .sidebar {
        width: 250px;
        background: #2c3e50;
        color: white;
        overflow-y: auto;
      }

      .room-list {
        padding: 20px;
      }

      .room-item {
        padding: 10px;
        cursor: pointer;
        border-radius: 5px;
        margin-bottom: 5px;
        transition: background 0.3s;
      }

      .room-item:hover {
        background: #34495e;
      }
      .room-item.active {
        background: #3498db;
      }

      .chat-container {
        flex: 1;
        display: flex;
        flex-direction: column;
        background: white;
      }

      .chat-header {
        background: #34495e;
        color: white;
        padding: 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .online-users {
        display: flex;
        gap: 10px;
      }

      .user-avatar {
        width: 30px;
        height: 30px;
        background: #3498db;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        font-weight: bold;
      }

      .messages-container {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        background: #ecf0f1;
      }

      .message {
        margin-bottom: 15px;
        padding: 10px;
        border-radius: 10px;
        max-width: 70%;
        animation: fadeIn 0.3s ease-in;
      }

      .message.own {
        background: #3498db;
        color: white;
        margin-left: auto;
      }

      .message.other {
        background: white;
        border: 1px solid #bdc3c7;
      }

      .message-header {
        font-size: 12px;
        margin-bottom: 5px;
        opacity: 0.7;
      }

      .typing-indicator {
        padding: 10px;
        font-style: italic;
        color: #7f8c8d;
        font-size: 14px;
      }

      .message-input-container {
        padding: 20px;
        background: white;
        border-top: 1px solid #bdc3c7;
        display: flex;
        gap: 10px;
      }

      .message-input {
        flex: 1;
        padding: 12px;
        border: 1px solid #bdc3c7;
        border-radius: 25px;
        outline: none;
        font-size: 16px;
      }

      .send-button {
        padding: 12px 20px;
        background: #3498db;
        color: white;
        border: none;
        border-radius: 25px;
        cursor: pointer;
        font-weight: bold;
      }

      .send-button:hover {
        background: #2980b9;
      }

      .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: #2ecc71;
        color: white;
        padding: 15px;
        border-radius: 5px;
        z-index: 1000;
        animation: slideIn 0.3s ease-in;
      }

      @keyframes fadeIn {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      @keyframes slideIn {
        from {
          transform: translateX(100%);
        }
        to {
          transform: translateX(0);
        }
      }

      .connection-status {
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 12px;
        font-weight: bold;
      }

      .status-connected {
        background: #2ecc71;
        color: white;
      }
      .status-connecting {
        background: #f39c12;
        color: white;
      }
      .status-disconnected {
        background: #e74c3c;
        color: white;
      }
    </style>
  </head>
  <body>
    <div class="sidebar">
      <div class="room-list">
        <h3>Salas de Chat</h3>
        <div id="roomList"></div>
      </div>
    </div>

    <div class="chat-container">
      <div class="chat-header">
        <div>
          <h3 id="currentRoomName">Selecciona una sala</h3>
          <span
            id="connectionStatus"
            class="connection-status status-disconnected"
            >Desconectado</span
          >
        </div>
        <div
          class="online-users"
          id="onlineUsers"></div>
      </div>

      <div
        class="messages-container"
        id="messagesContainer">
        <div class="message other">
          <div class="message-header">Sistema</div>
          <div>¡Bienvenido al chat! Selecciona una sala para comenzar.</div>
        </div>
      </div>

      <div
        class="typing-indicator"
        id="typingIndicator"
        style="display: none;"></div>

      <div class="message-input-container">
        <input
          type="text"
          id="messageInput"
          class="message-input"
          placeholder="Escribe tu mensaje..."
          disabled />
        <button
          id="sendButton"
          class="send-button"
          disabled>
          Enviar
        </button>
      </div>
    </div>

    <script src="/static/js/chat.js"></script>
  </body>
</html>
```

### **JavaScript del chat**

```javascript
// app/static/js/chat.js
class ChatApp {
  constructor() {
    this.ws = null;
    this.currentRoom = null;
    this.currentUser = null;
    this.typingUsers = new Set();
    this.typingTimeout = null;

    this.initializeElements();
    this.setupEventListeners();
    this.loadRooms();
    this.setupNotifications();
  }

  initializeElements() {
    this.roomList = document.getElementById('roomList');
    this.messagesContainer = document.getElementById('messagesContainer');
    this.messageInput = document.getElementById('messageInput');
    this.sendButton = document.getElementById('sendButton');
    this.currentRoomName = document.getElementById('currentRoomName');
    this.connectionStatus = document.getElementById('connectionStatus');
    this.onlineUsers = document.getElementById('onlineUsers');
    this.typingIndicator = document.getElementById('typingIndicator');
  }

  setupEventListeners() {
    this.sendButton.addEventListener('click', () => this.sendMessage());
    this.messageInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        this.sendMessage();
      } else {
        this.handleTyping();
      }
    });

    this.messageInput.addEventListener('input', () => this.handleTyping());
  }

  async loadRooms() {
    try {
      const response = await fetch('/api/chat/rooms');
      const rooms = await response.json();

      this.roomList.innerHTML = '';
      rooms.forEach((room) => {
        const roomElement = document.createElement('div');
        roomElement.className = 'room-item';
        roomElement.textContent = room.name;
        roomElement.onclick = () => this.joinRoom(room.id, room.name);
        this.roomList.appendChild(roomElement);
      });
    } catch (error) {
      console.error('Error loading rooms:', error);
    }
  }

  joinRoom(roomId, roomName) {
    if (this.currentRoom === roomId) return;

    // Desconectar de sala actual
    if (this.ws) {
      this.ws.close();
    }

    this.currentRoom = roomId;
    this.currentRoomName.textContent = roomName;

    // Limpiar mensajes
    this.messagesContainer.innerHTML = '';

    // Habilitar input
    this.messageInput.disabled = false;
    this.sendButton.disabled = false;

    // Actualizar UI
    document.querySelectorAll('.room-item').forEach((item) => {
      item.classList.remove('active');
    });
    event.target.classList.add('active');

    // Conectar WebSocket
    this.connectWebSocket(roomId);
  }

  connectWebSocket(roomId) {
    const token = localStorage.getItem('access_token');
    const wsUrl = `ws://localhost:8000/ws/chat/${roomId}${
      token ? `?token=${token}` : ''
    }`;

    this.updateConnectionStatus('connecting');

    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      console.log('WebSocket connected');
      this.updateConnectionStatus('connected');
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleWebSocketMessage(data);
    };

    this.ws.onclose = () => {
      console.log('WebSocket disconnected');
      this.updateConnectionStatus('disconnected');

      // Reconectar después de 3 segundos
      setTimeout(() => {
        if (this.currentRoom) {
          this.connectWebSocket(this.currentRoom);
        }
      }, 3000);
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      this.updateConnectionStatus('disconnected');
    };
  }

  handleWebSocketMessage(data) {
    switch (data.type) {
      case 'message':
        this.displayMessage(data.data);
        break;

      case 'typing':
        this.handleTypingIndicator(data.data);
        break;

      case 'user_presence':
        this.updateUserPresence(data.data);
        break;

      case 'pong':
        // Heartbeat response
        break;

      default:
        console.log('Unknown message type:', data.type);
    }
  }

  displayMessage(messageData) {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${
      messageData.user_id === this.currentUser?.id ? 'own' : 'other'
    }`;

    messageElement.innerHTML = `
            <div class="message-header">
                ${messageData.username} - ${new Date(
      messageData.created_at
    ).toLocaleTimeString()}
            </div>
            <div>${this.escapeHtml(messageData.content)}</div>
        `;

    this.messagesContainer.appendChild(messageElement);
    this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
  }

  sendMessage() {
    const content = this.messageInput.value.trim();
    if (!content || !this.ws) return;

    this.ws.send(
      JSON.stringify({
        type: 'chat_message',
        content: content,
      })
    );

    this.messageInput.value = '';
    this.clearTyping();
  }

  handleTyping() {
    if (!this.ws) return;

    // Enviar indicador de escritura
    this.ws.send(
      JSON.stringify({
        type: 'typing',
        is_typing: true,
      })
    );

    // Limpiar timeout anterior
    if (this.typingTimeout) {
      clearTimeout(this.typingTimeout);
    }

    // Programar limpieza de indicador
    this.typingTimeout = setTimeout(() => {
      this.clearTyping();
    }, 3000);
  }

  clearTyping() {
    if (!this.ws) return;

    this.ws.send(
      JSON.stringify({
        type: 'typing',
        is_typing: false,
      })
    );
  }

  handleTypingIndicator(data) {
    if (data.is_typing) {
      this.typingUsers.add(data.username);
    } else {
      this.typingUsers.delete(data.username);
    }

    this.updateTypingDisplay();
  }

  updateTypingDisplay() {
    if (this.typingUsers.size === 0) {
      this.typingIndicator.style.display = 'none';
    } else {
      const users = Array.from(this.typingUsers);
      let text;

      if (users.length === 1) {
        text = `${users[0]} está escribiendo...`;
      } else if (users.length === 2) {
        text = `${users[0]} y ${users[1]} están escribiendo...`;
      } else {
        text = `${users.length} usuarios están escribiendo...`;
      }

      this.typingIndicator.textContent = text;
      this.typingIndicator.style.display = 'block';
    }
  }

  updateConnectionStatus(status) {
    this.connectionStatus.className = `connection-status status-${status}`;
    this.connectionStatus.textContent = {
      connected: 'Conectado',
      connecting: 'Conectando...',
      disconnected: 'Desconectado',
    }[status];
  }

  updateUserPresence(data) {
    // Actualizar lista de usuarios online
    // Implementar según necesidades
  }

  setupNotifications() {
    if ('Notification' in window) {
      Notification.requestPermission();
    }
  }

  showNotification(title, message) {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, {
        body: message,
        icon: '/static/icon.png',
      });
    }

    // Mostrar notificación en pantalla
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.innerHTML = `<strong>${title}</strong><br>${message}`;
    document.body.appendChild(notification);

    setTimeout(() => {
      notification.remove();
    }, 5000);
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Inicializar aplicación
document.addEventListener('DOMContentLoaded', () => {
  new ChatApp();
});
```

---

## 🧪 Paso 6: Testing Integrado (5 min)

### **Tests para aplicación completa**

```python
# tests/test_chat_integration.py
import pytest
import asyncio
import json
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket
from app.main import app
from app.database import get_db, override_get_db
from app.auth.dependencies import get_current_user

client = TestClient(app)

class TestChatIntegration:

    @pytest.mark.asyncio
    async def test_websocket_chat_flow(self):
        """Test completo de flujo de chat"""
        with client.websocket_connect("/ws/chat/1") as websocket1:
            with client.websocket_connect("/ws/chat/1") as websocket2:
                # Usuario 1 envía mensaje
                websocket1.send_text(json.dumps({
                    "type": "chat_message",
                    "content": "Hola mundo!"
                }))

                # Usuario 2 recibe mensaje
                data = websocket2.receive_text()
                message = json.loads(data)

                assert message["type"] == "message"
                assert message["data"]["content"] == "Hola mundo!"

    def test_sse_dashboard_stream(self):
        """Test de SSE para dashboard"""
        with client.stream("GET", "/dashboard/stream") as response:
            assert response.status_code == 200
            assert response.headers["content-type"] == "text/event-stream; charset=utf-8"

    def test_notification_creation(self):
        """Test de sistema de notificaciones"""
        # Implementar test de notificaciones
        pass

    def test_presence_system(self):
        """Test de sistema de presencia"""
        # Implementar test de presencia
        pass

if __name__ == "__main__":
    pytest.main([__file__])
```

---

## 🎯 Resultados Esperados

Al completar esta práctica habrás creado:

✅ **Chat completo** con múltiples salas y usuarios  
✅ **Sistema de notificaciones** con Background Tasks  
✅ **Dashboard en tiempo real** con SSE  
✅ **Sistema de presencia** de usuarios  
✅ **Frontend moderno** e interactivo  
✅ **Testing integrado** para toda la aplicación

### **Próximos pasos**

- Optimizar rendimiento con caching
- Agregar moderación de contenido
- Implementar archivo de medios
- Integrar con sistema de usuarios avanzado

---

**🚀 ¡Excelente trabajo!** Has construido una aplicación de chat completa que integra todas las tecnologías avanzadas de API. Esta base te permitirá crear aplicaciones en tiempo real de nivel profesional.

---

_Práctica 38 - Semana 10 - Bootcamp FastAPI_  
_Tiempo total: ~120 minutos_
