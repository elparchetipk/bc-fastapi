# WebSockets Cheat Sheet - Referencia Rápida

🚀 **Guía de referencia rápida para WebSockets en FastAPI**

---

## ⚡ Quick Start

### **Instalación**

```bash
pip install fastapi uvicorn websockets
```

### **Server Básico**

```python
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except:
        pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### **Cliente HTML**

```html
<!DOCTYPE html>
<html>
  <head>
    <title>WebSocket Test</title>
  </head>
  <body>
    <input
      type="text"
      id="messageText"
      placeholder="Enter message" />
    <button onclick="sendMessage()">Send</button>
    <div id="messages"></div>

    <script>
      const ws = new WebSocket('ws://localhost:8000/ws');

      ws.onmessage = function (event) {
        const messages = document.getElementById('messages');
        messages.innerHTML += '<div>' + event.data + '</div>';
      };

      function sendMessage() {
        const input = document.getElementById('messageText');
        ws.send(input.value);
        input.value = '';
      }
    </script>
  </body>
</html>
```

---

## 🔧 Connection Manager Pattern

### **Basic Manager**

```python
from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client {client_id}: {data}")
    except:
        manager.disconnect(websocket)
```

### **Advanced Manager con Rooms**

```python
from typing import Dict, Set
import json

class RoomManager:
    def __init__(self):
        self.connections: Dict[str, Set[WebSocket]] = {}
        self.user_rooms: Dict[WebSocket, Set[str]] = {}

    async def join_room(self, websocket: WebSocket, room: str):
        if room not in self.connections:
            self.connections[room] = set()

        self.connections[room].add(websocket)

        if websocket not in self.user_rooms:
            self.user_rooms[websocket] = set()
        self.user_rooms[websocket].add(room)

    async def leave_room(self, websocket: WebSocket, room: str):
        if room in self.connections:
            self.connections[room].discard(websocket)

        if websocket in self.user_rooms:
            self.user_rooms[websocket].discard(room)

    async def send_to_room(self, room: str, message: dict):
        if room in self.connections:
            message_str = json.dumps(message)
            for websocket in self.connections[room]:
                try:
                    await websocket.send_text(message_str)
                except:
                    # Connection closed
                    self.connections[room].discard(websocket)
```

---

## 🔐 Autenticación

### **JWT en WebSockets**

```python
from fastapi import WebSocket, HTTPException, Depends, Query
from jose import jwt, JWTError

async def get_current_user_websocket(
    websocket: WebSocket,
    token: str = Query(...)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            await websocket.close(code=4001)
            return None
        return await get_user(user_id)
    except JWTError:
        await websocket.close(code=4001)
        return None

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    current_user = Depends(get_current_user_websocket)
):
    if not current_user:
        return

    await websocket.accept()
    # ... rest of logic
```

### **Session-based Auth**

```python
from fastapi import Cookie

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    session_token: str = Cookie(None)
):
    user = await validate_session(session_token)
    if not user:
        await websocket.close(code=4003)
        return

    await websocket.accept()
    # ... authenticated logic
```

---

## 📨 Message Types

### **Structured Messages**

```python
from pydantic import BaseModel
from enum import Enum

class MessageType(str, Enum):
    CHAT = "chat"
    JOIN = "join"
    LEAVE = "leave"
    TYPING = "typing"
    ERROR = "error"

class WebSocketMessage(BaseModel):
    type: MessageType
    data: dict
    timestamp: str = None

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            raw_data = await websocket.receive_text()
            message = WebSocketMessage.parse_raw(raw_data)

            if message.type == MessageType.CHAT:
                await handle_chat_message(websocket, message.data)
            elif message.type == MessageType.JOIN:
                await handle_join(websocket, message.data)
            # ... handle other types

    except Exception as e:
        error_msg = WebSocketMessage(
            type=MessageType.ERROR,
            data={"error": str(e)}
        )
        await websocket.send_text(error_msg.json())
```

### **Binary Messages**

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            # Can receive text or bytes
            try:
                data = await websocket.receive_text()
                await handle_text_message(data)
            except:
                data = await websocket.receive_bytes()
                await handle_binary_message(data)
    except:
        pass
```

---

## 🔄 Error Handling

### **Connection Errors**

```python
from fastapi import WebSocketDisconnect
import logging

logger = logging.getLogger(__name__)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    try:
        await manager.connect(websocket)

        while True:
            try:
                data = await websocket.receive_text()
                await process_message(data)
            except WebSocketDisconnect:
                logger.info(f"Client {client_id} disconnected")
                break
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Failed to process message"
                }))

    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
    finally:
        manager.disconnect(websocket)
```

### **Graceful Shutdown**

```python
import signal
import asyncio

class GracefulShutdown:
    def __init__(self, manager: ConnectionManager):
        self.manager = manager
        self.shutdown = False

    async def shutdown_handler(self):
        self.shutdown = True

        # Notify all clients
        for connection in self.manager.active_connections:
            try:
                await connection.send_text(json.dumps({
                    "type": "server_shutdown",
                    "message": "Server is shutting down"
                }))
                await connection.close()
            except:
                pass

    def setup_signal_handlers(self):
        signal.signal(signal.SIGTERM, lambda s, f: asyncio.create_task(self.shutdown_handler()))
        signal.signal(signal.SIGINT, lambda s, f: asyncio.create_task(self.shutdown_handler()))
```

---

## 📊 Monitoring

### **Connection Metrics**

