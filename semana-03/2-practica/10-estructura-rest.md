# Práctica 10: Estructura REST Profesional - Semana 3

## 🎯 Objetivo

Organizar el código en una estructura profesional y escalable siguiendo principios REST, separación de responsabilidades, y mejores prácticas de arquitectura de software.

## ⏱️ Tiempo Estimado: 90 minutos

## 📋 Pre-requisitos

- ✅ API con manejo de errores robusto (Práctica 9)
- ✅ Comprensión de principios REST
- ✅ Familiaridad con patrones de arquitectura

## 🏗️ Paso 1: Estructura de Proyecto Profesional (20 min)

### **Arquitectura del Proyecto Final**

```text
semana-03-inventory-api/
├── app/
│   ├── __init__.py
│   ├── main.py                     # Punto de entrada de la aplicación
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py             # Configuraciones de la aplicación
│   │   └── database.py             # Configuración de base de datos (simulada)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                 # Modelos base
│   │   ├── product.py              # Modelos de producto
│   │   └── response.py             # Modelos de respuesta
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── product.py              # Esquemas Pydantic para API
│   │   └── error.py                # Esquemas de error
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py         # Dependencias de FastAPI
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── api.py              # Router principal v1
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       ├── products.py     # Endpoints de productos
│   │   │       └── health.py       # Endpoints de salud
│   ├── core/
│   │   ├── __init__.py
│   │   ├── exceptions.py           # Excepciones custom
│   │   ├── security.py             # Seguridad y autenticación
│   │   └── logging.py              # Configuración de logging
│   ├── services/
│   │   ├── __init__.py
│   │   ├── product_service.py      # Lógica de negocio de productos
│   │   └── external_service.py     # Servicios externos
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py                 # Repository base
│   │   └── product_repository.py   # Repository de productos
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py           # Validadores custom
│   │   ├── helpers.py              # Funciones auxiliares
│   │   └── constants.py            # Constantes de la aplicación
│   └── middleware/
│       ├── __init__.py
│       ├── logging_middleware.py   # Middleware de logging
│       ├── cors_middleware.py      # Middleware de CORS
│       └── error_middleware.py     # Middleware de errores
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Configuración de pytest
│   ├── test_products.py            # Tests de productos
│   └── test_health.py              # Tests de salud
├── docs/
│   ├── api_design.md               # Documentación de diseño API
│   └── development.md              # Guía de desarrollo
├── scripts/
│   ├── start.sh                    # Script de inicio
│   └── setup.py                    # Script de configuración
├── requirements.txt                # Dependencias de producción
├── requirements-dev.txt            # Dependencias de desarrollo
├── .env.example                    # Ejemplo de variables de entorno
├── .gitignore
├── Dockerfile
├── docker-compose.yml
└── README.md
```

### **Crear la Estructura Base**

```bash
# Crear directorios
mkdir -p semana-03-inventory-api/app/{config,models,schemas,api/v1/endpoints,core,services,repositories,utils,middleware}
mkdir -p semana-03-inventory-api/{tests,docs,scripts}

# Crear archivos __init__.py
find semana-03-inventory-api/app -type d -exec touch {}/__init__.py \;
touch semana-03-inventory-api/tests/__init__.py
```

## ⚙️ Paso 2: Configuración y Settings (15 min)

### **app/config/settings.py**

