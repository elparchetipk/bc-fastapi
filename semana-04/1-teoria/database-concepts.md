# Teoría - Semana 4: Bases de Datos y ORMs para APIs

## 📚 Conceptos Fundamentales

### 1. ¿Qué son las Bases de Datos en APIs?

Una **base de datos** es un sistema organizado para almacenar, gestionar y recuperar información de manera persistente. En el contexto de APIs REST, las bases de datos proporcionan **persistencia** - los datos sobreviven al reinicio de la aplicación.

#### **Sin Base de Datos (Semanas anteriores)**

```python
# ❌ Datos en memoria - se pierden al reiniciar
productos = [
    {"id": 1, "nombre": "Laptop", "precio": 999.99},
    {"id": 2, "nombre": "Mouse", "precio": 25.99}
]

@app.post("/productos")
def crear_producto(producto: Producto):
    productos.append(producto.dict())  # Se pierde al reiniciar
    return producto
```

#### **Con Base de Datos (Esta semana)**

```python
# ✅ Datos persistentes - sobreviven al reiniciar
@app.post("/productos")
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    db_producto = Producto(**producto.dict())
    db.add(db_producto)
    db.commit()  # Guardado permanente
    db.refresh(db_producto)
    return db_producto
```

---

### 2. Tipos de Bases de Datos

#### **📊 Bases de Datos Relacionales (SQL)**

**Características:**

- **Estructuradas** en tablas con filas y columnas
- **Relaciones** entre tablas (Foreign Keys)
- **ACID** (Atomicidad, Consistencia, Aislamiento, Durabilidad)
- **SQL** como lenguaje de consulta

**Ejemplos:**

- **SQLite** - Archivo local, perfecta para desarrollo
- **PostgreSQL** - Robusta, escalable, open source
- **MySQL** - Popular, amplio soporte
- **SQL Server** - Microsoft, enterprise

```sql
-- Ejemplo SQL básico
CREATE TABLE productos (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2),
    categoria_id INTEGER,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);
```

#### **📄 Bases de Datos NoSQL (No relacionales)**

**Tipos principales:**

- **Documentales** (MongoDB, CouchDB)
- **Clave-Valor** (Redis, DynamoDB)
- **Columnares** (Cassandra, HBase)
- **Grafos** (Neo4j, Amazon Neptune)

**Para esta semana:** Nos enfocamos en **SQLite** (SQL relacional)

---

### 3. ¿Qué es un ORM?

**ORM** (Object-Relational Mapping) es una técnica que permite **mapear** objetos de programación orientada a objetos con registros de una base de datos relacional.

#### **Sin ORM (SQL directo)**

```python
# ❌ SQL directo - propenso a errores, difícil mantenimiento
import sqlite3

def crear_producto(nombre: str, precio: float):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # SQL vulnerable a injection
    query = f"INSERT INTO productos (nombre, precio) VALUES ('{nombre}', {precio})"
    cursor.execute(query)
    conn.commit()
    conn.close()
```

#### **Con ORM (SQLAlchemy)**

```python
# ✅ ORM - seguro, mantenible, pythónico
def crear_producto(producto: ProductoCreate, db: Session):
    db_producto = Producto(
        nombre=producto.nombre,
        precio=producto.precio
    )
    db.add(db_producto)
    db.commit()
    return db_producto
```

#### **Ventajas del ORM:**

1. **🔒 Seguridad** - Previene SQL injection automáticamente
2. **🐍 Pythónico** - Trabajas con objetos Python, no SQL
3. **🔧 Mantenible** - Cambios de esquema más fáciles
4. **🚀 Productividad** - Menos código boilerplate
5. **🔄 Portabilidad** - Cambiar de BD es más fácil

#### **Desventajas del ORM:**

1. **📈 Curva de aprendizaje** - Nuevo concepto a dominar
2. **🐌 Performance** - Puede ser más lento que SQL optimizado
3. **🕳️ Abstraction leaks** - A veces necesitas SQL directo
4. **📦 Dependencia** - Agregás una librería más

---

### 4. SQLAlchemy - El ORM de Python

