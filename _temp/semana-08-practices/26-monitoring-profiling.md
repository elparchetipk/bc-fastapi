# Práctica 26: Monitoring y Profiling

## Objetivos

- Implementar monitoring completo de la aplicación
- Configurar profiling para identificar cuellos de botella
- Crear dashboards de métricas en tiempo real
- Implementar alertas y notificaciones
- Analizar performance y optimizar código

## Duración Estimada

3 horas

## Prerrequisitos

- Práctica 24 y 25 completadas
- Redis y middleware configurados
- FastAPI con métricas funcionando

---

## Paso 1: Sistema de Monitoring Avanzado

### 1.1 Implementar collector de métricas

Crear archivo `app/monitoring/metrics_collector.py`:

```python
import time
import psutil
import asyncio
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import redis
import json

@dataclass
class SystemMetrics:
    """Métricas del sistema."""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_usage_percent: float
    network_sent_mb: float
    network_recv_mb: float

@dataclass
class ApplicationMetrics:
    """Métricas de la aplicación."""
    timestamp: str
    active_connections: int
    total_requests: int
    requests_per_second: float
    avg_response_time: float
    error_rate: float
    cache_hit_rate: float
    database_connections: int

class MetricsCollector:
    """Recolector de métricas del sistema y aplicación."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.last_network_stats = None
        self.last_stats_time = None
        self.request_history = []

    async def collect_system_metrics(self) -> SystemMetrics:
        """Recopilar métricas del sistema."""
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)

        # Memoria
        memory = psutil.virtual_memory()
        memory_used_mb = memory.used / (1024 * 1024)
        memory_available_mb = memory.available / (1024 * 1024)

        # Disco
        disk = psutil.disk_usage('/')
        disk_usage_percent = disk.percent

        # Red
        network = psutil.net_io_counters()
        current_time = time.time()

        if self.last_network_stats and self.last_stats_time:
            time_diff = current_time - self.last_stats_time
            sent_diff = network.bytes_sent - self.last_network_stats.bytes_sent
            recv_diff = network.bytes_recv - self.last_network_stats.bytes_recv

            network_sent_mb = (sent_diff / time_diff) / (1024 * 1024)
            network_recv_mb = (recv_diff / time_diff) / (1024 * 1024)
        else:
            network_sent_mb = 0
            network_recv_mb = 0

        self.last_network_stats = network
        self.last_stats_time = current_time

        return SystemMetrics(
            timestamp=datetime.now().isoformat(),
            cpu_percent=round(cpu_percent, 2),
            memory_percent=round(memory.percent, 2),
            memory_used_mb=round(memory_used_mb, 2),
            memory_available_mb=round(memory_available_mb, 2),
            disk_usage_percent=round(disk_usage_percent, 2),
            network_sent_mb=round(network_sent_mb, 4),
            network_recv_mb=round(network_recv_mb, 4)
        )

    async def collect_application_metrics(self, app_metrics_middleware) -> ApplicationMetrics:
        """Recopilar métricas de la aplicación."""
        try:
            # Obtener métricas del middleware
            metrics_data = app_metrics_middleware.get_metrics()

            # Calcular requests per second
            current_time = time.time()
            total_requests = metrics_data.get('total_requests', 0)

            # Mantener historial de requests
            self.request_history.append({
                'timestamp': current_time,
                'total_requests': total_requests
            })

            # Limpiar historial viejo (últimos 60 segundos)
            cutoff_time = current_time - 60
            self.request_history = [
                r for r in self.request_history
                if r['timestamp'] > cutoff_time
            ]

            # Calcular RPS
            if len(self.request_history) >= 2:
                oldest = self.request_history[0]
                newest = self.request_history[-1]
                time_diff = newest['timestamp'] - oldest['timestamp']
                request_diff = newest['total_requests'] - oldest['total_requests']
                rps = request_diff / time_diff if time_diff > 0 else 0
            else:
                rps = 0

            # Calcular error rate
            status_codes = metrics_data.get('status_codes', {})
            total_responses = sum(status_codes.values())
            error_responses = sum(
                count for code, count in status_codes.items()
                if str(code).startswith(('4', '5'))
            )
            error_rate = (error_responses / total_responses * 100) if total_responses > 0 else 0

            # Cache hit rate (simulated - implementar según cache real)
            cache_hit_rate = await self._calculate_cache_hit_rate()

            return ApplicationMetrics(
                timestamp=datetime.now().isoformat(),
                active_connections=len(self.request_history),  # Aproximación
                total_requests=total_requests,
                requests_per_second=round(rps, 2),
                avg_response_time=round(metrics_data.get('avg_response_time', 0), 4),
                error_rate=round(error_rate, 2),
                cache_hit_rate=round(cache_hit_rate, 2),
                database_connections=await self._get_db_connections()
            )

        except Exception as e:
            print(f"Error collecting application metrics: {e}")
            return ApplicationMetrics(
                timestamp=datetime.now().isoformat(),
                active_connections=0,
                total_requests=0,
                requests_per_second=0,
                avg_response_time=0,
                error_rate=0,
                cache_hit_rate=0,
                database_connections=0
            )

    async def _calculate_cache_hit_rate(self) -> float:
        """Calcular cache hit rate."""
        try:
            # Obtener estadísticas de Redis
            info = self.redis.info()
            keyspace_hits = info.get('keyspace_hits', 0)
            keyspace_misses = info.get('keyspace_misses', 0)

            total = keyspace_hits + keyspace_misses
            if total > 0:
                return (keyspace_hits / total) * 100
            return 0
        except:
            return 0

    async def _get_db_connections(self) -> int:
        """Obtener número de conexiones de base de datos activas."""
        # Implementar según el pool de conexiones utilizado
        # Por ahora devuelve un valor simulado
        return 5

    async def store_metrics(self, system_metrics: SystemMetrics, app_metrics: ApplicationMetrics):
        """Almacenar métricas en Redis."""
        try:
            current_time = int(time.time())

            # Almacenar métricas del sistema
            system_key = f"metrics:system:{current_time}"
            self.redis.setex(
                system_key,
                3600,  # TTL 1 hora
                json.dumps(asdict(system_metrics))
            )

            # Almacenar métricas de aplicación
            app_key = f"metrics:application:{current_time}"
            self.redis.setex(
                app_key,
                3600,  # TTL 1 hora
                json.dumps(asdict(app_metrics))
            )

            # Mantener lista de timestamps para consultas
            self.redis.lpush("metrics:timestamps", current_time)
            self.redis.ltrim("metrics:timestamps", 0, 720)  # Últimas 12 horas

        except Exception as e:
            print(f"Error storing metrics: {e}")

class AlertManager:
    """Gestor de alertas basado en métricas."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.alert_thresholds = {
            'cpu_percent': 80,
            'memory_percent': 85,
            'disk_usage_percent': 90,
            'error_rate': 5,
            'avg_response_time': 2.0
        }
        self.alert_cooldown = 300  # 5 minutos

    async def check_alerts(self, system_metrics: SystemMetrics, app_metrics: ApplicationMetrics):
        """Verificar si se deben disparar alertas."""
        alerts = []

        # Verificar métricas del sistema
        if system_metrics.cpu_percent > self.alert_thresholds['cpu_percent']:
            alerts.append({
                'type': 'system',
                'metric': 'cpu_percent',
                'value': system_metrics.cpu_percent,
                'threshold': self.alert_thresholds['cpu_percent'],
                'severity': 'warning'
            })

        if system_metrics.memory_percent > self.alert_thresholds['memory_percent']:
            alerts.append({
                'type': 'system',
                'metric': 'memory_percent',
                'value': system_metrics.memory_percent,
                'threshold': self.alert_thresholds['memory_percent'],
                'severity': 'critical'
            })

        if system_metrics.disk_usage_percent > self.alert_thresholds['disk_usage_percent']:
            alerts.append({
                'type': 'system',
                'metric': 'disk_usage_percent',
                'value': system_metrics.disk_usage_percent,
                'threshold': self.alert_thresholds['disk_usage_percent'],
                'severity': 'critical'
            })

        # Verificar métricas de aplicación
        if app_metrics.error_rate > self.alert_thresholds['error_rate']:
            alerts.append({
                'type': 'application',
                'metric': 'error_rate',
                'value': app_metrics.error_rate,
                'threshold': self.alert_thresholds['error_rate'],
                'severity': 'warning'
            })

        if app_metrics.avg_response_time > self.alert_thresholds['avg_response_time']:
            alerts.append({
                'type': 'application',
                'metric': 'avg_response_time',
                'value': app_metrics.avg_response_time,
                'threshold': self.alert_thresholds['avg_response_time'],
                'severity': 'warning'
            })

        # Procesar alertas
        for alert in alerts:
            await self._process_alert(alert)

    async def _process_alert(self, alert: dict):
        """Procesar una alerta individual."""
        alert_key = f"alert:{alert['type']}:{alert['metric']}"

        # Verificar cooldown
        if self.redis.exists(alert_key):
            return  # Alerta en cooldown

        # Disparar alerta
        alert['timestamp'] = datetime.now().isoformat()

        # Log de la alerta
        print(f"🚨 ALERT [{alert['severity'].upper()}]: "
              f"{alert['metric']} = {alert['value']} "
              f"(threshold: {alert['threshold']})")

        # Almacenar alerta
        self.redis.setex(
            f"alerts:history:{int(time.time())}",
            86400,  # TTL 24 horas
            json.dumps(alert)
        )

        # Activar cooldown
        self.redis.setex(alert_key, self.alert_cooldown, "1")

        # Aquí se puede integrar con sistemas de notificación
        # como Slack, email, PagerDuty, etc.
```

