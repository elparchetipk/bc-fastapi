# Environment Setup Guide - Bootcamp bc-fastapi

## 🎯 Objetivo

Establecer un entorno de desarrollo consistente y profesional para todos los aprendices del bootcamp, garantizando que cada herramienta esté configurada según las mejores prácticas de la industria.

## 📋 Prerrequisitos del Sistema

### Sistema Operativo

- **Linux**: Ubuntu 20.04+ (recomendado)
- **macOS**: 11.0+ (Big Sur o superior)
- **Windows**: Windows 10/11 con WSL2 configurado

### Hardware Mínimo

- **RAM**: 8GB (16GB recomendado)
- **Almacenamiento**: 50GB libres
- **Procesador**: Dual-core 2.5GHz+

## 🐍 Python Setup

### Instalación de Python 3.11+

#### Ubuntu/Debian

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.11
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip

# Verificar instalación
python3.11 --version
```

#### macOS

```bash
# Usando Homebrew (recomendado)
brew install python@3.11

# Verificar instalación
python3.11 --version
```

#### Windows (WSL2)

```bash
# En WSL2 Ubuntu
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip
```

### Configuración de Virtual Environments

#### pyenv (Recomendado para gestión de versiones)

```bash
# Instalar pyenv
curl https://pyenv.run | bash

# Agregar a ~/.bashrc o ~/.zshrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc

# Reiniciar shell
exec "$SHELL"

# Instalar Python 3.11
pyenv install 3.11.4
pyenv global 3.11.4
```

#### venv (Alternativa built-in)

```bash
# Crear entorno virtual
python3.11 -m venv bootcamp-env

# Activar entorno (Linux/macOS)
source bootcamp-env/bin/activate

# Activar entorno (Windows)
bootcamp-env\Scripts\activate

# Verificar entorno activo
which python
python --version
```

## 🐳 Docker Setup

### Instalación de Docker

#### Ubuntu

```bash
# Remover versiones anteriores
sudo apt-get remove docker docker-engine docker.io containerd runc

# Instalar dependencias
sudo apt-get update
sudo apt-get install ca-certificates curl gnupg lsb-release

# Agregar GPG key oficial de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Configurar repositorio
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER
newgrp docker

# Verificar instalación
docker --version
docker compose version
```

#### macOS

```bash
# Descargar Docker Desktop desde https://www.docker.com/products/docker-desktop
# O usando Homebrew
brew install --cask docker

# Verificar instalación
docker --version
docker compose version
```

#### Windows

1. Instalar Docker Desktop para Windows
2. Habilitar WSL2 integration
3. Verificar en WSL2: `docker --version`

### Configuración Post-instalación

```bash
# Test de funcionamiento
docker run hello-world

# Verificar compose
docker compose version
```

## 🔧 Development Tools

### Visual Studio Code

#### Instalación

```bash
# Ubuntu
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code

# macOS
brew install --cask visual-studio-code

# Windows
# Descargar desde https://code.visualstudio.com/
```

#### Extensions Obligatorias

```bash
# Instalar extensions via CLI
code --install-extension ms-python.python
code --install-extension ms-python.black-formatter
code --install-extension ms-python.flake8
code --install-extension ms-python.mypy-type-checker
code --install-extension ms-vscode.vscode-json
code --install-extension redhat.vscode-yaml
code --install-extension ms-vscode.makefile-tools
code --install-extension GitHub.copilot
code --install-extension eamodio.gitlens
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-vscode-remote.remote-containers
```

#### VS Code Settings (settings.json)

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length=88"],
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.linting.mypyEnabled": true,
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/venv": true,
    "**/.env": true
  },
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter",
    "editor.rulers": [88],
    "editor.tabSize": 4
  },
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.tabSize": 2
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.tabSize": 2
  },
  "git.autofetch": true,
  "git.confirmSync": false,
  "terminal.integrated.defaultProfile.linux": "bash",
  "docker.showStartPage": false
}
```

### Git Configuration

#### Configuración Global

```bash
# Configuración básica
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
git config --global init.defaultBranch main

# Editor por defecto
git config --global core.editor "code --wait"

# Aliases útiles (introducir gradualmente)
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.last 'log -1 HEAD'
git config --global alias.unstage 'reset HEAD --'

# Configuración de merge
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd 'code --wait $MERGED'

# Configuración de diff
git config --global diff.tool vscode
git config --global difftool.vscode.cmd 'code --wait --diff $LOCAL $REMOTE'
```

#### SSH Keys Setup

```bash
# Generar SSH key
ssh-keygen -t ed25519 -C "tu.email@ejemplo.com"

# Agregar a ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Mostrar public key para agregar a GitHub
cat ~/.ssh/id_ed25519.pub

# Test de conexión
ssh -T git@github.com
```

## 📊 Database Setup

### PostgreSQL

#### Instalación Local

```bash
# Ubuntu
sudo apt update
sudo apt install postgresql postgresql-contrib

# macOS
brew install postgresql
brew services start postgresql

# Crear usuario y database
sudo -u postgres createuser --interactive bootcamp_user
sudo -u postgres createdb bootcamp_db -O bootcamp_user
```

#### Docker Compose para Desarrollo

