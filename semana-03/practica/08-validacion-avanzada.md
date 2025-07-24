# Práctica 8: Validación Avanzada - Semana 3

## 🎯 Objetivo

Implementar validación robusta y avanzada en FastAPI usando Pydantic, incluyendo validadores custom, dependencias, y manejo sofisticado de parámetros.

## ⏱️ Tiempo Estimado: 90 minutos

## 📋 Pre-requisitos

- ✅ API con endpoints HTTP completos (Práctica 7)
- ✅ Comprensión de Pydantic básico
- ✅ Familiaridad con validators de Python

## 🧱 Paso 1: Validadores Custom Avanzados (25 min)

### **Expandir Modelos con Validación Sofisticada**

Actualiza `models/product_models.py`:

```python
from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
import re
from decimal import Decimal

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

class ProductValidated(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre del producto (2-100 caracteres)"
    )

    price: Decimal = Field(
        ...,
        gt=0,
        le=999999.99,
        decimal_places=2,
        description="Precio del producto con máximo 2 decimales"
    )

    sku: str = Field(
        ...,
        min_length=6,
        max_length=20,
        description="Código SKU del producto (formato: CAT-BRAND-XXXX)"
    )

    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Descripción detallada del producto"
    )

    category: CategoryEnum = Field(..., description="Categoría del producto")
    brand: BrandEnum = Field(..., description="Marca del producto")

    weight: Optional[float] = Field(
        None,
        gt=0,
        le=1000,
        description="Peso en kilogramos (0-1000 kg)"
    )

    dimensions: Optional[Dict[str, float]] = Field(
        None,
        description="Dimensiones: {length, width, height} en cm"
    )

    tags: Optional[List[str]] = Field(
        None,
        max_items=10,
        description="Etiquetas del producto (máximo 10)"
    )

    release_date: Optional[date] = Field(
        None,
        description="Fecha de lanzamiento del producto"
    )

    is_digital: bool = Field(
        False,
        description="Indica si es un producto digital"
    )

    min_age: Optional[int] = Field(
        None,
        ge=0,
        le=100,
        description="Edad mínima recomendada"
    )

    warranty_months: Optional[int] = Field(
        None,
        ge=0,
        le=120,
        description="Meses de garantía (0-120)"
    )

    # Validadores personalizados
    @validator('name')
    def validate_name(cls, v):
        # Eliminar espacios extra y capitalizar
        v = ' '.join(v.split())

        # No permitir solo números
        if v.isdigit():
            raise ValueError('El nombre no puede ser solo números')

        # No permitir caracteres especiales problemáticos
        forbidden_chars = ['<', '>', '"', "'", '&', '%']
        if any(char in v for char in forbidden_chars):
            raise ValueError(f'El nombre no puede contener: {", ".join(forbidden_chars)}')

        return v.title()

    @validator('sku')
    def validate_sku(cls, v):
        # Formato: CAT-BRAND-XXXX (ej: ELE-APPLE-1234)
        pattern = r'^[A-Z]{3}-[A-Z]{3,6}-[A-Z0-9]{4}$'

        v = v.upper().strip()

        if not re.match(pattern, v):
            raise ValueError(
                'SKU debe tener formato CAT-BRAND-XXXX '
                '(ej: ELE-APPLE-1234, CLO-NIKE-AB12)'
            )

        return v

    @validator('description')
    def validate_description(cls, v):
        if v is None:
            return v

        # Eliminar espacios extra
        v = ' '.join(v.split())

        # Mínimo de palabras para descripción
        if len(v.split()) < 3:
            raise ValueError('La descripción debe tener al menos 3 palabras')

        return v

    @validator('dimensions')
    def validate_dimensions(cls, v):
        if v is None:
            return v

        required_keys = {'length', 'width', 'height'}

        # Verificar que tenga las claves requeridas
        if not required_keys.issubset(v.keys()):
            raise ValueError(f'Dimensiones debe incluir: {", ".join(required_keys)}')

        # Verificar que todos los valores sean positivos
        for key, value in v.items():
            if key in required_keys and (not isinstance(value, (int, float)) or value <= 0):
                raise ValueError(f'{key} debe ser un número positivo')

        # Verificar rangos razonables (en cm)
        max_dimension = 500  # 5 metros
        for key, value in v.items():
            if key in required_keys and value > max_dimension:
                raise ValueError(f'{key} no puede ser mayor a {max_dimension} cm')

        return v

    @validator('tags')
    def validate_tags(cls, v):
        if v is None:
            return v

        # Limpiar y validar cada tag
        cleaned_tags = []
        for tag in v:
            tag = tag.strip().lower()

            if len(tag) < 2:
                raise ValueError('Cada etiqueta debe tener al menos 2 caracteres')

            if len(tag) > 30:
                raise ValueError('Cada etiqueta no puede tener más de 30 caracteres')

            if tag not in cleaned_tags:  # Evitar duplicados
                cleaned_tags.append(tag)

        return cleaned_tags

    @validator('release_date')
    def validate_release_date(cls, v):
        if v is None:
            return v

        # No permitir fechas muy antiguas o muy futuras
        min_date = date(1900, 1, 1)
        max_date = date.today().replace(year=date.today().year + 5)

        if v < min_date or v > max_date:
            raise ValueError(f'Fecha debe estar entre {min_date} y {max_date}')

        return v

    # Validadores de raíz (cross-field validation)
    @root_validator
    def validate_digital_product_logic(cls, values):
        is_digital = values.get('is_digital', False)
        weight = values.get('weight')
        dimensions = values.get('dimensions')

        if is_digital:
            # Productos digitales no deberían tener peso o dimensiones
            if weight is not None and weight > 0:
                raise ValueError('Productos digitales no pueden tener peso')

            if dimensions is not None:
                raise ValueError('Productos digitales no pueden tener dimensiones físicas')

        return values

    @root_validator
    def validate_sku_category_consistency(cls, values):
        sku = values.get('sku')
        category = values.get('category')

        if sku and category:
            # Mapeo de categorías a prefijos SKU
            category_prefixes = {
                'electronics': 'ELE',
                'clothing': 'CLO',
                'books': 'BOO',
                'home': 'HOM',
                'sports': 'SPO',
                'beauty': 'BEA',
                'automotive': 'AUT'
            }

            expected_prefix = category_prefixes.get(category.value)
            if expected_prefix and not sku.startswith(expected_prefix):
                raise ValueError(
                    f'SKU debe comenzar con {expected_prefix} para categoría {category.value}'
                )

        return values

    @root_validator
    def validate_brand_category_compatibility(cls, values):
        brand = values.get('brand')
        category = values.get('category')

        if brand and category:
            # Definir compatibilidades de marca-categoría
            brand_categories = {
                'apple': ['electronics'],
                'samsung': ['electronics'],
                'sony': ['electronics'],
                'nike': ['clothing', 'sports'],
                'adidas': ['clothing', 'sports'],
                'generic': ['electronics', 'clothing', 'books', 'home', 'sports', 'beauty', 'automotive']
            }

            allowed_categories = brand_categories.get(brand.value, [])
            if category.value not in allowed_categories:
                raise ValueError(
                    f'Marca {brand.value} no es compatible con categoría {category.value}'
                )

        return values

class ProductCreateValidated(ProductValidated):
    in_stock: bool = Field(True, description="Producto disponible en stock")
    stock_quantity: int = Field(
        0,
        ge=0,
        le=9999,
        description="Cantidad disponible en inventario"
    )

    supplier_email: Optional[str] = Field(
        None,
        regex=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        description="Email del proveedor"
    )

    @validator('stock_quantity')
    def validate_stock_consistency(cls, v, values):
        in_stock = values.get('in_stock', True)

        if in_stock and v == 0:
            raise ValueError('Si el producto está en stock, la cantidad debe ser mayor a 0')

        if not in_stock and v > 0:
            raise ValueError('Si el producto no está en stock, la cantidad debe ser 0')

        return v

class ProductUpdateValidated(ProductValidated):
    in_stock: bool = Field(..., description="Producto disponible en stock")
    stock_quantity: int = Field(
        ...,
        ge=0,
        le=9999,
        description="Cantidad disponible en inventario"
    )

    @validator('stock_quantity')
    def validate_stock_consistency(cls, v, values):
        in_stock = values.get('in_stock', True)

        if in_stock and v == 0:
            raise ValueError('Si el producto está en stock, la cantidad debe ser mayor a 0')

        if not in_stock and v > 0:
            raise ValueError('Si el producto no está en stock, la cantidad debe ser 0')

        return v

class ProductResponseValidated(ProductValidated):
    id: int = Field(..., description="ID único del producto")
    in_stock: bool
    stock_quantity: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Campos calculados
    estimated_value: Optional[float] = Field(None, description="Valor estimado del inventario")
    popularity_score: Optional[float] = Field(None, ge=0, le=10, description="Score de popularidad")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "iPhone 14 Pro",
                "price": 1199.99,
                "sku": "ELE-APPLE-I14P",
                "description": "Smartphone premium con cámara avanzada y chip A16",
                "category": "electronics",
                "brand": "apple",
                "weight": 0.206,
                "dimensions": {
                    "length": 15.54,
                    "width": 7.65,
                    "height": 0.79
                },
                "tags": ["smartphone", "premium", "camera", "5g"],
                "release_date": "2022-09-16",
                "is_digital": False,
                "min_age": 13,
                "warranty_months": 12,
                "in_stock": True,
                "stock_quantity": 25,
                "created_at": "2025-07-24T10:00:00",
                "updated_at": None,
                "estimated_value": 29999.75,
                "popularity_score": 9.2
            }
        }
```

