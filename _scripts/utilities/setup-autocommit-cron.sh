#!/bin/bash
# setup-autocommit-cron.sh
# Configura una tarea cron para ejecutar autocommit automáticamente

SCRIPT_PATH="/home/epti/Documentos/epti-dev/bc-channel/bc-fastapi/_scripts/utilities/autocommit.sh"
CRON_SCHEDULE="0 */2 * * *"  # Cada 2 horas
LOG_FILE="/home/epti/Documentos/epti-dev/bc-channel/bc-fastapi/_scripts/utilities/autocommit.log"

echo "🔧 Configurando autocommit automático para bc-fastapi..."
echo "======================================================"

# Verificar que el script existe
if [[ ! -f "$SCRIPT_PATH" ]]; then
    echo "❌ ERROR: Script autocommit.sh no encontrado en $SCRIPT_PATH"
    exit 1
fi

# Verificar que el script es ejecutable
if [[ ! -x "$SCRIPT_PATH" ]]; then
    echo "🔧 Haciendo ejecutable el script..."
    chmod +x "$SCRIPT_PATH"
fi

# Crear entrada de cron
CRON_ENTRY="$CRON_SCHEDULE $SCRIPT_PATH >> $LOG_FILE 2>&1"

echo ""
echo "📅 Configuración de cron:"
echo "   Frecuencia: Cada 2 horas"
echo "   Comando: $SCRIPT_PATH"
echo "   Log: $LOG_FILE"
echo ""

# Verificar si ya existe la entrada en cron
if crontab -l 2>/dev/null | grep -q "$SCRIPT_PATH"; then
    echo "⚠️  Ya existe una tarea cron para autocommit"
    echo "🔍 Tareas cron actuales relacionadas:"
    crontab -l 2>/dev/null | grep "$SCRIPT_PATH"
    echo ""
    read -p "¿Deseas reemplazarla? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cancelado por el usuario"
        exit 0
    fi
    
    # Remover entrada existente
    crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH" | crontab -
    echo "🗑️  Entrada anterior removida"
fi

# Agregar nueva entrada de cron
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

if crontab -l 2>/dev/null | grep -q "$SCRIPT_PATH"; then
    echo "✅ Tarea cron configurada exitosamente"
    echo ""
    echo "📋 Configuración activa:"
    crontab -l 2>/dev/null | grep "$SCRIPT_PATH"
    echo ""
    echo "🎯 El autocommit se ejecutará:"
    echo "   - Cada 2 horas automáticamente"
    echo "   - Logs en: $LOG_FILE"
    echo "   - Para ejecutar manualmente: $SCRIPT_PATH"
    echo ""
    echo "🔧 Comandos útiles:"
    echo "   - Ver cron activo: crontab -l"
    echo "   - Editar cron: crontab -e"
    echo "   - Ver logs: tail -f $LOG_FILE"
    echo "   - Remover autocommit: crontab -l | grep -v autocommit.sh | crontab -"
else
    echo "❌ ERROR: No se pudo configurar la tarea cron"
    exit 1
fi

echo ""
echo "🚀 ¡Autocommit configurado y listo!"
