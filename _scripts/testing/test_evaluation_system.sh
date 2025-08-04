#!/bin/bash
# test_evaluation_system.sh
# Script para probar el sistema de evaluación bc-fastapi

set -e

echo "🧪 TESTING - Sistema de Evaluación bc-fastapi"
echo "=============================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funciones de utilidad
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Test 1: Verificar estructura de archivos
echo ""
echo "📁 Test 1: Verificando estructura de archivos..."

if [ -f ".github/workflows/bc-fastapi-evaluation-final.yml" ]; then
    print_success "GitHub Action encontrado"
else
    print_error "GitHub Action no encontrado en .github/workflows/"
    exit 1
fi

if [ -f "_scripts/evaluation-system/bc_fastapi_evaluator.py" ]; then
    print_success "Script evaluador encontrado"
else
    print_error "Script evaluador no encontrado en _scripts/evaluation-system/"
    exit 1
fi

# Test 2: Verificar sintaxis del workflow
echo ""
echo "📋 Test 2: Verificando sintaxis del workflow..."

# Verifica que no hay problemas básicos de YAML
if python3 -c "import yaml; yaml.safe_load(open('.github/workflows/bc-fastapi-evaluation-final.yml'))" 2>/dev/null; then
    print_success "Sintaxis YAML válida"
else
    print_error "Problema de sintaxis en el workflow YAML"
    exit 1
fi

# Test 3: Verificar script Python
echo ""
echo "🐍 Test 3: Verificando script Python..."

if python3 -m py_compile _scripts/evaluation-system/bc_fastapi_evaluator.py; then
    print_success "Script Python compila correctamente"
else
    print_error "Errores de sintaxis en el script Python"
    exit 1
fi

# Test 4: Crear repositorio de prueba
echo ""
echo "📦 Test 4: Creando repositorio de prueba..."

TEST_DIR="test_student_repo"
rm -rf $TEST_DIR
mkdir -p $TEST_DIR

# Crear código Python de prueba
cat > $TEST_DIR/main.py << 'EOF'
from fastapi import FastAPI

app = FastAPI(title="Test API")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/test")
def get_test():
    return {"test": True}

@app.post("/items")
def create_item(item: dict):
    return {"item": item}

def helper_function():
    """Función auxiliar para testing"""
    return "helper"

class TestClass:
    """Clase de prueba"""
    def __init__(self):
        self.value = 42
EOF

# Crear archivo de test
cat > $TEST_DIR/test_main.py << 'EOF'
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
EOF

print_success "Repositorio de prueba creado en $TEST_DIR"

# Test 5: Ejecutar evaluador en repositorio de prueba
echo ""
echo "🔍 Test 5: Ejecutando evaluador en repositorio de prueba..."

# Copiar el repositorio de prueba como student-repo
cp -r $TEST_DIR student-repo

# Ejecutar el evaluador
export STUDENT_NAME="TestStudent"
export WEEK_NUMBER="5"

if python3 _scripts/evaluation-system/bc_fastapi_evaluator.py; then
    print_success "Evaluador ejecutado exitosamente"
else
    print_error "Error ejecutando el evaluador"
    exit 1
fi

# Test 6: Verificar resultados
echo ""
echo "📊 Test 6: Verificando resultados generados..."

if [ -f "evaluation_report.md" ]; then
    print_success "Reporte de evaluación generado"
    
    # Verificar contenido básico del reporte
    if grep -q "TestStudent" evaluation_report.md; then
        print_success "Nombre del estudiante en el reporte"
    else
        print_warning "Nombre del estudiante no encontrado en el reporte"
    fi
    
    if grep -q "Calificación:" evaluation_report.md; then
        SCORE=$(grep "Calificación:" evaluation_report.md | head -1)
        print_success "Puntuación encontrada: $(echo $SCORE | cut -d':' -f2)"
    else
        print_warning "Puntuación no encontrada en el reporte"
    fi
else
    print_error "Reporte de evaluación no generado"
    exit 1
fi

if [ -f "analysis_result.json" ]; then
    print_success "Análisis JSON generado"
    
    # Verificar contenido del JSON
    if python3 -c "import json; data=json.load(open('analysis_result.json')); print(f'Archivos: {len(data[\"files_analyzed\"])}, FastAPI: {data[\"fastapi_usage\"]}, Score: {data.get(\"evaluation_score\", \"N/A\")}')" 2>/dev/null; then
        print_success "Análisis JSON válido y con datos"
    else
        print_warning "Problema leyendo el análisis JSON"
    fi
else
    print_error "Análisis JSON no generado"
    exit 1
fi

# Test 7: Cleanup y mostrar resultados
echo ""
echo "🧹 Test 7: Limpieza y resultados finales..."

echo ""
echo "📋 MUESTRA DEL REPORTE GENERADO:"
echo "================================"
head -20 evaluation_report.md
echo "..."
echo "(Ver evaluation_report.md para el reporte completo)"

# Limpieza opcional (comentado para revisión)
# rm -rf $TEST_DIR student-repo
# rm -f evaluation_report.md analysis_result.json

print_success "Archivos de prueba mantenidos para revisión"

echo ""
echo "🎉 TODOS LOS TESTS COMPLETADOS EXITOSAMENTE"
echo "============================================"
echo "✅ Estructura de archivos correcta"
echo "✅ Sintaxis YAML válida"
echo "✅ Script Python funcional"
echo "✅ Evaluación ejecutada correctamente"
echo "✅ Reportes generados adecuadamente"
echo ""
echo "🔗 El sistema está listo para usar en producción"
echo "📚 Ver _docs/evaluation-system/README.md para instrucciones completas"
echo ""
echo "📁 Archivos generados para revisión:"
echo "   - evaluation_report.md (reporte completo)"
echo "   - analysis_result.json (datos técnicos)"
echo "   - test_student_repo/ (código de prueba)"
