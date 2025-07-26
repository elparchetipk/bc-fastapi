# Ejercicios Prácticos - Semana 2 (Consolidación)

## 🎯 Objetivo Ultra-Básico

Consolidar conceptos de **Type Hints + Pydantic + Endpoints POST** en el Bloque 4 (45 minutos) a través de ejercicios súper simples.

## ⏱️ Tiempo: 45 minutos (Bloque 4 - Consolidación)

## 📋 Pre-requisitos

- ✅ API de los Bloques 1-3 funcionando
- ✅ Type hints implementados
- ✅ Pydantic básico funcionando
- ✅ Al menos 1 endpoint POST

---

## 🏋️ Ejercicio 1: Verificación Completa (20 min)

**Objetivo**: Asegurar que todo lo aprendido funciona

### 📝 Checklist de Verificación

**Revisa tu main.py actual y marca:**

- [ ] **Type hints**: ¿Tus funciones tienen tipos como `-> dict` o `nombre: str`?
- [ ] **Modelo Pydantic**: ¿Tienes al menos 1 clase que hereda de `BaseModel`?
- [ ] **Endpoint POST**: ¿Tienes un POST que recibe un modelo Pydantic?
- [ ] **Endpoint GET con ID**: ¿Tienes un GET como `/productos/{id}`?
- [ ] **API funcionando**: ¿`uvicorn main:app --reload` funciona sin errores?
- [ ] **Documentación**: ¿Se ve bien en http://127.0.0.1:8000/docs?

### 🔧 **Si algo no funciona**:

1. **Problema con imports**:

   ```python
   from fastapi import FastAPI
   from pydantic import BaseModel
   from typing import Optional
   ```

2. **Problema con POST**: Usa el ejemplo más simple:

   ```python
   class Item(BaseModel):
       nombre: str

   @app.post("/items")
   def crear_item(item: Item) -> dict:
       return {"item": item.dict()}
   ```

3. **Problema con type hints**: Empezar simple:
   ```python
   @app.get("/")
   def home() -> dict:
       return {"mensaje": "funciona"}
   ```

---

## 🏋️ Ejercicio 2: README y GitHub (25 min)

**Objetivo**: Documentar tu progreso y subir a GitHub

### 📝 Instrucciones

**1. Actualizar README.md** (15 min):

````markdown
# Mi API FastAPI - Semana 2

## ¿Qué hace?

API mejorada con validación automática de datos y type hints.

## Nuevos Features (Semana 2)

- ✅ Type hints en todas las funciones
- ✅ Validación automática con Pydantic
- ✅ Endpoint POST para crear datos
- ✅ Parámetros de ruta (ejemplo: /productos/{id})
- ✅ Búsqueda con parámetros query

## ¿Cómo ejecutar?

```bash
pip install fastapi pydantic uvicorn
uvicorn main:app --reload
```
````

## Endpoints principales

- `GET /`: Mensaje de bienvenida
- `POST /productos`: Crear nuevo producto
- `GET /productos`: Ver todos los productos
- `GET /productos/{id}`: Ver producto específico
- `GET /buscar?nombre=...`: Buscar productos

## Documentación

http://127.0.0.1:8000/docs

## Mi progreso

**Semana 1**: API básica con Hello World
**Semana 2**: API con validación y type hints

## Reflexión

[Escribe 2-3 oraciones sobre qué fue lo más útil de esta semana]

````

**2. Subir a GitHub** (10 min):

```bash
# En tu terminal, en la carpeta de tu proyecto
git add .
git commit -m "Semana 2: API con Pydantic y Type Hints"
git push
````

---

## 🚨 Si tienes problemas

### Problemas comunes en Bloque 4:

1. **"Mi API no arranca"**:

   - Verificar imports
   - Verificar indentación
   - Pedir ayuda inmediatamente

2. **"Git no funciona"**:

   - El instructor ayudará paso a paso
   - Es normal, no te frustres

3. **"No sé qué escribir en README"**:
   - Copia el template de arriba
   - Personaliza solo lo básico

### Solución rápida:

- **Enfócate en lo que SÍ funciona**
- **Deja lo complejo para después**
- **Pide ayuda sin pena**

---

## 🎯 Resultado Final (Lo que deberías tener)

Al final del Bloque 4:

1. **✅ API funcionando** con todos los conceptos de Semana 2
2. **✅ README actualizado** con documentación básica
3. **✅ Código en GitHub** con commit de Semana 2
4. **✅ Comprensión clara** de tu progreso

### 📁 Estructura Final

```
tu-repositorio/
├── main.py                    # API con Type Hints + Pydantic
├── requirements.txt           # fastapi, pydantic, uvicorn
└── README.md                  # Documentación actualizada
```

---

## 📊 Auto-evaluación (1 minuto)

**¿Tu API tiene type hints funcionando?** ✅ Sí / ❌ No

**¿Tienes al menos 1 endpoint POST con Pydantic?** ✅ Sí / ❌ No

**¿Está todo subido a GitHub?** ✅ Sí / ❌ No

**Si respondiste 2/3 "Sí": ¡EXCELENTE PROGRESO!**  
**Si respondiste 1/3 "Sí": ¡MUY BIEN, sigue así!**  
**Si respondiste 0/3 "Sí": ¡El instructor te ayudará ahora mismo!**

---

## 🚀 Preparación para Semana 3

Con esta base sólida de Semana 2, en la Semana 3 estarás listo para:

- **Más métodos HTTP** (PUT, DELETE)
- **Manejo de errores avanzado** (status codes)
- **Parámetros más complejos** (headers, forms)

**¡Felicidades por completar la Semana 2! Tu API está evolucionando profesionalmente! 🎉**
