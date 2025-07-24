# Práctica 9: Manejo de Errores Profesional - Semana 3

## 🎯 Objetivo

Implementar un sistema robusto y profesional de manejo de errores en FastAPI, incluyendo custom exception handlers, logging, y responses consistentes.

## ⏱️ Tiempo Estimado: 90 minutos

## 📋 Pre-requisitos

- ✅ API con validación avanzada (Práctica 8)
- ✅ Comprensión de HTTPException básico
- ✅ Familiaridad con conceptos de logging

## 🛠️ Paso 1: Sistema de Excepciones Custom (25 min)

### **Crear Excepciones Personalizadas**

Crear `exceptions/custom_exceptions.py`:

```python
from fastapi import HTTPException, status
from typing import Optional, Dict, Any
from datetime import datetime

class BaseAPIException(Exception):
    """Excepción base para todas las excepciones de la API"""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        self.timestamp = datetime.now()
        super().__init__(self.message)

class ValidationError(BaseAPIException):
    """Errores de validación de datos"""

    def __init__(
        self,
        message: str = "Error de validación",
        field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        error_details = details or {}
        if field:
            error_details["field"] = field

        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code="VALIDATION_ERROR",
            details=error_details
        )

class ResourceNotFoundError(BaseAPIException):
    """Recurso no encontrado"""

    def __init__(
        self,
        resource_type: str = "Resource",
        resource_id: Any = None,
        message: Optional[str] = None
    ):
        if not message:
            if resource_id:
                message = f"{resource_type} con ID '{resource_id}' no encontrado"
            else:
                message = f"{resource_type} no encontrado"

        details = {
            "resource_type": resource_type,
            "resource_id": resource_id
        }

        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="RESOURCE_NOT_FOUND",
            details=details
        )

class ConflictError(BaseAPIException):
    """Conflicto en el estado de la aplicación"""

    def __init__(
        self,
        message: str = "Conflicto en la operación",
        conflict_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        error_details = details or {}
        if conflict_type:
            error_details["conflict_type"] = conflict_type

        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            error_code="CONFLICT_ERROR",
            details=error_details
        )

class BusinessLogicError(BaseAPIException):
    """Errores de lógica de negocio"""

    def __init__(
        self,
        message: str,
        rule: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        error_details = details or {}
        if rule:
            error_details["business_rule"] = rule

        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="BUSINESS_LOGIC_ERROR",
            details=error_details
        )

class AuthenticationError(BaseAPIException):
    """Errores de autenticación"""

    def __init__(
        self,
        message: str = "Credenciales inválidas o ausentes",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="AUTHENTICATION_ERROR",
            details=details or {}
        )

class AuthorizationError(BaseAPIException):
    """Errores de autorización"""

    def __init__(
        self,
        message: str = "No tienes permisos para realizar esta acción",
        required_permission: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        error_details = details or {}
        if required_permission:
            error_details["required_permission"] = required_permission

        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="AUTHORIZATION_ERROR",
            details=error_details
        )

class ExternalServiceError(BaseAPIException):
    """Errores relacionados con servicios externos"""

    def __init__(
        self,
        message: str = "Error en servicio externo",
        service_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        error_details = details or {}
        if service_name:
            error_details["service_name"] = service_name

        super().__init__(
            message=message,
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            error_code="EXTERNAL_SERVICE_ERROR",
            details=error_details
        )

class RateLimitError(BaseAPIException):
    """Errores de límite de tasa"""

    def __init__(
        self,
        message: str = "Límite de tasa excedido",
        retry_after: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        error_details = details or {}
        if retry_after:
            error_details["retry_after_seconds"] = retry_after

        super().__init__(
            message=message,
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_ERROR",
            details=error_details
        )
```

### **Modelos de Response de Error**

Crear `models/error_models.py`:

```python
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class ErrorDetail(BaseModel):
    field: Optional[str] = Field(None, description="Campo que causó el error")
    message: str = Field(..., description="Mensaje del error específico")
    code: Optional[str] = Field(None, description="Código del error específico")

class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Indica si la operación fue exitosa")
    error_code: str = Field(..., description="Código único del error")
    message: str = Field(..., description="Mensaje principal del error")
    details: Optional[Dict[str, Any]] = Field(None, description="Detalles adicionales del error")
    timestamp: datetime = Field(..., description="Momento en que ocurrió el error")
    path: Optional[str] = Field(None, description="Endpoint donde ocurrió el error")
    method: Optional[str] = Field(None, description="Método HTTP utilizado")

    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error_code": "RESOURCE_NOT_FOUND",
                "message": "Producto con ID '123' no encontrado",
                "details": {
                    "resource_type": "Product",
                    "resource_id": 123
                },
                "timestamp": "2025-07-24T10:30:00.123456",
                "path": "/products/123",
                "method": "GET"
            }
        }

class ValidationErrorResponse(BaseModel):
    success: bool = Field(False, description="Indica si la operación fue exitosa")
    error_code: str = Field("VALIDATION_ERROR", description="Código del error de validación")
    message: str = Field(..., description="Mensaje principal del error")
    validation_errors: List[ErrorDetail] = Field(..., description="Lista de errores de validación")
    timestamp: datetime = Field(..., description="Momento en que ocurrió el error")
    path: Optional[str] = Field(None, description="Endpoint donde ocurrió el error")
    method: Optional[str] = Field(None, description="Método HTTP utilizado")

    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "error_code": "VALIDATION_ERROR",
                "message": "Error en la validación de datos",
                "validation_errors": [
                    {
                        "field": "price",
                        "message": "El precio debe ser mayor a 0",
                        "code": "value_error.number.not_gt"
                    },
                    {
                        "field": "sku",
                        "message": "SKU debe tener formato CAT-BRAND-XXXX",
                        "code": "value_error.str.regex"
                    }
                ],
                "timestamp": "2025-07-24T10:30:00.123456",
                "path": "/products",
                "method": "POST"
            }
        }

class SuccessResponse(BaseModel):
    success: bool = Field(True, description="Indica si la operación fue exitosa")
    message: str = Field(..., description="Mensaje de éxito")
    data: Optional[Any] = Field(None, description="Datos de respuesta")
    timestamp: datetime = Field(default_factory=datetime.now, description="Momento de la respuesta")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Operación completada exitosamente",
                "data": {"id": 123, "name": "Producto ejemplo"},
                "timestamp": "2025-07-24T10:30:00.123456"
            }
        }
```

## 🔧 Paso 2: Exception Handlers Globales (25 min)

### **Configurar Handlers de Excepciones**

Crear `handlers/exception_handlers.py`:

```python
import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from exceptions.custom_exceptions import BaseAPIException
from models.error_models import ErrorResponse, ValidationErrorResponse, ErrorDetail

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_exception_handlers(app):
    """Configurar todos los manejadores de excepciones"""

    @app.exception_handler(BaseAPIException)
    async def custom_exception_handler(request: Request, exc: BaseAPIException):
        """Manejador para excepciones personalizadas"""

        # Log del error
        logger.error(
            f"Custom Exception: {exc.error_code} - {exc.message} - "
            f"Path: {request.url.path} - Method: {request.method}",
            extra={
                "error_code": exc.error_code,
                "details": exc.details,
                "path": str(request.url.path),
                "method": request.method
            }
        )

        error_response = ErrorResponse(
            error_code=exc.error_code,
            message=exc.message,
            details=exc.details,
            timestamp=exc.timestamp,
            path=str(request.url.path),
            method=request.method
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.dict()
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        """Manejador para errores de validación de FastAPI/Pydantic"""

        # Procesar errores de validación
        validation_errors = []
        for error in exc.errors():
            field_path = " -> ".join(str(loc) for loc in error["loc"])
            validation_errors.append(ErrorDetail(
                field=field_path,
                message=error["msg"],
                code=error["type"]
            ))

        # Log del error
        logger.warning(
            f"Validation Error - Path: {request.url.path} - Method: {request.method} - "
            f"Errors: {len(validation_errors)}",
            extra={
                "validation_errors": [err.dict() for err in validation_errors],
                "path": str(request.url.path),
                "method": request.method
            }
        )

        error_response = ValidationErrorResponse(
            message="Error en la validación de datos de entrada",
            validation_errors=validation_errors,
            timestamp=datetime.now(),
            path=str(request.url.path),
            method=request.method
        )

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response.dict()
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        """Manejador para HTTPException estándar"""

        # Log del error
        logger.warning(
            f"HTTP Exception: {exc.status_code} - {exc.detail} - "
            f"Path: {request.url.path} - Method: {request.method}",
            extra={
                "status_code": exc.status_code,
                "detail": exc.detail,
                "path": str(request.url.path),
                "method": request.method
            }
        )

        error_response = ErrorResponse(
            error_code=f"HTTP_{exc.status_code}",
            message=exc.detail,
            details={"status_code": exc.status_code},
            timestamp=datetime.now(),
            path=str(request.url.path),
            method=request.method
        )

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response.dict()
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Manejador para excepciones no controladas"""

        # Log del error con stack trace
        logger.critical(
            f"Unhandled Exception: {type(exc).__name__} - {str(exc)} - "
            f"Path: {request.url.path} - Method: {request.method}",
            exc_info=True,
            extra={
                "exception_type": type(exc).__name__,
                "path": str(request.url.path),
                "method": request.method
            }
        )

        # En producción, no exponer detalles internos
        error_response = ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message="Error interno del servidor. Por favor, contacta al administrador.",
            details={
                "error_id": f"ERR_{int(datetime.now().timestamp())}"
            },
            timestamp=datetime.now(),
            path=str(request.url.path),
            method=request.method
        )

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response.dict()
        )

# Decorador para manejo automático de errores en endpoints
def handle_errors(func):
    """Decorador para manejo automático de errores en funciones"""
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except BaseAPIException:
            # Las excepciones custom se propagan para ser manejadas por el handler
            raise
        except Exception as e:
            # Convertir excepciones generales en excepciones custom
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}", exc_info=True)
            raise BaseAPIException(
                message="Error interno en el procesamiento",
                error_code="PROCESSING_ERROR",
                details={"function": func.__name__}
            )
    return wrapper
```

