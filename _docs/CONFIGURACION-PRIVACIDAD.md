# 🔒 Estrategia de Privacidad - Configuraciones de Grabación

## 📋 Objetivo

Mantener **toda la configuración de dev containers y scripts de grabación** oculta en GitHub, pero rastreable localmente para desarrollo y mejoras continuas.

## 🎯 Archivos y Carpetas Ocultos

### ✅ **Completamente Ocultos en GitHub:**

```bash
# Carpeta principal de configuraciones de grabación
_docs/video-bc_channel/

# Dev Containers (toda la configuración)
**/.devcontainer/
**/devcontainer.json

# Scripts de control de grabación
**/recording-mode.sh
**/recording-mode.json
**/.vscode/recording-mode.json
**/.vscode/normal-mode.json

# Scripts de setup automático
**/setup.sh
**/*-recording-*.sh
**/*-recording-*.json
```

### ✅ **Scripts de Video (ya ocultos):**

```bash
_docs/video-scripts/
**/video-scripts/
```

## 🚀 Flujo de Trabajo

### **Local (Privado)**

- ✅ Todos los archivos disponibles
- ✅ Control completo de configuraciones
- ✅ Historial de cambios en Git
- ✅ Desarrollo y mejoras continuas

### **GitHub (Público)**

- ❌ Sin configuraciones de dev containers
- ❌ Sin scripts de grabación
- ❌ Sin información sensible de producción de videos
- ✅ Solo código educativo público

## 🔧 Comandos de Verificación

```bash
# Verificar que archivos están siendo ignorados
git status --ignored

# Verificar archivo específico
git check-ignore _docs/video-bc_channel/semana1/.devcontainer/devcontainer.json

# Ver qué reglas aplican a un archivo
git check-ignore -v archivo.json
```

## 📁 Estructura de Grabación (Solo Local)

```
_docs/video-bc_channel/
├── semana1/
│   ├── .devcontainer/
│   │   ├── devcontainer.json     # Config optimizada Python 3.13
│   │   └── setup.sh             # Setup automático FastAPI
│   ├── .vscode/
│   │   └── recording-mode.json   # Configs sin distracciones
│   ├── recording-mode.sh         # Script control de modos
│   ├── README.md                # Documentación completa
│   └── script-video-semana1.md  # Script del video
├── semana2/
│   └── [configuración futura]
└── shared/
    └── [configuraciones comunes]
```

## 🎬 Beneficios de esta Estrategia

### **Para el Creador (Erick):**

- **Privacidad total** de configuraciones de producción
- **Control completo** sobre el entorno de grabación
- **Escalabilidad** para futuras semanas
- **Profesionalismo** sin exposición de "behind the scenes"

### **Para la Audiencia:**

- **Contenido limpio** sin distracciones técnicas
- **Foco en aprendizaje** FastAPI, no en configuración
- **Experiencia profesional** sin ruido de setup

### **Para el Repositorio Público:**

- **Solo contenido educativo** visible
- **Sin configuraciones técnicas** que confundan
- **Profesional y limpio** para estudiantes

## ⚠️ Importante

- **Nunca usar `git add -f`** en archivos de `video-bc_channel/`
- **Verificar siempre** con `git status --ignored` antes de commit
- **Mantener documentación** de cambios en este archivo local

## 🔄 Futuras Expansiones

Para nuevas semanas, seguir el patrón:

```bash
_docs/video-bc_channel/semanaN/
├── .devcontainer/
├── .vscode/
├── recording-mode.sh
└── README.md
```

---

**🎯 Esta estrategia asegura que tu contenido educativo sea público y profesional, mientras mantienes privada toda la infraestructura de producción.**
