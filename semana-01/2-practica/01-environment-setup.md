# Práctica 1: Configuración Rápida del Entorno

## 🎯 Objetivo

Configurar el entorno mínimo necesario para desarrollar con FastAPI en solo 90 minutos, enfocándonos en lo esencial y la gestión adecuada en equipos compartidos.

## ⏱️ Tiempo Estimado: 90 minutos (incluye buffer para problemas)

## 🚨 IMPORTANTE: Configuración para Equipos Compartidos

**ANTES DE EMPEZAR:** Este bootcamp reconoce que muchos estudiantes trabajan en equipos compartidos donde múltiples aprendices de diferentes jornadas utilizan las mismas máquinas. Esta práctica está diseñada para evitar conflictos y garantizar que cada estudiante pueda trabajar de forma independiente.

### Principios Clave:

1. **Carpetas personales separadas** - Cada estudiante en su propio espacio
2. **Git configuración local** - Sin afectar configuración global
3. **Entornos virtuales aislados** - Dependencias independientes
4. **Documentación personal** - Identificar tu trabajo claramente

## 📋 Pre-requisitos

- Python 3.8+ ya instalado (verificar con `python3 --version`)
- Conexión a internet estable
- Cuenta de GitHub activa
- Editor de código (VS Code recomendado)
- **CLAVE**: Respetar el trabajo de otros estudiantes en equipos compartidos

## 🚀 Setup Rápido (4 pasos esenciales)

### Paso 0: VERIFICACIÓN PREVIA en Equipos Compartidos (10 min)

**🚨 CRÍTICO**: Antes de configurar cualquier cosa, verificar el estado actual del equipo para no interferir con otros estudiantes.

```bash
# PASO 1: Verificar configuración Git global existente
echo "=== Configuración Git Global Actual ==="
git config --global user.name 2>/dev/null || echo "No hay configuración global de nombre"
git config --global user.email 2>/dev/null || echo "No hay configuración global de email"

# PASO 2: Si aparece configuración de otro usuario, NO MODIFICAR
# Ejemplo de salida problemática:
# user.name=Maria Rodriguez
# user.email=maria@ejemplo.com
# ⚠️  En este caso, usaremos configuración LOCAL únicamente

# PASO 3: Verificar directorios de desarrollo existentes
echo "=== Directorios de desarrollo existentes ==="
ls -la ~/desarrollo-personal/ 2>/dev/null || echo "No existe carpeta desarrollo-personal (perfecto)"
ls -la ~/Desktop/proyecto* 2>/dev/null || echo "No hay proyectos en Desktop (bien)"

# PASO 4: Verificar procesos Python/servidor activos
echo "=== Procesos activos que podrían causar conflictos ==="
ps aux | grep -E "(python|uvicorn|fastapi)" | grep -v grep | head -5

# PASO 5: Solo proceder si:
# ✅ Entiendes qué configuración Git existe
# ✅ Has elegido tu carpeta personal única
# ✅ No hay conflictos de puertos/procesos evidentes
```

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

### Paso 2: Crear Tu Carpeta Personal de Desarrollo (15 min)

**🚨 REGLA DE ORO**: En equipos compartidos, cada estudiante DEBE trabajar en su propia carpeta personal identificada con su nombre real. Esto previene conflictos y facilita la identificación de proyectos.

