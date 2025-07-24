from typing import List, Dict, Optional, Union
from datetime import datetime

# Tipos básicos
def greet(name: str) -> str:
    return f"Hola, {name}!"

def calculate_age(birth_year: int) -> int:
    current_year = datetime.now().year
    return current_year - birth_year

# Tipos complejos
def process_scores(scores: List[float]) -> Dict[str, float]:
    return {
        "average": sum(scores) / len(scores),
        "max": max(scores),
        "min": min(scores)
    }

# Tipos opcionales
def create_user(name: str, email: Optional[str] = None) -> Dict[str, str]:
    user = {"name": name}
    if email:
        user["email"] = email
    return user

# Union types (Python 3.10+: int | str)
def process_id(user_id: Union[int, str]) -> str:
    return str(user_id).upper()

# Ejemplos de uso
if __name__ == "__main__":
    print(greet("Juan"))
    print(calculate_age(1990))
    print(process_scores([85.5, 92.0, 78.5, 95.0]))
    print(create_user("María", "maria@email.com"))
    print(process_id(12345))
