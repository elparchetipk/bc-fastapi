# Práctica 12: CRUD con Base de Datos - Semana 4

## 🎯 Objetivo

Implementar operaciones CRUD completas y robustas con SQLAlchemy, incluyendo validaciones avanzadas, manejo de errores específicos de base de datos, y optimizaciones básicas de consultas.

## ⏱️ Tiempo Estimado: 90 minutos

## 📋 Pre-requisitos

- ✅ **Práctica 11 completada** - SQLAlchemy setup funcionando
- ✅ **Base de datos** conectada y modelo Product creado
- ✅ **CRUD básico** implementado y funcionando
- ✅ **Tests** ejecutándose correctamente

## 🏗️ Paso 1: Extender el Modelo Product (15 min)

### **Actualizar app/models/product.py**

```python
"""
Modelo extendido de productos con más funcionalidades
"""
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from app.database import Base

class Product(Base):
    """
    Modelo SQLAlchemy extendido para productos
    """
    __tablename__ = "products"

    # Columnas principales
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=True)  # Text para descripciones largas
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    is_active = Column(Boolean, default=True, index=True)

    # Nuevos campos
    sku = Column(String(50), unique=True, index=True, nullable=True)  # Código único
    category = Column(String(50), index=True, nullable=True)
    weight = Column(Float, nullable=True)  # Peso en kg

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Índices compuestos para optimizar consultas
    __table_args__ = (
        Index('idx_category_active', 'category', 'is_active'),
        Index('idx_price_stock', 'price', 'stock'),
    )

    @validates('price')
    def validate_price(self, key, price):
        """Validar que el precio sea positivo"""
        if price is not None and price <= 0:
            raise ValueError("Price must be positive")
        return price

    @validates('stock')
    def validate_stock(self, key, stock):
        """Validar que el stock no sea negativo"""
        if stock is not None and stock < 0:
            raise ValueError("Stock cannot be negative")
        return stock

    @validates('name')
    def validate_name(self, key, name):
        """Validar nombre del producto"""
        if name and len(name.strip()) == 0:
            raise ValueError("Name cannot be empty")
        return name.strip() if name else name

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}', price={self.price})>"

    @property
    def is_in_stock(self) -> bool:
        """Verificar si el producto tiene stock"""
        return self.stock > 0

    @property
    def value_in_stock(self) -> float:
        """Calcular valor total del stock"""
        return self.price * self.stock if self.price and self.stock else 0
```

## 📨 Paso 2: Actualizar Schemas Pydantic (15 min)

### **Actualizar app/schemas/product.py**

```python
"""
Schemas Pydantic actualizados para productos
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator
from enum import Enum

class ProductCategory(str, Enum):
    """Categorías permitidas para productos"""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    BOOKS = "books"
    HOME = "home"
    SPORTS = "sports"
    OTHER = "other"

class ProductBase(BaseModel):
    """Campos base para productos"""
    name: str = Field(..., min_length=1, max_length=100, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=1000, description="Descripción detallada")
    price: float = Field(..., gt=0, le=999999, description="Precio en USD")
    stock: int = Field(0, ge=0, le=999999, description="Cantidad en inventario")
    is_active: bool = Field(True, description="Producto activo")
    sku: Optional[str] = Field(None, max_length=50, description="Código SKU único")
    category: Optional[ProductCategory] = Field(None, description="Categoría del producto")
    weight: Optional[float] = Field(None, gt=0, le=1000, description="Peso en kilogramos")

    @validator('name')
    def validate_name(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty or whitespace')
        return v.strip()

    @validator('sku')
    def validate_sku(cls, v):
        if v is not None:
            v = v.strip().upper()
            if not v:
                return None
            if len(v) < 3:
                raise ValueError('SKU must be at least 3 characters')
        return v

class ProductCreate(ProductBase):
    """Schema para crear producto"""
    pass

class ProductUpdate(BaseModel):
    """Schema para actualizar producto - todos los campos opcionales"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0, le=999999)
    stock: Optional[int] = Field(None, ge=0, le=999999)
    is_active: Optional[bool] = None
    sku: Optional[str] = Field(None, max_length=50)
    category: Optional[ProductCategory] = None
    weight: Optional[float] = Field(None, gt=0, le=1000)

    @validator('name')
    def validate_name(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Name cannot be empty or whitespace')
        return v.strip() if v else v

    @validator('sku')
    def validate_sku(cls, v):
        if v is not None:
            v = v.strip().upper()
            if not v:
                return None
            if len(v) < 3:
                raise ValueError('SKU must be at least 3 characters')
        return v

class Product(ProductBase):
    """Schema para respuesta de API"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Campos calculados
    is_in_stock: bool = Field(..., description="Si tiene stock disponible")
    value_in_stock: float = Field(..., description="Valor total del stock")

    class Config:
        from_attributes = True

class ProductSummary(BaseModel):
    """Schema resumido para listados"""
    id: int
    name: str
    price: float
    stock: int
    is_active: bool
    category: Optional[ProductCategory] = None
    is_in_stock: bool

    class Config:
        from_attributes = True

class ProductList(BaseModel):
    """Schema para respuesta paginada"""
    items: List[Product]
    total: int
    page: int
    per_page: int
    pages: int
    has_next: bool
    has_prev: bool

class ProductFilters(BaseModel):
    """Schema para filtros de búsqueda"""
    category: Optional[ProductCategory] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    in_stock_only: bool = Field(False, description="Solo productos con stock")
    is_active: Optional[bool] = Field(None, description="Filtrar por estado activo")
    search: Optional[str] = Field(None, max_length=100, description="Búsqueda en nombre y descripción")

    @validator('max_price')
    def validate_price_range(cls, v, values):
        if v is not None and 'min_price' in values and values['min_price'] is not None:
            if v < values['min_price']:
                raise ValueError('max_price must be greater than min_price')
        return v
```