```python
from pydantic import BaseSettings, Field
from typing import Optional, List
from pathlib import Path
import os

class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Información básica de la aplicación
    APP_NAME: str = Field("Inventory API", description="Nombre de la aplicación")
    APP_VERSION: str = Field("1.0.0", description="Versión de la aplicación")
    APP_DESCRIPTION: str = Field(
        "API REST profesional para gestión de inventario",
        description="Descripción de la aplicación"
    )

    # Configuración del servidor
    HOST: str = Field("0.0.0.0", description="Host del servidor")
    PORT: int = Field(8000, description="Puerto del servidor")
    DEBUG: bool = Field(False, description="Modo debug")
    RELOAD: bool = Field(False, description="Auto-reload en desarrollo")

    # Configuración de la API
    API_V1_STR: str = Field("/api/v1", description="Prefijo de la API v1")
    DOCS_URL: str = Field("/docs", description="URL de documentación Swagger")
    REDOC_URL: str = Field("/redoc", description="URL de documentación ReDoc")
    OPENAPI_URL: str = Field("/openapi.json", description="URL del esquema OpenAPI")

    # Configuración de CORS
    CORS_ORIGINS: List[str] = Field(
        ["http://localhost:3000", "http://localhost:8080"],
        description="Orígenes permitidos para CORS"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(True, description="Permitir credenciales en CORS")
    CORS_ALLOW_METHODS: List[str] = Field(
        ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        description="Métodos HTTP permitidos"
    )
    CORS_ALLOW_HEADERS: List[str] = Field(
        ["*"],
        description="Headers permitidos"
    )

    # Configuración de logging
    LOG_LEVEL: str = Field("INFO", description="Nivel de logging")
    LOG_FILE: str = Field("logs/app.log", description="Archivo de logs")
    LOG_MAX_SIZE: int = Field(10 * 1024 * 1024, description="Tamaño máximo de archivo de log")
    LOG_BACKUP_COUNT: int = Field(5, description="Número de archivos de backup")

    # Configuración de base de datos (simulada)
    DATABASE_URL: str = Field("sqlite:///./inventory.db", description="URL de base de datos")
    DATABASE_ECHO: bool = Field(False, description="Echo de queries de DB")

    # Configuración de cache
    CACHE_TTL: int = Field(300, description="TTL del cache en segundos")
    CACHE_MAX_SIZE: int = Field(1000, description="Tamaño máximo del cache")

    # Configuración de rate limiting
    RATE_LIMIT_ENABLED: bool = Field(True, description="Habilitar rate limiting")
    RATE_LIMIT_REQUESTS: int = Field(100, description="Requests por ventana")
    RATE_LIMIT_WINDOW: int = Field(60, description="Ventana de tiempo en segundos")

    # Configuración de paginación
    DEFAULT_PAGE_SIZE: int = Field(10, description="Tamaño de página por defecto")
    MAX_PAGE_SIZE: int = Field(100, description="Tamaño máximo de página")

    # Paths de archivos
    BASE_DIR: Path = Field(Path(__file__).parent.parent.parent, description="Directorio base")
    LOG_DIR: Path = Field(Path("logs"), description="Directorio de logs")

    # Configuración de servicios externos
    EXTERNAL_SERVICE_TIMEOUT: int = Field(30, description="Timeout para servicios externos")
    EXTERNAL_SERVICE_RETRIES: int = Field(3, description="Reintentos para servicios externos")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

# Instancia global de configuración
settings = Settings()

# Crear directorios necesarios
settings.LOG_DIR.mkdir(exist_ok=True)
```

### **app/config/database.py**

