# Ejercicios - Semana 2: Python Moderno para APIs

## 🎯 Objetivo

Reforzar los conceptos aprendidos con ejercicios prácticos graduales que complementan las prácticas de la semana.

---

## 📋 Ejercicio 1: Type Hints Básicos (15 min)

### Instrucciones:

Convierte las siguientes funciones sin tipo a funciones con type hints apropiados:

```python
# 1. Función básica
def calcular_precio_total(precio, impuesto, descuento):
    precio_con_impuesto = precio * (1 + impuesto)
    precio_final = precio_con_impuesto * (1 - descuento)
    return precio_final

# 2. Función con lista
def filtrar_pares(numeros):
    return [n for n in numeros if n % 2 == 0]

# 3. Función con diccionario
def contar_palabras(texto):
    palabras = texto.split()
    contador = {}
    for palabra in palabras:
        contador[palabra] = contador.get(palabra, 0) + 1
    return contador

# 4. Función con opcional
def saludar_usuario(nombre, titulo):
    if titulo:
        return f"Hola {titulo} {nombre}"
    return f"Hola {nombre}"
```

### Solución Esperada:

```python
from typing import List, Dict, Optional

def calcular_precio_total(precio: float, impuesto: float, descuento: float) -> float:
    precio_con_impuesto = precio * (1 + impuesto)
    precio_final = precio_con_impuesto * (1 - descuento)
    return precio_final

def filtrar_pares(numeros: List[int]) -> List[int]:
    return [n for n in numeros if n % 2 == 0]

def contar_palabras(texto: str) -> Dict[str, int]:
    palabras = texto.split()
    contador = {}
    for palabra in palabras:
        contador[palabra] = contador.get(palabra, 0) + 1
    return contador

def saludar_usuario(nombre: str, titulo: Optional[str] = None) -> str:
    if titulo:
        return f"Hola {titulo} {nombre}"
    return f"Hola {nombre}"
```

---

## 📋 Ejercicio 2: Modelos Pydantic (20 min)

### Instrucciones:

Crea modelos Pydantic para un sistema de biblioteca:

1. **Libro**: título, autor, ISBN, año publicación, disponible (bool)
2. **Usuario**: nombre, email, fecha nacimiento, tipo (estudiante/profesor/público)
3. **Préstamo**: usuario_id, libro_id, fecha_prestamo, fecha_devolucion

### Requisitos:

- Validación de ISBN (debe tener 13 dígitos)
- Email válido para usuarios
- Año de publicación no puede ser futuro
- Tipos de usuario usando Enum
- Fecha de devolución debe ser posterior a préstamo

### Plantilla:

```python
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date
from enum import Enum
from typing import Optional

class TipoUsuario(str, Enum):
    # Completar aquí

class Libro(BaseModel):
    # Completar aquí

    @validator('isbn')
    def validar_isbn(cls, v):
        # Completar validación
        pass

class Usuario(BaseModel):
    # Completar aquí

class Prestamo(BaseModel):
    # Completar aquí

    @validator('fecha_devolucion')
    def fecha_devolucion_posterior(cls, v, values):
        # Completar validación
        pass
```

### Solución Esperada:

```python
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import date
from enum import Enum
from typing import Optional

class TipoUsuario(str, Enum):
    estudiante = "estudiante"
    profesor = "profesor"
    publico = "publico"

class Libro(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=200)
    autor: str = Field(..., min_length=1, max_length=100)
    isbn: str = Field(..., regex=r'^\d{13}$')
    año_publicacion: int = Field(..., le=date.today().year)
    disponible: bool = True

    @validator('isbn')
    def validar_isbn(cls, v):
        if len(v) != 13 or not v.isdigit():
            raise ValueError('ISBN debe tener exactamente 13 dígitos')
        return v

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    fecha_nacimiento: date
    tipo: TipoUsuario

class Prestamo(BaseModel):
    usuario_id: int = Field(..., ge=1)
    libro_id: int = Field(..., ge=1)
    fecha_prestamo: date
    fecha_devolucion: Optional[date] = None

    @validator('fecha_devolucion')
    def fecha_devolucion_posterior(cls, v, values):
        if v and values.get('fecha_prestamo'):
            if v <= values['fecha_prestamo']:
                raise ValueError('Fecha de devolución debe ser posterior al préstamo')
        return v
```

