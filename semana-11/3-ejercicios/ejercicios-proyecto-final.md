# Ejercicios Avanzados de Proyecto Final

## 📋 Ejercicios Detallados por Nivel

### **Nivel 1: Mejoras Básicas (Tiempo: 30-45 min)**

Perfectos para estudiantes que quieren pulir su proyecto base sin agregar complejidad excesiva.

#### **E1.1: Personalización de Tema**

**Objetivo:** Hacer la aplicación visualmente única

**Implementación:**

```css
/* src/index.css - Tema personalizado */
:root {
  --primary-50: #f0f9ff;
  --primary-100: #e0f2fe;
  --primary-500: #06b6d4;
  --primary-600: #0891b2;
  --primary-700: #0e7490;
  --success: #10b981;
  --warning: #f59e0b;
  --error: #ef4444;
}

.theme-custom {
  --tw-bg-opacity: 1;
  background-color: linear-gradient(
    135deg,
    var(--primary-50) 0%,
    var(--primary-100) 100%
  );
}

.card-gradient {
  background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
```

**Entregable:** Aplicación con identidad visual propia

#### **E1.2: Validaciones Mejoradas**

**Objetivo:** Agregar validaciones más robustas

**Frontend:**

```typescript
// src/utils/validation.ts
export const taskValidation = {
  title: {
    required: 'Title is required',
    minLength: { value: 3, message: 'Title must be at least 3 characters' },
    maxLength: { value: 100, message: 'Title cannot exceed 100 characters' },
  },
  description: {
    maxLength: {
      value: 500,
      message: 'Description cannot exceed 500 characters',
    },
  },
  dueDate: {
    validate: (value: string) => {
      const selected = new Date(value);
      const today = new Date();
      return selected >= today || 'Due date cannot be in the past';
    },
  },
};
```

**Backend:**

```python
# app/schemas/task.py - Validaciones mejoradas
from datetime import datetime
from pydantic import validator

class TaskCreate(TaskBase):
    @validator('title')
    def validate_title(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters')
        if len(v.strip()) > 100:
            raise ValueError('Title cannot exceed 100 characters')
        return v.strip()

    @validator('due_date')
    def validate_due_date(cls, v):
        if v and v < datetime.now():
            raise ValueError('Due date cannot be in the past')
        return v
```

**Entregable:** Validaciones robustas implementadas y probadas

#### **E1.3: Estados de Loading**

**Objetivo:** Mejorar UX con indicadores de carga

```typescript
// src/components/common/LoadingSpinner.tsx
export const LoadingSpinner: React.FC<{ size?: 'sm' | 'md' | 'lg' }> = ({
  size = 'md',
}) => {
  const sizeClasses = {
    sm: 'h-4 w-4',
    md: 'h-8 w-8',
    lg: 'h-12 w-12',
  };

  return (
    <div
      className={`animate-spin rounded-full border-2 border-gray-300 border-t-primary-600 ${sizeClasses[size]}`}
    />
  );
};

// src/hooks/useAsyncOperation.ts
export const useAsyncOperation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = async (operation: () => Promise<any>) => {
    setLoading(true);
    setError(null);
    try {
      const result = await operation();
      return result;
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { loading, error, execute };
};
```

---

### **Nivel 2: Funcionalidades Intermedias (Tiempo: 60-90 min)**

Para estudiantes que quieren agregar valor significativo a su proyecto.

#### **E2.1: Sistema de Comentarios**

**Objetivo:** Agregar colaboración en tareas

**Backend Models:**

```python
# app/models/comment.py
class Comment(Base, TimestampMixin):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relaciones
    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="comments")

# Actualizar app/models/task.py
class Task(Base, TimestampMixin):
    # ... campos existentes ...
    comments = relationship("Comment", back_populates="task", cascade="all, delete-orphan")
```

**API Endpoints:**

```python
# app/api/v1/comments.py
@router.post("/tasks/{task_id}/comments", response_model=CommentResponse)
async def create_comment(
    task_id: int,
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    return await comment_service.create_comment(task_id, comment_data, current_user.id)

@router.get("/tasks/{task_id}/comments", response_model=List[CommentResponse])
async def get_task_comments(
    task_id: int,
    current_user: User = Depends(get_current_user),
    comment_service: CommentService = Depends(get_comment_service)
):
    return await comment_service.get_task_comments(task_id, current_user.id)
```

**Frontend Component:**