```python
from datetime import datetime
import time

class ConnectionMetrics:
    def __init__(self):
        self.connections_count = 0
        self.total_messages = 0
        self.start_time = time.time()
        self.connection_history = []

    def on_connect(self, websocket: WebSocket):
        self.connections_count += 1
        self.connection_history.append({
            "event": "connect",
            "timestamp": datetime.utcnow().isoformat(),
            "total_connections": self.connections_count
        })

    def on_disconnect(self, websocket: WebSocket):
        self.connections_count -= 1
        self.connection_history.append({
            "event": "disconnect",
            "timestamp": datetime.utcnow().isoformat(),
            "total_connections": self.connections_count
        })

    def on_message(self):
        self.total_messages += 1

    def get_stats(self):
        uptime = time.time() - self.start_time
        return {
            "active_connections": self.connections_count,
            "total_messages": self.total_messages,
            "uptime_seconds": uptime,
            "messages_per_second": self.total_messages / uptime if uptime > 0 else 0
        }

metrics = ConnectionMetrics()

@app.get("/stats")
async def get_websocket_stats():
    return metrics.get_stats()
```

### **Health Check**

```python
@app.get("/health/websocket")
async def websocket_health():
    return {
        "status": "healthy",
        "active_connections": len(manager.active_connections),
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

## 🧪 Testing

### **Basic WebSocket Test**

```python
import pytest
from fastapi.testclient import TestClient

def test_websocket():
    client = TestClient(app)
    with client.websocket_connect("/ws") as websocket:
        websocket.send_text("Hello")
        data = websocket.receive_text()
        assert "Hello" in data
```

### **Multiple Connections Test**

```python
def test_multiple_connections():
    client = TestClient(app)

    with client.websocket_connect("/ws") as ws1:
        with client.websocket_connect("/ws") as ws2:
            # Test broadcasting
            ws1.send_text("Hello from client 1")

            # Both should receive the message
            data1 = ws1.receive_text()
            data2 = ws2.receive_text()

            assert "client 1" in data2
```

### **Async Testing**

```python
import pytest
import asyncio
from fastapi.testclient import TestClient

@pytest.mark.asyncio
async def test_websocket_async():
    # For more complex async testing
    pass
```

---

## 🎯 Common Patterns

### **Heartbeat/Ping-Pong**

```python
import asyncio

async def heartbeat(websocket: WebSocket):
    while True:
        try:
            await asyncio.sleep(30)  # Ping every 30 seconds
            await websocket.ping()
        except:
            break

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    # Start heartbeat
    heartbeat_task = asyncio.create_task(heartbeat(websocket))

    try:
        while True:
            data = await websocket.receive_text()
            # Process data
    except:
        heartbeat_task.cancel()
```

### **Rate Limiting**

```python
import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, max_requests=10, window=60):
        self.max_requests = max_requests
        self.window = window
        self.clients = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        # Clean old requests
        self.clients[client_id] = [
            req_time for req_time in self.clients[client_id]
            if now - req_time < self.window
        ]

        if len(self.clients[client_id]) >= self.max_requests:
            return False

        self.clients[client_id].append(now)
        return True

rate_limiter = RateLimiter()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()

            if not rate_limiter.is_allowed(client_id):
                await websocket.send_text(json.dumps({
                    "type": "error",
                    "message": "Rate limit exceeded"
                }))
                continue

            # Process message
    except:
        pass
```

---

## 🚀 Production Tips

### **Load Balancing**

```python
# Use Redis for pub/sub between multiple instances
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

class DistributedManager:
    def __init__(self):
        self.local_connections = {}
        self.redis = redis_client

    async def broadcast(self, message: dict):
        # Send to local connections
        for websocket in self.local_connections.values():
            await websocket.send_text(json.dumps(message))

        # Publish to other instances
        self.redis.publish('websocket_broadcast', json.dumps(message))

    async def listen_for_broadcasts(self):
        pubsub = self.redis.pubsub()
        pubsub.subscribe('websocket_broadcast')

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                await self.send_to_local_connections(data)
```

### **Logging**

```python
import structlog

logger = structlog.get_logger()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    logger.info("websocket_connect", client_id=client_id)

    try:
        await websocket.accept()

        while True:
            data = await websocket.receive_text()
            logger.info("message_received",
                       client_id=client_id,
                       message_length=len(data))

    except Exception as e:
        logger.error("websocket_error",
                    client_id=client_id,
                    error=str(e))
    finally:
        logger.info("websocket_disconnect", client_id=client_id)
```

---

## 📱 Frontend JavaScript

### **Connection Management**

```javascript
class WebSocketManager {
  constructor(url) {
    this.url = url;
    this.ws = null;
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectInterval = 1000;
    this.messageQueue = [];
  }

  connect() {
    this.ws = new WebSocket(this.url);

    this.ws.onopen = () => {
      console.log('Connected');
      this.reconnectAttempts = 0;
      this.flushMessageQueue();
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.handleMessage(data);
    };

    this.ws.onclose = () => {
      console.log('Disconnected');
      this.reconnect();
    };

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
  }

  send(message) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message));
    } else {
      this.messageQueue.push(message);
    }
  }

  reconnect() {
    if (this.reconnectAttempts < this.maxReconnectAttempts) {
      setTimeout(() => {
        this.reconnectAttempts++;
        console.log(`Reconnecting... (${this.reconnectAttempts})`);
        this.connect();
      }, this.reconnectInterval * this.reconnectAttempts);
    }
  }

  flushMessageQueue() {
    while (this.messageQueue.length > 0) {
      const message = this.messageQueue.shift();
      this.send(message);
    }
  }
}

// Usage
const wsManager = new WebSocketManager('ws://localhost:8000/ws');
wsManager.connect();
```

---

**💡 Tip**: Guarda este cheat sheet como referencia rápida durante el desarrollo de aplicaciones WebSocket.
