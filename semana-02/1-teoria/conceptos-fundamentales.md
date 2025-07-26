# Teoría - Semana 2: Python Moderno para APIs

## 📚 Conceptos Fundamentales

### 1. Type Hints en Python

#### ¿Qué son los Type Hints?

Los **type hints** son anotaciones que indican qué tipo de datos espera o retorna una función, sin afectar la ejecución del código.

```python
# Sin type hints
def greet(name):
    return f"Hello {name}"

# Con type hints
def greet(name: str) -> str:
    return f"Hello {name}"
```

#### Beneficios:

- ✅ **Mejor documentación** del código
- ✅ **Detección temprana de errores** con herramientas como mypy
- ✅ **Mejor autocompletado** en IDEs
- ✅ **Facilita el mantenimiento** del código

#### Tipos Básicos:

```python
from typing import List, Dict, Optional, Union

def process_data(
    numbers: List[int],
    config: Dict[str, str],
    optional: Optional[str] = None
) -> Union[str, int]:
    pass
```

### 2. Pydantic: Validación de Datos

#### Filosofía de Pydantic

Pydantic sigue el principio **"Parse, don't validate"**:

- **Validación tradicional**: Verificar que los datos sean correctos
- **Parsing con Pydantic**: Convertir y garantizar que los datos sean del tipo correcto

#### Modelo Básico:

```python
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., ge=18, le=120)
    email: EmailStr
    active: bool = True
```

#### Validación Automática:

```python
# Datos válidos
user = User(
    name="Ana",
    age=25,
    email="ana@example.com"
)

# Datos inválidos - lanza ValidationError
try:
    bad_user = User(
        name="A",  # Muy corto
        age=15,     # Menor a 18
        email="invalid-email"  # Email inválido
    )
except ValidationError as e:
    print(e.json())
```

### 3. Programación Asíncrona

#### Conceptos Clave:

- **Sincronía**: Una tarea a la vez, bloqueante
- **Asincronía**: Múltiples tareas concurrentes, no bloqueante
- **Event Loop**: Motor que gestiona tareas asíncronas
- **Corrutina**: Función que puede pausarse y reanudarse

#### Ejemplo Conceptual:

```python
import asyncio
import time

# Función síncrona - bloquea
def slow_task_sync():
    time.sleep(2)
    return "Completed"

# Función asíncrona - no bloquea
async def slow_task_async():
    await asyncio.sleep(2)
    return "Completed"

# Ejecutar múltiples tareas
async def main():
    # Secuencial (6 segundos total)
    start = time.time()
    result1 = await slow_task_async()
    result2 = await slow_task_async()
    result3 = await slow_task_async()
    print(f"Secuencial: {time.time() - start:.2f}s")

    # Paralelo (2 segundos total)
    start = time.time()
    results = await asyncio.gather(
        slow_task_async(),
        slow_task_async(),
        slow_task_async()
    )
    print(f"Paralelo: {time.time() - start:.2f}s")
```

#### Cuándo Usar Async:

**✅ Usar async para:**

- Operaciones de I/O (base de datos, archivos, red)
- Llamadas a APIs externas
- Operaciones que involucran espera

**❌ NO usar async para:**

- Cálculos matemáticos intensivos
- Operaciones rápidas en memoria
- Transformaciones de datos simples

### 4. FastAPI y HTTP Methods

#### Métodos HTTP y sus Propósitos:

| Método     | Propósito           | Idempotente | Ejemplo      |
| ---------- | ------------------- | ----------- | ------------ |
| **GET**    | Obtener datos       | ✅          | List users   |
| **POST**   | Crear recurso       | ❌          | Create user  |
| **PUT**    | Actualizar completo | ✅          | Replace user |
| **PATCH**  | Actualizar parcial  | ❌          | Change email |
| **DELETE** | Eliminar recurso    | ✅          | Delete user  |

#### Status Codes Importantes:

```python
from fastapi import status

# 2xx - Éxito
status.HTTP_200_OK          # Operación exitosa
status.HTTP_201_CREATED     # Recurso creado
status.HTTP_204_NO_CONTENT  # Éxito sin contenido

# 4xx - Error del cliente
status.HTTP_400_BAD_REQUEST     # Datos inválidos
status.HTTP_401_UNAUTHORIZED    # No autenticado
status.HTTP_403_FORBIDDEN       # Sin permisos
status.HTTP_404_NOT_FOUND       # Recurso no existe
status.HTTP_422_UNPROCESSABLE_ENTITY  # Error de validación

# 5xx - Error del servidor
status.HTTP_500_INTERNAL_SERVER_ERROR  # Error interno
```

### 5. Principios de Diseño de APIs REST

#### Recursos y URIs:

```python
# ✅ Buenas prácticas
GET    /users          # List users
GET    /users/123      # Get specific user
POST   /users          # Create new user
PUT    /users/123      # Update complete user
PATCH  /users/123      # Update partial user
DELETE /users/123      # Delete user

# ❌ Malas prácticas
GET    /getUsers       # Verbo en URL
POST   /users/create   # Acción innecesaria
GET    /users/123/delete  # Acción incorrecta
```

#### Consistencia en Respuestas:

```python
# Estructura consistente para errores
{
    "error": "ValidationError",
    "message": "Email already exists",
    "details": {...},
    "timestamp": "2025-07-24T10:30:00Z"
}

# Estructura para éxito
{
    "data": {...},
    "message": "User created successfully",
    "timestamp": "2025-07-24T10:30:00Z"
}
```

### 6. Validación vs Transformación

#### Pydantic hace ambas:

```python
from pydantic import BaseModel, validator

class Product(BaseModel):
    name: str
    price: float
    category: str

    # Validator que transforma
    @validator('name')
    def normalize_name(cls, v):
        return v.strip().title()

    # Validator que valida
    @validator('price')
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

    # Root validator para validaciones complejas
    @root_validator
    def validate_complete_product(cls, values):
        name = values.get('name')
        price = values.get('price')

        # Productos premium deben tener nombre largo
        if price > 1000 and len(name) < 10:
            raise ValueError('Expensive products need descriptive names')

        return values
```

## 🎯 Resumen de Conceptos Clave

1. **Type Hints**: Documentan y mejoran la calidad del código
2. **Pydantic**: Valida y transforma datos automáticamente
3. **Async/Await**: Mejora rendimiento en operaciones I/O
4. **HTTP Methods**: Cada uno tiene un propósito específico
5. **REST API Design**: Consistencia y predictibilidad
6. **Validación**: Garantiza integridad de datos

Estos conceptos se combinan en FastAPI para crear APIs robustas, eficientes y fáciles de mantener.