```typescript
// src/components/comments/CommentsList.tsx
export const CommentsList: React.FC<{ taskId: number }> = ({ taskId }) => {
  const [comments, setComments] = useState<Comment[]>([]);
  const [newComment, setNewComment] = useState('');

  const addComment = async () => {
    if (!newComment.trim()) return;

    try {
      const comment = await commentService.createComment(taskId, {
        content: newComment,
      });
      setComments((prev) => [comment, ...prev]);
      setNewComment('');
      toast.success('Comment added');
    } catch (error) {
      toast.error('Failed to add comment');
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex space-x-2">
        <input
          value={newComment}
          onChange={(e) => setNewComment(e.target.value)}
          placeholder="Add a comment..."
          className="flex-1 input-field"
        />
        <button
          onClick={addComment}
          className="btn-primary">
          Add
        </button>
      </div>

      <div className="space-y-2">
        {comments.map((comment) => (
          <div
            key={comment.id}
            className="bg-gray-50 p-3 rounded">
            <p className="text-sm text-gray-700">{comment.content}</p>
            <div className="text-xs text-gray-500 mt-1">
              {comment.user.full_name} • {formatDate(comment.created_at)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

**Entregable:** Sistema de comentarios funcionando con WebSocket updates

#### **E2.2: Búsqueda y Filtros Avanzados**

**Objetivo:** Mejorar la usabilidad con filtros inteligentes

**Backend:**

```python
# app/services/task_service.py
class TaskSearchService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    async def search_tasks(
        self,
        user_id: int,
        search_query: Optional[str] = None,
        status_filter: Optional[List[TaskStatus]] = None,
        priority_filter: Optional[List[TaskPriority]] = None,
        date_range: Optional[dict] = None
    ) -> List[TaskResponse]:

        query = self.task_repo.get_base_query(user_id)

        if search_query:
            search_term = f"%{search_query}%"
            query = query.filter(
                or_(
                    Task.title.ilike(search_term),
                    Task.description.ilike(search_term)
                )
            )

        if status_filter:
            query = query.filter(Task.status.in_(status_filter))

        if priority_filter:
            query = query.filter(Task.priority.in_(priority_filter))

        if date_range:
            if date_range.get('start'):
                query = query.filter(Task.created_at >= date_range['start'])
            if date_range.get('end'):
                query = query.filter(Task.created_at <= date_range['end'])

        tasks = query.all()
        return [TaskResponse.from_orm(task) for task in tasks]
```

**Frontend:**

```typescript
// src/components/tasks/TaskFilters.tsx
export const TaskFilters: React.FC<{
  onFiltersChange: (filters: TaskFilters) => void;
}> = ({ onFiltersChange }) => {
  const [filters, setFilters] = useState<TaskFilters>({});

  const updateFilters = (newFilters: Partial<TaskFilters>) => {
    const updated = { ...filters, ...newFilters };
    setFilters(updated);
    onFiltersChange(updated);
  };

  return (
    <div className="bg-white p-4 rounded-lg shadow space-y-4">
      <div className="flex flex-wrap gap-4">
        <input
          type="text"
          placeholder="Search tasks..."
          className="input-field flex-1 min-w-64"
          onChange={(e) => updateFilters({ search: e.target.value })}
        />

        <select
          className="input-field"
          onChange={(e) =>
            updateFilters({
              status: e.target.value
                ? [e.target.value as TaskStatus]
                : undefined,
            })
          }>
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
        </select>

        <select
          className="input-field"
          onChange={(e) =>
            updateFilters({
              priority: e.target.value
                ? [e.target.value as TaskPriority]
                : undefined,
            })
          }>
          <option value="">All Priorities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>
    </div>
  );
};
```

**Entregable:** Sistema de búsqueda y filtros funcional con resultados en tiempo real

#### **E2.3: Drag & Drop para Tareas**

**Objetivo:** Implementar interfaz intuitiva tipo Kanban

```typescript
// npm install react-beautiful-dnd @types/react-beautiful-dnd

// src/components/tasks/KanbanBoard.tsx
import { DragDropContext, Droppable, Draggable } from 'react-beautiful-dnd';

