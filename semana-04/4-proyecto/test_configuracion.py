#!/usr/bin/env python3
"""
Test de configuración de VS Code para Semana 4
Ejecutar este script para verificar que todo está bien configurado
"""

def test_imports():
    """Verificar que todas las librerías se pueden importar"""
    try:
        import fastapi
        print("✅ FastAPI importado correctamente - Versión:", fastapi.__version__)
    except ImportError as e:
        print("❌ Error importando FastAPI:", e)
        return False
    
    try:
        import pydantic
        print("✅ Pydantic importado correctamente - Versión:", pydantic.__version__)
    except ImportError as e:
        print("❌ Error importando Pydantic:", e)
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy importado correctamente - Versión:", sqlalchemy.__version__)
    except ImportError as e:
        print("❌ Error importando SQLAlchemy:", e)
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn importado correctamente")
    except ImportError as e:
        print("❌ Error importando Uvicorn:", e)
        return False
    
    return True

def test_environment():
    """Verificar el entorno de Python"""
    import sys
    import os
    
    print("\n🔍 Información del entorno:")
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    # Verificar si estamos en el entorno virtual correcto
    if "semana-04" in sys.executable:
        print("✅ Ejecutándose en entorno virtual de semana-04")
    else:
        print("⚠️  No se detectó entorno virtual de semana-04")
        print("   Asegúrate de activar: source ../../recursos-compartidos/venv/semana-04/bin/activate")

def main():
    print("🧪 Test de configuración - Semana 4 FastAPI Bootcamp")
    print("=" * 50)
    
    success = test_imports()
    test_environment()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ¡Configuración correcta! Puedes empezar a trabajar.")
        print("💡 Si VS Code muestra errores, consulta CONFIGURACION_VSCODE.md")
    else:
        print("❌ Hay problemas de configuración.")
        print("💡 Solución:")
        print("   1. Activar entorno virtual: source ../../recursos-compartidos/venv/semana-04/bin/activate")
        print("   2. Instalar dependencias: pip install -r requirements.txt")
        print("   3. Configurar VS Code: ver CONFIGURACION_VSCODE.md")

if __name__ == "__main__":
    main()
