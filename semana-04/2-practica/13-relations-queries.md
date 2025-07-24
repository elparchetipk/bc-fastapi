# Práctica 13: Relaciones y Consultas Avanzadas

**⏱️ Tiempo estimado:** 90 minutos  
**🎯 Objetivo:** Implementar relaciones entre modelos y consultas complejas con SQLAlchemy

## 📋 En esta práctica aprenderás

- Relaciones One-to-Many y Many-to-Many
- Foreign Keys y referencias
- Joins y consultas relacionales
- Carga eager y lazy de relaciones
- Consultas complejas con filtros y agregaciones

## 🗂️ Estructura del Proyecto

```
mi_api_tienda/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py        # ← NUEVO
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py        # ← NUEVO
│   └── crud/
│       ├── __init__.py
│       ├── user.py
│       ├── product.py
│       └── order.py        # ← NUEVO
└── requirements.txt
```

## 🔧 Paso 1: Modelo Order con Relaciones

Crea `app/models/order.py`:

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Tabla intermedia para Many-to-Many entre Orders y Products
order_products = Table(
    'order_products',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('quantity', Integer, default=1),
    Column('unit_price', Float)
)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)
    customer_email = Column(String, index=True)
    total_amount = Column(Float, default=0.0)
    status = Column(String, default="pending")  # pending, completed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relación One-to-Many con User (un usuario puede tener muchas órdenes)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")

    # Relación Many-to-Many con Products
    products = relationship(
        "Product",
        secondary=order_products,
        back_populates="orders"
    )
```

## 🔧 Paso 2: Actualizar Modelos Existentes

### Actualizar `app/models/user.py`:

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación One-to-Many con Orders
    orders = relationship("Order", back_populates="user")
```

### Actualizar `app/models/product.py`:

```python
from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    price = Column(Float)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    category = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación Many-to-Many con Orders
    orders = relationship(
        "Order",
        secondary="order_products",
        back_populates="products"
    )
```

## 🔧 Paso 3: Schemas para Orders

Crea `app/schemas/order.py`:

```python
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.schemas.user import UserBase
from app.schemas.product import ProductBase

class OrderProductBase(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="Cantidad debe ser mayor a 0")
    unit_price: Optional[float] = None

class OrderProductCreate(OrderProductBase):
    pass

class OrderProductResponse(OrderProductBase):
    product: ProductBase

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_email: str = Field(..., description="Email del cliente")
    status: str = Field(default="pending", description="Estado de la orden")

class OrderCreate(OrderBase):
    products: List[OrderProductCreate] = Field(..., description="Productos en la orden")

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    customer_email: Optional[str] = None

class OrderResponse(OrderBase):
    id: int
    order_number: str
    total_amount: float
    created_at: datetime
    updated_at: Optional[datetime]
    user: Optional[UserBase] = None
    products: List[OrderProductResponse] = []

    class Config:
        from_attributes = True

class OrderSummary(BaseModel):
    id: int
    order_number: str
    customer_email: str
    total_amount: float
    status: str
    created_at: datetime
    product_count: int

    class Config:
        from_attributes = True
```

## 🔧 Paso 4: CRUD para Orders

Crea `app/crud/order.py`:

```python
from sqlalchemy.orm import Session, selectinload, joinedload
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from app.models.order import Order, order_products
from app.models.user import User
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate, OrderProductCreate

class OrderCRUD:

    def create_order(self, db: Session, order: OrderCreate, user_id: Optional[int] = None) -> Order:
        """Crear una nueva orden con productos"""

        # Generar número de orden único
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"

        # Crear la orden base
        db_order = Order(
            order_number=order_number,
            customer_email=order.customer_email,
            status=order.status,
            user_id=user_id
        )

        db.add(db_order)
        db.flush()  # Para obtener el ID sin hacer commit

        total_amount = 0.0

        # Procesar cada producto
        for order_product in order.products:
            # Verificar que el producto existe y tiene stock
            product = db.query(Product).filter(Product.id == order_product.product_id).first()
            if not product:
                raise ValueError(f"Producto con ID {order_product.product_id} no encontrado")

            if product.stock < order_product.quantity:
                raise ValueError(f"Stock insuficiente para {product.name}")

            # Usar precio actual del producto si no se especifica
            unit_price = order_product.unit_price or product.price
            total_amount += unit_price * order_product.quantity

            # Actualizar stock
            product.stock -= order_product.quantity

            # Crear relación en tabla intermedia
            db.execute(
                order_products.insert().values(
                    order_id=db_order.id,
                    product_id=product.id,
                    quantity=order_product.quantity,
                    unit_price=unit_price
                )
            )

        # Actualizar total de la orden
        db_order.total_amount = total_amount

        db.commit()
        db.refresh(db_order)

        return db_order

    def get_order(self, db: Session, order_id: int) -> Optional[Order]:
        """Obtener orden con relaciones cargadas"""
        return db.query(Order).options(
            selectinload(Order.user),
            selectinload(Order.products)
        ).filter(Order.id == order_id).first()

    def get_order_by_number(self, db: Session, order_number: str) -> Optional[Order]:
        """Obtener orden por número"""
        return db.query(Order).options(
            selectinload(Order.user),
            selectinload(Order.products)
        ).filter(Order.order_number == order_number).first()

    def get_orders(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        user_id: Optional[int] = None
    ) -> List[Order]:
        """Obtener órdenes con filtros opcionales"""
        query = db.query(Order).options(
            selectinload(Order.user),
            selectinload(Order.products)
        )

        if status:
            query = query.filter(Order.status == status)

        if user_id:
            query = query.filter(Order.user_id == user_id)

        return query.order_by(desc(Order.created_at)).offset(skip).limit(limit).all()

    def update_order(self, db: Session, order_id: int, order_update: OrderUpdate) -> Optional[Order]:
        """Actualizar orden"""
        db_order = db.query(Order).filter(Order.id == order_id).first()
        if not db_order:
            return None

        update_data = order_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)

        db.commit()
        db.refresh(db_order)
        return db_order

    def get_orders_summary(self, db: Session, days: int = 30):
        """Obtener resumen de órdenes con estadísticas"""
        since_date = datetime.now() - timedelta(days=days)

        return db.query(
            Order.id,
            Order.order_number,
            Order.customer_email,
            Order.total_amount,
            Order.status,
            Order.created_at,
            func.count(order_products.c.product_id).label('product_count')
        ).outerjoin(order_products).filter(
            Order.created_at >= since_date
        ).group_by(Order.id).order_by(desc(Order.created_at)).all()

    def get_user_orders(self, db: Session, user_id: int) -> List[Order]:
        """Obtener todas las órdenes de un usuario"""
        return db.query(Order).options(
            selectinload(Order.products)
        ).filter(Order.user_id == user_id).order_by(desc(Order.created_at)).all()

    def get_popular_products(self, db: Session, limit: int = 10):
        """Obtener productos más vendidos"""
        return db.query(
            Product.id,
            Product.name,
            func.sum(order_products.c.quantity).label('total_sold'),
            func.count(order_products.c.order_id).label('order_count')
        ).join(order_products).group_by(
            Product.id, Product.name
        ).order_by(desc('total_sold')).limit(limit).all()

# Instancia global del CRUD
order_crud = OrderCRUD()
```

## 🔧 Paso 5: Endpoints con Relaciones

Actualizar `app/main.py` para incluir endpoints de orders:

```python
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.crud.order import order_crud
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate, OrderSummary

app = FastAPI(title="API Tienda con Relaciones", version="2.0.0")

# ... endpoints existentes ...

@app.post("/orders/", response_model=OrderResponse)
def create_order(
    order: OrderCreate,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Crear nueva orden"""
    try:
        return order_crud.create_order(db=db, order=order, user_id=user_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders/", response_model=List[OrderResponse])
def read_orders(
    skip: int = 0,
    limit: int = Query(default=100, le=100),
    status: Optional[str] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Obtener órdenes con filtros opcionales"""
    orders = order_crud.get_orders(
        db=db, skip=skip, limit=limit, status=status, user_id=user_id
    )
    return orders

@app.get("/orders/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    """Obtener orden específica"""
    order = order_crud.get_order(db=db, order_id=order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order

@app.get("/orders/number/{order_number}", response_model=OrderResponse)
def read_order_by_number(order_number: str, db: Session = Depends(get_db)):
    """Obtener orden por número"""
    order = order_crud.get_order_by_number(db=db, order_number=order_number)
    if order is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order

@app.put("/orders/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar orden"""
    order = order_crud.update_order(db=db, order_id=order_id, order_update=order_update)
    if order is None:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    return order

@app.get("/orders-summary/", response_model=List[OrderSummary])
def read_orders_summary(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Obtener resumen de órdenes con estadísticas"""
    return order_crud.get_orders_summary(db=db, days=days)

@app.get("/users/{user_id}/orders", response_model=List[OrderResponse])
def read_user_orders(user_id: int, db: Session = Depends(get_db)):
    """Obtener órdenes de un usuario específico"""
    return order_crud.get_user_orders(db=db, user_id=user_id)

@app.get("/reports/popular-products")
def read_popular_products(
    limit: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Obtener productos más vendidos"""
    return order_crud.get_popular_products(db=db, limit=limit)
```

## 🔧 Paso 6: Crear las Tablas

Actualizar el script de inicialización. Ejecutar:

```bash
# Desde el directorio del proyecto
python -c "
from app.database import engine, Base
from app.models import user, product, order
Base.metadata.create_all(bind=engine)
print('Tablas creadas con éxito')
"
```

## 🧪 Paso 7: Probar las Relaciones

