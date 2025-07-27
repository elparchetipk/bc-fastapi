# Práctica 24: Database Performance Optimization

⏰ **Tiempo:** 90 minutos  
📚 **Prerequisito:** Práctica 23 completada  
🎯 **Objetivo:** Optimizar performance de base de datos con índices, connection pooling y query optimization

## 📋 Contenido de la Práctica

### **Parte 1: Query Analysis y Optimization (30 min)**

1. **EXPLAIN y análisis de queries**
2. **Identificación de queries lentas**
3. **Query optimization techniques**

### **Parte 2: Database Indexing (35 min)**

1. **Tipos de índices y cuándo usarlos**
2. **Creación de índices estratégicos**
3. **Índices compuestos y parciales**

### **Parte 3: Connection Pooling y Async (25 min)**

1. **Configuración de connection pooling**
2. **Operaciones asíncronas**
3. **Monitoring de conexiones**

---

## 🎯 Parte 1: Query Analysis y Optimization (30 min)

### 1.1 Configurar Query Logging

**Archivo: `app/core/database.py`** (actualizar)

```python
"""
Database configuration with performance monitoring.
"""
import logging
import time
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from app.core.config import settings

# Configure SQL logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Database URL with optimizations
DATABASE_URL = (
    f"postgresql://{settings.database_user}:{settings.database_password}"
    f"@{settings.database_host}:{settings.database_port}/{settings.database_name}"
)

# Engine with connection pooling optimizations
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,              # Base number of connections
    max_overflow=30,           # Additional connections if needed
    pool_pre_ping=True,        # Verify connections before use
    pool_recycle=3600,         # Recycle connections every hour
    echo=settings.debug,       # Log SQL queries in debug mode
    echo_pool=settings.debug,  # Log connection pool events
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Query performance monitoring
@event.listens_for(engine, "before_cursor_execute")
def receive_before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log query start time."""
    context._query_start_time = time.time()

@event.listens_for(engine, "after_cursor_execute")
def receive_after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """Log query execution time."""
    total = time.time() - context._query_start_time
    if total > 0.1:  # Log queries slower than 100ms
        logger = logging.getLogger('slow_queries')
        logger.warning(f"Slow query ({total:.4f}s): {statement[:200]}...")

def get_db():
    """Get database session with proper cleanup."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 1.2 Query Analysis Tools

**Archivo: `app/utils/db_profiler.py`** (crear)

```python
"""
Database profiling and analysis utilities.
"""
import time
import logging
from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

