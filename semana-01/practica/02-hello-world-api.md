# Práctica 2: Tu Primera API FastAPI con Calidad Profesional

## 🎯 Objetivo

Crear una API "Hello World" que demuestre mejores prácticas desde la primera línea de código, estableciendo el estándar de calidad para todo el bootcamp.

## ⏱️ Tiempo Estimado: 90 minutos

## 📋 Pre-requisitos

- ✅ Entorno de desarrollo configurado (Práctica 1)
- ✅ Python 3.11+ y FastAPI instalados
- ✅ Entorno virtual activado

## 🏗️ Arquitectura del "Hello World API"

![API Architecture](./hello-world-api-diagram.svg)

Esta no será una API básica. Implementaremos:

- ✅ Estructura profesional desde día 1
- ✅ Validación de datos con Pydantic
- ✅ Documentación automática completa
- ✅ Manejo de errores robusto
- ✅ Testing básico
- ✅ Type hints en todo el código

## 🚀 Paso 1: Estructura del Proyecto

### Crear la estructura base

```bash
# Asegúrate de estar en tu proyecto y entorno virtual activo
cd fastapi-bootcamp-w1
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Crear estructura específica para la API
mkdir -p src/api/{routes,models,schemas,core,utils}
mkdir -p tests/{unit,integration}

# Crear archivos Python iniciales
touch src/__init__.py
touch src/api/__init__.py
touch src/api/{routes,models,schemas,core,utils}/__init__.py
touch tests/{__init__.py,conftest.py}
```

### Verificar estructura

```bash
tree src tests -I "__pycache__"
# Debe mostrar:
# src/
# ├── __init__.py
# └── api/
#     ├── __init__.py
#     ├── core/
#     ├── models/
#     ├── routes/
#     ├── schemas/
#     └── utils/
# tests/
# ├── __init__.py
# ├── conftest.py
# ├── integration/
# └── unit/
```

## 🔧 Paso 2: Configuración Central

### src/api/core/config.py

```python
"""
Application configuration management.
Centralizes all configuration using environment variables with sensible defaults.
"""
from typing import List
from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings with validation."""

    # Application
    app_name: str = "FastAPI Bootcamp - Week 1"
    app_version: str = "1.0.0"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # API
    api_v1_prefix: str = "/api/v1"
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"

    # CORS
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    allowed_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allowed_headers: List[str] = ["*"]

    @validator("allowed_origins", pre=True)
    def parse_cors_origins(cls, value):
        """Parse CORS origins from string or list."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",")]
        return value

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
```

### src/api/core/exceptions.py

```python
"""
Custom exceptions for the application.
Provides structured error handling with meaningful messages.
"""
from typing import Any, Dict, Optional


class APIException(Exception):
    """Base exception for API errors."""

    def __init__(
        self,
        message: str,
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(APIException):
    """Exception raised when data validation fails."""

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message, status_code=422, details=details)


class NotFoundException(APIException):
    """Exception raised when a resource is not found."""

    def __init__(self, resource: str, identifier: str) -> None:
        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(message, status_code=404)
```

## 📊 Paso 3: Modelos de Datos con Pydantic

### src/api/schemas/base.py

```python
"""
Base schemas for API requests and responses.
Provides common patterns and utilities for data validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """Base schema with common configuration."""

    class Config:
        # Allow field population by name or alias
        allow_population_by_field_name = True
        # Validate all fields on assignment
        validate_assignment = True
        # Use enum values instead of names
        use_enum_values = True


class TimestampSchema(BaseSchema):
    """Schema for models with timestamp fields."""

    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")


class ResponseBase(BaseSchema):
    """Base response schema with metadata."""

    success: bool = Field(True, description="Operation success status")
    message: str = Field("Operation completed successfully", description="Response message")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Response timestamp")
```

### src/api/schemas/health.py

```python
"""
Health check schemas for API monitoring.
"""
from typing import Dict, Any
from pydantic import Field
from .base import ResponseBase


class HealthResponse(ResponseBase):
    """Health check response schema."""

    status: str = Field("healthy", description="Service health status")
    version: str = Field("1.0.0", description="API version")
    uptime: str = Field(..., description="Service uptime")
    dependencies: Dict[str, Any] = Field(default_factory=dict, description="Dependency status")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Service is healthy",
                "timestamp": "2024-01-01T12:00:00Z",
                "status": "healthy",
                "version": "1.0.0",
                "uptime": "0:05:30",
                "dependencies": {
                    "database": "connected",
                    "cache": "connected"
                }
            }
        }
```