## ⚙️ Paso 3: CRUD Avanzado (25 min)

### **Actualizar app/crud/product.py**

```python
"""
Operaciones CRUD avanzadas para productos
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductFilters

class ProductCRUD:
    """Clase para operaciones CRUD de productos"""

    @staticmethod
    def get_product(db: Session, product_id: int) -> Optional[Product]:
        """Obtener producto por ID"""
        return db.query(Product).filter(Product.id == product_id).first()

    @staticmethod
    def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
        """Obtener producto por SKU"""
        return db.query(Product).filter(Product.sku == sku.upper()).first()

    @staticmethod
    def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[ProductFilters] = None
    ) -> List[Product]:
        """Obtener productos con filtros y paginación"""
        query = db.query(Product)

        if filters:
            query = ProductCRUD._apply_filters(query, filters)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_products_count(db: Session, filters: Optional[ProductFilters] = None) -> int:
        """Obtener total de productos con filtros"""
        query = db.query(Product)

        if filters:
            query = ProductCRUD._apply_filters(query, filters)

        return query.count()

    @staticmethod
    def _apply_filters(query, filters: ProductFilters):
        """Aplicar filtros a la consulta"""
        if filters.category:
            query = query.filter(Product.category == filters.category)

        if filters.min_price is not None:
            query = query.filter(Product.price >= filters.min_price)

        if filters.max_price is not None:
            query = query.filter(Product.price <= filters.max_price)

        if filters.in_stock_only:
            query = query.filter(Product.stock > 0)

        if filters.is_active is not None:
            query = query.filter(Product.is_active == filters.is_active)

        if filters.search:
            search_term = f"%{filters.search}%"
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )

        return query

    @staticmethod
    def create_product(db: Session, product: ProductCreate) -> Product:
        """Crear nuevo producto con validaciones"""
        try:
            # Verificar SKU único si se proporciona
            if product.sku:
                existing_product = ProductCRUD.get_product_by_sku(db, product.sku)
                if existing_product:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Product with SKU '{product.sku}' already exists"
                    )

            # Crear producto
            db_product = Product(**product.model_dump())
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            return db_product

        except IntegrityError as e:
            db.rollback()
            if "UNIQUE constraint failed" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product with this SKU already exists"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database constraint violation"
            )
        except ValueError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    def update_product(
        db: Session,
        product_id: int,
        product_update: ProductUpdate
    ) -> Optional[Product]:
        """Actualizar producto con validaciones"""
        db_product = ProductCRUD.get_product(db, product_id)
        if not db_product:
            return None

        try:
            # Verificar SKU único si se está actualizando
            if product_update.sku is not None:
                existing_product = ProductCRUD.get_product_by_sku(db, product_update.sku)
                if existing_product and existing_product.id != product_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Product with SKU '{product_update.sku}' already exists"
                    )

            # Aplicar actualizaciones
            update_data = product_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_product, field, value)

            db.commit()
            db.refresh(db_product)
            return db_product

        except IntegrityError as e:
            db.rollback()
            if "UNIQUE constraint failed" in str(e):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product with this SKU already exists"
                )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Database constraint violation"
            )
        except ValueError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """Eliminar producto (soft delete recomendado para producción)"""
        db_product = ProductCRUD.get_product(db, product_id)
        if not db_product:
            return False

        try:
            # Soft delete - marcar como inactivo en lugar de eliminar
            db_product.is_active = False
            db.commit()
            return True

            # Hard delete (comentado - usar solo en desarrollo)
            # db.delete(db_product)
            # db.commit()
            # return True

        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error deleting product"
            )

    @staticmethod
    def get_inventory_stats(db: Session) -> Dict[str, Any]:
        """Obtener estadísticas del inventario"""
        total_products = db.query(Product).count()
        active_products = db.query(Product).filter(Product.is_active == True).count()
        out_of_stock = db.query(Product).filter(
            and_(Product.stock == 0, Product.is_active == True)
        ).count()

        total_value = db.query(func.sum(Product.price * Product.stock)).scalar() or 0

        # Productos por categoría
        category_stats = db.query(
            Product.category,
            func.count(Product.id).label('count')
        ).filter(Product.is_active == True).group_by(Product.category).all()

        return {
            "total_products": total_products,
            "active_products": active_products,
            "out_of_stock": out_of_stock,
            "total_inventory_value": round(total_value, 2),
            "categories": [{"category": cat, "count": count} for cat, count in category_stats]
        }

# Instancia global para usar en endpoints
product_crud = ProductCRUD()
```

