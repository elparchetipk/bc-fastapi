# Conceptos de APIs Avanzadas y Arquitectura Real-time

## 📚 Introducción

En esta semana exploraremos conceptos avanzados para el desarrollo de APIs modernas que requieren comunicación en tiempo real, procesamiento asíncrono y arquitecturas reactivas. Estos conceptos son fundamentales para aplicaciones contemporáneas como chat applications, dashboards en vivo, sistemas colaborativos y plataformas de gaming.

---

## 🌐 WebSockets: Comunicación Bidireccional

### Conceptos Fundamentales

**WebSocket** es un protocolo de comunicación que permite una conexión bidireccional persistente entre cliente y servidor, superando las limitaciones del tradicional modelo request/response de HTTP.

#### ¿Por qué WebSockets?

```python
# Problema con HTTP tradicional (polling)
# Cliente pregunta cada X segundos: "¿hay algo nuevo?"
def traditional_polling():
    while True:
        response = requests.get("/api/messages")
        update_ui(response.json())
        time.sleep(1)  # Desperdicia recursos, latencia alta

# Solución con WebSockets
# Servidor envía datos cuando ocurre algo nuevo
async def websocket_approach(websocket):
    async for message in websocket:
        # Procesar mensaje inmediatamente
        broadcast_to_all_clients(message)
```

#### Características Clave

1. **Persistent Connection**: Una sola conexión se mantiene abierta
2. **Bidirectional**: Cliente y servidor pueden enviar datos en cualquier momento
3. **Low Latency**: Sin overhead de HTTP headers en cada mensaje
4. **Real-time**: Datos se transmiten instantáneamente

### Casos de Uso Ideales

- 💬 **Chat Applications**: Mensajería instantánea
- 📊 **Live Dashboards**: Métricas actualizándose en tiempo real
- 🎮 **Multiplayer Games**: Sincronización de estado entre jugadores
- 📈 **Trading Platforms**: Precios de acciones en vivo
- 👥 **Collaborative Tools**: Editing simultáneo (Google Docs style)

---

## ⚙️ Background Tasks: Procesamiento Asíncrono

### ¿Qué son las Background Tasks?

Las **Background Tasks** son operaciones que se ejecutan fuera del ciclo de request/response principal, permitiendo que la API responda rápidamente mientras procesa operaciones pesadas en segundo plano.

#### Problema que Resuelven

```python
# ❌ Problema: Operación lenta bloquea la response
@app.post("/send-email")
async def send_email_sync(email_data: EmailData):
    # Esta operación puede tomar 5-10 segundos
    result = send_email_to_smtp_server(email_data)
    generate_pdf_report(email_data.user_id)  # Otros 3-5 segundos
    update_analytics(email_data)  # 2-3 segundos más

    return {"status": "sent"}  # Cliente espera 10-18 segundos 😫

# ✅ Solución: Background task
@app.post("/send-email")
async def send_email_async(email_data: EmailData, background_tasks: BackgroundTasks):
    # Respuesta inmediata
    background_tasks.add_task(send_email_to_smtp_server, email_data)
    background_tasks.add_task(generate_pdf_report, email_data.user_id)
    background_tasks.add_task(update_analytics, email_data)

    return {"status": "queued"}  # Cliente recibe respuesta en ~50ms 🚀
```

### Tipos de Background Tasks

#### 1. **FastAPI Background Tasks** (Simple)

```python
from fastapi import BackgroundTasks

# Para tareas simples y rápidas
def simple_task(name: str):
    time.sleep(2)
    print(f"Task {name} completed")

@app.post("/quick-task")
async def create_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(simple_task, "quick")
    return {"message": "Task started"}
```

#### 2. **Celery** (Distribuido y Robusto)

```python
from celery import Celery

# Para tareas complejas, distribuidas y con retry logic
celery_app = Celery('tasks', broker='redis://localhost:6379')

@celery_app.task(retry_backoff=True, max_retries=3)
def complex_task(data):
    # Procesamiento pesado
    result = heavy_computation(data)
    return result

@app.post("/heavy-task")
async def create_heavy_task(data: dict):
    task = complex_task.delay(data)
    return {"task_id": task.id, "status": "queued"}
```

