# Guía de Configuración de VS Code para FastAPI Bootcamp

Esta guía te ayudará a configurar VS Code correctamente para evitar errores de importación y tener una experiencia de desarrollo óptima.

## Problema Común

Si ves errores como:

```
Cannot find implementation or library stub for module named "fastapi"
Import "fastapi" could not be resolved
```

**Esto significa que VS Code no está usando el entorno virtual correcto.**

## Solución Paso a Paso

### 1. Verificar que el entorno virtual existe

```bash
# Navegar a la semana específica
cd semana-04

# Verificar que existe el entorno virtual
ls ../recursos-compartidos/venv/semana-04/bin/python
```

### 2. Configurar VS Code - Método 1: Automático (Recomendado)

La carpeta `semana-04` ya tiene configuración automática:

1. **Abrir VS Code** en la carpeta `semana-04` (no en `bc-fastapi`)

   ```bash
   cd semana-04
   code .
   ```

2. **VS Code detectará automáticamente** la configuración en `.vscode/settings.json`

3. **Verificar** que VS Code muestra el intérprete correcto en la barra inferior:
   ```
   Python 3.13.0 ('.../recursos-compartidos/venv/semana-04/bin/python')
   ```

### 3. Configurar VS Code - Método 2: Manual

Si el método automático no funciona:

1. **Abrir Command Palette**: `Ctrl+Shift+P` (Linux/Windows) o `Cmd+Shift+P` (Mac)

2. **Buscar**: "Python: Select Interpreter"

3. **Seleccionar**: "Enter interpreter path..."

4. **Navegar** y seleccionar:
   ```
   recursos-compartidos/venv/semana-04/bin/python
   ```

### 4. Verificar Configuración

Una vez configurado, deberías ver:

✅ **Barra inferior de VS Code**: Muestra el intérprete del entorno virtual
✅ **No hay errores rojos** en las importaciones de FastAPI, SQLAlchemy, etc.
✅ **Autocompletado funciona** para las librerías instaladas

### 5. Solución de Problemas

#### Problema: VS Code sigue mostrando errores

**Solución**:

```bash
# 1. Cerrar VS Code completamente
# 2. Activar el entorno virtual
source recursos-compartidos/venv/semana-04/bin/activate

# 3. Abrir VS Code desde la terminal
code semana-04/4-proyecto/ejemplo_main.py

# 4. VS Code debería heredar el entorno activo
```

#### Problema: El entorno virtual no existe

**Solución**:

```bash
# Crear el entorno virtual para la semana
cd recursos-compartidos/venv
python -m venv semana-04

# Activar y instalar dependencias
source semana-04/bin/activate
pip install fastapi==0.115.0 uvicorn==0.32.0 sqlalchemy==2.0.35 pydantic==2.9.0
```

#### Problema: Errores persisten después de configurar

**Solución**:

1. **Recargar VS Code**: `Ctrl+Shift+P` → "Developer: Reload Window"
2. **Verificar terminal**: `Ctrl+Shift+\`` → Debería mostrar el entorno activado
3. **Verificar extensión Python**: Asegúrate de que esté instalada y actualizada

## Configuración Recomendada por Semana

Cada semana debería tener su propia configuración:

```
semana-01/
├── .vscode/settings.json  # Apunta a venv/semana-01
└── 4-proyecto/

semana-02/
├── .vscode/settings.json  # Apunta a venv/semana-02
└── 4-proyecto/

semana-04/
├── .vscode/settings.json  # Apunta a venv/semana-04
└── 4-proyecto/
```

## Verificación Final

Para confirmar que todo está bien configurado:

1. **Abrir** `ejemplo_main.py`
2. **No debería haber líneas rojas** en las importaciones
3. **Hover sobre FastAPI** → Debería mostrar documentación
4. **Ctrl+Space** → Debería mostrar autocompletado

## Comandos Útiles

```bash
# Ver qué intérprete está usando VS Code
python --version

# Ver qué librerías están disponibles
pip list | grep fastapi

# Verificar que las importaciones funcionan
python -c "import fastapi; print('✅ FastAPI funciona')"
```

## Archivos de Configuración Incluidos

- **`.vscode/settings.json`**: Configuración específica del proyecto
- **`.env`**: Variables de entorno para Python
- **`requirements.txt`**: Dependencias específicas de la semana

## Notas Importantes

- ⚠️ **Nunca mezclar** entornos virtuales entre semanas
- ⚠️ **Siempre abrir VS Code** desde la carpeta de la semana específica
- ⚠️ **Verificar el intérprete** en la barra inferior antes de empezar a trabajar
- ✅ **Usar siempre** el entorno virtual correspondiente a la semana

## Soporte

Si sigues teniendo problemas:

1. **Verificar** que el archivo `semana-XX/.vscode/settings.json` existe
2. **Comprobar** que el entorno virtual tiene las librerías instaladas
3. **Reiniciar** VS Code completamente
4. **Abrir** VS Code desde la terminal con el entorno activado

Con esta configuración, deberías tener una experiencia de desarrollo fluida sin errores de importación.
