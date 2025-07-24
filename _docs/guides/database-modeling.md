# Data Modeling & Database Design Best Practices

## 📊 Database Design Principles

### Entity Relationship Design

```sql
-- Core entities with proper relationships
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP WITH TIME ZONE,

    -- Constraints
    CONSTRAINT valid_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    CONSTRAINT valid_username CHECK (username ~* '^[a-zA-Z0-9_]{3,50}$')
);

CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    bio TEXT,
    avatar_url VARCHAR(500),
    birth_date DATE,
    phone VARCHAR(20),
    location VARCHAR(100),
    website VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    slug VARCHAR(250) UNIQUE,
    status VARCHAR(20) DEFAULT 'draft' CHECK (status IN ('draft', 'published', 'archived')),
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Indexes for performance
    UNIQUE(user_id, slug)
);

CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    color VARCHAR(7) DEFAULT '#007bff',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Many-to-many relationship
CREATE TABLE post_tags (
    post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
    tag_id INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (post_id, tag_id)
);
```

### Indexes for Performance

```sql
-- Performance indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_active ON users(is_active) WHERE is_active = TRUE;
CREATE INDEX idx_users_created_at ON users(created_at);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_status ON posts(status);
CREATE INDEX idx_posts_published_at ON posts(published_at) WHERE published_at IS NOT NULL;
CREATE INDEX idx_posts_slug ON posts(slug);

-- Composite indexes for common queries
CREATE INDEX idx_posts_user_status ON posts(user_id, status);
CREATE INDEX idx_posts_status_published ON posts(status, published_at) WHERE status = 'published';

-- Full-text search index
CREATE INDEX idx_posts_search ON posts USING gin(to_tsvector('english', title || ' ' || content));
```

## 🐍 SQLAlchemy Models

### Base Model with Common Fields

```python
# src/infrastructure/database/models/base.py
from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()

class TimestampMixin:
    """Mixin for created_at and updated_at timestamps"""

    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )

class BaseModel(Base, TimestampMixin):
    """Base model with common fields"""
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)

    def to_dict(self) -> dict:
        """Convert model to dictionary"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    def update_from_dict(self, data: dict) -> None:
        """Update model from dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
```

### Domain Models

```python
# src/infrastructure/database/models/user.py
from sqlalchemy import Column, String, Boolean, DateTime, Text, Date, Integer, ForeignKey
from sqlalchemy.orm import relationship, validates
from sqlalchemy.dialects.postgresql import UUID
import uuid
import re

from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    # Core fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # Profile fields
    first_name = Column(String(100))
    last_name = Column(String(100))

    # Status fields
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)

    # Timestamps
    last_login = Column(DateTime(timezone=True))

    # Relationships
    profile = relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")

    # Validation
    @validates('email')
    def validate_email(self, key, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format")
        return email.lower()

    @validates('username')
    def validate_username(self, key, username):
        pattern = r'^[a-zA-Z0-9_]{3,50}$'
        if not re.match(pattern, username):
            raise ValueError("Username must be 3-50 chars, alphanumeric and underscore only")
        return username.lower()

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"

class Profile(BaseModel):
    __tablename__ = "profiles"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    bio = Column(Text)
    avatar_url = Column(String(500))
    birth_date = Column(Date)
    phone = Column(String(20))
    location = Column(String(100))
    website = Column(String(255))

    # Relationships
    user = relationship("User", back_populates="profile")

    @validates('website')
    def validate_website(self, key, website):
        if website and not website.startswith(('http://', 'https://')):
            return f'https://{website}'
        return website

class Post(BaseModel):
    __tablename__ = "posts"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    slug = Column(String(250))
    status = Column(String(20), default='draft', nullable=False)
    published_at = Column(DateTime(timezone=True))

    # Relationships
    author = relationship("User", back_populates="posts")
    tags = relationship("Tag", secondary="post_tags", back_populates="posts")

    # Indexes
    __table_args__ = (
        Index('idx_posts_user_status', 'user_id', 'status'),
        Index('idx_posts_slug', 'slug'),
        CheckConstraint("status IN ('draft', 'published', 'archived')", name='check_post_status'),
        UniqueConstraint('user_id', 'slug', name='unique_user_slug')
    )

    @validates('status')
    def validate_status(self, key, status):
        allowed_statuses = ['draft', 'published', 'archived']
        if status not in allowed_statuses:
            raise ValueError(f"Status must be one of: {allowed_statuses}")
        return status

    def generate_slug(self):
        """Generate URL-friendly slug from title"""
        import re
        import unicodedata

        # Normalize and convert to ASCII
        title = unicodedata.normalize('NFKD', self.title)
        title = title.encode('ascii', 'ignore').decode('ascii')

        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r'[^\w\s-]', '', title).strip().lower()
        slug = re.sub(r'[-\s]+', '-', slug)

        return slug[:250]  # Limit length

# Many-to-many association table
post_tags = Table(
    'post_tags',
    Base.metadata,
    Column('post_id', Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

class Tag(BaseModel):
    __tablename__ = "tags"

    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text)
    color = Column(String(7), default='#007bff')

    # Relationships
    posts = relationship("Post", secondary=post_tags, back_populates="tags")

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name.strip()) < 2:
            raise ValueError("Tag name must be at least 2 characters")
        return name.strip().lower()

    @validates('color')
    def validate_color(self, key, color):
        pattern = r'^#[0-9A-Fa-f]{6}$'
        if color and not re.match(pattern, color):
            raise ValueError("Color must be a valid hex color (e.g., #007bff)")
        return color
```

