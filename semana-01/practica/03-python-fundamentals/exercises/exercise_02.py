"""
Ejercicio 2: Modelos Pydantic Avanzados

Instrucciones:
1. Crea modelos Pydantic según las especificaciones
2. Implementa validadores personalizados
3. Añade configuración apropiada
"""

from pydantic import BaseModel, validator, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# TODO: Crear enum para categorías de productos
class ProductCategory(str, Enum):
    # Definir categorías: ELECTRONICS, CLOTHING, BOOKS, HOME, SPORTS
    pass

# TODO: Crear modelo Product
class Product(BaseModel):
    """
    Modelo para productos.
    
    Campos requeridos:
    - id: entero positivo
    - name: string (2-100 caracteres)
    - description: string opcional
    - price: float positivo
    - category: ProductCategory
    - in_stock: boolean (default True)
    - created_at: datetime (default now)
    - tags: lista opcional de strings
    
    Validadores:
    - name debe estar capitalizado
    - price debe tener máximo 2 decimales
    - tags no pueden estar vacíos si se proporcionan
    """
    # Tu código aquí
    pass

# TODO: Crear modelo Order
class Order(BaseModel):
    """
    Modelo para órdenes.
    
    Campos requeridos:
    - id: entero positivo
    - customer_email: email válido
    - products: lista de Product (mínimo 1)
    - order_date: datetime (default now)
    - status: enum (PENDING, PROCESSING, SHIPPED, DELIVERED)
    - total_amount: float calculado automáticamente
    
    Validadores:
    - total_amount debe coincidir con suma de precios de productos
    """
    # Tu código aquí
    pass

# TODO: Crear modelo OrderResponse (para API responses)
class OrderResponse(BaseModel):
    """
    Modelo de respuesta para órdenes (sin información sensible).
    
    Incluir solo: id, order_date, status, total_amount, product_count
    """
    # Tu código aquí
    pass

# Tests
if __name__ == "__main__":
    # Test Product
    try:
        product_data = {
            "id": 1,
            "name": "laptop gaming",
            "description": "Laptop para gaming de alta gama",
            "price": 1299.99,
            "category": "electronics",
            "tags": ["gaming", "laptop", "high-end"]
        }
        product = Product(**product_data)
        print("Producto creado:", product.json(indent=2))
    except Exception as e:
        print("Error creando producto:", e)
    
    # Test Order
    try:
        order_data = {
            "id": 1,
            "customer_email": "cliente@email.com",
            "products": [product_data],
            "status": "pending"
        }
        order = Order(**order_data)
        print("Orden creada:", order.json(indent=2))
        
        # Test OrderResponse
        response = OrderResponse(**order.dict())
        print("Respuesta de orden:", response.json(indent=2))
    except Exception as e:
        print("Error creando orden:", e)