class QueryProfiler:
    """Database query profiler for performance analysis."""

    def __init__(self, db: Session):
        self.db = db

    def explain_query(self, query: str, params: dict = None) -> List[Dict[str, Any]]:
        """
        Execute EXPLAIN ANALYZE on a query.

        Args:
            query: SQL query to analyze
            params: Query parameters

        Returns:
            Query execution plan
        """
        explain_query = f"EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON) {query}"

        try:
            result = self.db.execute(text(explain_query), params or {})
            return result.fetchall()[0][0]
        except Exception as e:
            logger.error(f"Failed to explain query: {e}")
            return []

    def profile_query(self, query: str, params: dict = None, iterations: int = 5) -> Dict[str, float]:
        """
        Profile query performance over multiple iterations.

        Args:
            query: SQL query to profile
            params: Query parameters
            iterations: Number of times to execute

        Returns:
            Performance statistics
        """
        execution_times = []

        for _ in range(iterations):
            start_time = time.time()
            try:
                result = self.db.execute(text(query), params or {})
                result.fetchall()  # Ensure all results are fetched
                execution_time = time.time() - start_time
                execution_times.append(execution_time)
            except Exception as e:
                logger.error(f"Query execution failed: {e}")
                return {"error": str(e)}

        return {
            "avg_time": sum(execution_times) / len(execution_times),
            "min_time": min(execution_times),
            "max_time": max(execution_times),
            "total_time": sum(execution_times),
            "iterations": iterations
        }

    def find_slow_queries(self) -> List[Dict[str, Any]]:
        """
        Find slow queries from PostgreSQL stats.

        Returns:
            List of slow queries with statistics
        """
        slow_query_sql = """
        SELECT
            query,
            calls,
            total_exec_time,
            mean_exec_time,
            max_exec_time,
            rows
        FROM pg_stat_statements
        WHERE mean_exec_time > 100  -- Queries slower than 100ms
        ORDER BY mean_exec_time DESC
        LIMIT 20;
        """

        try:
            result = self.db.execute(text(slow_query_sql))
            return [dict(row) for row in result.fetchall()]
        except Exception as e:
            logger.warning(f"Could not fetch slow queries (pg_stat_statements not available): {e}")
            return []

    def analyze_table_stats(self, table_name: str) -> Dict[str, Any]:
        """
        Get table statistics and usage info.

        Args:
            table_name: Name of table to analyze

        Returns:
            Table statistics
        """
        stats_query = """
        SELECT
            schemaname,
            tablename,
            n_tup_ins as inserts,
            n_tup_upd as updates,
            n_tup_del as deletes,
            n_live_tup as live_tuples,
            n_dead_tup as dead_tuples,
            last_vacuum,
            last_autovacuum,
            last_analyze,
            last_autoanalyze
        FROM pg_stat_user_tables
        WHERE tablename = :table_name;
        """

        try:
            result = self.db.execute(text(stats_query), {"table_name": table_name})
            row = result.fetchone()
            return dict(row) if row else {}
        except Exception as e:
            logger.error(f"Failed to get table stats: {e}")
            return {}

    def check_index_usage(self, table_name: str) -> List[Dict[str, Any]]:
        """
        Check index usage statistics for a table.

        Args:
            table_name: Name of table to check

        Returns:
            Index usage statistics
        """
        index_usage_query = """
        SELECT
            indexname,
            idx_tup_read,
            idx_tup_fetch,
            idx_scan,
            idx_blks_read,
            idx_blks_hit
        FROM pg_stat_user_indexes
        WHERE tablename = :table_name
        ORDER BY idx_scan DESC;
        """

        try:
            result = self.db.execute(text(index_usage_query), {"table_name": table_name})
            return [dict(row) for row in result.fetchall()]
        except Exception as e:
            logger.error(f"Failed to get index usage stats: {e}")
            return []
