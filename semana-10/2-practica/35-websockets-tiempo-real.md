# Práctica 35: WebSockets y Comunicación en Tiempo Real

⏰ **Tiempo estimado**: 75 minutos _(optimizado)_  
🎯 **Objetivo**: Implementar WebSockets básicos para comunicación bidireccional en tiempo real

---

## 📋 Qué vas a lograr

Al final de esta práctica habrás:

- ✅ Configurado WebSockets básicos en FastAPI
- ✅ Implementado un chat funcional en tiempo real
- ✅ Gestionado conexiones y desconexiones básicas
- ✅ Integrado autenticación con WebSockets
- ✅ Creado un sistema de salas básico

**OPTIMIZADO PARA 75MIN:**

- ✅ Enfoque en implementación funcional vs configuraciones complejas
- ✅ Chat operativo con features esenciales
- ⬇️ Simplificado: Error handling avanzado, optimizaciones complejas

---

## 🛠️ Paso 1: Setup y Dependencias (10 min)

### **Instalar dependencias adicionales**

```bash
# 1. Instalar WebSocket dependencies
pip install python-socketio
pip install websockets

# 2. Verificar que tienes Redis corriendo (de semana anterior)
redis-cli ping
# Debe responder: PONG

# 3. Si no tienes Redis:
# Ubuntu/Debian:
sudo apt install redis-server
sudo systemctl start redis-server

# macOS:
brew install redis
brew services start redis

# Windows:
# Descargar desde: https://github.com/microsoftarchive/redis/releases
```

### **Actualizar requirements.txt**

```bash
# Agregar a requirements.txt
echo "websockets==12.0" >> requirements.txt
echo "python-socketio==5.10.0" >> requirements.txt
echo "redis==5.0.1" >> requirements.txt
```

---

## 🔌 Paso 2: WebSocket Básico (20 min)

### **Crear archivo websocket_manager.py**

```python
# app/websocket_manager.py
from typing import Dict, Set
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        # Almacenar conexiones activas
        self.active_connections: Dict[str, WebSocket] = {}
        # Mapear usuarios a sus conexiones
        self.user_connections: Dict[str, Set[str]] = {}
        # Salas de chat
        self.rooms: Dict[str, Set[str]] = {}

    async def connect(self, connection_id: str, websocket: WebSocket, user_id: str = None):
        """Conectar un nuevo WebSocket"""
        await websocket.accept()
        self.active_connections[connection_id] = websocket

        if user_id:
            if user_id not in self.user_connections:
                self.user_connections[user_id] = set()
            self.user_connections[user_id].add(connection_id)

        logger.info(f"WebSocket connected: {connection_id} (user: {user_id})")
        return connection_id

    def disconnect(self, connection_id: str, user_id: str = None):
        """Desconectar WebSocket"""
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]

        if user_id and user_id in self.user_connections:
            self.user_connections[user_id].discard(connection_id)
            if not self.user_connections[user_id]:
                del self.user_connections[user_id]

        # Remover de todas las salas
        for room_connections in self.rooms.values():
            room_connections.discard(connection_id)

        logger.info(f"WebSocket disconnected: {connection_id}")

    async def send_personal_message(self, message: str, connection_id: str):
        """Enviar mensaje a una conexión específica"""
        websocket = self.active_connections.get(connection_id)
        if websocket:
            try:
                await websocket.send_text(message)
                return True
            except Exception as e:
                logger.error(f"Error sending message to {connection_id}: {e}")
                self.disconnect(connection_id)
                return False
        return False

    async def send_to_user(self, message: str, user_id: str):
        """Enviar mensaje a todas las conexiones de un usuario"""
        connections = self.user_connections.get(user_id, set())
        success_count = 0

        for connection_id in connections.copy():
            if await self.send_personal_message(message, connection_id):
                success_count += 1

        return success_count

    async def broadcast(self, message: str):
        """Enviar mensaje a todas las conexiones activas"""
        success_count = 0
        for connection_id in list(self.active_connections.keys()):
            if await self.send_personal_message(message, connection_id):
                success_count += 1
        return success_count

    async def join_room(self, connection_id: str, room: str):
        """Unir conexión a una sala"""
        if room not in self.rooms:
            self.rooms[room] = set()
        self.rooms[room].add(connection_id)
        logger.info(f"Connection {connection_id} joined room {room}")

    async def leave_room(self, connection_id: str, room: str):
        """Salir de una sala"""
        if room in self.rooms:
            self.rooms[room].discard(connection_id)
            if not self.rooms[room]:
                del self.rooms[room]
        logger.info(f"Connection {connection_id} left room {room}")

    async def send_to_room(self, message: str, room: str):
        """Enviar mensaje a todos en una sala"""
        if room not in self.rooms:
            return 0

        success_count = 0
        for connection_id in list(self.rooms[room]):
            if await self.send_personal_message(message, connection_id):
                success_count += 1

        return success_count

    def get_stats(self):
        """Obtener estadísticas de conexiones"""
        return {
            "total_connections": len(self.active_connections),
            "unique_users": len(self.user_connections),
            "active_rooms": len(self.rooms),
            "rooms": {room: len(connections) for room, connections in self.rooms.items()}
        }

# Instancia global del manager
manager = ConnectionManager()
```