```bash
# PASO 1: Crear tu carpeta personal con nomenclatura clara
# Usar formato: nombre-apellido-bootcamp (sin espacios, sin acentos)
mkdir -p ~/desarrollo-personal/tu-nombre-apellido-bootcamp
cd ~/desarrollo-personal/tu-nombre-apellido-bootcamp

# Ejemplos específicos de nomenclatura correcta:
# mkdir -p ~/desarrollo-personal/juan-perez-bootcamp
# mkdir -p ~/desarrollo-personal/maria-garcia-bootcamp
# mkdir -p ~/desarrollo-personal/carlos-rodriguez-bootcamp

# PASO 2: Verificar que estás en TU carpeta personal
pwd
# Debe mostrar algo como: /home/usuario/desarrollo-personal/tu-nombre-apellido-bootcamp

# PASO 3: Crear proyecto FastAPI dentro de tu carpeta personal
mkdir mi-primera-api-fastapi
cd mi-primera-api-fastapi

# PASO 4: Crear entorno virtual AISLADO (crucial para equipos compartidos)
python3 -m venv venv-personal

# PASO 5: Activar entorno virtual (verificar que funciona)
source venv-personal/bin/activate
# Verificar activación: el prompt debe cambiar para mostrar (venv-personal)

# PASO 6: Actualizar pip e instalar dependencias EN TU ENTORNO AISLADO
pip install --upgrade pip
pip install "fastapi[all]" uvicorn

# PASO 7: Verificar instalación local (no global)
echo "=== Verificación de instalación local ==="
which python  # Debe mostrar ruta de tu venv
which pip     # Debe mostrar ruta de tu venv
pip list | grep fastapi
pip list | grep uvicorn
```

**🔍 Checkpoint de Aislamiento:**

```bash
# Estos comandos deben mostrar rutas de TU entorno virtual:
echo "Python ejecutable: $(which python)"
echo "Pip ejecutable: $(which pip)"
echo "Directorio actual: $(pwd)"
echo "Entorno virtual activo: $VIRTUAL_ENV"
```

### Paso 3: Configuración Git LOCAL (20 min)

**🚨 PRINCIPIO FUNDAMENTAL**: En equipos compartidos, NUNCA modificar la configuración global de Git. Usar ÚNICAMENTE configuración local por proyecto para evitar interferir con el trabajo de otros estudiantes.