```

### 1.3 Query Optimization Examples

**Archivo: `app/services/optimized_queries.py`** (crear)

```python
"""
Optimized query examples and patterns.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy import and_, or_, func, text

from app.models.user import User
from app.models.task import Task
from app.schemas.user import UserWithStats

class OptimizedQueries:
    """Collection of optimized database queries."""

    @staticmethod
    def get_users_with_task_count(
        db: Session,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get users with their task count using efficient aggregation.

        ❌ Bad: N+1 query problem
        users = db.query(User).all()
        for user in users:
            task_count = db.query(Task).filter(Task.user_id == user.id).count()

        ✅ Good: Single query with JOIN and aggregation
        """
        query = """
        SELECT
            u.id,
            u.email,
            u.full_name,
            u.is_active,
            u.created_at,
            COALESCE(t.task_count, 0) as task_count
        FROM users u
        LEFT JOIN (
            SELECT
                user_id,
                COUNT(*) as task_count
            FROM tasks
            GROUP BY user_id
        ) t ON u.id = t.user_id
        WHERE u.is_active = true
        ORDER BY u.created_at DESC
        LIMIT :limit OFFSET :offset;
        """

        result = db.execute(text(query), {"limit": limit, "offset": offset})
        return [dict(row) for row in result.fetchall()]

    @staticmethod
    def get_user_dashboard_data(db: Session, user_id: int) -> Dict[str, Any]:
        """
        Get comprehensive user dashboard data in a single query.

        ✅ Optimized: Single query with multiple aggregations
        """
        query = """
        SELECT
            u.id,
            u.email,
            u.full_name,
            COUNT(t.id) as total_tasks,
            COUNT(CASE WHEN t.completed = true THEN 1 END) as completed_tasks,
            COUNT(CASE WHEN t.completed = false THEN 1 END) as pending_tasks,
            COUNT(CASE WHEN t.priority = 'high' AND t.completed = false THEN 1 END) as urgent_tasks,
            MAX(t.created_at) as latest_task_date
        FROM users u
        LEFT JOIN tasks t ON u.id = t.user_id
        WHERE u.id = :user_id
        GROUP BY u.id, u.email, u.full_name;
        """

        result = db.execute(text(query), {"user_id": user_id})
        row = result.fetchone()
        return dict(row) if row else {}

    @staticmethod
    def search_tasks_optimized(
        db: Session,
        user_id: int,
        search_term: Optional[str] = None,
        priority: Optional[str] = None,
        completed: Optional[bool] = None,
        limit: int = 50
    ) -> List[Task]:
        """
        Optimized task search with proper indexing strategy.

        ✅ Uses indexes effectively and avoids full table scans
        """
        query = db.query(Task).filter(Task.user_id == user_id)

        # Add filters conditionally to use indexes
        if search_term:
            # Use gin index for full-text search if available
            query = query.filter(
                or_(
                    Task.title.ilike(f"%{search_term}%"),
                    Task.description.ilike(f"%{search_term}%")
                )
            )

        if priority is not None:
            query = query.filter(Task.priority == priority)

        if completed is not None:
            query = query.filter(Task.completed == completed)

        # Order by indexed column for efficient sorting
        return query.order_by(Task.created_at.desc()).limit(limit).all()

    @staticmethod
    def get_task_statistics(db: Session) -> Dict[str, Any]:
        """
        Get system-wide task statistics with efficient aggregation.

        ✅ Single query with multiple aggregations
        """
        query = """
        SELECT
            COUNT(*) as total_tasks,
            COUNT(CASE WHEN completed = true THEN 1 END) as completed_tasks,
            COUNT(CASE WHEN completed = false THEN 1 END) as pending_tasks,
            COUNT(CASE WHEN priority = 'high' THEN 1 END) as high_priority_tasks,
            COUNT(CASE WHEN priority = 'medium' THEN 1 END) as medium_priority_tasks,
            COUNT(CASE WHEN priority = 'low' THEN 1 END) as low_priority_tasks,
            COUNT(DISTINCT user_id) as active_users,
            AVG(EXTRACT(EPOCH FROM (
                CASE
                    WHEN completed = true AND updated_at IS NOT NULL
                    THEN updated_at - created_at
                END
            ))) as avg_completion_time_seconds
        FROM tasks;
        """

        result = db.execute(text(query))
        row = result.fetchone()
        return dict(row) if row else {}

    @staticmethod
    def get_users_with_eager_loading(db: Session, user_ids: List[int]) -> List[User]:
        """
        Get users with their tasks using eager loading to avoid N+1.

        ✅ Efficient eager loading with joinedload
        """
        return (
            db.query(User)
            .options(joinedload(User.tasks))
            .filter(User.id.in_(user_ids))
            .all()
        )

    @staticmethod
    def bulk_update_task_status(
        db: Session,
        task_ids: List[int],
        completed: bool
    ) -> int:
        """
        Bulk update multiple tasks efficiently.

        ✅ Single UPDATE query instead of multiple individual updates
        """
        result = (
            db.query(Task)
            .filter(Task.id.in_(task_ids))
            .update(
                {"completed": completed, "updated_at": func.now()},
                synchronize_session=False
            )
        )
        db.commit()
        return result
```

---

## 🎯 Parte 2: Database Indexing (35 min)

### 2.1 Análisis de Índices Actuales

**Archivo: `scripts/analyze_indexes.py`** (crear)

```python
"""
Script to analyze current database indexes and suggest improvements.
"""
from sqlalchemy import create_engine, text
from app.core.config import settings

