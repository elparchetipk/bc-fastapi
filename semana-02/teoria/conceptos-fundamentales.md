# Teoría - Semana 2: Python Moderno para APIs

## 📚 Conceptos Fundamentales

### 1. Type Hints en Python

#### ¿Qué son los Type Hints?

Los **type hints** son anotaciones que indican qué tipo de datos espera o retorna una función, sin afectar la ejecución del código.

```python
# Sin type hints
def saludar(nombre):
    return f"Hola {nombre}"

# Con type hints
def saludar(nombre: str) -> str:
    return f"Hola {nombre}"
```

#### Beneficios:

- ✅ **Mejor documentación** del código
- ✅ **Detección temprana de errores** con herramientas como mypy
- ✅ **Mejor autocompletado** en IDEs
- ✅ **Facilita el mantenimiento** del código

#### Tipos Básicos:

```python
from typing import List, Dict, Optional, Union

def procesar_datos(
    numeros: List[int],
    configuracion: Dict[str, str],
    opcional: Optional[str] = None
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

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=50)
    edad: int = Field(..., ge=18, le=120)
    email: EmailStr
    activo: bool = True
```

#### Validación Automática:

```python
# Datos válidos
usuario = Usuario(
    nombre="Ana",
    edad=25,
    email="ana@ejemplo.com"
)

# Datos inválidos - lanza ValidationError
try:
    usuario_malo = Usuario(
        nombre="A",  # Muy corto
        edad=15,     # Menor a 18
        email="email-malo"  # Email inválido
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
def tarea_lenta_sync():
    time.sleep(2)
    return "Completado"

# Función asíncrona - no bloquea
async def tarea_lenta_async():
    await asyncio.sleep(2)
    return "Completado"

# Ejecutar múltiples tareas
async def main():
    # Secuencial (6 segundos total)
    inicio = time.time()
    resultado1 = await tarea_lenta_async()
    resultado2 = await tarea_lenta_async()
    resultado3 = await tarea_lenta_async()
    print(f"Secuencial: {time.time() - inicio:.2f}s")

    # Paralelo (2 segundos total)
    inicio = time.time()
    resultados = await asyncio.gather(
        tarea_lenta_async(),
        tarea_lenta_async(),
        tarea_lenta_async()
    )
    print(f"Paralelo: {time.time() - inicio:.2f}s")
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

| Método     | Propósito           | Idempotente | Ejemplo            |
| ---------- | ------------------- | ----------- | ------------------ |
| **GET**    | Obtener datos       | ✅          | Listar usuarios    |
| **POST**   | Crear recurso       | ❌          | Crear usuario      |
| **PUT**    | Actualizar completo | ✅          | Reemplazar usuario |
| **PATCH**  | Actualizar parcial  | ❌          | Cambiar email      |
| **DELETE** | Eliminar recurso    | ✅          | Eliminar usuario   |

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
GET    /usuarios          # Listar usuarios
GET    /usuarios/123      # Obtener usuario específico
POST   /usuarios          # Crear nuevo usuario
PUT    /usuarios/123      # Actualizar usuario completo
PATCH  /usuarios/123      # Actualizar usuario parcial
DELETE /usuarios/123      # Eliminar usuario

# ❌ Malas prácticas
GET    /getUsuarios       # Verbo en URL
POST   /usuarios/create   # Acción innecesaria
GET    /usuarios/123/delete  # Acción incorrecta
```

#### Consistencia en Respuestas:

```python
# Estructura consistente para errores
{
    "error": "ValidationError",
    "message": "Email ya existe",
    "details": {...},
    "timestamp": "2025-07-24T10:30:00Z"
}

# Estructura para éxito
{
    "data": {...},
    "message": "Usuario creado exitosamente",
    "timestamp": "2025-07-24T10:30:00Z"
}
```

### 6. Validación vs Transformación

#### Pydantic hace ambas:

```python
from pydantic import BaseModel, validator

class Producto(BaseModel):
    nombre: str
    precio: float
    categoria: str

    # Validator que transforma
    @validator('nombre')
    def normalizar_nombre(cls, v):
        return v.strip().title()

    # Validator que valida
    @validator('precio')
    def validar_precio(cls, v):
        if v <= 0:
            raise ValueError('Precio debe ser positivo')
        return v

    # Root validator para validaciones complejas
    @root_validator
    def validar_producto_completo(cls, values):
        nombre = values.get('nombre')
        precio = values.get('precio')

        # Productos premium deben tener nombre largo
        if precio > 1000 and len(nombre) < 10:
            raise ValueError('Productos caros necesitan nombres descriptivos')

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