---

## 📋 Ejercicio 3: Endpoints FastAPI (25 min)

### Instrucciones:

Usando los modelos del ejercicio anterior, crea endpoints para:

1. **POST /libros** - Crear libro
2. **GET /libros** - Listar libros (con filtro por disponibilidad)
3. **GET /libros/buscar** - Buscar por título o autor
4. **PATCH /libros/{libro_id}/disponibilidad** - Cambiar disponibilidad
5. **POST /prestamos** - Crear préstamo (marcar libro como no disponible)

### Plantilla:

```python
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional

app = FastAPI(title="Sistema Biblioteca")

# Almacenamiento temporal
libros = []
usuarios = []
prestamos = []

@app.post("/libros")
def crear_libro(libro: Libro):
    # Completar implementación
    pass

@app.get("/libros")
def listar_libros(disponible: Optional[bool] = None):
    # Completar implementación
    pass

# Completar resto de endpoints
```

### Solución Esperada:

```python
from fastapi import FastAPI, HTTPException, Query, status
from typing import List, Optional

app = FastAPI(title="Sistema Biblioteca")

# Almacenamiento temporal
libros = []
usuarios = []
prestamos = []

@app.post("/libros", status_code=status.HTTP_201_CREATED)
def crear_libro(libro: Libro):
    # Verificar ISBN único
    for l in libros:
        if l.isbn == libro.isbn:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="ISBN ya existe"
            )

    nuevo_libro = libro.dict()
    nuevo_libro["id"] = len(libros) + 1
    libros.append(nuevo_libro)
    return nuevo_libro

@app.get("/libros")
def listar_libros(disponible: Optional[bool] = None):
    resultado = libros.copy()
    if disponible is not None:
        resultado = [l for l in resultado if l["disponible"] == disponible]
    return resultado

@app.get("/libros/buscar")
def buscar_libros(
    titulo: Optional[str] = Query(None, min_length=1),
    autor: Optional[str] = Query(None, min_length=1)
):
    resultado = libros.copy()

    if titulo:
        resultado = [l for l in resultado if titulo.lower() in l["titulo"].lower()]

    if autor:
        resultado = [l for l in resultado if autor.lower() in l["autor"].lower()]

    return resultado

@app.patch("/libros/{libro_id}/disponibilidad")
def cambiar_disponibilidad(libro_id: int, disponible: bool):
    for libro in libros:
        if libro["id"] == libro_id:
            libro["disponible"] = disponible
            return libro

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Libro no encontrado"
    )

@app.post("/prestamos", status_code=status.HTTP_201_CREATED)
def crear_prestamo(prestamo: Prestamo):
    # Verificar que libro existe y está disponible
    libro = None
    for l in libros:
        if l["id"] == prestamo.libro_id:
            libro = l
            break

    if not libro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Libro no encontrado"
        )

    if not libro["disponible"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Libro no disponible"
        )

    # Crear préstamo y marcar libro como no disponible
    nuevo_prestamo = prestamo.dict()
    nuevo_prestamo["id"] = len(prestamos) + 1
    prestamos.append(nuevo_prestamo)

    libro["disponible"] = False

    return nuevo_prestamo
```

---

## 📋 Ejercicio 4: Async/Await (20 min)

### Instrucciones:

Convierte los siguientes endpoints a versiones async y agrega funcionalidad de búsqueda externa:

```python
# Función que simula búsqueda en base de datos externa
import httpx
import asyncio

async def buscar_libro_externo(isbn: str):
    """Simula búsqueda en API externa de libros"""
    await asyncio.sleep(1)  # Simula latencia de red
    return {
        "isbn": isbn,
        "fuente": "API Externa",
        "encontrado": len(isbn) == 13
    }

# Endpoint a convertir:
@app.get("/libros/{libro_id}/info-completa")
def obtener_info_completa(libro_id: int):
    # 1. Buscar libro local
    libro_local = None
    for libro in libros:
        if libro["id"] == libro_id:
            libro_local = libro
            break

    if not libro_local:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    # 2. Buscar información externa (simulado)
    info_externa = buscar_libro_externo(libro_local["isbn"])

    return {
        "libro_local": libro_local,
        "info_externa": info_externa
    }
```