### 1.2 Profiling con cProfile

Crear archivo `app/monitoring/profiler.py`:

```python
import cProfile
import pstats
import io
from typing import Optional, Dict, Any
from functools import wraps
import time
import asyncio
from contextlib import contextmanager

class APIProfiler:
    """Profiler para endpoints de FastAPI."""

    def __init__(self):
        self.profiles = {}
        self.enabled = False

    def enable(self):
        """Habilitar profiling."""
        self.enabled = True

    def disable(self):
        """Deshabilitar profiling."""
        self.enabled = False

    @contextmanager
    def profile_context(self, name: str):
        """Context manager para profiling."""
        if not self.enabled:
            yield
            return

        profiler = cProfile.Profile()
        profiler.enable()

        try:
            yield
        finally:
            profiler.disable()

            # Guardar perfil
            self.profiles[name] = {
                'profiler': profiler,
                'timestamp': time.time()
            }

    def profile_endpoint(self, name: str):
        """Decorador para profiling de endpoints."""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                if not self.enabled:
                    return await func(*args, **kwargs)

                with self.profile_context(name):
                    return await func(*args, **kwargs)

            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                if not self.enabled:
                    return func(*args, **kwargs)

                with self.profile_context(name):
                    return func(*args, **kwargs)

            return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
        return decorator

    def get_profile_stats(self, name: str, top_n: int = 20) -> Optional[Dict[str, Any]]:
        """Obtener estadísticas de un perfil."""
        if name not in self.profiles:
            return None

        profiler = self.profiles[name]['profiler']
        timestamp = self.profiles[name]['timestamp']

        # Crear string buffer para capturar output
        output = io.StringIO()
        stats = pstats.Stats(profiler, stream=output)
        stats.sort_stats('cumulative')
        stats.print_stats(top_n)

        # Obtener estadísticas como string
        stats_output = output.getvalue()
        output.close()

        # Obtener estadísticas clave
        total_calls = stats.total_calls
        total_time = stats.total_tt

        return {
            'name': name,
            'timestamp': timestamp,
            'total_calls': total_calls,
            'total_time': round(total_time, 4),
            'stats_output': stats_output
        }

    def get_all_profiles(self) -> Dict[str, Any]:
        """Obtener todos los perfiles."""
        result = {}
        for name in self.profiles:
            result[name] = self.get_profile_stats(name)
        return result

    def clear_profiles(self):
        """Limpiar todos los perfiles."""
        self.profiles.clear()

# Instancia global del profiler
api_profiler = APIProfiler()

class PerformanceTracker:
    """Tracker de performance para operaciones específicas."""

    def __init__(self):
        self.tracked_operations = {}

    @contextmanager
    def track_operation(self, operation_name: str):
        """Context manager para trackear operaciones."""
        start_time = time.time()

        try:
            yield
        finally:
            end_time = time.time()
            execution_time = end_time - start_time

            if operation_name not in self.tracked_operations:
                self.tracked_operations[operation_name] = []

            self.tracked_operations[operation_name].append({
                'execution_time': execution_time,
                'timestamp': start_time
            })

            # Mantener solo las últimas 100 mediciones
            if len(self.tracked_operations[operation_name]) > 100:
                self.tracked_operations[operation_name] = \
                    self.tracked_operations[operation_name][-100:]

    def get_operation_stats(self, operation_name: str) -> Optional[Dict[str, Any]]:
        """Obtener estadísticas de una operación."""
        if operation_name not in self.tracked_operations:
            return None

        times = [
            op['execution_time']
            for op in self.tracked_operations[operation_name]
        ]

        if not times:
            return None

        return {
            'operation': operation_name,
            'count': len(times),
            'avg_time': round(sum(times) / len(times), 4),
            'min_time': round(min(times), 4),
            'max_time': round(max(times), 4),
            'total_time': round(sum(times), 4)
        }

    def get_all_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de todas las operaciones."""
        result = {}
        for operation_name in self.tracked_operations:
            result[operation_name] = self.get_operation_stats(operation_name)
        return result

# Instancia global del tracker
performance_tracker = PerformanceTracker()
```

