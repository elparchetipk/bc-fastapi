# Architecture Patterns & Design Principles

## 🏗️ Clean Architecture Implementation

### Layered Architecture Structure

```
src/
├── domain/              # Business Logic Layer
│   ├── entities/        # Core business entities
│   ├── repositories/    # Repository interfaces
│   └── services/        # Business services
├── application/         # Application Layer
│   ├── use_cases/       # Use case implementations
│   ├── dto/             # Data Transfer Objects
│   └── interfaces/      # Port definitions
├── infrastructure/      # Infrastructure Layer
│   ├── database/        # Database implementations
│   ├── external/        # External API clients
│   └── repositories/    # Repository implementations
└── presentation/        # Presentation Layer
    ├── api/             # REST API endpoints
    ├── schemas/         # Pydantic models
    └── middleware/      # HTTP middleware
```

### Domain Layer Implementation

```python
# src/domain/entities/user.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class User:
    """Core User entity - contains business logic"""
    id: Optional[int]
    email: str
    username: str
    hashed_password: str
    is_active: bool
    created_at: datetime

    def activate(self) -> None:
        """Business rule: Activate user account"""
        if self.is_active:
            raise ValueError("User is already active")
        self.is_active = True

    def deactivate(self) -> None:
        """Business rule: Deactivate user account"""
        if not self.is_active:
            raise ValueError("User is already inactive")
        self.is_active = False

    def can_login(self) -> bool:
        """Business rule: Check if user can login"""
        return self.is_active

    def update_email(self, new_email: str) -> None:
        """Business rule: Update user email with validation"""
        if not self._is_valid_email(new_email):
            raise ValueError("Invalid email format")
        self.email = new_email

    def _is_valid_email(self, email: str) -> bool:
        """Private validation logic"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

# src/domain/repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.user import User

class UserRepository(ABC):
    """Abstract repository interface - defines contract"""

    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        pass

    @abstractmethod
    async def list_active(self, limit: int = 10, offset: int = 0) -> List[User]:
        pass
```

### Use Cases (Application Layer)

```python
# src/application/use_cases/create_user.py
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.application.interfaces.password_hasher import PasswordHasher
from src.application.interfaces.email_service import EmailService
from src.application.dto.user_dto import CreateUserRequest, UserResponse

class CreateUserUseCase:
    """Use case for creating a new user - orchestrates business logic"""

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        email_service: EmailService
    ):
        self._user_repository = user_repository
        self._password_hasher = password_hasher
        self._email_service = email_service

    async def execute(self, request: CreateUserRequest) -> UserResponse:
        """Main execution logic"""

        # 1. Validate business rules
        existing_user = await self._user_repository.get_by_email(request.email)
        if existing_user:
            raise ValueError("User with this email already exists")

        # 2. Create domain entity
        hashed_password = await self._password_hasher.hash(request.password)
        user = User(
            id=None,
            email=request.email,
            username=request.username,
            hashed_password=hashed_password,
            is_active=True,
            created_at=datetime.utcnow()
        )

        # 3. Persist entity
        created_user = await self._user_repository.create(user)

        # 4. Side effects (email notification)
        await self._email_service.send_welcome_email(created_user.email)

        # 5. Return response DTO
        return UserResponse.from_entity(created_user)

# src/application/dto/user_dto.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from src.domain.entities.user import User

class CreateUserRequest(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> 'UserResponse':
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at
        )
```

## 🔌 Dependency Injection

### DI Container Setup

```python
# src/container.py
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from src.infrastructure.database.connection import Database
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.infrastructure.services.password_hasher_impl import PasswordHasherImpl
from src.infrastructure.services.email_service_impl import EmailServiceImpl
from src.application.use_cases.create_user import CreateUserUseCase

class Container(containers.DeclarativeContainer):
    """DI Container - manages all dependencies"""

    # Configuration
    config = providers.Configuration()

    # Database
    database = providers.Singleton(
        Database,
        database_url=config.database_url
    )

    # Repositories
    user_repository = providers.Factory(
        UserRepositoryImpl,
        session_factory=database.provided.session_factory
    )

    # Services
    password_hasher = providers.Singleton(PasswordHasherImpl)
    email_service = providers.Singleton(
        EmailServiceImpl,
        smtp_host=config.smtp_host,
        smtp_port=config.smtp_port
    )

    # Use Cases
    create_user_use_case = providers.Factory(
        CreateUserUseCase,
        user_repository=user_repository,
        password_hasher=password_hasher,
        email_service=email_service
    )

# FastAPI integration
@inject
async def create_user_endpoint(
    request: CreateUserRequest,
    use_case: CreateUserUseCase = Provide[Container.create_user_use_case]
) -> UserResponse:
    return await use_case.execute(request)
```

## 🎨 Design Patterns Implementation

### Repository Pattern

