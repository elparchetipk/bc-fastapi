# Ejercicios Detallados - API Avanzada

## 🏃‍♂️ Ejercicio 1: WebSocket Echo Server (30 min)

### **Objetivo**

Crear un servidor WebSocket que haga eco de mensajes con funcionalidades adicionales.

### **Requisitos**

- Echo server básico que devuelve mensajes
- Contador de mensajes por conexión
- Timestamps en respuestas
- Manejo de comandos especiales

### **Especificaciones**

```python
# Comandos especiales a implementar:
# /stats - Devolver estadísticas de la conexión
# /time - Devolver hora actual
# /count - Devolver número de mensajes enviados
# /clear - Limpiar contador (responder con confirmación)
```

### **Estructura esperada**

```text
ejercicio1/
├── main.py
├── websocket_server.py
├── client_test.html
├── README.md
└── tests/
    └── test_echo_server.py
```

### **Código base**

```python
# websocket_server.py - Completar implementación
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from datetime import datetime
import json

app = FastAPI()

class EchoConnection:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.message_count = 0
        self.connected_at = datetime.utcnow()

    async def send_message(self, message: str):
        """Enviar mensaje al cliente"""
        # TODO: Implementar
        pass

    async def handle_command(self, command: str):
        """Manejar comandos especiales"""
        # TODO: Implementar comandos /stats, /time, /count, /clear
        pass

@app.websocket("/echo")
async def websocket_endpoint(websocket: WebSocket):
    # TODO: Implementar lógica del echo server
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### **Cliente de prueba**

```html
<!-- client_test.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Echo Server Test</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 20px;
      }
      #messages {
        border: 1px solid #ccc;
        height: 300px;
        overflow-y: auto;
        padding: 10px;
        margin: 10px 0;
      }
      input[type='text'] {
        width: 70%;
        padding: 5px;
      }
      button {
        padding: 5px 10px;
      }
      .message {
        margin: 5px 0;
      }
      .sent {
        color: blue;
      }
      .received {
        color: green;
      }
      .error {
        color: red;
      }
    </style>
  </head>
  <body>
    <h1>WebSocket Echo Server Test</h1>
    <div id="messages"></div>
    <input
      type="text"
      id="messageInput"
      placeholder="Escribe un mensaje o comando..." />
    <button onclick="sendMessage()">Enviar</button>
    <button onclick="connect()">Conectar</button>
    <button onclick="disconnect()">Desconectar</button>

    <div>
      <h3>Comandos disponibles:</h3>
      <ul>
        <li>/stats - Ver estadísticas</li>
        <li>/time - Ver hora actual</li>
        <li>/count - Ver contador de mensajes</li>
        <li>/clear - Limpiar contador</li>
      </ul>
    </div>

    <script>
      let ws = null;

      function connect() {
        // TODO: Implementar conexión WebSocket
      }

      function disconnect() {
        // TODO: Implementar desconexión
      }

      function sendMessage() {
        // TODO: Implementar envío de mensajes
      }

      function addMessage(message, type = 'received') {
        // TODO: Implementar display de mensajes
      }
    </script>
  </body>
</html>
```

### **Tests esperados**

```python
# tests/test_echo_server.py
import pytest
from fastapi.testclient import TestClient
from websocket_server import app

client = TestClient(app)

def test_websocket_echo():
    """Test básico de echo"""
    with client.websocket_connect("/echo") as websocket:
        websocket.send_text("Hola mundo")
        data = websocket.receive_text()
        # TODO: Verificar que el eco funciona correctamente

def test_websocket_commands():
    """Test de comandos especiales"""
    with client.websocket_connect("/echo") as websocket:
        # TODO: Probar comandos /stats, /time, /count, /clear
        pass

def test_websocket_multiple_messages():
    """Test de múltiples mensajes"""
    # TODO: Verificar contador de mensajes
    pass