def analyze_database_indexes():
    """Analyze current database indexes and performance."""

    engine = create_engine(
        f"postgresql://{settings.database_user}:{settings.database_password}"
        f"@{settings.database_host}:{settings.database_port}/{settings.database_name}"
    )

    with engine.connect() as conn:
        # Get current indexes
        indexes_query = """
        SELECT
            schemaname,
            tablename,
            indexname,
            indexdef
        FROM pg_indexes
        WHERE schemaname = 'public'
        ORDER BY tablename, indexname;
        """

        result = conn.execute(text(indexes_query))
        indexes = result.fetchall()

        print("Current Database Indexes:")
        print("=" * 50)

        current_table = None
        for row in indexes:
            if row.tablename != current_table:
                current_table = row.tablename
                print(f"\nTable: {row.tablename}")
                print("-" * 30)

            print(f"  {row.indexname}")
            print(f"    {row.indexdef}")

        # Check for unused indexes
        unused_indexes_query = """
        SELECT
            schemaname,
            tablename,
            indexname,
            idx_scan,
            idx_tup_read,
            idx_tup_fetch
        FROM pg_stat_user_indexes
        WHERE idx_scan < 10  -- Indexes used less than 10 times
        ORDER BY idx_scan;
        """

        result = conn.execute(text(unused_indexes_query))
        unused_indexes = result.fetchall()

        print("\n\nPotentially Unused Indexes:")
        print("=" * 50)
        for row in unused_indexes:
            print(f"{row.tablename}.{row.indexname} - Scans: {row.idx_scan}")

        # Check for missing indexes on foreign keys
        missing_fk_indexes_query = """
        SELECT
            c.conname AS constraint_name,
            t.relname AS table_name,
            a.attname AS column_name
        FROM pg_constraint c
        JOIN pg_class t ON c.conrelid = t.oid
        JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(c.conkey)
        WHERE c.contype = 'f'
        AND NOT EXISTS (
            SELECT 1 FROM pg_index i
            WHERE i.indrelid = t.oid
            AND a.attnum = ANY(i.indkey)
        );
        """

        result = conn.execute(text(missing_fk_indexes_query))
        missing_fk_indexes = result.fetchall()

        print("\n\nMissing Indexes on Foreign Keys:")
        print("=" * 50)
        for row in missing_fk_indexes:
            print(f"{row.table_name}.{row.column_name}")

if __name__ == "__main__":
    analyze_database_indexes()