## 🔍 Paso 2: Validación de Parámetros de Query Avanzada (20 min)

Crear `utils/query_validators.py`:

```python
from fastapi import Query, HTTPException, status
from typing import Optional, List, Literal
from datetime import date, datetime
from enum import Enum

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class SortField(str, Enum):
    name = "name"
    price = "price"
    created_at = "created_at"
    stock_quantity = "stock_quantity"
    popularity_score = "popularity_score"

def validate_price_range(min_price: Optional[float], max_price: Optional[float]):
    """Validar que el rango de precios sea lógico"""
    if min_price is not None and max_price is not None:
        if min_price > max_price:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio mínimo no puede ser mayor al precio máximo"
            )

        if min_price < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El precio mínimo no puede ser negativo"
            )

def validate_date_range(start_date: Optional[date], end_date: Optional[date]):
    """Validar que el rango de fechas sea lógico"""
    if start_date is not None and end_date is not None:
        if start_date > end_date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La fecha de inicio no puede ser posterior a la fecha final"
            )

        # No permitir rangos muy amplios (más de 10 años)
        if (end_date - start_date).days > 3650:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El rango de fechas no puede ser mayor a 10 años"
            )

class AdvancedQueryParams:
    """Clase para manejar parámetros de query avanzados"""

    def __init__(
        self,
        # Filtros básicos
        category: Optional[str] = Query(None, description="Filtrar por categoría"),
        brand: Optional[str] = Query(None, description="Filtrar por marca"),
        in_stock: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),

        # Filtros de precio
        min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
        max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),

        # Filtros de fecha
        created_after: Optional[date] = Query(None, description="Creado después de esta fecha"),
        created_before: Optional[date] = Query(None, description="Creado antes de esta fecha"),

        # Filtros de inventario
        min_stock: Optional[int] = Query(None, ge=0, description="Stock mínimo"),
        max_stock: Optional[int] = Query(None, ge=0, description="Stock máximo"),

        # Filtros de peso/dimensiones
        max_weight: Optional[float] = Query(None, gt=0, description="Peso máximo en kg"),
        is_digital: Optional[bool] = Query(None, description="Solo productos digitales/físicos"),

        # Búsqueda de texto
        search: Optional[str] = Query(
            None,
            min_length=2,
            max_length=100,
            description="Buscar en nombre, descripción y tags"
        ),

        # Filtros por tags
        tags: Optional[List[str]] = Query(
            None,
            description="Filtrar por etiquetas (formato: ?tags=tag1&tags=tag2)"
        ),

        # Ordenamiento
        sort_by: SortField = Query(
            SortField.created_at,
            description="Campo por el cual ordenar"
        ),
        sort_order: SortOrder = Query(
            SortOrder.desc,
            description="Orden ascendente o descendente"
        ),

        # Paginación
        page: int = Query(1, ge=1, le=1000, description="Número de página"),
        page_size: int = Query(
            10,
            ge=1,
            le=100,
            description="Elementos por página (máximo 100)"
        ),

        # Incluir campos opcionales
        include_inactive: bool = Query(
            False,
            description="Incluir productos inactivos"
        ),
        include_calculated_fields: bool = Query(
            True,
            description="Incluir campos calculados (valor estimado, popularidad)"
        )
    ):
        # Validaciones cross-parameter
        validate_price_range(min_price, max_price)
        validate_date_range(created_after, created_before)

        if min_stock is not None and max_stock is not None and min_stock > max_stock:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El stock mínimo no puede ser mayor al stock máximo"
            )

        # Asignar valores
        self.category = category
        self.brand = brand
        self.in_stock = in_stock
        self.min_price = min_price
        self.max_price = max_price
        self.created_after = created_after
        self.created_before = created_before
        self.min_stock = min_stock
        self.max_stock = max_stock
        self.max_weight = max_weight
        self.is_digital = is_digital
        self.search = search.strip() if search else None
        self.tags = [tag.strip().lower() for tag in tags] if tags else None
        self.sort_by = sort_by
        self.sort_order = sort_order
        self.page = page
        self.page_size = page_size
        self.include_inactive = include_inactive
        self.include_calculated_fields = include_calculated_fields
```

