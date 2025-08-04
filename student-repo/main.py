from fastapi import FastAPI

app = FastAPI(title="Test API")

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/test")
def get_test():
    return {"test": True}

@app.post("/items")
def create_item(item: dict):
    return {"item": item}

def helper_function():
    """Función auxiliar para testing"""
    return "helper"

class TestClass:
    """Clase de prueba"""
    def __init__(self):
        self.value = 42
