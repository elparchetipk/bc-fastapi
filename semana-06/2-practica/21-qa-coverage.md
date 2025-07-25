# Práctica 21: Quality Assurance y Coverage

## Objetivos de Aprendizaje

- Implementar herramientas de calidad de código (linting, formateo)
- Configurar y analizar cobertura de tests
- Establecer métricas de calidad para el proyecto
- Integrar QA en el workflow de desarrollo

## Duración Estimada

⏱️ **90 minutos**

## Prerrequisitos

- Práctica 19: Configuración de pytest completada
- Práctica 20: Tests unitarios e integración completados
- Entendimiento básico de linting y formateo de código

---

## 📋 Contenido de la Práctica

### Parte 1: Configuración de Herramientas de QA (30 min)

#### 1.1 Instalación de Herramientas de Calidad

**Paso 1: Actualizar requirements-dev.txt**

```bash
# Agregar nuevas dependencias de desarrollo
echo "# Quality Assurance tools" >> requirements-dev.txt
echo "black>=23.0.0" >> requirements-dev.txt
echo "isort>=5.12.0" >> requirements-dev.txt
echo "flake8>=6.0.0" >> requirements-dev.txt
echo "mypy>=1.5.0" >> requirements-dev.txt
echo "pytest-cov>=4.1.0" >> requirements-dev.txt
echo "coverage[toml]>=7.3.0" >> requirements-dev.txt
```

**Paso 2: Instalar dependencias**

```bash
pip install -r requirements-dev.txt
```

#### 1.2 Configuración de Black (Formateo)

**Crear pyproject.toml**

```toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | \.env
  | venv
  | env
  | __pycache__
  | \.pytest_cache
  | migrations
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
ensure_newline_before_comments = true

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
ignore_missing_imports = true
exclude = [
    "migrations/",
    "venv/",
    ".venv/",
]

[tool.coverage.run]
source = ["app"]
omit = [
    "*/migrations/*",
    "*/venv/*",
    "*/.venv/*",
    "*/tests/*",
    "*/test_*",
]

[tool.coverage.report]
precision = 2
show_missing = true
skip_covered = false
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if self.debug:",
    "if settings.DEBUG",
    "raise AssertionError",
    "raise NotImplementedError",
    "if 0:",
    "if __name__ == .__main__.:",
    "class .*\bProtocol\):",
    "@(abc\.)?abstractmethod",
]

[tool.coverage.html]
directory = "htmlcov"
```

#### 1.3 Configuración de Flake8

**Crear .flake8**

```ini
[flake8]
max-line-length = 88
extend-ignore = E203, E266, E501, W503, F403, F401
max-complexity = 10
select = B,C,E,F,W,T4,B9
exclude =
    .git,
    __pycache__,
    .venv,
    venv,
    env,
    migrations,
    .pytest_cache
```

### Parte 2: Implementación de Coverage (25 min)

#### 2.1 Configuración de pytest-cov

**Actualizar pytest.ini**

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --tb=short
    --strict-config
    --strict-markers
    --cov=app
    --cov-report=term-missing
    --cov-report=html
    --cov-report=xml
    --cov-fail-under=80
markers =
    unit: marks tests as unit tests
    integration: marks tests as integration tests
    slow: marks tests as slow running
```

#### 2.2 Script de Coverage

**Crear scripts/coverage.sh**

```bash
#!/bin/bash

echo "🔍 Ejecutando análisis de cobertura..."

# Limpiar resultados anteriores
rm -rf htmlcov/
rm -f .coverage

# Ejecutar tests con coverage
pytest --cov=app \
       --cov-report=html \
       --cov-report=term-missing \
       --cov-report=xml \
       --cov-fail-under=80

# Verificar si se generó el reporte
if [ -d "htmlcov" ]; then
    echo "✅ Reporte HTML generado en htmlcov/"
    echo "🌐 Abrir htmlcov/index.html en el navegador"
else
    echo "❌ Error generando reporte de cobertura"
    exit 1
fi

# Mostrar resumen
echo ""
echo "📊 Resumen de cobertura:"
coverage report --show-missing
```

**Hacer ejecutable:**

```bash
chmod +x scripts/coverage.sh
```

### Parte 3: Análisis de Calidad (35 min)

#### 3.1 Script de Quality Check

**Crear scripts/quality_check.sh**

```bash
#!/bin/bash

echo "🚀 Iniciando análisis de calidad de código..."

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Función para verificar resultado
check_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2 - OK${NC}"
        return 0
    else
        echo -e "${RED}❌ $2 - FAILED${NC}"
        return 1
    fi
}

# Contador de errores
ERRORS=0

echo "1️⃣ Verificando formato con Black..."
black --check --diff app/
check_result $? "Black formatting"
if [ $? -ne 0 ]; then ((ERRORS++)); fi

echo ""
echo "2️⃣ Verificando imports con isort..."
isort --check-only --diff app/
check_result $? "Import sorting"
if [ $? -ne 0 ]; then ((ERRORS++)); fi

echo ""
echo "3️⃣ Verificando estilo con Flake8..."
flake8 app/
check_result $? "Code style (Flake8)"
if [ $? -ne 0 ]; then ((ERRORS++)); fi

echo ""
echo "4️⃣ Verificando tipos con MyPy..."
mypy app/
check_result $? "Type checking (MyPy)"
if [ $? -ne 0 ]; then ((ERRORS++)); fi

echo ""
echo "5️⃣ Ejecutando tests con cobertura..."
pytest --cov=app --cov-fail-under=80 -q
check_result $? "Tests and coverage"
if [ $? -ne 0 ]; then ((ERRORS++)); fi