## 🔍 Paso 3: Implementar Logging Avanzado (20 min)

### **Sistema de Logging Robusto**

Crear `utils/logging_config.py`:

```python
import logging
import logging.handlers
import json
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

class JSONFormatter(logging.Formatter):
    """Formatter para logs en formato JSON"""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }

        # Agregar información adicional si está disponible
        if hasattr(record, 'path'):
            log_entry["path"] = record.path

        if hasattr(record, 'method'):
            log_entry["method"] = record.method

        if hasattr(record, 'error_code'):
            log_entry["error_code"] = record.error_code

        if hasattr(record, 'details'):
            log_entry["details"] = record.details

        # Agregar stack trace para errores
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_entry, ensure_ascii=False)

def setup_logging():
    """Configurar el sistema de logging"""

    # Crear directorio de logs si no existe
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configuración del logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Limpiar handlers existentes
    root_logger.handlers.clear()

    # Handler para consola (desarrollo)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Handler para archivo de logs generales
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / "api.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(file_handler)

    # Handler para errores críticos
    error_handler = logging.handlers.RotatingFileHandler(
        log_dir / "errors.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(JSONFormatter())
    root_logger.addHandler(error_handler)

    # Logger específico para la aplicación
    app_logger = logging.getLogger("fastapi_app")
    app_logger.setLevel(logging.INFO)

    return app_logger

# Función para log estructurado
def log_api_call(
    logger: logging.Logger,
    method: str,
    path: str,
    status_code: int,
    duration: float,
    user_id: str = None,
    additional_data: Dict[str, Any] = None
):
    """Log estructurado para llamadas a la API"""

    extra_data = {
        "method": method,
        "path": path,
        "status_code": status_code,
        "duration_ms": round(duration * 1000, 2),
        "type": "api_call"
    }

    if user_id:
        extra_data["user_id"] = user_id

    if additional_data:
        extra_data.update(additional_data)

    level = logging.ERROR if status_code >= 500 else logging.WARNING if status_code >= 400 else logging.INFO

    logger.log(
        level,
        f"{method} {path} - {status_code} - {duration*1000:.2f}ms",
        extra=extra_data
    )

# Middleware para logging automático
class LoggingMiddleware:
    def __init__(self, app, logger):
        self.app = app
        self.logger = logger

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        start_time = datetime.now()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                log_api_call(
                    self.logger,
                    method=scope["method"],
                    path=scope["path"],
                    status_code=message["status"],
                    duration=duration
                )

            await send(message)

        await self.app(scope, receive, send_wrapper)
```

## 🔧 Paso 4: Actualizar API con Manejo de Errores (20 min)

### **Integrar Sistema de Errores en main.py**

