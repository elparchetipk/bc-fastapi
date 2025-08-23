# Referencias a la Guía de Configuración de VS Code

Este documento resume todas las ubicaciones donde se ha agregado la referencia a la guía de configuración de VS Code del bootcamp.

## 📁 Referencias Agregadas

### 1. README Principal del Bootcamp

**Archivo**: `/bc-fastapi/README.md`

- **Línea ~260**: En la sección de requisitos previos, después de mencionar VS Code
- **Línea ~451**: En la sección "Setup y Configuración" bajo `_docs/setup/`

### 2. Semana 1 - Introducción a FastAPI

**Archivo**: `/semana-01/README.md`

- **Línea ~71**: Después de las prácticas de environment setup
- **Contexto**: Configuración inicial para evitar errores desde el principio

### 3. Semana 2 - Python Moderno para APIs

**Archivo**: `/semana-02/README.md`

- **Línea ~79**: Después de las prácticas de Pydantic
- **Contexto**: Mejor autocompletado con Pydantic y type hints

### 4. Semana 3 - FastAPI Intermedio

**Archivo**: `/semana-03/README.md`

- **Línea ~97**: Después de las prácticas de validación y errores
- **Contexto**: Trabajo eficiente con validaciones y manejo de errores

### 5. Semana 4 - Bases de Datos con FastAPI

**Archivo**: `/semana-04/README.md`

- **Línea ~18**: Nueva sección "Configuración Previa" antes del contenido
- **Contexto**: Configuración específica para SQLAlchemy, FastAPI y Pydantic

## 🎯 Mensajes por Contexto

### Mensaje General (README principal)

```markdown
> 💡 **Configuración de VS Code**: Para evitar errores de importación y tener la mejor experiencia de desarrollo, consulta la [Guía de Configuración de VS Code](recursos-compartidos/GUIA_CONFIGURACION_VSCODE.md)
```

### Mensaje Semana 1 (Setup inicial)

```markdown
> 💡 **Configuración de VS Code**: Para evitar errores de importación y tener una mejor experiencia de desarrollo, consulta la [Guía de Configuración de VS Code](../recursos-compartidos/GUIA_CONFIGURACION_VSCODE.md)
```

### Mensaje Semana 2 (Pydantic)

```markdown
> 💡 **Configuración de VS Code**: Para mejor autocompletado y detección de errores con Pydantic, consulta la [Guía de Configuración de VS Code](../recursos-compartidos/GUIA_CONFIGURACION_VSCODE.md)
```

### Mensaje Semana 3 (Validaciones)

```markdown
> 💡 **Configuración de VS Code**: Para trabajar eficientemente con validaciones y errores de FastAPI, consulta la [Guía de Configuración de VS Code](../recursos-compartidos/GUIA_CONFIGURACION_VSCODE.md)
```

### Mensaje Semana 4 (Bases de Datos)

```markdown
> **🔧 VS Code Setup**: Para evitar errores de importación con SQLAlchemy, FastAPI y Pydantic, consulta la [Guía de Configuración de VS Code](../recursos-compartidos/GUIA_CONFIGURACION_VSCODE.md) y la [Configuración Rápida](./CONFIGURACION_VSCODE.md)
```

## 📋 Archivos de Configuración Relacionados

### Guías Principales

- `recursos-compartidos/GUIA_CONFIGURACION_VSCODE.md` - Guía completa y detallada
- `semana-04/CONFIGURACION_VSCODE.md` - Guía rápida para semana 4
- `semana-04/4-proyecto/test_configuracion.py` - Script de verificación automática

### Configuración VS Code

- `semana-04/.vscode/settings.json` - Configuración automática para la semana 4
- `semana-04/.env` - Variables de entorno

### Entornos Virtuales

- `recursos-compartidos/venv/semana-04/` - Entorno virtual específico
- `recursos-compartidos/venv/activate-semana.sh` - Script de activación automática
- `recursos-compartidos/venv/README.md` - Documentación de entornos virtuales

## ✅ Resultado

Los estudiantes ahora tienen:

1. **Referencias claras** desde cualquier semana hacia la guía de configuración
2. **Contexto específico** de por qué es importante la configuración en cada etapa
3. **Múltiples puntos de entrada** para encontrar ayuda con VS Code
4. **Guías progresivas** desde configuración básica hasta avanzada

La configuración de VS Code ya no será un bloqueador para el aprendizaje del bootcamp.