### Casos de Uso Comunes

- 📧 **Email Processing**: Envío masivo de newsletters
- 🖼️ **Image Processing**: Redimensionado, filtros, compresión
- 📊 **Report Generation**: PDFs, Excel, análisis pesados
- 🔄 **Data Synchronization**: ETL processes, API integrations
- 🧹 **Cleanup Tasks**: Eliminación de archivos temporales
- 📱 **Push Notifications**: Envío a dispositivos móviles

---

## 📡 Event-Driven Architecture

### Conceptos Fundamentales

La **Arquitectura Event-Driven** es un patrón donde los componentes del sistema se comunican através de eventos, creando sistemas altamente desacoplados y reactivos.

#### Componentes Principales

```python
# Event Publisher (Publicador)
class UserService:
    def create_user(self, user_data):
        user = User.create(user_data)

        # Publicar evento
        event_bus.publish("user.created", {
            "user_id": user.id,
            "email": user.email,
            "timestamp": datetime.now()
        })

        return user

# Event Subscriber (Suscriptor)
class EmailService:
    @event_bus.subscribe("user.created")
    async def send_welcome_email(self, event_data):
        user_id = event_data["user_id"]
        await send_welcome_email(user_id)

class AnalyticsService:
    @event_bus.subscribe("user.created")
    async def track_user_signup(self, event_data):
        await analytics.track("user_signup", event_data)
```

### Beneficios de Event-Driven Architecture

1. **Desacoplamiento**: Servicios no dependen directamente entre sí
2. **Escalabilidad**: Fácil agregar nuevos subscribers
3. **Resilience**: Fallos en un servicio no afectan otros
4. **Auditability**: Historial completo de eventos del sistema

### Patrones Comunes

#### 1. **Event Bus Pattern**

```python
class EventBus:
    def __init__(self):
        self.subscribers = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable):
        self.subscribers[event_type].append(handler)

    async def publish(self, event_type: str, event_data: dict):
        for handler in self.subscribers[event_type]:
            await handler(event_data)
```

#### 2. **Pub/Sub with Redis**

```python
import redis
import json

class RedisPubSub:
    def __init__(self):
        self.redis = redis.Redis()

    def publish(self, channel: str, message: dict):
        self.redis.publish(channel, json.dumps(message))

    def subscribe(self, channel: str, callback: Callable):
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)

        for message in pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                callback(data)
```

---

## 🔔 Real-time Notifications

### Sistema de Notificaciones Moderno

Un sistema de notificaciones real-time permite comunicar cambios y actualizaciones a los usuarios instantáneamente a través de múltiples canales.

#### Arquitectura de Notificaciones

```python
# 1. Event Detection
@app.post("/orders/{order_id}/pay")
async def process_payment(order_id: int, payment_data: PaymentData):
    # Procesar pago
    result = payment_processor.charge(payment_data)

    if result.success:
        # 2. Trigger Notification Event
        await notification_service.send_notification(
            user_id=order.user_id,
            type="payment_success",
            channels=["websocket", "email", "push"],
            data={"order_id": order_id, "amount": payment_data.amount}
        )

# 3. Multi-channel Delivery
class NotificationService:
    async def send_notification(self, user_id: int, type: str, channels: list, data: dict):
        notification = Notification(
            user_id=user_id,
            type=type,
            data=data,
            timestamp=datetime.now()
        )

        # Enviar por todos los canales especificados
        tasks = []
        if "websocket" in channels:
            tasks.append(self.send_websocket(user_id, notification))
        if "email" in channels:
            tasks.append(self.send_email(user_id, notification))
        if "push" in channels:
            tasks.append(self.send_push(user_id, notification))

        await asyncio.gather(*tasks)
```

### Tipos de Notificaciones

#### 1. **In-App Notifications** (WebSocket)

```python
# Real-time, instantáneo, dentro de la aplicación
await websocket_manager.send_to_user(user_id, {
    "type": "notification",
    "title": "Payment Successful",
    "message": "Your order #1234 has been paid",
    "timestamp": datetime.now().isoformat()
})
```

#### 2. **Email Notifications** (Background Task)