```yaml
# docker-compose.dev.yml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: bootcamp_db
      POSTGRES_USER: bootcamp_user
      POSTGRES_PASSWORD: dev_password
    ports:
      - '5432:5432'
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -U bootcamp_user -d bootcamp_db']
      interval: 30s
      timeout: 10s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - '6379:6379'
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### SQLite (Desarrollo/Testing)

```bash
# SQLite viene incluido con Python
python -c "import sqlite3; print(sqlite3.version)"
```

## 🔧 Development Environment Variables

### Template .env

```bash
# .env.template
# Database
DATABASE_URL=postgresql://bootcamp_user:dev_password@localhost:5432/bootcamp_db
TEST_DATABASE_URL=sqlite:///./test.db

# Application
DEBUG=true
SECRET_KEY=your-secret-key-for-development
API_V1_STR=/api/v1

# External Services
REDIS_URL=redis://localhost:6379/0

# Security
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# CORS
ALLOWED_HOSTS=["localhost", "127.0.0.1"]
CORS_ORIGINS=["http://localhost:3000", "http://localhost:5173"]

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

### Gestión de Secrets

```bash
# Instalar python-dotenv
pip install python-dotenv

# Nunca commitear archivos .env reales
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
echo "!.env.template" >> .gitignore
```

## 🧪 Testing Tools Setup

### pytest Configuration

```bash
# Instalar herramientas de testing
pip install pytest pytest-cov pytest-asyncio pytest-mock httpx

# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --strict-markers
    --strict-config
    --cov=src
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-report=xml
    --cov-fail-under=80
asyncio_mode = auto
```

### Coverage Configuration

```bash
# .coveragerc
[run]
source = src
omit =
    */tests/*
    */venv/*
    */__pycache__/*
    */migrations/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## 🛠️ Quality Tools

### Linting and Formatting

```bash
# Instalar herramientas de calidad
pip install black flake8 mypy isort bandit safety

# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  migrations
  | venv
  | build
  | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 88
multi_line_output = 3

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

### Pre-commit Setup (Semana 5+)

```bash
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.3.0
    hooks:
      - id: mypy
```

## 📱 API Testing Tools

### Postman Setup

1. Descargar desde https://www.postman.com/downloads/
2. Crear workspace "Bootcamp FastAPI"
3. Configurar environment variables:
   - `base_url`: http://localhost:8000
   - `api_version`: /api/v1

### HTTPie (Alternativa CLI)

```bash
# Instalación
pip install httpie

# Uso básico
http GET localhost:8000/docs
http POST localhost:8000/api/v1/users name="John Doe" email="john@example.com"
```

## 🔍 Verification Script

```bash
#!/bin/bash
# verify-setup.sh

echo "🔍 Verificando configuración del entorno..."

# Python
echo "📍 Python:"
python --version || echo "❌ Python no encontrado"

# Virtual environment
echo "📍 Virtual environment:"
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Virtual environment activo: $VIRTUAL_ENV"
else
    echo "⚠️ No hay virtual environment activo"
fi

# Docker
echo "📍 Docker:"
docker --version || echo "❌ Docker no encontrado"
docker compose version || echo "❌ Docker Compose no encontrado"

# Git
echo "📍 Git:"
git --version || echo "❌ Git no encontrado"
git config user.name || echo "⚠️ Git user.name no configurado"
git config user.email || echo "⚠️ Git user.email no configurado"

# VS Code
echo "📍 VS Code:"
code --version || echo "❌ VS Code no encontrado"

# Python packages
echo "📍 Python packages:"
pip list | grep -E "(fastapi|uvicorn|pytest|black|flake8)" || echo "⚠️ Packages faltantes"

# Database
echo "📍 Database:"
psql --version || echo "⚠️ PostgreSQL no encontrado (opcional para desarrollo local)"

echo "✅ Verificación completada"
```

## 🎯 Checklist de Setup Completo

### Básico (Semana 1)

- [ ] Python 3.11+ instalado y configurado
- [ ] Virtual environment creado y activo
- [ ] Git configurado con user.name y user.email
- [ ] VS Code instalado con extensions básicas
- [ ] SSH keys configuradas para GitHub
- [ ] Repositorio personal creado y clonado

### Intermedio (Semana 2-3)

- [ ] Docker y Docker Compose funcionando
- [ ] PostgreSQL configurado (local o Docker)
- [ ] Herramientas de testing instaladas
- [ ] Linting tools configurados
- [ ] Environment variables template configurado

### Avanzado (Semana 4+)

- [ ] Pre-commit hooks configurados
- [ ] CI/CD básico funcionando
- [ ] Postman/HTTPie configurado
- [ ] Monitoring tools setup
- [ ] Security scanning tools activos

## 🚨 Troubleshooting Común

### Python Issues

```bash
# ModuleNotFoundError
pip install --upgrade pip
pip install -r requirements.txt

# Permission errors
sudo chown -R $USER:$USER ~/.local
```

### Docker Issues

```bash
# Permission denied
sudo usermod -aG docker $USER
newgrp docker

# Port already in use
docker ps
docker stop $(docker ps -q)
```

### Git Issues

```bash
# SSH problems
ssh -T git@github.com
ssh-add ~/.ssh/id_ed25519

# Credential issues
git config --global credential.helper store
```

## 📚 Recursos Adicionales

- [Python Official Documentation](https://docs.python.org/3.11/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Git Documentation](https://git-scm.com/doc)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)

**Nota importante**: Esta configuración debe completarse antes de la primera semana del bootcamp. Cualquier problema debe resolverse durante la sesión de setup inicial.