### Solución Esperada:

```python
@app.get("/libros/{libro_id}/info-completa")
async def obtener_info_completa(libro_id: int):
    # 1. Buscar libro local
    libro_local = None
    for libro in libros:
        if libro["id"] == libro_id:
            libro_local = libro
            break

    if not libro_local:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    # 2. Buscar información externa (async)
    info_externa = await buscar_libro_externo(libro_local["isbn"])

    return {
        "libro_local": libro_local,
        "info_externa": info_externa
    }

# Bonus: Endpoint que busca múltiples libros en paralelo
@app.get("/libros/info-externa")
async def obtener_info_externa_lotes():
    """Obtener información externa de todos los libros en paralelo"""
    if not libros:
        return {"libros": []}

    # Crear tareas para buscar información externa en paralelo
    tareas = [buscar_libro_externo(libro["isbn"]) for libro in libros]
    resultados_externos = await asyncio.gather(*tareas)

    # Combinar información local y externa
    libros_completos = []
    for libro, info_externa in zip(libros, resultados_externos):
        libros_completos.append({
            "libro_local": libro,
            "info_externa": info_externa
        })

    return {"libros": libros_completos}
```

---

## 📋 Ejercicio 5: Integración Completa (Opcional - 30 min)

### Instrucciones:

Crea un endpoint que combine todos los conceptos:

**POST /prestamos/inteligente**

Este endpoint debe:

1. Validar datos del préstamo con Pydantic
2. Verificar disponibilidad del libro (async)
3. Buscar información externa del libro (async)
4. Verificar si el usuario tiene préstamos pendientes (async)
5. Crear el préstamo si todo está correcto
6. Enviar notificación (simulada - async)

### Plantilla:

```python
class PrestamoInteligente(BaseModel):
    usuario_id: int
    libro_isbn: str  # Buscar por ISBN en lugar de ID
    dias_prestamo: int = Field(default=14, ge=1, le=30)

async def verificar_prestamos_pendientes(usuario_id: int) -> bool:
    # Simular verificación async
    await asyncio.sleep(0.1)
    prestamos_pendientes = [p for p in prestamos if p["usuario_id"] == usuario_id and not p["fecha_devolucion"]]
    return len(prestamos_pendientes) < 3  # Máximo 3 libros

async def enviar_notificacion(usuario_id: int, libro_titulo: str):
    # Simular envío de notificación
    await asyncio.sleep(0.1)
    return f"Notificación enviada: Préstamo de '{libro_titulo}' confirmado"

@app.post("/prestamos/inteligente")
async def crear_prestamo_inteligente(prestamo: PrestamoInteligente):
    # Implementar lógica completa
    pass
```

### Solución:

Ver archivo separado `ejercicio-5-solucion.py` en la carpeta recursos.

---

## 🎯 Autoevaluación

### Criterios de Éxito:

- [ ] **Ejercicio 1**: Type hints correctos y apropiados
- [ ] **Ejercicio 2**: Modelos Pydantic con validación funcionando
- [ ] **Ejercicio 3**: Endpoints REST siguiendo buenas prácticas
- [ ] **Ejercicio 4**: Uso correcto de async/await
- [ ] **Ejercicio 5**: Integración de todos los conceptos

### Reflexión:

Después de completar los ejercicios, responde:

1. **¿Qué ventajas notaste al usar type hints?**
2. **¿Cómo facilita Pydantic la validación de datos?**
3. **¿En qué casos el async/await mejoró el rendimiento?**
4. **¿Qué patrones de diseño de API identificaste?**

---

**💡 Tip**: Estos ejercicios están diseñados para reforzar lo aprendido en las prácticas. Si algo no está claro, revisa los archivos de teoría y práctica correspondientes.
