# Estrategia Git/GitHub y CI/CD - Bootcamp bc-fastapi

## 🎯 Filosofía: "Primero Picapiedra, Luego Altamente Productivo"

### Principio Fundamental

**TODOS los entregables deben ser exclusivamente a través de GitHub**. Los aprendices desarrollarán competencias profesionales en control de versiones y CI/CD desde el primer día.

## 📋 Progresión por Semanas

### 🪨 **SEMANA 1-2: Fundamentos "Picapiedra"**

#### Objetivos

- Establecer disciplina manual en Git
- Crear músculo memoria en comandos básicos
- Entender el flujo fundamental antes de automatizar

#### Prácticas Obligatorias

```bash
# Workflow básico MANUAL (sin shortcuts)
git status
git add .
git commit -m "Add user authentication endpoint"
git push origin main
```

#### Convenciones Estrictas desde Día 1

- **Commits descriptivos en inglés**: Tiempo presente, específicos
- **Branches con nombres claros**: `feature/user-auth`, `fix/database-connection`
- **Pull Requests obligatorios**: Aunque trabajen solos
- **Code reviews**: Entre compañeros desde la primera semana

#### Entregables Semana 1-2

- ✅ Repositorio personal configurado
- ✅ README.md con setup instructions
- ✅ Commits diarios con progreso
- ✅ Al menos 1 Pull Request con review
- ✅ Issues creados para track de tareas

### ⚡ **SEMANA 3-4: Introducción a Automation**

#### Nuevas Herramientas

```bash
# Git aliases básicos
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.st status

# Conventional commits (manual todavía)
git commit -m "feat: add user authentication"
git commit -m "fix: resolve database connection timeout"
git commit -m "docs: update API documentation"
```

#### GitHub Actions Básico

```yaml
# .github/workflows/basic-ci.yml
name: Basic CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

#### Entregables Semana 3-4

- ✅ CI básico funcionando
- ✅ Conventional commits aplicados
- ✅ Branch protection rules configuradas
- ✅ Tests automáticos en cada push

### 🚀 **SEMANA 5-6: Automatización Intermedia**

#### Git Hooks Locales

```bash
# pre-commit hook básico
#!/bin/sh
# Ejecutar tests antes de commit
pytest
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

#### Better Commits con Templates

```bash
# .gitmessage template
# <type>(<scope>): <subject>
#
# <body>
#
# <footer>

# Example:
# feat(auth): add JWT authentication
#
# Implements user authentication using JWT tokens
# with refresh mechanism and role-based access
#
# Closes #123
```

#### Entregables Semana 5-6

- ✅ Pre-commit hooks configurados
- ✅ Commit message templates
- ✅ Linting automático (flake8, black)
- ✅ Code coverage reports

### 🎯 **SEMANA 7-8: Automatización Avanzada**

#### Auto-commit para Desarrollo (CON CUIDADO)

```bash
# Script para auto-commits de trabajo en progreso
#!/bin/bash
# auto-wip.sh - Solo para desarrollo, NUNCA para producción

while true; do
    if [[ `git status --porcelain` ]]; then
        git add .
        git commit -m "wip: auto-save $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    sleep 300  # cada 5 minutos
done
```

#### Cron Jobs para Maintenance

```bash
# Crontab entry para cleanup automático
0 2 * * * cd /path/to/project && git gc --prune=now
0 3 * * 1 cd /path/to/project && git remote prune origin
```

#### Entregables Semana 7-8

- ✅ Auto-commit script (solo para WIP)
- ✅ Automated dependency updates
- ✅ Security scanning en CI
- ✅ Performance testing automático

### 🏆 **SEMANA 9-12: Productividad Máxima**

#### Herramientas Avanzadas

```bash
# Commitizen para commits consistentes
npm install -g commitizen
npm install -g cz-conventional-changelog

# Husky para git hooks automáticos
npm install --save-dev husky
npx husky install
npx husky add .husky/pre-commit "npm test"
npx husky add .husky/commit-msg "npx commitlint --edit $1"
```

#### CI/CD Completo

```yaml
# .github/workflows/complete-cicd.yml
name: Complete CI/CD
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Lint
        run: |
          flake8 src/
          black --check src/
          mypy src/
      - name: Test
        run: |
          pytest --cov=src/ --cov-report=xml
      - name: Security scan
        run: bandit -r src/
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  build:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t app:${{ github.sha }} .
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker push app:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - name: Deploy to staging
        run: echo "Deploying app:${{ github.sha }} to staging"
```

## 📚 Documentación Requerida por Semana

### Semana 1-2: Git Fundamentals

