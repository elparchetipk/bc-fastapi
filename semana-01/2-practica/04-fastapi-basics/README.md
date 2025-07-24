# FastAPI Basics - Aplicación de Ejemplo

Esta es la aplicación de ejemplo para aprender los fundamentos de FastAPI.

## Estructura

- `app/main.py` - Aplicación principal
- `app/models.py` - Modelos Pydantic
- `app/examples/` - Ejemplos específicos por concepto

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

## URLs

- Aplicación: http://localhost:8000
- Documentación: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