```

---

## 📧 Ejercicio 2: Sistema de Notificaciones (45 min)

### **Objetivo**

Implementar un sistema completo de notificaciones con Background Tasks.

### **Requisitos**

- Envío de notificaciones por email (simulado)
- Cola de notificaciones con prioridades
- Dashboard para ver notificaciones pendientes
- API para crear y gestionar notificaciones

### **Estructura esperada**

```text
ejercicio2/
├── main.py
├── models.py
├── notification_service.py
├── background_tasks.py
├── dashboard.html
├── requirements.txt
└── tests/
    └── test_notifications.py
```

### **Modelos base**

```python
# models.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from enum import Enum

Base = declarative_base()

class NotificationPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    recipient_email = Column(String(255), nullable=False)
    subject = Column(String(500), nullable=False)
    body = Column(Text, nullable=False)
    priority = Column(String(20), default=NotificationPriority.MEDIUM)
    status = Column(String(20), default="pending")  # pending, sent, failed
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime, nullable=True)
    attempts = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)

# TODO: Implementar otros modelos necesarios
```

### **Servicio de notificaciones**

```python
# notification_service.py
from fastapi import BackgroundTasks
import asyncio
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self):
        self.queue = asyncio.PriorityQueue()
        self.processing = False

    async def add_notification(self, notification_data: dict):
        """Agregar notificación a la cola"""
        # TODO: Implementar priorización y encolado
        pass

    async def process_queue(self):
        """Procesar cola de notificaciones"""
        # TODO: Implementar procesamiento en background
        pass

    async def send_email(self, notification):
        """Enviar email (simulado)"""
        # TODO: Implementar envío de email simulado
        # Usar logging para simular envío
        pass

    def get_stats(self):
        """Obtener estadísticas del servicio"""
        # TODO: Implementar estadísticas
        pass

# Instancia global
notification_service = NotificationService()
```

### **API endpoints**

```python
# main.py - Completar implementación
from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from notification_service import notification_service

app = FastAPI()

class NotificationCreate(BaseModel):
    recipient_email: str
    subject: str
    body: str
    priority: str = "medium"

@app.post("/notifications/")
async def create_notification(
    notification: NotificationCreate,
    background_tasks: BackgroundTasks
):
    """Crear nueva notificación"""
    # TODO: Implementar creación y encolado
    pass

@app.get("/notifications/stats")
async def get_notification_stats():
    """Obtener estadísticas"""
    # TODO: Implementar estadísticas
    pass

@app.get("/notifications/queue")
async def get_queue_status():
    """Ver estado de la cola"""
    # TODO: Implementar vista de cola
    pass

# TODO: Implementar más endpoints según necesidad
```

### **Dashboard**

```html
<!-- dashboard.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Notification Dashboard</title>
    <style>
      /* TODO: Implementar estilos para dashboard */
    </style>
  </head>
  <body>
    <h1>Sistema de Notificaciones</h1>

    <!-- Formulario para crear notificación -->
    <div>
      <h2>Crear Notificación</h2>
      <!-- TODO: Implementar formulario -->
    </div>

    <!-- Estadísticas -->
    <div>
      <h2>Estadísticas</h2>
      <div id="stats">
        <!-- TODO: Mostrar estadísticas en tiempo real -->
      </div>
    </div>

    <!-- Cola de notificaciones -->
    <div>
      <h2>Cola de Notificaciones</h2>
      <div id="queue">
        <!-- TODO: Mostrar notificaciones pendientes -->
      </div>
    </div>

    <script>
      // TODO: Implementar JavaScript para dashboard interactivo
    </script>
  </body>
</html>
```

---

## 📊 Ejercicio 3: Monitor de Sistema SSE (45 min)

### **Objetivo**

Crear un monitor de sistema en tiempo real usando Server-Sent Events.

### **Requisitos**

- Monitorear CPU, memoria y disco
- Stream de eventos SSE con métricas
- Dashboard con gráficos en tiempo real
- Alertas cuando se superan umbrales

### **Estructura esperada**

```text
ejercicio3/
├── main.py
├── system_monitor.py
├── sse_endpoints.py
├── static/
│   ├── monitor.html
│   ├── monitor.js
│   └── chart.min.js  # Chart.js library
├── requirements.txt
└── tests/
    └── test_monitor.py
