# Práctica 30: Documentación Avanzada y Automatización

## 🎯 Objetivo

Implementar documentación avanzada de APIs, automatizar procesos de testing y establecer pipelines de CI/CD básicos en 90 minutos.

## ⏱️ Tiempo: 90 minutos

### 📋 Distribución del tiempo

- **Documentación avanzada con OpenAPI** (25 min)
- **Automatización de tests** (25 min)
- **CI/CD básico con GitHub Actions** (25 min)
- **Monitoreo y métricas** (15 min)

## 📋 Pre-requisitos

- ✅ Práctica 29 completada (cobertura y calidad)
- ✅ Suite completa de tests funcionando
- ✅ Repositorio Git configurado
- ✅ Cuenta de GitHub activa

## 🚀 Desarrollo Paso a Paso

### Paso 1: Documentación Avanzada con OpenAPI (25 min)

#### 1.1 Mejorar metadatos de la API

```python
# main.py
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Mi API FastAPI",
    description="""
    ## API Completa con FastAPI

    Esta API proporciona funcionalidades completas para:

    * **Gestión de usuarios** - CRUD completo
    * **Autenticación JWT** - Login y registro seguro
    * **Validación de datos** - Con Pydantic
    * **Tests automatizados** - Coverage > 80%

    ### Autenticación

    Usa JWT Bearer tokens. Primero regístrate en `/register`,
    luego haz login en `/login` para obtener tu token.
    """,
    version="2.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Soporte API",
        "url": "http://example.com/contact/",
        "email": "soporte@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

def custom_openapi():
    """Personalizar esquema OpenAPI"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Agregar ejemplos personalizados
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }

    # Configurar seguridad
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

#### 1.2 Documentar endpoints con ejemplos

```python
# auth.py (o donde tengas tus endpoints)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

class UserCreate(BaseModel):
    """Modelo para creación de usuario"""
    name: str = Field(..., example="Juan Pérez", description="Nombre completo del usuario")
    email: str = Field(..., example="juan@example.com", description="Email único del usuario")
    age: int = Field(..., ge=0, le=120, example=30, description="Edad del usuario")

    class Config:
        schema_extra = {
            "example": {
                "name": "Juan Pérez",
                "email": "juan@example.com",
                "age": 30
            }
        }

class UserResponse(BaseModel):
    """Modelo de respuesta de usuario"""
    id: int = Field(..., example=1, description="ID único del usuario")
    name: str = Field(..., example="Juan Pérez")
    email: str = Field(..., example="juan@example.com")
    age: int = Field(..., example=30)
    created_at: str = Field(..., example="2024-01-15T10:30:00Z")

@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
    summary="Crear nuevo usuario",
    description="Crea un nuevo usuario con los datos proporcionados",
    response_description="Usuario creado exitosamente",
    responses={
        201: {
            "description": "Usuario creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Juan Pérez",
                        "email": "juan@example.com",
                        "age": 30,
                        "created_at": "2024-01-15T10:30:00Z"
                    }
                }
            }
        },
        422: {
            "description": "Error de validación",
            "content": {
                "application/json": {
                    "example": {
                        "detail": [
                            {
                                "loc": ["body", "email"],
                                "msg": "field required",
                                "type": "value_error.missing"
                            }
                        ]
                    }
                }
            }
        }
    },
    tags=["Usuarios"]
)
async def create_user(user: UserCreate):
    """
    Crear un nuevo usuario en el sistema.

    - **name**: Nombre completo del usuario (requerido)
    - **email**: Email único válido (requerido)
    - **age**: Edad entre 0 y 120 años (requerido)

    Retorna el usuario creado con su ID asignado.
    """
    # Tu lógica aquí
    pass
```

#### 1.3 Generar documentación estática

```bash
# Instalar herramientas
pip install redoc-cli

# Exportar esquema OpenAPI
python -c "
from main import app
import json
with open('openapi.json', 'w') as f:
    json.dump(app.openapi(), f, indent=2)
"

# Generar documentación HTML estática
redoc-cli build openapi.json --output docs/api-docs.html
```

---

### Paso 2: Automatización de Tests (25 min)

#### 2.1 Crear Makefile para automatización

```makefile
# Makefile
.PHONY: help install test test-cov lint format clean docs

help:  ## Mostrar ayuda
	@echo "Comandos disponibles:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Instalar dependencias
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:  ## Ejecutar tests
	pytest -v

test-cov:  ## Ejecutar tests con cobertura
	pytest --cov --cov-report=html --cov-report=term-missing

lint:  ## Verificar calidad de código
	flake8 .
	mypy .
	black --check .
	isort --check-only .

format:  ## Formatear código
	black .
	isort .

clean:  ## Limpiar archivos temporales
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete
	rm -rf htmlcov/
	rm -rf .pytest_cache/

docs:  ## Generar documentación
	python -c "from main import app; import json; json.dump(app.openapi(), open('openapi.json', 'w'), indent=2)"
	redoc-cli build openapi.json --output docs/api-docs.html

ci: lint test-cov  ## Pipeline de CI completo

dev:  ## Ejecutar servidor en modo desarrollo
	uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 2.2 Scripts de automatización

