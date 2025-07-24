# Práctica 6: Async/Await Básico en FastAPI

## 🎯 Objetivo

Comprender cuándo y cómo usar programación asíncrona en FastAPI para mejorar el rendimiento de tu API.

## ⏱️ Tiempo Estimado: 90 minutos

## 📋 Pre-requisitos

- ✅ API con modelos Pydantic funcionando
- ✅ Entendimiento básico de funciones Python
- ✅ Familiaridad con endpoints FastAPI

## 🤔 ¿Qué es Async/Await?

La programación asíncrona permite que tu API maneje múltiples peticiones sin bloquear mientras espera operaciones lentas (DB, API externa, archivos).

### **Conceptos Clave:**

- **Sync (Síncrono)**: Una operación a la vez, bloquea hasta completarse
- **Async (Asíncrono)**: Puede manejar otras tareas mientras espera
- **await**: Pausa la función hasta que una operación async termine
- **async def**: Define una función asíncrona

## 🔄 Cuándo Usar Async vs Sync

### **✅ Usar ASYNC cuando:**

- Conectas a bases de datos
- Haces llamadas a APIs externas
- Lees/escribes archivos grandes
- Operaciones de red (email, HTTP requests)

### **✅ Usar SYNC cuando:**

- Cálculos matemáticos puros
- Operaciones rápidas en memoria
- Transformaciones de datos simples
- Lógica de negocio sin I/O

## 🚀 Paso 1: Comparación Sync vs Async (20 min)

Agregar a tu `main.py` ejemplos comparativos:

```python
import asyncio
import time
from fastapi import FastAPI
import httpx  # pip install httpx

# Función sync que simula operación lenta
def operacion_lenta_sync():
    """Simula consulta a BD o API externa"""
    time.sleep(2)  # Bloquea por 2 segundos
    return {"resultado": "Operación completada (sync)", "tiempo": 2}

# Función async equivalente
async def operacion_lenta_async():
    """Simula consulta async a BD o API externa"""
    await asyncio.sleep(2)  # No bloquea, permite otras tareas
    return {"resultado": "Operación completada (async)", "tiempo": 2}

# Endpoint sync - BLOQUEA el servidor
@app.get("/sync/lento")
def endpoint_sync_lento():
    """Endpoint que bloquea el servidor"""
    inicio = time.time()
    resultado = operacion_lenta_sync()
    fin = time.time()
    return {
        "mensaje": "Endpoint sync completado",
        "resultado": resultado,
        "tiempo_total": round(fin - inicio, 2)
    }

# Endpoint async - NO bloquea el servidor
@app.get("/async/lento")
async def endpoint_async_lento():
    """Endpoint que NO bloquea el servidor"""
    inicio = time.time()
    resultado = await operacion_lenta_async()
    fin = time.time()
    return {
        "mensaje": "Endpoint async completado",
        "resultado": resultado,
        "tiempo_total": round(fin - inicio, 2)
    }
```

## 🧪 Paso 2: Test de Concurrencia (15 min)

Crear script para probar la diferencia:

```python
# Agregar endpoint para testear concurrencia
@app.get("/test/concurrencia")
async def test_concurrencia():
    """Demuestra ventaja de async con múltiples operaciones"""
    inicio = time.time()

    # Ejecutar 3 operaciones en paralelo
    tareas = [
        operacion_lenta_async(),
        operacion_lenta_async(),
        operacion_lenta_async()
    ]

    # await asyncio.gather() ejecuta todas en paralelo
    resultados = await asyncio.gather(*tareas)

    fin = time.time()

    return {
        "mensaje": "3 operaciones async en paralelo",
        "resultados": resultados,
        "tiempo_total": round(fin - inicio, 2),  # ~2 seg en lugar de 6
        "ventaja": "Con sync habrían tomado 6 segundos"
    }

@app.get("/test/concurrencia-sync")
def test_concurrencia_sync():
    """Comparación: 3 operaciones sync secuenciales"""
    inicio = time.time()

    # Ejecutar 3 operaciones secuencialmente
    resultados = [
        operacion_lenta_sync(),
        operacion_lenta_sync(),
        operacion_lenta_sync()
    ]

    fin = time.time()

    return {
        "mensaje": "3 operaciones sync secuenciales",
        "resultados": resultados,
        "tiempo_total": round(fin - inicio, 2),  # ~6 segundos
        "problema": "Cada operación espera a la anterior"
    }
```