## Paso 2: Endpoints de Monitoring

### 2.1 Router de monitoring

Crear archivo `app/routers/monitoring.py`:

```python
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, List, Optional
import time
import json

from app.monitoring.metrics_collector import MetricsCollector, AlertManager
from app.monitoring.profiler import api_profiler, performance_tracker

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

# Variables globales (en producción usar dependency injection)
metrics_collector = None
alert_manager = None

def set_monitoring_dependencies(collector: MetricsCollector, alerts: AlertManager):
    """Configurar dependencias de monitoring."""
    global metrics_collector, alert_manager
    metrics_collector = collector
    alert_manager = alerts

@router.get("/system")
async def get_system_metrics() -> Dict[str, Any]:
    """Obtener métricas actuales del sistema."""
    if not metrics_collector:
        raise HTTPException(status_code=503, detail="Metrics collector not configured")

    system_metrics = await metrics_collector.collect_system_metrics()
    return {
        "status": "success",
        "data": system_metrics.__dict__
    }

@router.get("/application")
async def get_application_metrics(app_metrics_middleware) -> Dict[str, Any]:
    """Obtener métricas actuales de la aplicación."""
    if not metrics_collector:
        raise HTTPException(status_code=503, detail="Metrics collector not configured")

    app_metrics = await metrics_collector.collect_application_metrics(app_metrics_middleware)
    return {
        "status": "success",
        "data": app_metrics.__dict__
    }

@router.get("/history")
async def get_metrics_history(
    hours: int = Query(1, ge=1, le=24, description="Horas de historial")
) -> Dict[str, Any]:
    """Obtener historial de métricas."""
    if not metrics_collector:
        raise HTTPException(status_code=503, detail="Metrics collector not configured")

    try:
        # Obtener timestamps
        current_time = int(time.time())
        start_time = current_time - (hours * 3600)

        timestamps = metrics_collector.redis.lrange("metrics:timestamps", 0, -1)
        timestamps = [int(ts) for ts in timestamps if int(ts) >= start_time]

        system_history = []
        app_history = []

        for timestamp in timestamps:
            # Métricas del sistema
            system_key = f"metrics:system:{timestamp}"
            system_data = metrics_collector.redis.get(system_key)
            if system_data:
                system_history.append(json.loads(system_data))

            # Métricas de aplicación
            app_key = f"metrics:application:{timestamp}"
            app_data = metrics_collector.redis.get(app_key)
            if app_data:
                app_history.append(json.loads(app_data))

        return {
            "status": "success",
            "period_hours": hours,
            "data": {
                "system": system_history,
                "application": app_history
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving history: {str(e)}")

@router.get("/alerts")
async def get_alerts_history(
    hours: int = Query(24, ge=1, le=168, description="Horas de historial de alertas")
) -> Dict[str, Any]:
    """Obtener historial de alertas."""
    if not metrics_collector:
        raise HTTPException(status_code=503, detail="Metrics collector not configured")

    try:
        current_time = int(time.time())
        start_time = current_time - (hours * 3600)

        # Buscar alertas en el rango de tiempo
        pattern = "alerts:history:*"
        keys = metrics_collector.redis.keys(pattern)

        alerts = []
        for key in keys:
            timestamp = int(key.split(":")[-1])
            if timestamp >= start_time:
                alert_data = metrics_collector.redis.get(key)
                if alert_data:
                    alerts.append(json.loads(alert_data))

        # Ordenar por timestamp
        alerts.sort(key=lambda x: x['timestamp'], reverse=True)

        return {
            "status": "success",
            "period_hours": hours,
            "total_alerts": len(alerts),
            "data": alerts
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving alerts: {str(e)}")

@router.get("/profiling")
async def get_profiling_data() -> Dict[str, Any]:
    """Obtener datos de profiling."""
    profiles = api_profiler.get_all_profiles()
    performance_stats = performance_tracker.get_all_stats()

    return {
        "status": "success",
        "data": {
            "profiles": profiles,
            "performance_stats": performance_stats,
            "profiling_enabled": api_profiler.enabled
        }
    }

@router.post("/profiling/enable")
async def enable_profiling() -> Dict[str, str]:
    """Habilitar profiling."""
    api_profiler.enable()
    return {"status": "success", "message": "Profiling enabled"}

@router.post("/profiling/disable")
async def disable_profiling() -> Dict[str, str]:
    """Deshabilitar profiling."""
    api_profiler.disable()
    return {"status": "success", "message": "Profiling disabled"}

@router.delete("/profiling")
async def clear_profiling_data() -> Dict[str, str]:
    """Limpiar datos de profiling."""
    api_profiler.clear_profiles()
    performance_tracker.tracked_operations.clear()
    return {"status": "success", "message": "Profiling data cleared"}

@router.get("/dashboard")
async def get_dashboard_data(app_metrics_middleware) -> Dict[str, Any]:
    """Obtener datos consolidados para dashboard."""
    if not metrics_collector:
        raise HTTPException(status_code=503, detail="Metrics collector not configured")

    try:
        # Métricas actuales
        system_metrics = await metrics_collector.collect_system_metrics()
        app_metrics = await metrics_collector.collect_application_metrics(app_metrics_middleware)

        # Profiling
        performance_stats = performance_tracker.get_all_stats()

        # Alertas recientes (última hora)
        current_time = int(time.time())
        start_time = current_time - 3600

        pattern = "alerts:history:*"
        keys = metrics_collector.redis.keys(pattern)
        recent_alerts = []

        for key in keys:
            timestamp = int(key.split(":")[-1])
            if timestamp >= start_time:
                alert_data = metrics_collector.redis.get(key)
                if alert_data:
                    recent_alerts.append(json.loads(alert_data))

        return {
            "status": "success",
            "timestamp": system_metrics.timestamp,
            "data": {
                "system": system_metrics.__dict__,
                "application": app_metrics.__dict__,
                "performance": performance_stats,
                "recent_alerts": len(recent_alerts),
                "profiling_enabled": api_profiler.enabled
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting dashboard data: {str(e)}")
```