```markdown
# README.md obligatorio

## Setup Instructions

## How to Run

## How to Test

## How to Contribute

# CONTRIBUTING.md básico

## Git Workflow

## Commit Conventions

## PR Process
```

### Semana 3-4: CI/CD Basics

```markdown
# .github/workflows/ documentation

## CI Pipeline Description

## How to Add Tests

## Branch Protection Rules

# docs/git-workflow.md

## Branching Strategy

## Code Review Process

## Merge Policies
```

### Semana 5-6: Advanced Git

```markdown
# docs/development-setup.md

## Git Hooks Configuration

## Pre-commit Setup

## Local Development Tools

# docs/testing-strategy.md

## Test Types and Coverage

## Automated Testing

## Quality Gates
```

### Semana 7-12: Production Ready

```markdown
# docs/deployment.md

## CI/CD Pipeline Architecture

## Environment Management

## Rollback Procedures

# docs/monitoring.md

## Application Monitoring

## Performance Metrics

## Alert Configuration
```

## 🎯 Criterios de Evaluación por Semana

### Semana 1-2 (Fundamentos)

- **Git History Limpio** (20%): Commits descriptivos y frecuentes
- **README Quality** (30%): Documentación clara y completa
- **PR Process** (25%): Pull requests con descriptions apropiadas
- **Code Organization** (25%): Estructura de proyecto profesional

### Semana 3-4 (CI/CD Básico)

- **Pipeline Functionality** (40%): CI/CD funcionando correctamente
- **Test Coverage** (30%): Tests automáticos implementados
- **Branch Protection** (15%): Rules configuradas apropiadamente
- **Documentation** (15%): Workflow documentado

### Semana 5-6 (Automatización)

- **Git Hooks** (25%): Pre-commit hooks funcionando
- **Code Quality** (35%): Linting y formatting automático
- **Commit Quality** (20%): Conventional commits aplicados
- **Tool Integration** (20%): Herramientas integradas correctamente

### Semana 7-12 (Productividad)

- **Full Pipeline** (30%): CI/CD completo y robusto
- **Automation Level** (25%): Nivel apropiado de automatización
- **Production Readiness** (25%): Deployment ready code
- **Best Practices** (20%): Aplicación consistente de mejores prácticas

## ⚠️ Reglas Estrictas

### Prohibiciones Absolutas

- ❌ **No commits directos a main** (excepto setup inicial)
- ❌ **No auto-commits en producción** (solo para WIP local)
- ❌ **No bypassing CI checks**
- ❌ **No commits sin descripción**

### Obligaciones Diarias

- ✅ **Commit diario mínimo** con progreso
- ✅ **Status updates en issues/PRs**
- ✅ **Code review participation**
- ✅ **Documentation updates**

## 🚀 Herramientas de Productividad (Introducción Gradual)

### Semana 1-4: Manual Básico

```bash
# Solo comandos básicos
git add, commit, push, pull, merge
```

### Semana 5-8: Semi-automatizado

```bash
# Git aliases y scripts simples
git config --global alias.acp '!git add . && git commit -m "$1" && git push'
```

### Semana 9-12: Altamente Productivo

```bash
# Herramientas avanzadas
- Commitizen
- Husky
- Lint-staged
- Conventional changelog
- Automated dependency updates
```

## 📊 Métricas de Seguimiento

### KPIs por Aprendiz

- **Commit Frequency**: Commits por día
- **PR Quality**: Tiempo de review y merge
- **CI Success Rate**: Porcentaje de builds exitosos
- **Code Coverage**: Tendencia de coverage
- **Review Participation**: PRs reviewed vs created

### Dashboards

- **GitHub Insights**: Activity overview
- **CI/CD Metrics**: Build times y success rates
- **Code Quality**: SonarQube metrics
- **Team Collaboration**: PR interactions

## 🎓 Beneficios Educativos

### Competencias Desarrolladas

- **Version Control Mastery**: Git workflow profesional
- **Collaboration Skills**: Code review y team work
- **Quality Assurance**: Testing y CI/CD
- **Production Mindset**: Deployment y monitoring

### Preparación Profesional

- **Industry Standards**: Herramientas y procesos reales
- **Portfolio Building**: Historial visible en GitHub
- **Best Practices**: Desde el primer día
- **Continuous Learning**: Evolución gradual de herramientas

## 🔄 Evolución Continua

La estrategia evoluciona basada en:

- **Feedback de aprendices**: Adaptación a necesidades
- **Industry trends**: Nuevas herramientas y prácticas
- **Performance metrics**: Optimización basada en datos
- **Instructor insights**: Mejoras pedagógicas

**Recordatorio**: La clave está en la progresión gradual - primero dominar lo manual, luego automatizar inteligentemente.