## 🚀 Paso 4: Actualizar FastAPI Endpoints (25 min)

### **Actualizar app/main.py**

```python
"""
FastAPI application con CRUD avanzado
"""
import math
from fastapi import FastAPI, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import SessionLocal, engine, get_db, Base
from app.models import Product
from app.schemas.product import (
    Product as ProductSchema,
    ProductCreate,
    ProductUpdate,
    ProductList,
    ProductSummary,
    ProductFilters,
    ProductCategory
)
from app.crud.product import product_crud

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce API - Advanced CRUD",
    description="API avanzada para manejo de productos con filtros y validaciones",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/", tags=["Root"])
def read_root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "E-commerce API with Advanced CRUD",
        "version": "2.0.0",
        "docs": "/docs",
        "features": [
            "Advanced filtering",
            "Pagination",
            "Input validation",
            "Error handling",
            "Inventory stats"
        ]
    }

@app.get("/products", response_model=ProductList, tags=["Products"])
def get_products(
    page: int = Query(1, ge=1, description="Página (iniciando en 1)"),
    per_page: int = Query(20, ge=1, le=100, description="Productos por página"),
    category: Optional[ProductCategory] = Query(None, description="Filtrar por categoría"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    in_stock_only: bool = Query(False, description="Solo productos con stock"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo"),
    search: Optional[str] = Query(None, max_length=100, description="Buscar en nombre y descripción"),
    db: Session = Depends(get_db)
):
    """Obtener productos con filtros y paginación avanzada"""

    # Crear filtros
    filters = ProductFilters(
        category=category,
        min_price=min_price,
        max_price=max_price,
        in_stock_only=in_stock_only,
        is_active=is_active,
        search=search
    )

    # Calcular offset
    skip = (page - 1) * per_page

    # Obtener productos y total
    products = product_crud.get_products(db, skip=skip, limit=per_page, filters=filters)
    total = product_crud.get_products_count(db, filters=filters)

    # Calcular paginación
    pages = math.ceil(total / per_page) if total > 0 else 1

    return ProductList(
        items=products,
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1
    )

@app.get("/products/summary", response_model=List[ProductSummary], tags=["Products"])
def get_products_summary(
    limit: int = Query(50, ge=1, le=200, description="Número máximo de productos"),
    db: Session = Depends(get_db)
):
    """Obtener resumen de productos para listados rápidos"""
    products = product_crud.get_products(db, skip=0, limit=limit)
    return products

@app.get("/products/{product_id}", response_model=ProductSchema, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Obtener producto específico por ID"""
    db_product = product_crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    return db_product

@app.get("/products/sku/{sku}", response_model=ProductSchema, tags=["Products"])
def get_product_by_sku(sku: str, db: Session = Depends(get_db)):
    """Obtener producto por SKU"""
    db_product = product_crud.get_product_by_sku(db, sku=sku)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with SKU '{sku}' not found"
        )
    return db_product

@app.post("/products", response_model=ProductSchema, status_code=status.HTTP_201_CREATED, tags=["Products"])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Crear nuevo producto con validaciones avanzadas"""
    return product_crud.create_product(db=db, product=product)

@app.put("/products/{product_id}", response_model=ProductSchema, tags=["Products"])
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar producto existente"""
    db_product = product_crud.update_product(db, product_id, product_update)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )
    return db_product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Eliminar producto (soft delete)"""
    success = product_crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found"
        )

@app.get("/inventory/stats", tags=["Inventory"])
def get_inventory_stats(db: Session = Depends(get_db)):
    """Obtener estadísticas del inventario"""
    return product_crud.get_inventory_stats(db)

@app.get("/health", tags=["Health"])
def health_check(db: Session = Depends(get_db)):
    """Verificar estado de la aplicación y base de datos"""
    try:
        # Test database connection
        db.execute("SELECT 1")
        return {
            "status": "healthy",
            "database": "connected",
            "version": "2.0.0"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 🧪 Paso 5: Tests Avanzados (10 min)

### **Actualizar tests/test_products.py**

```python
"""
Tests avanzados para CRUD de productos
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base

# Configuración de BD de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

def test_create_product_with_sku(client):
    """Test crear producto con SKU"""
    response = client.post(
        "/products",
        json={
            "name": "Test Product",
            "description": "A test product with SKU",
            "price": 99.99,
            "stock": 10,
            "sku": "TEST001",
            "category": "electronics"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["sku"] == "TEST001"
    assert data["category"] == "electronics"

def test_create_duplicate_sku(client):
    """Test error al crear producto con SKU duplicado"""
    # Crear primer producto
    client.post(
        "/products",
        json={
            "name": "First Product",
            "price": 50.0,
            "sku": "DUPLICATE"
        }
    )

    # Intentar crear segundo producto con mismo SKU
    response = client.post(
        "/products",
        json={
            "name": "Second Product",
            "price": 75.0,
            "sku": "DUPLICATE"
        }
    )
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

def test_get_products_with_filters(client):
    """Test obtener productos con filtros"""
    # Crear productos de prueba
    products = [
        {"name": "Laptop", "price": 999.99, "category": "electronics", "stock": 5},
        {"name": "Book", "price": 19.99, "category": "books", "stock": 0},
        {"name": "Shirt", "price": 29.99, "category": "clothing", "stock": 10}
    ]

    for product in products:
        client.post("/products", json=product)

    # Test filtro por categoría
    response = client.get("/products?category=electronics")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["name"] == "Laptop"

    # Test filtro por stock
    response = client.get("/products?in_stock_only=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 2  # Laptop y Shirt tienen stock

def test_get_product_by_sku(client):
    """Test obtener producto por SKU"""
    # Crear producto
    client.post(
        "/products",
        json={
            "name": "SKU Product",
            "price": 100.0,
            "sku": "FIND001"
        }
    )

    # Buscar por SKU
    response = client.get("/products/sku/FIND001")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SKU Product"

def test_update_product(client):
    """Test actualizar producto"""
    # Crear producto
    response = client.post(
        "/products",
        json={
            "name": "Original Name",
            "price": 50.0,
            "stock": 5
        }
    )
    product_id = response.json()["id"]

    # Actualizar producto
    response = client.put(
        f"/products/{product_id}",
        json={
            "name": "Updated Name",
            "price": 75.0
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["price"] == 75.0
    assert data["stock"] == 5  # No cambió

def test_pagination(client):
    """Test paginación"""
    # Crear múltiples productos
    for i in range(25):
        client.post(
            "/products",
            json={
                "name": f"Product {i}",
                "price": 10.0 + i
            }
        )

    # Test primera página
    response = client.get("/products?page=1&per_page=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 10
    assert data["page"] == 1
    assert data["pages"] == 3
    assert data["has_next"] == True
    assert data["has_prev"] == False

def test_inventory_stats(client):
    """Test estadísticas de inventario"""
    # Crear productos de prueba
    products = [
        {"name": "Electronics 1", "price": 100.0, "stock": 5, "category": "electronics"},
        {"name": "Electronics 2", "price": 200.0, "stock": 3, "category": "electronics"},
        {"name": "Book 1", "price": 20.0, "stock": 0, "category": "books"},
    ]

    for product in products:
        client.post("/products", json=product)

    response = client.get("/inventory/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_products"] == 3
    assert data["active_products"] == 3
    assert data["out_of_stock"] == 1
    assert data["total_inventory_value"] == 1100.0  # (100*5) + (200*3) + (20*0)
```

## ✅ Paso 6: Testing y Verificación (5 min)

### **Ejecutar y verificar todo**

```bash
# Recrear BD con nuevo esquema
rm -f ecommerce.db test.db

# Ejecutar aplicación
uvicorn app.main:app --reload

# En otra terminal, probar endpoints avanzados
curl -X POST "http://localhost:8000/products" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Gaming Laptop",
       "description": "High-performance gaming laptop",
       "price": 1299.99,
       "stock": 5,
       "sku": "LAPTOP001",
       "category": "electronics",
       "weight": 2.5
     }'

# Probar filtros
curl "http://localhost:8000/products?category=electronics&in_stock_only=true"

# Probar búsqueda
curl "http://localhost:8000/products?search=gaming"

# Probar estadísticas
curl "http://localhost:8000/inventory/stats"

# Ejecutar tests
pytest tests/ -v
```

### **Verificar en Swagger UI**

1. Ir a `http://localhost:8000/docs`
2. Probar endpoints con diferentes filtros
3. Verificar validaciones de entrada
4. Probar manejo de errores

## 📋 Checklist de Completitud

### **✅ Funcionalidades Implementadas**

- [ ] ✅ **Modelo extendido** con validaciones SQLAlchemy
- [ ] ✅ **Schemas avanzados** con validaciones Pydantic
- [ ] ✅ **CRUD completo** con manejo de errores
- [ ] ✅ **Filtros avanzados** (categoría, precio, stock, búsqueda)
- [ ] ✅ **Paginación** completa con metadatos
- [ ] ✅ **Búsqueda por SKU** único
- [ ] ✅ **Validación de unicidad** en tiempo real
- [ ] ✅ **Soft delete** implementado
- [ ] ✅ **Estadísticas de inventario**
- [ ] ✅ **Tests comprehensivos**

### **✅ Verificaciones Manuales**

1. **Crear producto** con todos los campos
2. **Intentar SKU duplicado** (debe fallar)
3. **Buscar con filtros** múltiples
4. **Paginar resultados** grandes
5. **Actualizar parcialmente** un producto
6. **Eliminar producto** (soft delete)
7. **Ver estadísticas** del inventario

## 🎯 Resultado Esperado

Al finalizar esta práctica tendrás:

- ✅ **CRUD robusto** con validaciones avanzadas
- ✅ **Sistema de filtros** completo y flexible
- ✅ **Paginación** eficiente para grandes datasets
- ✅ **Manejo de errores** específicos de BD
- ✅ **Validaciones** en múltiples capas
- ✅ **Testing comprehensivo** de todas las funcionalidades

## 🚀 Próximos Pasos

Esta práctica prepara para:

- **Práctica 13**: Relaciones entre tablas (Foreign Keys)
- **Práctica 14**: Migraciones con Alembic

## 🆘 Troubleshooting Común

### **Error: "Constraint violation"**

- Verificar unicidad de SKU
- Revisar validaciones de modelo

### **Error: "Page not found"**

- Verificar parámetros de paginación
- Confirmar que hay datos en BD

### **Tests fallan**

```bash
# Limpiar BD de test
rm -f test.db
pytest tests/ -v
```

---

**🎉 ¡Excelente!** Ahora tienes un sistema CRUD completo y robusto, listo para manejar operaciones complejas con validaciones y filtros avanzados.
