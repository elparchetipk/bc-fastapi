# 🗄️ SQLAlchemy Setup - Configuración de Base de Datos

## 📋 Introducción

SQLAlchemy es el ORM (Object-Relational Mapping) más popular de Python. En esta práctica configuraremos la base de datos para nuestro proyecto FastAPI.

## ⏱️ Tiempo estimado: 30 minutos

## 🎯 Objetivos

- Instalar SQLAlchemy y dependencias
- Configurar la conexión a base de datos
- Crear el primer modelo simple
- Conectar FastAPI con la base de datos

## 📦 Instalación

```bash
pip install sqlalchemy
pip install python-dotenv
```

Para diferentes bases de datos:

```bash
# SQLite (ya incluido en Python)
# No necesitas instalar nada adicional

# PostgreSQL (si planeas usar PostgreSQL)
pip install psycopg2-binary

# MySQL (si planeas usar MySQL)
pip install pymysql
```

## ⚙️ Configuración Básica

### 1. Estructura de Archivos

```text
proyecto/
├── .env              # Variables de entorno
├── database.py       # Configuración de la base de datos
├── models.py        # Modelos SQLAlchemy (básicos)
└── main.py          # Aplicación FastAPI
```

### 2. Variables de Entorno (`.env`)

```env
# Para desarrollo local con SQLite
DATABASE_URL=sqlite:///./fastapi_app.db

# Para PostgreSQL (comentado por ahora)
# DATABASE_URL=postgresql://username:password@localhost/dbname
```

### 3. Configuración de Base de Datos (`database.py`)

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# URL de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Crear engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Solo necesario para SQLite
)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Función para obtener la sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 4. Primer Modelo Simple (`models.py`)

```python
from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Integer, nullable=False)  # Precio en centavos
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
```

### 5. Integración Básica con FastAPI (`main.py`)

```python
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI con SQLAlchemy",
    description="Setup básico de base de datos",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "FastAPI con SQLAlchemy funcionando!"}

@app.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    """Endpoint para probar la conexión a la base de datos"""
    try:
        # Realizar una consulta simple
        result = db.execute("SELECT 1").fetchone()
        return {"database": "connected", "test_query": result[0]}
    except Exception as e:
        return {"database": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🧪 Probar la Configuración

1. **Ejecutar la aplicación:**

```bash
uvicorn main:app --reload
```

2. **Probar endpoints:**

```bash
# Endpoint básico
curl http://localhost:8000/

# Probar conexión a base de datos
curl http://localhost:8000/test-db
```

3. **Verificar que se creó la base de datos:**
   - Deberías ver un archivo `fastapi_app.db` en tu directorio
   - El endpoint `/test-db` debería retornar `{"database": "connected", "test_query": 1}`

## 📁 Estructura Final

Al completar esta práctica tendrás:

```text
proyecto/
├── .env              # ✅ Variables de entorno
├── database.py       # ✅ Configuración de SQLAlchemy
├── models.py         # ✅ Modelo Product básico
├── main.py           # ✅ FastAPI con conexión a BD
└── fastapi_app.db    # ✅ Base de datos SQLite (se crea automáticamente)
```

## ✅ Verificación

Marca como completado cuando:

- [ ] La aplicación inicia sin errores
- [ ] El endpoint `/` responde correctamente
- [ ] El endpoint `/test-db` muestra "connected"
- [ ] Se creó el archivo de base de datos

## 🔍 Troubleshooting

**Error común 1:** `ImportError: No module named 'sqlalchemy'`

```bash
# Solución: Instalar SQLAlchemy
pip install sqlalchemy
```

**Error común 2:** `RuntimeError: There is no current event loop`

```bash
# Solución: Usar uvicorn en lugar de python directamente
uvicorn main:app --reload
```

**Error común 3:** No se encuentra el archivo `.env`

```bash
# Solución: Crear el archivo .env en el directorio raíz
echo "DATABASE_URL=sqlite:///./fastapi_app.db" > .env
```

## 📚 Siguientes Pasos

Una vez completado este setup básico, continuaremos con:

- **Práctica 12:** Operaciones CRUD básicas
- **Práctica 13:** Relaciones entre tablas
- **Práctica 14:** Migraciones y testing

---

**💡 Nota:** Este setup está optimizado para desarrollo local con SQLite. En las siguientes prácticas aprenderemos operaciones CRUD y relaciones más complejas.

# Para SQLite

engine = create_engine(
DATABASE_URL,
connect_args={"check_same_thread": False} # Solo para SQLite
)

# Para PostgreSQL

# engine = create_engine(DATABASE_URL)

# Sesión de base de datos

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos

Base = declarative_base()

# Dependencia para obtener la sesión de BD

def get_db():
db = SessionLocal()
try:
yield db
finally:
db.close()

````

### 3. Variables de Entorno (`.env`)

```env
# SQLite
DATABASE_URL=sqlite:///./fastapi_app.db

# PostgreSQL
# DATABASE_URL=postgresql://username:password@localhost/dbname

# MySQL
# DATABASE_URL=mysql+pymysql://username:password@localhost/dbname
````

## 📊 Modelos SQLAlchemy (`models.py`)

```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación con posts
    posts = relationship("Post", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación con usuario
    owner = relationship("User", back_populates="posts")
```

## 🔗 Esquemas Pydantic (`schemas.py`)