```python
# src/infrastructure/repositories/user_repository_impl.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from typing import List, Optional

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.infrastructure.database.models import UserModel

class UserRepositoryImpl(UserRepository):
    """Concrete repository implementation"""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def create(self, user: User) -> User:
        async with self._session_factory() as session:
            db_user = UserModel(
                email=user.email,
                username=user.username,
                hashed_password=user.hashed_password,
                is_active=user.is_active,
                created_at=user.created_at
            )
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)

            return self._to_entity(db_user)

    async def get_by_id(self, user_id: int) -> Optional[User]:
        async with self._session_factory() as session:
            result = await session.execute(
                select(UserModel).where(UserModel.id == user_id)
            )
            db_user = result.scalar_one_or_none()
            return self._to_entity(db_user) if db_user else None

    def _to_entity(self, db_user: UserModel) -> User:
        """Convert database model to domain entity"""
        return User(
            id=db_user.id,
            email=db_user.email,
            username=db_user.username,
            hashed_password=db_user.hashed_password,
            is_active=db_user.is_active,
            created_at=db_user.created_at
        )
```

### Factory Pattern

```python
# src/application/factories/user_factory.py
from datetime import datetime
from src.domain.entities.user import User
from src.application.interfaces.password_hasher import PasswordHasher

class UserFactory:
    """Factory for creating User entities"""

    def __init__(self, password_hasher: PasswordHasher):
        self._password_hasher = password_hasher

    async def create_user(
        self,
        email: str,
        username: str,
        password: str,
        is_active: bool = True
    ) -> User:
        """Create a new user with hashed password"""
        hashed_password = await self._password_hasher.hash(password)

        return User(
            id=None,
            email=email,
            username=username,
            hashed_password=hashed_password,
            is_active=is_active,
            created_at=datetime.utcnow()
        )

    def create_admin_user(
        self,
        email: str,
        username: str,
        password: str
    ) -> User:
        """Factory method for admin users"""
        # Admin-specific logic here
        return self.create_user(email, username, password, is_active=True)
```

### Strategy Pattern

```python
# src/application/strategies/notification_strategy.py
from abc import ABC, abstractmethod
from src.domain.entities.user import User

class NotificationStrategy(ABC):
    """Strategy interface for notifications"""

    @abstractmethod
    async def send_welcome_notification(self, user: User) -> bool:
        pass

class EmailNotificationStrategy(NotificationStrategy):
    """Email notification implementation"""

    def __init__(self, email_service):
        self._email_service = email_service

    async def send_welcome_notification(self, user: User) -> bool:
        return await self._email_service.send_welcome_email(user.email)

class SMSNotificationStrategy(NotificationStrategy):
    """SMS notification implementation"""

    def __init__(self, sms_service):
        self._sms_service = sms_service

    async def send_welcome_notification(self, user: User) -> bool:
        return await self._sms_service.send_welcome_sms(user.phone)

class NotificationContext:
    """Context for notification strategies"""

    def __init__(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: NotificationStrategy):
        self._strategy = strategy

    async def send_welcome_notification(self, user: User) -> bool:
        return await self._strategy.send_welcome_notification(user)
```

## 🧪 Testable Architecture

### Unit Testing with Mocks

```python
# tests/unit/use_cases/test_create_user.py
import pytest
from unittest.mock import AsyncMock, Mock
from datetime import datetime

from src.application.use_cases.create_user import CreateUserUseCase
from src.application.dto.user_dto import CreateUserRequest
from src.domain.entities.user import User

@pytest.fixture
def mock_user_repository():
    return AsyncMock()

@pytest.fixture
def mock_password_hasher():
    mock = AsyncMock()
    mock.hash.return_value = "hashed_password_123"
    return mock

@pytest.fixture
def mock_email_service():
    return AsyncMock()

@pytest.fixture
def create_user_use_case(mock_user_repository, mock_password_hasher, mock_email_service):
    return CreateUserUseCase(
        user_repository=mock_user_repository,
        password_hasher=mock_password_hasher,
        email_service=mock_email_service
    )

@pytest.mark.asyncio
async def test_create_user_success(
    create_user_use_case,
    mock_user_repository,
    mock_password_hasher,
    mock_email_service
):
    # Arrange
    request = CreateUserRequest(
        email="test@example.com",
        username="testuser",
        password="password123"
    )

    mock_user_repository.get_by_email.return_value = None
    mock_user_repository.create.return_value = User(
        id=1,
        email=request.email,
        username=request.username,
        hashed_password="hashed_password_123",
        is_active=True,
        created_at=datetime.utcnow()
    )

    # Act
    result = await create_user_use_case.execute(request)

    # Assert
    assert result.email == request.email
    assert result.username == request.username
    assert result.is_active is True

    mock_password_hasher.hash.assert_called_once_with(request.password)
    mock_email_service.send_welcome_email.assert_called_once_with(request.email)

@pytest.mark.asyncio
async def test_create_user_duplicate_email_raises_error(
    create_user_use_case,
    mock_user_repository
):
    # Arrange
    request = CreateUserRequest(
        email="existing@example.com",
        username="testuser",
        password="password123"
    )

    existing_user = User(
        id=1,
        email=request.email,
        username="existing_user",
        hashed_password="hash",
        is_active=True,
        created_at=datetime.utcnow()
    )
    mock_user_repository.get_by_email.return_value = existing_user

    # Act & Assert
    with pytest.raises(ValueError, match="User with this email already exists"):
        await create_user_use_case.execute(request)
```