**SQLAlchemy** es el ORM más popular y poderoso para Python. Tiene dos estilos principales:

#### **Core** (Expresiones SQL)

```python
# SQLAlchemy Core - más parecido a SQL
from sqlalchemy import select

stmt = select(productos).where(productos.c.precio > 100)
result = connection.execute(stmt)
```

#### **ORM** (Objetos Python)

```python
# SQLAlchemy ORM - más pythónico (lo que usaremos)
productos_caros = session.query(Producto).filter(Producto.precio > 100).all()
```

**Para esta semana:** Usamos **SQLAlchemy ORM** con **declarative style**

---

### 5. Arquitectura de una API con Base de Datos

#### **Capas de la Aplicación:**

```
┌─────────────────┐
│   FastAPI       │ ← Endpoints HTTP, validación Pydantic
│   (Presentation)│
├─────────────────┤
│   Business      │ ← Lógica de negocio, reglas específicas
│   Logic         │
├─────────────────┤
│   Data Access   │ ← CRUD operations, SQLAlchemy
│   (Repository)  │
├─────────────────┤
│   Database      │ ← SQLite, PostgreSQL, etc.
│   (Persistence) │
└─────────────────┘
```

#### **Flujo de una Request:**

1. **Cliente** envía HTTP request
2. **FastAPI** recibe y valida request (Pydantic)
3. **Router** llama función correspondiente
4. **CRUD function** interactúa con BD (SQLAlchemy)
5. **Database** persiste/recupera datos
6. **Response** se formatea (Pydantic) y envía al cliente

---

### 6. Modelos en FastAPI + SQLAlchemy

#### **Tres tipos de modelos necesarios:**

#### **1. SQLAlchemy Models (Tabla de BD)**

```python
# models/producto.py
from sqlalchemy import Column, Integer, String, Float

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True)
    precio = Column(Float)
```

#### **2. Pydantic Request Models (Input)**

```python
# schemas/producto.py
class ProductoCreate(BaseModel):
    nombre: str
    precio: float

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
```

#### **3. Pydantic Response Models (Output)**

```python
# schemas/producto.py
class Producto(BaseModel):
    id: int
    nombre: str
    precio: float

    class Config:
        orm_mode = True  # Permite trabajar con objetos SQLAlchemy
```

---

### 7. Relaciones entre Tablas

#### **One-to-Many (Uno a Muchos)**

```python
# Una categoría tiene muchos productos
class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)

    # Relación
    productos = relationship("Producto", back_populates="categoria")

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

    # Relación
    categoria = relationship("Categoria", back_populates="productos")
```

#### **Many-to-Many (Muchos a Muchos)**

```python
# Tabla de asociación
producto_tag_association = Table(
    'producto_tags',
    Base.metadata,
    Column('producto_id', Integer, ForeignKey('productos.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)

    # Relación many-to-many
    tags = relationship("Tag", secondary=producto_tag_association, back_populates="productos")
```

---

### 8. Sesiones y Transacciones

#### **Session - Unidad de Trabajo**

```python
# Una sesión agrupa operaciones relacionadas
def crear_pedido_completo(datos_pedido):
    db = SessionLocal()
    try:
        # Todo en una transacción
        pedido = Pedido(**datos_pedido.dict())
        db.add(pedido)

        for item_data in datos_pedido.items:
            item = ItemPedido(pedido_id=pedido.id, **item_data.dict())
            db.add(item)

        db.commit()  # Todo se guarda junto
        return pedido
    except Exception as e:
        db.rollback()  # Si algo falla, nada se guarda
        raise e
    finally:
        db.close()
```

#### **Dependency Injection en FastAPI**

```python
# Patrón de inyección de dependencias
def get_db():
    db = SessionLocal()
    try:
        yield db  # Proporciona la sesión
    finally:
        db.close()  # Siempre cierra la sesión

@app.post("/productos")
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    # db es automáticamente inyectada y cerrada
    return crud.create_producto(db=db, producto=producto)
```

---

### 9. Migraciones de Base de Datos

#### **¿Qué son las Migraciones?**

Las **migraciones** son scripts que permiten **versionar** y **evolver** el esquema de tu base de datos de manera controlada.

