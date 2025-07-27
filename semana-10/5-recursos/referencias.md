# Referencias y Recursos - Semana 10

📚 **Recursos complementarios para API avanzada: WebSockets, Background Tasks y SSE**

---

## 📖 Documentación Oficial

### **FastAPI**

- [WebSockets Guide](https://fastapi.tiangolo.com/advanced/websockets/) - Guía oficial de WebSockets
- [Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) - Tareas en segundo plano
- [Advanced Features](https://fastapi.tiangolo.com/advanced/) - Características avanzadas

### **Python Libraries**

- [python-socketio](https://python-socketio.readthedocs.io/) - Socket.IO para Python
- [websockets](https://websockets.readthedocs.io/) - WebSockets puros
- [celery](https://docs.celeryproject.org/) - Queue distribuido
- [redis-py](https://redis-py.readthedocs.io/) - Cliente Redis para Python

### **Frontend APIs**

- [WebSocket API](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) - MDN WebSocket reference
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events) - MDN SSE reference
- [EventSource API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) - Cliente SSE

---

## 🎓 Tutoriales y Cursos

### **WebSockets**

- [Real-time Web Apps with WebSockets](https://realpython.com/python-websockets/)
- [WebSocket Chat Tutorial](https://channels.readthedocs.io/en/stable/tutorial/)
- [Building Real-time Apps](https://testdriven.io/blog/fastapi-websockets/)

### **Background Tasks**

- [Celery Best Practices](https://docs.celeryproject.org/en/stable/userguide/tasks.html)
- [Redis as Message Broker](https://redis.io/docs/manual/pubsub/)
- [Monitoring Background Tasks](https://flower.readthedocs.io/)

### **Server-Sent Events**

- [SSE Complete Guide](https://www.smashingmagazine.com/2018/02/sse-websockets-data-flow-http2/)
- [Real-time Dashboard with SSE](https://testdriven.io/blog/server-sent-events/)

---

## 🔧 Herramientas y Libraries

### **Testing**

```bash
# Testing WebSockets
pip install pytest-asyncio
pip install websocket-client
pip install pytest-websocket

# Load testing
pip install websockets
pip install locust
```

### **Monitoring**

```bash
# Monitoring y logging
pip install prometheus-client
pip install grafana-api
pip install elasticsearch
pip install loguru

# APM
pip install newrelic
pip install datadog
```

### **Development Tools**

```bash
# WebSocket clients
npm install -g wscat
pip install websocket-client

# Redis tools
redis-cli
redis-commander

# Database tools
pgcli
```

---

## 📊 Arquitecturas de Referencia

### **Microservicios con WebSockets**

```text
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Gateway   │    │   Chat      │    │ Notification│
│   Service   │◄──►│   Service   │◄──►│   Service   │
└─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Load      │    │   Redis     │    │   Message   │
│   Balancer  │    │   Cluster   │    │   Queue     │
└─────────────┘    └─────────────┘    └─────────────┘
```

### **Escalabilidad Horizontal**

- Load balancing para WebSockets
- Redis Cluster para pub/sub
- Database sharding
- CDN para archivos estáticos

---

## 🛠️ Patrones de Diseño

### **WebSocket Patterns**

#### **Connection Manager Pattern**

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
```

#### **Event-Driven Pattern**

```python
class EventBus:
    def __init__(self):
        self.subscribers = {}

    def subscribe(self, event_type: str, callback):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)

    async def publish(self, event_type: str, data):
        if event_type in self.subscribers:
            for callback in self.subscribers[event_type]:
                await callback(data)
```

### **Background Task Patterns**

#### **Queue Pattern**

```python
from celery import Celery

app = Celery('tasks', broker='redis://localhost:6379')

@app.task
def send_notification(user_id: int, message: str):
    # Process notification
    pass

# En FastAPI
from fastapi import BackgroundTasks

@app.post("/send-notification/")
async def send_notification(
    user_id: int,
    message: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_notification, user_id, message)
    return {"message": "Notification queued"}
```

#### **Publisher-Subscriber Pattern**

```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

class PubSubManager:
    def __init__(self):
        self.redis = redis_client

    async def publish(self, channel: str, message: dict):
        self.redis.publish(channel, json.dumps(message))

    async def subscribe(self, channel: str, callback):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                await callback(data)
```

---

## 🔒 Seguridad Best Practices

### **WebSocket Security**

```python
# Autenticación en WebSockets
async def get_current_user_websocket(
    websocket: WebSocket,
    token: str = Query(...)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
        return await get_user(user_id)
    except JWTError:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    client_id: int,
    current_user: User = Depends(get_current_user_websocket)
):
    await manager.connect(websocket, client_id)
    # ... rest of the logic
```

### **Rate Limiting**

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/messages/")
@limiter.limit("10/minute")
async def send_message(request: Request, message: MessageCreate):
    # Message sending logic
    pass
```

### **Input Validation**

```python
from pydantic import BaseModel, validator
import bleach

class MessageCreate(BaseModel):
    content: str

    @validator('content')
    def sanitize_content(cls, v):
        # Remove potentially dangerous HTML
        return bleach.clean(v, tags=[], strip=True)

    @validator('content')
    def validate_length(cls, v):
        if len(v) > 1000:
            raise ValueError('Message too long')
        return v
```

---

## 📈 Performance Optimization

### **Database Optimization**

```sql
-- Índices para chat
CREATE INDEX idx_messages_channel_created
ON messages(channel_id, created_at DESC);

CREATE INDEX idx_messages_user_created
ON messages(user_id, created_at DESC);

-- Particionado por fecha
CREATE TABLE messages_2024_01 PARTITION OF messages
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

### **Caching Strategies**

```python
import redis
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expire_time=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"

            # Try to get from cache
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Get fresh data
            result = await func(*args, **kwargs)

            # Cache result
            redis_client.setex(
                cache_key,
                expire_time,
                json.dumps(result, default=str)
            )

            return result
        return wrapper
    return decorator

@cache_result(expire_time=60)
async def get_channel_messages(channel_id: int, limit: int = 50):
    # Database query
    return messages
```

### **WebSocket Optimization**

```python
import asyncio
from typing import Dict, Set

class OptimizedConnectionManager:
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

    async def broadcast_to_room(self, room: str, message: str, exclude: WebSocket = None):
        if room not in self.connections:
            return

        # Batch send for better performance
        tasks = []
        for websocket in self.connections[room]:
            if websocket != exclude:
                tasks.append(websocket.send_text(message))

        # Send all messages concurrently
        await asyncio.gather(*tasks, return_exceptions=True)
```

---

## 🧪 Testing Strategies

### **WebSocket Testing**

```python
import pytest
from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

def test_websocket_connection():
    with TestClient(app).websocket_connect("/ws") as websocket:
        websocket.send_text("Hello")
        data = websocket.receive_text()
        assert data == "Hello"

@pytest.mark.asyncio
async def test_websocket_broadcast():
    # Test multiple connections
    pass
```

### **Background Task Testing**

```python
import pytest
from unittest.mock import patch

@pytest.mark.asyncio
async def test_notification_task():
    with patch('app.tasks.send_email') as mock_send:
        await send_notification.delay(user_id=1, message="Test")
        mock_send.assert_called_once()
```

### **Load Testing**

```python
# locustfile.py
from locust import User, task, between
import websocket
import json

class WebSocketUser(User):
    wait_time = between(1, 3)

    def on_start(self):
        self.ws = websocket.WebSocket()
        self.ws.connect("ws://localhost:8000/ws")

    @task
    def send_message(self):
        message = {
            "type": "chat_message",
            "content": "Load test message"
        }
        self.ws.send(json.dumps(message))

    def on_stop(self):
        self.ws.close()
```

---

## 🔍 Debugging y Troubleshooting

### **Common Issues**

#### **WebSocket Connection Drops**

```python
import logging

logger = logging.getLogger(__name__)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        while True:
            try:
                data = await asyncio.wait_for(
                    websocket.receive_text(),
                    timeout=30.0
                )
                # Process data
            except asyncio.TimeoutError:
                # Send ping to keep connection alive
                await websocket.ping()
                logger.info("Sent ping to maintain connection")

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        # Cleanup
        await cleanup_connection(websocket)
```

#### **Memory Leaks in Connections**

```python
import weakref
import gc

class ConnectionTracker:
    def __init__(self):
        self._connections = weakref.WeakSet()

    def add_connection(self, websocket):
        self._connections.add(websocket)

    def get_connection_count(self):
        return len(self._connections)

    def cleanup_dead_connections(self):
        gc.collect()  # Force garbage collection
```

### **Monitoring Tools**

#### **Custom Metrics**

```python
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
websocket_connections = Counter('websocket_connections_total')
message_processing_time = Histogram('message_processing_seconds')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    websocket_connections.inc()

    try:
        with message_processing_time.time():
            # Process message
            pass
    finally:
        websocket_connections.dec()

@app.get("/metrics")
async def metrics():
    return Response(generate_latest())
```

---

## 📚 Libros y Recursos Adicionales

### **Libros Recomendados**

- **"Real-Time Web Application Development"** - Rami Sayar
- **"High Performance Browser Networking"** - Ilya Grigorik
- **"Building Microservices"** - Sam Newman
- **"Designing Data-Intensive Applications"** - Martin Kleppmann

### **Blogs y Artículos**

- [WebSocket Best Practices](https://blog.teamtreehouse.com/an-introduction-to-websockets)
- [Scaling WebSockets](https://blog.pusher.com/websockets-from-scratch/)
- [Background Task Patterns](https://testdriven.io/blog/fastapi-and-celery/)

### **Videos y Conferencias**

- [PyCon Talks on WebSockets](https://www.youtube.com/results?search_query=pycon+websockets)
- [Real-time Architecture Patterns](https://www.youtube.com/results?search_query=real+time+architecture)

---

## 🎯 Proyectos de Práctica

### **Beginner Projects**

1. **Simple Echo Server** - WebSocket que hace eco de mensajes
2. **Basic Chat Room** - Chat multiusuario básico
3. **Live Counter** - Contador que se actualiza en tiempo real

### **Intermediate Projects**

1. **Collaborative Editor** - Editor de texto colaborativo
2. **Live Dashboard** - Dashboard con métricas en tiempo real
3. **Game Server** - Servidor para juegos multijugador simple

### **Advanced Projects**

1. **Video Conference Platform** - WebRTC + WebSockets
2. **Trading Platform** - Sistema de trading en tiempo real
3. **IoT Data Platform** - Procesamiento de datos de sensores

---

## 🤝 Comunidades y Foros

### **Discord/Slack Communities**

- FastAPI Discord
- Python Discord
- Real-time Web Developers

### **Stack Overflow Tags**

- [fastapi-websocket](https://stackoverflow.com/questions/tagged/fastapi+websocket)
- [python-websockets](https://stackoverflow.com/questions/tagged/python+websockets)
- [server-sent-events](https://stackoverflow.com/questions/tagged/server-sent-events)

### **Reddit Communities**

- r/FastAPI
- r/Python
- r/webdev

---

**📖 Mantén estos recursos como referencia durante y después del bootcamp. La tecnología en tiempo real está en constante evolución.**