```python
from typing import Dict, List, Any, Optional
from datetime import datetime
import json
from pathlib import Path

class InMemoryDatabase:
    """Simulador de base de datos en memoria"""

    def __init__(self):
        self._products: Dict[int, dict] = {}
        self._next_id = 1
        self._init_sample_data()

    def _init_sample_data(self):
        """Inicializar con datos de ejemplo"""
        sample_products = [
            {
                "name": "Laptop Gaming Pro",
                "price": 1299.99,
                "sku": "ELE-GENER-LP01",
                "description": "Laptop gaming de alta performance con RTX 4060",
                "category": "electronics",
                "brand": "generic",
                "weight": 2.5,
                "dimensions": {"length": 35.6, "width": 25.4, "height": 2.3},
                "tags": ["gaming", "laptop", "performance"],
                "release_date": "2024-01-15",
                "is_digital": False,
                "min_age": 13,
                "warranty_months": 24,
                "in_stock": True,
                "stock_quantity": 25
            },
            {
                "name": "Camiseta Deportiva",
                "price": 29.99,
                "sku": "CLO-NIKE-TS01",
                "description": "Camiseta deportiva de alta calidad con tecnología Dri-FIT",
                "category": "clothing",
                "brand": "nike",
                "weight": 0.2,
                "dimensions": {"length": 70, "width": 50, "height": 0.5},
                "tags": ["deportes", "camiseta", "nike"],
                "release_date": "2024-03-01",
                "is_digital": False,
                "min_age": 0,
                "warranty_months": 6,
                "in_stock": True,
                "stock_quantity": 150
            },
            {
                "name": "Smartphone Premium",
                "price": 899.99,
                "sku": "ELE-SAMSU-SP01",
                "description": "Smartphone con cámara de 108MP y pantalla AMOLED",
                "category": "electronics",
                "brand": "samsung",
                "weight": 0.195,
                "dimensions": {"length": 15.8, "width": 7.4, "height": 0.89},
                "tags": ["smartphone", "premium", "camera"],
                "release_date": "2024-02-10",
                "is_digital": False,
                "min_age": 13,
                "warranty_months": 12,
                "in_stock": True,
                "stock_quantity": 75
            }
        ]

        for product_data in sample_products:
            self.create(product_data)

    def create(self, data: dict) -> dict:
        """Crear un nuevo registro"""
        product_id = self._next_id
        self._next_id += 1

        product = {
            "id": product_id,
            **data,
            "created_at": datetime.now(),
            "updated_at": None
        }

        self._products[product_id] = product
        return product.copy()

    def get_by_id(self, product_id: int) -> Optional[dict]:
        """Obtener registro por ID"""
        product = self._products.get(product_id)
        return product.copy() if product else None

    def get_all(self) -> List[dict]:
        """Obtener todos los registros"""
        return [product.copy() for product in self._products.values()]

    def update(self, product_id: int, data: dict) -> Optional[dict]:
        """Actualizar registro existente"""
        if product_id not in self._products:
            return None

        updated_product = {
            **self._products[product_id],
            **data,
            "updated_at": datetime.now()
        }

        self._products[product_id] = updated_product
        return updated_product.copy()

    def delete(self, product_id: int) -> bool:
        """Eliminar registro"""
        if product_id in self._products:
            del self._products[product_id]
            return True
        return False

    def exists_by_field(self, field: str, value: Any, exclude_id: Optional[int] = None) -> bool:
        """Verificar si existe un registro con un valor específico en un campo"""
        for product_id, product in self._products.items():
            if exclude_id and product_id == exclude_id:
                continue
            if product.get(field) == value:
                return True
        return False

    def filter_products(self, filters: dict) -> List[dict]:
        """Filtrar productos según criterios"""
        products = self.get_all()

        for filter_key, filter_value in filters.items():
            if filter_value is None:
                continue

            if filter_key == "category":
                products = [p for p in products if p.get("category") == filter_value]
            elif filter_key == "brand":
                products = [p for p in products if p.get("brand") == filter_value]
            elif filter_key == "in_stock":
                products = [p for p in products if p.get("in_stock") == filter_value]
            elif filter_key == "min_price":
                products = [p for p in products if p.get("price", 0) >= filter_value]
            elif filter_key == "max_price":
                products = [p for p in products if p.get("price", 0) <= filter_value]
            elif filter_key == "is_digital":
                products = [p for p in products if p.get("is_digital") == filter_value]
            elif filter_key == "search":
                search_lower = filter_value.lower()
                products = [
                    p for p in products
                    if search_lower in p.get("name", "").lower() or
                       search_lower in p.get("description", "").lower() or
                       any(search_lower in tag.lower() for tag in p.get("tags", []))
                ]

        return products

    def get_stats(self) -> dict:
        """Obtener estadísticas de la base de datos"""
        products = self.get_all()

        total_products = len(products)
        in_stock_count = len([p for p in products if p.get("in_stock", False)])
        total_value = sum(p.get("price", 0) * p.get("stock_quantity", 0) for p in products)

        categories = {}
        brands = {}

        for product in products:
            category = product.get("category", "unknown")
            brand = product.get("brand", "unknown")

            categories[category] = categories.get(category, 0) + 1
            brands[brand] = brands.get(brand, 0) + 1

        return {
            "total_products": total_products,
            "in_stock_count": in_stock_count,
            "out_of_stock_count": total_products - in_stock_count,
            "total_inventory_value": round(total_value, 2),
            "categories": categories,
            "brands": brands,
            "last_updated": datetime.now().isoformat()
        }

# Instancia global de la base de datos
db = InMemoryDatabase()
```

