#!/usr/bin/env python3
"""
Script de pruebas básicas para la API de Biblioteca Personal
Ejecutar: python test_api.py
Asegúrate de que la API esté corriendo en http://localhost:8000

Dependencias requeridas:
- pip install requests

O instalar todas las dependencias:
- pip install -r requirements.txt
"""

import json
from datetime import datetime

# Verificar que requests esté instalado
try:
    import requests  # type: ignore
except ImportError:
    print("❌ Error: La biblioteca 'requests' no está instalada.")
    print("🔧 Solución: Ejecuta 'pip install requests' o 'pip install -r requirements.txt'")
    exit(1)

BASE_URL = "http://localhost:8000"

def test_connection():
    """Probar conexión básica"""
    print("🔍 Probando conexión...")
    try:
        response = requests.get(f"{BASE_URL}/")  # type: ignore
        if response.status_code == 200:
            print("✅ Conexión exitosa")
            return True
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:  # type: ignore
        print("❌ No se puede conectar a la API. ¿Está ejecutándose?")
        return False

def test_create_book():
    """Probar creación de libro"""
    print("\n📚 Probando crear libro...")
    book_data = {
        "title": "Test Book",
        "author": "Test Author",
        "isbn": "9781234567890",
        "genre": "fiction",
        "pages": 200,
        "publication_year": 2023,
        "status": "to_read",
        "rating": 4,
        "notes": "Libro de prueba"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/books", json=book_data)  # type: ignore
        if response.status_code in [200, 201]:
            print("✅ Libro creado exitosamente")
            print(f"   Respuesta: {response.json()}")
            return True
        else:
            print(f"❌ Error al crear libro: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_get_books():
    """Probar listado de libros"""
    print("\n📋 Probando listar libros...")
    try:
        response = requests.get(f"{BASE_URL}/books")  # type: ignore
        if response.status_code == 200:
            books = response.json()
            print(f"✅ Se obtuvieron {len(books)} libros")
            if books:
                print(f"   Primer libro: {books[0].get('title', 'Sin título')}")
            return True
        else:
            print(f"❌ Error al obtener libros: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_search_title():
    """Probar búsqueda por título"""
    print("\n🔍 Probando búsqueda por título...")
    try:
        response = requests.get(f"{BASE_URL}/books/search/title?title=test")
        if response.status_code == 200:
            books = response.json()
            print(f"✅ Búsqueda exitosa, {len(books)} resultados")
            return True
        else:
            print(f"❌ Error en búsqueda: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_async_endpoint():
    """Probar endpoint async (si existe)"""
    print("\n⚡ Probando endpoint async...")
    try:
        # Primero verificar si hay libros
        books_response = requests.get(f"{BASE_URL}/books")
        if books_response.status_code == 200:
            books = books_response.json()
            if books:
                book_id = books[0]["id"]
                response = requests.get(f"{BASE_URL}/books/{book_id}/metadata")
                if response.status_code == 200:
                    print("✅ Endpoint async funcionando")
                    print(f"   Metadata: {response.json()}")
                    return True
                else:
                    print(f"❌ Error en endpoint async: {response.status_code}")
                    return False
            else:
                print("⚠️  No hay libros para probar endpoint async")
                return True
        else:
            print("⚠️  No se puede acceder a la lista de libros")
            return False
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("🧪 INICIANDO PRUEBAS DE LA API")
    print("=" * 50)
    
    tests = [
        test_connection,
        test_create_book,
        test_get_books,
        test_search_title,
        test_async_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"🏆 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Todas las pruebas pasaron! Tu API está funcionando bien.")
    elif passed >= total * 0.7:
        print("👍 La mayoría de pruebas pasaron. Revisa los errores.")
    else:
        print("⚠️  Varias pruebas fallaron. Revisa tu implementación.")

def main():
    """Función principal"""
    print("API de Biblioteca Personal - Script de Pruebas")
    print("Verificando si la API está ejecutándose en http://localhost:8000")
    
    run_all_tests()

if __name__ == "__main__":
    main()
