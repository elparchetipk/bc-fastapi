# Práctica 40: Desarrollo Backend Completo

⏰ **Tiempo estimado:** 90 minutos _(mantenido completo)_  
🎯 **Dificultad:** Integrador  
📋 **Prerrequisitos:** Práctica 39 completada

## 🎯 Objetivos de la Práctica

Al finalizar esta práctica, los estudiantes:

1. ✅ **Implementarán los modelos** de datos con SQLAlchemy
2. ✅ **Crearán los esquemas** de validación con Pydantic
3. ✅ **Desarrollarán servicios** de lógica de negocio
4. ✅ **Configurarán autenticación** JWT completa
5. ✅ **Implementarán endpoints** API REST funcionales

**MANTENIDO EN 90MIN:**

- ✅ Backend es el core del portfolio
- ✅ Tiempo completo para API completa y robusta
- ✅ Calidad no comprometida en funcionalidades principales

## 📋 Desarrollo Backend TaskFlow

### **Paso 1: Configuración Principal**

#### **app/main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth, users, tasks, websockets
from app.core.config import settings
from app.core.database import engine
from app.models import base

# Crear tablas en la base de datos
base.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Sistema de gestión de tareas colaborativo",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["tasks"])
app.include_router(websockets.router, prefix="/ws", tags=["websockets"])

@app.get("/")
async def root():
    return {"message": "TaskFlow API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

#### **app/core/config.py**

```python
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "TaskFlow API"
    API_V1_STR: str = "/api/v1"

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://taskflow_user:taskflow_password@localhost:5432/taskflow_db"
    )

    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # CORS
    ALLOWED_HOSTS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    class Config:
        env_file = ".env"

settings = Settings()
```

#### **app/core/database.py**

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### **Paso 2: Modelos de Datos**

#### **app/models/base.py**

```python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

Base = declarative_base()

class TimestampMixin:
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
```

#### **app/models/user.py**

```python
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relaciones
    created_tasks = relationship(
        "Task",
        foreign_keys="[Task.creator_id]",
        back_populates="creator"
    )
    assigned_tasks = relationship(
        "Task",
        foreign_keys="[Task.assignee_id]",
        back_populates="assignee"
    )
```

#### **app/models/task.py**

```python
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.models.base import Base, TimestampMixin
import enum

class TaskPriority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class Task(Base, TimestampMixin):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    due_date = Column(DateTime, nullable=True)

    # Foreign Keys
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relaciones
    creator = relationship(
        "User",
        foreign_keys=[creator_id],
        back_populates="created_tasks"
    )
    assignee = relationship(
        "User",
        foreign_keys=[assignee_id],
        back_populates="assigned_tasks"
    )
```

### **Paso 3: Esquemas Pydantic**

#### **app/schemas/user.py**

```python
from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str

class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    hashed_password: str
```

#### **app/schemas/task.py**

```python
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime
from app.models.task import TaskPriority, TaskStatus
from app.schemas.user import UserResponse

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    assignee_id: Optional[int] = None

    @validator('title')
    def validate_title(cls, v):
        if len(v.strip()) < 3:
            raise ValueError('Title must be at least 3 characters long')
        return v.strip()

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    assignee_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    status: TaskStatus
    creator_id: int
    assignee_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    # Relaciones
    creator: UserResponse
    assignee: Optional[UserResponse] = None

    class Config:
        from_attributes = True

class TaskStatusUpdate(BaseModel):
    status: TaskStatus
```

#### **app/schemas/auth.py**

```python
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    username: str
    password: str
```

### **Paso 4: Seguridad y Autenticación**

#### **app/core/security.py**

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None
```

### **Paso 5: Repositorios**

#### **app/repositories/user_repository.py**

```python
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create(self, user_data: UserCreate) -> User:
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None

        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
```

#### **app/repositories/task_repository.py**

```python
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task)\
            .options(joinedload(Task.creator), joinedload(Task.assignee))\
            .filter(Task.id == task_id).first()

    def create(self, task_data: TaskCreate, creator_id: int) -> Task:
        db_task = Task(
            **task_data.dict(),
            creator_id=creator_id
        )
        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)

        # Cargar relaciones
        return self.db.query(Task)\
            .options(joinedload(Task.creator), joinedload(Task.assignee))\
            .filter(Task.id == db_task.id).first()

    def update(self, task_id: int, task_data: TaskUpdate) -> Optional[Task]:
        task = self.get_by_id(task_id)
        if not task:
            return None

        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task_id: int) -> bool:
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False

        self.db.delete(task)
        self.db.commit()
        return True

    def get_user_tasks(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        return self.db.query(Task)\
            .options(joinedload(Task.creator), joinedload(Task.assignee))\
            .filter((Task.creator_id == user_id) | (Task.assignee_id == user_id))\
            .offset(skip).limit(limit).all()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Task]:
        return self.db.query(Task)\
            .options(joinedload(Task.creator), joinedload(Task.assignee))\
            .offset(skip).limit(limit).all()
