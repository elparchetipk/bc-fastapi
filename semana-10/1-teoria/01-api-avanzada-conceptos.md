# Conceptos de API Avanzada: WebSockets, Background Tasks y SSE

## 📚 Introducción

En esta semana exploraremos las funcionalidades avanzadas de FastAPI que nos permiten crear aplicaciones **interactivas y de alto rendimiento**. Mientras que las APIs REST tradicionales siguen un patrón de **request-response**, las funcionalidades que veremos esta semana nos permiten:

- **Comunicación bidireccional** en tiempo real
- **Procesamiento asíncrono** de tareas pesadas
- **Actualizaciones automáticas** del cliente sin polling

## 🔌 WebSockets: Comunicación en Tiempo Real

### **¿Qué son los WebSockets?**

Los WebSockets proporcionan un **canal de comunicación bidireccional** entre cliente y servidor sobre una única conexión TCP. A diferencia de HTTP tradicional:

```
HTTP Tradicional:
Cliente → Request  → Servidor
Cliente ← Response ← Servidor
[Conexión cerrada]

WebSocket:
Cliente ↔ Conexión Persistente ↔ Servidor
[Comunicación bidireccional continua]
```

### **Casos de Uso Ideales**

✅ **Perfectos para:**

- Chat en tiempo real
- Notificaciones push
- Colaboración en vivo (docs compartidos)
- Gaming multijugador
- Trading/dashboard financiero
- Actualizaciones de estado en vivo

❌ **No ideales para:**

- APIs REST tradicionales
- Transferencia de archivos grandes
- Operaciones stateless simples
- SEO-dependent content

### **Ventajas y Desventajas**

#### ✅ **Ventajas**

- **Latencia ultra-baja**: Sin overhead de HTTP headers
- **Bidireccional**: Servidor puede iniciar comunicación
- **Persistente**: Una conexión para múltiples mensajes
- **Eficiente**: Menos bandwidth que polling

#### ❌ **Desventajas**

- **Resource intensive**: Mantiene conexiones abiertas
- **Complejidad**: Manejo de estado y reconexión
- **Scaling challenges**: Sticky sessions, load balancing
- **Debugging**: Más difícil que HTTP tradicional

### **Anatomía de una Conexión WebSocket**

```python
# 1. Handshake HTTP → WebSocket
GET /ws HTTP/1.1
Host: example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==

# 2. Server Response
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: HSmrc0sMlYUkAGmm5OPpG2HaGWk=

# 3. Comunicación bidireccional
Cliente → {"type": "message", "data": "Hello"}
Servidor → {"type": "response", "data": "Hi there!"}
```

## ⚙️ Background Tasks: Procesamiento Asíncrono

### **¿Qué son las Background Tasks?**

Las Background Tasks permiten **ejecutar operaciones pesadas** sin bloquear la respuesta HTTP al cliente. Son ideales para operaciones que:

- Toman tiempo considerable
- No afectan la respuesta inmediata
- Pueden fallar sin afectar la experiencia del usuario

### **Tipos de Background Tasks**

#### **1. FastAPI Background Tasks**

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Simula envío de email (operación lenta)
    time.sleep(2)
    print(f"Email enviado a {email}: {message}")

@app.post("/send-notification/")
async def create_user(email: str, background_tasks: BackgroundTasks):
    # Respuesta inmediata al cliente
    user = create_user_in_db(email)

    # Tarea en background (no bloquea)
    background_tasks.add_task(send_email, email, "¡Bienvenido!")

    return {"message": "Usuario creado", "user_id": user.id}
```

#### **2. Async Background Tasks**

```python
import asyncio

async def process_data_async(data: dict):
    # Procesamiento asíncrono pesado
    await asyncio.sleep(5)  # Simula operación lenta
    # Procesamiento de datos...

@app.post("/process/")
async def process_request(data: dict, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_data_async, data)
    return {"status": "processing started"}
```

### **Casos de Uso Comunes**

✅ **Perfectas para:**

- Envío de emails/SMS
- Procesamiento de imágenes
- Generación de reportes
- Limpieza de datos
- Notificaciones push
- Backup de datos
- Análisis de logs

❌ **No apropiadas para:**

- Operaciones críticas para la respuesta
- Tareas que requieren resultado inmediato
- Operaciones que deben ser transaccionales
- Tasks de muy larga duración (>30 min)

### **Patterns y Best Practices**

#### **1. Error Handling**

```python
async def safe_background_task(data: dict):
    try:
        await risky_operation(data)
    except Exception as e:
        # Log error, send to monitoring system
        logger.error(f"Background task failed: {e}")
        # Optionally notify admins
```

#### **2. Task Status Tracking**

```python
# Usando Redis para tracking
import redis

async def tracked_task(task_id: str, data: dict):
    redis_client.set(f"task:{task_id}", "processing")
    try:
        result = await long_operation(data)
        redis_client.set(f"task:{task_id}", f"completed:{result}")
    except Exception as e:
        redis_client.set(f"task:{task_id}", f"failed:{str(e)}")