## 🔄 Database Migrations

### Alembic Advanced Usage

```python
# alembic/versions/001_initial_schema.py
"""Initial schema

Revision ID: 001
Revises:
Create Date: 2024-01-01 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('first_name', sa.String(length=100), nullable=True),
        sa.Column('last_name', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('last_login', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.CheckConstraint("email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'", name='valid_email'),
        sa.CheckConstraint("username ~* '^[a-zA-Z0-9_]{3,50}$'", name='valid_username'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Indexes
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_users_username', 'users', ['username'])
    op.create_index('idx_users_active', 'users', ['is_active'], postgresql_where=sa.text('is_active = true'))

    # Profiles table
    op.create_table(
        'profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('avatar_url', sa.String(length=500), nullable=True),
        sa.Column('birth_date', sa.Date(), nullable=True),
        sa.Column('phone', sa.String(length=20), nullable=True),
        sa.Column('location', sa.String(length=100), nullable=True),
        sa.Column('website', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )

def downgrade() -> None:
    op.drop_table('profiles')
    op.drop_index('idx_users_active', table_name='users')
    op.drop_index('idx_users_username', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    op.drop_table('users')
```

### Data Migrations

```python
# alembic/versions/002_seed_data.py
"""Seed initial data

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 12:00:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Boolean, DateTime
from datetime import datetime
import bcrypt

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Define table structure for data operations
    users_table = table('users',
        column('id', Integer),
        column('email', String),
        column('username', String),
        column('hashed_password', String),
        column('first_name', String),
        column('last_name', String),
        column('is_active', Boolean),
        column('is_verified', Boolean),
        column('is_superuser', Boolean),
        column('created_at', DateTime),
        column('updated_at', DateTime)
    )

    # Create admin user
    admin_password = bcrypt.hashpw(b'admin123!', bcrypt.gensalt()).decode('utf-8')

    op.bulk_insert(users_table, [
        {
            'email': 'admin@fastapi-bootcamp.com',
            'username': 'admin',
            'hashed_password': admin_password,
            'first_name': 'System',
            'last_name': 'Administrator',
            'is_active': True,
            'is_verified': True,
            'is_superuser': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    ])

    # Create default tags
    tags_table = table('tags',
        column('name', String),
        column('description', String),
        column('color', String),
        column('created_at', DateTime),
        column('updated_at', DateTime)
    )

    op.bulk_insert(tags_table, [
        {
            'name': 'python',
            'description': 'Python programming language',
            'color': '#3776ab',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            'name': 'fastapi',
            'description': 'FastAPI web framework',
            'color': '#009688',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        },
        {
            'name': 'tutorial',
            'description': 'Tutorial and learning content',
            'color': '#ff9800',
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
    ])

def downgrade() -> None:
    # Remove seeded data
    op.execute("DELETE FROM users WHERE username = 'admin'")
    op.execute("DELETE FROM tags WHERE name IN ('python', 'fastapi', 'tutorial')")
```

## 🔍 Query Optimization

### Efficient Query Patterns

