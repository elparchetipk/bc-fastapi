# Práctica 26: Monitoreo y APM (Application Performance Monitoring)

## Objetivo

Implementar un sistema completo de monitoreo y APM para observar, medir y optimizar el rendimiento de aplicaciones FastAPI en tiempo real.

## Duración Estimada

⏱️ **80 minutos**

- Preparación: 20 minutos
- Implementación: 45 minutos
- Configuración y pruebas: 15 minutos

## Requisitos Previos

- Aplicación FastAPI en funcionamiento
- Conocimientos básicos de métricas y logging
- Configuración de Redis y base de datos

## Conceptos Teóricos

### 1. Pilares del Observability

- **Logs**: Eventos discretos en el tiempo
- **Metrics**: Datos numéricos agregados
- **Traces**: Seguimiento de requests a través del sistema

### 2. Métricas Clave (Golden Signals)

- **Latency**: Tiempo de respuesta
- **Traffic**: Rate de requests
- **Errors**: Tasa de errores
- **Saturation**: Utilización de recursos

### 3. Herramientas de APM

- **Prometheus**: Métricas y alertas
- **Grafana**: Visualización
- **Jaeger**: Distributed tracing
- **ELK Stack**: Logs centralizados

## Implementación

### Paso 1: Configuración de Métricas con Prometheus

Primero, configuremos Prometheus para recopilar métricas:

```python
# app/monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import time
from functools import wraps
from typing import Optional

# Métricas principales
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)

DATABASE_CONNECTIONS = Gauge(
    'database_connections_active',
    'Active database connections'
)

CACHE_OPERATIONS = Counter(
    'cache_operations_total',
    'Total cache operations',
    ['operation', 'result']
)

MEMORY_USAGE = Gauge(
    'memory_usage_bytes',
    'Memory usage in bytes'
)

CPU_USAGE = Gauge(
    'cpu_usage_percent',
    'CPU usage percentage'
)

class MetricsCollector:
    def __init__(self):
        self.active_requests = 0

    def track_request(self, method: str, endpoint: str):
        """Decorador para trackear requests"""
        def decorator(func):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                start_time = time.time()
                self.active_requests += 1
                ACTIVE_CONNECTIONS.set(self.active_requests)

                status_code = 200
                try:
                    result = await func(*args, **kwargs)
                    return result
                except Exception as e:
                    status_code = 500
                    raise
                finally:
                    # Registrar métricas
                    duration = time.time() - start_time
                    REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
                    REQUEST_COUNT.labels(
                        method=method,
                        endpoint=endpoint,
                        status_code=status_code
                    ).inc()

                    self.active_requests -= 1
                    ACTIVE_CONNECTIONS.set(self.active_requests)

            return wrapper
        return decorator

    def track_cache_operation(self, operation: str, result: str):
        """Trackear operaciones de cache"""
        CACHE_OPERATIONS.labels(operation=operation, result=result).inc()

    def update_system_metrics(self):
        """Actualizar métricas del sistema"""
        import psutil

        # Memoria
        memory = psutil.virtual_memory()
        MEMORY_USAGE.set(memory.used)

        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        CPU_USAGE.set(cpu_percent)

# Instancia global
metrics_collector = MetricsCollector()
```

### Paso 2: Middleware de Monitoreo

Creemos un middleware para capturar automáticamente todas las métricas:

```python
# app/middleware/monitoring_middleware.py
from fastapi import Request, Response
import time
import uuid
import logging
from app.monitoring.metrics import metrics_collector, REQUEST_COUNT, REQUEST_DURATION
import asyncio

logger = logging.getLogger(__name__)

class MonitoringMiddleware:
    def __init__(self):
        self.active_requests = {}

    async def __call__(self, request: Request, call_next):
        # Generar ID único para la request
        request_id = str(uuid.uuid4())
        start_time = time.time()

        # Información de la request
        method = request.method
        path = request.url.path
        user_agent = request.headers.get("user-agent", "")

        # Agregar información al contexto
        request.state.request_id = request_id
        request.state.start_time = start_time

        # Log de inicio de request
        logger.info(
            f"Request started: {request_id} {method} {path}",
            extra={
                "request_id": request_id,
                "method": method,
                "path": path,
                "user_agent": user_agent,
                "timestamp": start_time
            }
        )

        # Trackear request activa
        self.active_requests[request_id] = {
            "method": method,
            "path": path,
            "start_time": start_time
        }

        status_code = 200
        exception_info = None

        try:
            # Procesar request
            response = await call_next(request)
            status_code = response.status_code

        except Exception as e:
            status_code = 500
            exception_info = str(e)
            logger.error(
                f"Request failed: {request_id}",
                extra={
                    "request_id": request_id,
                    "error": exception_info
                },
                exc_info=True
            )
            raise

        finally:
            # Calcular duración
            duration = time.time() - start_time

            # Registrar métricas
            REQUEST_COUNT.labels(
                method=method,
                endpoint=path,
                status_code=status_code
            ).inc()

            REQUEST_DURATION.labels(
                method=method,
                endpoint=path
            ).observe(duration)

            # Log de finalización
            logger.info(
                f"Request completed: {request_id}",
                extra={
                    "request_id": request_id,
                    "method": method,
                    "path": path,
                    "status_code": status_code,
                    "duration": duration,
                    "exception": exception_info
                }
            )

            # Limpiar request activa
            self.active_requests.pop(request_id, None)

            # Agregar headers de monitoreo
            if 'response' in locals():
                response.headers["X-Request-ID"] = request_id
                response.headers["X-Response-Time"] = f"{duration:.4f}"

        return response

    def get_active_requests(self):
        """Obtener información de requests activas"""
        current_time = time.time()
        return [
            {
                "request_id": req_id,
                "method": info["method"],
                "path": info["path"],
                "duration": current_time - info["start_time"]
            }
            for req_id, info in self.active_requests.items()
        ]

# Instancia global
monitoring_middleware = MonitoringMiddleware()
```

### Paso 3: Sistema de Logging Estructurado

Implementemos logging estructurado para mejor observabilidad:

```python
# app/monitoring/logging_config.py
import logging
import json
import sys
from datetime import datetime
from typing import Dict, Any

class StructuredLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.setup_logger()

    def setup_logger(self):
        """Configurar logger estructurado"""
        # Crear formatter personalizado
        formatter = StructuredFormatter()

        # Handler para stdout
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)

        # Handler para archivo
        file_handler = logging.FileHandler('app.log')
        file_handler.setFormatter(formatter)

        # Configurar logger
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    def info(self, message: str, **kwargs):
        """Log info con contexto adicional"""
        self.logger.info(message, extra=kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning con contexto adicional"""
        self.logger.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs):
        """Log error con contexto adicional"""
        self.logger.error(message, extra=kwargs)

class StructuredFormatter(logging.Formatter):
    def format(self, record):
        # Crear log entry estructurado
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Agregar contexto adicional si existe
        if hasattr(record, '__dict__'):
            for key, value in record.__dict__.items():
                if key not in ['name', 'msg', 'args', 'levelname', 'levelno',
                              'pathname', 'filename', 'module', 'lineno',
                              'funcName', 'created', 'msecs', 'relativeCreated',
                              'thread', 'threadName', 'processName', 'process',
                              'getMessage', 'exc_info', 'exc_text', 'stack_info']:
                    log_entry[key] = value

        return json.dumps(log_entry, default=str)

# Logger global para la aplicación
app_logger = StructuredLogger("fastapi_app")
```

### Paso 4: Health Checks y Endpoints de Monitoreo