```

### **Monitor de sistema**

```python
# system_monitor.py
import psutil
import asyncio
from datetime import datetime
from typing import Dict, Any
import json

class SystemMonitor:
    def __init__(self):
        self.thresholds = {
            "cpu": 80.0,      # 80%
            "memory": 85.0,   # 85%
            "disk": 90.0      # 90%
        }
        self.history = []
        self.max_history = 100

    def get_current_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas actuales del sistema"""
        # TODO: Implementar usando psutil
        # Retornar: CPU%, memoria%, disco%, red, procesos
        pass

    def check_alerts(self, stats: Dict[str, Any]) -> list:
        """Verificar si hay alertas"""
        # TODO: Comparar con umbrales y generar alertas
        pass

    def add_to_history(self, stats: Dict[str, Any]):
        """Agregar estadísticas al historial"""
        # TODO: Implementar historial circular
        pass

    async def start_monitoring(self, callback=None):
        """Iniciar monitoreo continuo"""
        # TODO: Loop de monitoreo que llame callback con nuevos datos
        pass

# Instancia global
system_monitor = SystemMonitor()
```

### **SSE Endpoints**

```python
# sse_endpoints.py
from fastapi import Request
from fastapi.responses import StreamingResponse
from system_monitor import system_monitor
import asyncio
import json

async def system_stats_stream(request: Request):
    """Stream SSE de estadísticas del sistema"""

    async def event_generator():
        """Generador de eventos SSE"""
        try:
            while True:
                # Verificar si cliente se desconectó
                if await request.is_disconnected():
                    break

                # TODO: Obtener estadísticas actuales
                # TODO: Verificar alertas
                # TODO: Enviar evento SSE

                await asyncio.sleep(2)  # Actualizar cada 2 segundos

        except Exception as e:
            print(f"Error en stream: {e}")

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )

# TODO: Implementar más endpoints SSE según necesidad
```

### **Dashboard con gráficos**

```html
<!-- static/monitor.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>System Monitor</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 20px;
        background: #f5f5f5;
      }
      .container {
        max-width: 1200px;
        margin: 0 auto;
      }
      .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin-bottom: 20px;
      }
      .metric-card {
        background: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      .chart-container {
        position: relative;
        height: 200px;
      }
      .alerts {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 20px;
      }
      .alert-item {
        color: #856404;
        margin: 5px 0;
      }
      .status {
        padding: 5px 10px;
        border-radius: 4px;
        font-weight: bold;
      }
      .status.connected {
        background: #d4edda;
        color: #155724;
      }
      .status.disconnected {
        background: #f8d7da;
        color: #721c24;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>Monitor de Sistema en Tiempo Real</h1>

      <div class="status-bar">
        <span>Estado: </span>
        <span
          id="connectionStatus"
          class="status disconnected"
          >Desconectado</span
        >
        <span style="margin-left: 20px;">Última actualización: </span>
        <span id="lastUpdate">--</span>
      </div>

      <div
        id="alerts"
        class="alerts"
        style="display: none;">
        <h3>🚨 Alertas Activas</h3>
        <div id="alertList"></div>
      </div>

      <div class="metrics-grid">
        <div class="metric-card">
          <h3>CPU Usage</h3>
          <div class="chart-container">
            <canvas id="cpuChart"></canvas>
          </div>
        </div>

        <div class="metric-card">
          <h3>Memory Usage</h3>
          <div class="chart-container">
            <canvas id="memoryChart"></canvas>
          </div>
        </div>

        <div class="metric-card">
          <h3>Disk Usage</h3>
          <div class="chart-container">
            <canvas id="diskChart"></canvas>
          </div>
        </div>

        <div class="metric-card">
          <h3>Network I/O</h3>
          <div class="chart-container">
            <canvas id="networkChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <script>
      // TODO: Implementar JavaScript para:
      // - Conexión SSE
      // - Actualización de gráficos
      // - Manejo de alertas
      // - Configuración de Chart.js

      class SystemMonitorDashboard {
        constructor() {
          this.eventSource = null;
          this.charts = {};
          this.init();
        }

        init() {
          // TODO: Inicializar dashboard
        }

        connectSSE() {
          // TODO: Conectar a stream SSE
        }

        initCharts() {
          // TODO: Inicializar gráficos Chart.js
        }

        updateCharts(data) {
          // TODO: Actualizar gráficos con nuevos datos
        }

        showAlerts(alerts) {
          // TODO: Mostrar alertas en UI
        }
      }

      // Inicializar dashboard
      document.addEventListener('DOMContentLoaded', () => {
        new SystemMonitorDashboard();
      });
    </script>
  </body>
</html>
```

---

## 🛡️ Ejercicio 4: Chat con Moderación (60 min)

### **Objetivo**

Crear un sistema de chat con moderación automática y manual.

### **Requisitos**

- Filtro de palabras prohibidas
- Sistema de reportes de usuarios
- Panel de moderación en tiempo real
- Acciones automatizadas (mute, ban temporal)
- Logs de moderación

### **Características del sistema**

- **Moderación automática**: Filtro de contenido en tiempo real
- **Moderación manual**: Panel para moderadores
- **Sistema de reportes**: Los usuarios pueden reportar mensajes
- **Acciones**: Advertencias, mute temporal, ban temporal/permanente
- **Auditoría**: Log completo de acciones de moderación

### **Estructura esperada**

```text
ejercicio4/
├── main.py
├── models/
│   ├── __init__.py
│   ├── chat.py
│   ├── moderation.py
│   └── user.py
├── services/
│   ├── __init__.py
│   ├── chat_service.py
│   ├── moderation_service.py
│   └── filter_service.py
├── routers/
│   ├── __init__.py
│   ├── chat.py
│   └── moderation.py
├── static/
│   ├── chat.html
│   ├── moderation.html
│   └── js/
│       ├── chat.js
│       └── moderation.js
├── config/
│   └── banned_words.txt
├── requirements.txt
└── tests/
    ├── test_chat.py
    ├── test_moderation.py
    └── test_filters.py
```

### **Modelos de moderación**

```python
# models/moderation.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
from enum import Enum

class ModerationAction(str, Enum):
    WARNING = "warning"
    MUTE = "mute"
    TEMPORARY_BAN = "temporary_ban"
    PERMANENT_BAN = "permanent_ban"
    MESSAGE_DELETE = "message_delete"

class ReportReason(str, Enum):
    SPAM = "spam"
    HARASSMENT = "harassment"
    INAPPROPRIATE_CONTENT = "inappropriate_content"
    HATE_SPEECH = "hate_speech"
    OTHER = "other"

class UserModerationStatus(Base):
    __tablename__ = "user_moderation_status"

    # TODO: Implementar modelo completo
    pass

class MessageReport(Base):
    __tablename__ = "message_reports"

    # TODO: Implementar modelo de reportes
    pass

class ModerationLog(Base):
    __tablename__ = "moderation_logs"

    # TODO: Implementar log de moderación
    pass

class BannedWord(Base):
    __tablename__ = "banned_words"

    # TODO: Implementar lista de palabras prohibidas
    pass
```

### **Servicio de filtros**

```python
# services/filter_service.py
import re
from typing import List, Dict, Tuple
from models.moderation import BannedWord
from sqlalchemy.orm import Session

class ContentFilter:
    def __init__(self):
        self.banned_words = set()
        self.load_banned_words()

    def load_banned_words(self):
        """Cargar palabras prohibidas desde archivo y DB"""
        # TODO: Cargar desde config/banned_words.txt
        # TODO: Cargar desde base de datos
        pass

    def check_message(self, content: str) -> Dict[str, any]:
        """Verificar si el mensaje contiene contenido prohibido"""
        # TODO: Implementar verificación
        # Retornar: {
        #   "is_clean": bool,
        #   "violations": List[str],
        #   "severity": str,  # low, medium, high
        #   "suggested_action": str
        # }
        pass

    def clean_message(self, content: str) -> str:
        """Limpiar mensaje reemplazando palabras prohibidas"""
        # TODO: Reemplazar palabras prohibidas con ***
        pass

    def add_banned_word(self, word: str, severity: str = "medium"):
        """Agregar palabra a la lista prohibida"""
        # TODO: Implementar
        pass

content_filter = ContentFilter()
```

### **Servicio de moderación**

```python
# services/moderation_service.py
from datetime import datetime, timedelta
from models.moderation import ModerationAction, UserModerationStatus, ModerationLog
from services.filter_service import content_filter
import asyncio

class ModerationService:
    def __init__(self):
        self.active_moderators = set()

    async def moderate_message(self, message_id: int, user_id: int, content: str):
        """Moderar mensaje automáticamente"""
        # TODO: Usar content_filter para verificar contenido
        # TODO: Aplicar acciones automáticas según severidad
        # TODO: Notificar moderadores si es necesario
        pass

    async def apply_action(
        self,
        user_id: int,
        action: ModerationAction,
        duration: timedelta = None,
        reason: str = "",
        moderator_id: int = None
    ):
        """Aplicar acción de moderación"""
        # TODO: Implementar aplicación de acciones
        # TODO: Registrar en log de moderación
        # TODO: Notificar al usuario afectado
        pass

    def is_user_muted(self, user_id: int) -> bool:
        """Verificar si usuario está silenciado"""
        # TODO: Implementar verificación
        pass

    def is_user_banned(self, user_id: int) -> bool:
        """Verificar si usuario está baneado"""
        # TODO: Implementar verificación
        pass

    async def process_report(self, report_id: int):
        """Procesar reporte de usuario"""
        # TODO: Implementar procesamiento de reportes
        # TODO: Notificar moderadores
        pass

    def get_moderation_stats(self) -> Dict:
        """Obtener estadísticas de moderación"""
        # TODO: Implementar estadísticas
        pass

moderation_service = ModerationService()
```

### **Panel de moderación**

```html
<!-- static/moderation.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Panel de Moderación</title>
    <style>
      /* TODO: Implementar estilos para panel de moderación */
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        background: #f8f9fa;
      }
      .header {
        background: #dc3545;
        color: white;
        padding: 15px;
      }
      .container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
      }
      .tabs {
        display: flex;
        background: white;
        border-radius: 8px 8px 0 0;
      }
      .tab {
        padding: 15px 20px;
        cursor: pointer;
        border-bottom: 3px solid transparent;
      }
      .tab.active {
        border-bottom-color: #dc3545;
        background: #f8f9fa;
      }
      .tab-content {
        background: white;
        min-height: 500px;
        padding: 20px;
        border-radius: 0 0 8px 8px;
      }
      /* Más estilos... */
    </style>
  </head>
  <body>
    <div class="header">
      <h1>🛡️ Panel de Moderación</h1>
      <div>Moderador: <span id="moderatorName">--</span></div>
    </div>

    <div class="container">
      <div class="tabs">
        <div
          class="tab active"
          onclick="showTab('reports')">
          Reportes Pendientes
        </div>
        <div
          class="tab"
          onclick="showTab('logs')">
          Logs de Moderación
        </div>
        <div
          class="tab"
          onclick="showTab('users')">
          Usuarios
        </div>
        <div
          class="tab"
          onclick="showTab('words')">
          Palabras Prohibidas
        </div>
        <div
          class="tab"
          onclick="showTab('stats')">
          Estadísticas
        </div>
      </div>

      <div class="tab-content">
        <!-- Reportes pendientes -->
        <div
          id="reports"
          class="tab-pane active">
          <h2>Reportes Pendientes</h2>
          <div id="reportsList">
            <!-- TODO: Lista de reportes -->
          </div>
        </div>

        <!-- Logs de moderación -->
        <div
          id="logs"
          class="tab-pane">
          <h2>Historial de Moderación</h2>
          <div id="logsList">
            <!-- TODO: Lista de logs -->
          </div>
        </div>

        <!-- Gestión de usuarios -->
        <div
          id="users"
          class="tab-pane">
          <h2>Gestión de Usuarios</h2>
          <div id="usersList">
            <!-- TODO: Lista de usuarios con acciones -->
          </div>
        </div>

        <!-- Palabras prohibidas -->
        <div
          id="words"
          class="tab-pane">
          <h2>Palabras Prohibidas</h2>
          <div id="wordsList">
            <!-- TODO: Gestión de palabras prohibidas -->
          </div>
        </div>

        <!-- Estadísticas -->
        <div
          id="stats"
          class="tab-pane">
          <h2>Estadísticas de Moderación</h2>
          <div id="statsContent">
            <!-- TODO: Gráficos y estadísticas -->
          </div>
        </div>
      </div>
    </div>

    <script>
      // TODO: Implementar JavaScript para panel de moderación
      class ModerationPanel {
        constructor() {
          this.init();
        }

        init() {
          // TODO: Inicializar panel
          this.loadReports();
          this.setupEventListeners();
        }

        loadReports() {
          // TODO: Cargar reportes pendientes
        }

        processReport(reportId, action) {
          // TODO: Procesar reporte
        }

        applyModerationAction(userId, action, duration = null) {
          // TODO: Aplicar acción de moderación
        }

        loadModerationLogs() {
          // TODO: Cargar logs de moderación
        }

        setupEventListeners() {
          // TODO: Configurar event listeners
        }
      }

      function showTab(tabName) {
        // TODO: Implementar cambio de tabs
      }

      // Inicializar panel
      document.addEventListener('DOMContentLoaded', () => {
        new ModerationPanel();
      });
    </script>
  </body>
</html>
```

### **Tests de moderación**

```python
# tests/test_moderation.py
import pytest
from services.moderation_service import moderation_service
from services.filter_service import content_filter

class TestModerationService:

    def test_content_filter_detects_banned_words(self):
        """Test que el filtro detecta palabras prohibidas"""
        # TODO: Implementar test
        pass

    def test_automatic_moderation_actions(self):
        """Test de acciones automáticas de moderación"""
        # TODO: Implementar test
        pass

    def test_user_mute_functionality(self):
        """Test de funcionalidad de silenciar usuario"""
        # TODO: Implementar test
        pass

    def test_report_processing(self):
        """Test de procesamiento de reportes"""
        # TODO: Implementar test
        pass

    def test_moderation_logs(self):
        """Test de logs de moderación"""
        # TODO: Implementar test
        pass

class TestContentFilter:

    def test_banned_words_detection(self):
        """Test de detección de palabras prohibidas"""
        # TODO: Implementar test
        pass

    def test_message_cleaning(self):
        """Test de limpieza de mensajes"""
        # TODO: Implementar test
        pass

    def test_severity_classification(self):
        """Test de clasificación de severidad"""
        # TODO: Implementar test
        pass
```

---

## 🎯 Criterios de Evaluación

### **Funcionalidad (40 puntos)**

- ✅ **Ejercicio 1**: Echo server funcional con comandos (10 pts)
- ✅ **Ejercicio 2**: Sistema de notificaciones completo (10 pts)
- ✅ **Ejercicio 3**: Monitor SSE con gráficos (10 pts)
- ✅ **Ejercicio 4**: Chat con moderación funcional (10 pts)

### **Código Limpio (30 puntos)**

- 📝 Estructura clara y organizada (8 pts)
- 📝 Comentarios y documentación (7 pts)
- 📝 Manejo de errores apropiado (8 pts)
- 📝 Buenas prácticas de FastAPI (7 pts)

### **Testing (20 puntos)**

- 🧪 Tests básicos implementados (5 pts por ejercicio)

### **Documentación (10 puntos)**

- 📄 README claro con instrucciones (5 pts)
- 📄 Comentarios en código (5 pts)

---

## 📚 Recursos Adicionales

### **Bibliotecas útiles**

```bash
pip install psutil  # Para monitor de sistema
pip install python-multipart  # Para formularios
pip install jinja2  # Para templates
pip install pytest-asyncio  # Para tests async
```

### **Documentación**

- [FastAPI WebSockets](https://fastapi.tiangolo.com/advanced/websockets/)
- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)
- [Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

---

**🚀 ¡A programar!** Estos ejercicios te permitirán dominar las tecnologías avanzadas de API en FastAPI.

---

**Tiempo total estimado: 180 minutos (3 horas)**