### src/api/schemas/greetings.py

```python
"""
Greeting-related schemas for the Hello World API.
"""
from typing import Optional
from pydantic import Field, validator
from .base import ResponseBase, TimestampSchema


class GreetingRequest(BaseModel):
    """Request schema for personalized greetings."""

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name for personalized greeting",
        example="Alice"
    )
    language: Optional[str] = Field(
        "en",
        description="Language code for greeting",
        example="en"
    )
    formal: bool = Field(
        False,
        description="Whether to use formal greeting",
        example=False
    )

    @validator("name")
    def validate_name(cls, value: str) -> str:
        """Validate and sanitize name input."""
        # Remove extra whitespace and ensure proper capitalization
        name = value.strip().title()

        # Basic validation - only letters, spaces, hyphens, apostrophes
        if not all(char.isalpha() or char in " -'" for char in name):
            raise ValueError("Name must contain only letters, spaces, hyphens, and apostrophes")

        return name

    @validator("language")
    def validate_language(cls, value: str) -> str:
        """Validate language code."""
        if value:
            value = value.lower().strip()
            supported_languages = ["en", "es", "fr", "de"]
            if value not in supported_languages:
                raise ValueError(f"Language must be one of: {', '.join(supported_languages)}")
        return value or "en"


class GreetingResponse(ResponseBase):
    """Response schema for greeting endpoints."""

    greeting: str = Field(..., description="Generated greeting message")
    name: str = Field(..., description="Name used in greeting")
    language: str = Field(..., description="Language used")
    formal: bool = Field(..., description="Whether formal greeting was used")

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "Greeting generated successfully",
                "timestamp": "2024-01-01T12:00:00Z",
                "greeting": "Hello, Alice! Welcome to FastAPI Bootcamp!",
                "name": "Alice",
                "language": "en",
                "formal": False
            }
        }


class GreetingHistory(TimestampSchema):
    """Schema for greeting history records."""

    id: int = Field(..., description="Unique greeting ID")
    greeting: str = Field(..., description="The greeting message")
    name: str = Field(..., description="Name used in greeting")
    language: str = Field(..., description="Language used")
    formal: bool = Field(..., description="Whether formal greeting was used")
    ip_address: Optional[str] = Field(None, description="Client IP address")
```

## 🛠️ Paso 4: Lógica de Negocio

### src/api/utils/greetings.py

