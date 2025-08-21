# Ejemplo para Proyecto Semana 3: API de Productos con Validaciones
# Este archivo demuestra validaciones Pydantic y manejo básico de errores

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict
from enum import Enum

# ==================== MODELOS PYDANTIC ====================

class ProductStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    out_of_stock = "out_of_stock"

class ProductCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    books = "books"
    home = "home"
    sports = "sports"
    other = "other"

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del producto")
    description: Optional[str] = Field(None, max_length=500, description="Descripción del producto")
    price: float = Field(..., gt=0, description="Precio debe ser mayor que 0")
    stock: int = Field(..., ge=0, description="Stock no puede ser negativo")
    category: ProductCategory = Field(default=ProductCategory.other)
    status: ProductStatus = Field(default=ProductStatus.active)

    @validator('name')
    def validate_name(cls, v):
        """Capitalizar y limpiar espacios en el nombre"""
        cleaned = v.strip().title()
        if len(cleaned) < 2:
            raise ValueError('Nombre debe tener al menos 2 caracteres después de limpiar')
        return cleaned

    @validator('price')
    def validate_price(cls, v):
        """Redondear precio a 2 decimales"""
        return round(v, 2)

    @validator('description')
    def validate_description(cls, v):
        """Limpiar descripción si existe"""
        if v is not None:
            cleaned = v.strip()
            return cleaned if cleaned else None
        return v

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[ProductCategory] = None
    status: Optional[ProductStatus] = None

    @validator('name')
    def validate_name(cls, v):
        if v is not None:
            cleaned = v.strip().title()
            if len(cleaned) < 2:
                raise ValueError('Nombre debe tener al menos 2 caracteres')
            return cleaned
        return v

    @validator('price')
    def validate_price(cls, v):
        if v is not None:
            return round(v, 2)
        return v

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

# ==================== CONFIGURACIÓN FASTAPI ====================

app = FastAPI(
    title="API de Productos - Semana 3",
    description="API para gestión de productos con validaciones Pydantic y manejo de errores",
    version="1.0.0"
)

# Base de datos en memoria
products_db: Dict[int, dict] = {}
next_id: int = 1

# ==================== FUNCIONES AUXILIARES ====================

def get_current_time() -> datetime:
    return datetime.now()

def product_not_found(product_id: int):
    """Helper para error 404"""
    raise HTTPException(
        status_code=404,
        detail=f"Producto con ID {product_id} no encontrado"
    )

def validation_error(message: str):
    """Helper para errores de validación custom"""
    raise HTTPException(
        status_code=400,
        detail=message
    )

def create_product_record(product_data: ProductCreate) -> dict:
    """Crear registro de producto con timestamp"""
    global next_id
    
    # Verificar si ya existe un producto con el mismo nombre (bonus)
    for existing_product in products_db.values():
        if existing_product["name"].lower() == product_data.name.lower():
            validation_error(f"Ya existe un producto con el nombre '{product_data.name}'")
    
    product_dict = product_data.dict()
    product_dict.update({
        "id": next_id,
        "created_at": get_current_time(),
        "updated_at": get_current_time()
    })
    
    products_db[next_id] = product_dict
    next_id += 1
    return product_dict

# ==================== ENDPOINTS ====================

@app.get("/")
def read_root():
    """Endpoint de bienvenida"""
    return {
        "message": "Bienvenido a la API de Productos - Semana 3",
        "version": "1.0.0",
        "docs": "/docs",
        "total_products": len(products_db),
        "features": [
            "CRUD completo de productos",
            "Validaciones Pydantic avanzadas", 
            "Manejo de errores con HTTPException",
            "Filtros por precio y categoría"
        ]
    }

# ==================== CRUD ENDPOINTS ====================

@app.post("/products", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate):
    """Crear un nuevo producto"""
    product_record = create_product_record(product)
    return ProductResponse(**product_record)

@app.get("/products", response_model=List[ProductResponse])
def get_products(
    min_price: Optional[float] = Query(None, ge=0, description="Precio mínimo"),
    max_price: Optional[float] = Query(None, ge=0, description="Precio máximo"),
    category: Optional[ProductCategory] = Query(None, description="Filtrar por categoría"),
    status: Optional[ProductStatus] = Query(None, description="Filtrar por estado"),
    limit: int = Query(20, ge=1, le=100, description="Límite de resultados")
):
    """Listar productos con filtros opcionales"""
    products = list(products_db.values())
    
    # Aplicar filtros
    if min_price is not None:
        products = [p for p in products if p["price"] >= min_price]
    
    if max_price is not None:
        products = [p for p in products if p["price"] <= max_price]
    
    if category is not None:
        products = [p for p in products if p["category"] == category]
    
    if status is not None:
        products = [p for p in products if p["status"] == status]
    
    # Validar rango de precios
    if min_price is not None and max_price is not None and min_price > max_price:
        validation_error("El precio mínimo no puede ser mayor que el precio máximo")
    
    # Limitar resultados
    products = products[:limit]
    
    return [ProductResponse(**product) for product in products]

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int):
    """Obtener un producto específico por ID"""
    if product_id not in products_db:
        product_not_found(product_id)
    
    return ProductResponse(**products_db[product_id])

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate):
    """Actualizar un producto completamente"""
    if product_id not in products_db:
        product_not_found(product_id)
    
    # Verificar nombre único excluyendo el producto actual
    for existing_id, existing_product in products_db.items():
        if (existing_id != product_id and 
            existing_product["name"].lower() == product.name.lower()):
            validation_error(f"Ya existe otro producto con el nombre '{product.name}'")
    
    # Actualizar con todos los datos nuevos
    updated_data = product.dict()
    updated_data.update({
        "id": product_id,
        "created_at": products_db[product_id]["created_at"],
        "updated_at": get_current_time()
    })
    
    products_db[product_id] = updated_data
    return ProductResponse(**updated_data)

