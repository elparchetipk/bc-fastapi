# Práctica 6: Endpoints PUT (Actualizar Datos)

## 🎯 Objetivo Ultra-Básico

Aprender a **actualizar datos existentes** con endpoints PUT en 75 minutos (Bloque 1 pre-break), enfocándose solo en lo esencial.

## ⏱️ Tiempo: 75 minutos (Bloque 1 pre-break)

## 📋 Pre-requisitos

- ✅ API de Semana 2 con POST funcionando
- ✅ Modelos Pydantic implementados
- ✅ Datos creándose correctamente

## 🚀 Desarrollo Ultra-Rápido (Solo 3 pasos)

### Paso 1: Concepto PUT - Actualizar (25 min)

**Concepto Simple**: PUT actualiza datos que ya existen.

**Diferencias básicas**:

- **POST**: Crear algo nuevo
- **PUT**: Actualizar algo existente
- **GET**: Ver/leer datos

```python
# Partir de tu API de Semana 2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Mi API con CRUD")

# Tu modelo existente (de Semana 2)
class Producto(BaseModel):
    nombre: str
    precio: int
    disponible: bool = True

# Lista temporal (como en Semana 2)
productos = []

# Tus endpoints existentes (GET y POST)
@app.get("/")
def hola_mundo() -> dict:
    return {"mensaje": "¡API Semana 3 con CRUD!"}

@app.post("/productos")
def crear_producto(producto: Producto) -> dict:
    producto_dict = producto.dict()
    producto_dict["id"] = len(productos) + 1
    productos.append(producto_dict)
    return {"mensaje": "Producto creado", "producto": producto_dict}

@app.get("/productos")
def obtener_productos() -> dict:
    return {"productos": productos, "total": len(productos)}
```

### Paso 2: Implementar PUT Básico (25 min)

**Agregar endpoint PUT** (actualizar producto):

```python
# NUEVO: Endpoint PUT para actualizar
@app.put("/productos/{producto_id}")
def actualizar_producto(producto_id: int, producto: Producto) -> dict:
    # Buscar el producto existente
    for i, p in enumerate(productos):
        if p["id"] == producto_id:
            # Actualizar los datos
            producto_actualizado = producto.dict()
            producto_actualizado["id"] = producto_id  # Mantener el ID
            productos[i] = producto_actualizado
            return {
                "mensaje": "Producto actualizado",
                "producto": producto_actualizado
            }

    # Si no se encuentra
    raise HTTPException(status_code=404, detail="Producto no encontrado")

# Endpoint auxiliar para obtener un producto específico
@app.get("/productos/{producto_id}")
def obtener_producto(producto_id: int) -> dict:
    for producto in productos:
        if producto["id"] == producto_id:
            return {"producto": producto}
    raise HTTPException(status_code=404, detail="Producto no encontrado")
```

**🔍 Verificación (5 min):**

1. Ejecuta `uvicorn main:app --reload`
2. Ve a http://127.0.0.1:8000/docs
3. Primero crea un producto con POST
4. Luego actualízalo con PUT

### Paso 3: Probar PUT en Acción (25 min)

**Flujo de prueba completo:**

```python
# 1. Crear producto
POST /productos
{
  "nombre": "Laptop Gaming",
  "precio": 200000,
  "disponible": true
}

# 2. Ver que se creó
GET /productos/1

# 3. Actualizar el producto
PUT /productos/1
{
  "nombre": "Laptop Gaming Pro",
  "precio": 250000,
  "disponible": false
}

# 4. Verificar que se actualizó
GET /productos/1
```

**Casos que debes probar** (15 min):

1. **Actualización exitosa**: PUT con ID existente
2. **Producto no encontrado**: PUT con ID que no existe (debería dar error 404)
3. **Datos válidos**: PUT con datos correctos
4. **Datos inválidos**: PUT con datos incorrectos (Pydantic debería rechazar)

**Ejemplo de uso en /docs** (10 min):

- Usa la interfaz de FastAPI para probar
- Crea al menos 2 productos
- Actualiza al menos 1 producto
- Intenta actualizar un ID que no existe

## ✅ Criterios de Éxito (Solo estos 3)

1. **✅ Endpoint PUT funcionando**: Actualiza datos existentes
2. **✅ Error 404 funcionando**: Cuando el ID no existe
3. **✅ Validación Pydantic**: Rechaza datos incorrectos

## 🚨 Si algo no funciona

**Problemas comunes**:

1. **"No encuentra el producto"**: Verificar que el ID existe
2. **"HTTPException no funciona"**: Verificar import `from fastapi import HTTPException`
3. **"Datos no se actualizan"**: Verificar que estás modificando la lista correcta

**Solución rápida**:

- **Copia exacto el código de arriba**
- **Pide ayuda inmediatamente**
- **Asegúrate de que POST funciona primero**

## 📝 Reflexión (Solo 1 pregunta)

**¿En qué se diferencia PUT de POST en tu API?**

Anota 2-3 oraciones para incluir en tu README.

---

## 🎯 Resultado Final Esperado

Al final de estos 75 minutos tendrás:

- ✅ Endpoint PUT funcionando correctamente
- ✅ Capacidad de actualizar productos existentes
- ✅ Manejo básico de error 404
- ✅ Comprensión de diferencia POST vs PUT
- ✅ Preparación para DELETE (después del break)

**¡Excelente! Ya puedes crear Y actualizar datos! 🎉**

---

## 📋 Para el Break (30 min)

Durante el break obligatorio:

1. **Descansa** - PUT puede ser confuso al principio
2. **Revisa tu código** - Verifica que PUT funciona
3. **Prepárate mentalmente** - Después del break: DELETE (eliminar datos)

**Guarda tu main.py actualizado - lo necesitaremos para DELETE después del break**
