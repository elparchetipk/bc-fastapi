import time
import functools
from typing import Callable, Any

# Decorador básico para medir tiempo
def timing_decorator(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} tomó {end_time - start_time:.4f} segundos")
        return result
    return wrapper

# Decorador con parámetros
def retry_decorator(max_attempts: int = 3):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Intento {attempt + 1} falló: {e}")
                    time.sleep(1)
        return wrapper
    return decorator

# Decorador para logging
def log_calls(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Llamando a {func.__name__} con args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} retornó: {result}")
        return result
    return wrapper

# Ejemplos de uso
@timing_decorator
@log_calls
def slow_function(n: int) -> int:
    """Función que simula operación lenta"""
    time.sleep(0.1)
    return n * 2

@retry_decorator(max_attempts=3)
def unreliable_function(success_rate: float = 0.7) -> str:
    """Función que puede fallar aleatoriamente"""
    import random
    if random.random() < success_rate:
        return "¡Éxito!"
    else:
        raise Exception("Operación falló")

if __name__ == "__main__":
    # Probar decoradores
    result = slow_function(5)
    print(f"Resultado: {result}")
    
    try:
        result = unreliable_function(0.3)  # Baja probabilidad de éxito
        print(f"Función poco confiable: {result}")
    except Exception as e:
        print(f"Función falló definitivamente: {e}")