## 🔧 Paso 3: Actualizar Endpoints con Validación Avanzada (25 min)

Actualizar `main.py`:

```python
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
from models.product_models import (
    ProductCreateValidated, ProductUpdateValidated,
    ProductResponseValidated, CategoryEnum, BrandEnum
)
from utils.query_validators import AdvancedQueryParams
from data.products_data import *

app = FastAPI(
    title="API de Inventario Avanzada - Semana 3",
    description="API REST con validación robusta para manejo de productos",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get(
    "/products",
    response_model=Dict[str, Any],
    summary="Obtener productos con filtros avanzados",
    description="Endpoint con validación avanzada y múltiples filtros"
)
async def get_products_advanced(
    params: AdvancedQueryParams = Depends()
):
    try:
        # Aplicar filtros (implementación simplificada)
        products = get_all_products()
        filtered_products = []

        for product in products:
            # Aplicar todos los filtros
            if params.category and product.get("category") != params.category:
                continue

            if params.brand and product.get("brand") != params.brand:
                continue

            if params.in_stock is not None and product.get("in_stock") != params.in_stock:
                continue

            if params.min_price is not None and product.get("price", 0) < params.min_price:
                continue

            if params.max_price is not None and product.get("price", 0) > params.max_price:
                continue

            if params.min_stock is not None and product.get("stock_quantity", 0) < params.min_stock:
                continue

            if params.max_stock is not None and product.get("stock_quantity", 0) > params.max_stock:
                continue

            if params.is_digital is not None and product.get("is_digital", False) != params.is_digital:
                continue

            # Búsqueda de texto
            if params.search:
                search_text = params.search.lower()
                searchable_text = f"{product.get('name', '')} {product.get('description', '')}".lower()
                product_tags = product.get('tags', [])

                if search_text not in searchable_text and not any(search_text in tag for tag in product_tags):
                    continue

            # Filtro por tags
            if params.tags:
                product_tags = [tag.lower() for tag in product.get('tags', [])]
                if not any(tag in product_tags for tag in params.tags):
                    continue

            filtered_products.append(product)

        # Aplicar ordenamiento
        reverse_order = params.sort_order.value == "desc"

        if params.sort_by.value == "name":
            filtered_products.sort(key=lambda x: x.get("name", ""), reverse=reverse_order)
        elif params.sort_by.value == "price":
            filtered_products.sort(key=lambda x: x.get("price", 0), reverse=reverse_order)
        elif params.sort_by.value == "stock_quantity":
            filtered_products.sort(key=lambda x: x.get("stock_quantity", 0), reverse=reverse_order)
        # Agregar más campos de ordenamiento según necesidad

        # Aplicar paginación
        total = len(filtered_products)
        start_idx = (params.page - 1) * params.page_size
        end_idx = start_idx + params.page_size
        paginated_products = filtered_products[start_idx:end_idx]

        # Calcular campos adicionales si está habilitado
        if params.include_calculated_fields:
            for product in paginated_products:
                product["estimated_value"] = product.get("price", 0) * product.get("stock_quantity", 0)
                product["popularity_score"] = min(10.0, product.get("stock_quantity", 0) / 10.0)

        return {
            "success": True,
            "data": {
                "products": paginated_products,
                "pagination": {
                    "total": total,
                    "page": params.page,
                    "page_size": params.page_size,
                    "total_pages": (total + params.page_size - 1) // params.page_size
                },
                "filters_applied": {
                    "category": params.category,
                    "brand": params.brand,
                    "in_stock": params.in_stock,
                    "price_range": f"{params.min_price}-{params.max_price}" if params.min_price or params.max_price else None,
                    "search": params.search,
                    "tags": params.tags
                },
                "sorting": {
                    "field": params.sort_by.value,
                    "order": params.sort_order.value
                }
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error en el procesamiento: {str(e)}"
        )

@app.post(
    "/products",
    response_model=ProductResponseValidated,
    status_code=status.HTTP_201_CREATED,
    summary="Crear producto con validación avanzada"
)
async def create_product_advanced(product: ProductCreateValidated):
    try:
        # Validaciones adicionales de negocio
        existing_products = get_all_products()

        # Verificar SKU único
        for existing in existing_products:
            if existing.get("sku") == product.sku:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un producto con SKU '{product.sku}'"
                )

        # Crear producto con todos los campos
        product_data = product.dict()

        # Agregar campos calculados
        product_data["estimated_value"] = product.price * product.stock_quantity
        product_data["popularity_score"] = 5.0  # Score inicial

        new_product = create_product(product_data)

        return ProductResponseValidated(**new_product)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear producto: {str(e)}"
        )
```

