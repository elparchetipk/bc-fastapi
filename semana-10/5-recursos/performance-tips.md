# Performance Tips - API Avanzada

⚡ **Optimización de rendimiento para WebSockets, Background Tasks y SSE**

---

## 🚀 WebSocket Performance

### **Connection Optimization**

#### **Connection Pooling**

```python
import asyncio
from typing import Dict, Set
import weakref

class OptimizedConnectionManager:
    def __init__(self, max_connections_per_room=1000):
        self.connections: Dict[str, Set[weakref.ref]] = {}
        self.max_connections_per_room = max_connections_per_room
        self._connection_count = 0

    async def add_connection(self, room: str, websocket):
        # Use weak references to prevent memory leaks
        if room not in self.connections:
            self.connections[room] = set()

        # Check room capacity
        if len(self.connections[room]) >= self.max_connections_per_room:
            await websocket.close(code=4004, reason="Room is full")
            return False

        self.connections[room].add(weakref.ref(websocket))
        self._connection_count += 1
        return True

    async def broadcast_optimized(self, room: str, message: str):
        if room not in self.connections:
            return

        # Batch sending for better performance
        dead_refs = set()
        tasks = []

        for ws_ref in self.connections[room]:
            websocket = ws_ref()
            if websocket is None:
                dead_refs.add(ws_ref)
            else:
                tasks.append(websocket.send_text(message))

        # Clean up dead references
        self.connections[room] -= dead_refs

        # Send all messages concurrently
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
```

#### **Message Batching**

```python
import asyncio
from collections import defaultdict
import json

class MessageBatcher:
    def __init__(self, batch_size=10, max_wait_time=0.1):
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self.message_queues = defaultdict(list)
        self.timers = {}

    async def add_message(self, room: str, message: dict):
        self.message_queues[room].append(message)

        # Start timer if this is the first message
        if len(self.message_queues[room]) == 1:
            self.timers[room] = asyncio.create_task(
                self._flush_after_delay(room)
            )

        # Flush immediately if batch is full
        if len(self.message_queues[room]) >= self.batch_size:
            await self._flush_messages(room)

    async def _flush_after_delay(self, room: str):
        await asyncio.sleep(self.max_wait_time)
        await self._flush_messages(room)

    async def _flush_messages(self, room: str):
        if room in self.timers:
            self.timers[room].cancel()
            del self.timers[room]

        if self.message_queues[room]:
            batch = {
                "type": "batch",
                "messages": self.message_queues[room]
            }
            await manager.broadcast_to_room(room, json.dumps(batch))
            self.message_queues[room].clear()

# Usage
batcher = MessageBatcher()

async def send_message_optimized(room: str, message: dict):
    await batcher.add_message(room, message)
```

### **Memory Management**

#### **Connection Cleanup**

```python
import gc
import asyncio
from datetime import datetime, timedelta

class ConnectionCleaner:
    def __init__(self, cleanup_interval=300):  # 5 minutes
        self.cleanup_interval = cleanup_interval
        self.last_activity = {}
        self._running = False

    def track_activity(self, connection_id: str):
        self.last_activity[connection_id] = datetime.utcnow()

    async def start_cleanup_task(self):
        self._running = True
        while self._running:
            await asyncio.sleep(self.cleanup_interval)
            await self._cleanup_inactive_connections()
            gc.collect()  # Force garbage collection

    async def _cleanup_inactive_connections(self):
        cutoff_time = datetime.utcnow() - timedelta(minutes=30)
        inactive_connections = [
            conn_id for conn_id, last_active in self.last_activity.items()
            if last_active < cutoff_time
        ]

        for conn_id in inactive_connections:
            await self._close_connection(conn_id)
            del self.last_activity[conn_id]

    async def _close_connection(self, connection_id: str):
        # Implementation depends on your connection manager
        pass

cleaner = ConnectionCleaner()

# Start cleanup task
asyncio.create_task(cleaner.start_cleanup_task())
```

---

## ⚙️ Background Tasks Optimization

### **Task Queue Optimization**

#### **Priority Queues**

