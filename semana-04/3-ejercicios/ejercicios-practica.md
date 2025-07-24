# Ejercicios de Práctica - Semana 4

## 🎯 Objetivo General

Reforzar los conceptos de bases de datos, relaciones, migraciones y testing mediante ejercicios prácticos progresivos.

**⏱️ Tiempo total:** 60-90 minutos  
**📊 Nivel de dificultad:** Intermedio-Avanzado

---

## 📋 Ejercicio 1: Extensión del Modelo de Datos (20 min)

### Contexto

Necesitas extender el sistema de e-commerce con nuevas entidades para mejorar la funcionalidad.

### Tareas

1. **Crear modelo Category** con relación One-to-Many a productos:

```python
# app/models/category.py
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relación One-to-Many con productos
    products = relationship("Product", back_populates="category")
```

2. **Actualizar modelo Product** para incluir la relación:

```python
# Agregar a Product
category_id = Column(Integer, ForeignKey("categories.id"))
category = relationship("Category", back_populates="products")
```

3. **Crear modelo Review** con relaciones a User y Product:

```python
# app/models/review.py
class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)  # 1-5 estrellas
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relaciones
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    user = relationship("User")
    product = relationship("Product")
```

### Verificación

- [ ] Modelos creados correctamente
- [ ] Relaciones definidas en ambas direcciones
- [ ] Migración generada y aplicada exitosamente

---

## 📋 Ejercicio 2: CRUD Completo con Validaciones (25 min)

### Contexto

Implementar operaciones CRUD completas para las nuevas entidades con validaciones de negocio.

### Tareas

1. **Implementar CategoryCRUD** con validaciones:

```python
# app/crud/category.py
class CategoryCRUD:
    def create_category(self, db: Session, category: CategoryCreate) -> Category:
        # Verificar que el nombre no exista
        existing = db.query(Category).filter(Category.name == category.name).first()
        if existing:
            raise ValueError("Categoría ya existe")

        db_category = Category(**category.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    def get_categories_with_product_count(self, db: Session):
        # Obtener categorías con cantidad de productos
        return db.query(
            Category,
            func.count(Product.id).label('product_count')
        ).outerjoin(Product).group_by(Category.id).all()
```

2. **Implementar ReviewCRUD** con lógica de negocio:

```python
# app/crud/review.py
class ReviewCRUD:
    def create_review(self, db: Session, review: ReviewCreate, user_id: int) -> Review:
        # Verificar que el usuario no haya reseñado ya este producto
        existing = db.query(Review).filter(
            Review.user_id == user_id,
            Review.product_id == review.product_id
        ).first()

        if existing:
            raise ValueError("Usuario ya ha reseñado este producto")

        # Validar rating entre 1-5
        if not 1 <= review.rating <= 5:
            raise ValueError("Rating debe estar entre 1 y 5")

        db_review = Review(**review.model_dump(), user_id=user_id)
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        return db_review

    def get_product_rating_average(self, db: Session, product_id: int) -> float:
        result = db.query(func.avg(Review.rating)).filter(
            Review.product_id == product_id
        ).scalar()
        return float(result) if result else 0.0
```

3. **Crear schemas correspondientes**:

```python
# app/schemas/category.py
class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = None
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime
    product_count: Optional[int] = None

    class Config:
        from_attributes = True

# app/schemas/review.py
class ReviewBase(BaseModel):
    rating: int = Field(..., ge=1, le=5, description="Rating entre 1 y 5 estrellas")
    comment: Optional[str] = Field(None, max_length=1000)

class ReviewCreate(ReviewBase):
    product_id: int

class ReviewResponse(ReviewBase):
    id: int
    created_at: datetime
    user: UserBase
    product: ProductBase

    class Config:
        from_attributes = True
```

### Verificación

- [ ] CRUD implementado con validaciones
- [ ] Errores de negocio manejados correctamente
- [ ] Consultas con agregaciones funcionando

---

## 📋 Ejercicio 3: Consultas Complejas y Reportes (20 min)

### Contexto

Crear endpoints para reportes y estadísticas del negocio.

### Tareas

1. **Implementar reporte de productos por categoría**:

```python
@app.get("/reports/products-by-category")
def products_by_category_report(db: Session = Depends(get_db)):
    """Reporte de productos agrupados por categoría"""
    return db.query(
        Category.name.label('category'),
        func.count(Product.id).label('total_products'),
        func.avg(Product.price).label('avg_price'),
        func.sum(Product.stock).label('total_stock')
    ).join(Product).group_by(Category.id, Category.name).all()
```