```python
# Persistente, formal, para información importante
@celery_app.task
def send_email_notification(user_id: int, template: str, context: dict):
    user = User.get(user_id)
    email_service.send_template_email(
        to=user.email,
        template=template,
        context=context
    )
```

#### 3. **Push Notifications** (Mobile)

```python
# Para usuarios móviles, incluso cuando app está cerrada
async def send_push_notification(user_id: int, message: str):
    user_devices = await get_user_devices(user_id)

    for device in user_devices:
        await push_service.send(
            device_token=device.token,
            title="New Message",
            body=message,
            badge_count=await get_unread_count(user_id)
        )
```

---

## 🏗️ Arquitectura Integrada

### Combinando Todos los Conceptos

Una aplicación moderna típicamente combina todos estos patrones:

```python
# Ejemplo: Sistema de Chat Colaborativo
class ChatApplication:
    def __init__(self):
        self.websocket_manager = WebSocketManager()
        self.event_bus = EventBus()
        self.notification_service = NotificationService()
        self.background_tasks = CeleryApp()

    @app.websocket("/chat/{room_id}")
    async def chat_endpoint(self, websocket: WebSocket, room_id: str):
        # 1. WebSocket Connection
        await self.websocket_manager.connect(websocket, room_id)

        try:
            while True:
                # 2. Receive Message
                message = await websocket.receive_json()

                # 3. Process via Event-Driven
                await self.event_bus.publish("message.received", {
                    "room_id": room_id,
                    "user_id": message["user_id"],
                    "content": message["content"],
                    "timestamp": datetime.now()
                })

        except WebSocketDisconnect:
            await self.websocket_manager.disconnect(websocket, room_id)

    @event_bus.subscribe("message.received")
    async def handle_new_message(self, event_data):
        room_id = event_data["room_id"]

        # 4. Real-time Broadcasting (WebSocket)
        await self.websocket_manager.broadcast_to_room(room_id, event_data)

        # 5. Background Processing
        self.background_tasks.delay_task("process_message", event_data)

        # 6. Notifications for offline users
        offline_users = await get_offline_room_users(room_id)
        for user_id in offline_users:
            await self.notification_service.send_notification(
                user_id=user_id,
                type="new_message",
                channels=["email", "push"],
                data=event_data
            )
```

---

## 🎯 Patterns y Best Practices

### 1. **Connection Management** (WebSockets)

```python
class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.user_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, room_id: str, user_id: int):
        await websocket.accept()

        # Gestión de rooms
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

        # Mapeo usuario -> conexión
        self.user_connections[user_id] = websocket

    async def disconnect(self, websocket: WebSocket, room_id: str, user_id: int):
        self.active_connections[room_id].remove(websocket)
        if user_id in self.user_connections:
            del self.user_connections[user_id]

    async def send_to_user(self, user_id: int, message: dict):
        if user_id in self.user_connections:
            websocket = self.user_connections[user_id]
            await websocket.send_json(message)

    async def broadcast_to_room(self, room_id: str, message: dict):
        if room_id in self.active_connections:
            disconnected = []
            for websocket in self.active_connections[room_id]:
                try:
                    await websocket.send_json(message)
                except:
                    disconnected.append(websocket)

            # Cleanup desconectados
            for ws in disconnected:
                self.active_connections[room_id].remove(ws)
```

### 2. **Task Queue Patterns**

```python
# Retry Logic
@celery_app.task(bind=True, max_retries=3)
def reliable_task(self, data):
    try:
        return process_data(data)
    except Exception as exc:
        # Exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

# Task Prioritization
@celery_app.task(priority=1)  # Alta prioridad
def urgent_task(data):
    return process_urgent_data(data)

@celery_app.task(priority=5)  # Baja prioridad
def background_cleanup():
    cleanup_temp_files()

# Task Chaining
from celery import chain
task_chain = chain(
    download_file.s(url),
    process_file.s(),
    send_notification.s()
)
result = task_chain.apply_async()
```

### 3. **Event Sourcing Básico**

