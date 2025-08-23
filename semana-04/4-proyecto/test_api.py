#!/usr/bin/env python3
"""
Script de testing LTS para API de Biblioteca - Semana 4
Compatible con versiones estables de FastAPI y Python 3.8+
"""

import requests
import json
import time
import sys
from typing import Optional

BASE_URL = "http://localhost:8000"

def wait_for_server(max_attempts=5):
    """Esperar a que el servidor esté listo"""
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{BASE_URL}/")
            if response.status_code == 200:
                print("✅ Servidor funcionando correctamente")
                return True
        except requests.exceptions.ConnectionError:
            print(f"⏳ Esperando servidor... intento {attempt + 1}/{max_attempts}")
            time.sleep(2)
    return False

def test_create_book():
    """Test: Crear un libro"""
    print("\n📚 Testing: Crear libro")
    book_data = {
        "title": "Don Quijote de la Mancha",
        "author": "Miguel de Cervantes",
        "isbn": "978-84-376-0494-7",
        "publication_year": 1605
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/books/", json=book_data)
        if response.status_code == 201:
            book = response.json()
            print(f"✅ Libro creado: {book['title']} (ID: {book['id']})")
            return book['id']
        else:
            print(f"❌ Error creando libro: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_create_user():
    """Test: Crear un usuario"""
    print("\n👤 Testing: Crear usuario")
    user_data = {
        "name": "Juan Pérez",
        "email": "juan.perez@example.com",
        "phone": "+1234567890"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/users/", json=user_data)
        if response.status_code == 201:
            user = response.json()
            print(f"✅ Usuario creado: {user['name']} (ID: {user['id']})")
            return user['id']
        else:
            print(f"❌ Error creando usuario: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_list_books():
    """Test: Listar libros"""
    print("\n📋 Testing: Listar libros")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/books/")
        if response.status_code == 200:
            books = response.json()
            print(f"✅ {len(books)} libro(s) encontrado(s)")
            return True
        else:
            print(f"❌ Error listando libros: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_create_loan(user_id, book_id):
    """Test: Crear un préstamo"""
    print("\n🔄 Testing: Crear préstamo")
    if not user_id or not book_id:
        print("❌ Faltan IDs de usuario o libro")
        return None
        
    loan_data = {
        "user_id": user_id,
        "book_id": book_id
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/loans/", json=loan_data)
        if response.status_code == 201:
            loan = response.json()
            print(f"✅ Préstamo creado (ID: {loan['id']})")
            print(f"   Usuario: {loan['user_id']}, Libro: {loan['book_id']}")
            return loan['id']
        else:
            print(f"❌ Error creando préstamo: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_return_book(loan_id):
    """Test: Devolver un libro"""
    print("\n↩️ Testing: Devolver libro")
    if not loan_id:
        print("❌ Falta ID de préstamo")
        return False
        
    try:
        response = requests.put(f"{BASE_URL}/api/v1/loans/{loan_id}/return")
        if response.status_code == 200:
            loan = response.json()
            print(f"✅ Libro devuelto correctamente")
            print(f"   Fecha devolución: {loan['return_date']}")
            return True
        else:
            print(f"❌ Error devolviendo libro: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_book_availability():
    """Test: Verificar disponibilidad de libros"""
    print("\n🔍 Testing: Verificar disponibilidad")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/stats/books")
        if response.status_code == 200:
            stats = response.json()
            print(f"✅ Estadísticas de libros:")
            print(f"   Total: {stats['total_books']}")
            print(f"   Disponibles: {stats['available_books']}")
            print(f"   Prestados: {stats['borrowed_books']}")
            return True
        else:
            print(f"❌ Error obteniendo estadísticas: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_validation_errors():
    """Test: Validar manejo de errores"""
    print("\n⚠️ Testing: Validación de errores")
    
    # Test 1: Email duplicado
    print("   Test 1: Email duplicado")
    user_data = {
        "name": "Ana García",
        "email": "juan.perez@example.com"  # Email ya usado
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/v1/users/", json=user_data)
        if response.status_code == 400:
            print("   ✅ Error de email duplicado manejado correctamente")
        else:
            print(f"   ❌ Error esperado no ocurrió: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Libro no encontrado
    print("   Test 2: Libro no encontrado")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/books/999")
        if response.status_code == 404:
            print("   ✅ Error de libro no encontrado manejado correctamente")
        else:
            print(f"   ❌ Error esperado no ocurrió: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def test_business_rules(user_id):
    """Test: Reglas de negocio"""
    print("\n📏 Testing: Reglas de negocio")
    
    if not user_id:
        print("❌ Falta ID de usuario")
        return
    
    # Crear múltiples libros para probar límite de préstamos
    book_ids = []
    for i in range(4):  # Intentar crear 4 libros
        book_data = {
            "title": f"Libro de Prueba {i+1}",
            "author": "Autor de Prueba"
        }
        try:
            response = requests.post(f"{BASE_URL}/api/v1/books/", json=book_data)
            if response.status_code == 201:
                book_ids.append(response.json()['id'])
        except:
            pass
    
    # Intentar prestar más de 3 libros al mismo usuario
    loans_created = 0
    for book_id in book_ids:
        loan_data = {"user_id": user_id, "book_id": book_id}
        try:
            response = requests.post(f"{BASE_URL}/api/v1/loans/", json=loan_data)
            if response.status_code == 201:
                loans_created += 1
                print(f"   ✅ Préstamo {loans_created} creado")
            elif response.status_code == 400 and loans_created >= 3:
                print(f"   ✅ Límite de 3 préstamos funcionando correctamente")
                break
        except:
            pass

def run_all_tests():
    """Ejecutar todos los tests"""
    print("🧪 INICIANDO TESTS DE LA API DE BIBLIOTECA")
    print("=" * 50)
    
    # Verificar que el servidor esté corriendo
    if not wait_for_server():
        print("❌ No se pudo conectar al servidor")
        print("💡 Asegúrate de ejecutar: python ejemplo_main.py")
        sys.exit(1)
    
    # Ejecutar tests principales
    book_id = test_create_book()
    user_id = test_create_user()
    test_list_books()
    
    loan_id = test_create_loan(user_id, book_id)
    test_book_availability()
    test_return_book(loan_id)
    test_book_availability()
    
    # Tests de validación
    test_validation_errors()
    test_business_rules(user_id)
    
    print("\n" + "=" * 50)
    print("🎉 TESTS COMPLETADOS")
    print("💡 Revisa la documentación automática en: http://localhost:8000/docs")

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print("\n⏹️ Tests interrumpidos por el usuario")
    except Exception as e:
        print(f"\n❌ Error general: {e}")