```python
"""
Greeting generation utilities.
Business logic for creating personalized greetings.
"""
from typing import Dict
from datetime import datetime


class GreetingGenerator:
    """Generates personalized greetings in multiple languages."""

    # Greeting templates by language and formality
    GREETINGS: Dict[str, Dict[str, list]] = {
        "en": {
            "informal": [
                "Hello, {name}! Welcome to FastAPI Bootcamp!",
                "Hi {name}! Great to see you here!",
                "Hey {name}! Ready to learn FastAPI?",
                "Welcome {name}! Let's build amazing APIs together!"
            ],
            "formal": [
                "Good day, {name}. Welcome to the FastAPI Bootcamp.",
                "Greetings, {name}. We are pleased to have you here.",
                "Welcome, {name}. Thank you for joining our program."
            ]
        },
        "es": {
            "informal": [
                "¡Hola, {name}! ¡Bienvenido al Bootcamp de FastAPI!",
                "¡Hola {name}! ¡Qué bueno verte aquí!",
                "¡Hey {name}! ¿Listo para aprender FastAPI?"
            ],
            "formal": [
                "Buenos días, {name}. Bienvenido al Bootcamp de FastAPI.",
                "Saludos, {name}. Nos complace tenerlo aquí."
            ]
        },
        "fr": {
            "informal": [
                "Salut {name}! Bienvenue au Bootcamp FastAPI!",
                "Bonjour {name}! Ravi de te voir ici!"
            ],
            "formal": [
                "Bonjour, {name}. Bienvenue au Bootcamp FastAPI.",
                "Salutations, {name}. Nous sommes ravis de vous accueillir."
            ]
        },
        "de": {
            "informal": [
                "Hallo {name}! Willkommen beim FastAPI Bootcamp!",
                "Hi {name}! Schön dich hier zu sehen!"
            ],
            "formal": [
                "Guten Tag, {name}. Willkommen beim FastAPI Bootcamp.",
                "Grüße, {name}. Wir freuen uns, Sie hier zu haben."
            ]
        }
    }

    @classmethod
    def generate_greeting(
        cls,
        name: str,
        language: str = "en",
        formal: bool = False
    ) -> str:
        """
        Generate a personalized greeting.

        Args:
            name: Person's name
            language: Language code (en, es, fr, de)
            formal: Whether to use formal greeting

        Returns:
            Personalized greeting message
        """
        # Get language greetings or fallback to English
        lang_greetings = cls.GREETINGS.get(language, cls.GREETINGS["en"])

        # Get formality level greetings
        formality = "formal" if formal else "informal"
        greetings = lang_greetings.get(formality, lang_greetings["informal"])

        # Select greeting based on current time (pseudo-random)
        greeting_index = datetime.now().second % len(greetings)
        greeting_template = greetings[greeting_index]

        # Format with name
        return greeting_template.format(name=name)

    @classmethod
    def get_supported_languages(cls) -> list:
        """Get list of supported language codes."""
        return list(cls.GREETINGS.keys())

    @classmethod
    def is_language_supported(cls, language: str) -> bool:
        """Check if a language is supported."""
        return language in cls.GREETINGS
```

## 🎯 Paso 5: Rutas de la API

### src/api/routes/health.py

```python
"""
Health check endpoints for API monitoring.
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, status
from ..schemas.health import HealthResponse
from ..core.config import settings

# Router for health-related endpoints
router = APIRouter(
    prefix="/health",
    tags=["Health Check"],
    responses={
        500: {"description": "Internal server error"},
    }
)

# Store startup time for uptime calculation
startup_time = datetime.utcnow()


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API service is healthy and running properly.",
    response_description="Service health status with uptime and dependencies"
)
async def health_check() -> HealthResponse:
    """
    Comprehensive health check endpoint.

    Returns detailed information about service status, uptime, and dependencies.
    This endpoint should be used by load balancers and monitoring systems.
    """
    current_time = datetime.utcnow()
    uptime = current_time - startup_time

    # Format uptime as human-readable string
    total_seconds = int(uptime.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}:{minutes:02d}:{seconds:02d}"

    # Check dependencies (placeholder for future database/cache checks)
    dependencies = {
        "python": "✓ 3.11+",
        "fastapi": "✓ running",
        "pydantic": "✓ validation active"
    }

    return HealthResponse(
        success=True,
        message="Service is healthy and running optimally",
        status="healthy",
        version=settings.app_version,
        uptime=uptime_str,
        dependencies=dependencies
    )


@router.get(
    "/simple",
    status_code=status.HTTP_200_OK,
    summary="Simple Health Check",
    description="Lightweight health check for basic monitoring.",
    response_model=dict
)
async def simple_health_check() -> dict:
    """
    Simple health check endpoint.

    Returns minimal response for basic monitoring needs.
    Lower overhead than the detailed health check.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
```

### src/api/routes/greetings.py