```python
# src/infrastructure/repositories/optimized_queries.py
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, joinedload, contains_eager
from typing import List, Optional

class OptimizedUserRepository:
    """Repository with optimized query patterns"""

    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def get_users_with_posts_count(self, limit: int = 10) -> List[dict]:
        """Get users with their post count - optimized with subquery"""
        async with self._session_factory() as session:
            # Subquery for post count
            post_count_subq = (
                select(
                    Post.user_id,
                    func.count(Post.id).label('post_count')
                )
                .where(Post.status == 'published')
                .group_by(Post.user_id)
                .subquery()
            )

            # Main query with left join
            result = await session.execute(
                select(
                    User.id,
                    User.username,
                    User.email,
                    func.coalesce(post_count_subq.c.post_count, 0).label('post_count')
                )
                .outerjoin(post_count_subq, User.id == post_count_subq.c.user_id)
                .where(User.is_active == True)
                .limit(limit)
            )

            return [
                {
                    'id': row.id,
                    'username': row.username,
                    'email': row.email,
                    'post_count': row.post_count
                }
                for row in result
            ]

    async def get_user_with_recent_posts(self, user_id: int) -> Optional[User]:
        """Get user with their recent posts - optimized eager loading"""
        async with self._session_factory() as session:
            result = await session.execute(
                select(User)
                .options(
                    selectinload(User.posts)
                    .selectinload(Post.tags)  # Load post tags too
                )
                .where(User.id == user_id)
            )

            user = result.scalar_one_or_none()
            if user:
                # Sort posts by created_at (most recent first)
                user.posts.sort(key=lambda p: p.created_at, reverse=True)

            return user

    async def search_posts_with_filters(
        self,
        search_term: Optional[str] = None,
        tag_names: Optional[List[str]] = None,
        user_id: Optional[int] = None,
        status: str = 'published',
        limit: int = 20,
        offset: int = 0
    ) -> List[Post]:
        """Complex search with multiple filters - optimized"""
        async with self._session_factory() as session:
            query = (
                select(Post)
                .join(User)  # Join to access user data
                .options(
                    contains_eager(Post.author),  # Eager load author
                    selectinload(Post.tags)  # Eager load tags
                )
                .where(Post.status == status)
            )

            # Add search condition
            if search_term:
                search_filter = or_(
                    Post.title.icontains(search_term),
                    Post.content.icontains(search_term),
                    User.username.icontains(search_term)
                )
                query = query.where(search_filter)

            # Add tag filter
            if tag_names:
                query = (
                    query
                    .join(Post.tags)
                    .where(Tag.name.in_(tag_names))
                    .group_by(Post.id, User.id)
                    .having(func.count(Tag.id) == len(tag_names))  # Must have ALL tags
                )

            # Add user filter
            if user_id:
                query = query.where(Post.user_id == user_id)

            # Add ordering and pagination
            query = (
                query
                .order_by(Post.published_at.desc())
                .offset(offset)
                .limit(limit)
            )

            result = await session.execute(query)
            return result.scalars().unique().all()

    async def get_post_statistics(self) -> dict:
        """Get aggregated post statistics"""
        async with self._session_factory() as session:
            result = await session.execute(
                select(
                    func.count(Post.id).label('total_posts'),
                    func.count(Post.id).filter(Post.status == 'published').label('published_posts'),
                    func.count(Post.id).filter(Post.status == 'draft').label('draft_posts'),
                    func.avg(func.length(Post.content)).label('avg_content_length'),
                    func.count(func.distinct(Post.user_id)).label('active_authors')
                )
            )

            row = result.first()
            return {
                'total_posts': row.total_posts or 0,
                'published_posts': row.published_posts or 0,
                'draft_posts': row.draft_posts or 0,
                'avg_content_length': float(row.avg_content_length or 0),
                'active_authors': row.active_authors or 0
            }
```

## 🔐 Database Security

### Row Level Security (RLS)

```sql
-- Enable RLS on sensitive tables
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Policy: Users can only see their own drafts
CREATE POLICY posts_user_isolation ON posts
    FOR ALL TO application_role
    USING (user_id = current_setting('app.current_user_id')::INTEGER OR status = 'published');

-- Policy: Only post authors can update their posts
CREATE POLICY posts_update_own ON posts
    FOR UPDATE TO application_role
    USING (user_id = current_setting('app.current_user_id')::INTEGER);
```

### Connection Security

```python
# src/infrastructure/database/security.py
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool
import ssl

def create_secure_engine(database_url: str, **kwargs):
    """Create database engine with security best practices"""

    # SSL configuration for production
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_REQUIRED

    engine = create_async_engine(
        database_url,
        # Security settings
        connect_args={
            "ssl": ssl_context,
            "command_timeout": 30,
            "server_settings": {
                "application_name": "fastapi_app",
                "jit": "off"  # Disable JIT for predictable performance
            }
        },
        # Connection pool settings
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600,
        # Disable connection pooling in development
        poolclass=NullPool if kwargs.get('development') else None,
        # Query echo (only in development)
        echo=kwargs.get('development', False),
        # JSON serializer for better performance
        json_serializer=orjson.dumps,
        json_deserializer=orjson.loads
    )

    return engine
```

## 📋 Implementation Checklist

### Database Design

- [ ] Normalized schema (3NF minimum)
- [ ] Proper relationships and constraints
- [ ] Indexes on frequently queried columns
- [ ] Check constraints for data validation
- [ ] Proper data types chosen

### SQLAlchemy Models

- [ ] Base model with common fields
- [ ] Proper relationships configured
- [ ] Validation methods implemented
- [ ] Efficient query methods
- [ ] Model serialization methods

### Migrations

- [ ] Version control for schema changes
- [ ] Rollback procedures tested
- [ ] Data migration scripts
- [ ] Production migration strategy
- [ ] Migration testing in staging

### Performance

- [ ] Query optimization implemented
- [ ] N+1 query problems resolved
- [ ] Proper eager loading used
- [ ] Database connection pooling
- [ ] Query performance monitoring

### Security

- [ ] SQL injection prevention
- [ ] Input validation at model level
- [ ] Row-level security (when needed)
- [ ] Secure connection configuration
- [ ] Sensitive data encryption

## 🎯 Implementation Timeline

### Semana 3-4: Database Fundamentals

- Schema design and normalization
- Basic SQLAlchemy models
- Simple CRUD operations
- Migration setup

### Semana 5-6: Advanced Modeling

- Complex relationships
- Model validation
- Query optimization basics
- Advanced migrations

### Semana 7-8: Performance & Security

- Query optimization
- Security implementation
- Connection pooling
- Performance monitoring

### Semana 9-12: Production Ready

- Advanced querying techniques
- Database security hardening
- Performance tuning
- Monitoring and alerting