### Datos de Prueba

```python
# script_datos_prueba.py
from sqlalchemy.orm import Session
from app.database import get_db, engine
from app.crud.user import user_crud
from app.crud.product import product_crud
from app.crud.order import order_crud
from app.schemas.user import UserCreate
from app.schemas.product import ProductCreate
from app.schemas.order import OrderCreate, OrderProductCreate

def crear_datos_prueba():
    db = Session(bind=engine)

    # Crear usuarios
    users_data = [
        UserCreate(username="juan_perez", email="juan@email.com", full_name="Juan Pérez"),
        UserCreate(username="maria_lopez", email="maria@email.com", full_name="María López"),
    ]

    users = []
    for user_data in users_data:
        user = user_crud.create_user(db=db, user=user_data)
        users.append(user)
        print(f"Usuario creado: {user.username}")

    # Crear productos
    products_data = [
        ProductCreate(name="Laptop Gaming", description="Laptop para gaming", price=1200.00, stock=10, category="electronics"),
        ProductCreate(name="Mouse Gaming", description="Mouse óptico gaming", price=45.00, stock=50, category="electronics"),
        ProductCreate(name="Teclado Mecánico", description="Teclado mecánico RGB", price=89.99, stock=25, category="electronics"),
    ]

    products = []
    for product_data in products_data:
        product = product_crud.create_product(db=db, product=product_data)
        products.append(product)
        print(f"Producto creado: {product.name}")

    # Crear órdenes con productos
    order_data = OrderCreate(
        customer_email="juan@email.com",
        products=[
            OrderProductCreate(product_id=products[0].id, quantity=1),  # Laptop
            OrderProductCreate(product_id=products[1].id, quantity=2),  # 2 Mouse
        ]
    )

    order = order_crud.create_order(db=db, order=order_data, user_id=users[0].id)
    print(f"Orden creada: {order.order_number} - Total: ${order.total_amount}")

    db.close()

if __name__ == "__main__":
    crear_datos_prueba()
```

### Probar con FastAPI

```bash
# Ejecutar el servidor
uvicorn app.main:app --reload

# Probar endpoints (en otra terminal)
curl -X GET "http://localhost:8000/orders/"
curl -X GET "http://localhost:8000/users/1/orders"
curl -X GET "http://localhost:8000/reports/popular-products"
```

## 📊 Consultas Avanzadas de Ejemplo

```python
# Dentro de order_crud, agregar estos métodos:

def get_orders_with_total_filter(self, db: Session, min_total: float = 0):
    """Órdenes con total mínimo"""
    return db.query(Order).filter(Order.total_amount >= min_total).all()

def get_customers_by_orders_count(self, db: Session):
    """Clientes ordenados por cantidad de órdenes"""
    return db.query(
        Order.customer_email,
        func.count(Order.id).label('order_count'),
        func.sum(Order.total_amount).label('total_spent')
    ).group_by(Order.customer_email).order_by(desc('order_count')).all()

def get_monthly_sales(self, db: Session, year: int):
    """Ventas por mes"""
    return db.query(
        func.extract('month', Order.created_at).label('month'),
        func.count(Order.id).label('orders'),
        func.sum(Order.total_amount).label('revenue')
    ).filter(
        func.extract('year', Order.created_at) == year
    ).group_by('month').order_by('month').all()
```

## ✅ Ejercicios de Práctica

1. **Implementar categorías**: Crear modelo `Category` con relación One-to-Many con productos
2. **Reviews de productos**: Modelo `Review` con relaciones a User y Product
3. **Carrito de compras**: Modelo `Cart` para órdenes no confirmadas
4. **Consulta compleja**: Productos más vendidos por categoría en el último mes

## 🎯 Entregables

- [ ] Modelos con relaciones implementadas
- [ ] CRUD completo para órdenes
- [ ] Endpoints funcionando con datos relacionados
- [ ] Consultas con joins y agregaciones
- [ ] Datos de prueba funcionando

## 📚 Conceptos Clave Aprendidos

- **Foreign Keys**: Referencias entre tablas
- **Relaciones SQLAlchemy**: One-to-Many, Many-to-Many
- **Joins**: Consultas con múltiples tablas
- **Eager/Lazy Loading**: Estrategias de carga de relaciones
- **Agregaciones**: COUNT, SUM, AVG con SQLAlchemy

---

## 🚨 Problemas Comunes

### Error: "Table 'order_products' doesn't exist"

```bash
# Recrear todas las tablas
python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine)"
```

### Error: "Stock insuficiente"

```python
# Verificar stock antes de crear orden
GET /products/{id}  # Revisar campo 'stock'
```

### Relaciones no cargadas

```python
# Usar selectinload para cargar relaciones
query.options(selectinload(Order.products))
```

¡Continúa con la [Práctica 14: Migraciones y Testing](./14-migrations-testing.md)!
