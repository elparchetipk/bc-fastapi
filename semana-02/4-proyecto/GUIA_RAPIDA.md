# Guía Rápida - Semana 2: API de Biblioteca Personal

## 🚀 Inicio Rápido

### 1. Configuración (15 min)

```bash
# Crear proyecto
mkdir mi-biblioteca-api
cd mi-biblioteca-api

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Instalar dependencias
pip install fastapi uvicorn
```

### 2. Archivo Básico (main.py)

```python
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="Mi Biblioteca API")

# Modelo básico
class Book(BaseModel):
    title: str
    author: str
    pages: Optional[int] = None

# Base de datos en memoria
books = []

@app.get("/")
def read_root():
    return {"message": "Mi Biblioteca API"}

@app.post("/books")
def create_book(book: Book):
    books.append(book.dict())
    return {"message": "Libro creado"}

@app.get("/books")
def get_books():
    return books
```

### 3. Ejecutar

```bash
uvicorn main:app --reload
```

Visita: <http://localhost:8000/docs>

## ✅ Checklist del Proyecto

### Funcionalidades Básicas (60%)

- [ ] Modelo Book con Pydantic
- [ ] POST /books (crear)
- [ ] GET /books (listar)
- [ ] GET /books/{id} (obtener uno)
- [ ] PUT/PATCH /books/{id} (actualizar)
- [ ] DELETE /books/{id} (eliminar)

### Funcionalidades Avanzadas (25%)

- [ ] Búsqueda por título
- [ ] Búsqueda por autor
- [ ] Validaciones custom con Pydantic
- [ ] Enums para status y género

### Async/Await (15%)

- [ ] Mínimo 2 endpoints async
- [ ] Simulación de operaciones I/O
- [ ] Uso correcto de await

## 🎯 Entregables

1. **Código**: main.py funcional
2. **Documentación**: README.md básico
3. **Demo**: Video 3-5 min mostrando la API
4. **Pruebas**: Collection de requests o script

## ⚡ Tips de Éxito

1. **Empieza simple**: CRUD básico primero
2. **Usa /docs**: Para probar endpoints
3. **Un paso a la vez**: No todo de una vez
4. **Pregunta**: Si te atascas, pregunta

## 🔗 Recursos

- [Documentación FastAPI](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://pydantic-docs.helpmanual.io/)
- Archivo `ejemplo_main.py` en este directorio
