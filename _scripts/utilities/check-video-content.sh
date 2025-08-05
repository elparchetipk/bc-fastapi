#!/bin/bash
# Script para verificar que el contenido de video-bc_channel está disponible localmente
# pero siendo ignorado por GitHub

echo "🔍 Verificando estado de _docs/video-bc_channel/"
echo "=================================================="

# Verificar que la carpeta existe localmente
if [ -d "_docs/video-bc_channel" ]; then
    echo "✅ Carpeta _docs/video-bc_channel/ existe localmente"
    
    # Contar archivos
    file_count=$(find _docs/video-bc_channel -type f | wc -l)
    echo "📁 Total de archivos encontrados: $file_count"
    
    # Mostrar estructura
    echo ""
    echo "📂 Estructura de carpetas:"
    find _docs/video-bc_channel -type d | sort
    
    echo ""
    echo "📄 Archivos principales:"
    find _docs/video-bc_channel -name "*.md" -o -name "*.json" -o -name "*.sh" | sort
    
else
    echo "❌ ERROR: Carpeta _docs/video-bc_channel/ no encontrada"
    exit 1
fi

echo ""
echo "🚫 Verificando que está siendo ignorada por git..."

# Verificar que está siendo ignorada por git
if git check-ignore _docs/video-bc_channel/ > /dev/null 2>&1; then
    echo "✅ _docs/video-bc_channel/ está siendo ignorada por git"
    
    # Mostrar la regla específica que la ignora
    ignore_rule=$(git check-ignore -v _docs/video-bc_channel/ 2>/dev/null | cut -d':' -f2-)
    echo "📋 Regla aplicada: $ignore_rule"
else
    echo "⚠️  ADVERTENCIA: _docs/video-bc_channel/ NO está siendo ignorada por git"
    echo "   Esto podría causar que se suba accidentalmente a GitHub"
fi

echo ""
echo "✨ Verificación completada"
echo "👍 Los archivos de grabación están disponibles localmente pero privados en GitHub"
