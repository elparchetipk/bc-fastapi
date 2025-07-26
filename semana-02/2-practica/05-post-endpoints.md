# Práctica 5: Endpoints POST y Parámetros

## 🎯 Objetivo Ultra-Básico

Dominar **endpoints POST y parámetros** básicos en 90 minutos (Bloque 3), consolidando todo lo aprendido.

## ⏱️ Tiempo: 90 minutos (Bloque 3)

## 📋 Pre-requisitos

- ✅ Type hints implementados (Bloque 1)
- ✅ Pydantic básico funcionando (Bloque 2)
- ✅ Al menos 1 endpoint POST creado

## 🚀 Desarrollo Ultra-Rápido (Solo 3 pasos)

### Paso 1: Parámetros de Ruta y Query (30 min)

**Parámetros de Ruta** (en la URL):

```python
# Agregar a tu main.py existente

# Parámetro de ruta simple
@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int) -> dict:
    for producto in productos:
        if producto["id"] == producto_id:
            return {"producto": producto}
    return {"error": "Producto no encontrado"}

# Múltiples parámetros de ruta
@app.get("/categorias/{categoria}/productos/{producto_id}")
def producto_por_categoria(categoria: str, producto_id: int) -> dict:
    return {
        "categoria": categoria,
        "producto_id": producto_id,
        "mensaje": f"Buscando producto {producto_id} en {categoria}"
    }
```

**Parámetros de Query** (después del ?):

```python
from typing import Optional

# Query parameters opcionales
@app.get("/buscar")
def buscar_productos(
    nombre: Optional[str] = None,
    precio_max: Optional[int] = None,
    disponible: Optional[bool] = None
) -> dict:
    resultados = productos.copy()

    if nombre:
        resultados = [p for p in resultados if nombre.lower() in p["nombre"].lower()]
    if precio_max:
        resultados = [p for p in resultados if p["precio"] <= precio_max]
    if disponible is not None:
        resultados = [p for p in resultados if p["disponible"] == disponible]

    return {"resultados": resultados, "total": len(resultados)}
```

**🔍 Probar** (5 min):

- http://127.0.0.1:8000/productos/1
- http://127.0.0.1:8000/buscar?nombre=laptop
- http://127.0.0.1:8000/buscar?precio_max=50000&disponible=true

### Paso 2: Response Models con Pydantic (30 min)

**Definir respuestas consistentes:**

```python
# Agregar estos modelos después de tu modelo Producto

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: int
    disponible: bool
    mensaje: str = "Producto obtenido exitosamente"

class ListaProductosResponse(BaseModel):
    productos: list
    total: int
    mensaje: str = "Lista obtenida exitosamente"

# Actualizar endpoints para usar response models
@app.get("/productos", response_model=ListaProductosResponse)
def obtener_productos() -> ListaProductosResponse:
    return ListaProductosResponse(
        productos=productos,
        total=len(productos)
    )

@app.post("/productos", response_model=ProductoResponse)
def crear_producto(producto: Producto) -> ProductoResponse:
    producto_dict = producto.dict()
    producto_dict["id"] = len(productos) + 1
    productos.append(producto_dict)

    return ProductoResponse(
        id=producto_dict["id"],
        nombre=producto_dict["nombre"],
        precio=producto_dict["precio"],
        disponible=producto_dict["disponible"],
        mensaje="Producto creado exitosamente"
    )
```

### Paso 3: Integración y Consolidación (30 min)

**Tu API completa debería verse así:**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI(title="Mi API Mejorada - Semana 2")

# Modelos de datos
class Producto(BaseModel):
    nombre: str
    precio: int
    disponible: bool = True

class ProductoResponse(BaseModel):
    id: int
    nombre: str
    precio: int
    disponible: bool
    mensaje: str = "Operación exitosa"

class ListaProductosResponse(BaseModel):
    productos: List[dict]
    total: int
    mensaje: str = "Lista obtenida"

# Almacenamiento temporal
productos = []

# Endpoints básicos
@app.get("/")
def hola_mundo() -> dict:
    return {"mensaje": "¡API Semana 2 con Pydantic y Type Hints!"}

@app.get("/productos", response_model=ListaProductosResponse)
def obtener_productos() -> ListaProductosResponse:
    return ListaProductosResponse(
        productos=productos,
        total=len(productos)
    )

@app.post("/productos", response_model=ProductoResponse)
def crear_producto(producto: Producto) -> ProductoResponse:
    producto_dict = producto.dict()
    producto_dict["id"] = len(productos) + 1
    productos.append(producto_dict)

    return ProductoResponse(**producto_dict, mensaje="Producto creado")

@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int) -> dict:
    for producto in productos:
        if producto["id"] == producto_id:
            return {"producto": producto}
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.get("/buscar")
def buscar_productos(
    nombre: Optional[str] = None,
    precio_max: Optional[int] = None
) -> dict:
    resultados = productos.copy()

    if nombre:
        resultados = [p for p in resultados if nombre.lower() in p["nombre"].lower()]
    if precio_max:
        resultados = [p for p in resultados if p["precio"] <= precio_max]

    return {"resultados": resultados, "total": len(resultados)}
```

**🔍 Verificación Final** (15 min):

1. Todos los endpoints funcionan
2. /docs muestra response models
3. Validación automática funciona
4. Búsqueda con parámetros funciona

## ✅ Criterios de Éxito (Solo estos 4)

1. **✅ Endpoint POST funcionando**: Con Pydantic y response model
2. **✅ Parámetros de ruta**: Al menos 1 endpoint con {id}
3. **✅ Parámetros de query**: Al menos 1 endpoint con búsqueda
4. **✅ Response models**: Respuestas consistentes

## 🚨 Si algo no funciona

**Prioridades en orden**:

1. **Que funcione el POST básico** (más importante)
2. **Que funcionen los parámetros de ruta**
3. **Que funcionen los query parameters**
4. **Response models** (si hay tiempo)

**Pide ayuda inmediatamente** si el POST no funciona.

## 📝 Reflexión (Solo 1 pregunta)

**¿Cómo mejoraron estos conceptos tu API comparada con Semana 1?**

Anota 2-3 oraciones para tu README.

---

## 🎯 Resultado Final Esperado

Al final de estos 90 minutos tendrás:

- ✅ API completa con POST, GET con parámetros
- ✅ Validación automática funcionando
- ✅ Response models para respuestas consistentes
- ✅ Manejo básico de errores
- ✅ API significativamente más robusta que Semana 1

**¡Excelente! Tu API está evolucionando profesionalmente! 🎉**

---

## 📋 Para el Bloque 4 (45 min) - Consolidación

En el último bloque:

1. **Probar todo funcionando** completamente
2. **Actualizar README** con nuevos endpoints
3. **Subir a GitHub** código mejorado
4. **Reflexión final** sobre el progreso

**Tu API está lista para ser entregada - ¡gran progreso desde Semana 1!**