2. **Implementar top productos por rating**:

```python
@app.get("/reports/top-rated-products")
def top_rated_products(
    limit: int = Query(default=10, le=50),
    db: Session = Depends(get_db)
):
    """Productos mejor valorados"""
    return db.query(
        Product.id,
        Product.name,
        func.avg(Review.rating).label('avg_rating'),
        func.count(Review.id).label('review_count')
    ).join(Review).group_by(
        Product.id, Product.name
    ).having(
        func.count(Review.id) >= 3  # Mínimo 3 reseñas
    ).order_by(desc('avg_rating')).limit(limit).all()
```

3. **Implementar búsqueda avanzada de productos**:

```python
@app.get("/products/search-advanced")
def search_products_advanced(
    q: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    min_rating: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Búsqueda avanzada de productos"""
    query = db.query(Product).join(Category, isouter=True)

    if q:
        query = query.filter(
            or_(
                Product.name.contains(q),
                Product.description.contains(q),
                Category.name.contains(q)
            )
        )

    if category_id:
        query = query.filter(Product.category_id == category_id)

    if min_price:
        query = query.filter(Product.price >= min_price)

    if max_price:
        query = query.filter(Product.price <= max_price)

    if min_rating:
        # Subconsulta para rating promedio
        rating_subquery = db.query(
            Review.product_id,
            func.avg(Review.rating).label('avg_rating')
        ).group_by(Review.product_id).subquery()

        query = query.join(
            rating_subquery,
            Product.id == rating_subquery.c.product_id
        ).filter(rating_subquery.c.avg_rating >= min_rating)

    return query.all()
```

### Verificación

- [ ] Reportes generando datos correctos
- [ ] Filtros combinados funcionando
- [ ] Consultas optimizadas (sin N+1 queries)

---

## 📋 Ejercicio 4: Testing Avanzado (25 min)

### Contexto

Crear tests comprehensivos para las nuevas funcionalidades.

### Tareas

1. **Test de relaciones y constrains**:

```python
# tests/test_relationships.py
def test_category_product_relationship(db_session):
    """Test relación Category-Product"""
    # Crear categoría
    category = Category(name="Electronics", description="Electronic products")
    db_session.add(category)
    db_session.commit()

    # Crear producto con categoría
    product = Product(
        name="Laptop",
        price=999.99,
        stock=5,
        category_id=category.id
    )
    db_session.add(product)
    db_session.commit()

    # Verificar relación
    assert product.category.name == "Electronics"
    assert category.products[0].name == "Laptop"

def test_unique_constraint_category(db_session):
    """Test constraint único en nombre de categoría"""
    # Crear primera categoría
    category1 = Category(name="Test Category")
    db_session.add(category1)
    db_session.commit()

    # Intentar crear segunda con mismo nombre
    category2 = Category(name="Test Category")
    db_session.add(category2)

    with pytest.raises(Exception):  # IntegrityError esperado
        db_session.commit()
```

2. **Test de validaciones de negocio**:

```python
# tests/test_business_logic.py
def test_duplicate_review_validation(client, sample_user_data, sample_product_data):
    """Test que impide reseñas duplicadas del mismo usuario-producto"""
    # Crear usuario y producto
    user_response = client.post("/users/", json=sample_user_data)
    user_id = user_response.json()["id"]

    product_response = client.post("/products/", json=sample_product_data)
    product_id = product_response.json()["id"]

    # Crear primera reseña
    review_data = {
        "rating": 5,
        "comment": "Great product!",
        "product_id": product_id
    }

    response = client.post(f"/reviews/?user_id={user_id}", json=review_data)
    assert response.status_code == 200

    # Intentar crear segunda reseña del mismo usuario-producto
    response = client.post(f"/reviews/?user_id={user_id}", json=review_data)
    assert response.status_code == 400
    assert "ya ha reseñado" in response.json()["detail"]

def test_rating_validation(client, sample_user_data, sample_product_data):
    """Test validación de rating entre 1-5"""
    user_response = client.post("/users/", json=sample_user_data)
    user_id = user_response.json()["id"]

    product_response = client.post("/products/", json=sample_product_data)
    product_id = product_response.json()["id"]

    # Rating inválido (0)
    review_data = {
        "rating": 0,
        "comment": "Invalid rating",
        "product_id": product_id
    }

    response = client.post(f"/reviews/?user_id={user_id}", json=review_data)
    assert response.status_code == 422  # Validation error

    # Rating inválido (6)
    review_data["rating"] = 6
    response = client.post(f"/reviews/?user_id={user_id}", json=review_data)
    assert response.status_code == 422
```