```python
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime
import time

# Imports del sistema de errores
from handlers.exception_handlers import setup_exception_handlers, handle_errors
from utils.logging_config import setup_logging, LoggingMiddleware
from exceptions.custom_exceptions import (
    ResourceNotFoundError, ConflictError, BusinessLogicError,
    ValidationError, ExternalServiceError
)
from models.error_models import ErrorResponse, SuccessResponse

# Configurar logging
logger = setup_logging()

app = FastAPI(
    title="API de Inventario - Sistema de Errores Robusto",
    description="API con manejo profesional de errores y logging",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar exception handlers
setup_exception_handlers(app)

# Configurar middleware de logging
app.add_middleware(LoggingMiddleware, logger=logger)

# Ejemplos de endpoints con manejo de errores robusto

@app.get(
    "/products/{product_id}",
    response_model=ProductResponseValidated,
    responses={
        404: {"model": ErrorResponse, "description": "Producto no encontrado"},
        500: {"model": ErrorResponse, "description": "Error interno del servidor"}
    }
)
@handle_errors
async def get_product_with_error_handling(product_id: int):
    """Obtener producto con manejo robusto de errores"""

    # Validar entrada
    if product_id <= 0:
        raise ValidationError(
            message="El ID del producto debe ser un número positivo",
            field="product_id",
            details={"provided_value": product_id}
        )

    # Buscar producto
    product = get_product_by_id(product_id)

    if not product:
        raise ResourceNotFoundError(
            resource_type="Producto",
            resource_id=product_id
        )

    # Simular verificación de servicio externo
    if product.get("requires_external_check", False):
        # Simular falla de servicio externo
        import random
        if random.random() < 0.1:  # 10% chance de falla
            raise ExternalServiceError(
                message="Servicio de verificación de productos no disponible",
                service_name="product_verification_service",
                details={"retry_recommended": True}
            )

    logger.info(f"Producto {product_id} obtenido exitosamente")
    return ProductResponseValidated(**product)

@app.post(
    "/products",
    response_model=ProductResponseValidated,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"model": ErrorResponse, "description": "Conflicto - Producto ya existe"},
        422: {"model": ValidationErrorResponse, "description": "Error de validación"},
        400: {"model": ErrorResponse, "description": "Error de lógica de negocio"}
    }
)
@handle_errors
async def create_product_with_error_handling(product: ProductCreateValidated):
    """Crear producto con validación de negocio robusta"""

    existing_products = get_all_products()

    # Verificar SKU único
    for existing in existing_products:
        if existing.get("sku") == product.sku:
            raise ConflictError(
                message=f"Ya existe un producto con SKU '{product.sku}'",
                conflict_type="sku_duplicate",
                details={
                    "existing_product_id": existing.get("id"),
                    "existing_product_name": existing.get("name")
                }
            )

    # Verificar nombre único
    for existing in existing_products:
        if existing.get("name", "").lower() == product.name.lower():
            raise ConflictError(
                message=f"Ya existe un producto con el nombre '{product.name}'",
                conflict_type="name_duplicate",
                details={
                    "existing_product_id": existing.get("id"),
                    "suggestion": "Usa un nombre diferente o agrega un sufijo distintivo"
                }
            )

    # Validar lógica de negocio
    if product.price > 10000 and product.stock_quantity > 100:
        raise BusinessLogicError(
            message="Productos de alto valor no pueden tener stock masivo sin aprobación",
            rule="high_value_stock_limit",
            details={
                "max_allowed_stock": 100,
                "price_threshold": 10000,
                "approval_required": True
            }
        )

    # Crear producto
    try:
        product_data = product.dict()
        new_product = create_product(product_data)

        logger.info(
            f"Producto creado exitosamente: {new_product['id']} - {new_product['name']}",
            extra={
                "product_id": new_product["id"],
                "product_sku": new_product["sku"],
                "action": "product_created"
            }
        )

        return ProductResponseValidated(**new_product)

    except Exception as e:
        logger.error(f"Error inesperado al crear producto: {str(e)}", exc_info=True)
        raise BaseAPIException(
            message="Error interno al crear el producto",
            error_code="PRODUCT_CREATION_ERROR",
            details={"original_error": str(e)}
        )

@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        404: {"model": ErrorResponse, "description": "Producto no encontrado"},
        400: {"model": ErrorResponse, "description": "No se puede eliminar el producto"}
    }
)
@handle_errors
async def delete_product_with_validation(product_id: int):
    """Eliminar producto con validaciones de negocio"""

    # Verificar que existe
    product = get_product_by_id(product_id)
    if not product:
        raise ResourceNotFoundError(
            resource_type="Producto",
            resource_id=product_id
        )

    # Validar si se puede eliminar
    if product.get("is_featured", False):
        raise BusinessLogicError(
            message="No se pueden eliminar productos destacados",
            rule="featured_product_protection",
            details={
                "product_name": product.get("name"),
                "action_required": "Remover el estado 'destacado' antes de eliminar"
            }
        )

    if product.get("has_active_orders", False):
        raise BusinessLogicError(
            message="No se puede eliminar producto con órdenes activas",
            rule="active_orders_protection",
            details={
                "active_orders_count": product.get("active_orders_count", 0)
            }
        )

    # Eliminar producto
    deleted = delete_product(product_id)
    if not deleted:
        raise BaseAPIException(
            message="Error al eliminar el producto",
            error_code="DELETE_OPERATION_FAILED",
            details={"product_id": product_id}
        )

    logger.info(
        f"Producto eliminado: {product_id} - {product.get('name')}",
        extra={
            "product_id": product_id,
            "action": "product_deleted"
        }
    )

    return None

# Endpoint para testing de errores
@app.get("/test-errors/{error_type}")
async def test_error_handling(error_type: str):
    """Endpoint para probar diferentes tipos de errores"""

    if error_type == "validation":
        raise ValidationError("Error de validación de prueba", field="test_field")

    elif error_type == "not_found":
        raise ResourceNotFoundError("TestResource", 999)

    elif error_type == "conflict":
        raise ConflictError("Conflicto de prueba", conflict_type="test_conflict")

    elif error_type == "business":
        raise BusinessLogicError("Regla de negocio violada", rule="test_rule")

    elif error_type == "external":
        raise ExternalServiceError("Servicio externo falló", service_name="test_service")

    elif error_type == "server":
        raise Exception("Error interno simulado")

    else:
        return {"message": "Tipos disponibles: validation, not_found, conflict, business, external, server"}
```