## Paso 3: Background Tasks para Monitoring

### 3.1 Task scheduler

Crear archivo `app/monitoring/scheduler.py`:

```python
import asyncio
import logging
from typing import Callable, Dict, Any
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class TaskScheduler:
    """Planificador de tareas para monitoring."""

    def __init__(self):
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.running = False

    def add_task(
        self,
        name: str,
        func: Callable,
        interval_seconds: int,
        args: tuple = (),
        kwargs: dict = None
    ):
        """Agregar tarea programada."""
        self.tasks[name] = {
            'func': func,
            'interval': interval_seconds,
            'args': args or (),
            'kwargs': kwargs or {},
            'last_run': None,
            'next_run': datetime.now(),
            'enabled': True
        }
        logger.info(f"Task '{name}' scheduled to run every {interval_seconds} seconds")

    def remove_task(self, name: str):
        """Remover tarea programada."""
        if name in self.tasks:
            del self.tasks[name]
            logger.info(f"Task '{name}' removed")

    def enable_task(self, name: str):
        """Habilitar tarea."""
        if name in self.tasks:
            self.tasks[name]['enabled'] = True
            logger.info(f"Task '{name}' enabled")

    def disable_task(self, name: str):
        """Deshabilitar tarea."""
        if name in self.tasks:
            self.tasks[name]['enabled'] = False
            logger.info(f"Task '{name}' disabled")

    async def run_scheduler(self):
        """Ejecutar planificador de tareas."""
        self.running = True
        logger.info("Task scheduler started")

        try:
            while self.running:
                current_time = datetime.now()

                for name, task in self.tasks.items():
                    if not task['enabled']:
                        continue

                    if current_time >= task['next_run']:
                        try:
                            logger.debug(f"Running task: {name}")

                            # Ejecutar tarea
                            if asyncio.iscoroutinefunction(task['func']):
                                await task['func'](*task['args'], **task['kwargs'])
                            else:
                                task['func'](*task['args'], **task['kwargs'])

                            # Actualizar tiempos
                            task['last_run'] = current_time
                            task['next_run'] = current_time + timedelta(seconds=task['interval'])

                            logger.debug(f"Task '{name}' completed successfully")

                        except Exception as e:
                            logger.error(f"Error running task '{name}': {e}")
                            # Reprogramar la tarea incluso si falló
                            task['next_run'] = current_time + timedelta(seconds=task['interval'])

                # Dormir por un segundo antes de la siguiente verificación
                await asyncio.sleep(1)

        except Exception as e:
            logger.error(f"Scheduler error: {e}")
        finally:
            logger.info("Task scheduler stopped")

    def stop(self):
        """Detener planificador."""
        self.running = False

    def get_status(self) -> Dict[str, Any]:
        """Obtener estado del planificador."""
        current_time = datetime.now()

        task_status = {}
        for name, task in self.tasks.items():
            task_status[name] = {
                'enabled': task['enabled'],
                'interval': task['interval'],
                'last_run': task['last_run'].isoformat() if task['last_run'] else None,
                'next_run': task['next_run'].isoformat(),
                'seconds_until_next': (task['next_run'] - current_time).total_seconds()
            }

        return {
            'running': self.running,
            'total_tasks': len(self.tasks),
            'enabled_tasks': sum(1 for t in self.tasks.values() if t['enabled']),
            'tasks': task_status
        }

# Instancia global del scheduler
task_scheduler = TaskScheduler()
```

