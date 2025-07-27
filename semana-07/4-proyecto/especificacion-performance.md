# Proyecto de Performance: Sistema de Monitoreo E-commerce

## Descripción General

Desarrollar un sistema completo de optimización y monitoreo de performance para una plataforma de e-commerce de alta concurrencia. El proyecto integra todas las técnicas aprendidas en la semana 7: caching con Redis, optimización de base de datos, middleware personalizado, rate limiting, monitoring avanzado y profiling.

## Objetivos del Proyecto

### Objetivo Principal

Crear una API de e-commerce optimizada que pueda manejar 1000+ usuarios concurrentes manteniendo tiempos de respuesta inferiores a 200ms para el 95% de las requests.

### Objetivos Específicos

- Implementar sistema de cache multi-layer con Redis
- Optimizar queries de base de datos con índices estratégicos
- Desarrollar middleware de performance y rate limiting
- Crear dashboard de monitoring en tiempo real
- Establecer sistema de alertas automáticas
- Implementar profiling automático de endpoints críticos

## Duración Estimada

8-10 horas (proyecto para completar durante la semana)

---

## Contexto del Negocio

### Escenario

**TechMart** es una plataforma de e-commerce en crecimiento que experimenta:

- 10,000+ usuarios activos por día
- Picos de tráfico durante promociones (5x tráfico normal)
- Catálogo de 50,000+ productos
- 1000+ transacciones por hora
- Múltiples tipos de usuarios (clientes, vendedores, admins)

### Problemas Actuales

- Respuestas lentas durante picos de tráfico
- Búsquedas de productos tardan >3 segundos
- Base de datos sobrecargada
- Sin visibilidad de performance en tiempo real
- Sistema colapsa con >500 usuarios concurrentes

### Metas de Performance

- Response time promedio: <200ms
- Response time p95: <500ms
- Throughput: 1000+ RPS
- Error rate: <0.1%
- Disponibilidad: 99.9%

---

## Arquitectura del Sistema

### Componentes Principales

```
┌─────────────────────────────────────────────────────────────┐
│                    Load Balancer                            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Application                       │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │ Rate Limit  │ │ Performance │ │    Monitoring           ││
│  │ Middleware  │ │ Middleware  │ │    Middleware           ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │   Products  │ │   Orders    │ │      Users              ││
│  │   Service   │ │   Service   │ │      Service            ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                     Data Layer                              │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐│
│  │  PostgreSQL │ │    Redis    │ │    Monitoring           ││
│  │  (Primary)  │ │   (Cache)   │ │      Store              ││
│  └─────────────┘ └─────────────┘ └─────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

---

## Especificaciones Técnicas

### 1. Modelos de Datos

#### 1.1 Esquema de Base de Datos

```python
# models/database.py
from sqlalchemy import Column, Integer, String, DateTime, Decimal, Boolean, Text, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(128), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20))
    is_active = Column(Boolean, default=True, index=True)
    is_verified = Column(Boolean, default=False, index=True)
    user_type = Column(String(20), default="customer", index=True)  # customer, seller, admin
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    last_login = Column(DateTime, index=True)

    # Relationships
    orders = relationship("Order", back_populates="user")
    cart_items = relationship("CartItem", back_populates="user")
    reviews = relationship("Review", back_populates="user")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    slug = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)
    parent_id = Column(Integer, ForeignKey("categories.id"), index=True)
    is_active = Column(Boolean, default=True, index=True)
    sort_order = Column(Integer, default=0)

    # Relationships
    parent = relationship("Category", remote_side=[id])
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    slug = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(Text)
    short_description = Column(String(500))
    sku = Column(String(50), unique=True, nullable=False, index=True)
    price = Column(Decimal(10, 2), nullable=False, index=True)
    sale_price = Column(Decimal(10, 2), index=True)
    stock_quantity = Column(Integer, default=0, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), index=True, nullable=False)
    brand = Column(String(100), index=True)
    weight = Column(Decimal(8, 2))
    dimensions = Column(String(50))
    is_active = Column(Boolean, default=True, index=True)
    is_featured = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    cart_items = relationship("CartItem", back_populates="product")
    reviews = relationship("Review", back_populates="product")

    # Índices compuestos para optimización
    __table_args__ = (
        Index('idx_product_category_active', 'category_id', 'is_active'),
        Index('idx_product_featured_active', 'is_featured', 'is_active'),
        Index('idx_product_price_active', 'price', 'is_active'),
        Index('idx_product_created_active', 'created_at', 'is_active'),
    )

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    status = Column(String(20), default="pending", index=True)  # pending, processing, shipped, delivered, cancelled
    total_amount = Column(Decimal(10, 2), nullable=False)
    shipping_address = Column(Text, nullable=False)
    billing_address = Column(Text, nullable=False)
    payment_method = Column(String(50), nullable=False)
    payment_status = Column(String(20), default="pending", index=True)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    shipped_at = Column(DateTime, index=True)
    delivered_at = Column(DateTime, index=True)

    # Relationships
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

    # Índices compuestos
    __table_args__ = (
        Index('idx_order_user_status', 'user_id', 'status'),
        Index('idx_order_created_status', 'created_at', 'status'),
        Index('idx_order_payment_status', 'payment_status', 'status'),
    )

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Decimal(10, 2), nullable=False)
    total_price = Column(Decimal(10, 2), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="cart_items")
    product = relationship("Product", back_populates="cart_items")

    # Índice único para evitar duplicados
    __table_args__ = (
        Index('idx_cart_user_product', 'user_id', 'product_id', unique=True),
    )

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), index=True, nullable=False)
    rating = Column(Integer, nullable=False, index=True)  # 1-5
    title = Column(String(200))
    comment = Column(Text)
    is_verified_purchase = Column(Boolean, default=False, index=True)
    is_approved = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")

    # Índices compuestos
    __table_args__ = (
        Index('idx_review_product_approved', 'product_id', 'is_approved'),
        Index('idx_review_product_rating', 'product_id', 'rating'),
        Index('idx_review_user_product', 'user_id', 'product_id', unique=True),
    )