## 🧪 Paso 4: Testing de Validación Avanzada (20 min)

### **Testing de Validaciones Custom**

```bash
# 1. Crear producto con validación exitosa
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "iPhone 15 Pro Max",
    "price": 1299.99,
    "sku": "ELE-APPLE-I15P",
    "description": "El smartphone más avanzado de Apple con chip A17 Pro",
    "category": "electronics",
    "brand": "apple",
    "weight": 0.221,
    "dimensions": {
      "length": 16.01,
      "width": 7.70,
      "height": 0.83
    },
    "tags": ["smartphone", "premium", "5g", "pro"],
    "release_date": "2023-09-22",
    "is_digital": false,
    "min_age": 13,
    "warranty_months": 12,
    "in_stock": true,
    "stock_quantity": 50,
    "supplier_email": "apple@supplier.com"
  }'

# 2. Intentar crear producto con SKU inválido (debe fallar)
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Producto Inválido",
    "price": 99.99,
    "sku": "INVALID-SKU",
    "description": "Este producto tiene SKU inválido",
    "category": "electronics",
    "brand": "generic",
    "in_stock": true,
    "stock_quantity": 10
  }'

# 3. Intentar crear producto digital con peso (debe fallar)
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Software Premium",
    "price": 199.99,
    "sku": "ELE-GENER-SW01",
    "description": "Software digital para productividad avanzada",
    "category": "electronics",
    "brand": "generic",
    "weight": 0.5,
    "is_digital": true,
    "in_stock": true,
    "stock_quantity": 100
  }'

# 4. Intentar crear con marca incompatible (debe fallar)
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Libro de Apple",
    "price": 29.99,
    "sku": "BOO-APPLE-BK01",
    "description": "Un libro sobre tecnología Apple",
    "category": "books",
    "brand": "apple",
    "in_stock": true,
    "stock_quantity": 20
  }'
```

