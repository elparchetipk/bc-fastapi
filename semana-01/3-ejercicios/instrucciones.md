# Ejercicios Prácticos - Semana 1 (Simplificados)

## 🎯 Objetivo Ultra-Básico

Reforzar conceptos de tu primera API mediante **1-2 ejercicios súper simples** en el Bloque 3 (90 minutos).

> **🔄 AJUSTE APLICADO**: Ejercicios reducidos al mínimo para garantizar éxito y no sobrecargar.

## ⏱️ Tiempo: 90 minutos (Bloque 3)

## 📋 Pre-requisitos

- ✅ API de la Práctica 2 funcionando
- ✅ main.py creado y ejecutándose
- ✅ Documentación /docs accesible

---

## 🏋️ Ejercicio 1: Añadir Endpoint Personal (45 min)

**Objetivo**: Crear UN endpoint personalizado para tu API

### 📝 Instrucciones

1. **Abrir tu main.py** (del Bloque 2)

2. **Agregar este endpoint**:

```python
# Agregar al final de tu main.py existente

@app.get("/mi-perfil")
def mi_perfil():
    return {
        "nombre": "Tu Nombre Aquí",           # Cambiar por tu nombre
        "bootcamp": "FastAPI",
        "semana": 1,
        "fecha": "2024",
        "me_gusta_fastapi": True              # ¿Te gustó FastAPI?
    }
```

3. **Probar el endpoint**:
   - http://127.0.0.1:8000/mi-perfil
   - Verificar en /docs que aparece el nuevo endpoint

### ✅ Criterio de Éxito

- Endpoint responde con tus datos personales
- Aparece en la documentación automática

---

## 🏋️ Ejercicio 2: GitHub y README (45 min)

**Objetivo**: Subir tu API a GitHub con README básico

### 📝 Instrucciones

1. **Crear requirements.txt**:

```bash
# En tu terminal (donde está main.py)
pip freeze > requirements.txt
```

2. **Crear README.md básico**:

````markdown
# Mi Primera API FastAPI

## ¿Qué hace?

Una API básica creada en el Bootcamp FastAPI Semana 1.

## ¿Cómo ejecutar?

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
````

## Endpoints

- `/`: Mensaje de bienvenida
- `/info`: Información de la API
- `/mi-perfil`: Mi perfil personal

## Documentación

http://127.0.0.1:8000/docs

## Reflexión

[Escribe 2-3 oraciones sobre qué aprendiste]

```

3. **Subir a GitHub** (paso a paso con instructor):
   - Crear repositorio: `tu-apellido-primera-api`
   - `git init`
   - `git add .`
   - `git commit -m "Mi primera API FastAPI"`
   - `git push`

### ✅ Criterio de Éxito
- Repositorio en GitHub con 3 archivos mínimos
- README se ve bien en GitHub

---

## 🚨 Si tienes problemas

**NO te compliques**. Este bloque es para consolidar, no para frustrarse.

### Problemas comunes:
- **Git no funciona**: El instructor te ayudará
- **Endpoint no responde**: Revisar sintaxis del código
- **No sale en /docs**: Reiniciar uvicorn

### Solución rápida:
- Levanta la mano
- Pide ayuda a un compañero
- Enfócate en lo que SÍ funciona

---

## 🎯 Resultado Final (Lo que deberías tener)

Al final del Bloque 3:

1. **✅ API con 3-4 endpoints funcionando**
2. **✅ Código en GitHub**
3. **✅ README básico**
4. **✅ Sensación de logro**

### 📁 Estructura Final Mínima

```

tu-repositorio/
├── main.py # Tu API
├── requirements.txt # Dependencias
└── README.md # Documentación básica

```

---

## 📊 Auto-evaluación (1 minuto)

**¿Lograste crear tu primera API?** ✅ Sí / ❌ No

**¿Está funcionando /docs?** ✅ Sí / ❌ No

**¿Está en GitHub?** ✅ Sí / ❌ No

**Si respondiste 2/3 "Sí": ¡EXCELENTE!**
**Si respondiste 1/3 "Sí": ¡MUY BIEN!**
**Si respondiste 0/3 "Sí": ¡El instructor te ayudará!**

---

## 🚀 Preparación para Semana 2

Con estos ejercicios básicos completados, en la Semana 2 estarás listo para:

- **Python Type Hints** (conceptos que ya usaste sin saberlo)
- **Pydantic Models** (para datos más estructurados)
- **Más tipos de endpoints** (POST, PUT, DELETE básicos)

**¡Felicidades por completar tu primera semana! 🎉**
```
