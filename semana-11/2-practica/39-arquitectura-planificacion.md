# Práctica 39: Arquitectura y Planificación del Proyecto Final

⏰ **Tiempo estimado:** 90 minutos  
🎯 **Dificultad:** Integrador  
📋 **Prerrequisitos:** Conocimiento completo de semanas 1-10

## 🎯 Objetivos de la Práctica

Al finalizar esta práctica, los estudiantes:

1. ✅ **Diseñarán la arquitectura** completa del proyecto final
2. ✅ **Definirán las especificaciones** técnicas del sistema
3. ✅ **Crearán la estructura** del proyecto con mejores prácticas
4. ✅ **Planificarán el desarrollo** con tareas específicas
5. ✅ **Configurarán el entorno** de desarrollo integrado

## 📋 Proyecto a Desarrollar: TaskFlow - Sistema de Gestión de Tareas

### 🎯 **Descripción del Sistema**

**TaskFlow** es una aplicación web completa para gestión de tareas colaborativa que integra todas las tecnologías aprendidas en el bootcamp.

### 🔧 **Funcionalidades Principales**

1. **👥 Gestión de Usuarios**

   - Registro y autenticación con JWT
   - Perfiles de usuario
   - Roles y permisos básicos

2. **📋 Gestión de Tareas**

   - CRUD completo de tareas
   - Asignación de tareas a usuarios
   - Estados de tareas (pendiente, en progreso, completada)
   - Prioridades (baja, media, alta)

3. **🔔 Notificaciones en Tiempo Real**

   - WebSockets para notificaciones instantáneas
   - Notificaciones de nuevas tareas asignadas
   - Actualizaciones de estado en tiempo real

4. **📊 Dashboard y Reportes**

   - Vista general de tareas
   - Estadísticas básicas
   - Filtros y búsqueda

5. **📱 Interfaz Responsive**
   - Diseño adaptable para desktop y móvil
   - Interfaz moderna con Tailwind CSS

## 🏗️ Arquitectura del Sistema

### **Stack Tecnológico Integrado**

```
Frontend:
├── React 18 con TypeScript
├── Vite como build tool
├── Tailwind CSS para styling
├── React Router para navegación
└── Axios para HTTP requests

Backend:
├── FastAPI con Python 3.11+
├── Pydantic para validación
├── SQLAlchemy como ORM
├── Alembic para migraciones
├── JWT para autenticación
├── WebSockets para tiempo real
└── Background tasks para jobs

Base de Datos:
├── PostgreSQL (principal)
├── Redis (cache y sessions)
└── SQLite (desarrollo y testing)

DevOps:
├── Docker & Docker Compose
├── GitHub Actions para CI/CD
└── pytest para testing
```

### **Arquitectura en Capas**

```
┌─────────────────────────────────────────┐
│           Frontend (React)              │
│    Components + Pages + Services        │
└─────────────────┬───────────────────────┘
                  │ HTTP/WebSocket
┌─────────────────▼───────────────────────┐
│          API Layer (FastAPI)            │
│      Routes + Middleware + Auth         │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       Business Logic (Services)        │
│     TaskService + UserService + ...    │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│      Data Access (Repositories)        │
│    TaskRepository + UserRepository     │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│       Data Layer (Databases)           │
│        PostgreSQL + Redis              │
└─────────────────────────────────────────┘
```

## 📁 Estructura del Proyecto

### **Paso 1: Crear la estructura base del proyecto**

```bash
# Crear directorio principal
mkdir taskflow-app
cd taskflow-app

# Crear estructura de directorios
mkdir -p backend/{app/{api,core,models,schemas,services,repositories,websockets,dependencies},tests,migrations}
mkdir -p frontend/{src/{components,pages,services,hooks,utils,types},public}
mkdir -p deployment/{docker,nginx}
mkdir -p docs/{api,architecture}

# Crear archivos de configuración
touch backend/requirements.txt
touch backend/Dockerfile
touch frontend/package.json
touch frontend/Dockerfile
touch docker-compose.yml
touch docker-compose.prod.yml
touch README.md
touch .gitignore
```