## 🔧 Paso 3: Modelos y Schemas Organizados (20 min)

### **app/models/base.py**

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class BaseEntity(BaseModel):
    """Modelo base para todas las entidades"""

    id: Optional[int] = Field(None, description="ID único de la entidad")
    created_at: Optional[datetime] = Field(None, description="Fecha de creación")
    updated_at: Optional[datetime] = Field(None, description="Fecha de última actualización")

    class Config:
        orm_mode = True
        use_enum_values = True
        allow_population_by_field_name = True

class TimestampMixin(BaseModel):
    """Mixin para campos de timestamp"""

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(None)

class MetadataMixin(BaseModel):
    """Mixin para metadatos adicionales"""

    is_active: bool = Field(True, description="Indica si la entidad está activa")
    created_by: Optional[str] = Field(None, description="Usuario que creó la entidad")
    updated_by: Optional[str] = Field(None, description="Usuario que actualizó la entidad")
```

### **app/schemas/product.py**

```python
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List, Dict
from datetime import datetime, date
from enum import Enum
from decimal import Decimal

from app.models.base import BaseEntity

class CategoryEnum(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    home = "home"
    sports = "sports"
    beauty = "beauty"
    automotive = "automotive"

class BrandEnum(str, Enum):
    apple = "apple"
    samsung = "samsung"
    sony = "sony"
    nike = "nike"
    adidas = "adidas"
    generic = "generic"

class ProductBase(BaseModel):
    """Schema base para productos"""

    name: str = Field(..., min_length=2, max_length=100)
    price: Decimal = Field(..., gt=0, le=999999.99, decimal_places=2)
    sku: str = Field(..., min_length=6, max_length=20)
    description: Optional[str] = Field(None, max_length=1000)
    category: CategoryEnum
    brand: BrandEnum
    weight: Optional[float] = Field(None, gt=0, le=1000)
    dimensions: Optional[Dict[str, float]] = None
    tags: Optional[List[str]] = Field(None, max_items=10)
    release_date: Optional[date] = None
    is_digital: bool = Field(False)
    min_age: Optional[int] = Field(None, ge=0, le=100)
    warranty_months: Optional[int] = Field(None, ge=0, le=120)

    @validator('name')
    def validate_name(cls, v):
        v = ' '.join(v.split()).title()
        if v.isdigit():
            raise ValueError('El nombre no puede ser solo números')
        return v

    @validator('sku')
    def validate_sku(cls, v):
        import re
        pattern = r'^[A-Z]{3}-[A-Z]{3,6}-[A-Z0-9]{4}$'
        v = v.upper().strip()
        if not re.match(pattern, v):
            raise ValueError('SKU debe tener formato CAT-BRAND-XXXX')
        return v

    @root_validator
    def validate_digital_product_logic(cls, values):
        is_digital = values.get('is_digital', False)
        weight = values.get('weight')
        dimensions = values.get('dimensions')

        if is_digital:
            if weight is not None and weight > 0:
                raise ValueError('Productos digitales no pueden tener peso')
            if dimensions is not None:
                raise ValueError('Productos digitales no pueden tener dimensiones físicas')

        return values

class ProductCreate(ProductBase):
    """Schema para crear productos"""

    in_stock: bool = Field(True)
    stock_quantity: int = Field(0, ge=0, le=9999)
    supplier_email: Optional[str] = Field(None, regex=r'^[^@]+@[^@]+\.[^@]+$')

class ProductUpdate(ProductBase):
    """Schema para actualizar productos"""

    in_stock: bool
    stock_quantity: int = Field(..., ge=0, le=9999)

class ProductInDB(ProductBase, BaseEntity):
    """Schema para productos en base de datos"""

    in_stock: bool
    stock_quantity: int
    estimated_value: Optional[float] = None
    popularity_score: Optional[float] = None

class ProductResponse(ProductInDB):
    """Schema para respuestas de productos"""

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "iPhone 15 Pro",
                "price": 1199.99,
                "sku": "ELE-APPLE-I15P",
                "description": "Smartphone premium con cámara avanzada",
                "category": "electronics",
                "brand": "apple",
                "weight": 0.195,
                "dimensions": {"length": 15.8, "width": 7.4, "height": 0.89},
                "tags": ["smartphone", "premium", "camera"],
                "release_date": "2024-01-15",
                "is_digital": False,
                "min_age": 13,
                "warranty_months": 12,
                "in_stock": True,
                "stock_quantity": 50,
                "created_at": "2024-07-24T10:00:00",
                "updated_at": None,
                "estimated_value": 59999.50,
                "popularity_score": 9.2
            }
        }

