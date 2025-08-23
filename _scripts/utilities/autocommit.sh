#!/bin/bash
# autocommit.sh
# Script de autocommit para el bootcamp bc-fastapi
# Automatiza commits periódicos con mensajes descriptivos

# Configuración
PROJECT_DIR="/home/epti/Documentos/epti-dev/bc-channel/bc-fastapi"
LOG_FILE="${PROJECT_DIR}/_scripts/utilities/autocommit.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Función para logging
log_message() {
    echo "[$TIMESTAMP] $1" | tee -a "$LOG_FILE"
}

# Cambiar al directorio del proyecto
cd "$PROJECT_DIR" || {
    log_message "❌ ERROR: No se pudo acceder al directorio $PROJECT_DIR"
    exit 1
}

log_message "🚀 Iniciando autocommit para bc-fastapi..."

# Verificar si hay cambios
if git diff --quiet && git diff --cached --quiet; then
    log_message "ℹ️  No hay cambios para commitear"
    exit 0
fi

# Obtener estadísticas de cambios
MODIFIED_FILES=$(git diff --name-only | wc -l)
STAGED_FILES=$(git diff --cached --name-only | wc -l)
NEW_FILES=$(git ls-files --others --exclude-standard | wc -l)

# Agregar todos los archivos modificados
git add .

# Generar mensaje de commit automático
WEEK_CHANGES=$(git diff --cached --name-only | grep -E "semana-[0-9]+" | head -3)
DOCS_CHANGES=$(git diff --cached --name-only | grep -E "_docs|README|\.md$" | head -2)

# Crear mensaje de commit descriptivo
if [[ -n "$WEEK_CHANGES" ]]; then
    COMMIT_MSG="📚 Actualización automática bootcamp FastAPI
    
🔄 Archivos modificados: $MODIFIED_FILES
📁 Archivos nuevos: $NEW_FILES
📊 Archivos staged: $STAGED_FILES

📖 Cambios en semanas:
$(echo "$WEEK_CHANGES" | sed 's/^/  - /')

📝 Cambios en documentación:
$(echo "$DOCS_CHANGES" | sed 's/^/  - /')

⏰ Autocommit: $TIMESTAMP"
elif [[ -n "$DOCS_CHANGES" ]]; then
    COMMIT_MSG="📝 Actualización documentación bootcamp FastAPI

🔄 Archivos modificados: $MODIFIED_FILES
📁 Archivos nuevos: $NEW_FILES

📖 Cambios:
$(echo "$DOCS_CHANGES" | sed 's/^/  - /')

⏰ Autocommit: $TIMESTAMP"
else
    COMMIT_MSG="🔄 Actualización automática bootcamp FastAPI

📊 Estadísticas:
  - Archivos modificados: $MODIFIED_FILES
  - Archivos nuevos: $NEW_FILES
  - Archivos staged: $STAGED_FILES

⏰ Autocommit: $TIMESTAMP"
fi

# Realizar el commit
if git commit -m "$COMMIT_MSG"; then
    log_message "✅ Commit exitoso: $MODIFIED_FILES archivos modificados, $NEW_FILES nuevos"
    
    # Opcionalmente hacer push (comentado por seguridad)
    # git push origin main
    
else
    log_message "❌ ERROR: Falló el commit"
    exit 1
fi

log_message "🎉 Autocommit completado exitosamente"