```python
# app/routers/monitoring.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import psutil
import time
from app.database import get_db
from app.monitoring.metrics import metrics_collector
from app.monitoring.logging_config import app_logger
from app.cache.redis_client import cache

router = APIRouter(prefix="/monitoring", tags=["monitoring"])

@router.get("/health")
async def health_check():
    """Health check básico"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Health check detallado"""
    checks = {}
    overall_status = "healthy"

    # Check database
    try:
        db.execute("SELECT 1")
        checks["database"] = {"status": "healthy", "response_time": 0.001}
    except Exception as e:
        checks["database"] = {"status": "unhealthy", "error": str(e)}
        overall_status = "unhealthy"

    # Check Redis
    try:
        start_time = time.time()
        cache.client.ping()
        response_time = time.time() - start_time
        checks["redis"] = {"status": "healthy", "response_time": response_time}
    except Exception as e:
        checks["redis"] = {"status": "unhealthy", "error": str(e)}
        overall_status = "degraded" if overall_status == "healthy" else "unhealthy"

    # Check system resources
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    checks["system"] = {
        "memory_usage": memory.percent,
        "disk_usage": disk.percent,
        "cpu_usage": psutil.cpu_percent(interval=1)
    }

    # Determinar status general basado en recursos
    if memory.percent > 90 or disk.percent > 90:
        overall_status = "degraded" if overall_status == "healthy" else overall_status

    return {
        "status": overall_status,
        "timestamp": time.time(),
        "checks": checks
    }

@router.get("/metrics")
async def get_metrics():
    """Endpoint para métricas de Prometheus"""
    # Actualizar métricas del sistema
    metrics_collector.update_system_metrics()

    # Generar métricas en formato Prometheus
    metrics_data = generate_latest()
    return Response(
        content=metrics_data,
        media_type=CONTENT_TYPE_LATEST
    )

@router.get("/stats/requests")
async def get_request_stats():
    """Estadísticas de requests"""
    active_requests = monitoring_middleware.get_active_requests()

    return {
        "active_requests": len(active_requests),
        "active_requests_details": active_requests,
        "timestamp": time.time()
    }

@router.get("/stats/system")
async def get_system_stats():
    """Estadísticas del sistema"""
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    cpu_times = psutil.cpu_times()

    return {
        "memory": {
            "total": memory.total,
            "used": memory.used,
            "free": memory.free,
            "percent": memory.percent
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        },
        "cpu": {
            "percent": psutil.cpu_percent(interval=1),
            "user_time": cpu_times.user,
            "system_time": cpu_times.system,
            "idle_time": cpu_times.idle
        },
        "timestamp": time.time()
    }

@router.get("/logs/recent")
async def get_recent_logs(limit: int = 100):
    """Obtener logs recientes"""
    try:
        with open('app.log', 'r') as f:
            lines = f.readlines()
            recent_lines = lines[-limit:] if len(lines) > limit else lines

            # Parsear logs JSON
            logs = []
            for line in recent_lines:
                try:
                    log_entry = json.loads(line.strip())
                    logs.append(log_entry)
                except:
                    # Si no es JSON válido, agregar como texto plano
                    logs.append({"message": line.strip(), "raw": True})

            return {"logs": logs, "count": len(logs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading logs: {str(e)}")
```

### Paso 5: Dashboard Básico con FastAPI

Creemos un dashboard simple para visualizar métricas:

```python
# app/routers/dashboard.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def dashboard_home(request: Request):
    """Dashboard principal"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/metrics", response_class=HTMLResponse)
async def metrics_dashboard(request: Request):
    """Dashboard de métricas"""
    return templates.TemplateResponse("metrics.html", {"request": request})
```

Dashboard HTML template:

```html
<!-- templates/dashboard.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>FastAPI Monitoring Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 20px;
      }
      .container {
        max-width: 1200px;
        margin: 0 auto;
      }
      .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
      }
      .metric-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        background: #f9f9f9;
      }
      .metric-value {
        font-size: 2em;
        font-weight: bold;
        color: #2e7d32;
      }
      .metric-label {
        color: #666;
        margin-bottom: 10px;
      }
      .status-healthy {
        color: #2e7d32;
      }
      .status-degraded {
        color: #f57c00;
      }
      .status-unhealthy {
        color: #d32f2f;
      }
      .chart-container {
        height: 300px;
        margin-top: 20px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>FastAPI Monitoring Dashboard</h1>

      <div id="health-status">
        <h2>System Health</h2>
        <div id="health-indicator">Loading...</div>
      </div>

      <div class="metrics-grid">
        <div class="metric-card">
          <div class="metric-label">Active Requests</div>
          <div
            class="metric-value"
            id="active-requests">
            -
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-label">Memory Usage</div>
          <div
            class="metric-value"
            id="memory-usage">
            -
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-label">CPU Usage</div>
          <div
            class="metric-value"
            id="cpu-usage">
            -
          </div>
        </div>

        <div class="metric-card">
          <div class="metric-label">Disk Usage</div>
          <div
            class="metric-value"
            id="disk-usage">
            -
          </div>
        </div>
      </div>

      <div class="chart-container">
        <canvas id="requestsChart"></canvas>
      </div>
    </div>

    <script>
      // Variables globales
      let requestsChart;
      let requestsData = [];

      // Función para actualizar métricas
      async function updateMetrics() {
        try {
          // Health check
          const healthResponse = await fetch('/monitoring/health/detailed');
          const healthData = await healthResponse.json();

          const healthIndicator = document.getElementById('health-indicator');
          healthIndicator.textContent = `Status: ${healthData.status}`;
          healthIndicator.className = `status-${healthData.status}`;

          // System stats
          const statsResponse = await fetch('/monitoring/stats/system');
          const statsData = await statsResponse.json();

          document.getElementById(
            'memory-usage'
          ).textContent = `${statsData.memory.percent.toFixed(1)}%`;
          document.getElementById(
            'cpu-usage'
          ).textContent = `${statsData.cpu.percent.toFixed(1)}%`;
          document.getElementById(
            'disk-usage'
          ).textContent = `${statsData.disk.percent.toFixed(1)}%`;

          // Request stats
          const requestsResponse = await fetch('/monitoring/stats/requests');
          const requestsStats = await requestsResponse.json();

          document.getElementById('active-requests').textContent =
            requestsStats.active_requests;

          // Actualizar gráfico
          updateChart(requestsStats.active_requests);
        } catch (error) {
          console.error('Error updating metrics:', error);
        }
      }

      // Función para actualizar gráfico
      function updateChart(activeRequests) {
        const now = new Date();
        requestsData.push({
          time: now.toLocaleTimeString(),
          requests: activeRequests,
        });

        // Mantener solo los últimos 20 puntos
        if (requestsData.length > 20) {
          requestsData.shift();
        }

        requestsChart.data.labels = requestsData.map((d) => d.time);
        requestsChart.data.datasets[0].data = requestsData.map(
          (d) => d.requests
        );
        requestsChart.update();
      }

      // Inicializar gráfico
      function initChart() {
        const ctx = document.getElementById('requestsChart').getContext('2d');
        requestsChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: [],
            datasets: [
              {
                label: 'Active Requests',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1,
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
              },
            },
          },
        });
      }

      // Inicializar dashboard
      document.addEventListener('DOMContentLoaded', function () {
        initChart();
        updateMetrics();

        // Actualizar cada 5 segundos
        setInterval(updateMetrics, 5000);
      });
    </script>
  </body>
</html>
```

### Paso 6: Configuración de Alertas