### **Estructura Completa del Proyecto**

```
taskflow-app/
├── README.md
├── .gitignore
├── docker-compose.yml
├── docker-compose.prod.yml
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py
│   │   │       ├── users.py
│   │   │       ├── tasks.py
│   │   │       └── websockets.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   └── base.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── task.py
│   │   │   └── auth.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── user_service.py
│   │   │   ├── task_service.py
│   │   │   └── notification_service.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py
│   │   │   └── task_repository.py
│   │   ├── websockets/
│   │   │   ├── __init__.py
│   │   │   └── manager.py
│   │   └── dependencies/
│   │       ├── __init__.py
│   │       ├── database.py
│   │       └── auth.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_users.py
│   │   └── test_tasks.py
│   ├── migrations/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── common/
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   └── Layout.tsx
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   └── RegisterForm.tsx
│   │   │   └── tasks/
│   │   │       ├── TaskList.tsx
│   │   │       ├── TaskForm.tsx
│   │   │       └── TaskCard.tsx
│   │   ├── pages/
│   │   │   ├── HomePage.tsx
│   │   │   ├── LoginPage.tsx
│   │   │   ├── DashboardPage.tsx
│   │   │   └── TasksPage.tsx
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── auth.ts
│   │   │   ├── tasks.ts
│   │   │   └── websocket.ts
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   ├── useTasks.ts
│   │   │   └── useWebSocket.ts
│   │   ├── utils/
│   │   │   ├── constants.ts
│   │   │   └── formatters.ts
│   │   ├── types/
│   │   │   ├── auth.ts
│   │   │   └── task.ts
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
│
└── deployment/
    ├── docker/
    └── nginx/
```

## 🛠️ Configuración del Entorno de Desarrollo

### **Paso 2: Configurar Backend**

#### **requirements.txt**

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9
redis==5.0.1
pydantic==2.5.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
websockets==12.0
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
python-dotenv==1.0.0
```

#### **Backend Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### **Paso 3: Configurar Frontend**

#### **package.json**

```json
{
  "name": "taskflow-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "axios": "^1.6.2",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.37",
    "@types/react-dom": "^18.2.15",
    "@typescript-eslint/eslint-plugin": "^6.10.0",
    "@typescript-eslint/parser": "^6.10.0",
    "@vitejs/plugin-react": "^4.1.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.53.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.4",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6",
    "typescript": "^5.2.2",
    "vite": "^4.5.0"
  }
}
```

#### **Frontend Dockerfile**

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source code and build
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built app
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

### **Paso 4: Docker Compose para desarrollo**

#### **docker-compose.yml**

```yaml
version: '3.8'

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: taskflow_db
      POSTGRES_USER: taskflow_user
      POSTGRES_PASSWORD: taskflow_password
    ports:
      - '5432:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - taskflow-network

  # Redis Cache
  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'
    networks:
      - taskflow-network

  # Backend API
  backend:
    build: ./backend
    ports:
      - '8000:8000'
    environment:
      DATABASE_URL: postgresql://taskflow_user:taskflow_password@postgres:5432/taskflow_db
      REDIS_URL: redis://redis:6379
      SECRET_KEY: your-secret-key-here
    depends_on:
      - postgres
      - redis
    volumes:
      - ./backend/app:/app/app
    networks:
      - taskflow-network

  # Frontend
  frontend:
    build: ./frontend
    ports:
      - '3000:80'
    depends_on:
      - backend
    networks:
      - taskflow-network

volumes:
  postgres_data:

networks:
  taskflow-network:
    driver: bridge
```

## 📋 Especificaciones Técnicas Detalladas

### **Modelos de Datos**

#### **Usuario (User)**

```python
class User(Base):
    __tablename__ = "users"

    id: int (PK)
    email: str (unique)
    username: str (unique)
    hashed_password: str
    full_name: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

    # Relaciones
    tasks: List[Task] = relationship("Task", back_populates="assignee")