export const KanbanBoard: React.FC<{
  tasks: Task[];
  onTaskUpdate: (id: number, data: Partial<Task>) => void;
}> = ({ tasks, onTaskUpdate }) => {
  const columns = {
    pending: tasks.filter((t) => t.status === 'pending'),
    in_progress: tasks.filter((t) => t.status === 'in_progress'),
    completed: tasks.filter((t) => t.status === 'completed'),
  };

  const handleDragEnd = async (result: any) => {
    if (!result.destination) return;

    const { source, destination, draggableId } = result;

    if (source.droppableId !== destination.droppableId) {
      const newStatus = destination.droppableId as TaskStatus;
      await onTaskUpdate(parseInt(draggableId), { status: newStatus });
    }
  };

  return (
    <DragDropContext onDragEnd={handleDragEnd}>
      <div className="grid grid-cols-3 gap-6">
        {Object.entries(columns).map(([status, statusTasks]) => (
          <div
            key={status}
            className="bg-gray-50 p-4 rounded-lg">
            <h3 className="font-semibold mb-4 capitalize">
              {status.replace('_', ' ')}
            </h3>

            <Droppable droppableId={status}>
              {(provided) => (
                <div
                  {...provided.droppableProps}
                  ref={provided.innerRef}
                  className="space-y-3">
                  {statusTasks.map((task, index) => (
                    <Draggable
                      key={task.id}
                      draggableId={task.id.toString()}
                      index={index}>
                      {(provided) => (
                        <div
                          ref={provided.innerRef}
                          {...provided.draggableProps}
                          {...provided.dragHandleProps}
                          className="bg-white p-3 rounded shadow hover:shadow-md transition-shadow">
                          <TaskCard
                            task={task}
                            compact
                          />
                        </div>
                      )}
                    </Draggable>
                  ))}
                  {provided.placeholder}
                </div>
              )}
            </Droppable>
          </div>
        ))}
      </div>
    </DragDropContext>
  );
};
```

**Entregable:** Interfaz Kanban con drag & drop funcionando

---

### **Nivel 3: Características Avanzadas (Tiempo: 90+ min)**

Para estudiantes que quieren destacar con funcionalidades enterprise-level.

#### **E3.1: Sistema de Notificaciones Push**

**Objetivo:** Implementar notificaciones en tiempo real completas

**Backend Service:**

```python
# app/services/notification_service.py
from enum import Enum
from typing import List, Dict

class NotificationType(str, Enum):
    TASK_ASSIGNED = "task_assigned"
    TASK_COMPLETED = "task_completed"
    TASK_OVERDUE = "task_overdue"
    COMMENT_ADDED = "comment_added"

class NotificationService:
    def __init__(self, websocket_manager: ConnectionManager):
        self.ws_manager = websocket_manager

    async def send_notification(
        self,
        user_id: int,
        notification_type: NotificationType,
        title: str,
        message: str,
        data: Dict = None
    ):
        notification = {
            "type": notification_type.value,
            "title": title,
            "message": message,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat()
        }

        await self.ws_manager.send_personal_message(notification, user_id)

        # También guardar en base de datos para historial
        await self._save_notification(user_id, notification)

    async def notify_task_assigned(self, task: Task, assignee: User):
        await self.send_notification(
            user_id=assignee.id,
            notification_type=NotificationType.TASK_ASSIGNED,
            title="New Task Assigned",
            message=f"You have been assigned to task: {task.title}",
            data={"task_id": task.id, "task_title": task.title}
        )
```

**Frontend Hook:**

```typescript
// src/hooks/useNotifications.ts
export const useNotifications = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const { user } = useAuth();

  useEffect(() => {
    if (!user) return;

    const ws = new WebSocket(`ws://localhost:8000/ws/notifications/${user.id}`);

    ws.onmessage = (event) => {
      const notification = JSON.parse(event.data);

      setNotifications((prev) => [notification, ...prev.slice(0, 49)]); // Keep last 50
      setUnreadCount((prev) => prev + 1);

      // Show toast notification
      toast.success(notification.title, {
        description: notification.message,
        action: notification.data?.task_id
          ? {
              label: 'View Task',
              onClick: () => navigate(`/tasks/${notification.data.task_id}`),
            }
          : undefined,
      });
    };

    return () => ws.close();
  }, [user]);

  const markAsRead = (notificationId: string) => {
    setNotifications((prev) =>
      prev.map((n) => (n.id === notificationId ? { ...n, read: true } : n))
    );
    setUnreadCount((prev) => Math.max(0, prev - 1));
  };

  return {
    notifications,
    unreadCount,
    markAsRead,
  };
};
```

**Entregable:** Sistema completo de notificaciones push funcionando

#### **E3.2: Analytics Dashboard**

**Objetivo:** Agregar métricas y reportes avanzados

**Backend Analytics Service:**

```python
# app/services/analytics_service.py
from sqlalchemy import func, extract
from datetime import datetime, timedelta

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_analytics(self, user_id: int) -> Dict:
        # Tareas por estado
        status_counts = self.db.query(
            Task.status,
            func.count(Task.id).label('count')
        ).filter(
            or_(Task.creator_id == user_id, Task.assignee_id == user_id)
        ).group_by(Task.status).all()

        # Productividad por día (últimos 30 días)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        daily_completion = self.db.query(
            func.date(Task.updated_at).label('date'),
            func.count(Task.id).label('completed')
        ).filter(
            Task.status == TaskStatus.COMPLETED,
            Task.updated_at >= thirty_days_ago,
            or_(Task.creator_id == user_id, Task.assignee_id == user_id)
        ).group_by(func.date(Task.updated_at)).all()

        # Tareas por prioridad
        priority_counts = self.db.query(
            Task.priority,
            func.count(Task.id).label('count')
        ).filter(
            or_(Task.creator_id == user_id, Task.assignee_id == user_id),
            Task.status != TaskStatus.COMPLETED
        ).group_by(Task.priority).all()

        return {
            "status_distribution": {item.status: item.count for item in status_counts},
            "daily_completions": [
                {"date": item.date.isoformat(), "count": item.completed}
                for item in daily_completion
            ],
            "priority_distribution": {item.priority: item.count for item in priority_counts},
            "total_tasks": sum(item.count for item in status_counts),
            "completion_rate": self._calculate_completion_rate(user_id)
        }
