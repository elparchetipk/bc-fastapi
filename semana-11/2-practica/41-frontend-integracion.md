# Práctica 41: Frontend e Integración

⏰ **Tiempo estimado:** 90 minutos  
🎯 **Dificultad:** Integrador  
📋 **Prerrequisitos:** Práctica 40 completada

## 🎯 Objetivos de la Práctica

Al finalizar esta práctica, los estudiantes:

1. ✅ **Crearán la interfaz** de usuario con React y Tailwind CSS
2. ✅ **Implementarán navegación** con React Router
3. ✅ **Conectarán con la API** backend
4. ✅ **Configurarán WebSockets** para tiempo real
5. ✅ **Desplegarán la aplicación** con Docker

## 📋 Desarrollo Frontend TaskFlow

### **Paso 1: Configuración del Proyecto React**

#### **package.json - Dependencias completas**

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
    "lucide-react": "^0.294.0",
    "react-hook-form": "^7.48.2",
    "react-hot-toast": "^2.4.1"
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

### **Paso 2: Configuración de Estilos**

#### **tailwind.config.js**

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
      },
    },
  },
  plugins: [],
};
```

#### **src/index.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-gray-50 text-gray-900;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary-500 hover:bg-primary-600 text-white font-medium py-2 px-4 rounded-lg transition-colors;
  }

  .btn-secondary {
    @apply bg-gray-200 hover:bg-gray-300 text-gray-700 font-medium py-2 px-4 rounded-lg transition-colors;
  }

  .input-field {
    @apply w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent;
  }

  .card {
    @apply bg-white rounded-lg shadow-sm border border-gray-200 p-6;
  }
}
```

### **Paso 3: Tipos TypeScript**

#### **src/types/auth.ts**

```typescript
export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  full_name: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
```

#### **src/types/task.ts**

```typescript
export type TaskPriority = 'low' | 'medium' | 'high';
export type TaskStatus = 'pending' | 'in_progress' | 'completed';

export interface Task {
  id: number;
  title: string;
  description?: string;
  priority: TaskPriority;
  status: TaskStatus;
  due_date?: string;
  creator_id: number;
  assignee_id?: number;
  created_at: string;
  updated_at: string;
  creator: {
    id: number;
    username: string;
    full_name: string;
  };
  assignee?: {
    id: number;
    username: string;
    full_name: string;
  };
}

export interface CreateTaskRequest {
  title: string;
  description?: string;
  priority: TaskPriority;
  due_date?: string;
  assignee_id?: number;
}

export interface UpdateTaskRequest {
  title?: string;
  description?: string;
  priority?: TaskPriority;
  status?: TaskStatus;
  due_date?: string;
  assignee_id?: number;
}
```

### **Paso 4: Servicios API**

#### **src/services/api.ts**

```typescript
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar token de autenticación
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores de autenticación
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

#### **src/services/auth.ts**

```typescript
import { api } from './api';
import {
  LoginRequest,
  RegisterRequest,
  AuthResponse,
  User,
} from '../types/auth';

export const authService = {
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>(
      '/api/v1/auth/login',
      credentials
    );
    return response.data;
  },

  async register(userData: RegisterRequest): Promise<User> {
    const response = await api.post<User>('/api/v1/auth/register', userData);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await api.get<User>('/api/v1/users/me');
    return response.data;
  },

  logout() {
    localStorage.removeItem('access_token');
  },

  getToken(): string | null {
    return localStorage.getItem('access_token');
  },

  setToken(token: string) {
    localStorage.setItem('access_token', token);
  },
};
```

#### **src/services/tasks.ts**

```typescript
import { api } from './api';
import { Task, CreateTaskRequest, UpdateTaskRequest } from '../types/task';

