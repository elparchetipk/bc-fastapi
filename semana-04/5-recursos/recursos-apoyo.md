# Recursos de Apoyo - Semana 4

## 📚 Referencias Básicas

### Documentación Esencial

- **[FastAPI SQL Tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/)** - Tutorial oficial SQLAlchemy
- **[SQLAlchemy ORM Básico](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)** - Conceptos fundamentales
- **[Pydantic v2](https://docs.pydantic.dev/latest/)** - Validación de datos
- **[pytest Básico](https://docs.pytest.org/en/stable/getting-started.html)** - Testing simple

## 🛠️ Herramientas de Desarrollo

### Editor Recomendado

- **VS Code** con extensiones:
  - Python
  - SQLite Viewer
  - Thunder Client (para probar APIs)

### Cliente de API

- **Thunder Client** (integrado en VS Code)
- **Postman** (alternativa externa)

---

## 📝 Ejemplos de Código Rápido

### Conexión Básica a BD

```python
# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Modelo Simple

```python
# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
```

### Schema Básico

```python
# schemas.py
from pydantic import BaseModel

class UsuarioBase(BaseModel):
    nombre: str
    email: str

class UsuarioCreate(UsuarioBase):
    pass

class Usuario(UsuarioBase):
    id: int

    class Config:
        from_attributes = True
```

---

## 🚀 Comandos Útiles

### SQLAlchemy

```bash
# Crear todas las tablas
python -c "from database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
```

### Testing

```bash
# Ejecutar tests
pytest

# Con verbose
pytest -v

# Con coverage
pytest --cov=app
```

---

## 🆘 Problemas Comunes

### Error: "No module named 'sqlalchemy'"

```bash
pip install sqlalchemy
```

### Error: "Table doesn't exist"

- Asegúrate de crear las tablas con `Base.metadata.create_all()`

### Error 422 en validación

- Revisa que los schemas coincidan con los modelos

---

## 📖 Lectura Adicional (Opcional)

Para quien quiera profundizar más:

- [Real Python - SQLAlchemy Tutorial](https://realpython.com/python-sqlite-sqlalchemy/)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Database Design Patterns](https://www.sqlalchemy.org/features.html)

---

¡Estos recursos te ayudarán a completar exitosamente la Semana 4! 🎉