```bash
# PASO 1: Inicializar repositorio Git en TU proyecto
git init

# PASO 2: Configurar Git EXCLUSIVAMENTE para este proyecto (NO global)
# ⚠️  NOTA: Sin el flag --global, la configuración solo aplica a este proyecto
git config user.name "Tu Nombre Completo Real"

# CONFIGURACIÓN DE EMAIL - RECOMENDACIÓN DE SEGURIDAD:
# 🔒 OPCIÓN 1 (RECOMENDADA): Usar email privado de GitHub para proteger tu email real
# Ir a GitHub.com → Settings → Emails → "Keep my email addresses private"
# GitHub genera un email como: 123456789+tunombre@users.noreply.github.com
git config user.email "123456789+tunombre@users.noreply.github.com"

# 🔓 OPCIÓN 2 (MENOS SEGURA): Usar tu email real
# git config user.email "tu-email-personal@gmail.com"

# 💡 CÓMO OBTENER TU EMAIL PRIVADO DE GITHUB:
# 1. Ir a https://github.com/settings/emails
# 2. Marcar "Keep my email addresses private"
# 3. Copiar el email que aparece como "ID+username@users.noreply.github.com"
# 4. Usar ese email en la configuración Git

# PASO 3: Verificar que la configuración local está correcta
echo "=== Configuración Git de este proyecto ==="
git config user.name
git config user.email
echo "=== Configuración Git global (NO modificada) ==="
git config --global user.name 2>/dev/null || echo "Sin configuración global (perfecto)"
git config --global user.email 2>/dev/null || echo "Sin configuración global (perfecto)"

# PASO 4: Crear .gitignore específico para FastAPI
cat > .gitignore << 'EOF'
# Entorno virtual (crucial para aislar dependencias en equipos compartidos)
venv-personal/
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
pip-log.txt
pip-delete-this-directory.txt

# Variables de entorno (pueden contener información sensible)
.env
.env.local
.env.production

# IDE y editores (configuraciones personales)
.vscode/
.idea/
*.swp
*.swo

# Archivos del sistema operativo
.DS_Store
Thumbs.db

# Logs y archivos temporales
*.log
logs/
temp/
tmp/
EOF

# PASO 5: Crear README personal con información de identificación
cat > README.md << EOF
# Mi Primera API FastAPI - Bootcamp

**👤 Desarrollador**: $(git config user.name)
**📧 Email**: $(git config user.email)
**� Privacidad**: Email configurado según mejores prácticas de GitHub
**�📅 Fecha de creación**: $(date '+%Y-%m-%d %H:%M:%S')
**📂 Ruta del proyecto**: $(pwd)
**💻 Equipo de trabajo**: $(hostname)

## 🔧 Configuración Local

Este proyecto está configurado para trabajo en equipo compartido:

- **Entorno virtual aislado**: \`venv-personal/\`
- **Configuración Git local**: Solo para este proyecto
- **Dependencias independientes**: No afecta otras instalaciones

## 🚀 Instalación y Ejecución

\`\`\`bash
# 1. Activar entorno virtual personal
source venv-personal/bin/activate

# 2. Instalar dependencias (si es necesario)
pip install -r requirements.txt

# 3. Ejecutar servidor de desarrollo
uvicorn main:app --reload --port 8000
\`\`\`

## 📝 Notas del Desarrollador

- **Configuración Git**: Local únicamente, no afecta configuración global
- **Email de GitHub**: Configurado con email privado para proteger información personal
- **Entorno aislado**: Todas las dependencias en venv-personal/
- **Puerto por defecto**: 8000 (cambiar si hay conflictos)
- **Estado del bootcamp**: Semana 1 - Configuración inicial

## 🛠️ Troubleshooting Personal

- Si el entorno virtual no se activa: \`rm -rf venv-personal && python3 -m venv venv-personal\`
- Si hay conflictos de puerto: cambiar --port en uvicorn
- Si Git no funciona: verificar \`git config user.name\` y \`git config user.email\`
- Si necesitas cambiar el email: usar el email privado de GitHub desde Settings → Emails

EOF

# PASO 6: Crear archivo de dependencias con versiones específicas
pip freeze > requirements.txt

# PASO 7: Primer commit con configuración local verificada
git add .

**Ejemplos de buenas prácticas de commit**
https://www.conventionalcommits.org/en/v1.0.0/

git commit -m "feat: configuración inicial personal del proyecto FastAPI

- Entorno virtual aislado creado: venv-personal/
- Git configurado localmente (no afecta configuración global)
- README con información personal del desarrollador
- Dependencias FastAPI instaladas y documentadas
- Configuración lista para equipo compartido

Desarrollador: $(git config user.name)
Email: $(git config user.email)
Fecha: $(date)"

echo "✅ Configuración Git local completada"
echo "✅ Primer commit realizado con información personal"
echo "✅ Listo para desarrollo sin interferir con otros estudiantes"
```

**🔍 Verificación Final de Aislamiento:**

```bash
echo "=== VERIFICACIÓN DE AISLAMIENTO COMPLETA ==="
echo "📁 Directorio de trabajo: $(pwd)"
echo "👤 Git usuario (local): $(git config user.name)"
echo "📧 Git email (local): $(git config user.email)"
echo "🐍 Python activo: $(which python)"
echo "📦 Pip activo: $(which pip)"
echo "🌍 Entorno virtual: $VIRTUAL_ENV"
echo "🔧 Git global NO modificado: $(git config --global user.name 2>/dev/null && echo 'ATENCIÓN: Hay configuración global' || echo 'Perfecto: Sin configuración global')"
```

### Paso 4: Verificación del Setup y Primera API (15 min)

Crear un archivo de prueba completo para verificar que todo funciona correctamente:

```bash
# PASO 1: Crear archivo main.py con API básica de verificación
cat > main.py << 'EOF'
#!/usr/bin/env python3
"""
Mi Primera API FastAPI - Verificación de Setup
Desarrollador: [Tu nombre se llenará automáticamente]
"""

from fastapi import FastAPI
import os
import sys
from datetime import datetime

# Crear instancia de FastAPI
app = FastAPI(
    title="Mi Primera API FastAPI",
    description="API de verificación para setup del bootcamp",
    version="1.0.0"
)

@app.get("/")
def home():
    """Endpoint principal de verificación"""
    return {
        "message": "¡Setup completado correctamente!",
        "project": "FastAPI Bootcamp - Semana 1",
        "timestamp": datetime.now().isoformat(),
        "status": "✅ Funcionando perfectamente"
    }

@app.get("/info/setup")
def info_setup():
    """Información del entorno de desarrollo"""
    return {
        "python_version": sys.version,
        "python_path": sys.executable,
        "working_directory": os.getcwd(),
        "virtual_env": os.environ.get("VIRTUAL_ENV", "No detectado"),
        "user": os.environ.get("USER", "No detectado"),
        "hostname": os.environ.get("HOSTNAME", "No detectado")
    }

@app.get("/health")
def health_check():
    """Endpoint de verificación de salud"""
    return {
        "status": "healthy",
        "message": "API funcionando correctamente",
        "environment": "development"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando servidor de verificación...")
    print("📍 Acceder a: http://localhost:8000")
    print("📖 Documentación: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
EOF

# PASO 2: Crear script de verificación rápida
cat > verificar_setup.py << 'EOF'
#!/usr/bin/env python3
"""
Script de verificación rápida del setup FastAPI
"""

import sys
import os
from pathlib import Path

def verificar_setup():
    print("🔍 VERIFICACIÓN DEL SETUP FASTAPI")
    print("=" * 50)

    # Verificar Python
    print(f"✅ Python version: {sys.version.split()[0]}")
    print(f"✅ Python path: {sys.executable}")

    # Verificar entorno virtual
    venv = os.environ.get("VIRTUAL_ENV")
    if venv:
        print(f"✅ Entorno virtual activo: {venv}")
    else:
        print("⚠️  Entorno virtual no detectado")

    # Verificar directorio de trabajo
    print(f"✅ Directorio actual: {os.getcwd()}")

    # Verificar instalaciones
    try:
        import fastapi
        print(f"✅ FastAPI instalado: v{fastapi.__version__}")
    except ImportError:
        print("❌ FastAPI NO instalado")
        return False

    try:
        import uvicorn
        print(f"✅ Uvicorn instalado: v{uvicorn.__version__}")
    except ImportError:
        print("❌ Uvicorn NO instalado")
        return False

    # Verificar archivos del proyecto
    archivos_requeridos = ["main.py", "requirements.txt", "README.md", ".gitignore"]
    for archivo in archivos_requeridos:
        if Path(archivo).exists():
            print(f"✅ Archivo presente: {archivo}")
        else:
            print(f"⚠️  Archivo faltante: {archivo}")

    # Verificar configuración Git
    import subprocess
    try:
        git_user = subprocess.check_output(['git', 'config', 'user.name'],
                                         stderr=subprocess.DEVNULL).decode().strip()
        git_email = subprocess.check_output(['git', 'config', 'user.email'],
                                          stderr=subprocess.DEVNULL).decode().strip()
        print(f"✅ Git configurado - Usuario: {git_user}")
        print(f"✅ Git configurado - Email: {git_email}")
    except:
        print("⚠️  Git no configurado localmente")

    print("\n🎯 RESUMEN DEL SETUP:")
    print("✅ Setup básico completado")
    print("🚀 Listo para ejecutar: uvicorn main:app --reload")
    print("📖 Documentación disponible en: http://localhost:8000/docs")
    print("🔧 Verificación disponible en: http://localhost:8000/info/setup")

    return True

if __name__ == "__main__":
    verificar_setup()
EOF

# PASO 3: Ejecutar verificación
python verificar_setup.py

# PASO 4: Actualizar requirements.txt con dependencias actuales
pip freeze > requirements.txt

# PASO 5: Hacer commit con la API de verificación
git add .
git commit -m "feat: agregar API de verificación y script de diagnóstico

- main.py: API básica con endpoints de verificación
- verificar_setup.py: script de diagnóstico del entorno
- requirements.txt actualizado con dependencias actuales
- Setup listo para testing y desarrollo

Cambios listos para ejecutar y verificar funcionamiento"

echo ""
echo "🎉 ¡SETUP COMPLETADO!"
echo "🚀 Para probar tu API ejecuta:"
echo "   uvicorn main:app --reload"
echo ""
echo "📍 Luego visita:"
echo "   http://localhost:8000 (página principal)"
echo "   http://localhost:8000/docs (documentación automática)"
echo "   http://localhost:8000/info/setup (información del entorno)"
```