```python
# app/monitoring/alerting.py
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from typing import List, Dict, Any
import asyncio
from app.monitoring.logging_config import app_logger

class AlertManager:
    def __init__(self):
        self.thresholds = {
            "memory_usage": 85.0,
            "cpu_usage": 80.0,
            "disk_usage": 90.0,
            "error_rate": 5.0,
            "response_time": 2.0
        }
        self.alert_cooldown = {}  # Para evitar spam de alertas

    async def check_system_health(self, stats: Dict[str, Any]):
        """Verificar salud del sistema y enviar alertas si es necesario"""
        alerts = []

        # Check memory
        if stats["memory"]["percent"] > self.thresholds["memory_usage"]:
            alerts.append({
                "type": "memory",
                "severity": "warning",
                "message": f"High memory usage: {stats['memory']['percent']:.1f}%",
                "value": stats["memory"]["percent"],
                "threshold": self.thresholds["memory_usage"]
            })

        # Check CPU
        if stats["cpu"]["percent"] > self.thresholds["cpu_usage"]:
            alerts.append({
                "type": "cpu",
                "severity": "warning",
                "message": f"High CPU usage: {stats['cpu']['percent']:.1f}%",
                "value": stats["cpu"]["percent"],
                "threshold": self.thresholds["cpu_usage"]
            })

        # Check disk
        if stats["disk"]["percent"] > self.thresholds["disk_usage"]:
            alerts.append({
                "type": "disk",
                "severity": "critical",
                "message": f"High disk usage: {stats['disk']['percent']:.1f}%",
                "value": stats["disk"]["percent"],
                "threshold": self.thresholds["disk_usage"]
            })

        # Procesar alertas
        for alert in alerts:
            await self.process_alert(alert)

        return alerts

    async def process_alert(self, alert: Dict[str, Any]):
        """Procesar una alerta individual"""
        alert_key = f"{alert['type']}_{alert['severity']}"
        current_time = time.time()

        # Verificar cooldown (5 minutos)
        if alert_key in self.alert_cooldown:
            if current_time - self.alert_cooldown[alert_key] < 300:
                return  # Alerta en cooldown

        # Log de la alerta
        app_logger.warning(
            f"Alert triggered: {alert['message']}",
            alert_type=alert["type"],
            severity=alert["severity"],
            value=alert["value"],
            threshold=alert["threshold"]
        )

        # Enviar notificación (implementar según necesidades)
        await self.send_notification(alert)

        # Actualizar cooldown
        self.alert_cooldown[alert_key] = current_time

    async def send_notification(self, alert: Dict[str, Any]):
        """Enviar notificación de alerta"""
        # Aquí se puede implementar envío de email, Slack, etc.
        # Por ahora solo log
        app_logger.info(
            f"Alert notification sent for {alert['type']}: {alert['message']}"
        )

# Instancia global
alert_manager = AlertManager()
```

## Ejercicios Prácticos

### Ejercicio 1: Configuración Básica

1. Configura Prometheus y métricas básicas
2. Implementa middleware de monitoreo
3. Crea endpoints de health check
4. Prueba la recopilación de métricas

### Ejercicio 2: Dashboard Personalizado

1. Implementa el dashboard HTML
2. Añade métricas personalizadas
3. Crea gráficos en tiempo real
4. Implementa alertas visuales

### Ejercicio 3: Monitoreo Avanzado

1. Configura logging estructurado
2. Implementa distributed tracing
3. Crea alertas automáticas
4. Integra con herramientas externas

## Métricas de Evaluación

### ✅ Checklist de Completitud

- [ ] Configuraste métricas de Prometheus
- [ ] Implementaste middleware de monitoreo
- [ ] Creaste health checks detallados
- [ ] Implementaste logging estructurado
- [ ] Creaste dashboard de monitoreo
- [ ] Configuraste alertas automáticas
- [ ] Documentaste todas las métricas

### 📊 Indicadores de Rendimiento

- **Cobertura de métricas**: Todas las funciones críticas monitoreadas
- **Tiempo de detección**: Alertas en <1 minuto
- **Dashboard útil**: Información clara y accionable
- **Logs estructurados**: Fácil búsqueda y análisis

## Troubleshooting

### Problema: Métricas no aparecen

```python
# Verificar que Prometheus esté funcionando
from prometheus_client import generate_latest
print(generate_latest().decode())

# Verificar configuración
metrics_collector.update_system_metrics()
```

### Problema: Alto overhead de monitoreo

```python
# Usar sampling para requests de alto volumen
import random

if random.random() < 0.1:  # Solo 10% de las requests
    # Aplicar monitoreo detallado
    pass
```

### Problema: Logs demasiado verbosos

```python
# Configurar niveles de logging apropiados
logging.getLogger("fastapi").setLevel(logging.WARNING)
logging.getLogger("uvicorn").setLevel(logging.INFO)
```

## Recursos Adicionales

- [Prometheus Documentation](https://prometheus.io/docs/)
- [OpenTelemetry](https://opentelemetry.io/)
- [The RED Method](https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/)
- [The USE Method](http://www.brendangregg.com/usemethod.html)

## Próximos Pasos

Con el sistema de monitoreo implementado, podrás:

- Detectar problemas de rendimiento proactivamente
- Optimizar recursos basándote en datos reales
- Implementar alertas automáticas
- Crear dashboards para stakeholders
