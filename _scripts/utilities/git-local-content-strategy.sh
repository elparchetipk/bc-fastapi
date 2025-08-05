#!/bin/bash
# git-local-content-strategy.sh
# Estrategia para manejar contenido local que no debe ir a GitHub

echo "🔐 Estrategias para Contenido Local + Trazabilidad Git"
echo "======================================================"

echo ""
echo "📋 OPCIÓN 1: .gitignore (YA IMPLEMENTADA)"
echo "✅ Carpeta _docs/video-scripts/ ahora oculta en GitHub"
echo "✅ Git local sigue rastreando cambios normalmente"
echo "✅ Colaboradores no ven contenido sensible"

echo ""
echo "📋 OPCIÓN 2: Rama Local Privada (Si necesitas más seguridad)"
echo "# Crear rama solo para contenido local"
echo "git checkout -b local-content"
echo "git add _docs/video-scripts/"
echo "git commit -m 'Add local video scripts'"
echo ""
echo "# Volver a main sin el contenido sensible"
echo "git checkout main"
echo "# El contenido queda solo en la rama local-content"

echo ""
echo "📋 OPCIÓN 3: Git Submodule Privado"
echo "# Para proyectos grandes con mucho contenido sensible"
echo "git submodule add https://github.com/tu-usuario/bc-fastapi-private _private"
echo "echo '_private/' >> .gitignore"

echo ""
echo "📋 OPCIÓN 4: Git Hooks para Filtrado Automático"
echo "# Avanzado - filtra automáticamente antes de push"
echo "# Útil para equipos grandes"

echo ""
echo "🎯 RECOMENDACIÓN PARA TU CASO:"
echo "✅ Usar .gitignore (ya implementado)"
echo "✅ Simple, efectivo, y fácil de mantener"
echo "✅ Perfecto para scripts de video y contenido educativo privado"

echo ""
echo "🔍 VERIFICAR CONFIGURACIÓN ACTUAL:"
git status --ignored | grep -A 10 "Archivos ignorados"

echo ""
echo "✅ Tu configuración actual es ideal para el bootcamp bc-fastapi"