## 🔒 PROTOCOLO OBLIGATORIO para Equipos Compartidos

### Reglas de Convivencia para el Bootcamp:

1. **🏠 Espacios Personales**: Cada estudiante trabaja ÚNICAMENTE en `~/desarrollo-personal/su-nombre-apellido-bootcamp/`
2. **⚠️ Git Local**: NUNCA usar `git config --global` - Solo configuración local por proyecto
3. **🔒 Entornos Aislados**: Siempre usar entornos virtuales con nombres únicos (`venv-personal/`)
4. **📝 Identificación**: Cada proyecto debe tener README con datos del desarrollador
5. **🤝 Respeto**: No modificar ni acceder a carpetas de otros estudiantes
6. **🆘 Comunicación**: Reportar problemas sin intentar "arreglar" configuración global

### ⚠️ Situaciones Problemáticas y Soluciones:

#### "Git ya está configurado con otro usuario"

```bash
# ❌ NO HACER: git config --global user.name "Mi Nombre"
# ✅ SÍ HACER: Configuración local únicamente
cd mi-proyecto
git config user.name "Mi Nombre Real"
git config user.email "mi-email@ejemplo.com"
git config user.name  # Verificar que muestra MI nombre
```

#### "No puedo crear carpetas / Permisos denegados"

```bash
# ✅ Usar directorio home personal
cd ~
mkdir -p desarrollo-personal/mi-nombre-apellido-bootcamp
cd desarrollo-personal/mi-nombre-apellido-bootcamp
ls -la  # Verificar permisos correctos
```

#### "El entorno virtual ya existe / Conflictos de dependencias"

```bash
# ✅ Crear entorno con nombre único
python3 -m venv venv-mi-nombre
source venv-mi-nombre/bin/activate
# O recrear completamente en tu carpeta
rm -rf venv-mi-nombre
python3 -m venv venv-mi-nombre
source venv-personal/bin/activate
```

#### "Puerto 8000 ya está en uso"

```bash
# ✅ Usar puerto diferente
uvicorn main:app --reload --port 8001
# O verificar qué proceso lo usa
lsof -i :8000
```

#### "Error al hacer push a GitHub"

```bash
# Verificar configuración local
git config user.name
git config user.email
# Si aparece otro usuario, reconfigurar localmente
git config user.name "Mi Nombre Real"
git config user.email "mi-email-personal@gmail.com"
```

## ✅ Objetivos Cumplidos

Al finalizar este setup rápido, deberías tener:

- ✅ **Verificación previa realizada** (sin interferir con otros usuarios)
- ✅ **Carpeta personal identificada creada** (`~/desarrollo-personal/tu-nombre-apellido-bootcamp/`)
- ✅ **Python 3.8+ funcionando en tu espacio aislado**
- ✅ **Entorno virtual personal creado** (`venv-personal/`)
- ✅ **FastAPI y Uvicorn instalados localmente** (sin afectar instalaciones globales)
- ✅ **Git configurado EXCLUSIVAMENTE para tu proyecto** (configuración local)
- ✅ **API de verificación funcionando** (main.py con endpoints de prueba)
- ✅ **Documentación personal completa** (README con tus datos)
- ✅ **Script de diagnóstico disponible** (verificar_setup.py)