```python
import asyncio
import heapq
from dataclasses import dataclass, field
from typing import Any, Callable
from enum import IntEnum

class Priority(IntEnum):
    LOW = 3
    NORMAL = 2
    HIGH = 1
    URGENT = 0

@dataclass
class Task:
    priority: Priority
    func: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)

    def __lt__(self, other):
        return (self.priority, self.created_at) < (other.priority, other.created_at)

class PriorityTaskManager:
    def __init__(self, max_workers=10):
        self.task_queue = []
        self.max_workers = max_workers
        self.workers = []
        self.running = False

    async def add_task(self, func: Callable, priority: Priority = Priority.NORMAL, *args, **kwargs):
        task = Task(priority=priority, func=func, args=args, kwargs=kwargs)
        heapq.heappush(self.task_queue, task)

    async def start_workers(self):
        self.running = True
        self.workers = [
            asyncio.create_task(self._worker(f"worker-{i}"))
            for i in range(self.max_workers)
        ]

    async def _worker(self, name: str):
        while self.running:
            if self.task_queue:
                task = heapq.heappop(self.task_queue)
                try:
                    if asyncio.iscoroutinefunction(task.func):
                        await task.func(*task.args, **task.kwargs)
                    else:
                        task.func(*task.args, **task.kwargs)
                except Exception as e:
                    logger.error(f"Task failed in {name}: {e}")
            else:
                await asyncio.sleep(0.1)

# Usage
task_manager = PriorityTaskManager(max_workers=5)

@app.on_event("startup")
async def startup():
    await task_manager.start_workers()

async def send_urgent_notification(user_id: int, message: str):
    await task_manager.add_task(
        process_notification,
        Priority.URGENT,
        user_id,
        message
    )
```

#### **Batch Processing**

```python
import asyncio
from collections import defaultdict
from typing import List, Dict, Any

class BatchProcessor:
    def __init__(self, batch_size=100, max_wait_time=5.0):
        self.batch_size = batch_size
        self.max_wait_time = max_wait_time
        self.batches: Dict[str, List[Any]] = defaultdict(list)
        self.timers: Dict[str, asyncio.Task] = {}

    async def add_to_batch(self, batch_type: str, item: Any):
        self.batches[batch_type].append(item)

        # Start timer if this is the first item
        if len(self.batches[batch_type]) == 1:
            self.timers[batch_type] = asyncio.create_task(
                self._process_after_delay(batch_type)
            )

        # Process immediately if batch is full
        if len(self.batches[batch_type]) >= self.batch_size:
            await self._process_batch(batch_type)

    async def _process_after_delay(self, batch_type: str):
        await asyncio.sleep(self.max_wait_time)
        await self._process_batch(batch_type)

    async def _process_batch(self, batch_type: str):
        if batch_type in self.timers:
            self.timers[batch_type].cancel()
            del self.timers[batch_type]

        if self.batches[batch_type]:
            items = self.batches[batch_type].copy()
            self.batches[batch_type].clear()

            # Process batch based on type
            if batch_type == "emails":
                await self._send_email_batch(items)
            elif batch_type == "notifications":
                await self._send_notification_batch(items)

    async def _send_email_batch(self, emails: List[Dict]):
        # Batch email sending for better performance
        async with aiosmtplib.SMTP() as smtp:
            for email in emails:
                await smtp.send_message(email)

    async def _send_notification_batch(self, notifications: List[Dict]):
        # Batch notification processing
        pass

batch_processor = BatchProcessor()

async def queue_email(recipient: str, subject: str, body: str):
    email_data = {
        "recipient": recipient,
        "subject": subject,
        "body": body
    }
    await batch_processor.add_to_batch("emails", email_data)
```

### **Resource Management**

#### **Connection Pooling for Databases**