```python
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# Esquemas base
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Esquemas para Post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    owner: User

    class Config:
        from_attributes = True

# Esquemas con relaciones
class UserWithPosts(User):
    posts: List[Post] = []
```

## 🔧 Operaciones CRUD (`crud.py`)

```python
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional
import models
import schemas
from passlib.context import CryptContext

# Configuración de hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# CRUD para Usuario
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

# CRUD para Post
def get_post(db: Session, post_id: int) -> Optional[models.Post]:
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def get_posts(db: Session, skip: int = 0, limit: int = 100) -> List[models.Post]:
    return db.query(models.Post).offset(skip).limit(limit).all()

def get_posts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Post]:
    return db.query(models.Post).filter(models.Post.owner_id == user_id).offset(skip).limit(limit).all()

def create_post(db: Session, post: schemas.PostCreate, user_id: int) -> models.Post:
    db_post = models.Post(**post.dict(), owner_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate) -> Optional[models.Post]:
    db_post = get_post(db, post_id)
    if db_post:
        update_data = post_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_post, field, value)
        db.commit()
        db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int) -> bool:
    db_post = get_post(db, post_id)
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False
```

## 🚀 Integración con FastAPI (`main.py`)

```python
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import crud
from database import engine, get_db

# Crear las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI con SQLAlchemy",
    description="API con base de datos usando SQLAlchemy ORM",
    version="1.0.0"
)

# Endpoints para usuarios
@app.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )

    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.UserWithPosts)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    if not crud.delete_user(db, user_id=user_id):
        raise HTTPException(status_code=404, detail="User not found")

# Endpoints para posts
@app.post("/users/{user_id}/posts/", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post_for_user(user_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # Verificar que el usuario existe
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return crud.create_post(db=db, post=post, user_id=user_id)

@app.get("/posts/", response_model=List[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts

@app.get("/posts/{post_id}", response_model=schemas.Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.put("/posts/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post_update: schemas.PostUpdate, db: Session = Depends(get_db)):
    db_post = crud.update_post(db, post_id=post_id, post_update=post_update)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    if not crud.delete_post(db, post_id=post_id):
        raise HTTPException(status_code=404, detail="Post not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🔍 Consultas Avanzadas

### Filtros y Búsquedas

```python
# En crud.py - Ejemplos de consultas avanzadas

def search_users(db: Session, search_term: str) -> List[models.User]:
    """Buscar usuarios por email o username"""
    return db.query(models.User).filter(
        or_(
            models.User.email.contains(search_term),
            models.User.username.contains(search_term)
        )
    ).all()

def get_active_users(db: Session) -> List[models.User]:
    """Obtener solo usuarios activos"""
    return db.query(models.User).filter(models.User.is_active == True).all()

def get_published_posts(db: Session) -> List[models.Post]:
    """Obtener solo posts publicados"""
    return db.query(models.Post).filter(models.Post.published == True).all()

def get_posts_with_users(db: Session) -> List[models.Post]:
    """Obtener posts con información del usuario (JOIN)"""
    return db.query(models.Post).join(models.User).all()
```

## 📋 Requirements.txt

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
alembic==1.12.1
python-dotenv==1.0.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
email-validator==2.1.0

# Para PostgreSQL
psycopg2-binary==2.9.9

# Para MySQL
# PyMySQL==1.1.0
```

## 🔧 Comandos Útiles

```bash
# Ejecutar la aplicación
uvicorn main:app --reload

# Crear migración con Alembic
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head

# Abrir shell interactivo
python -c "
from database import SessionLocal, engine
from models import Base
Base.metadata.create_all(bind=engine)
db = SessionLocal()
# Aquí puedes hacer consultas manuales
"
```

## 🧪 Pruebas con curl

```bash
# Crear usuario
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "username": "testuser",
       "password": "secretpassword"
     }'

# Obtener usuarios
curl -X GET "http://localhost:8000/users/"

# Crear post para usuario
curl -X POST "http://localhost:8000/users/1/posts/" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Mi primer post",
       "content": "Contenido del post",
       "published": true
     }'

# Obtener posts
curl -X GET "http://localhost:8000/posts/"
```

## 🛠️ Mejores Prácticas

1. **Separación de responsabilidades**: Mantén modelos, esquemas y CRUD en archivos separados
2. **Validación de datos**: Usa Pydantic para validar entrada y salida
3. **Manejo de errores**: Implementa manejo apropiado de errores HTTP
4. **Migraciones**: Usa Alembic para manejar cambios en la base de datos
5. **Variables de entorno**: Nunca hardcodees cadenas de conexión
6. **Sesiones**: Siempre cierra las sesiones de base de datos
7. **Índices**: Agrega índices apropiados para mejorar performance

## 📚 Recursos Adicionales

- [Documentación oficial de SQLAlchemy](https://docs.sqlalchemy.org/)
- [FastAPI con bases de datos](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🎯 Ejercicios Prácticos

1. **Básico**: Agrega un modelo `Category` y relación con `Post`
2. **Intermedio**: Implementa paginación avanzada con metadatos
3. **Avanzado**: Agrega full-text search usando PostgreSQL
4. **Bonus**: Implementa soft delete (borrado lógico)

## 🔍 Debugging y Logs

```python
# En database.py - Para debugging SQL
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Engine con echo para ver SQL queries
engine = create_engine(DATABASE_URL, echo=True)
```

---

Este setup de SQLAlchemy te proporciona una base sólida para trabajar con bases de datos en FastAPI de manera profesional y escalable.