## 🎯 Verificación Final del Setup

```bash
# Ejecutar desde tu proyecto para verificar todo:
cd ~/desarrollo-personal/tu-nombre-apellido-bootcamp/mi-primera-api-fastapi
source venv-personal/bin/activate
python verificar_setup.py
uvicorn main:app --reload --port 8000
```

## 🔄 Próximos Pasos

1. **Inmediato**: Ejecutar tu API y probar los endpoints de verificación
2. **Semana 2**: Desarrollo de endpoints más complejos manteniendo el aislamiento
3. **Futuro**: Setup de testing y CI/CD en tu entorno personal

## 🆘 Problemas Comunes ESPECÍFICOS para Equipos Compartidos

### "Git dice que ya está configurado con otro usuario"

**Síntoma**: Al hacer `git config --global user.name` aparece el nombre de otro estudiante

```bash
# ❌ NO HACER: git config --global user.name "Mi Nombre"
# ❌ NO HACER: git config --global user.email "mi@email.com"

# ✅ SOLUCIÓN CORRECTA: Usar configuración local únicamente
cd tu-proyecto
git init  # Si no es un repo aún
git config user.name "Tu Nombre Real"
git config user.email "tu-email@ejemplo.com"

# Verificar que funciona localmente (sin --global)
git config user.name  # Debe mostrar TU nombre
git config user.email # Debe mostrar TU email

# Verificar que NO modificaste la configuración global
git config --global user.name  # Debe mostrar el nombre original (de otro usuario)
```

### "No puedo crear carpetas en el directorio actual"

**Síntoma**: `mkdir` dice "Permission denied" o no puedes escribir archivos

```bash
# ✅ SOLUCIÓN: Usar tu directorio home personal
cd ~  # Ir a tu directorio personal
pwd   # Verificar que estás en /home/tu-usuario

# Crear estructura en tu espacio personal
mkdir -p desarrollo-personal/tu-nombre-apellido-bootcamp
cd desarrollo-personal/tu-nombre-apellido-bootcamp
ls -la  # Verificar permisos correctos (debe mostrar tu usuario como propietario)
```

### "El entorno virtual ya existe de otro usuario"

**Síntoma**: Error al crear `venv` o `source` no funciona

```bash
# ✅ SOLUCIÓN: Crear entorno con nombre único en tu carpeta
cd ~/desarrollo-personal/tu-nombre-apellido-bootcamp/tu-proyecto

# Opción 1: Nombre único
python3 -m venv venv-tu-nombre-apellido
source venv-tu-nombre-apellido/bin/activate

# Opción 2: Limpiar y recrear en tu espacio
rm -rf venv  # Solo si estás en TU carpeta personal
python3 -m venv venv-personal
source venv-personal/bin/activate

# Verificar que el entorno es tuyo
echo $VIRTUAL_ENV  # Debe mostrar ruta a TU directorio
```

### "FastAPI ya está instalado globalmente / Conflictos de versiones"

**Síntoma**: `pip list` muestra FastAPI pero en versión diferente o no funciona

```bash
# ESTO ES NORMAL y ESPERADO en equipos compartidos
# ✅ SOLUCIÓN: Usar tu entorno virtual aislado

source venv-personal/bin/activate  # Activar TU entorno
pip list  # Verificar que estás en entorno aislado (lista corta)
pip install "fastapi[all]" uvicorn  # Instalar en TU entorno

# Verificar aislamiento
which python  # Debe mostrar ruta de tu venv
which pip     # Debe mostrar ruta de tu venv
pip list | grep fastapi  # Verificar versión en tu entorno
```

### "Conflictos al hacer push a GitHub"

**Síntoma**: Git rechaza el push o aparece el nombre de otro usuario en commits