## 🌐 Paso 3: Casos Reales con APIs Externas (25 min)

```python
# Instalar primero: pip install httpx
import httpx

# Cliente HTTP async para APIs externas
async def obtener_datos_externos(url: str):
    """Función async para llamadas HTTP"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=5.0)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            return {"error": f"Error de conexión: {e}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"Error HTTP {e.response.status_code}"}

@app.get("/api-externa/usuario/{user_id}")
async def obtener_usuario_github(user_id: str):
    """Obtener información de usuario de GitHub"""
    url = f"https://api.github.com/users/{user_id}"

    inicio = time.time()
    datos = await obtener_datos_externos(url)
    fin = time.time()

    if "error" in datos:
        raise HTTPException(status_code=400, detail=datos["error"])

    return {
        "usuario": datos.get("login"),
        "nombre": datos.get("name"),
        "repositorios": datos.get("public_repos"),
        "tiempo_respuesta": round(fin - inicio, 2)
    }

@app.get("/api-externa/multiples-usuarios")
async def obtener_multiples_usuarios():
    """Obtener múltiples usuarios en paralelo"""
    usuarios = ["octocat", "torvalds", "gvanrossum"]
    urls = [f"https://api.github.com/users/{user}" for user in usuarios]

    inicio = time.time()

    # Ejecutar todas las peticiones en paralelo
    tareas = [obtener_datos_externos(url) for url in urls]
    resultados = await asyncio.gather(*tareas)

    fin = time.time()

    return {
        "usuarios_obtenidos": len([r for r in resultados if "error" not in r]),
        "resultados": resultados,
        "tiempo_total": round(fin - inicio, 2),
        "ventaja": "Todas las peticiones en paralelo"
    }
```

## 💾 Paso 4: Simulación de Base de Datos Async (20 min)

```python
# Simular operaciones de base de datos async
class DatabaseSimulator:
    """Simulador de operaciones de BD async"""

    async def buscar_persona(self, persona_id: int):
        """Simula búsqueda en BD"""
        await asyncio.sleep(0.1)  # Simula latencia de BD
        # Buscar en nuestra lista en memoria
        for persona in personas:
            if persona.id == persona_id:
                return persona
        return None

    async def buscar_personas_por_categoria(self, categoria: CategoriaPersona):
        """Simula consulta compleja"""
        await asyncio.sleep(0.2)  # Simula consulta compleja
        return [p for p in personas if p.categoria == categoria]

    async def contar_personas(self):
        """Simula operación de conteo"""
        await asyncio.sleep(0.05)
        return len(personas)

# Instancia del simulador
db = DatabaseSimulator()

# Endpoints usando el simulador async
@app.get("/db-async/persona/{persona_id}")
async def obtener_persona_async(persona_id: int):
    """Obtener persona usando BD async simulada"""
    inicio = time.time()

    persona = await db.buscar_persona(persona_id)
    if not persona:
        raise HTTPException(
            status_code=404,
            detail=f"Persona {persona_id} no encontrada"
        )

    fin = time.time()

    return {
        "persona": persona,
        "tiempo_bd": round(fin - inicio, 3),
        "tipo": "async"
    }

@app.get("/db-async/estadisticas")
async def obtener_estadisticas_async():
    """Obtener estadísticas usando múltiples consultas async"""
    inicio = time.time()

    # Ejecutar múltiples consultas en paralelo
    tareas = [
        db.contar_personas(),
        db.buscar_personas_por_categoria(CategoriaPersona.estudiante),
        db.buscar_personas_por_categoria(CategoriaPersona.instructor),
        db.buscar_personas_por_categoria(CategoriaPersona.administrador)
    ]

    total, estudiantes, instructores, admins = await asyncio.gather(*tareas)

    fin = time.time()

    return {
        "estadisticas": {
            "total_personas": total,
            "estudiantes": len(estudiantes),
            "instructores": len(instructores),
            "administradores": len(admins)
        },
        "tiempo_total": round(fin - inicio, 3),
        "ventaja": "Todas las consultas en paralelo"
    }
```

## ⚡ Paso 5: Mejores Prácticas y Errores Comunes (10 min)

