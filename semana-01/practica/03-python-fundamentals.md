# 03 - Fundamentos de Python para FastAPI

## 🎯 Objetivos de Aprendizaje

Al finalizar este módulo, podrás:

- Dominar conceptos fundamentales de Python necesarios para FastAPI
- Utilizar type hints de manera efectiva
- Manejar modelos de datos con Pydantic
- Aplicar decoradores y conceptos de programación asíncrona

## 📋 Prerrequisitos

- Haber completado [01-environment-setup.md](./01-environment-setup.md)
- Haber completado [02-hello-world-api.md](./02-hello-world-api.md)
- Python 3.8+ instalado
- Editor de código configurado

## 🏗️ Estructura de la Práctica

```
semana-01/
├── practica/
│   └── 03-python-fundamentals/
│       ├── examples/
│       │   ├── type_hints.py
│       │   ├── pydantic_models.py
│       │   ├── decorators.py
│       │   └── async_concepts.py
│       └── exercises/
│           ├── exercise_01.py
│           ├── exercise_02.py
│           └── exercise_03.py
```

## 📝 Contenido

### 1. Type Hints en Python

Los type hints son fundamentales para FastAPI y mejoran la experiencia de desarrollo:

#### ¿Por qué usar Type Hints?

- **Documentación automática**: FastAPI genera documentación basada en tipos
- **Validación automática**: Validación de datos de entrada/salida
- **Mejor IDE**: Autocompletado y detección de errores
- **Código más legible**: Claridad sobre tipos de datos esperados

#### Ejemplo Práctico

Crea el archivo `examples/type_hints.py`:

```python
from typing import List, Dict, Optional, Union
from datetime import datetime

# Tipos básicos
def greet(name: str) -> str:
    return f"Hola, {name}!"

def calculate_age(birth_year: int) -> int:
    current_year = datetime.now().year
    return current_year - birth_year

# Tipos complejos
def process_scores(scores: List[float]) -> Dict[str, float]:
    return {
        "average": sum(scores) / len(scores),
        "max": max(scores),
        "min": min(scores)
    }

# Tipos opcionales
def create_user(name: str, email: Optional[str] = None) -> Dict[str, str]:
    user = {"name": name}
    if email:
        user["email"] = email
    return user

# Union types (Python 3.10+: int | str)
def process_id(user_id: Union[int, str]) -> str:
    return str(user_id).upper()

# Ejemplos de uso
if __name__ == "__main__":
    print(greet("Juan"))
    print(calculate_age(1990))
    print(process_scores([85.5, 92.0, 78.5, 95.0]))
    print(create_user("María", "maria@email.com"))
    print(process_id(12345))
```

### 2. Pydantic Models

Pydantic es el corazón de la validación de datos en FastAPI:

#### ¿Qué es Pydantic?

- **Validación de datos**: Valida tipos y formatos automáticamente
- **Serialización**: Convierte datos entre formatos (JSON, dict, etc.)
- **Documentación**: Genera esquemas JSON automáticamente
- **Rendimiento**: Validación rápida basada en type hints

#### Ejemplo Práctico

Crea el archivo `examples/pydantic_models.py`:

```python
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enum para roles
class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

# Modelo básico
class User(BaseModel):
    id: int
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    age: int = Field(..., ge=18, le=120)  # ge = greater equal, le = less equal
    role: UserRole = UserRole.USER
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.now)
    tags: Optional[List[str]] = None

    # Validador personalizado
    @validator('name')
    def name_must_contain_space(cls, v):
        if ' ' not in v.strip():
            raise ValueError('El nombre debe contener al menos un espacio')
        return v.title()

    # Configuración del modelo
    class Config:
        # Permite usar enum values
        use_enum_values = True
        # Ejemplo de JSON válido
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Juan Pérez",
                "email": "juan@email.com",
                "age": 25,
                "role": "user",
                "is_active": True,
                "tags": ["python", "fastapi"]
            }
        }

# Modelo para respuestas (sin campos sensibles)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: UserRole
    is_active: bool
    created_at: datetime

# Modelo para actualización (campos opcionales)
class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    age: Optional[int] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

# Ejemplos de uso
if __name__ == "__main__":
    # Crear usuario válido
    user_data = {
        "id": 1,
        "name": "juan pérez",
        "email": "juan@email.com",
        "age": 25,
        "role": "admin"
    }

    user = User(**user_data)
    print("Usuario creado:", user)
    print("JSON:", user.json(indent=2))
    print("Dict:", user.dict())

    # Validación de errores
    try:
        invalid_user = User(
            id=1,
            name="Juan",  # Sin espacio - error
            email="invalid-email",  # Email inválido
            age=15,  # Menor de 18 - error
            role="invalid_role"  # Rol inválido
        )
    except Exception as e:
        print("Errores de validación:", e)
```