```python
import asyncpg
import asyncio
from typing import Optional

class DatabasePool:
    def __init__(self, dsn: str, min_size=10, max_size=50):
        self.dsn = dsn
        self.min_size = min_size
        self.max_size = max_size
        self.pool: Optional[asyncpg.Pool] = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(
            self.dsn,
            min_size=self.min_size,
            max_size=self.max_size,
            command_timeout=60,
            server_settings={
                'jit': 'off',  # Disable JIT for faster connection
                'application_name': 'fastapi_app'
            }
        )

    async def execute_query(self, query: str, *args):
        async with self.pool.acquire() as connection:
            return await connection.fetch(query, *args)

    async def execute_transaction(self, queries: List[tuple]):
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                results = []
                for query, args in queries:
                    result = await connection.fetch(query, *args)
                    results.append(result)
                return results

# Global pool instance
db_pool = DatabasePool("postgresql://user:password@localhost/db")

@app.on_event("startup")
async def startup():
    await db_pool.create_pool()

@app.on_event("shutdown")
async def shutdown():
    if db_pool.pool:
        await db_pool.pool.close()
```

---

## 📊 Server-Sent Events Optimization

### **Efficient Event Streaming**

#### **Event Buffering**

```python
import asyncio
from collections import deque
from typing import Dict, Deque
import json

class SSEManager:
    def __init__(self, buffer_size=1000):
        self.clients: Dict[str, asyncio.Queue] = {}
        self.event_buffer: Deque = deque(maxlen=buffer_size)
        self.buffer_size = buffer_size

    async def add_client(self, client_id: str) -> asyncio.Queue:
        queue = asyncio.Queue(maxsize=100)
        self.clients[client_id] = queue

        # Send buffered events to new client
        for event in self.event_buffer:
            try:
                queue.put_nowait(event)
            except asyncio.QueueFull:
                # Skip old events if queue is full
                pass

        return queue

    def remove_client(self, client_id: str):
        if client_id in self.clients:
            del self.clients[client_id]

    async def broadcast_event(self, event_data: dict):
        event_json = json.dumps(event_data)

        # Add to buffer
        self.event_buffer.append(event_json)

        # Send to all clients
        dead_clients = []
        for client_id, queue in self.clients.items():
            try:
                queue.put_nowait(event_json)
            except asyncio.QueueFull:
                # Client is not consuming events fast enough
                dead_clients.append(client_id)

        # Remove dead clients
        for client_id in dead_clients:
            self.remove_client(client_id)

sse_manager = SSEManager()

@app.get("/sse/stream")
async def sse_stream(request: Request):
    client_id = str(uuid.uuid4())
    queue = await sse_manager.add_client(client_id)

    async def event_generator():
        try:
            while True:
                if await request.is_disconnected():
                    break

                try:
                    # Wait for event with timeout
                    event = await asyncio.wait_for(queue.get(), timeout=30)
                    yield f"data: {event}\n\n"
                except asyncio.TimeoutError:
                    # Send heartbeat
                    yield f"data: {json.dumps({'type': 'heartbeat'})}\n\n"

        except Exception as e:
            logger.error(f"SSE error for client {client_id}: {e}")
        finally:
            sse_manager.remove_client(client_id)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )
```

### **Memory-Efficient Event History**

#### **Circular Buffer Implementation**

```python
import threading
from typing import Any, Optional

class CircularEventBuffer:
    def __init__(self, max_size=10000):
        self.max_size = max_size
        self.buffer = [None] * max_size
        self.head = 0
        self.tail = 0
        self.size = 0
        self.lock = threading.RLock()

    def add_event(self, event: Any):
        with self.lock:
            self.buffer[self.tail] = event
            self.tail = (self.tail + 1) % self.max_size

            if self.size < self.max_size:
                self.size += 1
            else:
                # Buffer is full, move head
                self.head = (self.head + 1) % self.max_size

    def get_recent_events(self, count: Optional[int] = None) -> list:
        with self.lock:
            if count is None:
                count = self.size
            else:
                count = min(count, self.size)

            events = []
            for i in range(count):
                index = (self.tail - 1 - i) % self.max_size
                if self.buffer[index] is not None:
                    events.append(self.buffer[index])

            return list(reversed(events))

    def clear(self):
        with self.lock:
            self.buffer = [None] * self.max_size
            self.head = 0
            self.tail = 0
            self.size = 0

# Usage
event_buffer = CircularEventBuffer(max_size=5000)

async def add_dashboard_event(event_type: str, data: dict):
    event = {
        "type": event_type,
        "data": data,
        "timestamp": datetime.utcnow().isoformat()
    }
    event_buffer.add_event(event)
    await sse_manager.broadcast_event(event)
```