```

### **Paso 6: Servicios**

#### **app/services/user_service.py**

```python
from typing import Optional, List
from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.core.security import verify_password

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_data: UserCreate) -> UserResponse:
        # Verificar si el email ya existe
        if self.repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        # Verificar si el username ya existe
        if self.repository.get_by_username(user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

        user = self.repository.create(user_data)
        return UserResponse.from_orm(user)

    def authenticate_user(self, username: str, password: str) -> Optional[UserResponse]:
        user = self.repository.get_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return UserResponse.from_orm(user)

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        return UserResponse.from_orm(user)

    def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        user = self.repository.get_by_username(username)
        if not user:
            return None
        return UserResponse.from_orm(user)

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        user = self.repository.update(user_id, user_data)
        if not user:
            return None
        return UserResponse.from_orm(user)

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = self.repository.get_all(skip, limit)
        return [UserResponse.from_orm(user) for user in users]
```

#### **app/services/task_service.py**

```python
from typing import Optional, List
from fastapi import HTTPException, status
from app.repositories.task_repository import TaskRepository
from app.repositories.user_repository import UserRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatusUpdate

class TaskService:
    def __init__(self, task_repo: TaskRepository, user_repo: UserRepository):
        self.task_repo = task_repo
        self.user_repo = user_repo

    def create_task(self, task_data: TaskCreate, creator_id: int) -> TaskResponse:
        # Verificar que el assignee existe si se proporciona
        if task_data.assignee_id:
            assignee = self.user_repo.get_by_id(task_data.assignee_id)
            if not assignee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Assignee not found"
                )

        task = self.task_repo.create(task_data, creator_id)
        return TaskResponse.from_orm(task)

    def get_task_by_id(self, task_id: int, current_user_id: int) -> Optional[TaskResponse]:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            return None

        # Verificar que el usuario tiene acceso a la tarea
        if task.creator_id != current_user_id and task.assignee_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        return TaskResponse.from_orm(task)

    def update_task(self, task_id: int, task_data: TaskUpdate, current_user_id: int) -> Optional[TaskResponse]:
        # Verificar que la tarea existe y el usuario tiene permisos
        existing_task = self.task_repo.get_by_id(task_id)
        if not existing_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        if existing_task.creator_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only task creator can update task"
            )

        # Verificar assignee si se está actualizando
        if task_data.assignee_id:
            assignee = self.user_repo.get_by_id(task_data.assignee_id)
            if not assignee:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Assignee not found"
                )

        task = self.task_repo.update(task_id, task_data)
        return TaskResponse.from_orm(task)

    def update_task_status(self, task_id: int, status_data: TaskStatusUpdate, current_user_id: int) -> Optional[TaskResponse]:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Solo el creador o assignee pueden cambiar el estado
        if task.creator_id != current_user_id and task.assignee_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )

        update_data = TaskUpdate(status=status_data.status)
        updated_task = self.task_repo.update(task_id, update_data)
        return TaskResponse.from_orm(updated_task)

    def delete_task(self, task_id: int, current_user_id: int) -> bool:
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        if task.creator_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only task creator can delete task"
            )

        return self.task_repo.delete(task_id)

    def get_user_tasks(self, user_id: int, skip: int = 0, limit: int = 100) -> List[TaskResponse]:
        tasks = self.task_repo.get_user_tasks(user_id, skip, limit)
        return [TaskResponse.from_orm(task) for task in tasks]

    def get_all_tasks(self, skip: int = 0, limit: int = 100) -> List[TaskResponse]:
        tasks = self.task_repo.get_all(skip, limit)
        return [TaskResponse.from_orm(task) for task in tasks]
```

### **Paso 7: Dependencias**

#### **app/dependencies/auth.py**

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security import verify_token
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user import UserResponse

security = HTTPBearer()

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    token = credentials.credentials
    username = verify_token(token)

    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = user_service.get_user_by_username(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user

def get_current_active_user(current_user: UserResponse = Depends(get_current_user)) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
```

#### **app/dependencies/services.py**

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.task_repository import TaskRepository
from app.services.user_service import UserService
from app.services.task_service import TaskService

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)

def get_user_service(repo: UserRepository = Depends(get_user_repository)) -> UserService:
    return UserService(repo)

def get_task_service(
    task_repo: TaskRepository = Depends(get_task_repository),
    user_repo: UserRepository = Depends(get_user_repository)
) -> TaskService:
    return TaskService(task_repo, user_repo)
```

### **Paso 8: Endpoints API**

#### **app/api/v1/auth.py**

```python
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.dependencies.services import get_user_service
from app.core.security import create_access_token
from app.core.config import settings

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    """Registrar un nuevo usuario"""
    return user_service.create_user(user_data)