```

## 📡 Server-Sent Events (SSE): Streaming en Tiempo Real

### **¿Qué son los Server-Sent Events?**

SSE permite al servidor **enviar actualizaciones automáticas** al cliente usando una conexión HTTP persistente. Es más simple que WebSockets pero **unidireccional** (solo servidor → cliente).

```
Cliente: GET /events (EventSource)
Servidor: data: {"update": "New message"}
Servidor: data: {"update": "User joined"}
Servidor: data: {"update": "Status changed"}
[Conexión se mantiene abierta]
```

### **SSE vs WebSockets vs Polling**

| Aspecto             | SSE                | WebSockets    | Polling            |
| ------------------- | ------------------ | ------------- | ------------------ |
| **Dirección**       | Servidor → Cliente | Bidireccional | Cliente → Servidor |
| **Complejidad**     | Baja               | Media         | Muy Baja           |
| **Overhead**        | Bajo               | Muy Bajo      | Alto               |
| **Reconexión**      | Automática         | Manual        | No aplica          |
| **Browser Support** | Excelente          | Excelente     | Universal          |

### **Casos de Uso para SSE**

✅ **Ideal para:**

- Feeds de noticias/social media
- Actualizaciones de stock/precios
- Notificaciones en tiempo real
- Progress bars de operaciones largas
- Dashboard metrics en vivo
- Live blogs/comentarios

### **Implementación Básica**

```python
from fastapi.responses import StreamingResponse
import json
import asyncio

@app.get("/events")
async def stream_events():
    async def event_generator():
        while True:
            # Simular datos en tiempo real
            data = {"timestamp": time.time(), "value": random.randint(1, 100)}
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(1)

    return StreamingResponse(
        event_generator(),
        media_type="text/plain"
    )
```

```javascript
// Cliente JavaScript
const eventSource = new EventSource('/events');
eventSource.onmessage = function (event) {
  const data = JSON.parse(event.data);
  updateDashboard(data);
};
```

## 🚀 Caching Avanzado con Redis

### **¿Por qué Redis para APIs Avanzadas?**

Redis no es solo un cache, es una **estructura de datos en memoria** que potencia las funcionalidades avanzadas:

- **Cache inteligente** para WebSockets
- **Message broker** para Background Tasks
- **Pub/Sub** para eventos en tiempo real
- **Session storage** para conexiones persistentes

### **Patterns de Caching Avanzado**

#### **1. Cache-Aside Pattern**

```python
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

async def get_user_data(user_id: int):
    # 1. Intentar cache primero
    cached = redis_client.get(f"user:{user_id}")
    if cached:
        return json.loads(cached)

    # 2. Si no está en cache, consultar DB
    user = await db.get_user(user_id)

    # 3. Guardar en cache para próximas consultas
    redis_client.setex(
        f"user:{user_id}",
        3600,  # TTL: 1 hora
        json.dumps(user)
    )

    return user
```

#### **2. Write-Through Pattern**

```python
async def update_user(user_id: int, data: dict):
    # 1. Actualizar base de datos
    updated_user = await db.update_user(user_id, data)

    # 2. Actualizar cache inmediatamente
    redis_client.setex(
        f"user:{user_id}",
        3600,
        json.dumps(updated_user)
    )

    return updated_user
```

#### **3. Pub/Sub para Eventos en Tiempo Real**

```python
# Publisher (cuando algo cambia)
async def notify_user_update(user_id: int, data: dict):
    redis_client.publish(
        f"user_updates:{user_id}",
        json.dumps(data)
    )

# Subscriber (en WebSocket connection)
async def listen_for_updates(user_id: int, websocket: WebSocket):
    pubsub = redis_client.pubsub()
    pubsub.subscribe(f"user_updates:{user_id}")

    for message in pubsub.listen():
        if message['type'] == 'message':
            await websocket.send_text(message['data'])
```

## 🔧 Integración: Combinando Todas las Tecnologías

### **Arquitectura de Sistema Completo**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Frontend      │    │    FastAPI       │    │     Redis       │
│                 │    │                  │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │ WebSocket   │◄┼────┼─│ WebSocket    │ │    │ │ Pub/Sub     │ │
│ │ Client      │ │    │ │ Handler      │◄┼────┼─│ Messages    │ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
│                 │    │                  │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │ EventSource │◄┼────┼─│ SSE          │ │    │ │ Cache       │ │
│ │ (SSE)       │ │    │ │ Endpoint     │◄┼────┼─│ Layer       │ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
│                 │    │                  │    │                 │
│ ┌─────────────┐ │    │ ┌──────────────┐ │    │ ┌─────────────┐ │
│ │ REST API    │◄┼────┼─│ Background   │ │    │ │ Task Queue  │ │
│ │ Calls       │ │    │ │ Tasks        │◄┼────┼─│ (Optional)  │ │
│ └─────────────┘ │    │ └──────────────┘ │    │ └─────────────┘ │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   PostgreSQL    │
                       │   Database      │
                       └─────────────────┘
```

### **Flujo de Datos Típico**

1. **Usuario hace acción** (REST API call)
2. **API procesa request** y actualiza base de datos
3. **Background Task** se ejecuta (email, procesamiento)
4. **Redis Pub/Sub** notifica cambios
5. **WebSocket** envía actualización en tiempo real
6. **SSE** actualiza dashboard/metrics
7. **Cache** optimiza próximas consultas