```

**Frontend Dashboard:**

```typescript
// src/components/analytics/AnalyticsDashboard.tsx
// npm install recharts

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

export const AnalyticsDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);

  useEffect(() => {
    analyticsService.getUserAnalytics().then(setAnalytics);
  }, []);

  if (!analytics) return <LoadingSpinner />;

  const statusData = Object.entries(analytics.status_distribution).map(
    ([status, count]) => ({
      name: status.replace('_', ' '),
      value: count,
    })
  );

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold">Analytics Dashboard</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold mb-4">
            Task Status Distribution
          </h3>
          <PieChart
            width={300}
            height={300}>
            <Pie
              data={statusData}
              cx={150}
              cy={150}
              labelLine={false}
              label={({ name, percent }) =>
                `${name} ${(percent * 100).toFixed(0)}%`
              }
              outerRadius={80}
              fill="#8884d8"
              dataKey="value">
              {statusData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[index % COLORS.length]}
                />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </div>

        <div className="card">
          <h3 className="text-lg font-semibold mb-4">
            Daily Completions (Last 30 Days)
          </h3>
          <BarChart
            width={300}
            height={300}
            data={analytics.daily_completions}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Bar
              dataKey="count"
              fill="#3b82f6"
            />
          </BarChart>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card text-center">
          <h4 className="text-sm text-gray-500">Total Tasks</h4>
          <p className="text-2xl font-bold">{analytics.total_tasks}</p>
        </div>
        <div className="card text-center">
          <h4 className="text-sm text-gray-500">Completion Rate</h4>
          <p className="text-2xl font-bold">{analytics.completion_rate}%</p>
        </div>
        <div className="card text-center">
          <h4 className="text-sm text-gray-500">Avg. Daily Completions</h4>
          <p className="text-2xl font-bold">
            {(
              analytics.daily_completions.reduce(
                (acc, day) => acc + day.count,
                0
              ) / 30
            ).toFixed(1)}
          </p>
        </div>
        <div className="card text-center">
          <h4 className="text-sm text-gray-500">High Priority Tasks</h4>
          <p className="text-2xl font-bold text-red-600">
            {analytics.priority_distribution.high || 0}
          </p>
        </div>
      </div>
    </div>
  );
};
```

**Entregable:** Dashboard de analytics con gráficos interactivos

#### **E3.3: Sistema de Equipos y Colaboración**

**Objetivo:** Agregar funcionalidades de trabajo en equipo

**Backend Models:**

```python
# app/models/team.py
class Team(Base, TimestampMixin):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relaciones
    owner = relationship("User", back_populates="owned_teams")
    members = relationship("TeamMember", back_populates="team")
    projects = relationship("Project", back_populates="team")

class TeamMember(Base, TimestampMixin):
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(Enum(TeamRole), default=TeamRole.MEMBER)

    # Relaciones
    team = relationship("Team", back_populates="members")
    user = relationship("User", back_populates="team_memberships")

class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    team_id = Column(Integer, ForeignKey("teams.id"), nullable=False)

    # Relaciones
    team = relationship("Team", back_populates="projects")
    tasks = relationship("Task", back_populates="project")
