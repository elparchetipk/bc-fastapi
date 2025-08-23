# Semana 4 - Instrucciones de Ejecución

## Opción 1: Con entorno virtual (Recomendado)

```bash
# Activar entorno virtual de la semana 4
source ../../recursos-compartidos/venv/activate-semana.sh 4

# Ejecutar la aplicación
python ejemplo_main.py

# Ejecutar tests (en otra terminal)
source ../../recursos-compartidos/venv/activate-semana.sh 4
python test_api.py
```

## Opción 2: Instalación directa

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
python ejemplo_main.py
```

## Verificar funcionamiento

1. Abrir http://localhost:8000 - Página principal
2. Abrir http://localhost:8000/docs - Documentación automática
3. Ejecutar `python test_api.py` para tests automáticos

## Solución de problemas

Si hay conflictos de versiones:

1. Usar SIEMPRE el entorno virtual de la semana 4
2. No mezclar instalaciones globales con las del entorno virtual
3. Verificar versiones: `pip list | grep fastapi`
