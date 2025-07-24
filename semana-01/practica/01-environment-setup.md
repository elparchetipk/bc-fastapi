# Práctica 1: Configuración Rápida del Entorno

## 🎯 Objetivo

Configurar el entorno mínimo necesario para desarrollar con FastAPI en solo 90 minutos, enfocándonos en lo esencial.

## ⏱️ Tiempo Estimado: 90 minutos (incluye buffer para problemas)

## 📋 Pre-requisitos

- Python 3.8+ ya instalado (verificar con `python3 --version`)
- Conexión a internet estable
- Cuenta de GitHub activa
- Editor de código (VS Code recomendado)

## 🚀 Setup Rápido (3 pasos esenciales)

### Paso 1: Verificar Python (5 min)

```bash
# Verificar versión de Python
python3 --version
# Debe mostrar Python 3.8 o superior

# Verificar pip
python3 -m pip --version

# Si no tienes Python 3.8+, usar versión del sistema
# NOTA: Para Semana 2 configuraremos pyenv profesional
```

### Paso 2: Crear Proyecto FastAPI (15 min)

```bash
# Crear directorio del proyecto
mkdir mi-primera-api
cd mi-primera-api

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Actualizar pip
pip install --upgrade pip

# Instalar FastAPI y Uvicorn
pip install "fastapi[all]" uvicorn

# Verificar instalación
pip list | grep fastapi
pip list | grep uvicorn
```

### Paso 3: Configuración Git Básica (10 min)

```bash
# Configurar Git globalmente (solo primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"

# Inicializar repositorio
git init

# Crear .gitignore básico
cat > .gitignore << EOF
# Entorno virtual
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
pip-log.txt
pip-delete-this-directory.txt
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
EOF

# Primer commit
git add .gitignore
git commit -m "feat: configuración inicial del proyecto"
```

## ✅ Verificación del Setup (5 min)

Crear un archivo de prueba para verificar que todo funciona:

```bash
# Crear archivo de prueba
cat > test_setup.py << EOF
#!/usr/bin/env python3
"""
Verificación rápida del entorno FastAPI
"""

try:
    import fastapi
    import uvicorn
    print("✅ FastAPI instalado correctamente")
    print(f"   Versión FastAPI: {fastapi.__version__}")
    print(f"   Versión Uvicorn: {uvicorn.__version__}")

    # Crear API mínima de prueba
    from fastapi import FastAPI
    app = FastAPI()

    @app.get("/")
    def test():
        return {"mensaje": "¡Entorno configurado correctamente!"}

    print("✅ Setup completado - API de prueba creada")
    print("🚀 Para ejecutar: uvicorn test_setup:app --reload")

except ImportError as e:
    print("❌ Error en la instalación:")
    print(f"   {e}")
    print("💡 Intenta reinstalar: pip install 'fastapi[all]' uvicorn")

EOF

# Ejecutar verificación
python test_setup.py
```

## 🎯 Objetivos Cumplidos

Al finalizar este setup rápido, deberías tener:

- ✅ **Python 3.8+ funcionando**
- ✅ **Entorno virtual creado y activado**
- ✅ **FastAPI y Uvicorn instalados**
- ✅ **Git configurado básicamente**
- ✅ **Proyecto inicial listo para desarrollo**

## 🔄 Próximos Pasos

1. **Inmediato**: Proceder a crear tu primera API (Práctica 2)
2. **Semana 2**: Configuraremos herramientas avanzadas (pyenv, Docker)
3. **Semana 3**: Setup de testing y CI/CD

## 🆘 Problemas Comunes

### Python no encontrado

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip python3-venv

# macOS (con Homebrew)
brew install python3

# Windows
# Descargar desde python.org
```

### pip no funciona

```bash
# Reinstalar pip
python3 -m ensurepip --upgrade
python3 -m pip install --upgrade pip
```

### Entorno virtual no se activa

```bash
# Verificar que venv existe
ls -la venv/

# Recrear si es necesario
rm -rf venv
python3 -m venv venv
source venv/bin/activate
```

## 📝 Notas Importantes

- **Este es un setup mínimo**: En Semana 2 profundizaremos
- **No te preocupes por perfección**: Busca funcionalidad
- **Pide ayuda temprano**: No gastes más de 20 min en un problema
- **Documenta errores**: Ayudarán a mejorar el proceso

## 🎯 Tiempo Target vs Real

- **Setup Python**: 5 min target
- **Entorno virtual + FastAPI**: 15 min target
- **Git básico**: 10 min target
- **Verificación**: 5 min target
- **Buffer problemas**: 55 min disponibles

**Total: 90 min (realistas con troubleshooting)**
python --version # Debe mostrar Python 3.11.4
which python # Debe mostrar ruta de pyenv

````

**Windows (WSL2):**

```bash
# En WSL2, seguir los mismos pasos que Linux
# Asegurarse de que WSL2 esté configurado correctamente
wsl --version
````

#### ✅ Checkpoint 1: Verificación de Python

```bash
# Estos comandos deben ejecutarse sin errores
python --version
pip --version
python -c "import sys; print(f'Python path: {sys.executable}')"
```

### 2. Git Configuración Profesional

#### Configuración global básica

```bash
# Información personal (CAMBIAR POR TUS DATOS)
git config --global user.name "Tu Nombre Completo"
git config --global user.email "tu.email@ejemplo.com"

# Editor preferido (opcional)
git config --global core.editor "code --wait"  # VS Code
# git config --global core.editor "vim"        # Vim

# Configuraciones de calidad
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global push.default simple
git config --global core.autocrlf input  # Linux/macOS
# git config --global core.autocrlf true  # Windows
```

