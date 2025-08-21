# API de Biblioteca - Semana 4

Sistema de gestión de biblioteca desarrollado con FastAPI y SQLAlchemy.

## Funcionalidades

- ✅ **Gestión de Libros**: CRUD completo (crear, leer, actualizar, eliminar)
- ✅ **Gestión de Usuarios**: CRUD completo con validaciones
- ✅ **Sistema de Préstamos**: Lógica de préstamo y devolución
- ✅ **Validaciones de Negocio**: Límites y restricciones
- ✅ **Estadísticas Básicas**: Reportes de uso

## Instalación Rápida

### 1. Prerrequisitos

- Python 3.8+
- pip

### 2. Setup del Proyecto

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python ejemplo_main.py
```

### 3. Verificar Instalación

- Abrir http://localhost:8000
- Documentación automática: http://localhost:8000/docs

## Estructura de la Base de Datos

### Entidades

- **Book**: Libros de la biblioteca
- **User**: Usuarios registrados
- **Loan**: Préstamos activos/históricos

### Reglas de Negocio

- Un libro solo puede prestarse si está disponible
- Un usuario puede tener máximo 3 préstamos activos
- No se puede eliminar un usuario con préstamos activos

## API Endpoints

### Libros

- `POST /api/v1/books/` - Crear libro
- `GET /api/v1/books/` - Listar libros
- `GET /api/v1/books/{id}` - Obtener libro
- `PUT /api/v1/books/{id}` - Actualizar libro
- `DELETE /api/v1/books/{id}` - Eliminar libro

### Usuarios

- `POST /api/v1/users/` - Crear usuario
- `GET /api/v1/users/` - Listar usuarios
- `GET /api/v1/users/{id}` - Obtener usuario
- `PUT /api/v1/users/{id}` - Actualizar usuario
- `DELETE /api/v1/users/{id}` - Eliminar usuario

### Préstamos

- `POST /api/v1/loans/` - Crear préstamo
- `GET /api/v1/loans/` - Listar préstamos
- `PUT /api/v1/loans/{id}/return` - Devolver libro
- `GET /api/v1/loans/active` - Préstamos activos

## Testing

```bash
# Ejecutar tests
python test_api.py
```

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno
- **SQLAlchemy**: ORM para Python
- **SQLite**: Base de datos ligera
- **Pydantic**: Validación de datos
- **pytest**: Framework de testing

## Desarrollo

### Agregar Nuevo Libro

```bash
curl -X POST "http://localhost:8000/api/v1/books/" \
     -H "Content-Type: application/json" \
     -d '{"title": "El Quijote", "author": "Cervantes"}'
```

### Crear Préstamo

```bash
curl -X POST "http://localhost:8000/api/v1/loans/" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 1, "book_id": 1}'
```

## Autor

Desarrollado para el Bootcamp FastAPI - Semana 4