```python
# ❌ ERROR: Usar funciones sync en endpoints async
@app.get("/malo/ejemplo")
async def mal_ejemplo():
    """NO hagas esto"""
    time.sleep(2)  # ❌ Bloquea el evento loop
    return {"mensaje": "Mal ejemplo"}

# ✅ CORRECTO: Usar funciones async en endpoints async
@app.get("/bueno/ejemplo")
async def buen_ejemplo():
    """Haz esto en su lugar"""
    await asyncio.sleep(2)  # ✅ No bloquea
    return {"mensaje": "Buen ejemplo"}

# ✅ PATRÓN: Manejar errores en operaciones async
async def operacion_con_timeout():
    """Operación con timeout para evitar cuelgues"""
    try:
        return await asyncio.wait_for(
            operacion_lenta_async(),
            timeout=5.0
        )
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=408,
            detail="Operación tomó demasiado tiempo"
        )

@app.get("/async/con-timeout")
async def endpoint_con_timeout():
    """Endpoint con manejo de timeout"""
    resultado = await operacion_con_timeout()
    return {"resultado": resultado}

# ✅ PATRÓN: Limitar concurrencia
from asyncio import Semaphore

# Semáforo para limitar operaciones concurrentes
semaforo = Semaphore(3)  # Máximo 3 operaciones simultáneas

async def operacion_limitada():
    """Operación con límite de concurrencia"""
    async with semaforo:
        await asyncio.sleep(1)
        return {"mensaje": "Operación completada"}

@app.get("/async/limitado")
async def endpoint_limitado():
    """Endpoint con límite de concurrencia"""
    resultado = await operacion_limitada()
    return resultado
```

## 🧪 Verificación y Testing (Último tiempo)

Script para probar los endpoints async:

```bash
#!/bin/bash
# test_async.sh

echo "🧪 Testing endpoints async vs sync..."

echo "1. Test endpoint sync (debería tomar ~2 segundos):"
time curl -s http://localhost:8000/sync/lento | jq .

echo "2. Test endpoint async (debería tomar ~2 segundos):"
time curl -s http://localhost:8000/async/lento | jq .

echo "3. Test concurrencia async (debería tomar ~2 segundos para 3 operaciones):"
time curl -s http://localhost:8000/test/concurrencia | jq .

echo "4. Test concurrencia sync (debería tomar ~6 segundos para 3 operaciones):"
time curl -s http://localhost:8000/test/concurrencia-sync | jq .

echo "5. Test API externa (GitHub):"
curl -s http://localhost:8000/api-externa/usuario/octocat | jq .

echo "✅ Tests completados"
```

## 🎯 Objetivos Logrados

Al finalizar esta práctica, habrás aprendido:

- ✅ **Diferencia entre sync y async** en la práctica
- ✅ **Cuándo usar cada enfoque** según el caso de uso
- ✅ **asyncio.gather()** para operaciones en paralelo
- ✅ **Manejo de APIs externas** con httpx async
- ✅ **Patrones de timeout y límites** de concurrencia
- ✅ **Errores comunes** y cómo evitarlos

## 📊 Comparación de Rendimiento

| Escenario                 | Sync       | Async    | Mejora          |
| ------------------------- | ---------- | -------- | --------------- |
| 1 operación lenta         | 2s         | 2s       | Sin diferencia  |
| 3 operaciones lentas      | 6s         | 2s       | 3x más rápido   |
| 100 requests concurrentes | Bloqueo    | Fluido   | Dramatica       |
| API + BD + File           | Secuencial | Paralelo | 2-5x más rápido |

## 🚨 Reglas de Oro para Async

1. **Usa async solo cuando necesites I/O** (BD, APIs, archivos)
2. **No uses time.sleep() en funciones async** (usa asyncio.sleep())
3. **Siempre await las operaciones async**
4. **Usa asyncio.gather() para operaciones en paralelo**
5. **Implementa timeouts para evitar cuelgues**
6. **Limita concurrencia para no sobrecargar servicios externos**

## 🔄 Próximos Pasos

1. **Experimenta** con diferentes combinaciones de endpoints
2. **Mide el rendimiento** con herramientas como `ab` o `wrk`
3. **Semana 3**: Usar async con bases de datos reales
4. **Semana 4**: Implementar caché async para mejor rendimiento

---

**💡 Tip**: Async no siempre es mejor. Para operaciones rápidas en memoria, sync puede ser más eficiente debido al overhead del event loop.