@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    user_service: UserService = Depends(get_user_service)
):
    """Autenticar usuario y obtener token"""
    user = user_service.authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
```

#### **app/api/v1/users.py**

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService
from app.dependencies.services import get_user_service
from app.dependencies.auth import get_current_active_user

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Obtener perfil del usuario actual"""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """Actualizar perfil del usuario actual"""
    updated_user = user_service.update_user(current_user.id, user_data)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return updated_user

@router.get("/", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    current_user: UserResponse = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """Obtener lista de usuarios"""
    return user_service.get_all_users(skip, limit)

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    current_user: UserResponse = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """Obtener usuario por ID"""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
```

#### **app/api/v1/tasks.py**

```python
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStatusUpdate
from app.schemas.user import UserResponse
from app.services.task_service import TaskService
from app.dependencies.services import get_task_service
from app.dependencies.auth import get_current_active_user

router = APIRouter()

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: UserResponse = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """Crear una nueva tarea"""
    return task_service.create_task(task_data, current_user.id)

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: UserResponse = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """Obtener tareas del usuario"""
    return task_service.get_user_tasks(current_user.id, skip, limit)

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: UserResponse = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """Obtener tarea específica"""
    task = task_service.get_task_by_id(task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """Actualizar tarea"""
    return task_service.update_task(task_id, task_data, current_user.id)

@router.put("/{task_id}/status", response_model=TaskResponse)
async def update_task_status(
    task_id: int,
    status_data: TaskStatusUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """Actualizar estado de tarea"""
    return task_service.update_task_status(task_id, status_data, current_user.id)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: UserResponse = Depends(get_current_active_user),
    task_service: TaskService = Depends(get_task_service)
):
    """Eliminar tarea"""
    task_service.delete_task(task_id, current_user.id)
```

### **Paso 9: WebSocket Manager Básico**

#### **app/websockets/manager.py**

```python
from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect
import json

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

        # Enviar mensaje de conexión exitosa
        await websocket.send_text(json.dumps({
            "type": "connection",
            "message": "Connected successfully"
        }))

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    # Conexión cerrada, remover
                    self.disconnect(connection, user_id)

    async def broadcast(self, message: dict):
        for user_id, connections in self.active_connections.items():
            for connection in connections:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    self.disconnect(connection, user_id)

manager = ConnectionManager()
```

#### **app/api/v1/websockets.py**

```python
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from app.websockets.manager import manager
from app.dependencies.auth import get_user_service
from app.services.user_service import UserService

router = APIRouter()

@router.websocket("/notifications/{user_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: int,
    token: str = Query(...),
    user_service: UserService = Depends(get_user_service)
):
    # Aquí deberías validar el token de manera similar a get_current_user
    # Por simplicidad, asumimos que el user_id es válido

    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            # Aquí puedes manejar mensajes del cliente si es necesario
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
```

## 🧪 Testing del Backend

### **Paso 10: Configurar testing básico**

#### **tests/conftest.py**

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db
from app.models.base import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User",
        "password": "testpassword123"
    }
```

## 🚀 Verificación y Testing

### **Paso 11: Ejecutar y probar el backend**

```bash
# Desde el directorio backend/
cd backend

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# En otra terminal, probar endpoints
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "full_name": "Test User",
    "password": "testpass123"
  }'

# Probar login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### **Documentación API Automática**

Una vez ejecutado el servidor, la documentación estará disponible en:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🎯 Entregables de esta Práctica

### ✅ **Backend Completo Funcionando:**

1. **Modelos de datos** implementados con SQLAlchemy
2. **Esquemas de validación** con Pydantic
3. **Autenticación JWT** completa
4. **Endpoints REST** funcionales
5. **Arquitectura en capas** implementada
6. **WebSocket manager** básico
7. **Testing básico** configurado

### 📁 **Estructura implementada:**

```
backend/
├── app/
│   ├── main.py ✅
│   ├── core/ ✅
│   ├── models/ ✅
│   ├── schemas/ ✅
│   ├── services/ ✅
│   ├── repositories/ ✅
│   ├── api/v1/ ✅
│   ├── dependencies/ ✅
│   └── websockets/ ✅
├── tests/ ✅
└── requirements.txt ✅
```

## 📚 Recursos Adicionales

### **Documentación**

- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [SQLAlchemy Relationships](https://docs.sqlalchemy.org/en/20/orm/relationships.html)
- [Pydantic Validation](https://docs.pydantic.dev/latest/usage/validation_decorator/)

---

## 🎯 ¡Backend TaskFlow Completado!

El backend está completamente funcional y listo para ser integrado con el frontend en la siguiente práctica.

**Siguiente:** [Práctica 41 - Frontend e Integración](./41-frontend-integracion.md)

---

**💡 El backend implementa una arquitectura limpia y escalable que servirá como base sólida para el proyecto final.**