### 3. Decoradores y Middlewares

Los decoradores son fundamentales para FastAPI:

#### Conceptos Clave

- **Decoradores**: Funciones que modifican otras funciones
- **Middlewares**: Procesan requests/responses
- **Dependency Injection**: Sistema de dependencias de FastAPI

#### Ejemplo Práctico

Crea el archivo `examples/decorators.py`:

```python
import time
import functools
from typing import Callable, Any

# Decorador básico para medir tiempo
def timing_decorator(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} tomó {end_time - start_time:.4f} segundos")
        return result
    return wrapper

# Decorador con parámetros
def retry_decorator(max_attempts: int = 3):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Intento {attempt + 1} falló: {e}")
                    time.sleep(1)
        return wrapper
    return decorator

# Decorador para logging
def log_calls(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Llamando a {func.__name__} con args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} retornó: {result}")
        return result
    return wrapper

# Ejemplos de uso
@timing_decorator
@log_calls
def slow_function(n: int) -> int:
    """Función que simula operación lenta"""
    time.sleep(0.1)
    return n * 2

@retry_decorator(max_attempts=3)
def unreliable_function(success_rate: float = 0.7) -> str:
    """Función que puede fallar aleatoriamente"""
    import random
    if random.random() < success_rate:
        return "¡Éxito!"
    else:
        raise Exception("Operación falló")

if __name__ == "__main__":
    # Probar decoradores
    result = slow_function(5)
    print(f"Resultado: {result}")

    try:
        result = unreliable_function(0.3)  # Baja probabilidad de éxito
        print(f"Función poco confiable: {result}")
    except Exception as e:
        print(f"Función falló definitivamente: {e}")
```

### 4. Programación Asíncrona

FastAPI está construido sobre programación asíncrona:

#### Conceptos Clave

- **async/await**: Sintaxis para código asíncrono
- **Coroutines**: Funciones que pueden pausarse y reanudarse
- **Event Loop**: Bucle que maneja operaciones asíncronas
- **Concurrencia vs Paralelismo**: Diferencias importantes

#### Ejemplo Práctico

Crea el archivo `examples/async_concepts.py`:

```python
import asyncio
import aiohttp
import time
from typing import List

# Función síncrona tradicional
def sync_fetch_data(url: str) -> str:
    time.sleep(1)  # Simula llamada a API
    return f"Datos de {url}"

# Función asíncrona
async def async_fetch_data(url: str) -> str:
    await asyncio.sleep(1)  # Simula llamada a API asíncrona
    return f"Datos de {url}"

# Múltiples llamadas síncronas
def sync_fetch_multiple(urls: List[str]) -> List[str]:
    start_time = time.time()
    results = []
    for url in urls:
        result = sync_fetch_data(url)
        results.append(result)

    end_time = time.time()
    print(f"Síncrono tomó: {end_time - start_time:.2f} segundos")
    return results

# Múltiples llamadas asíncronas
async def async_fetch_multiple(urls: List[str]) -> List[str]:
    start_time = time.time()

    # Crear todas las tareas
    tasks = [async_fetch_data(url) for url in urls]

    # Esperar que todas terminen
    results = await asyncio.gather(*tasks)

    end_time = time.time()
    print(f"Asíncrono tomó: {end_time - start_time:.2f} segundos")
    return results

# Ejemplo con aiohttp (HTTP client asíncrono)
async def fetch_real_url(session: aiohttp.ClientSession, url: str) -> dict:
    try:
        async with session.get(url) as response:
            return {
                "url": url,
                "status": response.status,
                "content_length": len(await response.text())
            }
    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }

async def fetch_multiple_urls(urls: List[str]) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_real_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Context manager asíncrono
class AsyncTimer:
    def __init__(self, name: str):
        self.name = name

    async def __aenter__(self):
        self.start_time = time.time()
        print(f"Iniciando {self.name}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        print(f"{self.name} tomó {end_time - self.start_time:.2f} segundos")

# Ejemplo de uso principal
async def main():
    urls = [
        "http://ejemplo1.com",
        "http://ejemplo2.com",
        "http://ejemplo3.com"
    ]

    print("=== Comparación Síncrono vs Asíncrono ===")

    # Llamadas síncronas
    sync_results = sync_fetch_multiple(urls)
    print("Resultados síncronos:", sync_results[:2])

    # Llamadas asíncronas
    async_results = await async_fetch_multiple(urls)
    print("Resultados asíncronos:", async_results[:2])

    print("\n=== Ejemplo con Context Manager Asíncrono ===")
    async with AsyncTimer("Operación compleja"):
        await asyncio.sleep(1)
        print("Procesando datos...")

    print("\n=== Ejemplo con URLs reales ===")
    real_urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/200",
        "https://httpbin.org/json"
    ]

    try:
        real_results = await fetch_multiple_urls(real_urls)
        for result in real_results:
            print(f"URL: {result['url']}, Status: {result.get('status', 'Error')}")
    except Exception as e:
        print(f"Error al obtener URLs: {e}")

if __name__ == "__main__":
    # Ejecutar el programa asíncrono
    asyncio.run(main())
```