## 🔒 Consideraciones de Seguridad

### **Autenticación en WebSockets**

```python
from fastapi import WebSocket, HTTPException, Depends
from jose import jwt

async def authenticate_websocket(websocket: WebSocket, token: str):
    try:
        # Validar JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401)
        return user_id
    except jwt.JWTError:
        await websocket.close(code=1008, reason="Invalid token")
        return None

@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    user_id = await authenticate_websocket(websocket, token)
    if user_id is None:
        return

    await websocket.accept()
    # ... resto de la lógica
```

### **Rate Limiting para APIs en Tiempo Real**

```python
from collections import defaultdict
import time

# Simple rate limiter en memoria
request_counts = defaultdict(list)

async def rate_limit_websocket(user_id: str, max_requests: int = 10, window: int = 60):
    now = time.time()
    requests = request_counts[user_id]

    # Limpiar requests antiguos
    requests[:] = [req_time for req_time in requests if now - req_time < window]

    if len(requests) >= max_requests:
        return False

    requests.append(now)
    return True
```

## 📊 Monitoring y Observabilidad

### **Métricas Importantes**

#### **WebSockets**

- Conexiones activas
- Mensajes por segundo
- Latencia promedio
- Errores de conexión
- Memory usage por conexión

#### **Background Tasks**

- Tasks en queue
- Tasks completadas/fallidas
- Tiempo promedio de ejecución
- Resource usage

#### **SSE**

- Streams activos
- Events por segundo
- Disconnection rate

### **Implementación de Métricas**

```python
from prometheus_client import Counter, Histogram, Gauge

# Métricas WebSocket
ws_connections = Gauge('websocket_connections_total', 'Total WebSocket connections')
ws_messages = Counter('websocket_messages_total', 'Total WebSocket messages', ['direction'])
ws_latency = Histogram('websocket_message_latency_seconds', 'WebSocket message latency')

# Métricas Background Tasks
bg_tasks = Counter('background_tasks_total', 'Total background tasks', ['status'])
bg_duration = Histogram('background_task_duration_seconds', 'Background task duration')

class WebSocketMetrics:
    def __init__(self):
        ws_connections.inc()

    def __del__(self):
        ws_connections.dec()

    def message_sent(self):
        ws_messages.labels(direction='sent').inc()
```

## 🎯 Best Practices y Patterns

### **1. Connection Management**

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_connections: Dict[str, Set[str]] = defaultdict(set)

    async def connect(self, connection_id: str, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[connection_id] = websocket
        self.user_connections[user_id].add(connection_id)

    def disconnect(self, connection_id: str, user_id: str):
        if connection_id in self.active_connections:
            del self.active_connections[connection_id]
            self.user_connections[user_id].discard(connection_id)

    async def send_to_user(self, user_id: str, message: str):
        connections = self.user_connections.get(user_id, set())
        for connection_id in connections.copy():
            websocket = self.active_connections.get(connection_id)
            if websocket:
                try:
                    await websocket.send_text(message)
                except:
                    # Connection is dead, clean up
                    self.disconnect(connection_id, user_id)
```

### **2. Graceful Degradation**

```python
async def send_notification(user_id: str, message: str):
    # 1. Intentar WebSocket primero (tiempo real)
    if await send_websocket_notification(user_id, message):
        return "websocket"

    # 2. Fallback a SSE
    if await send_sse_notification(user_id, message):
        return "sse"

    # 3. Fallback a background task (email/push)
    background_tasks.add_task(send_email_notification, user_id, message)
    return "email"
```

### **3. Resource Cleanup**

```python
import atexit
import signal

class ResourceManager:
    def __init__(self):
        self.active_connections = []
        self.background_tasks = []

        # Cleanup en shutdown
        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def cleanup(self):
        # Cerrar conexiones WebSocket
        for ws in self.active_connections:
            asyncio.create_task(ws.close())

        # Cancelar background tasks
        for task in self.background_tasks:
            task.cancel()

    def signal_handler(self, signum, frame):
        self.cleanup()
        sys.exit(0)
```

## 🚀 Conclusión

Las funcionalidades avanzadas de FastAPI nos permiten crear aplicaciones **modernas e interactivas** que van más allá de las APIs REST tradicionales. La combinación de:

- **WebSockets** para comunicación bidireccional
- **Background Tasks** para procesamiento asíncrono
- **Server-Sent Events** para actualizaciones automáticas
- **Caching inteligente** para optimización

...nos da las herramientas para construir aplicaciones de **clase empresarial** con experiencias de usuario excepcionales.

### **Próximos Pasos**

En las prácticas de esta semana implementaremos:

1. **Sistema de chat** completo con WebSockets
2. **Procesamiento de notificaciones** con Background Tasks
3. **Dashboard en tiempo real** con SSE
4. **Aplicación integrada** combinando todas las tecnologías

**¡Comencemos a construir el futuro de las APIs!** 🚀

---

_Teoría de API Avanzada - Semana 10 - Bootcamp FastAPI_