```

**Team Management Service:**

```python
# app/services/team_service.py
class TeamService:
    def __init__(self, team_repo: TeamRepository, user_repo: UserRepository):
        self.team_repo = team_repo
        self.user_repo = user_repo

    async def create_team(self, team_data: TeamCreate, owner_id: int) -> TeamResponse:
        team = await self.team_repo.create(team_data, owner_id)

        # Agregar owner como admin del equipo
        await self.team_repo.add_member(team.id, owner_id, TeamRole.ADMIN)

        return TeamResponse.from_orm(team)

    async def invite_member(self, team_id: int, email: str, current_user_id: int) -> bool:
        # Verificar permisos
        if not await self.team_repo.user_can_manage(team_id, current_user_id):
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        # Buscar usuario
        user = await self.user_repo.get_by_email(email)
        if not user:
            # Enviar invitación por email para registrarse
            await self._send_invite_email(email, team_id)
            return True

        # Agregar directamente
        await self.team_repo.add_member(team_id, user.id, TeamRole.MEMBER)

        # Notificar
        await self.notification_service.send_notification(
            user_id=user.id,
            notification_type=NotificationType.TEAM_INVITE,
            title="Team Invitation",
            message=f"You've been invited to join a team"
        )

        return True
```

**Frontend Team Management:**

```typescript
// src/components/teams/TeamDashboard.tsx
export const TeamDashboard: React.FC = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeam, setSelectedTeam] = useState<Team | null>(null);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold">Teams</h1>
        <button className="btn-primary">Create Team</button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Your Teams</h2>
          {teams.map((team) => (
            <div
              key={team.id}
              className={`card cursor-pointer transition-colors ${
                selectedTeam?.id === team.id ? 'border-primary-500' : ''
              }`}
              onClick={() => setSelectedTeam(team)}>
              <h3 className="font-medium">{team.name}</h3>
              <p className="text-sm text-gray-600">{team.description}</p>
              <div className="flex items-center justify-between mt-2">
                <span className="text-xs text-gray-500">
                  {team.members.length} members
                </span>
                <span className="text-xs bg-primary-100 text-primary-800 px-2 py-1 rounded">
                  {team.role}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="md:col-span-2">
          {selectedTeam ? (
            <TeamDetails team={selectedTeam} />
          ) : (
            <div className="card text-center text-gray-500">
              Select a team to view details
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
```

**Entregable:** Sistema completo de equipos con invitaciones y gestión de proyectos

---

## 🎯 Guía de Implementación

### **Cronograma Sugerido**

#### **Si tienes 30-45 minutos:**

- Elige 1 ejercicio de Nivel 1
- Enfócate en implementación completa y testing
- Documenta bien el proceso

#### **Si tienes 60-90 minutos:**

- Elige 1 ejercicio de Nivel 2
- O combina 2 ejercicios de Nivel 1
- Incluye tests para las nuevas funcionalidades

#### **Si tienes 90+ minutos:**

- Elige 1 ejercicio de Nivel 3
- O combina ejercicios de niveles anteriores
- Considera el impacto en tu portfolio objetivo

### **Criterios de Selección**

#### **Para maximizar empleabilidad en Backend:**

- E2.1 (Comentarios) + E3.1 (Notificaciones)
- E3.2 (Analytics) si apuntas a roles de datos

#### **Para maximizar empleabilidad en Frontend:**

- E1.1 (Tema personalizado) + E2.3 (Drag & Drop)
- E3.2 (Analytics Dashboard) para demostrar skills de visualización

#### **Para maximizar empleabilidad Full-Stack:**

- E2.1 (Comentarios) + E1.3 (Loading states)
- E3.3 (Equipos) para demostrar pensamiento de producto

### **Documentación Requerida**

Para cada ejercicio implementado, incluir:

1. **Justificación técnica** - ¿Por qué elegiste esta feature?
2. **Decisiones de implementación** - ¿Qué alternativas consideraste?
3. **Challenges y soluciones** - ¿Qué problemas enfrentaste?
4. **Impacto en UX** - ¿Cómo mejora la experiencia del usuario?
5. **Tests implementados** - ¿Cómo validaste que funciona?

### **Tips para el Éxito**

#### **🎯 Enfoque en Calidad**

- Mejor implementar menos features pero muy bien hechas
- Cada feature debe estar completamente terminada
- Incluye error handling y validaciones

#### **📝 Documenta Todo**

- Commit messages descriptivos
- Comments en código complejo
- README actualizado con nuevas features

#### **🧪 Testing es Clave**

- Al menos un test por cada nueva funcionalidad
- Tests de integración para features complejas
- Manual testing exhaustivo

#### **🎨 Consistencia Visual**

- Mantén el design system
- Todas las nuevas UI deben seguir los patrones existentes
- Responsive design en todas las nuevas pantallas

---

**💡 Recuerda: Estos ejercicios son opcionales pero pueden diferenciar significativamente tu proyecto en el mercado laboral. Elige los que mejor se alineen con tus objetivos profesionales.**