#### SSH Key para GitHub (Seguridad)

```bash
# Generar clave SSH (si no existe)
ssh-keygen -t ed25519 -C "tu.email@ejemplo.com"

# Agregar al ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Mostrar clave pública para agregar a GitHub
cat ~/.ssh/id_ed25519.pub
```

**📝 Acción requerida:**

1. Copiar la clave pública mostrada
2. Ir a GitHub.com → Settings → SSH and GPG keys → New SSH key
3. Pegar la clave y guardar

#### Verificar conexión SSH

```bash
ssh -T git@github.com
# Debe mostrar: "Hi username! You've successfully authenticated..."
```

#### ✅ Checkpoint 2: Verificación de Git

```bash
# Verificar configuración
git config --list --global

# Verificar conexión SSH con GitHub
ssh -T git@github.com
```

### 3. Entorno Virtual y Dependencias

#### Crear estructura del proyecto

```bash
# Crear directorio del proyecto
mkdir fastapi-bootcamp-w1
cd fastapi-bootcamp-w1

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Verificar que estamos en el entorno virtual
which python  # Debe mostrar ruta del venv
```

#### Instalar dependencias base

```bash
# Actualizar pip a la última versión
pip install --upgrade pip

# Instalar FastAPI y dependencias principales
pip install fastapi[all]==0.104.1
pip install uvicorn[standard]==0.24.0
pip install pydantic==2.4.2

# Dependencias de desarrollo
pip install pytest==7.4.3
pip install pytest-asyncio==0.21.1
pip install httpx==0.25.1
pip install black==23.10.1
pip install flake8==6.1.0
pip install mypy==1.6.1
pip install isort==5.12.0

# Generar requirements.txt
pip freeze > requirements.txt
```

#### ✅ Checkpoint 3: Verificación del entorno

```bash
# Verificar instalaciones
python -c "import fastapi; print(f'FastAPI version: {fastapi.__version__}')"
python -c "import uvicorn; print(f'Uvicorn version: {uvicorn.__version__}')"
python -c "import pydantic; print(f'Pydantic version: {pydantic.__version__}')"
```

### 4. Herramientas de Desarrollo Adicionales

#### Docker (Opcional pero recomendado)

```bash
# Verificar si Docker está instalado
docker --version

# Si no está instalado, seguir guías oficiales:
# Linux: https://docs.docker.com/engine/install/ubuntu/
# macOS: https://docs.docker.com/desktop/mac/install/
# Windows: https://docs.docker.com/desktop/windows/install/
```

#### Postman o Thunder Client

- **Postman:** Descargar desde https://www.postman.com/downloads/
- **Thunder Client:** Extensión para VS Code (más ligero)

#### ✅ Checkpoint 4: Verificación completa

```bash
# Verificar todas las herramientas
echo "=== VERIFICACIÓN COMPLETA ==="
echo "Python: $(python --version)"
echo "Pip: $(pip --version)"
echo "Git: $(git --version)"
echo "FastAPI instalado: $(python -c 'import fastapi; print("✓")')"
echo "Entorno virtual activo: $VIRTUAL_ENV"
if command -v docker &> /dev/null; then
    echo "Docker: $(docker --version)"
else
    echo "Docker: No instalado (opcional)"
fi
```

## 🎯 Estructura del Proyecto Base

Crear la estructura profesional que usaremos:

```bash
# Crear estructura de directorios
mkdir -p {src,tests,docs,scripts,.github/workflows}

# Crear archivos iniciales
touch {src/__init__.py,tests/__init__.py}
touch {README.md,.gitignore,requirements.txt,requirements-dev.txt}
touch {docker-compose.yml,Dockerfile,.env.example}

# Mostrar estructura creada
tree . -a -I 'venv|__pycache__'
```

## 📝 Archivos de Configuración Base

### .gitignore

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment variables
.env
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
EOF
```

### .env.example

```bash
cat > .env.example << 'EOF'
# Application
APP_NAME=FastAPI Bootcamp Week 1
APP_VERSION=1.0.0
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Database (for future weeks)
DATABASE_URL=sqlite:///./app.db

# Security (for future weeks)
SECRET_KEY=your-secret-key-here
EOF
```

## 🚀 Resultado Esperado

Al finalizar esta práctica debes tener:

✅ Python 3.11+ instalado y funcionando  
✅ Git configurado con SSH keys  
✅ Entorno virtual activo  
✅ FastAPI y dependencias instaladas  
✅ Estructura de proyecto profesional  
✅ Archivos de configuración base

## 🎯 Próximo Paso

Una vez completada esta configuración, estarás listo para crear tu primera API con FastAPI aplicando mejores prácticas desde el primer endpoint.

**Tiempo total invertido:** ~60 minutos  
**Valor generado:** Base sólida para desarrollo profesional

## 🆘 Troubleshooting Común

### Problema: pyenv no reconocido después de instalación

**Solución:**

```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

### Problema: SSH key no funciona con GitHub

**Solución:**

```bash
# Verificar que el ssh-agent esté corriendo
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Problema: Permisos en Linux/macOS

**Solución:**

```bash
# Para instalaciones de sistema, usar sudo solo cuando sea necesario
# Para pyenv y pip, NUNCA usar sudo
```

### Problema: Entorno virtual no se activa

**Solución:**

```bash
# Verificar que estás en el directorio correcto
pwd
# Reactivar
source venv/bin/activate
# Verificar
echo $VIRTUAL_ENV
```

## 📚 Referencias Adicionales

- [pyenv Documentation](https://github.com/pyenv/pyenv)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
