import asyncio
import aiohttp
import time
from typing import List

# Función síncrona tradicional
def sync_fetch_data(url: str) -> str:
    time.sleep(1)  # Simula llamada a API
    return f"Datos de {url}"

# Función asíncrona
async def async_fetch_data(url: str) -> str:
    await asyncio.sleep(1)  # Simula llamada a API asíncrona
    return f"Datos de {url}"

# Múltiples llamadas síncronas
def sync_fetch_multiple(urls: List[str]) -> List[str]:
    start_time = time.time()
    results = []
    for url in urls:
        result = sync_fetch_data(url)
        results.append(result)
    
    end_time = time.time()
    print(f"Síncrono tomó: {end_time - start_time:.2f} segundos")
    return results

# Múltiples llamadas asíncronas
async def async_fetch_multiple(urls: List[str]) -> List[str]:
    start_time = time.time()
    
    # Crear todas las tareas
    tasks = [async_fetch_data(url) for url in urls]
    
    # Esperar que todas terminen
    results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Asíncrono tomó: {end_time - start_time:.2f} segundos")
    return results

# Ejemplo con aiohttp (HTTP client asíncrono)
async def fetch_real_url(session: aiohttp.ClientSession, url: str) -> dict:
    try:
        async with session.get(url) as response:
            return {
                "url": url,
                "status": response.status,
                "content_length": len(await response.text())
            }
    except Exception as e:
        return {
            "url": url,
            "error": str(e)
        }

async def fetch_multiple_urls(urls: List[str]) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_real_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Context manager asíncrono
class AsyncTimer:
    def __init__(self, name: str):
        self.name = name
    
    async def __aenter__(self):
        self.start_time = time.time()
        print(f"Iniciando {self.name}")
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        print(f"{self.name} tomó {end_time - self.start_time:.2f} segundos")

# Ejemplo de uso principal
async def main():
    urls = [
        "http://ejemplo1.com",
        "http://ejemplo2.com",
        "http://ejemplo3.com"
    ]
    
    print("=== Comparación Síncrono vs Asíncrono ===")
    
    # Llamadas síncronas
    sync_results = sync_fetch_multiple(urls)
    print("Resultados síncronos:", sync_results[:2])
    
    # Llamadas asíncronas
    async_results = await async_fetch_multiple(urls)
    print("Resultados asíncronos:", async_results[:2])
    
    print("\n=== Ejemplo con Context Manager Asíncrono ===")
    async with AsyncTimer("Operación compleja"):
        await asyncio.sleep(1)
        print("Procesando datos...")
    
    print("\n=== Ejemplo con URLs reales ===")
    real_urls = [
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/200",
        "https://httpbin.org/json"
    ]
    
    try:
        real_results = await fetch_multiple_urls(real_urls)
        for result in real_results:
            print(f"URL: {result['url']}, Status: {result.get('status', 'Error')}")
    except Exception as e:
        print(f"Error al obtener URLs: {e}")

if __name__ == "__main__":
    # Ejecutar el programa asíncrono
    asyncio.run(main())