```python
"""
Greeting endpoints - the heart of our Hello World API.
"""
from typing import List
from fastapi import APIRouter, status, HTTPException, Request
from ..schemas.greetings import GreetingRequest, GreetingResponse, GreetingHistory
from ..utils.greetings import GreetingGenerator
from ..core.exceptions import ValidationException

# Router for greeting-related endpoints
router = APIRouter(
    prefix="/greetings",
    tags=["Greetings"],
    responses={
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    }
)

# In-memory storage for demonstration (will be replaced with database later)
greeting_history: List[dict] = []
greeting_counter = 0


@router.get(
    "/hello",
    response_model=GreetingResponse,
    status_code=status.HTTP_200_OK,
    summary="Basic Hello World",
    description="Returns a simple hello world greeting.",
    response_description="Basic greeting message"
)
async def hello_world() -> GreetingResponse:
    """
    Basic Hello World endpoint.

    Returns a simple greeting message without personalization.
    Perfect for testing API connectivity and basic functionality.
    """
    greeting = "Hello, World! Welcome to FastAPI Bootcamp!"

    return GreetingResponse(
        success=True,
        message="Basic greeting generated",
        greeting=greeting,
        name="World",
        language="en",
        formal=False
    )


@router.post(
    "/personalized",
    response_model=GreetingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Personalized Greeting",
    description="Generate a personalized greeting with custom options.",
    response_description="Personalized greeting with specified options"
)
async def create_personalized_greeting(
    greeting_request: GreetingRequest,
    request: Request
) -> GreetingResponse:
    """
    Create a personalized greeting.

    Generates a custom greeting based on the provided name, language preference,
    and formality level. The greeting is stored in history for analytics.

    Args:
        greeting_request: Greeting parameters (name, language, formality)
        request: HTTP request object for IP address extraction

    Returns:
        Personalized greeting response with metadata

    Raises:
        ValidationException: If the provided data is invalid
        HTTPException: If greeting generation fails
    """
    global greeting_counter

    try:
        # Generate the personalized greeting
        greeting = GreetingGenerator.generate_greeting(
            name=greeting_request.name,
            language=greeting_request.language,
            formal=greeting_request.formal
        )

        # Increment counter and store in history
        greeting_counter += 1

        # Extract client IP (handle proxy headers in production)
        client_ip = request.client.host if request.client else "unknown"

        # Store in history (in-memory for now)
        history_entry = {
            "id": greeting_counter,
            "greeting": greeting,
            "name": greeting_request.name,
            "language": greeting_request.language,
            "formal": greeting_request.formal,
            "ip_address": client_ip,
            "created_at": datetime.utcnow()
        }
        greeting_history.append(history_entry)

        return GreetingResponse(
            success=True,
            message=f"Personalized greeting created for {greeting_request.name}",
            greeting=greeting,
            name=greeting_request.name,
            language=greeting_request.language,
            formal=greeting_request.formal
        )

    except ValueError as e:
        # Handle validation errors from GreetingGenerator
        raise ValidationException(str(e))
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate greeting: {str(e)}"
        )


@router.get(
    "/history",
    response_model=List[GreetingHistory],
    status_code=status.HTTP_200_OK,
    summary="Greeting History",
    description="Retrieve history of all generated greetings.",
    response_description="List of greeting history records"
)
async def get_greeting_history() -> List[GreetingHistory]:
    """
    Get greeting history.

    Returns a list of all greetings that have been generated,
    useful for analytics and debugging.

    Returns:
        List of greeting history records
    """
    return [
        GreetingHistory(**entry) for entry in greeting_history
    ]


@router.get(
    "/languages",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Supported Languages",
    description="Get list of supported languages for greetings.",
    response_description="List of supported language codes and names"
)
async def get_supported_languages() -> dict:
    """
    Get supported languages.

    Returns information about all languages supported by the greeting system.
    Useful for client applications to build language selection UIs.

    Returns:
        Dictionary with supported languages and their details
    """
    languages = {
        "en": {"name": "English", "sample": "Hello, World!"},
        "es": {"name": "Spanish", "sample": "¡Hola, Mundo!"},
        "fr": {"name": "French", "sample": "Bonjour, le Monde!"},
        "de": {"name": "German", "sample": "Hallo, Welt!"}
    }

    return {
        "success": True,
        "message": "Supported languages retrieved",
        "count": len(languages),
        "languages": languages
    }
```

## 🎯 Paso 6: Aplicación Principal

### src/main.py

