#!/usr/bin/env python3
"""
Script de pruebas para API de Productos - Semana 3
Enfocado en validaciones Pydantic y manejo de errores

Ejecutar: python test_api.py
Asegúrate de que la API esté corriendo en http://localhost:8000
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_connection():
    """Probar conexión básica"""
    print("🔍 Probando conexión...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Conexión exitosa")
            return True
        else:
            print(f"❌ Error de conexión: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ No se puede conectar a la API. ¿Está ejecutándose?")
        return False

def test_create_product_valid():
    """Probar creación de producto válido"""
    print("\n📦 Probando crear producto válido...")
    product_data = {
        "name": "laptop test",  # Debe capitalizarse automáticamente
        "description": "Laptop para pruebas",
        "price": 599.999,  # Debe redondearse a 2 decimales
        "stock": 10,
        "category": "electronics",
        "status": "active"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/products", json=product_data)
        if response.status_code == 201:
            result = response.json()
            print("✅ Producto creado exitosamente")
            
            # Verificar validaciones automáticas
            if result.get("name") == "Laptop Test":
                print("   ✅ Nombre capitalizado correctamente")
            if result.get("price") == 600.00:
                print("   ✅ Precio redondeado correctamente")
                
            return True, result.get("id")
        else:
            print(f"❌ Error al crear producto: {response.status_code}")
            print(f"   Detalle: {response.text}")
            return False, None
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False, None

def test_create_product_invalid():
    """Probar validaciones con datos inválidos"""
    print("\n🚫 Probando validaciones con datos inválidos...")
    
    # Casos de error que deben fallar
    invalid_cases = [
        {
            "name": "Precio negativo",
            "data": {"name": "Test", "price": -10, "stock": 5, "category": "electronics"},
            "expected_error": "price"
        },
        {
            "name": "Stock negativo", 
            "data": {"name": "Test", "price": 10, "stock": -5, "category": "electronics"},
            "expected_error": "stock"
        },
        {
            "name": "Nombre muy corto",
            "data": {"name": "A", "price": 10, "stock": 5, "category": "electronics"},
            "expected_error": "name"
        },
        {
            "name": "Categoría inválida",
            "data": {"name": "Test Product", "price": 10, "stock": 5, "category": "invalid_category"},
            "expected_error": "category"
        }
    ]
    
    passed = 0
    for case in invalid_cases:
        try:
            response = requests.post(f"{BASE_URL}/products", json=case["data"])
            if response.status_code == 422:  # Validation Error
                print(f"   ✅ {case['name']}: Validación funcionando")
                passed += 1
            else:
                print(f"   ❌ {case['name']}: Debería fallar pero no lo hizo (status: {response.status_code})")
        except Exception as e:
            print(f"   ❌ {case['name']}: Error en prueba - {e}")
    
    print(f"📊 Validaciones: {passed}/{len(invalid_cases)} pasaron")
    return passed == len(invalid_cases)

def test_get_product_not_found():
    """Probar manejo de error 404"""
    print("\n🔍 Probando error 404 (producto no encontrado)...")
    try:
        response = requests.get(f"{BASE_URL}/products/999")
        if response.status_code == 404:
            print("✅ Error 404 manejado correctamente")
            error_detail = response.json().get("detail", "")
            if "999" in error_detail:
                print("   ✅ Mensaje de error incluye ID del producto")
            return True
        else:
            print(f"❌ Se esperaba 404, pero se obtuvo: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_filters():
    """Probar filtros básicos"""
    print("\n🔍 Probando filtros...")
    
    filter_tests = [
        {"filter": "min_price=100", "description": "Precio mínimo"},
        {"filter": "max_price=500", "description": "Precio máximo"},
        {"filter": "category=electronics", "description": "Por categoría"},
        {"filter": "status=active", "description": "Por status"},
        {"filter": "min_price=100&max_price=500", "description": "Rango de precios"}
    ]
    
    passed = 0
    for test in filter_tests:
        try:
            response = requests.get(f"{BASE_URL}/products?{test['filter']}")
            if response.status_code == 200:
                products = response.json()
                print(f"   ✅ {test['description']}: {len(products)} productos encontrados")
                passed += 1
            else:
                print(f"   ❌ {test['description']}: Error {response.status_code}")
        except Exception as e:
            print(f"   ❌ {test['description']}: Error - {e}")
    
    print(f"📊 Filtros: {passed}/{len(filter_tests)} funcionando")
    return passed >= len(filter_tests) * 0.8  # 80% success rate

def test_update_product(product_id):
    """Probar actualización de producto"""
    if product_id is None:
        print("\n⚠️  Saltando prueba de actualización (no hay producto)")
        return True
        
    print(f"\n✏️  Probando actualización de producto {product_id}...")
    update_data = {
        "name": "producto actualizado",
        "price": 999.99,
        "stock": 20
    }
    
    try:
        response = requests.put(f"{BASE_URL}/products/{product_id}", json=update_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Producto actualizado exitosamente")
            
            # Verificar actualización
            if result.get("name") == "Producto Actualizado":
                print("   ✅ Nombre actualizado y capitalizado")
            if result.get("price") == 999.99:
                print("   ✅ Precio actualizado correctamente")
                
            return True
        else:
            print(f"❌ Error al actualizar: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def test_duplicate_validation():
    """Probar validación de nombres duplicados (si está implementada)"""
    print("\n🔄 Probando validación de duplicados...")
    
    # Intentar crear un producto con nombre que ya existe
    duplicate_data = {
        "name": "laptop test",  # Mismo nombre que el primero
        "price": 500,
        "stock": 5,
        "category": "electronics"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/products", json=duplicate_data)
        if response.status_code == 400:  # Bad Request por duplicado
            print("✅ Validación de duplicados funcionando (BONUS)")
            return True
        elif response.status_code == 201:
            print("⚠️  Validación de duplicados no implementada (OK, es bonus)")
            return True
        else:
            print(f"⚠️  Respuesta inesperada: {response.status_code}")
            return True
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        return False

def run_all_tests():
    """Ejecutar todas las pruebas"""
    print("🧪 INICIANDO PRUEBAS DE VALIDACIONES Y ERRORES")
    print("=" * 60)
    
    tests = []
    product_id = None
    
    # Test 1: Conexión
    if test_connection():
        tests.append(True)
    else:
        tests.append(False)
        print("\n❌ No se puede continuar sin conexión")
        return
    
    # Test 2: Crear producto válido
    success, product_id = test_create_product_valid()
    tests.append(success)
    
    # Test 3: Validaciones con datos inválidos
    tests.append(test_create_product_invalid())
    
    # Test 4: Error 404
    tests.append(test_get_product_not_found())
    
    # Test 5: Filtros
    tests.append(test_filters())
    
    # Test 6: Actualización
    tests.append(test_update_product(product_id))
    
    # Test 7: Duplicados (bonus)
    tests.append(test_duplicate_validation())
    
    # Resultados
    passed = sum(tests)
    total = len(tests)
    
    print("\n" + "=" * 60)
    print(f"🏆 RESULTADO: {passed}/{total} pruebas pasaron")
    
    if passed == total:
        print("🎉 ¡Excelente! Todas las validaciones y manejo de errores funcionan.")
    elif passed >= total * 0.8:
        print("👍 Muy bien! La mayoría de validaciones funcionan correctamente.")
    elif passed >= total * 0.6:
        print("👌 Bien! Las funcionalidades básicas están implementadas.")
    else:
        print("⚠️  Hay varias validaciones que necesitan trabajo.")
    
    print("\n📝 Enfócate especialmente en:")
    print("   • Validaciones Pydantic automáticas")
    print("   • HTTPException para errores 404")
    print("   • Manejo de errores de validación (422)")

def main():
    """Función principal"""
    print("API de Productos - Semana 3 - Script de Pruebas")
    print("Enfoque: Validaciones Pydantic y Manejo de Errores")
    print("Asegúrate de que tu API esté ejecutándose en http://localhost:8000")
    input("Presiona Enter para continuar...")
    
    run_all_tests()

if __name__ == "__main__":
    main()