3. **Test de reportes y consultas complejas**:

```python
# tests/test_reports.py
def test_products_by_category_report(client):
    """Test reporte de productos por categoría"""
    # Crear categoría
    category_data = {"name": "Electronics", "description": "Electronic items"}
    category_response = client.post("/categories/", json=category_data)
    category_id = category_response.json()["id"]

    # Crear productos en la categoría
    for i in range(3):
        product_data = {
            "name": f"Product {i+1}",
            "price": 100.0 + i * 50,
            "stock": 10,
            "category_id": category_id
        }
        client.post("/products/", json=product_data)

    # Obtener reporte
    response = client.get("/reports/products-by-category")
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "Electronics"
    assert data[0]["total_products"] == 3
    assert data[0]["avg_price"] == 150.0  # (100 + 150 + 200) / 3

def test_search_products_advanced(client):
    """Test búsqueda avanzada de productos"""
    # Crear datos de prueba (categoría, productos, reseñas)
    # ... crear datos ...

    # Buscar por rango de precio
    response = client.get("/products/search-advanced?min_price=50&max_price=150")
    assert response.status_code == 200

    # Verificar que todos los productos están en el rango
    products = response.json()
    for product in products:
        assert 50 <= product["price"] <= 150
```

### Verificación

- [ ] Tests de relaciones pasando
- [ ] Tests de validaciones funcionando
- [ ] Tests de reportes con datos correctos
- [ ] Coverage de tests > 85%

---

## 🎯 Reto Extra (Opcional - 15 min)

### Implementar Cache Simple

Agrega un sistema de cache básico para consultas frecuentes:

```python
from functools import lru_cache
from typing import Dict, Any
import time

class SimpleCache:
    def __init__(self, ttl: int = 300):  # 5 minutos TTL
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl

    def get(self, key: str):
        if key in self.cache:
            if time.time() - self.cache[key]["timestamp"] < self.ttl:
                return self.cache[key]["data"]
            else:
                del self.cache[key]
        return None

    def set(self, key: str, data: Any):
        self.cache[key] = {
            "data": data,
            "timestamp": time.time()
        }

# Instancia global
cache = SimpleCache()

@app.get("/products/popular-cached")
def get_popular_products_cached(db: Session = Depends(get_db)):
    """Productos populares con cache"""
    cache_key = "popular_products"

    # Intentar obtener del cache
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    # Si no está en cache, consultar BD
    data = order_crud.get_popular_products(db=db, limit=10)

    # Guardar en cache
    cache.set(cache_key, data)

    return data
```

---

## ✅ Checklist de Completitud

### Modelo de Datos

- [ ] Modelo Category implementado
- [ ] Modelo Review implementado
- [ ] Relaciones definidas correctamente
- [ ] Migraciones aplicadas exitosamente

### CRUD y Lógica de Negocio

- [ ] CategoryCRUD con validaciones
- [ ] ReviewCRUD con reglas de negocio
- [ ] Schemas apropiados creados
- [ ] Endpoints funcionando

### Consultas y Reportes

- [ ] Reporte productos por categoría
- [ ] Top productos por rating
- [ ] Búsqueda avanzada implementada
- [ ] Consultas optimizadas

### Testing

- [ ] Tests de relaciones
- [ ] Tests de validaciones
- [ ] Tests de reportes
- [ ] Coverage > 85%

### Reto Extra

- [ ] Sistema de cache implementado
- [ ] Performance mejorada en consultas frecuentes

---

## 🏆 Criterios de Evaluación

| Aspecto                 | Peso | Criterios                                                 |
| ----------------------- | ---- | --------------------------------------------------------- |
| **Modelo de Datos**     | 25%  | Modelos correctos, relaciones bien definidas, migraciones |
| **Lógica de Negocio**   | 25%  | Validaciones, manejo de errores, CRUD completo            |
| **Consultas Complejas** | 25%  | Reportes, agregaciones, filtros avanzados                 |
| **Testing**             | 25%  | Cobertura, casos edge, tests de integración               |

---

## 📚 Recursos de Apoyo

- [SQLAlchemy Relationships](https://docs.sqlalchemy.org/en/20/orm/relationships.html)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)

---

¡Completa estos ejercicios para dominar completamente las bases de datos con FastAPI! 🚀