### 3.2 Configurar monitoring automático

Crear archivo `app/monitoring/auto_monitor.py`:

```python
import asyncio
import logging
from app.monitoring.metrics_collector import MetricsCollector, AlertManager
from app.monitoring.scheduler import task_scheduler

logger = logging.getLogger(__name__)

class AutoMonitor:
    """Monitoring automático de la aplicación."""

    def __init__(
        self,
        metrics_collector: MetricsCollector,
        alert_manager: AlertManager,
        app_metrics_middleware
    ):
        self.metrics_collector = metrics_collector
        self.alert_manager = alert_manager
        self.app_metrics_middleware = app_metrics_middleware
        self.enabled = False

    async def start(self):
        """Iniciar monitoring automático."""
        if self.enabled:
            return

        self.enabled = True
        logger.info("Starting automatic monitoring...")

        # Agregar tareas al scheduler
        task_scheduler.add_task(
            name="collect_metrics",
            func=self._collect_and_store_metrics,
            interval_seconds=30  # Cada 30 segundos
        )

        task_scheduler.add_task(
            name="check_alerts",
            func=self._check_and_process_alerts,
            interval_seconds=60  # Cada minuto
        )

        task_scheduler.add_task(
            name="cleanup_old_data",
            func=self._cleanup_old_data,
            interval_seconds=3600  # Cada hora
        )

        # Iniciar scheduler si no está corriendo
        if not task_scheduler.running:
            asyncio.create_task(task_scheduler.run_scheduler())

        logger.info("Automatic monitoring started")

    async def stop(self):
        """Detener monitoring automático."""
        if not self.enabled:
            return

        self.enabled = False

        # Remover tareas del scheduler
        task_scheduler.remove_task("collect_metrics")
        task_scheduler.remove_task("check_alerts")
        task_scheduler.remove_task("cleanup_old_data")

        logger.info("Automatic monitoring stopped")

    async def _collect_and_store_metrics(self):
        """Recopilar y almacenar métricas."""
        try:
            # Recopilar métricas
            system_metrics = await self.metrics_collector.collect_system_metrics()
            app_metrics = await self.metrics_collector.collect_application_metrics(
                self.app_metrics_middleware
            )

            # Almacenar en Redis
            await self.metrics_collector.store_metrics(system_metrics, app_metrics)

            logger.debug("Metrics collected and stored successfully")

        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")

    async def _check_and_process_alerts(self):
        """Verificar y procesar alertas."""
        try:
            # Obtener métricas más recientes
            system_metrics = await self.metrics_collector.collect_system_metrics()
            app_metrics = await self.metrics_collector.collect_application_metrics(
                self.app_metrics_middleware
            )

            # Verificar alertas
            await self.alert_manager.check_alerts(system_metrics, app_metrics)

            logger.debug("Alerts checked successfully")

        except Exception as e:
            logger.error(f"Error checking alerts: {e}")

    async def _cleanup_old_data(self):
        """Limpiar datos antiguos."""
        try:
            # Limpiar métricas más antiguas que 24 horas
            current_time = int(time.time())
            cutoff_time = current_time - (24 * 3600)

            # Limpiar timestamps antiguos
            self.metrics_collector.redis.lrem("metrics:timestamps", 0, cutoff_time)

            # Limpiar alertas más antiguas que 7 días
            alert_cutoff = current_time - (7 * 24 * 3600)
            pattern = "alerts:history:*"
            keys = self.metrics_collector.redis.keys(pattern)

            deleted_count = 0
            for key in keys:
                timestamp = int(key.split(":")[-1])
                if timestamp < alert_cutoff:
                    self.metrics_collector.redis.delete(key)
                    deleted_count += 1

            logger.info(f"Cleanup completed: deleted {deleted_count} old alert records")

        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
```

## Paso 4: Dashboard Web Simple

### 4.1 Template HTML para dashboard