### Integration Testing

```python
# tests/integration/test_user_repository.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from src.infrastructure.database.models import Base, UserModel
from src.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from src.domain.entities.user import User

@pytest.fixture
async def db_session():
    """Create test database session"""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession)

    async with async_session() as session:
        yield session

    await engine.dispose()

@pytest.fixture
def user_repository(db_session):
    return UserRepositoryImpl(lambda: db_session)

@pytest.mark.asyncio
async def test_create_and_retrieve_user(user_repository):
    # Arrange
    user = User(
        id=None,
        email="test@example.com",
        username="testuser",
        hashed_password="hashed_password",
        is_active=True,
        created_at=datetime.utcnow()
    )

    # Act
    created_user = await user_repository.create(user)
    retrieved_user = await user_repository.get_by_id(created_user.id)

    # Assert
    assert retrieved_user is not None
    assert retrieved_user.email == user.email
    assert retrieved_user.username == user.username
    assert retrieved_user.id is not None
```

## 📊 Architecture Quality Metrics

### Code Quality Metrics

```python
# tools/architecture_metrics.py
import ast
import os
from typing import Dict, List

class ArchitectureAnalyzer:
    """Analyze architecture quality metrics"""

    def __init__(self, src_path: str):
        self.src_path = src_path

    def analyze_layer_dependencies(self) -> Dict[str, List[str]]:
        """Check if layers depend only on allowed layers"""
        dependencies = {}

        for root, dirs, files in os.walk(self.src_path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    layer = self._get_layer(file_path)
                    deps = self._extract_dependencies(file_path)
                    dependencies[layer] = deps

        return dependencies

    def check_dependency_violations(self) -> List[str]:
        """Check for architecture violations"""
        violations = []
        dependencies = self.analyze_layer_dependencies()

        # Define allowed dependencies
        allowed_deps = {
            'presentation': ['application', 'domain'],
            'application': ['domain'],
            'infrastructure': ['application', 'domain'],
            'domain': []  # Domain should not depend on other layers
        }

        for layer, deps in dependencies.items():
            if layer in allowed_deps:
                for dep in deps:
                    if dep not in allowed_deps[layer]:
                        violations.append(f"{layer} → {dep} (violation)")

        return violations

    def _get_layer(self, file_path: str) -> str:
        """Determine which layer a file belongs to"""
        if 'presentation' in file_path or 'api' in file_path:
            return 'presentation'
        elif 'application' in file_path:
            return 'application'
        elif 'infrastructure' in file_path:
            return 'infrastructure'
        elif 'domain' in file_path:
            return 'domain'
        return 'unknown'

    def _extract_dependencies(self, file_path: str) -> List[str]:
        """Extract import dependencies from a Python file"""
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())

        deps = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if 'src.' in alias.name:
                        layer = self._get_layer_from_import(alias.name)
                        if layer:
                            deps.add(layer)
            elif isinstance(node, ast.ImportFrom):
                if node.module and 'src.' in node.module:
                    layer = self._get_layer_from_import(node.module)
                    if layer:
                        deps.add(layer)

        return list(deps)
```

## 🎯 Implementation Roadmap

### Semana 5-6: Architecture Foundations

- Clean Architecture layers setup
- Domain entities implementation
- Repository pattern introduction
- Basic dependency injection

### Semana 7-8: Advanced Patterns

- Use case implementation
- Design patterns (Factory, Strategy)
- Advanced DI container
- Architecture testing

### Semana 9-10: Quality & Testing

- Unit testing strategy
- Integration testing
- Architecture quality metrics
- Refactoring techniques

### Semana 11-12: Production Architecture

- Performance considerations
- Scalability patterns
- Monitoring integration
- Documentation completion

## ✅ Architecture Checklist

### Clean Architecture

- [ ] Clear layer separation
- [ ] Dependency inversion principle
- [ ] Business logic in domain layer
- [ ] Infrastructure abstracted
- [ ] Testable design

### Design Patterns

- [ ] Repository pattern implemented
- [ ] Factory pattern for complex creation
- [ ] Strategy pattern for algorithms
- [ ] Observer pattern for events
- [ ] Dependency injection configured

### Testing Strategy

- [ ] Unit tests for business logic
- [ ] Integration tests for repositories
- [ ] End-to-end tests for use cases
- [ ] Mocking external dependencies
- [ ] Test coverage > 90%

### Quality Metrics

- [ ] Low coupling between layers
- [ ] High cohesion within modules
- [ ] Cyclomatic complexity < 10
- [ ] No circular dependencies
- [ ] Architecture documentation updated