export const taskService = {
  async getTasks(): Promise<Task[]> {
    const response = await api.get<Task[]>('/api/v1/tasks/');
    return response.data;
  },

  async getTask(id: number): Promise<Task> {
    const response = await api.get<Task>(`/api/v1/tasks/${id}`);
    return response.data;
  },

  async createTask(taskData: CreateTaskRequest): Promise<Task> {
    const response = await api.post<Task>('/api/v1/tasks/', taskData);
    return response.data;
  },

  async updateTask(id: number, taskData: UpdateTaskRequest): Promise<Task> {
    const response = await api.put<Task>(`/api/v1/tasks/${id}`, taskData);
    return response.data;
  },

  async updateTaskStatus(id: number, status: string): Promise<Task> {
    const response = await api.put<Task>(`/api/v1/tasks/${id}/status`, {
      status,
    });
    return response.data;
  },

  async deleteTask(id: number): Promise<void> {
    await api.delete(`/api/v1/tasks/${id}`);
  },
};
```

### **Paso 5: Hooks Personalizados**

#### **src/hooks/useAuth.ts**

```typescript
import { useState, useEffect } from 'react';
import { User } from '../types/auth';
import { authService } from '../services/auth';

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = authService.getToken();
    if (token) {
      authService
        .getCurrentUser()
        .then(setUser)
        .catch(() => authService.logout())
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  const login = async (credentials: any) => {
    const response = await authService.login(credentials);
    authService.setToken(response.access_token);
    const userData = await authService.getCurrentUser();
    setUser(userData);
    return userData;
  };

  const logout = () => {
    authService.logout();
    setUser(null);
  };

  return {
    user,
    loading,
    login,
    logout,
    isAuthenticated: !!user,
  };
};
```

#### **src/hooks/useTasks.ts**

```typescript
import { useState, useEffect } from 'react';
import { Task } from '../types/task';
import { taskService } from '../services/tasks';
import toast from 'react-hot-toast';

export const useTasks = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchTasks = async () => {
    try {
      const tasksData = await taskService.getTasks();
      setTasks(tasksData);
    } catch (error) {
      toast.error('Error loading tasks');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const createTask = async (taskData: any) => {
    try {
      const newTask = await taskService.createTask(taskData);
      setTasks((prev) => [newTask, ...prev]);
      toast.success('Task created successfully');
      return newTask;
    } catch (error) {
      toast.error('Error creating task');
      throw error;
    }
  };

  const updateTask = async (id: number, taskData: any) => {
    try {
      const updatedTask = await taskService.updateTask(id, taskData);
      setTasks((prev) =>
        prev.map((task) => (task.id === id ? updatedTask : task))
      );
      toast.success('Task updated successfully');
      return updatedTask;
    } catch (error) {
      toast.error('Error updating task');
      throw error;
    }
  };

  const deleteTask = async (id: number) => {
    try {
      await taskService.deleteTask(id);
      setTasks((prev) => prev.filter((task) => task.id !== id));
      toast.success('Task deleted successfully');
    } catch (error) {
      toast.error('Error deleting task');
      throw error;
    }
  };

  return {
    tasks,
    loading,
    createTask,
    updateTask,
    deleteTask,
    refetch: fetchTasks,
  };
};
```

### **Paso 6: Componentes Principales**

#### **src/components/common/Layout.tsx**

```typescript
import React from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { LogOut, User, Home, CheckSquare } from 'lucide-react';

export const Layout: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center space-x-8">
              <Link
                to="/dashboard"
                className="text-xl font-bold text-primary-600">
                TaskFlow
              </Link>
              <div className="flex space-x-4">
                <Link
                  to="/dashboard"
                  className="flex items-center space-x-2 text-gray-600 hover:text-gray-900">
                  <Home size={20} />
                  <span>Dashboard</span>
                </Link>
                <Link
                  to="/tasks"
                  className="flex items-center space-x-2 text-gray-600 hover:text-gray-900">
                  <CheckSquare size={20} />
                  <span>Tasks</span>
                </Link>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <User
                  size={20}
                  className="text-gray-400"
                />
                <span className="text-sm text-gray-700">{user?.full_name}</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 text-gray-600 hover:text-gray-900">
                <LogOut size={20} />
                <span>Logout</span>
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
        <Outlet />
      </main>
    </div>
  );
};
```

#### **src/components/auth/LoginForm.tsx**

```typescript
import React from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { LoginRequest } from '../../types/auth';