---

## 💾 Caching Strategies

### **Redis Caching**

#### **Smart Cache Management**

```python
import redis.asyncio as redis
import pickle
import json
from typing import Any, Optional, Union
import hashlib

class SmartCache:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.default_ttl = 300  # 5 minutes

    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        # Generate deterministic key from arguments
        content = f"{prefix}:{args}:{sorted(kwargs.items())}"
        return hashlib.md5(content.encode()).hexdigest()

    async def get(self, key: str, default: Any = None) -> Any:
        try:
            data = await self.redis.get(key)
            if data:
                return pickle.loads(data)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        return default

    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        try:
            ttl = ttl or self.default_ttl
            serialized = pickle.dumps(value)
            await self.redis.setex(key, ttl, serialized)
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    async def delete(self, pattern: str) -> int:
        """Delete keys matching pattern"""
        try:
            keys = await self.redis.keys(pattern)
            if keys:
                return await self.redis.delete(*keys)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
        return 0

    async def get_or_set(self, key: str, func: callable, ttl: Optional[int] = None) -> Any:
        """Get from cache or compute and cache"""
        value = await self.get(key)
        if value is not None:
            return value

        # Compute value
        if asyncio.iscoroutinefunction(func):
            value = await func()
        else:
            value = func()

        await self.set(key, value, ttl)
        return value

cache = SmartCache()

# Decorator for caching function results
def cached(ttl: int = 300, prefix: str = "func"):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            key = cache._generate_key(f"{prefix}:{func.__name__}", *args, **kwargs)
            return await cache.get_or_set(key, lambda: func(*args, **kwargs), ttl)
        return wrapper
    return decorator

# Usage
@cached(ttl=600, prefix="user")
async def get_user_profile(user_id: int):
    # Expensive database operation
    return await db.fetch_user(user_id)
```

### **In-Memory Caching**

#### **LRU Cache Implementation**

```python
from collections import OrderedDict
import threading
import time
from typing import Any, Optional

class LRUCache:
    def __init__(self, max_size=1000, default_ttl=300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self.cache = OrderedDict()
        self.expiry_times = {}
        self.lock = threading.RLock()

    def _is_expired(self, key: str) -> bool:
        if key in self.expiry_times:
            return time.time() > self.expiry_times[key]
        return True

    def get(self, key: str, default: Any = None) -> Any:
        with self.lock:
            if key in self.cache and not self._is_expired(key):
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                return self.cache[key]
            elif key in self.cache:
                # Expired, remove
                del self.cache[key]
                del self.expiry_times[key]
        return default

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        with self.lock:
            ttl = ttl or self.default_ttl

            # Remove if exists
            if key in self.cache:
                del self.cache[key]

            # Add new item
            self.cache[key] = value
            self.expiry_times[key] = time.time() + ttl

            # Ensure max size
            while len(self.cache) > self.max_size:
                oldest_key = next(iter(self.cache))
                del self.cache[oldest_key]
                del self.expiry_times[oldest_key]

    def clear_expired(self) -> int:
        with self.lock:
            current_time = time.time()
            expired_keys = [
                key for key, expiry in self.expiry_times.items()
                if current_time > expiry
            ]

            for key in expired_keys:
                del self.cache[key]
                del self.expiry_times[key]

            return len(expired_keys)

# Global cache instance
memory_cache = LRUCache(max_size=5000)

# Cleanup task
async def cleanup_expired_cache():
    while True:
        expired_count = memory_cache.clear_expired()
        if expired_count > 0:
            logger.info(f"Cleared {expired_count} expired cache entries")
        await asyncio.sleep(60)  # Cleanup every minute

# Start cleanup task
asyncio.create_task(cleanup_expired_cache())
```

---

## 📈 Monitoring and Profiling

### **Performance Metrics**

#### **Custom Metrics Collection**

