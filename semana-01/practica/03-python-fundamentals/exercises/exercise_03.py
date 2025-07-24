"""
Ejercicio 3: Programación Asíncrona Práctica

Instrucciones:
1. Implementa funciones asíncronas
2. Usa asyncio para concurrencia
3. Maneja errores apropiadamente
"""

import asyncio
import aiohttp
import time
from typing import List, Dict, Optional

# TODO: Implementar simulador de base de datos asíncrona
class AsyncDatabase:
    """
    Simulador de base de datos asíncrona.
    """
    
    def __init__(self):
        self.users = {}
        self.delay = 0.1  # Simula latencia de BD
    
    async def get_user(self, user_id: int) -> Optional[Dict]:
        """
        Obtiene un usuario por ID.
        
        Args:
            user_id: ID del usuario
            
        Returns:
            Diccionario con datos del usuario o None
        """
        # TODO: Implementar con delay asíncrono
        pass
    
    async def create_user(self, user_data: Dict) -> Dict:
        """
        Crea un nuevo usuario.
        
        Args:
            user_data: Datos del usuario
            
        Returns:
            Usuario creado con ID asignado
        """
        # TODO: Implementar con delay asíncrono
        pass
    
    async def get_multiple_users(self, user_ids: List[int]) -> List[Dict]:
        """
        Obtiene múltiples usuarios concurrentemente.
        
        Args:
            user_ids: Lista de IDs de usuarios
            
        Returns:
            Lista de usuarios (sin None)
        """
        # TODO: Usar asyncio.gather para concurrencia
        pass

# TODO: Implementar cliente de API asíncrono
class AsyncAPIClient:
    """
    Cliente para llamadas a APIs externas.
    """
    
    def __init__(self):
        self.base_url = "https://jsonplaceholder.typicode.com"
    
    async def fetch_post(self, post_id: int) -> Optional[Dict]:
        """
        Obtiene un post por ID.
        
        Args:
            post_id: ID del post
            
        Returns:
            Datos del post o None si hay error
        """
        # TODO: Usar aiohttp para llamada HTTP
        pass
    
    async def fetch_multiple_posts(self, post_ids: List[int]) -> List[Dict]:
        """
        Obtiene múltiples posts concurrentemente.
        
        Args:
            post_ids: Lista de IDs de posts
            
        Returns:
            Lista de posts obtenidos exitosamente
        """
        # TODO: Implementar con manejo de errores
        pass

# TODO: Implementar procesador de datos asíncrono
async def process_user_data(db: AsyncDatabase, api: AsyncAPIClient, user_id: int) -> Dict:
    """
    Procesa datos de usuario combinando BD local y API externa.
    
    Args:
        db: Instancia de AsyncDatabase
        api: Instancia de AsyncAPIClient
        user_id: ID del usuario
        
    Returns:
        Diccionario con datos procesados
    """
    # TODO: Obtener datos de usuario y posts concurrentemente
    # TODO: Combinar datos y retornar resultado
    pass

# TODO: Implementar función principal
async def main():
    """
    Función principal que demuestra todas las funcionalidades.
    """
    # Inicializar componentes
    db = AsyncDatabase()
    api = AsyncAPIClient()
    
    # Crear usuarios de prueba
    users_data = [
        {"name": "Juan Pérez", "email": "juan@email.com"},
        {"name": "María García", "email": "maria@email.com"},
        {"name": "Pedro López", "email": "pedro@email.com"}
    ]
    
    print("=== Creando usuarios ===")
    # TODO: Crear usuarios concurrentemente
    
    print("\n=== Obteniendo usuarios ===")
    # TODO: Obtener usuarios creados
    
    print("\n=== Procesando datos de usuarios ===")
    # TODO: Procesar datos de usuarios con API externa
    
    print("\n=== Midiendo rendimiento ===")
    # TODO: Comparar rendimiento síncrono vs asíncrono

if __name__ == "__main__":
    # Ejecutar programa asíncrono
    asyncio.run(main())