```bash
# ✅ VERIFICAR configuración local primero
git config user.name
git config user.email

# Si aparece otro usuario, configurar localmente
git config user.name "Tu Nombre Real"

# 🔒 RECOMENDACIÓN DE SEGURIDAD: Usar email privado de GitHub
# Obtener tu email privado en: https://github.com/settings/emails
git config user.email "123456789+tunombre@users.noreply.github.com"
# O usar tu email real (menos recomendado):
# git config user.email "tu-email-personal@gmail.com"

# Verificar último commit
git log --oneline -1  # Debe mostrar TU nombre

# Si el commit anterior tiene otro nombre, crear nuevo commit
git commit --amend --author="Tu Nombre <123456789+tunombre@users.noreply.github.com>"
```

### "Puerto 8000 ya está en uso / No puedo acceder a la API"

**Síntoma**: Error "Address already in use" al ejecutar uvicorn

```bash
# ✅ SOLUCIÓN: Verificar qué está usando el puerto
lsof -i :8000  # Ver qué proceso usa el puerto 8000
ps aux | grep uvicorn  # Ver si hay otros servidores corriendo

# Opción 1: Usar puerto diferente
uvicorn main:app --reload --port 8001
uvicorn main:app --reload --port 8002

# Opción 2: Si el proceso es tuyo, detenerlo
# Encontrar PID en lsof y usar: kill PID

# Opción 3: Puerto automático
uvicorn main:app --reload --port 0  # Sistema asigna puerto libre
```

### "No puedo instalar paquetes / pip no funciona"

**Síntoma**: "pip: command not found" o errores de permisos

```bash
# ✅ VERIFICAR que estás en tu entorno virtual
echo $VIRTUAL_ENV  # Debe mostrar ruta a tu venv

# Si no hay entorno activo
source venv-personal/bin/activate

# Si pip no existe en el entorno
python -m ensurepip --upgrade
python -m pip install --upgrade pip

# Verificar pip funcionando
which pip  # Debe mostrar ruta dentro de tu venv
pip --version
```

## 📝 Notas Importantes para Equipos Compartidos

- **Este es un setup conservador**: Prioriza no interferir con otros usuarios sobre optimización
- **La configuración local es clave**: Permite que múltiples estudiantes trabajen sin conflictos
- **Los entornos virtuales son obligatorios**: Evitan conflictos de dependencias entre proyectos
- **Documentación personal es crítica**: Facilita identificar proyectos en equipos compartidos
- **Pide ayuda con contexto**: Menciona si compartes el equipo y qué configuración ya existe

## 🎯 Tiempo Target vs Real para Equipos Compartidos

- **Verificación previa**: 10 min (crítico para evitar problemas)
- **Setup Python**: 5 min (si ya está instalado)
- **Carpeta personal + entorno virtual**: 15 min (incluye nomenclatura y verificación)
- **Git configuración local**: 20 min (más tiempo para entender local vs global)
- **API de verificación**: 15 min (incluye testing)
- **Troubleshooting**: 25 min (buffer para problemas de equipos compartidos)

**Total: 90 min (realistas considerando problemas de equipos compartidos)**

## 🏆 Criterios de Éxito

Al completar esta práctica, debes poder demostrar:

1. **✅ Aislamiento completo**: Tu trabajo no afecta ni es afectado por otros usuarios
2. **✅ Identificación clara**: Tu proyecto tiene tu nombre y datos personales
3. **✅ Configuración local**: Git configurado solo para tu proyecto
4. **✅ API funcionando**: Endpoints de verificación respondiendo correctamente
5. **✅ Documentación completa**: README con información personal y troubleshooting

## 🤝 Protocolo de Ayuda en Equipos Compartidos

Si necesitas ayuda, proporciona:

1. **Tu nombre completo** (para identificar tu carpeta/proyecto)
2. **Ruta de trabajo actual** (`pwd`)
3. **Estado del entorno virtual** (`echo $VIRTUAL_ENV`)
4. **Configuración Git local** (`git config user.name`)
5. **Mensaje de error completo** (screenshot o copy-paste)

Esto permite ayudarte sin interferir con el trabajo de otros estudiantes.