```python
"""
FastAPI Bootcamp Week 1 - Main Application
A professional Hello World API demonstrating best practices from day one.
"""
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from datetime import datetime

from api.core.config import settings
from api.core.exceptions import APIException, ValidationException
from api.routes import health, greetings

# Create FastAPI application with comprehensive metadata
app = FastAPI(
    title=settings.app_name,
    description="""
    **FastAPI Bootcamp Week 1 - Professional Hello World API**

    This API demonstrates professional development practices from day one:

    * **Clean Architecture**: Proper separation of concerns
    * **Comprehensive Validation**: Input validation with Pydantic
    * **Error Handling**: Structured error responses
    * **Documentation**: Auto-generated OpenAPI docs
    * **Type Safety**: Full type hints throughout
    * **Testing Ready**: Built with testability in mind

    Perfect for learning FastAPI fundamentals with industry best practices.
    """,
    version=settings.app_version,
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    contact={
        "name": "FastAPI Bootcamp Team",
        "email": "bootcamp@fastapi-example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    tags_metadata=[
        {
            "name": "Health Check",
            "description": "Endpoints for monitoring API health and status."
        },
        {
            "name": "Greetings",
            "description": "Core greeting functionality with personalization options."
        }
    ]
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)


# Exception handlers for professional error responses
@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """Handle custom API exceptions with structured responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details,
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url.path)
            }
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors with detailed information."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "type": "ValidationError",
                "message": "Request validation failed",
                "details": {
                    "errors": exc.errors(),
                    "body": exc.body
                },
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url.path)
            }
        }
    )


@app.exception_handler(500)
async def internal_server_error_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected server errors gracefully."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "type": "InternalServerError",
                "message": "An unexpected error occurred",
                "timestamp": datetime.utcnow().isoformat(),
                "path": str(request.url.path)
            }
        }
    )


# Include routers with API versioning
app.include_router(
    health.router,
    prefix=settings.api_v1_prefix
)

app.include_router(
    greetings.router,
    prefix=settings.api_v1_prefix
)


# Root endpoint with API information
@app.get(
    "/",
    tags=["Root"],
    summary="API Information",
    description="Get basic information about the API."
)
async def root() -> dict:
    """
    API root endpoint.

    Provides basic information about the API including version,
    documentation links, and available endpoints.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Professional Hello World API with FastAPI",
        "docs_url": settings.docs_url,
        "redoc_url": settings.redoc_url,
        "health_check": f"{settings.api_v1_prefix}/health",
        "timestamp": datetime.utcnow().isoformat(),
        "message": "Welcome to FastAPI Bootcamp! 🚀"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="debug" if settings.debug else "info"
    )
```

## ✅ Paso 7: Testing Básico

### tests/conftest.py

```python
"""
Test configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI application."""
    return TestClient(app)


@pytest.fixture
def sample_greeting_request():
    """Sample greeting request data for tests."""
    return {
        "name": "Alice",
        "language": "en",
        "formal": False
    }
```

### tests/unit/test_greetings.py

```python
"""
Unit tests for greeting functionality.
"""
import pytest
from src.api.utils.greetings import GreetingGenerator


class TestGreetingGenerator:
    """Test cases for the GreetingGenerator class."""

    def test_generate_greeting_english_informal(self):
        """Test generating informal English greeting."""
        greeting = GreetingGenerator.generate_greeting("Alice", "en", False)

        assert "Alice" in greeting
        assert len(greeting) > 0
        assert isinstance(greeting, str)

    def test_generate_greeting_spanish_formal(self):
        """Test generating formal Spanish greeting."""
        greeting = GreetingGenerator.generate_greeting("Carlos", "es", True)

        assert "Carlos" in greeting
        assert len(greeting) > 0
        assert isinstance(greeting, str)

    def test_supported_languages(self):
        """Test getting supported languages."""
        languages = GreetingGenerator.get_supported_languages()

        assert isinstance(languages, list)
        assert "en" in languages
        assert "es" in languages
        assert len(languages) > 0

    def test_is_language_supported(self):
        """Test language support checking."""
        assert GreetingGenerator.is_language_supported("en") is True
        assert GreetingGenerator.is_language_supported("es") is True
        assert GreetingGenerator.is_language_supported("invalid") is False
```

### tests/integration/test_api.py