interface LoginFormProps {
  onSubmit: (data: LoginRequest) => Promise<void>;
  loading?: boolean;
}

export const LoginForm: React.FC<LoginFormProps> = ({ onSubmit, loading }) => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginRequest>();

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to TaskFlow
          </h2>
        </div>

        <form
          className="mt-8 space-y-6"
          onSubmit={handleSubmit(onSubmit)}>
          <div className="rounded-md shadow-sm -space-y-px">
            <div>
              <input
                {...register('username', { required: 'Username is required' })}
                type="text"
                className="input-field rounded-t-md"
                placeholder="Username"
              />
              {errors.username && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.username.message}
                </p>
              )}
            </div>

            <div>
              <input
                {...register('password', { required: 'Password is required' })}
                type="password"
                className="input-field rounded-b-md"
                placeholder="Password"
              />
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">
                  {errors.password.message}
                </p>
              )}
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50">
              {loading ? 'Signing in...' : 'Sign in'}
            </button>
          </div>

          <div className="text-center">
            <Link
              to="/register"
              className="text-primary-600 hover:text-primary-500">
              Don't have an account? Sign up
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
};
```

#### **src/components/tasks/TaskList.tsx**

```typescript
import React from 'react';
import { Task } from '../../types/task';
import { TaskCard } from './TaskCard';

interface TaskListProps {
  tasks: Task[];
  onUpdateTask: (id: number, data: any) => Promise<void>;
  onDeleteTask: (id: number) => Promise<void>;
}

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onUpdateTask,
  onDeleteTask,
}) => {
  const pendingTasks = tasks.filter((task) => task.status === 'pending');
  const inProgressTasks = tasks.filter((task) => task.status === 'in_progress');
  const completedTasks = tasks.filter((task) => task.status === 'completed');

  const renderTaskColumn = (title: string, tasks: Task[], status: string) => (
    <div className="flex-1">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
      <div className="space-y-4">
        {tasks.map((task) => (
          <TaskCard
            key={task.id}
            task={task}
            onUpdate={onUpdateTask}
            onDelete={onDeleteTask}
          />
        ))}
        {tasks.length === 0 && (
          <p className="text-gray-500 text-center py-8">
            No tasks in this column
          </p>
        )}
      </div>
    </div>
  );

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {renderTaskColumn('Pending', pendingTasks, 'pending')}
      {renderTaskColumn('In Progress', inProgressTasks, 'in_progress')}
      {renderTaskColumn('Completed', completedTasks, 'completed')}
    </div>
  );
};
```

#### **src/pages/DashboardPage.tsx**

```typescript
import React from 'react';
import { useTasks } from '../hooks/useTasks';
import { CheckSquare, Clock, TrendingUp, Users } from 'lucide-react';