### **Testing de Query Parameters Avanzados**

```bash
# 1. Búsqueda con múltiples filtros
curl -X GET "http://localhost:8000/products?category=electronics&brand=apple&min_price=1000&max_price=1500&in_stock=true&sort_by=price&sort_order=desc"

# 2. Búsqueda por texto
curl -X GET "http://localhost:8000/products?search=smartphone&include_calculated_fields=true"

# 3. Filtros de stock
curl -X GET "http://localhost:8000/products?min_stock=10&max_stock=100&sort_by=stock_quantity&sort_order=asc"

# 4. Filtros con tags
curl -X GET "http://localhost:8000/products?tags=premium&tags=smartphone"

# 5. Paginación avanzada
curl -X GET "http://localhost:8000/products?page=1&page_size=5&sort_by=name&sort_order=asc"

# 6. Intentar rango de precios inválido (debe fallar)
curl -X GET "http://localhost:8000/products?min_price=1000&max_price=500"
```

## ✅ Entregables

Al finalizar esta práctica deberías tener:

1. ✅ **Validadores custom** complejos implementados
2. ✅ **Cross-field validation** funcionando
3. ✅ **Query parameters** con validación avanzada
4. ✅ **Manejo de errores** específicos y detallados
5. ✅ **Testing exhaustivo** de validaciones
6. ✅ **Documentación automática** con ejemplos claros

## 🎯 Próximo Paso

En la siguiente práctica (09-manejo-errores.md) implementaremos un sistema robusto de manejo de errores y responses consistentes.

---

_Práctica desarrollada para Semana 3 - Bootcamp FastAPI_  
_Tiempo estimado: 90 minutos_
