#!/bin/bash
# monitor-autocommit.sh
# Monitor en tiempo real del autocommit para desarrollo activo

LOG_FILE="/home/epti/Documentos/epti-dev/bc-channel/bc-fastapi/_scripts/utilities/autocommit.log"
PROJECT_DIR="/home/epti/Documentos/epti-dev/bc-channel/bc-fastapi"

echo "📊 Monitor de Autocommit bc-fastapi"
echo "=================================="
echo "📁 Proyecto: $PROJECT_DIR"
echo "📝 Log: $LOG_FILE"
echo "⏰ Frecuencia: Cada 5 minutos"
echo ""

# Función para mostrar estado actual
show_status() {
    cd "$PROJECT_DIR" || {
        echo "❌ ERROR: No se pudo acceder al directorio $PROJECT_DIR"
        return 1
    }
    
    echo "🔍 Estado actual del repositorio:"
    echo "   - Rama: $(git branch --show-current)"
    echo "   - Último commit: $(git log -1 --oneline)"
    echo "   - Archivos modificados: $(git diff --name-only | wc -l)"
    echo "   - Archivos nuevos: $(git ls-files --others --exclude-standard | wc -l)"
    
    if [[ -f "$LOG_FILE" ]]; then
        echo ""
        echo "📝 Últimos 3 autocommits:"
        grep "✅ Commit exitoso" "$LOG_FILE" | tail -3 | while read line; do
            echo "   $line"
        done
    fi
}

# Mostrar estado inicial
show_status

echo ""
echo "🔄 Monitoreando autocommit en tiempo real..."
echo "   (Presiona Ctrl+C para salir)"
echo ""

# Monitor en tiempo real
tail -f "$LOG_FILE" 2>/dev/null &
TAIL_PID=$!

# Trap para limpiar al salir
trap 'kill $TAIL_PID 2>/dev/null; echo ""; echo "👋 Monitor detenido"; exit 0' INT

# Mantener el script corriendo
wait $TAIL_PID