```

### 2. Sistema de Cache

#### 2.1 Estrategia de Cache Multi-Layer

```python
# cache/cache_manager.py
from typing import Optional, List, Dict, Any
import redis
import json
import hashlib
from datetime import datetime, timedelta

class CacheManager:
    """Sistema de cache multi-layer para e-commerce."""

    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.cache_config = {
            # Cache de productos
            "product_detail": {"ttl": 3600, "prefix": "prod"},
            "product_list": {"ttl": 1800, "prefix": "prod_list"},
            "product_search": {"ttl": 1800, "prefix": "search"},

            # Cache de categorías
            "category_tree": {"ttl": 7200, "prefix": "cat_tree"},
            "category_products": {"ttl": 1800, "prefix": "cat_prod"},

            # Cache de usuarios
            "user_profile": {"ttl": 3600, "prefix": "user"},
            "user_cart": {"ttl": 1800, "prefix": "cart"},

            # Cache de órdenes
            "user_orders": {"ttl": 3600, "prefix": "orders"},
            "order_detail": {"ttl": 3600, "prefix": "order"},

            # Cache de métricas
            "dashboard_stats": {"ttl": 300, "prefix": "stats"},
            "popular_products": {"ttl": 1800, "prefix": "popular"},
        }

    def _get_cache_key(self, cache_type: str, identifier: str) -> str:
        """Generar key de cache consistente."""
        config = self.cache_config.get(cache_type, {})
        prefix = config.get("prefix", "default")
        return f"{prefix}:{identifier}"

    def _serialize_data(self, data: Any) -> str:
        """Serializar datos para cache."""
        return json.dumps(data, default=str, ensure_ascii=False)

    def _deserialize_data(self, data: str) -> Any:
        """Deserializar datos de cache."""
        try:
            return json.loads(data)
        except (json.JSONDecodeError, TypeError):
            return None

    async def get(self, cache_type: str, identifier: str) -> Optional[Any]:
        """Obtener datos del cache."""
        key = self._get_cache_key(cache_type, identifier)
        try:
            data = self.redis.get(key)
            if data:
                return self._deserialize_data(data)
        except redis.RedisError as e:
            print(f"Cache get error: {e}")
        return None

    async def set(self, cache_type: str, identifier: str, data: Any) -> bool:
        """Almacenar datos en cache."""
        key = self._get_cache_key(cache_type, identifier)
        config = self.cache_config.get(cache_type, {})
        ttl = config.get("ttl", 3600)

        try:
            serialized_data = self._serialize_data(data)
            self.redis.setex(key, ttl, serialized_data)
            return True
        except redis.RedisError as e:
            print(f"Cache set error: {e}")
            return False

    async def delete(self, cache_type: str, identifier: str) -> bool:
        """Eliminar datos del cache."""
        key = self._get_cache_key(cache_type, identifier)
        try:
            self.redis.delete(key)
            return True
        except redis.RedisError as e:
            print(f"Cache delete error: {e}")
            return False

    async def invalidate_pattern(self, pattern: str) -> int:
        """Invalidar múltiples keys por patrón."""
        try:
            keys = self.redis.keys(pattern)
            if keys:
                return self.redis.delete(*keys)
            return 0
        except redis.RedisError as e:
            print(f"Cache pattern invalidation error: {e}")
            return 0

    async def get_cache_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del cache."""
        try:
            info = self.redis.info()
            return {
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "hit_rate": self._calculate_hit_rate(info),
                "used_memory": info.get("used_memory_human", "0B"),
                "connected_clients": info.get("connected_clients", 0),
                "total_commands_processed": info.get("total_commands_processed", 0)
            }
        except redis.RedisError:
            return {}

    def _calculate_hit_rate(self, info: Dict) -> float:
        """Calcular hit rate del cache."""
        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total = hits + misses
        return (hits / total * 100) if total > 0 else 0
```

### 3. Servicios Optimizados

#### 3.1 Servicio de Productos

```python
# services/product_service.py
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, or_, func
from models.database import Product, Category, Review
from cache.cache_manager import CacheManager

class ProductService:
    """Servicio optimizado para manejo de productos."""

    def __init__(self, db: Session, cache_manager: CacheManager):
        self.db = db
        self.cache = cache_manager

    async def get_product_by_id(self, product_id: int) -> Optional[Dict[str, Any]]:
        """Obtener producto por ID con cache."""
        # Intentar desde cache primero
        cached_product = await self.cache.get("product_detail", str(product_id))
        if cached_product:
            return cached_product

        # Consulta optimizada con joins
        product = self.db.query(Product).options(
            joinedload(Product.category),
            joinedload(Product.reviews)
        ).filter(
            and_(Product.id == product_id, Product.is_active == True)
        ).first()

        if not product:
            return None

        # Calcular rating promedio de forma eficiente
        avg_rating = self.db.query(
            func.avg(Review.rating)
        ).filter(
            and_(
                Review.product_id == product_id,
                Review.is_approved == True
            )
        ).scalar() or 0

        review_count = self.db.query(
            func.count(Review.id)
        ).filter(
            and_(
                Review.product_id == product_id,
                Review.is_approved == True
            )
        ).scalar() or 0

        # Serializar resultado
        result = {
            "id": product.id,
            "name": product.name,
            "slug": product.slug,
            "description": product.description,
            "short_description": product.short_description,
            "sku": product.sku,
            "price": float(product.price),
            "sale_price": float(product.sale_price) if product.sale_price else None,
            "stock_quantity": product.stock_quantity,
            "brand": product.brand,
            "category": {
                "id": product.category.id,
                "name": product.category.name,
                "slug": product.category.slug
            },
            "rating": {
                "average": round(float(avg_rating), 2),
                "count": review_count
            },
            "is_featured": product.is_featured,
            "created_at": product.created_at.isoformat()
        }

        # Guardar en cache
        await self.cache.set("product_detail", str(product_id), result)

        return result

    async def search_products(
        self,
        query: Optional[str] = None,
        category_id: Optional[int] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        brand: Optional[str] = None,
        is_featured: Optional[bool] = None,
        sort_by: str = "name",
        sort_order: str = "asc",
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:
        """Búsqueda optimizada de productos con cache."""

        # Generar cache key basado en parámetros
        cache_params = {
            "query": query,
            "category_id": category_id,
            "min_price": min_price,
            "max_price": max_price,
            "brand": brand,
            "is_featured": is_featured,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "page": page,
            "page_size": page_size
        }
        cache_key = hashlib.md5(
            json.dumps(cache_params, sort_keys=True).encode()
        ).hexdigest()

        # Intentar desde cache
        cached_result = await self.cache.get("product_search", cache_key)
        if cached_result:
            return cached_result

        # Construir query optimizada
        query_obj = self.db.query(Product).options(
            joinedload(Product.category)
        ).filter(Product.is_active == True)

        # Filtros
        if query:
            query_obj = query_obj.filter(
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.description.ilike(f"%{query}%"),
                    Product.brand.ilike(f"%{query}%")
                )
            )

        if category_id:
            query_obj = query_obj.filter(Product.category_id == category_id)

        if min_price is not None:
            query_obj = query_obj.filter(Product.price >= min_price)

        if max_price is not None:
            query_obj = query_obj.filter(Product.price <= max_price)

        if brand:
            query_obj = query_obj.filter(Product.brand.ilike(f"%{brand}%"))

        if is_featured is not None:
            query_obj = query_obj.filter(Product.is_featured == is_featured)

        # Ordenamiento
        if sort_by == "price":
            if sort_order == "desc":
                query_obj = query_obj.order_by(Product.price.desc())
            else:
                query_obj = query_obj.order_by(Product.price.asc())
        elif sort_by == "created_at":
            if sort_order == "desc":
                query_obj = query_obj.order_by(Product.created_at.desc())
            else:
                query_obj = query_obj.order_by(Product.created_at.asc())
        else:  # name
            if sort_order == "desc":
                query_obj = query_obj.order_by(Product.name.desc())
            else:
                query_obj = query_obj.order_by(Product.name.asc())

        # Paginación
        total_count = query_obj.count()
        products = query_obj.offset((page - 1) * page_size).limit(page_size).all()

        # Serializar resultados
        products_data = []
        for product in products:
            products_data.append({
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "short_description": product.short_description,
                "price": float(product.price),
                "sale_price": float(product.sale_price) if product.sale_price else None,
                "stock_quantity": product.stock_quantity,
                "brand": product.brand,
                "category": {
                    "id": product.category.id,
                    "name": product.category.name,
                    "slug": product.category.slug
                },
                "is_featured": product.is_featured
            })

        result = {
            "products": products_data,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total_count": total_count,
                "total_pages": (total_count + page_size - 1) // page_size
            }
        }

        # Guardar en cache
        await self.cache.set("product_search", cache_key, result)

        return result

    async def get_popular_products(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtener productos populares basado en órdenes."""
        cached_result = await self.cache.get("popular_products", f"limit_{limit}")
        if cached_result:
            return cached_result

        # Query optimizada para productos populares
        popular_products = self.db.query(
            Product,
            func.count(OrderItem.product_id).label('order_count')
        ).join(
            OrderItem, Product.id == OrderItem.product_id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            and_(
                Product.is_active == True,
                Order.status.in_(['delivered', 'shipped']),
                Order.created_at >= datetime.utcnow() - timedelta(days=30)
            )
        ).group_by(
            Product.id
        ).order_by(
            func.count(OrderItem.product_id).desc()
        ).limit(limit).all()

        result = []
        for product, order_count in popular_products:
            result.append({
                "id": product.id,
                "name": product.name,
                "slug": product.slug,
                "price": float(product.price),
                "sale_price": float(product.sale_price) if product.sale_price else None,
                "order_count": order_count,
                "brand": product.brand
            })

        await self.cache.set("popular_products", f"limit_{limit}", result)
        return result
