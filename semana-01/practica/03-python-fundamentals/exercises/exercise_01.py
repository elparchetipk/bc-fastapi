"""
Ejercicio 1: Type Hints y Validación de Datos

Instrucciones:
1. Completa las funciones con type hints apropiados
2. Implementa validación de datos
3. Maneja errores apropiadamente
"""

from typing import List, Dict, Optional, Union
from datetime import datetime

# TODO: Añadir type hints y implementar la función
def calculate_statistics(numbers):
    """
    Calcula estadísticas básicas de una lista de números.
    
    Args:
        numbers: Lista de números (int o float)
    
    Returns:
        Diccionario con: count, sum, average, min, max
    
    Raises:
        ValueError: Si la lista está vacía
        TypeError: Si algún elemento no es número
    """
    # Tu código aquí
    pass

# TODO: Añadir type hints y implementar la función
def format_user_info(user_data):
    """
    Formatea información de usuario.
    
    Args:
        user_data: Diccionario con keys: name, age, email (opcional)
    
    Returns:
        String formateado con la información
    
    Raises:
        KeyError: Si faltan campos requeridos
        ValueError: Si age es negativo
    """
    # Tu código aquí
    pass

# TODO: Añadir type hints y implementar la función
def merge_user_lists(list1, list2):
    """
    Combina dos listas de usuarios sin duplicados.
    
    Args:
        list1: Lista de diccionarios de usuario
        list2: Lista de diccionarios de usuario
    
    Returns:
        Lista combinada sin usuarios duplicados (basado en 'id')
    """
    # Tu código aquí
    pass

# Tests
if __name__ == "__main__":
    # Test calculate_statistics
    try:
        stats = calculate_statistics([1, 2, 3, 4, 5])
        print("Stats:", stats)
    except Exception as e:
        print("Error en calculate_statistics:", e)
    
    # Test format_user_info
    user = {"name": "Juan", "age": 25, "email": "juan@email.com"}
    try:
        info = format_user_info(user)
        print("User info:", info)
    except Exception as e:
        print("Error en format_user_info:", e)
    
    # Test merge_user_lists
    users1 = [{"id": 1, "name": "Juan"}, {"id": 2, "name": "María"}]
    users2 = [{"id": 2, "name": "María"}, {"id": 3, "name": "Pedro"}]
    try:
        merged = merge_user_lists(users1, users2)
        print("Merged users:", merged)
    except Exception as e:
        print("Error en merge_user_lists:", e)