class ProductList(BaseModel):
    """Schema para listas de productos"""

    items: List[ProductResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

class ProductFilter(BaseModel):
    """Schema para filtros de productos"""

    category: Optional[CategoryEnum] = None
    brand: Optional[BrandEnum] = None
    in_stock: Optional[bool] = None
    min_price: Optional[float] = Field(None, ge=0)
    max_price: Optional[float] = Field(None, ge=0)
    is_digital: Optional[bool] = None
    search: Optional[str] = Field(None, min_length=2, max_length=100)
    tags: Optional[List[str]] = None

class ProductStats(BaseModel):
    """Schema para estadísticas de productos"""

    total_products: int
    in_stock_count: int
    out_of_stock_count: int
    total_inventory_value: float
    categories: Dict[str, int]
    brands: Dict[str, int]
    last_updated: datetime
```

## 🏭 Paso 4: Services y Repository Pattern (20 min)

### **app/repositories/base.py**

```python
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, TypeVar, Generic

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """Repository base abstracto"""

    @abstractmethod
    async def create(self, data: Dict[str, Any]) -> T:
        """Crear un nuevo registro"""
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> Optional[T]:
        """Obtener registro por ID"""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Obtener todos los registros con paginación"""
        pass

    @abstractmethod
    async def update(self, id: int, data: Dict[str, Any]) -> Optional[T]:
        """Actualizar registro existente"""
        pass

    @abstractmethod
    async def delete(self, id: int) -> bool:
        """Eliminar registro"""
        pass

    @abstractmethod
    async def exists(self, **filters) -> bool:
        """Verificar si existe un registro con los filtros dados"""
        pass
```

### **app/repositories/product_repository.py**

```python
from typing import List, Optional, Dict, Any
from app.repositories.base import BaseRepository
from app.config.database import db
from app.schemas.product import ProductInDB

class ProductRepository(BaseRepository[ProductInDB]):
    """Repository para productos"""

    def __init__(self):
        self.db = db

    async def create(self, data: Dict[str, Any]) -> ProductInDB:
        """Crear un nuevo producto"""
        product_data = await self.db.create(data)
        return ProductInDB(**product_data)

    async def get_by_id(self, product_id: int) -> Optional[ProductInDB]:
        """Obtener producto por ID"""
        product_data = await self.db.get_by_id(product_id)
        return ProductInDB(**product_data) if product_data else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ProductInDB]:
        """Obtener todos los productos con paginación"""
        all_products = await self.db.get_all()
        paginated = all_products[skip:skip + limit]
        return [ProductInDB(**product) for product in paginated]

    async def update(self, product_id: int, data: Dict[str, Any]) -> Optional[ProductInDB]:
        """Actualizar producto existente"""
        updated_data = await self.db.update(product_id, data)
        return ProductInDB(**updated_data) if updated_data else None

    async def delete(self, product_id: int) -> bool:
        """Eliminar producto"""
        return await self.db.delete(product_id)

    async def exists(self, **filters) -> bool:
        """Verificar si existe un producto con los filtros dados"""
        for field, value in filters.items():
            if await self.db.exists_by_field(field, value):
                return True
        return False

    async def exists_by_field(
        self,
        field: str,
        value: Any,
        exclude_id: Optional[int] = None
    ) -> bool:
        """Verificar si existe un producto por campo específico"""
        return await self.db.exists_by_field(field, value, exclude_id)

    async def filter_products(self, filters: Dict[str, Any]) -> List[ProductInDB]:
        """Filtrar productos según criterios"""
        filtered_data = await self.db.filter_products(filters)
        return [ProductInDB(**product) for product in filtered_data]

    async def get_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de productos"""
        return await self.db.get_stats()

    async def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Contar productos con filtros opcionales"""
        if filters:
            filtered_products = await self.filter_products(filters)
            return len(filtered_products)
        else:
            all_products = await self.db.get_all()
            return len(all_products)

# Instancia global del repository
product_repository = ProductRepository()
```

### **app/services/product_service.py**

```python
from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status

from app.repositories.product_repository import ProductRepository
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductInDB, ProductResponse,
    ProductList, ProductFilter, ProductStats
)
from app.core.exceptions import (
    ResourceNotFoundError, ConflictError, BusinessLogicError
)
from app.config.settings import settings

class ProductService:
    """Servicio de lógica de negocio para productos"""

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def create_product(self, product_data: ProductCreate) -> ProductResponse:
        """Crear un nuevo producto con validaciones de negocio"""

        # Validar SKU único
        if await self.repository.exists_by_field("sku", product_data.sku):
            raise ConflictError(
                message=f"Ya existe un producto con SKU '{product_data.sku}'",
                conflict_type="sku_duplicate"
            )

        # Validar nombre único
        if await self.repository.exists_by_field("name", product_data.name):
            raise ConflictError(
                message=f"Ya existe un producto con el nombre '{product_data.name}'",
                conflict_type="name_duplicate"
            )

        # Validar lógica de negocio: productos caros con alto stock
        if product_data.price > 10000 and product_data.stock_quantity > 100:
            raise BusinessLogicError(
                message="Productos de alto valor no pueden tener stock masivo sin aprobación",
                rule="high_value_stock_limit",
                details={
                    "max_allowed_stock": 100,
                    "price_threshold": 10000
                }
            )

        # Crear producto
        product = await self.repository.create(product_data.dict())

        # Calcular campos adicionales
        estimated_value = float(product.price * product.stock_quantity)
        popularity_score = min(10.0, product.stock_quantity / 10.0)

        # Actualizar con campos calculados
        updated_product = await self.repository.update(
            product.id,
            {
                "estimated_value": estimated_value,
                "popularity_score": popularity_score
            }
        )

        return ProductResponse(**updated_product.dict())

    async def get_product(self, product_id: int) -> ProductResponse:
        """Obtener producto por ID"""

        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundError("Producto", product_id)

        return ProductResponse(**product.dict())

    async def update_product(
        self,
        product_id: int,
        product_data: ProductUpdate
    ) -> ProductResponse:
        """Actualizar producto existente"""

        # Verificar que existe
        existing_product = await self.repository.get_by_id(product_id)
        if not existing_product:
            raise ResourceNotFoundError("Producto", product_id)

        # Validar SKU único (excluyendo el producto actual)
        if await self.repository.exists_by_field(
            "sku",
            product_data.sku,
            exclude_id=product_id
        ):
            raise ConflictError(
                message=f"Ya existe otro producto con SKU '{product_data.sku}'",
                conflict_type="sku_duplicate"
            )

        # Validar nombre único (excluyendo el producto actual)
        if await self.repository.exists_by_field(
            "name",
            product_data.name,
            exclude_id=product_id
        ):
            raise ConflictError(
                message=f"Ya existe otro producto con el nombre '{product_data.name}'",
                conflict_type="name_duplicate"
            )

        # Aplicar validaciones de negocio
        if product_data.price > 10000 and product_data.stock_quantity > 100:
            raise BusinessLogicError(
                message="Productos de alto valor no pueden tener stock masivo sin aprobación",
                rule="high_value_stock_limit"
            )

        # Actualizar producto
        update_data = product_data.dict()

        # Recalcular campos
        update_data["estimated_value"] = float(product_data.price * product_data.stock_quantity)
        update_data["popularity_score"] = min(10.0, product_data.stock_quantity / 10.0)

        updated_product = await self.repository.update(product_id, update_data)

        return ProductResponse(**updated_product.dict())

    async def delete_product(self, product_id: int) -> bool:
        """Eliminar producto con validaciones de negocio"""

        # Verificar que existe
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ResourceNotFoundError("Producto", product_id)

        # Validaciones de negocio para eliminación
        # (En un sistema real, verificaríamos órdenes activas, etc.)

        return await self.repository.delete(product_id)

    async def list_products(
        self,
        filters: ProductFilter,
        page: int = 1,
        page_size: int = None
    ) -> ProductList:
        """Listar productos con filtros y paginación"""

        if page_size is None:
            page_size = settings.DEFAULT_PAGE_SIZE

        page_size = min(page_size, settings.MAX_PAGE_SIZE)

        # Aplicar filtros
        filter_dict = {k: v for k, v in filters.dict().items() if v is not None}

        # Obtener productos filtrados
        filtered_products = await self.repository.filter_products(filter_dict)

        # Aplicar paginación
        total = len(filtered_products)
        skip = (page - 1) * page_size
        paginated_products = filtered_products[skip:skip + page_size]

        # Calcular metadatos de paginación
        total_pages = (total + page_size - 1) // page_size
        has_next = page < total_pages
        has_previous = page > 1

        return ProductList(
            items=[ProductResponse(**product.dict()) for product in paginated_products],
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=has_next,
            has_previous=has_previous
        )

    async def get_stats(self) -> ProductStats:
        """Obtener estadísticas de productos"""

        stats_data = await self.repository.get_stats()
        return ProductStats(**stats_data)

# Instancia del servicio
def get_product_service() -> ProductService:
    """Dependency para obtener el servicio de productos"""
    from app.repositories.product_repository import product_repository
    return ProductService(product_repository)
```

## 🔧 Paso 5: Endpoints Organizados y API Routes (15 min)

### **app/api/v1/endpoints/products.py**

```python
from fastapi import APIRouter, Depends, status, Query, Path
from typing import Optional

from app.services.product_service import ProductService, get_product_service
from app.schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductList,
    ProductFilter, ProductStats, CategoryEnum, BrandEnum
)
from app.core.exceptions import handle_errors

router = APIRouter()

@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo producto",
    description="Crea un nuevo producto en el inventario con validaciones completas"
)
@handle_errors
async def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
):
    """Crear un nuevo producto"""
    return await service.create_product(product)

@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Obtener producto por ID",
    description="Obtiene un producto específico por su ID único"
)
@handle_errors
async def get_product(
    product_id: int = Path(..., gt=0, description="ID del producto"),
    service: ProductService = Depends(get_product_service)
):
    """Obtener producto por ID"""
    return await service.get_product(product_id)

@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Actualizar producto",
    description="Actualiza completamente un producto existente"
)
@handle_errors
async def update_product(
    product_id: int = Path(..., gt=0, description="ID del producto"),
    product: ProductUpdate,
    service: ProductService = Depends(get_product_service)
):
    """Actualizar producto existente"""
    return await service.update_product(product_id, product)

@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar producto",
    description="Elimina un producto del inventario permanentemente"
)
@handle_errors
async def delete_product(
    product_id: int = Path(..., gt=0, description="ID del producto"),
    service: ProductService = Depends(get_product_service)
):
    """Eliminar producto"""
    await service.delete_product(product_id)
    return None

@router.get(
    "/",
    response_model=ProductList,
    summary="Listar productos",
    description="Obtiene una lista paginada de productos con filtros opcionales"
)
@handle_errors
async def list_products(
    # Filtros
    category: Optional[CategoryEnum] = Query(None, description="Filtrar por categoría"),
    brand: Optional[BrandEnum] = Query(None, description="Filtrar por marca"),
    in_stock: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    is_digital: Optional[bool] = Query(None, description="Filtrar productos digitales"),
    search: Optional[str] = Query(None, min_length=2, description="Búsqueda de texto"),

    # Paginación
    page: int = Query(1, ge=1, description="Número de página"),
    page_size: int = Query(10, ge=1, le=100, description="Elementos por página"),

    service: ProductService = Depends(get_product_service)
):
    """Listar productos con filtros y paginación"""

    filters = ProductFilter(
        category=category,
        brand=brand,
        in_stock=in_stock,
        min_price=min_price,
        max_price=max_price,
        is_digital=is_digital,
        search=search
    )

    return await service.list_products(filters, page, page_size)

@router.get(
    "/stats/summary",
    response_model=ProductStats,
    summary="Estadísticas de inventario",
    description="Obtiene estadísticas generales del inventario de productos"
)
@handle_errors
async def get_product_stats(
    service: ProductService = Depends(get_product_service)
):
    """Obtener estadísticas de productos"""
    return await service.get_stats()
```

### **app/api/v1/endpoints/health.py**

```python
from fastapi import APIRouter, status
from datetime import datetime
from app.config.settings import settings

router = APIRouter()

@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Endpoint para verificar el estado de la API"
)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.APP_VERSION,
        "service": settings.APP_NAME
    }

@router.get(
    "/health/detailed",
    status_code=status.HTTP_200_OK,
    summary="Detailed Health Check",
    description="Health check detallado con información del sistema"
)
async def detailed_health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": settings.APP_VERSION,
        "service": settings.APP_NAME,
        "environment": {
            "debug": settings.DEBUG,
            "api_version": settings.API_V1_STR
        },
        "dependencies": {
            "database": "healthy",  # En un sistema real, verificaríamos la conexión
            "cache": "healthy",
            "external_services": "healthy"
        }
    }
```

### **app/api/v1/api.py**

```python
from fastapi import APIRouter

from app.api.v1.endpoints import products, health

api_router = APIRouter()

# Incluir routers de endpoints
api_router.include_router(
    health.router,
    tags=["health"]
)

api_router.include_router(
    products.router,
    prefix="/products",
    tags=["products"]
)
```

### **app/main.py**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.core.logging import setup_logging
from app.core.exceptions import setup_exception_handlers
from app.api.v1.api import api_router

# Configurar logging
setup_logging()

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    openapi_url=settings.OPENAPI_URL
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# Configurar exception handlers
setup_exception_handlers(app)

# Incluir routers de API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/", tags=["root"])
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": f"Bienvenido a {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "docs": settings.DOCS_URL,
        "redoc": settings.REDOC_URL
    }
```

## ✅ Entregables Finales

Al finalizar esta práctica deberías tener:

1. ✅ **Estructura de proyecto profesional** completamente organizada
2. ✅ **Separación clara de responsabilidades** (Services, Repositories, Schemas)
3. ✅ **Configuración centralizada** y basada en entorno
4. ✅ **API versionada** con endpoints bien estructurados
5. ✅ **Patterns de diseño** implementados (Repository, Service Layer)
6. ✅ **Código mantenible y escalable** siguiendo mejores prácticas

### **Comandos de Testing Final**

```bash
# Ejecutar la API estructurada
cd semana-03-inventory-api
uvicorn app.main:app --reload

# Testing de endpoints
curl -X GET "http://localhost:8000/api/v1/health"
curl -X GET "http://localhost:8000/api/v1/products"
curl -X GET "http://localhost:8000/api/v1/products/stats/summary"

# Documentación automática
# http://localhost:8000/docs
# http://localhost:8000/redoc
```

## 🎯 Conclusión de Semana 3

Has completado exitosamente una API REST profesional con:

- ✅ **Arquitectura escalable** y bien organizada
- ✅ **Validación robusta** con Pydantic avanzado
- ✅ **Manejo de errores** profesional y consistente
- ✅ **Estructura REST** siguiendo mejores prácticas
- ✅ **Código de calidad** listo para producción

---

_Práctica desarrollada para Semana 3 - Bootcamp FastAPI_  
_Tiempo estimado: 90 minutos_