### **Crear endpoint WebSocket básico**

```python
# app/routers/websocket.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from app.websocket_manager import manager
import uuid
import json
from datetime import datetime

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Generar ID único para la conexión
    connection_id = str(uuid.uuid4())

    try:
        # Conectar
        await manager.connect(connection_id, websocket)

        # Enviar mensaje de bienvenida
        welcome_message = {
            "type": "system",
            "message": "Conectado al chat",
            "connection_id": connection_id,
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send_text(json.dumps(welcome_message))

        # Notificar a otros usuarios
        notification = {
            "type": "user_joined",
            "message": f"Usuario {connection_id[:8]} se conectó",
            "timestamp": datetime.now().isoformat()
        }
        await manager.broadcast(json.dumps(notification))

        # Loop principal para recibir mensajes
        while True:
            data = await websocket.receive_text()

            try:
                message_data = json.loads(data)

                # Procesar mensaje
                response = {
                    "type": "message",
                    "sender": connection_id[:8],
                    "message": message_data.get("message", ""),
                    "timestamp": datetime.now().isoformat()
                }

                # Broadcast a todos
                await manager.broadcast(json.dumps(response))

            except json.JSONDecodeError:
                error_message = {
                    "type": "error",
                    "message": "Formato de mensaje inválido",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send_text(json.dumps(error_message))

    except WebSocketDisconnect:
        # Usuario desconectado
        manager.disconnect(connection_id)

        # Notificar desconexión
        notification = {
            "type": "user_left",
            "message": f"Usuario {connection_id[:8]} se desconectó",
            "timestamp": datetime.now().isoformat()
        }
        await manager.broadcast(json.dumps(notification))
```

### **Integrar en main.py**

```python
# app/main.py
from fastapi import FastAPI
from app.routers import websocket

app = FastAPI(title="API Avanzada - WebSockets")

# Incluir router de WebSocket
app.include_router(websocket.router, prefix="/api/v1", tags=["websockets"])

# Endpoint de health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "websocket-api"}

# Endpoint para estadísticas
@app.get("/api/v1/websocket/stats")
async def get_websocket_stats():
    return manager.get_stats()
```

---

## 🎨 Paso 3: Cliente HTML de Prueba (15 min)

### **Crear archivo de prueba**