```

### 4. Sistema de Rate Limiting Avanzado

#### 4.1 Rate Limiter Adaptativo

```python
# middleware/adaptive_rate_limiter.py
import time
import redis
import psutil
from typing import Dict, Optional
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

class AdaptiveRateLimiter(BaseHTTPMiddleware):
    """Rate limiter que se adapta a la carga del sistema."""

    def __init__(self, app, redis_client: redis.Redis):
        super().__init__(app)
        self.redis = redis_client

        # Configuración base de rate limits
        self.base_limits = {
            # Endpoints de productos
            "GET /products": {"requests": 200, "window": 60},
            "GET /products/{id}": {"requests": 300, "window": 60},
            "POST /products/search": {"requests": 100, "window": 60},

            # Endpoints de usuarios
            "POST /auth/login": {"requests": 10, "window": 60},
            "POST /auth/register": {"requests": 5, "window": 60},
            "GET /users/profile": {"requests": 100, "window": 60},

            # Endpoints de órdenes
            "POST /orders": {"requests": 20, "window": 60},
            "GET /orders": {"requests": 50, "window": 60},

            # Endpoints de carrito
            "POST /cart/add": {"requests": 50, "window": 60},
            "GET /cart": {"requests": 100, "window": 60},

            # Default para otros endpoints
            "default": {"requests": 100, "window": 60}
        }

        # Configuración de adaptación basada en carga del sistema
        self.load_thresholds = {
            "low": {"cpu": 30, "memory": 50, "multiplier": 1.0},
            "medium": {"cpu": 60, "memory": 70, "multiplier": 0.7},
            "high": {"cpu": 80, "memory": 85, "multiplier": 0.4},
            "critical": {"cpu": 95, "memory": 95, "multiplier": 0.1}
        }

    async def dispatch(self, request: Request, call_next):
        # Obtener endpoint key
        endpoint_key = f"{request.method} {request.url.path}"

        # Para paths con parámetros, usar patrón genérico
        if "/products/" in request.url.path and request.method == "GET":
            if request.url.path.count("/") == 2:  # /products/{id}
                endpoint_key = "GET /products/{id}"

        # Obtener carga del sistema
        system_load = self._get_system_load()

        # Calcular límite adaptativo
        base_limit = self.base_limits.get(endpoint_key, self.base_limits["default"])
        adaptive_limit = self._calculate_adaptive_limit(base_limit, system_load)

        # Verificar rate limit
        client_id = self._get_client_id(request)
        if await self._is_rate_limited(client_id, endpoint_key, adaptive_limit):
            # Agregar headers informativos
            headers = {
                "X-RateLimit-Limit": str(adaptive_limit["requests"]),
                "X-RateLimit-Reset": str(int(time.time()) + adaptive_limit["window"]),
                "X-System-Load": system_load["level"],
                "Retry-After": str(min(60, adaptive_limit["window"]))
            }

            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "message": f"Too many requests. System load: {system_load['level']}",
                    "retry_after": adaptive_limit["window"]
                },
                headers=headers
            )

        # Procesar request
        response = await call_next(request)

        # Agregar headers informativos
        response.headers["X-RateLimit-Limit"] = str(adaptive_limit["requests"])
        response.headers["X-System-Load"] = system_load["level"]

        return response

    def _get_system_load(self) -> Dict[str, any]:
        """Obtener carga actual del sistema."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent

            # Determinar nivel de carga
            if cpu_percent >= 95 or memory_percent >= 95:
                level = "critical"
            elif cpu_percent >= 80 or memory_percent >= 85:
                level = "high"
            elif cpu_percent >= 60 or memory_percent >= 70:
                level = "medium"
            else:
                level = "low"

            return {
                "cpu": cpu_percent,
                "memory": memory_percent,
                "level": level
            }
        except:
            return {"cpu": 0, "memory": 0, "level": "low"}

    def _calculate_adaptive_limit(self, base_limit: Dict, system_load: Dict) -> Dict:
        """Calcular límite adaptativo basado en carga del sistema."""
        load_level = system_load["level"]
        multiplier = self.load_thresholds[load_level]["multiplier"]

        return {
            "requests": max(1, int(base_limit["requests"] * multiplier)),
            "window": base_limit["window"]
        }

    def _get_client_id(self, request: Request) -> str:
        """Obtener identificador único del cliente."""
        # Intentar obtener user ID desde JWT
        user_id = getattr(request.state, "user_id", None)
        if user_id:
            return f"user:{user_id}"

        # Usar IP como fallback
        client_ip = request.client.host if request.client else "unknown"
        user_agent_hash = hash(request.headers.get("user-agent", ""))
        return f"ip:{client_ip}:{user_agent_hash}"

    async def _is_rate_limited(self, client_id: str, endpoint: str, limit: Dict) -> bool:
        """Verificar si el cliente ha excedido el rate limit."""
        key = f"rate_limit:{client_id}:{endpoint}"
        window = limit["window"]
        max_requests = limit["requests"]

        current_time = int(time.time())
        window_start = current_time - window

        try:
            pipe = self.redis.pipeline()

            # Limpiar requests antiguos
            pipe.zremrangebyscore(key, 0, window_start)

            # Contar requests en ventana actual
            pipe.zcard(key)

            # Agregar request actual
            pipe.zadd(key, {str(current_time): current_time})

            # Establecer TTL
            pipe.expire(key, window)

            results = pipe.execute()
            current_requests = results[1]

            return current_requests >= max_requests

        except redis.RedisError:
            # En caso de error de Redis, permitir el request
            return False
```

### 5. Dashboard de Monitoring

#### 5.1 Sistema de Métricas E-commerce

```python
# monitoring/ecommerce_metrics.py
from typing import Dict, List, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models.database import User, Product, Order, OrderItem, Review
import redis

class EcommerceMetricsCollector:
    """Collector de métricas específicas para e-commerce."""

    def __init__(self, db: Session, redis_client: redis.Redis):
        self.db = db
        self.redis = redis_client

    async def collect_business_metrics(self) -> Dict[str, Any]:
        """Recopilar métricas clave del negocio."""
        now = datetime.utcnow()
        today = now.date()
        yesterday = today - timedelta(days=1)
        last_week = today - timedelta(days=7)
        last_month = today - timedelta(days=30)

        # Métricas de usuarios
        total_users = self.db.query(User).count()
        active_users_today = self.db.query(User).filter(
            func.date(User.last_login) == today
        ).count()

        new_users_today = self.db.query(User).filter(
            func.date(User.created_at) == today
        ).count()

        # Métricas de productos
        total_products = self.db.query(Product).filter(
            Product.is_active == True
        ).count()

        low_stock_products = self.db.query(Product).filter(
            and_(
                Product.is_active == True,
                Product.stock_quantity <= 10
            )
        ).count()

        # Métricas de órdenes
        orders_today = self.db.query(Order).filter(
            func.date(Order.created_at) == today
        ).count()

        orders_yesterday = self.db.query(Order).filter(
            func.date(Order.created_at) == yesterday
        ).count()

        total_revenue_today = self.db.query(
            func.sum(Order.total_amount)
        ).filter(
            func.date(Order.created_at) == today
        ).scalar() or 0

        total_revenue_month = self.db.query(
            func.sum(Order.total_amount)
        ).filter(
            Order.created_at >= last_month
        ).scalar() or 0

        # Métricas de conversion
        avg_order_value = self.db.query(
            func.avg(Order.total_amount)
        ).filter(
            Order.created_at >= last_month
        ).scalar() or 0

        # Top productos
        top_products = self.db.query(
            Product.name,
            func.sum(OrderItem.quantity).label('total_sold')
        ).join(
            OrderItem, Product.id == OrderItem.product_id
        ).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            Order.created_at >= last_week
        ).group_by(
            Product.id, Product.name
        ).order_by(
            func.sum(OrderItem.quantity).desc()
        ).limit(5).all()

        return {
            "users": {
                "total": total_users,
                "active_today": active_users_today,
                "new_today": new_users_today
            },
            "products": {
                "total": total_products,
                "low_stock": low_stock_products
            },
            "orders": {
                "today": orders_today,
                "yesterday": orders_yesterday,
                "growth": ((orders_today - orders_yesterday) / max(orders_yesterday, 1)) * 100
            },
            "revenue": {
                "today": float(total_revenue_today),
                "month": float(total_revenue_month),
                "avg_order_value": float(avg_order_value)
            },
            "top_products": [
                {"name": name, "total_sold": total_sold}
                for name, total_sold in top_products
            ]
        }

    async def collect_performance_metrics(self) -> Dict[str, Any]:
        """Recopilar métricas de performance."""
        # Obtener métricas de Redis
        redis_info = self.redis.info()

        # Métricas de cache
        cache_hits = redis_info.get("keyspace_hits", 0)
        cache_misses = redis_info.get("keyspace_misses", 0)
        total_cache_ops = cache_hits + cache_misses
        cache_hit_rate = (cache_hits / total_cache_ops * 100) if total_cache_ops > 0 else 0

        # Métricas de base de datos (simuladas - implementar según driver usado)
        db_connections = 5  # Implementar según pool de conexiones

        return {
            "cache": {
                "hit_rate": round(cache_hit_rate, 2),
                "total_operations": total_cache_ops,
                "memory_usage": redis_info.get("used_memory_human", "0B")
            },
            "database": {
                "active_connections": db_connections,
                "query_time_avg": 45  # ms - implementar medición real
            }
        }
```

---

## Tareas del Proyecto

### Fase 1: Configuración Base (2 horas)

#### 1.1 Setup del Proyecto

- [ ] Crear estructura de directorios
- [ ] Configurar base de datos PostgreSQL
- [ ] Configurar Redis
- [ ] Implementar modelos de datos
- [ ] Crear data de prueba (seeding)

#### 1.2 Configuración de FastAPI

- [ ] Setup básico de FastAPI
- [ ] Configurar CORS y middleware base
- [ ] Implementar sistema de logging
- [ ] Configurar variables de entorno

### Fase 2: Sistema de Cache (2 horas)

#### 2.1 Implementar Cache Manager

- [ ] Desarrollar CacheManager multi-layer
- [ ] Implementar cache para productos
- [ ] Implementar cache para categorías
- [ ] Implementar cache para usuarios

#### 2.2 Integrar Cache en Servicios

- [ ] Optimizar ProductService con cache
- [ ] Implementar cache invalidation
- [ ] Crear métricas de cache

### Fase 3: Optimización de Base de Datos (2 horas)

#### 3.1 Crear Índices Optimizados

- [ ] Implementar índices para queries frecuentes
- [ ] Optimizar queries de búsqueda
- [ ] Optimizar queries de agregación
- [ ] Configurar connection pooling

#### 3.2 Servicios Optimizados

- [ ] Implementar ProductService optimizado
- [ ] Implementar OrderService optimizado
- [ ] Implementar UserService optimizado

### Fase 4: Middleware y Rate Limiting (1.5 horas)

#### 4.1 Middleware de Performance

- [ ] Implementar RequestLoggingMiddleware
- [ ] Implementar MetricsMiddleware
- [ ] Implementar CompressionMiddleware

#### 4.2 Rate Limiting Adaptativo

- [ ] Desarrollar AdaptiveRateLimiter
- [ ] Configurar límites por endpoint
- [ ] Implementar whitelist de IPs

### Fase 5: Monitoring y Dashboard (2.5 horas)

#### 5.1 Sistema de Monitoring

- [ ] Implementar EcommerceMetricsCollector
- [ ] Desarrollar AlertManager
- [ ] Implementar background tasks

#### 5.2 Dashboard Web

- [ ] Crear dashboard HTML/CSS/JS
- [ ] Implementar métricas en tiempo real
- [ ] Agregar gráficos de performance
- [ ] Implementar sistema de alertas visual

---

## Criterios de Evaluación

### Performance (30%)

- [ ] API maneja 1000+ usuarios concurrentes
- [ ] Response time p95 < 500ms
- [ ] Cache hit rate > 80%
- [ ] Throughput > 500 RPS

### Funcionalidad (25%)

- [ ] Todas las funcionalidades implementadas
- [ ] Sistema de cache funcionando
- [ ] Rate limiting adaptativo operativo
- [ ] Dashboard mostrando métricas correctas

### Código y Arquitectura (25%)

- [ ] Código limpio y bien estructurado
- [ ] Patterns de diseño aplicados correctamente
- [ ] Manejo adecuado de errores
- [ ] Documentación clara

### Optimización y Monitoring (20%)

- [ ] Queries optimizadas efectivamente
- [ ] Sistema de monitoring completo
- [ ] Alertas automáticas funcionando
- [ ] Análisis de performance documentado

---

## Entregables

### 1. Código Fuente Completo

```
ecommerce-performance/
├── app/
│   ├── models/
│   ├── services/
│   ├── cache/
│   ├── middleware/
│   ├── monitoring/
│   ├── routers/
│   └── main.py
├── tests/
├── scripts/
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### 2. Documentación

- Guía de instalación y configuración
- Documentación de API endpoints
- Análisis de performance antes/después
- Reporte de load testing

### 3. Resultados de Testing

- Resultados de load testing
- Métricas de performance
- Análisis de cuellos de botella
- Recomendaciones de optimización

### 4. Dashboard Funcional

- Dashboard web accesible
- Métricas en tiempo real
- Sistema de alertas visual
- Reportes de performance

---

## Recursos de Apoyo

- [PostgreSQL Performance Tips](https://wiki.postgresql.org/wiki/Performance_Optimization)
- [Redis Patterns](https://redis.io/docs/manual/patterns/)
- [FastAPI Performance](https://fastapi.tiangolo.com/async/)
- [SQLAlchemy Optimization](https://docs.sqlalchemy.org/en/14/orm/loading_techniques.html)

## Tiempo Total Estimado

**8-10 horas** distribuidas en las 5 fases del proyecto