```python
class EventStore:
    def __init__(self):
        self.events = []

    def append_event(self, event):
        event['id'] = len(self.events) + 1
        event['timestamp'] = datetime.now()
        self.events.append(event)

    def get_events_for_aggregate(self, aggregate_id):
        return [e for e in self.events if e.get('aggregate_id') == aggregate_id]

    def replay_events(self, aggregate_id):
        events = self.get_events_for_aggregate(aggregate_id)
        state = {}

        for event in events:
            state = apply_event(state, event)

        return state
```

---

## 🚀 Performance Considerations

### WebSocket Optimization

- **Connection Pooling**: Limitar conexiones concurrentes
- **Message Batching**: Agrupar mensajes pequeños
- **Compression**: Usar compresión WebSocket para mensajes grandes
- **Heartbeat**: Implement ping/pong para detectar conexiones muertas

### Background Task Optimization

- **Worker Scaling**: Ajustar número de workers según carga
- **Task Batching**: Procesar múltiples elementos juntos
- **Memory Management**: Evitar memory leaks en long-running tasks
- **Monitoring**: Tracking de performance y bottlenecks

### Event System Optimization

- **Event Batching**: Procesar eventos en lotes
- **Async Processing**: Usar async/await en event handlers
- **Event Filtering**: Filtrar eventos irrelevantes temprano
- **Circuit Breaker**: Evitar cascading failures

---

## 🔒 Security Considerations

### WebSocket Security

```python
# Authentication
@app.websocket("/secure-chat")
async def secure_chat(websocket: WebSocket, token: str = Query(...)):
    user = verify_jwt_token(token)
    if not user:
        await websocket.close(code=4001, reason="Unauthorized")
        return

    await websocket.accept()
    # ... resto de la lógica

# Rate Limiting
class WebSocketRateLimiter:
    def __init__(self, max_messages_per_minute: int = 60):
        self.max_messages = max_messages_per_minute
        self.message_counts = {}

    async def check_rate_limit(self, user_id: int) -> bool:
        now = time.time()
        minute_window = int(now // 60)

        key = f"{user_id}:{minute_window}"

        if key not in self.message_counts:
            self.message_counts[key] = 0

        self.message_counts[key] += 1

        return self.message_counts[key] <= self.max_messages
```

### Background Task Security

```python
# Input Validation
@celery_app.task
def secure_task(data):
    # Validar input antes de procesar
    validated_data = TaskSchema(**data)
    return process_validated_data(validated_data)

# Access Control
@celery_app.task
def privileged_task(data, user_id):
    user = get_user(user_id)
    if not user.has_permission("admin"):
        raise PermissionError("Insufficient privileges")

    return process_admin_task(data)
```

---

## 📊 Monitoring y Observability

### Métricas Importantes

#### WebSocket Metrics

- Active connections count
- Messages per second
- Connection duration
- Error rates
- Latency percentiles

#### Background Task Metrics

- Queue length
- Task completion rate
- Task failure rate
- Processing time
- Worker utilization

#### Event System Metrics

- Events published per second
- Event processing latency
- Subscriber performance
- Failed event deliveries

```python
# Implementación básica de métricas
class MetricsCollector:
    def __init__(self):
        self.metrics = {
            'websocket_connections': 0,
            'messages_sent': 0,
            'tasks_completed': 0,
            'events_published': 0
        }

    def increment(self, metric: str, value: int = 1):
        self.metrics[metric] += value

    def get_metrics(self):
        return self.metrics.copy()

# Usage in WebSocket
metrics = MetricsCollector()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    metrics.increment('websocket_connections')
    try:
        while True:
            message = await websocket.receive_json()
            metrics.increment('messages_sent')
            # Process message
    finally:
        metrics.increment('websocket_connections', -1)
```

---

## 🎓 Próximos Pasos

Después de dominar estos conceptos fundamentales:

1. **Implementa WebSockets** en tu API siguiendo los patrones aprendidos
2. **Configura Background Tasks** para operaciones pesadas
3. **Diseña Event-Driven Architecture** para desacoplar servicios
4. **Integra notificaciones** multi-canal en tu aplicación
5. **Monitorea performance** y optimiza basándote en métricas reales

¡En las prácticas implementaremos cada uno de estos conceptos de manera hands-on! 🚀

---

_Conceptos desarrollados para Semana 8 - Bootcamp FastAPI_  
_Tiempo de estudio: 30 minutos_