```html
<!-- static/websocket_test.html -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0" />
    <title>WebSocket Chat Test</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
      }

      #messages {
        border: 1px solid #ddd;
        height: 400px;
        overflow-y: auto;
        padding: 10px;
        margin-bottom: 10px;
        background-color: #f9f9f9;
      }

      .message {
        margin-bottom: 5px;
        padding: 5px;
        border-radius: 3px;
      }

      .system {
        background-color: #e3f2fd;
        color: #1976d2;
      }

      .user_joined,
      .user_left {
        background-color: #fff3e0;
        color: #f57c00;
      }

      .message-type {
        background-color: #e8f5e8;
        color: #388e3c;
      }

      .error {
        background-color: #ffebee;
        color: #d32f2f;
      }

      #messageInput {
        width: 70%;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
      }

      #sendButton {
        width: 25%;
        padding: 10px;
        background-color: #1976d2;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }

      #sendButton:hover {
        background-color: #1565c0;
      }

      #sendButton:disabled {
        background-color: #ccc;
        cursor: not-allowed;
      }

      #status {
        margin-bottom: 10px;
        padding: 10px;
        border-radius: 4px;
        font-weight: bold;
      }

      .connected {
        background-color: #e8f5e8;
        color: #388e3c;
      }

      .disconnected {
        background-color: #ffebee;
        color: #d32f2f;
      }
    </style>
  </head>
  <body>
    <h1>WebSocket Chat Test</h1>

    <div
      id="status"
      class="disconnected">
      Desconectado
    </div>

    <div id="messages"></div>

    <div>
      <input
        type="text"
        id="messageInput"
        placeholder="Escribe tu mensaje..."
        disabled />
      <button
        id="sendButton"
        disabled>
        Enviar
      </button>
    </div>

    <div style="margin-top: 20px;">
      <button id="connectButton">Conectar</button>
      <button
        id="disconnectButton"
        disabled>
        Desconectar
      </button>
      <button id="clearButton">Limpiar Chat</button>
    </div>

    <script>
      let socket = null;
      let isConnected = false;

      const messagesDiv = document.getElementById('messages');
      const messageInput = document.getElementById('messageInput');
      const sendButton = document.getElementById('sendButton');
      const connectButton = document.getElementById('connectButton');
      const disconnectButton = document.getElementById('disconnectButton');
      const clearButton = document.getElementById('clearButton');
      const statusDiv = document.getElementById('status');

      function updateStatus(connected) {
        isConnected = connected;
        if (connected) {
          statusDiv.textContent = 'Conectado';
          statusDiv.className = 'connected';
          messageInput.disabled = false;
          sendButton.disabled = false;
          connectButton.disabled = true;
          disconnectButton.disabled = false;
        } else {
          statusDiv.textContent = 'Desconectado';
          statusDiv.className = 'disconnected';
          messageInput.disabled = true;
          sendButton.disabled = true;
          connectButton.disabled = false;
          disconnectButton.disabled = true;
        }
      }

      function addMessage(data) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${data.type}`;

        const timestamp = new Date(data.timestamp).toLocaleTimeString();

        if (data.type === 'message') {
          messageElement.innerHTML = `<strong>[${timestamp}] ${data.sender}:</strong> ${data.message}`;
        } else {
          messageElement.innerHTML = `<strong>[${timestamp}]</strong> ${data.message}`;
        }

        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
      }

      function connect() {
        if (socket) return;

        // Conectar al WebSocket
        socket = new WebSocket('ws://localhost:8000/api/v1/ws');

        socket.onopen = function (event) {
          console.log('WebSocket conectado');
          updateStatus(true);
        };

        socket.onmessage = function (event) {
          const data = JSON.parse(event.data);
          addMessage(data);
        };

        socket.onclose = function (event) {
          console.log('WebSocket desconectado');
          updateStatus(false);
          socket = null;
        };

        socket.onerror = function (error) {
          console.error('Error WebSocket:', error);
          addMessage({
            type: 'error',
            message: 'Error de conexión',
            timestamp: new Date().toISOString(),
          });
        };
      }

      function disconnect() {
        if (socket) {
          socket.close();
          socket = null;
        }
      }

      function sendMessage() {
        const message = messageInput.value.trim();
        if (message && socket && isConnected) {
          socket.send(
            JSON.stringify({
              message: message,
            })
          );
          messageInput.value = '';
        }
      }

      // Event listeners
      connectButton.addEventListener('click', connect);
      disconnectButton.addEventListener('click', disconnect);
      clearButton.addEventListener('click', () => {
        messagesDiv.innerHTML = '';
      });

      sendButton.addEventListener('click', sendMessage);

      messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') {
          sendMessage();
        }
      });

      // Auto-conectar al cargar la página
      connect();
    </script>
  </body>
</html>
```

### **Servir archivos estáticos**

```python
# app/main.py (actualizar)
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import websocket

app = FastAPI(title="API Avanzada - WebSockets")

# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# ...resto del código anterior
```

---

## 🔐 Paso 4: Integración con Autenticación (25 min)

### **Actualizar WebSocket con autenticación**

```python
# app/routers/websocket.py (actualizar)
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query
from app.websocket_manager import manager
from app.auth import verify_token  # Importar de tu sistema de auth existente
import uuid
import json
from datetime import datetime

router = APIRouter()

async def authenticate_websocket(token: str = Query(...)):
    """Autenticar conexión WebSocket usando token JWT"""
    try:
        # Verificar token (usando función de semana 7)
        payload = verify_token(token)
        user_id = payload.get("sub")
        username = payload.get("username", f"user_{user_id}")
        return {"user_id": user_id, "username": username}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Token inválido")

