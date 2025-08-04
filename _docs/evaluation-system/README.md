# 🎯 Sistema de Evaluación Automática bc-fastapi

Este documento explica el sistema de evaluación automática desarrollado para el bootcamp bc-fastapi, sus mejoras implementadas y cómo usarlo correctamente.

## 📋 Resumen de Problemas Corregidos

### ✅ Problemas Principales Solucionados:

1. **Sintaxis YAML problemática**

   - ❌ **Antes:** Código Python embebido directamente en YAML con strings multilínea complejos
   - ✅ **Después:** Script Python separado en archivo independiente, referenciado desde el workflow

2. **Dependencias complejas e innecesarias**

   - ❌ **Antes:** Ollama, modelos de IA pesados, múltiples jobs interdependientes
   - ✅ **Después:** Evaluación basada en análisis estático eficiente, un solo job principal

3. **Gestión de archivos incorrecta**

   - ❌ **Antes:** Referencias a archivos que no se crean correctamente
   - ✅ **Después:** Creación y manipulación de archivos simplificada y verificada

4. **Timeouts excesivos**

   - ❌ **Antes:** 20-25 minutos por evaluación
   - ✅ **Después:** 15 minutos máximo, con operaciones optimizadas

5. **Manejo de errores mejorado**
   - ❌ **Antes:** Fallos silenciosos o poco descriptivos
   - ✅ **Después:** Validación robusta y mensajes de error claros

## 🚀 Características del Sistema Corregido

### Funcionalidades Principales:

- **🔍 Análisis de código estático:** Detecta patrones FastAPI, endpoints, estructura
- **📊 Evaluación por criterios:** Sistema de puntuación basado en rúbricas del bootcamp
- **📝 Reportes detallados:** Feedback constructivo y específico para cada estudiante
- **⚡ Ejecución eficiente:** Sin dependencias pesadas, evaluación rápida
- **🎯 Adaptable por semana:** Criterios de evaluación que se adaptan al progreso

### Componentes del Sistema:

1. **GitHub Action Principal** (`bc-fastapi-evaluation-final.yml`)

   - Workflow optimizado y funcional
   - Manejo correcto de contexto y parámetros
   - Integración con artifacts para resultados

2. **Script de Evaluación** (`bc_fastapi_evaluator.py`)
   - Análisis completo de código Python
   - Sistema de puntuación configurable
   - Generación de reportes markdown profesionales

## 📦 Instalación y Configuración

### 1. Estructura de Archivos Requerida:

```
bc-fastapi/
├── .github/
│   └── workflows/
│       └── bc-fastapi-evaluation-final.yml
└── _scripts/
    └── evaluation-system/
        └── bc_fastapi_evaluator.py
```

### 2. Pasos de Configuración:

1. **Copiar archivos:**

   ```bash
   # Copiar el workflow corregido
   cp bc-fastapi-evaluation-final.yml .github/workflows/

   # Copiar el script evaluador
   cp bc_fastapi_evaluator.py _scripts/evaluation-system/
   ```

2. **Configurar variables (opcional):**

   - `CREATE_FEEDBACK_ISSUES`: Set a `'true'` para crear issues automáticos
   - `STUDENT_REPOS_TOKEN`: Token para acceso a repositorios de estudiantes

3. **Configurar secrets (para issues automáticos):**
   - `STUDENT_REPOS_TOKEN`: Personal Access Token con permisos de issues

## 🎮 Cómo Usar el Sistema

### Método 1: Ejecución Manual (Recomendado para pruebas)

1. Ve a Actions en tu repositorio GitHub
2. Selecciona "🎯 Evaluación bc-fastapi"
3. Click en "Run workflow"
4. Completa los parámetros:
   - **student_repo:** `usuario/repositorio-estudiante`
   - **pr_number:** Número del Pull Request
   - **week_number:** Semana a evaluar (1-11)

### Método 2: Webhook Automático (Para producción)

```bash
# Desde el repositorio del estudiante, enviar webhook:
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/elparchetipk/bc-fastapi/dispatches \
  -d '{
    "event_type": "student-submission",
    "client_payload": {
      "repository": "usuario/repo-estudiante",
      "pr_number": "123",
      "week_number": "5"
    }
  }'
```

## 📊 Criterios de Evaluación

### Sistema de Puntuación (Total: 100 puntos)

1. **Entrega de Archivos (20 pts)**

   - Presencia de archivos .py válidos
   - Estructura básica del proyecto

2. **Uso de FastAPI (30 pts)**

   - Importación y uso correcto de FastAPI
   - Configuración básica de la aplicación

3. **Implementación de Endpoints (25 pts)**

   - Cantidad y calidad de endpoints
   - Uso correcto de decoradores HTTP

4. **Calidad del Código (25 pts)**
   - Líneas de código desarrolladas
   - Modularización con funciones
   - Estructura general

### Bonus (hasta 10 pts adicionales):

- Tests implementados (+5 pts)
- Buena modularización (+5 pts)

### Categorías de Evaluación:

- 🏆 **Excelente (90-100):** Supera expectativas
- ✅ **Satisfactorio (80-89):** Cumple requisitos
- ⚠️ **Necesita Mejora (70-79):** Cumple parcialmente
- ❌ **Insuficiente (<70):** No cumple requisitos

## 📋 Formato de Resultados

### Artifacts Generados:

1. **evaluation_report.md:** Reporte completo para el estudiante
2. **analysis_result.json:** Datos técnicos del análisis

### Contenido del Reporte:

- Calificación numérica y categórica
- Fortalezas identificadas
- Áreas de mejora específicas
- Análisis técnico detallado
- Próximos pasos y recursos
- Consejos generales

## 🔧 Troubleshooting

### Problemas Comunes:

1. **"Error al clonar repositorio"**

   - Verificar que el repositorio existe y es público
   - Comprobar formato: `usuario/repositorio`

2. **"No se encontró código Python"**

   - Verificar archivos .py en el repositorio
   - Comprobar que está en la rama correcta

3. **"Script evaluador no encontrado"**

   - Verificar que existe `_scripts/evaluation-system/bc_fastapi_evaluator.py`
   - Comprobar permisos de archivo

4. **Issues no se crean automáticamente**
   - Configurar `CREATE_FEEDBACK_ISSUES='true'`
   - Configurar `STUDENT_REPOS_TOKEN` con permisos adecuados

### Logs de Depuración:

Para debugging, revisar los logs de GitHub Actions:

- Sección "📊 Mostrar resumen de evaluación"
- Artifacts generados
- Console output del script Python

## 🎓 Notas para el Bootcamp

### Adaptaciones por Semana:

- **Semanas 1-3:** Criterios más flexibles, enfoque en fundamentos
- **Semanas 4-7:** Incremento en expectativas, endpoints más complejos
- **Semanas 8-11:** Evaluación completa, incluyendo tests y mejores prácticas

### Personalización:

El script `bc_fastapi_evaluator.py` puede modificarse para:

- Ajustar criterios de evaluación por semana
- Cambiar sistema de puntuación
- Personalizar formato de reportes
- Agregar nuevos patrones de detección

## 📞 Soporte

Para problemas con el sistema de evaluación:

1. Revisar logs de GitHub Actions
2. Verificar configuración de archivos
3. Consultar este documento
4. Crear issue en el repositorio principal

---

**Desarrollado para:** bc-fastapi - Bootcamp FastAPI  
**Institución:** SENA - CGMLTI Regional Distrito Capital  
**Instructor:** Erick Granados Torres  
**Versión:** 2.0 - Optimizada y Corregida