export const DashboardPage: React.FC = () => {
  const { tasks, loading } = useTasks();

  if (loading) {
    return <div className="text-center py-8">Loading...</div>;
  }

  const stats = {
    total: tasks.length,
    pending: tasks.filter((t) => t.status === 'pending').length,
    inProgress: tasks.filter((t) => t.status === 'in_progress').length,
    completed: tasks.filter((t) => t.status === 'completed').length,
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Overview of your tasks and progress</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <CheckSquare className="h-8 w-8 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Total Tasks</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats.total}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Clock className="h-8 w-8 text-yellow-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Pending</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats.pending}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <TrendingUp className="h-8 w-8 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">In Progress</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats.inProgress}
              </p>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <Users className="h-8 w-8 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-500">Completed</p>
              <p className="text-2xl font-semibold text-gray-900">
                {stats.completed}
              </p>
            </div>
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          Recent Tasks
        </h2>
        <div className="space-y-3">
          {tasks.slice(0, 5).map((task) => (
            <div
              key={task.id}
              className="flex items-center justify-between py-2 border-b border-gray-100 last:border-0">
              <div>
                <p className="font-medium text-gray-900">{task.title}</p>
                <p className="text-sm text-gray-500">
                  Created by {task.creator.full_name}
                </p>
              </div>
              <span
                className={`px-2 py-1 text-xs rounded-full ${
                  task.status === 'completed'
                    ? 'bg-green-100 text-green-800'
                    : task.status === 'in_progress'
                    ? 'bg-orange-100 text-orange-800'
                    : 'bg-gray-100 text-gray-800'
                }`}>
                {task.status.replace('_', ' ')}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
```

### **Paso 7: Aplicación Principal**

#### **src/App.tsx**

```typescript
import React from 'react';
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { useAuth } from './hooks/useAuth';
import { Layout } from './components/common/Layout';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { DashboardPage } from './pages/DashboardPage';
import { TasksPage } from './pages/TasksPage';

function App() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
          <p className="mt-2 text-gray-600">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="App">
        <Toaster position="top-right" />

        <Routes>
          <Route
            path="/login"
            element={user ? <Navigate to="/dashboard" /> : <LoginPage />}
          />
          <Route
            path="/register"
            element={user ? <Navigate to="/dashboard" /> : <RegisterPage />}
          />

          <Route
            path="/"
            element={user ? <Layout /> : <Navigate to="/login" />}>
            <Route
              index
              element={<Navigate to="/dashboard" />}
            />
            <Route
              path="dashboard"
              element={<DashboardPage />}
            />
            <Route
              path="tasks"
              element={<TasksPage />}
            />
          </Route>
        </Routes>
      </div>
    </Router>
  );
}

export default App;
```

## 🐳 Deployment con Docker

### **Paso 8: Configurar Docker para Frontend**

#### **Frontend Dockerfile**

```dockerfile
# Build stage
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

#### **nginx.conf**

```nginx
events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    server {
        listen 80;
        server_name localhost;
        root /usr/share/nginx/html;
        index index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location /api {
            proxy_pass http://backend:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /ws {
            proxy_pass http://backend:8000;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }
    }
}
```

### **Paso 9: Docker Compose Completo**

#### **docker-compose.yml actualizado**

```yaml
version: '3.8'

services:
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

  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'
    networks:
      - taskflow-network

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
    networks:
      - taskflow-network

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

## 🚀 Despliegue y Testing

### **Paso 10: Ejecutar aplicación completa**

```bash
# Desde el directorio raíz del proyecto
docker-compose up --build

# La aplicación estará disponible en:
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🎯 Entregables de esta Práctica

### ✅ **Aplicación Frontend Completa:**

1. **Interfaz React** con Tailwind CSS
2. **Navegación** con React Router
3. **Autenticación** integrada
4. **CRUD de tareas** funcional
5. **Deployment** con Docker

### 📁 **Estructura implementada:**

```
frontend/
├── src/
│   ├── components/ ✅
│   ├── pages/ ✅
│   ├── services/ ✅
│   ├── hooks/ ✅
│   ├── types/ ✅
│   └── App.tsx ✅
├── nginx.conf ✅
├── Dockerfile ✅
└── package.json ✅
```

## 📚 Funcionalidades Implementadas

### **✅ Autenticación completa**

- Login y registro
- Protección de rutas
- Gestión de tokens JWT

### **✅ Gestión de tareas**

- Dashboard con estadísticas
- Vista kanban de tareas
- CRUD completo
- Filtros y búsqueda

### **✅ Interfaz moderna**

- Diseño responsive
- Componentes reutilizables
- UX optimizada

---

## 🎯 Frontend TaskFlow Completado

La aplicación frontend está completamente integrada con el backend y lista para uso en producción.

**Siguiente:** [Práctica 42 - Documentación y Presentación](./42-documentacion-presentacion.md)

---

**💡 La aplicación TaskFlow está funcionalmente completa y lista para el mercado laboral.**