```python
"""
Integration tests for API endpoints.
"""
import pytest
from fastapi import status


class TestHealthEndpoints:
    """Test cases for health check endpoints."""

    def test_health_check(self, client):
        """Test detailed health check endpoint."""
        response = client.get("/api/v1/health")

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is True
        assert data["status"] == "healthy"
        assert "version" in data
        assert "uptime" in data
        assert "dependencies" in data

    def test_simple_health_check(self, client):
        """Test simple health check endpoint."""
        response = client.get("/api/v1/health/simple")

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestGreetingEndpoints:
    """Test cases for greeting endpoints."""

    def test_hello_world(self, client):
        """Test basic hello world endpoint."""
        response = client.get("/api/v1/greetings/hello")

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is True
        assert "greeting" in data
        assert "World" in data["greeting"]

    def test_personalized_greeting(self, client, sample_greeting_request):
        """Test personalized greeting creation."""
        response = client.post(
            "/api/v1/greetings/personalized",
            json=sample_greeting_request
        )

        assert response.status_code == status.HTTP_201_CREATED

        data = response.json()
        assert data["success"] is True
        assert data["name"] == sample_greeting_request["name"]
        assert data["language"] == sample_greeting_request["language"]
        assert data["formal"] == sample_greeting_request["formal"]
        assert sample_greeting_request["name"] in data["greeting"]

    def test_personalized_greeting_validation_error(self, client):
        """Test validation error handling."""
        invalid_request = {
            "name": "",  # Invalid: empty name
            "language": "invalid",  # Invalid: unsupported language
            "formal": "not_boolean"  # Invalid: not a boolean
        }

        response = client.post(
            "/api/v1/greetings/personalized",
            json=invalid_request
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        data = response.json()
        assert data["success"] is False
        assert "error" in data

    def test_greeting_history(self, client, sample_greeting_request):
        """Test greeting history retrieval."""
        # First, create a greeting
        client.post(
            "/api/v1/greetings/personalized",
            json=sample_greeting_request
        )

        # Then check history
        response = client.get("/api/v1/greetings/history")

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_supported_languages(self, client):
        """Test supported languages endpoint."""
        response = client.get("/api/v1/greetings/languages")

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is True
        assert "languages" in data
        assert "count" in data
        assert data["count"] > 0


class TestRootEndpoint:
    """Test cases for root endpoint."""

    def test_root_endpoint(self, client):
        """Test API root information endpoint."""
        response = client.get("/")

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "docs_url" in data
        assert "message" in data
```

## 🚀 Paso 8: Ejecutar y Probar

### Ejecutar la aplicación

```bash
# Asegúrate de estar en el directorio raíz y entorno virtual activo
cd fastapi-bootcamp-w1
source venv/bin/activate

# Ejecutar en modo desarrollo
python src/main.py

# O usando uvicorn directamente
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Probar los endpoints

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Basic hello
curl http://localhost:8000/api/v1/greetings/hello

# Personalized greeting
curl -X POST "http://localhost:8000/api/v1/greetings/personalized" \
     -H "Content-Type: application/json" \
     -d '{"name": "Alice", "language": "en", "formal": false}'

# Check history
curl http://localhost:8000/api/v1/greetings/history
```

### Ejecutar tests

```bash
# Instalar pytest si no está instalado
pip install pytest pytest-asyncio httpx

# Ejecutar todos los tests
pytest tests/ -v

# Ejecutar con coverage
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

## 📖 Documentación Automática

Una vez que la aplicación esté ejecutándose:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🎯 Resultado Esperado

Al finalizar esta práctica tendrás:

✅ **API profesional funcionando** con múltiples endpoints  
✅ **Documentación automática** completa y profesional  
✅ **Validación robusta** con Pydantic y manejo de errores  
✅ **Estructura escalable** lista para crecimiento  
✅ **Tests básicos** funcionando con coverage  
✅ **Type hints** en todo el código  
✅ **Mejores prácticas** aplicadas desde línea 1

## 🏆 Criterios de Calidad Demostrados

1. **Architecture**: Clean separation of concerns
2. **Validation**: Comprehensive input validation
3. **Documentation**: Auto-generated and comprehensive
4. **Error Handling**: Structured and informative
5. **Testing**: Unit and integration tests
6. **Type Safety**: Full type annotations
7. **Standards**: Industry best practices

**¡Felicidades!** Has creado tu primera API FastAPI que demuestra calidad profesional desde el primer endpoint.

## 🎯 Próximo Paso

Esta API será la base para las siguientes semanas donde agregaremos:

- Base de datos con SQLAlchemy
- Autenticación y autorización
- Testing avanzado
- CI/CD pipeline
- Deployment con Docker

**Tiempo total:** ~90 minutos  
**Valor generado:** API profesional que establece el estándar de calidad
