# Configuración Rápida - Semana 4

## TL;DR (Muy Rápido)

```bash
# 1. Ir a semana 4
cd semana-04

# 2. Abrir VS Code AQUÍ (importante)
code .

# 3. VS Code debería configurarse automáticamente
# 4. Verificar barra inferior: debe mostrar "semana-04" en el intérprete
```

## Si hay errores de importación

### Opción A: Configuración automática

```bash
# Cerrar VS Code, luego:
cd semana-04
code .
```

### Opción B: Selección manual del intérprete

1. `Ctrl+Shift+P`
2. Escribir: "Python: Select Interpreter"
3. Seleccionar: `recursos-compartidos/venv/semana-04/bin/python`

## Verificación rápida

✅ Barra inferior muestra: `Python 3.13.0 ('.../semana-04/bin/python')`  
✅ No hay líneas rojas en `import fastapi`  
✅ Autocompletado funciona

## Archivos importantes ya configurados

- ✅ `.vscode/settings.json` - Configuración automática
- ✅ `recursos-compartidos/venv/semana-04/` - Entorno virtual con dependencias
- ✅ `requirements.txt` - Lista de dependencias exactas

## Si nada funciona

```bash
# Plan B: Ejecutar desde terminal
cd semana-04/4-proyecto
source ../../recursos-compartidos/venv/semana-04/bin/activate
python ejemplo_main.py
```

La aplicación debería funcionar perfectamente desde terminal aunque VS Code tenga errores de configuración.