@router.websocket("/ws/authenticated")
async def websocket_authenticated(websocket: WebSocket, token: str = Query(...)):
    connection_id = str(uuid.uuid4())

    try:
        # Autenticar antes de aceptar conexión
        try:
            user_data = await authenticate_websocket(token)
            user_id = user_data["user_id"]
            username = user_data["username"]
        except HTTPException:
            await websocket.close(code=1008, reason="Unauthorized")
            return

        # Conectar con información de usuario
        await manager.connect(connection_id, websocket, user_id)

        # Mensaje de bienvenida personalizado
        welcome_message = {
            "type": "system",
            "message": f"Bienvenido {username}",
            "user_id": user_id,
            "connection_id": connection_id,
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send_text(json.dumps(welcome_message))

        # Notificar a otros usuarios
        notification = {
            "type": "user_joined",
            "message": f"{username} se unió al chat",
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        await manager.broadcast(json.dumps(notification))

        # Loop principal
        while True:
            data = await websocket.receive_text()

            try:
                message_data = json.loads(data)
                message_type = message_data.get("type", "message")

                if message_type == "message":
                    # Mensaje de chat normal
                    response = {
                        "type": "message",
                        "sender": username,
                        "user_id": user_id,
                        "message": message_data.get("message", ""),
                        "timestamp": datetime.now().isoformat()
                    }
                    await manager.broadcast(json.dumps(response))

                elif message_type == "join_room":
                    # Unirse a una sala
                    room = message_data.get("room", "general")
                    await manager.join_room(connection_id, room)

                    response = {
                        "type": "room_joined",
                        "message": f"{username} se unió a la sala {room}",
                        "room": room,
                        "timestamp": datetime.now().isoformat()
                    }
                    await manager.send_to_room(json.dumps(response), room)

                elif message_type == "leave_room":
                    # Salir de una sala
                    room = message_data.get("room", "general")
                    await manager.leave_room(connection_id, room)

                    response = {
                        "type": "room_left",
                        "message": f"{username} salió de la sala {room}",
                        "room": room,
                        "timestamp": datetime.now().isoformat()
                    }
                    await manager.send_to_room(json.dumps(response), room)

                elif message_type == "private_message":
                    # Mensaje privado
                    target_user = message_data.get("target_user")
                    if target_user:
                        private_msg = {
                            "type": "private_message",
                            "sender": username,
                            "message": message_data.get("message", ""),
                            "timestamp": datetime.now().isoformat()
                        }
                        sent = await manager.send_to_user(json.dumps(private_msg), target_user)

                        # Confirmación al remitente
                        confirmation = {
                            "type": "private_sent",
                            "message": f"Mensaje privado enviado a {target_user}" if sent else f"Usuario {target_user} no está conectado",
                            "timestamp": datetime.now().isoformat()
                        }
                        await websocket.send_text(json.dumps(confirmation))

            except json.JSONDecodeError:
                error_message = {
                    "type": "error",
                    "message": "Formato de mensaje inválido",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send_text(json.dumps(error_message))

    except WebSocketDisconnect:
        # Usuario desconectado
        manager.disconnect(connection_id, user_id)

        # Notificar desconexión
        notification = {
            "type": "user_left",
            "message": f"{username} se desconectó",
            "timestamp": datetime.now().isoformat()
        }
        await manager.broadcast(json.dumps(notification))

# Endpoint para obtener token de prueba (solo para desarrollo)
@router.post("/api/v1/websocket/test-token")
async def get_test_token(username: str):
    """Generar token de prueba para WebSocket (solo desarrollo)"""
    from app.auth import create_access_token

    # Crear token con datos de prueba
    token_data = {"sub": username, "username": username}
    token = create_access_token(data=token_data)

    return {
        "access_token": token,
        "token_type": "bearer",
        "websocket_url": f"ws://localhost:8000/api/v1/ws/authenticated?token={token}"
    }
```

---

## 🏠 Paso 5: Sistema de Salas (15 min)

### **Crear endpoints para gestión de salas**

```python
# app/routers/websocket.py (agregar)
from typing import List

@router.get("/api/v1/websocket/rooms")
async def get_rooms():
    """Obtener lista de salas activas"""
    stats = manager.get_stats()
    return {
        "rooms": stats["rooms"],
        "total_rooms": stats["active_rooms"]
    }

@router.get("/api/v1/websocket/users")
async def get_connected_users():
    """Obtener usuarios conectados"""
    return {
        "connected_users": list(manager.user_connections.keys()),
        "total_users": len(manager.user_connections)
    }

@router.post("/api/v1/websocket/broadcast")
async def broadcast_message(message: str, room: str = None):
    """Enviar mensaje broadcast (admin only)"""
    broadcast_data = {
        "type": "admin_broadcast",
        "message": message,
        "timestamp": datetime.now().isoformat()
    }

    if room:
        sent = await manager.send_to_room(json.dumps(broadcast_data), room)
        return {"message": f"Mensaje enviado a sala {room}", "recipients": sent}
    else:
        sent = await manager.broadcast(json.dumps(broadcast_data))
        return {"message": "Mensaje enviado a todos", "recipients": sent}
```

### **Cliente HTML mejorado con salas**

```html
<!-- static/websocket_rooms.html -->
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0" />
    <title>WebSocket Chat con Salas</title>
    <style>
      /* Estilos anteriores + nuevos */
      .room-controls {
        margin-bottom: 10px;
        padding: 10px;
        border: 1px solid #ddd;
        border-radius: 4px;
        background-color: #f5f5f5;
      }

      .room-controls input,
      .room-controls button {
        margin: 2px;
        padding: 5px;
      }

      .current-room {
        font-weight: bold;
        color: #1976d2;
      }
    </style>
  </head>
  <body>
    <h1>WebSocket Chat con Salas</h1>

    <div
      id="status"
      class="disconnected">
      Desconectado
    </div>

    <!-- Controles de autenticación -->
    <div class="room-controls">
      <input
        type="text"
        id="usernameInput"
        placeholder="Nombre de usuario" />
      <button id="loginButton">Obtener Token</button>
      <span id="currentUser"></span>
    </div>

    <!-- Controles de salas -->
    <div class="room-controls">
      <span
        >Sala actual:
        <span
          id="currentRoom"
          class="current-room"
          >ninguna</span
        ></span
      >
      <input
        type="text"
        id="roomInput"
        placeholder="Nombre de sala" />
      <button id="joinRoomButton">Unirse a Sala</button>
      <button id="leaveRoomButton">Salir de Sala</button>
    </div>

    <!-- Mensajes privados -->
    <div class="room-controls">
      <input
        type="text"
        id="privateUserInput"
        placeholder="Usuario destinatario" />
      <input
        type="text"
        id="privateMessageInput"
        placeholder="Mensaje privado" />
      <button id="sendPrivateButton">Enviar Privado</button>
    </div>

    <div id="messages"></div>

    <div>
      <input
        type="text"
        id="messageInput"
        placeholder="Escribe tu mensaje..."
        disabled />
      <button
        id="sendButton"
        disabled>
        Enviar
      </button>
    </div>

    <div style="margin-top: 20px;">
      <button
        id="connectButton"
        disabled>
        Conectar
      </button>
      <button
        id="disconnectButton"
        disabled>
        Desconectar
      </button>
      <button id="clearButton">Limpiar Chat</button>
    </div>

    <script>
      let socket = null;
      let isConnected = false;
      let currentRoom = null;
      let currentToken = null;
      let currentUser = null;

      const messagesDiv = document.getElementById('messages');
      const messageInput = document.getElementById('messageInput');
      const sendButton = document.getElementById('sendButton');
      const connectButton = document.getElementById('connectButton');
      const disconnectButton = document.getElementById('disconnectButton');
      const statusDiv = document.getElementById('status');

      // Nuevos elementos
      const usernameInput = document.getElementById('usernameInput');
      const loginButton = document.getElementById('loginButton');
      const currentUserSpan = document.getElementById('currentUser');
      const roomInput = document.getElementById('roomInput');
      const joinRoomButton = document.getElementById('joinRoomButton');
      const leaveRoomButton = document.getElementById('leaveRoomButton');
      const currentRoomSpan = document.getElementById('currentRoom');
      const privateUserInput = document.getElementById('privateUserInput');
      const privateMessageInput = document.getElementById(
        'privateMessageInput'
      );
      const sendPrivateButton = document.getElementById('sendPrivateButton');

      // Función para obtener token
      async function getToken() {
        const username = usernameInput.value.trim();
        if (!username) {
          alert('Por favor ingresa un nombre de usuario');
          return;
        }

        try {
          const response = await fetch('/api/v1/websocket/test-token', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username }),
          });

          const data = await response.json();
          currentToken = data.access_token;
          currentUser = username;
          currentUserSpan.textContent = `Conectado como: ${username}`;
          connectButton.disabled = false;

          console.log('Token obtenido:', data.websocket_url);
        } catch (error) {
          console.error('Error obteniendo token:', error);
          alert('Error obteniendo token');
        }
      }

      function connect() {
        if (socket || !currentToken) return;

        const wsUrl = `ws://localhost:8000/api/v1/ws/authenticated?token=${currentToken}`;
        socket = new WebSocket(wsUrl);

        socket.onopen = function (event) {
          console.log('WebSocket autenticado conectado');
          updateStatus(true);
        };

        socket.onmessage = function (event) {
          const data = JSON.parse(event.data);
          addMessage(data);
        };

        socket.onclose = function (event) {
          console.log('WebSocket desconectado');
          updateStatus(false);
          socket = null;
        };

        socket.onerror = function (error) {
          console.error('Error WebSocket:', error);
        };
      }

      function joinRoom() {
        const room = roomInput.value.trim();
        if (room && socket && isConnected) {
          socket.send(
            JSON.stringify({
              type: 'join_room',
              room: room,
            })
          );
          currentRoom = room;
          currentRoomSpan.textContent = room;
          roomInput.value = '';
        }
      }

      function leaveRoom() {
        if (currentRoom && socket && isConnected) {
          socket.send(
            JSON.stringify({
              type: 'leave_room',
              room: currentRoom,
            })
          );
          currentRoom = null;
          currentRoomSpan.textContent = 'ninguna';
        }
      }

      function sendPrivateMessage() {
        const targetUser = privateUserInput.value.trim();
        const message = privateMessageInput.value.trim();

        if (targetUser && message && socket && isConnected) {
          socket.send(
            JSON.stringify({
              type: 'private_message',
              target_user: targetUser,
              message: message,
            })
          );
          privateMessageInput.value = '';
        }
      }

      // Event listeners
      loginButton.addEventListener('click', getToken);
      connectButton.addEventListener('click', connect);
      joinRoomButton.addEventListener('click', joinRoom);
      leaveRoomButton.addEventListener('click', leaveRoom);
      sendPrivateButton.addEventListener('click', sendPrivateMessage);

      // ...resto de event listeners anteriores

      // Enter key handlers
      roomInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') joinRoom();
      });

      privateMessageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') sendPrivateMessage();
      });
    </script>
  </body>