```python
import time
import psutil
from dataclasses import dataclass
from typing import Dict, List
import asyncio

@dataclass
class PerformanceMetric:
    name: str
    value: float
    timestamp: float
    tags: Dict[str, str] = None

class MetricsCollector:
    def __init__(self, max_history=1000):
        self.metrics: Dict[str, List[PerformanceMetric]] = {}
        self.max_history = max_history

    def record_metric(self, name: str, value: float, tags: Dict[str, str] = None):
        if name not in self.metrics:
            self.metrics[name] = []

        metric = PerformanceMetric(
            name=name,
            value=value,
            timestamp=time.time(),
            tags=tags or {}
        )

        self.metrics[name].append(metric)

        # Keep only recent metrics
        if len(self.metrics[name]) > self.max_history:
            self.metrics[name] = self.metrics[name][-self.max_history:]

    def get_recent_metrics(self, name: str, seconds: int = 300) -> List[PerformanceMetric]:
        if name not in self.metrics:
            return []

        cutoff_time = time.time() - seconds
        return [
            metric for metric in self.metrics[name]
            if metric.timestamp >= cutoff_time
        ]

    def get_system_metrics(self) -> Dict[str, float]:
        """Get current system metrics"""
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "active_connections": len(manager.active_connections) if 'manager' in globals() else 0
        }

metrics = MetricsCollector()

# Middleware for request timing
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    metrics.record_metric(
        "request_duration",
        duration,
        {
            "method": request.method,
            "endpoint": str(request.url.path),
            "status_code": str(response.status_code)
        }
    )

    return response

# System metrics collection task
async def collect_system_metrics():
    while True:
        system_metrics = metrics.get_system_metrics()
        for name, value in system_metrics.items():
            metrics.record_metric(f"system_{name}", value)

        await asyncio.sleep(30)  # Collect every 30 seconds

asyncio.create_task(collect_system_metrics())
```

### **Performance Profiling**

#### **Function Profiling Decorator**

```python
import functools
import time
import cProfile
import pstats
import io
from typing import Callable

def profile_function(func: Callable) -> Callable:
    """Decorator to profile function execution"""
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()

        start_time = time.time()
        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
        finally:
            duration = time.time() - start_time
            profiler.disable()

            # Log performance data
            stream = io.StringIO()
            stats = pstats.Stats(profiler, stream=stream)
            stats.sort_stats('cumulative').print_stats(10)

            logger.info(
                f"Function {func.__name__} took {duration:.4f}s\n"
                f"Profile data:\n{stream.getvalue()}"
            )

            # Record metric
            metrics.record_metric(
                f"function_duration_{func.__name__}",
                duration
            )

        return result

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        # Same logic for sync functions
        pass

    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

# Usage
@profile_function
async def expensive_operation():
    # Some expensive operation
    await asyncio.sleep(1)
    return "result"
```

---

## 🔧 Production Optimizations

### **Nginx Configuration**

```nginx
# nginx.conf for WebSocket and SSE optimization
upstream fastapi_backend {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
}

server {
    listen 80;
    server_name your-domain.com;

    # WebSocket configuration
    location /ws {
        proxy_pass http://fastapi_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouts
        proxy_read_timeout 3600s;
        proxy_send_timeout 3600s;

        # No buffering for real-time data
        proxy_buffering off;
    }

    # SSE configuration
    location /sse {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # SSE specific settings
        proxy_buffering off;
        proxy_cache off;
        proxy_read_timeout 24h;
        proxy_send_timeout 24h;

        # Headers for SSE
        add_header 'Access-Control-Allow-Origin' '*';
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS';
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range';
        add_header 'Access-Control-Expose-Headers' 'Content-Length,Content-Range';
    }

    # Static files
    location /static {
        alias /path/to/static/files;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API endpoints
    location / {
        proxy_pass http://fastapi_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### **Docker Optimization**

```dockerfile
# Multi-stage Dockerfile for production
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app
COPY . .

# Optimize Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONOPTIMIZE=2

# Performance tuning
ENV UVICORN_WORKERS=4
ENV UVICORN_WORKER_CLASS=uvicorn.workers.UvicornWorker

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

---

**⚡ Estas optimizaciones pueden mejorar significativamente el rendimiento de tu aplicación en producción. Implementa gradualmente y mide el impacto de cada optimización.**