```

#### **Tarea (Task)**

```python
class Task(Base):
    __tablename__ = "tasks"

    id: int (PK)
    title: str
    description: str
    priority: TaskPriority (enum: low, medium, high)
    status: TaskStatus (enum: pending, in_progress, completed)
    due_date: datetime (optional)
    created_at: datetime
    updated_at: datetime

    # Foreign Keys
    assignee_id: int (FK -> users.id)
    creator_id: int (FK -> users.id)

    # Relaciones
    assignee: User = relationship("User", foreign_keys=[assignee_id])
    creator: User = relationship("User", foreign_keys=[creator_id])
```

### **Endpoints API Principales**

```
Authentication:
POST   /api/v1/auth/register          # Registro de usuario
POST   /api/v1/auth/login             # Login
POST   /api/v1/auth/refresh           # Refresh token

Users:
GET    /api/v1/users/me               # Perfil del usuario actual
PUT    /api/v1/users/me               # Actualizar perfil
GET    /api/v1/users/                 # Listar usuarios

Tasks:
GET    /api/v1/tasks/                 # Listar tareas
POST   /api/v1/tasks/                 # Crear tarea
GET    /api/v1/tasks/{id}             # Obtener tarea específica
PUT    /api/v1/tasks/{id}             # Actualizar tarea
DELETE /api/v1/tasks/{id}             # Eliminar tarea
PUT    /api/v1/tasks/{id}/status      # Cambiar estado

WebSockets:
WS     /ws/notifications/{user_id}    # Notificaciones en tiempo real
```

## 📝 Plan de Desarrollo (Próximas 3 prácticas)

### **Práctica 40: Desarrollo Backend Completo (90 min)**

- Implementar modelos y esquemas
- Crear servicios y repositorios
- Configurar autenticación JWT
- Implementar endpoints principales

### **Práctica 41: Frontend e Integración (90 min)**

- Crear componentes React
- Implementar routing y navegación
- Conectar con API backend
- Configurar WebSockets

### **Práctica 42: Documentación y Presentación (90 min)**

- Completar testing
- Generar documentación
- Preparar deployment
- Ensayar presentación

## 🎯 Entregables de esta Práctica

### ✅ **Al finalizar esta práctica tendrás:**

1. **Estructura de proyecto** completa y organizada
2. **Arquitectura definida** con diagramas claros
3. **Entorno de desarrollo** configurado con Docker
4. **Especificaciones técnicas** detalladas
5. **Plan de desarrollo** para las próximas sesiones

### 📁 **Archivos creados:**

```
taskflow-app/
├── README.md ✅
├── docker-compose.yml ✅
├── backend/
│   ├── requirements.txt ✅
│   ├── Dockerfile ✅
│   └── app/ (estructura creada) ✅
├── frontend/
│   ├── package.json ✅
│   ├── Dockerfile ✅
│   └── src/ (estructura creada) ✅
└── docs/
    └── architecture.md ✅
```

## 🚀 Verificación y Testing

### **Paso 5: Verificar configuración**

```bash
# Desde el directorio taskflow-app/
docker-compose up -d postgres redis

# Verificar que los servicios estén funcionando
docker-compose ps

# Comprobar logs
docker-compose logs postgres
docker-compose logs redis
```

## 📚 Recursos Adicionales

### **Documentación de Referencia**

- [FastAPI Project Structure](https://fastapi.tiangolo.com/tutorial/bigger-applications/)
- [React Project Organization](https://react.dev/learn/thinking-in-react)
- [Docker Compose Guide](https://docs.docker.com/compose/)

### **Herramientas de Diseño**

- [Draw.io](https://app.diagrams.net/) para diagramas de arquitectura
- [Figma](https://figma.com/) para mockups de UI
- [DB Designer](https://www.dbdesigner.net/) para diagramas de base de datos

---

## 🎯 ¡Listo para el Desarrollo!

Con la arquitectura y planificación completa, estás preparado para comenzar el desarrollo del proyecto final. En las próximas prácticas implementarás cada componente paso a paso.

**Siguiente:** [Práctica 40 - Desarrollo Backend Completo](./40-desarrollo-backend-completo.md)

---

**💡 Recuerda: Una buena planificación es la clave del éxito en el desarrollo de software.**