## 🧪 Paso 5: Testing del Sistema de Errores (15 min)

### **Comandos de Testing**

```bash
# 1. Test de producto no encontrado
curl -X GET "http://localhost:8000/products/999"

# 2. Test de validación (ID inválido)
curl -X GET "http://localhost:8000/products/-1"

# 3. Test de conflicto (SKU duplicado)
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Producto Test",
    "price": 99.99,
    "sku": "ELE-APPLE-I15P",
    "description": "Producto de prueba con SKU duplicado",
    "category": "electronics",
    "brand": "apple",
    "in_stock": true,
    "stock_quantity": 10
  }'

# 4. Test de lógica de negocio (precio alto + stock alto)
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Producto Caro",
    "price": 15000.00,
    "sku": "ELE-APPLE-EXPE",
    "description": "Producto muy caro con mucho stock",
    "category": "electronics",
    "brand": "apple",
    "in_stock": true,
    "stock_quantity": 200
  }'

# 5. Test de diferentes tipos de errores
curl -X GET "http://localhost:8000/test-errors/validation"
curl -X GET "http://localhost:8000/test-errors/not_found"
curl -X GET "http://localhost:8000/test-errors/conflict"
curl -X GET "http://localhost:8000/test-errors/business"
curl -X GET "http://localhost:8000/test-errors/external"
curl -X GET "http://localhost:8000/test-errors/server"
```

## ✅ Entregables

Al finalizar esta práctica deberías tener:

1. ✅ **Sistema de excepciones custom** completo
2. ✅ **Exception handlers globales** configurados
3. ✅ **Logging avanzado** con formato JSON
4. ✅ **Responses de error** consistentes y detallados
5. ✅ **Validaciones de lógica de negocio** implementadas
6. ✅ **Testing exhaustivo** de diferentes tipos de errores

## 🎯 Próximo Paso

En la siguiente práctica (10-estructura-rest.md) organizaremos todo el código en una estructura profesional y escalable siguiendo las mejores prácticas de arquitectura REST.

---

_Práctica desarrollada para Semana 3 - Bootcamp FastAPI_  
_Tiempo estimado: 90 minutos_