</html>
```

---

## 🧪 Paso 6: Testing y Validación (10 min)

### **Probar la implementación**

```bash
# 1. Ejecutar el servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 2. Abrir en navegador múltiples pestañas:
# http://localhost:8000/static/websocket_rooms.html

# 3. Probar funcionalidades:
# - Crear usuarios diferentes
# - Unirse a salas
# - Enviar mensajes públicos y privados
# - Verificar notificaciones de conexión/desconexión
```

### **Script de testing automatizado**

```python
# test_websockets.py
import asyncio
import websockets
import json

async def test_websocket_connection():
    uri = "ws://localhost:8000/api/v1/ws"

    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Conexión WebSocket establecida")

            # Enviar mensaje de prueba
            test_message = {
                "message": "Mensaje de prueba automatizado"
            }
            await websocket.send(json.dumps(test_message))
            print("✅ Mensaje enviado")

            # Recibir respuesta
            response = await websocket.recv()
            data = json.loads(response)
            print(f"✅ Respuesta recibida: {data}")

    except Exception as e:
        print(f"❌ Error en testing: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket_connection())
```

---

## 📊 Conclusión y Próximos Pasos

### **¿Qué hemos logrado?**

- ✅ **WebSocket Manager** completo con gestión de conexiones
- ✅ **Autenticación** integrada con sistema existente
- ✅ **Sistema de salas** para chat organizado
- ✅ **Mensajes privados** entre usuarios
- ✅ **Cliente HTML** funcional para pruebas
- ✅ **API REST** complementaria para estadísticas

### **Conceptos clave aprendidos**

1. **Gestión de conexiones** WebSocket persistentes
2. **Autenticación** en tiempo real con JWT
3. **Broadcasting** y targeting de mensajes
4. **Manejo de errores** y desconexiones
5. **Integración** con sistemas de autenticación existentes

### **En la siguiente práctica**

Implementaremos **Background Tasks** para:

- Procesamiento de notificaciones
- Envío de emails asíncronos
- Tareas programadas
- Integración con Redis para queues

---

**🎯 ¡Felicitaciones!** Has implementado WebSockets profesionales. En la siguiente práctica añadiremos procesamiento en background para completar el stack de API avanzada.

---

_Práctica 35 - Semana 10 - Bootcamp FastAPI_  
_Tiempo total: ~90 minutos_