echo ""
echo "📊 RESUMEN FINAL:"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}🎉 ¡Todos los checks pasaron! Código listo.${NC}"
    exit 0
else
    echo -e "${RED}💥 $ERRORS errores encontrados. Revisar y corregir.${NC}"
    exit 1
fi
```

**Hacer ejecutable:**

```bash
chmod +x scripts/quality_check.sh
```

#### 3.2 Integración con VSCode

**Crear .vscode/settings.json**

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=88"],
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.linting.pylintEnabled": false,
  "python.sortImports.args": ["--profile", "black"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.pytestArgs": ["tests", "-v"],
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/htmlcov": true,
    "**/.coverage": true
  }
}
```

#### 3.3 Pre-commit Hooks (Opcional)

**Instalar pre-commit:**

```bash
pip install pre-commit
```

**Crear .pre-commit-config.yaml**

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.9.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort
        args: ['--profile', 'black']

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

**Instalar hooks:**

```bash
pre-commit install
```

---

## 🛠️ Ejercicios Prácticos

### Ejercicio 1: Aplicar Formateo y Linting

**Objetivo:** Limpiar y formatear el código existente

```bash
# 1. Formatear código con Black
black app/

# 2. Organizar imports con isort
isort app/

# 3. Verificar estilo con Flake8
flake8 app/

# 4. Verificar tipos con MyPy
mypy app/
```

### Ejercicio 2: Analizar Cobertura

**Objetivo:** Generar y analizar reporte de cobertura

```bash
# Ejecutar coverage
./scripts/coverage.sh

# Analizar resultados en htmlcov/index.html
# Identificar líneas no cubiertas
# Agregar tests para mejorar cobertura
```

### Ejercicio 3: Configurar CI/CD básico

**Crear .github/workflows/quality.yml**

```yaml
name: Quality Assurance

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Run quality checks
        run: ./scripts/quality_check.sh

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

---

## 📈 Métricas de Calidad

### Métricas Objetivo

| Métrica                 | Objetivo | Herramienta |
| ----------------------- | -------- | ----------- |
| Cobertura de código     | ≥ 80%    | pytest-cov  |
| Complejidad ciclomática | ≤ 10     | flake8      |
| Líneas por función      | ≤ 50     | flake8      |
| Errores de estilo       | 0        | flake8      |
| Errores de tipo         | 0        | mypy        |
| Formateo consistente    | 100%     | black       |

### Dashboard de Calidad

**Crear scripts/quality_report.py**

```python
#!/usr/bin/env python3

import subprocess
import json
from datetime import datetime

def run_command(cmd):
    """Ejecutar comando y capturar output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def generate_quality_report():
    """Generar reporte de calidad."""
    report = {
        "timestamp": datetime.now().isoformat(),
        "metrics": {}
    }

    # Coverage
    success, stdout, stderr = run_command("coverage report --format=json")
    if success:
        coverage_data = json.loads(stdout)
        report["metrics"]["coverage"] = {
            "percentage": coverage_data["totals"]["percent_covered"],
            "lines_covered": coverage_data["totals"]["covered_lines"],
            "lines_total": coverage_data["totals"]["num_statements"]
        }

    # Flake8
    success, stdout, stderr = run_command("flake8 app/ --format=json")
    flake8_issues = len(stdout.split('\n')) if stdout else 0
    report["metrics"]["style_issues"] = flake8_issues

    # MyPy
    success, stdout, stderr = run_command("mypy app/ --json-report mypy_report")
    report["metrics"]["type_errors"] = 0 if success else 1

    # Tests
    success, stdout, stderr = run_command("pytest --collect-only -q")
    if success:
        test_count = stdout.count("test session starts")
        report["metrics"]["test_count"] = test_count

    return report

if __name__ == "__main__":
    report = generate_quality_report()
    print(json.dumps(report, indent=2))
```

---

## ✅ Criterios de Evaluación

### Nivel Básico (60-70%)

- [ ] Configura Black y isort correctamente
- [ ] Ejecuta análisis de cobertura básico
- [ ] Identifica líneas no cubiertas por tests

### Nivel Intermedio (71-85%)

- [ ] Configura todas las herramientas de QA
- [ ] Genera reportes de cobertura HTML
- [ ] Configura VSCode para formateo automático
- [ ] Alcanza 70%+ de cobertura de código

### Nivel Avanzado (86-100%)

- [ ] Implementa pipeline completo de QA
- [ ] Configura pre-commit hooks
- [ ] Alcanza 80%+ de cobertura de código
- [ ] Crea scripts automatizados de calidad
- [ ] Configura CI/CD con checks de calidad

---

## 📚 Recursos Adicionales

### Documentación

- [Black Documentation](https://black.readthedocs.io/)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [MyPy Documentation](https://mypy.readthedocs.io/)

### Herramientas Adicionales

- **bandit**: Análisis de seguridad
- **safety**: Verificación de vulnerabilidades
- **vulture**: Detección de código muerto
- **radon**: Métricas de complejidad

### Mejores Prácticas

1. **Automatización**: Integrar QA en el workflow
2. **Métricas**: Establecer objetivos claros
3. **Feedback**: Reportes claros y accionables
4. **Evolución**: Mejorar métricas gradualmente

---

## 🎯 Próximos Pasos

1. **Aplicar formateo** a todo el código existente
2. **Configurar coverage** y generar primer reporte
3. **Establecer métricas** objetivo para el proyecto
4. **Integrar QA** en el workflow de desarrollo
5. **Preparar CI/CD** para checks automáticos

---

_Esta práctica es fundamental para mantener código limpio, consistente y de alta calidad. La inversión en QA se traduce en menos bugs, mayor mantenibilidad y mejor colaboración en equipo._