```

### 2.2 Migración con Índices Optimizados

**Archivo: `migrations/versions/add_performance_indexes.py`** (crear)

```python
"""Add performance indexes

Revision ID: add_performance_indexes
Revises: previous_revision
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'add_performance_indexes'
down_revision = 'previous_revision'
branch_labels = None
depends_on = None

def upgrade():
    """Add performance-focused indexes."""

    # Indexes for users table
    op.create_index(
        'idx_users_email_active',
        'users',
        ['email'],
        unique=True,
        postgresql_where=sa.text('is_active = true')
    )

    op.create_index(
        'idx_users_created_at',
        'users',
        ['created_at']
    )

    # Indexes for tasks table
    op.create_index(
        'idx_tasks_user_id_completed',
        'tasks',
        ['user_id', 'completed']
    )

    op.create_index(
        'idx_tasks_user_id_priority',
        'tasks',
        ['user_id', 'priority']
    )

    op.create_index(
        'idx_tasks_user_id_created_at',
        'tasks',
        ['user_id', 'created_at']
    )

    op.create_index(
        'idx_tasks_created_at',
        'tasks',
        ['created_at']
    )

    # Partial index for pending high-priority tasks
    op.create_index(
        'idx_tasks_pending_high_priority',
        'tasks',
        ['user_id', 'created_at'],
        postgresql_where=sa.text("completed = false AND priority = 'high'")
    )

    # GIN index for full-text search (if using PostgreSQL)
    op.execute("""
        CREATE INDEX idx_tasks_fulltext_search
        ON tasks
        USING gin(to_tsvector('english', title || ' ' || COALESCE(description, '')))
    """)

    # Composite index for common query patterns
    op.create_index(
        'idx_tasks_status_priority_date',
        'tasks',
        ['completed', 'priority', 'created_at']
    )

def downgrade():
    """Remove performance indexes."""

    # Drop all the indexes we created
    op.drop_index('idx_users_email_active', table_name='users')
    op.drop_index('idx_users_created_at', table_name='users')
    op.drop_index('idx_tasks_user_id_completed', table_name='tasks')
    op.drop_index('idx_tasks_user_id_priority', table_name='tasks')
    op.drop_index('idx_tasks_user_id_created_at', table_name='tasks')
    op.drop_index('idx_tasks_created_at', table_name='tasks')
    op.drop_index('idx_tasks_pending_high_priority', table_name='tasks')
    op.drop_index('idx_tasks_fulltext_search', table_name='tasks')
    op.drop_index('idx_tasks_status_priority_date', table_name='tasks')
```

### 2.3 Estrategias de Indexing en Models

**Archivo: `app/models/task.py`** (actualizar)

```python
"""
Task model with optimized indexing strategy.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Task(Base):
    """Task model with performance-focused indexes."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    priority = Column(String(10), default="medium", nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Foreign Keys with indexes
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    # Relationships
    user = relationship("User", back_populates="tasks")

    # Composite indexes for common query patterns
    __table_args__ = (
        # Most common: filter by user and status
        Index('idx_task_user_completed', 'user_id', 'completed'),

        # Priority filtering by user
        Index('idx_task_user_priority', 'user_id', 'priority'),

        # Date-based queries by user
        Index('idx_task_user_created', 'user_id', 'created_at'),

        # Global date sorting
        Index('idx_task_created_at', 'created_at'),

        # Partial index for urgent pending tasks
        Index(
            'idx_task_urgent_pending',
            'user_id', 'created_at',
            postgresql_where="completed = false AND priority = 'high'"
        ),

        # Composite index for complex filters
        Index('idx_task_status_priority_date', 'completed', 'priority', 'created_at'),

        # Due date index for deadline queries
        Index('idx_task_due_date', 'due_date', postgresql_where='due_date IS NOT NULL'),
    )
```

---

## 🎯 Parte 3: Connection Pooling y Async (25 min)

### 3.1 Advanced Connection Pool Configuration

**Archivo: `app/core/database_async.py`** (crear)

```python
"""
Async database configuration with advanced connection pooling.
"""
import asyncio
import logging
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import QueuePool
from sqlalchemy import event

from app.core.config import settings

logger = logging.getLogger(__name__)

# Async engine with optimized pooling
async_engine = create_async_engine(
    f"postgresql+asyncpg://{settings.database_user}:{settings.database_password}"
    f"@{settings.database_host}:{settings.database_port}/{settings.database_name}",

    # Connection pool settings
    poolclass=QueuePool,
    pool_size=10,              # Base connections in pool
    max_overflow=20,           # Additional connections when needed
    pool_timeout=30,           # Timeout to get connection from pool
    pool_recycle=3600,         # Recycle connections after 1 hour
    pool_pre_ping=True,        # Verify connections before use

    # Async specific settings
    echo=settings.debug,
    future=True,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

class ConnectionPoolMonitor:
    """Monitor connection pool health and performance."""

    def __init__(self):
        self.pool_stats = {
            "connections_created": 0,
            "connections_closed": 0,
            "pool_size": 0,
            "checked_out": 0,
            "overflow": 0,
            "invalid": 0
        }

    def get_pool_status(self) -> dict:
        """Get current connection pool status."""
        pool = async_engine.pool

        return {
            "pool_size": pool.size(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "checked_in": pool.checkedin(),
            "total_connections": pool.size() + pool.overflow(),
            "stats": self.pool_stats.copy()
        }

# Global pool monitor
pool_monitor = ConnectionPoolMonitor()

# Connection pool event listeners
@event.listens_for(async_engine.sync_engine, "connect")
def receive_connect(dbapi_connection, connection_record):
    """Log new database connections."""
    pool_monitor.pool_stats["connections_created"] += 1
    logger.debug("New database connection created")

@event.listens_for(async_engine.sync_engine, "checkout")
def receive_checkout(dbapi_connection, connection_record, connection_proxy):
    """Log connection checkout from pool."""
    logger.debug("Connection checked out from pool")

@event.listens_for(async_engine.sync_engine, "checkin")
def receive_checkin(dbapi_connection, connection_record):
    """Log connection checkin to pool."""
    logger.debug("Connection checked in to pool")

async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session with proper cleanup."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def health_check_db() -> bool:
    """Check database connectivity and pool health."""
    try:
        async with AsyncSessionLocal() as session:
            await session.execute("SELECT 1")
            return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False
```

### 3.2 Async Service Layer

**Arquivo: `app/services/async_task_service.py`** (crear)

```python
"""
Async task service for high-performance operations.
"""
import asyncio
import logging
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload

from app.models.task import Task
from app.models.user import User
from app.core.cache import cache
from app.core.config import settings

logger = logging.getLogger(__name__)

class AsyncTaskService:
    """Async task service for improved performance."""

    @staticmethod
    async def get_task_by_id(db: AsyncSession, task_id: int) -> Optional[Task]:
        """Get task by ID with async operation."""
        cache_key = f"task:{task_id}"

        # Check cache first
        cached_task = cache.get(cache_key)
        if cached_task:
            return Task(**cached_task)

        # Async database query
        result = await db.execute(
            select(Task).where(Task.id == task_id)
        )
        task = result.scalar_one_or_none()

        # Cache the result
        if task:
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority,
                "user_id": task.user_id,
                "created_at": task.created_at.isoformat() if task.created_at else None
            }
            cache.set(cache_key, task_dict, ttl=settings.cache_default_ttl)

        return task

    @staticmethod
    async def get_user_tasks_async(
        db: AsyncSession,
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> List[Task]:
        """Get user tasks with async operation and eager loading."""

        result = await db.execute(
            select(Task)
            .where(Task.user_id == user_id)
            .order_by(Task.created_at.desc())
            .limit(limit)
            .offset(offset)
        )

        return result.scalars().all()

    @staticmethod
    async def bulk_create_tasks(
        db: AsyncSession,
        tasks_data: List[Dict[str, Any]]
    ) -> List[Task]:
        """Bulk create tasks efficiently."""

        tasks = [Task(**task_data) for task_data in tasks_data]

        db.add_all(tasks)
        await db.commit()

        # Refresh all tasks to get IDs
        for task in tasks:
            await db.refresh(task)

        return tasks

    @staticmethod
    async def bulk_update_task_completion(
        db: AsyncSession,
        task_ids: List[int],
        completed: bool
    ) -> int:
        """Bulk update task completion status."""

        result = await db.execute(
            update(Task)
            .where(Task.id.in_(task_ids))
            .values(completed=completed, updated_at=func.now())
        )

        await db.commit()

        # Invalidate cache for updated tasks
        for task_id in task_ids:
            cache.delete(f"task:{task_id}")

        return result.rowcount

    @staticmethod
    async def get_task_statistics_async(db: AsyncSession) -> Dict[str, Any]:
        """Get task statistics with async aggregation."""

        result = await db.execute(
            select(
                func.count(Task.id).label('total_tasks'),
                func.sum(func.case((Task.completed == True, 1), else_=0)).label('completed_tasks'),
                func.sum(func.case((Task.completed == False, 1), else_=0)).label('pending_tasks'),
                func.sum(func.case((Task.priority == 'high', 1), else_=0)).label('high_priority_tasks'),
                func.count(func.distinct(Task.user_id)).label('active_users')
            )
        )

        row = result.first()
        return {
            "total_tasks": row.total_tasks or 0,
            "completed_tasks": row.completed_tasks or 0,
            "pending_tasks": row.pending_tasks or 0,
            "high_priority_tasks": row.high_priority_tasks or 0,
            "active_users": row.active_users or 0
        }

    @staticmethod
    async def concurrent_user_operations(
        db: AsyncSession,
        user_ids: List[int]
    ) -> Dict[int, Dict[str, Any]]:
        """
        Perform concurrent operations for multiple users.
        Demonstrates async performance benefits.
        """

        async def get_user_summary(user_id: int) -> Dict[str, Any]:
            """Get summary for a single user."""
            result = await db.execute(
                select(
                    func.count(Task.id).label('total_tasks'),
                    func.sum(func.case((Task.completed == True, 1), else_=0)).label('completed'),
                    func.sum(func.case((Task.priority == 'high', 1), else_=0)).label('high_priority')
                ).where(Task.user_id == user_id)
            )

            row = result.first()
            return {
                "total_tasks": row.total_tasks or 0,
                "completed": row.completed or 0,
                "high_priority": row.high_priority or 0
            }

        # Execute operations concurrently
        tasks = [get_user_summary(user_id) for user_id in user_ids]
        results = await asyncio.gather(*tasks)

        return dict(zip(user_ids, results))
```

### 3.3 Async Endpoints

**Archivo: `app/routers/async_tasks.py`** (crear)

```python
"""
Async task endpoints for improved performance.
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database_async import get_async_db
from app.services.async_task_service import AsyncTaskService
from app.models.user import User
from app.dependencies import get_current_user
from app.schemas.task import TaskResponse, TaskCreate