#### **Sin Migraciones**

```python
# ❌ Esquema recreado cada vez - pierdes datos
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```

#### **Con Migraciones (Alembic)**

```bash
# ✅ Evolución controlada del esquema
alembic revision --autogenerate -m "Add productos table"
alembic upgrade head
```

#### **Beneficios:**

- 📜 **Historial** de cambios en BD
- 🔄 **Reversibilidad** - puedes hacer rollback
- 👥 **Trabajo en equipo** - cambios sincronizados
- 🚀 **Deployment** - esquema se actualiza automáticamente

---

### 10. Testing con Bases de Datos

#### **Base de Datos de Prueba**

```python
# Configuración para testing
SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///./test.db"

engine_test = create_engine(SQLALCHEMY_DATABASE_URL_TEST)
TestingSessionLocal = sessionmaker(bind=engine_test)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine_test)
```

#### **Tests de Endpoints**

```python
def test_crear_producto(client, db):
    response = client.post(
        "/productos",
        json={"nombre": "Test Producto", "precio": 99.99}
    )
    assert response.status_code == 200

    # Verificar en BD
    producto = db.query(Producto).filter(Producto.nombre == "Test Producto").first()
    assert producto is not None
    assert producto.precio == 99.99
```

---

### 11. Buenas Prácticas

#### **🔒 Seguridad**

- ✅ **Nunca** hardcodear credenciales de BD
- ✅ **Variables de entorno** para configuración
- ✅ **Validación** de inputs con Pydantic
- ✅ **ORM** previene SQL injection automáticamente

#### **🚀 Performance**

- ✅ **Lazy loading** para relaciones grandes
- ✅ **Paginación** en endpoints que devuelven listas
- ✅ **Índices** en columnas frecuentemente consultadas
- ✅ **Connection pooling** para aplicaciones con carga

#### **🧹 Código Limpio**

- ✅ **Separar** modelos, schemas, y CRUD
- ✅ **Dependency injection** para sesiones de BD
- ✅ **Type hints** en todas las funciones
- ✅ **Documentación** de relaciones complejas

#### **🧪 Testing**

- ✅ **BD de prueba** separada de desarrollo
- ✅ **Fixtures** para datos de test
- ✅ **Teardown** automático después de tests
- ✅ **Test coverage** de operaciones CRUD

---

### 12. Patrón Repository (Opcional/Avanzado)

```python
# Separar lógica de acceso a datos
class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, producto_id: int) -> Optional[Producto]:
        return self.db.query(Producto).filter(Producto.id == producto_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        return self.db.query(Producto).offset(skip).limit(limit).all()

    def create(self, producto: ProductoCreate) -> Producto:
        db_producto = Producto(**producto.dict())
        self.db.add(db_producto)
        self.db.commit()
        self.db.refresh(db_producto)
        return db_producto
```

---

## 🎯 Resumen de Conceptos Clave

### **Para Entender**

1. **Persistencia** vs datos en memoria
2. **ORM** como abstracción sobre SQL
3. **Sesiones** como unidades de trabajo
4. **Relaciones** entre tablas
5. **Migraciones** para evolución de esquema

### **Para Implementar**

1. **SQLAlchemy models** para tablas
2. **Pydantic schemas** para API
3. **CRUD operations** básicas
4. **Dependency injection** para sesiones
5. **Testing** con BD de prueba

### **Para Recordar**

1. **Tres tipos de modelos** (SQLAlchemy, Pydantic Request, Pydantic Response)
2. **Sesiones siempre se cierran** (try/finally o Depends)
3. **ORM previene** SQL injection
4. **Migraciones** son tu historial de cambios
5. **Testing** requiere BD separada

---

## 📚 Referencias Adicionales

### **Documentación Oficial**

- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/14/orm/)
- [FastAPI with SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)

### **Conceptos Avanzados (Para explorar después)**

- **Connection Pooling**
- **Query Optimization**
- **Database Indexing**
- **Async SQLAlchemy**
- **Database Migrations in Production**

---

_Con estos conceptos fundamentales, estás listo para implementar APIs con persistencia real usando SQLAlchemy y FastAPI._