## 🏋️ Ejercicios Prácticos

### Ejercicio 1: Type Hints y Validación

Crea el archivo `exercises/exercise_01.py`:

```python
"""
Ejercicio 1: Type Hints y Validación de Datos

Instrucciones:
1. Completa las funciones con type hints apropiados
2. Implementa validación de datos
3. Maneja errores apropiadamente
"""

from typing import List, Dict, Optional, Union
from datetime import datetime

# TODO: Añadir type hints y implementar la función
def calculate_statistics(numbers):
    """
    Calcula estadísticas básicas de una lista de números.

    Args:
        numbers: Lista de números (int o float)

    Returns:
        Diccionario con: count, sum, average, min, max

    Raises:
        ValueError: Si la lista está vacía
        TypeError: Si algún elemento no es número
    """
    # Tu código aquí
    pass

# TODO: Añadir type hints y implementar la función
def format_user_info(user_data):
    """
    Formatea información de usuario.

    Args:
        user_data: Diccionario con keys: name, age, email (opcional)

    Returns:
        String formateado con la información

    Raises:
        KeyError: Si faltan campos requeridos
        ValueError: Si age es negativo
    """
    # Tu código aquí
    pass

# TODO: Añadir type hints y implementar la función
def merge_user_lists(list1, list2):
    """
    Combina dos listas de usuarios sin duplicados.

    Args:
        list1: Lista de diccionarios de usuario
        list2: Lista de diccionarios de usuario

    Returns:
        Lista combinada sin usuarios duplicados (basado en 'id')
    """
    # Tu código aquí
    pass

# Tests
if __name__ == "__main__":
    # Test calculate_statistics
    try:
        stats = calculate_statistics([1, 2, 3, 4, 5])
        print("Stats:", stats)
    except Exception as e:
        print("Error en calculate_statistics:", e)

    # Test format_user_info
    user = {"name": "Juan", "age": 25, "email": "juan@email.com"}
    try:
        info = format_user_info(user)
        print("User info:", info)
    except Exception as e:
        print("Error en format_user_info:", e)

    # Test merge_user_lists
    users1 = [{"id": 1, "name": "Juan"}, {"id": 2, "name": "María"}]
    users2 = [{"id": 2, "name": "María"}, {"id": 3, "name": "Pedro"}]
    try:
        merged = merge_user_lists(users1, users2)
        print("Merged users:", merged)
    except Exception as e:
        print("Error en merge_user_lists:", e)
```

### Ejercicio 2: Pydantic Models

Crea el archivo `exercises/exercise_02.py`:

```python
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
```

### Ejercicio 3: Programación Asíncrona

Crea el archivo `exercises/exercise_03.py`:

```python
"""
Ejercicio 3: Programación Asíncrona Práctica

Instrucciones:
1. Implementa funciones asíncronas
2. Usa asyncio para concurrencia
3. Maneja errores apropiadamente
"""

import asyncio
import aiohttp
import time
from typing import List, Dict, Optional

# TODO: Implementar simulador de base de datos asíncrona
class AsyncDatabase:
    """
    Simulador de base de datos asíncrona.
    """

    def __init__(self):
        self.users = {}
        self.delay = 0.1  # Simula latencia de BD

    async def get_user(self, user_id: int) -> Optional[Dict]:
        """
        Obtiene un usuario por ID.

        Args:
            user_id: ID del usuario

        Returns:
            Diccionario con datos del usuario o None
        """
        # TODO: Implementar con delay asíncrono
        pass

    async def create_user(self, user_data: Dict) -> Dict:
        """
        Crea un nuevo usuario.

        Args:
            user_data: Datos del usuario

        Returns:
            Usuario creado con ID asignado
        """
        # TODO: Implementar con delay asíncrono
        pass

    async def get_multiple_users(self, user_ids: List[int]) -> List[Dict]:
        """
        Obtiene múltiples usuarios concurrentemente.

        Args:
            user_ids: Lista de IDs de usuarios

        Returns:
            Lista de usuarios (sin None)
        """
        # TODO: Usar asyncio.gather para concurrencia
        pass

# TODO: Implementar cliente de API asíncrono
class AsyncAPIClient:
    """
    Cliente para llamadas a APIs externas.
    """

    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"

    async def fetch_post(self, post_id: int) -> Optional[Dict]:
        """
        Obtiene un post por ID.

        Args:
            post_id: ID del post

        Returns:
            Datos del post o None si hay error
        """
        # TODO: Usar aiohttp para llamada HTTP
        pass

    async def fetch_multiple_posts(self, post_ids: List[int]) -> List[Dict]:
        """
        Obtiene múltiples posts concurrentemente.

        Args:
            post_ids: Lista de IDs de posts

        Returns:
            Lista de posts obtenidos exitosamente
        """
        # TODO: Implementar con manejo de errores
        pass

# TODO: Implementar procesador de datos asíncrono
async def process_user_data(db: AsyncDatabase, api: AsyncAPIClient, user_id: int) -> Dict:
    """
    Procesa datos de usuario combinando BD local y API externa.

    Args:
        db: Instancia de AsyncDatabase
        api: Instancia de AsyncAPIClient
        user_id: ID del usuario

    Returns:
        Diccionario con datos procesados
    """
    # TODO: Obtener datos de usuario y posts concurrentemente
    # TODO: Combinar datos y retornar resultado
    pass

# TODO: Implementar función principal
async def main():
    """
    Función principal que demuestra todas las funcionalidades.
    """
    # Inicializar componentes
    db = AsyncDatabase()
    api = AsyncAPIClient()

    # Crear usuarios de prueba
    users_data = [
        {"name": "Juan Pérez", "email": "juan@email.com"},
        {"name": "María García", "email": "maria@email.com"},
        {"name": "Pedro López", "email": "pedro@email.com"}
    ]

    print("=== Creando usuarios ===")
    # TODO: Crear usuarios concurrentemente

    print("\n=== Obteniendo usuarios ===")
    # TODO: Obtener usuarios creados

    print("\n=== Procesando datos de usuarios ===")
    # TODO: Procesar datos de usuarios con API externa

    print("\n=== Midiendo rendimiento ===")
    # TODO: Comparar rendimiento síncrono vs asíncrono

if __name__ == "__main__":
    # Ejecutar programa asíncrono
    asyncio.run(main())
```

## 🔍 Validación y Pruebas

Para verificar tu implementación:

1. **Ejecuta cada ejemplo**:

```bash
cd semana-01/practica/03-python-fundamentals/examples
python type_hints.py
python pydantic_models.py
python decorators.py
python async_concepts.py
```

2. **Completa los ejercicios**:

```bash
cd ../exercises
python exercise_01.py
python exercise_02.py
python exercise_03.py
```

3. **Instala dependencias necesarias**:

```bash
pip install pydantic[email] aiohttp
```

## 📚 Recursos Adicionales

- [Python Type Hints Documentation](https://docs.python.org/3/library/typing.html)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Python Asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [Real Python - Python Type Checking](https://realpython.com/python-type-checking/)

## 🎯 Próximos Pasos

Una vez completado este módulo:

1. Revisa las soluciones en el directorio `soluciones/`
2. Continúa con [04-fastapi-basics.md](./04-fastapi-basics.md)
3. Aplica estos conceptos en el proyecto de la semana

¡Excelente trabajo dominando los fundamentos de Python para FastAPI! 🚀