router = APIRouter(prefix="/async/tasks", tags=["async-tasks"])

@router.get("/stats", response_model=Dict[str, Any])
async def get_async_task_stats(
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get task statistics with async performance."""
    return await AsyncTaskService.get_task_statistics_async(db)

@router.get("/user/{user_id}", response_model=List[TaskResponse])
async def get_user_tasks_async(
    user_id: int,
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get user tasks with async performance."""
    if user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Access denied")

    tasks = await AsyncTaskService.get_user_tasks_async(
        db, user_id, limit=limit, offset=offset
    )
    return tasks

@router.put("/bulk-complete")
async def bulk_complete_tasks(
    task_ids: List[int],
    completed: bool = True,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Bulk update task completion status."""
    updated_count = await AsyncTaskService.bulk_update_task_completion(
        db, task_ids, completed
    )

    return {
        "message": f"Updated {updated_count} tasks",
        "task_ids": task_ids,
        "completed": completed
    }

@router.get("/concurrent-stats")
async def get_concurrent_user_stats(
    user_ids: List[int] = Query(...),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_user)
):
    """Get stats for multiple users concurrently."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    stats = await AsyncTaskService.concurrent_user_operations(db, user_ids)
    return stats
```

---

## ✅ Checklist de Verificación

### **Query Analysis**

- [ ] Query logging configurado
- [ ] EXPLAIN ANALYZE ejecutado en queries críticas
- [ ] Queries lentas identificadas
- [ ] N+1 problems eliminados

### **Database Indexing**

- [ ] Índices en foreign keys creados
- [ ] Índices compuestos para queries comunes
- [ ] Índices parciales para casos específicos
- [ ] Índices no utilizados identificados

### **Connection Pooling**

- [ ] Connection pool configurado correctamente
- [ ] Pool monitoring implementado
- [ ] Async operations funcionando
- [ ] Health checks implementados

### **Performance Testing**

- [ ] Benchmarks antes/después comparados
- [ ] Connection pool metrics monitoreados
- [ ] Query performance medido
- [ ] Async vs sync performance comparado

---

## 🚨 Troubleshooting Común

### **Error: "Too many connections"**

```python
# Reducir pool size si hay problemas de conexiones
engine = create_engine(
    DATABASE_URL,
    pool_size=5,           # Reducir de 20 a 5
    max_overflow=10,       # Reducir de 30 a 10
)
```

### **Queries muy lentas después de índices**

```sql
-- Actualizar estadísticas de la tabla
ANALYZE tasks;

-- Verificar que el query planner usa los índices
EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM tasks WHERE user_id = 1;
```

### **Pool exhaustion en async operations**

```python
# Limitar concurrencia para evitar exhaustion
semaphore = asyncio.Semaphore(10)  # Max 10 concurrent operations

async def limited_operation():
    async with semaphore:
        # Tu operación aquí
        pass
```

---

## 🎯 Puntos Clave

1. **Measure before optimizing** - Use EXPLAIN ANALYZE
2. **Index strategically** - Focus on common query patterns
3. **Monitor pool health** - Watch connection metrics
4. **Async for I/O bound** - Use async for database operations
5. **Balance read vs write** - Consider index impact on writes

¡Continúa con la **Práctica 25: Middleware y Rate Limiting**! 🚀