Crear archivo `app/templates/dashboard.html`:

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta
      name="viewport"
      content="width=device-width, initial-scale=1.0" />
    <title>FastAPI Performance Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }

      body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
          sans-serif;
        background-color: #f5f5f5;
        color: #333;
      }

      .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        text-align: center;
      }

      .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
      }

      .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-bottom: 30px;
      }

      .metric-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #667eea;
      }

      .metric-title {
        font-size: 14px;
        color: #666;
        margin-bottom: 5px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
      }

      .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #333;
      }

      .metric-unit {
        font-size: 14px;
        color: #888;
      }

      .status-good {
        border-left-color: #4caf50;
      }
      .status-warning {
        border-left-color: #ff9800;
      }
      .status-critical {
        border-left-color: #f44336;
      }

      .chart-container {
        background: white;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
      }

      .chart-title {
        font-size: 18px;
        margin-bottom: 15px;
        color: #333;
      }

      .controls {
        text-align: center;
        margin-bottom: 20px;
      }

      .btn {
        background: #667eea;
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        cursor: pointer;
        margin: 0 5px;
        font-size: 14px;
      }

      .btn:hover {
        background: #5a6fd8;
      }

      .btn.active {
        background: #4caf50;
      }

      .alert-badge {
        background: #f44336;
        color: white;
        border-radius: 50%;
        width: 20px;
        height: 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        margin-left: 10px;
      }

      .last-updated {
        text-align: center;
        color: #666;
        font-size: 12px;
        margin-top: 20px;
      }
    </style>
  </head>
  <body>
    <div class="header">
      <h1>📊 FastAPI Performance Dashboard</h1>
      <p>Monitoring en tiempo real del sistema y aplicación</p>
    </div>

    <div class="container">
      <div class="controls">
        <button
          class="btn active"
          onclick="toggleAutoRefresh()">
          🔄 Auto Refresh (<span id="refresh-status">ON</span>)
        </button>
        <button
          class="btn"
          onclick="refreshData()">
          ⟳ Refresh Now
        </button>
        <button
          class="btn"
          onclick="toggleProfiling()">
          🔍 <span id="profiling-status">Enable</span> Profiling
        </button>
        <span id="alert-indicator"></span>
      </div>

      <div class="metrics-grid">
        <div
          class="metric-card"
          id="cpu-card">
          <div class="metric-title">CPU Usage</div>
          <div
            class="metric-value"
            id="cpu-value">
            --
          </div>
          <div class="metric-unit">%</div>
        </div>

        <div
          class="metric-card"
          id="memory-card">
          <div class="metric-title">Memory Usage</div>
          <div
            class="metric-value"
            id="memory-value">
            --
          </div>
          <div class="metric-unit">%</div>
        </div>

        <div
          class="metric-card"
          id="requests-card">
          <div class="metric-title">Requests/sec</div>
          <div
            class="metric-value"
            id="requests-value">
            --
          </div>
          <div class="metric-unit">req/s</div>
        </div>

        <div
          class="metric-card"
          id="response-card">
          <div class="metric-title">Avg Response Time</div>
          <div
            class="metric-value"
            id="response-value">
            --
          </div>
          <div class="metric-unit">ms</div>
        </div>

        <div
          class="metric-card"
          id="error-card">
          <div class="metric-title">Error Rate</div>
          <div
            class="metric-value"
            id="error-value">
            --
          </div>
          <div class="metric-unit">%</div>
        </div>

        <div
          class="metric-card"
          id="cache-card">
          <div class="metric-title">Cache Hit Rate</div>
          <div
            class="metric-value"
            id="cache-value">
            --
          </div>
          <div class="metric-unit">%</div>
        </div>
      </div>

      <div class="chart-container">
        <div class="chart-title">📈 System Metrics Over Time</div>
        <canvas
          id="systemChart"
          width="400"
          height="200"></canvas>
      </div>

      <div class="chart-container">
        <div class="chart-title">🌐 Application Metrics Over Time</div>
        <canvas
          id="appChart"
          width="400"
          height="200"></canvas>
      </div>

      <div
        class="last-updated"
        id="last-updated">
        Last updated: --
      </div>
    </div>

    <script>
      let autoRefresh = true;
      let refreshInterval;
      let profilingEnabled = false;

      // Configurar charts
      const systemCtx = document.getElementById('systemChart').getContext('2d');
      const appCtx = document.getElementById('appChart').getContext('2d');

      const systemChart = new Chart(systemCtx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [
            {
              label: 'CPU %',
              borderColor: '#FF6384',
              backgroundColor: 'rgba(255, 99, 132, 0.1)',
              data: [],
            },
            {
              label: 'Memory %',
              borderColor: '#36A2EB',
              backgroundColor: 'rgba(54, 162, 235, 0.1)',
              data: [],
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              max: 100,
            },
          },
        },
      });

      const appChart = new Chart(appCtx, {
        type: 'line',
        data: {
          labels: [],
          datasets: [
            {
              label: 'Requests/sec',
              borderColor: '#4BC0C0',
              backgroundColor: 'rgba(75, 192, 192, 0.1)',
              data: [],
            },
            {
              label: 'Response Time (ms)',
              borderColor: '#9966FF',
              backgroundColor: 'rgba(153, 102, 255, 0.1)',
              data: [],
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });

      async function fetchDashboardData() {
        try {
          const response = await fetch('/monitoring/dashboard');
          const result = await response.json();

          if (result.status === 'success') {
            updateMetrics(result.data);
            updateCharts(result.data);
            updateLastUpdated();
          }
        } catch (error) {
          console.error('Error fetching dashboard data:', error);
        }
      }

      function updateMetrics(data) {
        const { system, application, recent_alerts } = data;

        // Actualizar métricas del sistema
        updateMetricCard(
          'cpu',
          system.cpu_percent,
          '%',
          getStatusClass(system.cpu_percent, 80, 90)
        );
        updateMetricCard(
          'memory',
          system.memory_percent,
          '%',
          getStatusClass(system.memory_percent, 80, 90)
        );

        // Actualizar métricas de aplicación
        updateMetricCard(
          'requests',
          application.requests_per_second,
          'req/s',
          'status-good'
        );
        updateMetricCard(
          'response',
          (application.avg_response_time * 1000).toFixed(1),
          'ms',
          getStatusClass(application.avg_response_time * 1000, 1000, 2000)
        );
        updateMetricCard(
          'error',
          application.error_rate,
          '%',
          getStatusClass(application.error_rate, 5, 10)
        );
        updateMetricCard(
          'cache',
          application.cache_hit_rate,
          '%',
          'status-good'
        );

        // Actualizar indicador de alertas
        const alertIndicator = document.getElementById('alert-indicator');
        if (recent_alerts > 0) {
          alertIndicator.innerHTML = `<span class="alert-badge">${recent_alerts}</span> Alertas recientes`;
        } else {
          alertIndicator.innerHTML = '';
        }

        // Actualizar estado de profiling
        profilingEnabled = data.profiling_enabled;
        document.getElementById('profiling-status').textContent =
          profilingEnabled ? 'Disable' : 'Enable';
      }

      function updateMetricCard(id, value, unit, statusClass) {
        const valueElement = document.getElementById(`${id}-value`);
        const cardElement = document.getElementById(`${id}-card`);

        valueElement.textContent = value;

        // Actualizar clase de estado
        cardElement.className = `metric-card ${statusClass}`;
      }

      function getStatusClass(value, warningThreshold, criticalThreshold) {
        if (value >= criticalThreshold) return 'status-critical';
        if (value >= warningThreshold) return 'status-warning';
        return 'status-good';
      }

      function updateCharts(data) {
        const { system, application } = data;
        const now = new Date().toLocaleTimeString();

        // Limitar a últimos 20 puntos de data
        const maxPoints = 20;

        // Actualizar chart del sistema
        systemChart.data.labels.push(now);
        systemChart.data.datasets[0].data.push(system.cpu_percent);
        systemChart.data.datasets[1].data.push(system.memory_percent);

        if (systemChart.data.labels.length > maxPoints) {
          systemChart.data.labels.shift();
          systemChart.data.datasets[0].data.shift();
          systemChart.data.datasets[1].data.shift();
        }

        systemChart.update('none');

        // Actualizar chart de aplicación
        appChart.data.labels.push(now);
        appChart.data.datasets[0].data.push(application.requests_per_second);
        appChart.data.datasets[1].data.push(
          application.avg_response_time * 1000
        );

        if (appChart.data.labels.length > maxPoints) {
          appChart.data.labels.shift();
          appChart.data.datasets[0].data.shift();
          appChart.data.datasets[1].data.shift();
        }

        appChart.update('none');
      }

      function updateLastUpdated() {
        const now = new Date().toLocaleString();
        document.getElementById(
          'last-updated'
        ).textContent = `Last updated: ${now}`;
      }

      function toggleAutoRefresh() {
        autoRefresh = !autoRefresh;
        const statusElement = document.getElementById('refresh-status');
        const button = event.target.closest('button');

        if (autoRefresh) {
          statusElement.textContent = 'ON';
          button.classList.add('active');
          startAutoRefresh();
        } else {
          statusElement.textContent = 'OFF';
          button.classList.remove('active');
          stopAutoRefresh();
        }
      }

      function refreshData() {
        fetchDashboardData();
      }

      async function toggleProfiling() {
        try {
          const endpoint = profilingEnabled
            ? '/monitoring/profiling/disable'
            : '/monitoring/profiling/enable';
          const response = await fetch(endpoint, { method: 'POST' });
          const result = await response.json();

          if (result.status === 'success') {
            profilingEnabled = !profilingEnabled;
            document.getElementById('profiling-status').textContent =
              profilingEnabled ? 'Disable' : 'Enable';
          }
        } catch (error) {
          console.error('Error toggling profiling:', error);
        }
      }

      function startAutoRefresh() {
        if (refreshInterval) return;

        refreshInterval = setInterval(() => {
          if (autoRefresh) {
            fetchDashboardData();
          }
        }, 5000); // Refresh cada 5 segundos
      }

      function stopAutoRefresh() {
        if (refreshInterval) {
          clearInterval(refreshInterval);
          refreshInterval = null;
        }
      }

      // Inicializar dashboard
      document.addEventListener('DOMContentLoaded', () => {
        fetchDashboardData();
        startAutoRefresh();
      });
    </script>
  </body>
</html>
```

### 4.2 Endpoint para dashboard

Agregar a `app/routers/monitoring.py`:

```python
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def monitoring_dashboard(request: Request):
    """Mostrar dashboard de monitoring."""
    return templates.TemplateResponse("dashboard.html", {"request": request})
```

## Paso 5: Integración y Testing

### 5.1 Actualizar main.py

Actualizar `app/main.py` para incluir monitoring:

```python
import redis
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
# ... otros imports ...

from app.monitoring.metrics_collector import MetricsCollector, AlertManager
from app.monitoring.auto_monitor import AutoMonitor
from app.routers import monitoring
from app.routers.monitoring import set_monitoring_dependencies

# ... configuración existente ...

# Configurar monitoring
metrics_collector = MetricsCollector(redis_client)
alert_manager = AlertManager(redis_client)
set_monitoring_dependencies(metrics_collector, alert_manager)

# Auto monitor
auto_monitor = AutoMonitor(metrics_collector, alert_manager, metrics_middleware)

# Event handlers
@app.on_event("startup")
async def startup_event():
    """Inicializar servicios al arrancar."""
    await auto_monitor.start()
    logger.info("Application started with monitoring enabled")

@app.on_event("shutdown")
async def shutdown_event():
    """Limpiar recursos al cerrar."""
    await auto_monitor.stop()
    logger.info("Application shutdown complete")

# Incluir router de monitoring
app.include_router(monitoring.router)
```

### 5.2 Script de carga para testing

Crear archivo `scripts/load_test.py`:

```python
import asyncio
import aiohttp
import time
import random
from typing import List

async def generate_load(
    base_url: str = "http://localhost:8000",
    duration_minutes: int = 5,
    concurrent_users: int = 10,
    requests_per_user: int = 100
):
    """Generar carga para testing de monitoring."""

    endpoints = [
        "/",
        "/health",
        "/users",
        "/metrics/system",
        "/monitoring/dashboard"
    ]

    async def user_session(user_id: int, session: aiohttp.ClientSession):
        """Simular sesión de usuario."""
        print(f"👤 User {user_id} starting session")

        for i in range(requests_per_user):
            try:
                # Seleccionar endpoint aleatorio
                endpoint = random.choice(endpoints)

                # Pausa aleatoria entre requests
                await asyncio.sleep(random.uniform(0.1, 2.0))

                # Hacer request
                async with session.get(f"{base_url}{endpoint}") as response:
                    status = response.status
                    if i % 20 == 0:  # Log cada 20 requests
                        print(f"👤 User {user_id}: {endpoint} -> {status}")

            except Exception as e:
                print(f"👤 User {user_id} error: {e}")

        print(f"👤 User {user_id} session completed")

    # Configurar sesión HTTP
    connector = aiohttp.TCPConnector(limit=concurrent_users * 2)
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(
        connector=connector,
        timeout=timeout
    ) as session:

        print(f"🚀 Starting load test:")
        print(f"   Duration: {duration_minutes} minutes")
        print(f"   Concurrent users: {concurrent_users}")
        print(f"   Requests per user: {requests_per_user}")
        print(f"   Total requests: {concurrent_users * requests_per_user}")

        start_time = time.time()

        # Crear tareas para usuarios concurrentes
        tasks = [
            user_session(user_id, session)
            for user_id in range(concurrent_users)
        ]

        # Ejecutar todas las sesiones de usuario
        await asyncio.gather(*tasks)

        end_time = time.time()
        duration = end_time - start_time

        print(f"✅ Load test completed in {duration:.2f} seconds")
        print(f"   Average RPS: {(concurrent_users * requests_per_user) / duration:.2f}")

if __name__ == "__main__":
    asyncio.run(generate_load())
```

## Verificación

### ✅ Checklist de Verificación

- [ ] MetricsCollector recopilando métricas del sistema
- [ ] AlertManager verificando umbrales y disparando alertas
- [ ] Profiler funcionando para endpoints críticos
- [ ] Scheduler ejecutando tareas automáticas
- [ ] Dashboard web mostrando métricas en tiempo real
- [ ] Endpoints de monitoring respondiendo correctamente
- [ ] Auto-refresh del dashboard funcionando
- [ ] Alertas almacenándose en Redis
- [ ] Load testing generando métricas observables

### 🧪 Pruebas a Realizar

1. **Verificar dashboard:**

   ```bash
   # Abrir en navegador
   http://localhost:8000/monitoring/dashboard
   ```

2. **Ejecutar load test:**

   ```bash
   python scripts/load_test.py
   ```

3. **Verificar métricas:**

   ```bash
   curl http://localhost:8000/monitoring/system
   curl http://localhost:8000/monitoring/application
   ```

4. **Habilitar profiling:**
   ```bash
   curl -X POST http://localhost:8000/monitoring/profiling/enable
   ```

### 🔧 Troubleshooting

**Dashboard no carga:**

- Verificar que el directorio `templates` existe
- Verificar configuración de Jinja2Templates

**Métricas no se actualizan:**

- Verificar que auto_monitor esté iniciado
- Verificar logs del scheduler
- Verificar conexión a Redis

**Charts no muestran datos:**

- Verificar console de navegador para errores JavaScript
- Verificar que los endpoints de monitoring responden

### 📊 Análisis de Resultados

Durante y después del load testing:

1. **Observar dashboard** para ver cambios en tiempo real
2. **Verificar alertas** si se superan umbrales
3. **Analizar profiling** para identificar cuellos de botella
4. **Revisar logs** para errores o advertencias

### 🎯 Próximos Pasos

- Completar ejercicios y proyecto de la semana 7
- Configurar alertas avanzadas con notificaciones externas
- Implementar métricas custom para casos de uso específicos
- Optimizar configuración basada en resultados de monitoring

---

## Recursos Adicionales

- [Python psutil Documentation](https://psutil.readthedocs.io/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)
- [Redis Monitoring Best Practices](https://redis.io/docs/manual/admin/)
- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