```bash
# scripts/test-runner.sh
#!/bin/bash

echo "🚀 Iniciando pipeline de tests..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

run_command() {
    echo -e "${YELLOW}Ejecutando: $1${NC}"
    if eval $1; then
        echo -e "${GREEN}✅ $1 - EXITOSO${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 - FALLÓ${NC}"
        return 1
    fi
}

# Verificar formato
run_command "black --check ."
if [ $? -ne 0 ]; then exit 1; fi

# Verificar imports
run_command "isort --check-only ."
if [ $? -ne 0 ]; then exit 1; fi

# Linting
run_command "flake8 ."
if [ $? -ne 0 ]; then exit 1; fi

# Type checking
run_command "mypy ."
if [ $? -ne 0 ]; then exit 1; fi

# Tests con cobertura
run_command "pytest --cov --cov-fail-under=80"
if [ $? -ne 0 ]; then exit 1; fi

echo -e "${GREEN}🎉 Todos los tests pasaron exitosamente!${NC}"
```

#### 2.3 Configurar pre-commit

```bash
# Instalar pre-commit
pip install pre-commit

# Inicializar
pre-commit install

# Ejecutar en todos los archivos
pre-commit run --all-files
```

---

### Paso 3: CI/CD Básico con GitHub Actions (25 min)

#### 3.1 Crear workflow de CI

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Cache pip packages
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements*.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint with flake8
        run: |
          flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
          flake8 . --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics

      - name: Format check with black
        run: black --check .

      - name: Import order check with isort
        run: isort --check-only .

      - name: Type check with mypy
        run: mypy .

      - name: Test with pytest
        run: |
          pytest --cov --cov-report=xml --cov-report=term-missing

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          flags: unittests
          name: codecov-umbrella
```

#### 3.2 Workflow de deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  deploy:
    runs-on: ubuntu-latest
    needs: test
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.9

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Generate API documentation
        run: |
          python -c "
          from main import app
          import json
          with open('openapi.json', 'w') as f:
              json.dump(app.openapi(), f, indent=2)
          "

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./docs
```

#### 3.3 Configurar badges para README

````markdown
# Mi API FastAPI

[![CI](https://github.com/tu-usuario/tu-repo/workflows/CI/badge.svg)](https://github.com/tu-usuario/tu-repo/actions)
[![Coverage](https://codecov.io/gh/tu-usuario/tu-repo/branch/main/graph/badge.svg)](https://codecov.io/gh/tu-usuario/tu-repo)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com)

## 🚀 Quick Start

```bash
# Instalar dependencias
make install

# Ejecutar tests
make test-cov

# Verificar calidad
make lint

# Ejecutar servidor
make dev
```
````

## 📊 Métricas de Calidad

- **Cobertura de tests**: >80%
- **Líneas de código**: ~500
- **Tests automatizados**: 25+
- **Endpoints documentados**: 100%

````

---

### Paso 4: Monitoreo y Métricas (15 min)

#### 4.1 Agregar middleware de métricas

```python
# middleware.py
import time
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware para recopilar métricas básicas"""

    def __init__(self, app):
        super().__init__(app)
        self.request_count = 0
        self.request_times = []

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        self.request_count += 1

        response = await call_next(request)

        process_time = time.time() - start_time
        self.request_times.append(process_time)

        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-Count"] = str(self.request_count)

        return response

# main.py
from middleware import MetricsMiddleware

app.add_middleware(MetricsMiddleware)

@app.get("/metrics")
async def get_metrics():
    """Endpoint para obtener métricas básicas"""
    return {
        "total_requests": app.user_middleware[0].request_count,
        "avg_response_time": sum(app.user_middleware[0].request_times) / len(app.user_middleware[0].request_times) if app.user_middleware[0].request_times else 0,
        "endpoints": len(app.routes)
    }
````

#### 4.2 Health check avanzado

```python
# health.py
from fastapi import APIRouter
from sqlalchemy.orm import Session
from database import SessionLocal
import psutil
import time

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check completo del sistema"""
    start_time = time.time()

    # Verificar base de datos
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"

    # Métricas del sistema
    memory_percent = psutil.virtual_memory().percent
    cpu_percent = psutil.cpu_percent()

    response_time = time.time() - start_time

    status = "healthy" if db_status == "healthy" and memory_percent < 90 else "degraded"

    return {
        "status": status,
        "timestamp": time.time(),
        "version": "2.0.0",
        "database": db_status,
        "system": {
            "memory_usage_percent": memory_percent,
            "cpu_usage_percent": cpu_percent
        },
        "response_time_ms": round(response_time * 1000, 2)
    }
```

## ✅ Entregables

Al finalizar esta práctica debes tener:

1. ✅ **Documentación OpenAPI avanzada** con ejemplos
2. ✅ **Scripts de automatización** (Makefile, scripts)
3. ✅ **Pipeline CI/CD** funcionando en GitHub
4. ✅ **Métricas y monitoreo** básico implementado
5. ✅ **Badges de calidad** en el README

## 📚 Recursos de Apoyo

- [FastAPI OpenAPI Documentation](https://fastapi.tiangolo.com/tutorial/metadata/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Codecov Integration](https://about.codecov.io/blog/python-code-coverage-using-github-actions-and-codecov/)

## 🎉 ¡Felicitaciones!

Has completado la Semana 8 sobre **Testing y Calidad**. Ahora tienes:

- ✅ Suite completa de tests automatizados
- ✅ Métricas de cobertura y calidad
- ✅ Documentación profesional
- ✅ Pipeline de CI/CD funcional

¡Tu API está lista para producción!

---

💡 **Tip**: La automatización es clave para mantener la calidad a largo plazo. Invierte tiempo en configurarla bien al inicio.