@app.patch("/products/{product_id}", response_model=ProductResponse)
def update_product_partial(product_id: int, product: ProductUpdate):
    """Actualizar un producto parcialmente"""
    if product_id not in products_db:
        product_not_found(product_id)
    
    # Verificar nombre único si se está actualizando
    if product.name is not None:
        for existing_id, existing_product in products_db.items():
            if (existing_id != product_id and 
                existing_product["name"].lower() == product.name.lower()):
                validation_error(f"Ya existe otro producto con el nombre '{product.name}'")
    
    # Actualizar solo los campos proporcionados
    current_product = products_db[product_id].copy()
    update_data = product.dict(exclude_unset=True)
    
    current_product.update(update_data)
    current_product["updated_at"] = get_current_time()
    
    products_db[product_id] = current_product
    return ProductResponse(**current_product)

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    """Eliminar un producto (BONUS)"""
    if product_id not in products_db:
        product_not_found(product_id)
    
    deleted_product = products_db.pop(product_id)
    return {
        "message": f"Producto '{deleted_product['name']}' eliminado correctamente",
        "deleted_product": {
            "id": deleted_product["id"],
            "name": deleted_product["name"],
            "price": deleted_product["price"]
        }
    }

# ==================== ENDPOINTS ADICIONALES (BONUS) ====================

@app.get("/products/stats/summary")
def get_products_summary():
    """Obtener resumen estadístico de productos (BONUS)"""
    if not products_db:
        return {
            "total_products": 0,
            "total_value": 0,
            "average_price": 0,
            "categories": {},
            "status_counts": {}
        }
    
    total_products = len(products_db)
    total_value = sum(p["price"] * p["stock"] for p in products_db.values())
    average_price = sum(p["price"] for p in products_db.values()) / total_products
    
    # Contar por categorías
    categories = {}
    status_counts = {}
    
    for product in products_db.values():
        # Categorías
        cat = product["category"]
        categories[cat] = categories.get(cat, 0) + 1
        
        # Estados
        status = product["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    return {
        "total_products": total_products,
        "total_inventory_value": round(total_value, 2),
        "average_price": round(average_price, 2),
        "categories": categories,
        "status_counts": status_counts
    }

@app.get("/products/category/{category}", response_model=List[ProductResponse])
def get_products_by_category(category: ProductCategory):
    """Obtener productos por categoría específica (BONUS)"""
    products = [p for p in products_db.values() if p["category"] == category]
    return [ProductResponse(**product) for product in products]

# ==================== DATOS DE EJEMPLO ====================

def add_sample_data():
    """Agregar datos de ejemplo al iniciar la aplicación"""
    sample_products = [
        {
            "name": "laptop gamer",
            "description": "Laptop para gaming con RTX 4060",
            "price": 899.99,
            "stock": 5,
            "category": ProductCategory.electronics,
            "status": ProductStatus.active
        },
        {
            "name": "camiseta básica",
            "description": "Camiseta de algodón 100%",
            "price": 19.99,
            "stock": 25,
            "category": ProductCategory.clothing,
            "status": ProductStatus.active
        },
        {
            "name": "python cookbook",
            "description": "Recetas de programación en Python",
            "price": 45.50,
            "stock": 0,
            "category": ProductCategory.books,
            "status": ProductStatus.out_of_stock
        },
        {
            "name": "mouse inalámbrico",
            "description": "Mouse ergonómico inalámbrico",
            "price": 29.99,
            "stock": 15,
            "category": ProductCategory.electronics,
            "status": ProductStatus.active
        },
        {
            "name": "jean clásico",
            "description": "Jean azul talla 32",
            "price": 49.99,
            "stock": 8,
            "category": ProductCategory.clothing,
            "status": ProductStatus.inactive
        }
    ]
    
    for product_data in sample_products:
        product_create = ProductCreate(**product_data)
        create_product_record(product_create)

# Agregar datos de ejemplo al iniciar
add_sample_data()

# ==================== PUNTO DE ENTRADA ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
