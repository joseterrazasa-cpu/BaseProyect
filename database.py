import os
import certifi
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# --- Configuración (Usando variables de entorno) ---
# Usa os.getenv para obtener la URI y el nombre de la BD. 
# Si no encuentra la variable, usa el valor predeterminado (fallback).
# NOTA: Asegúrate de que tu archivo .env contenga la línea MONGO_URI="..."
MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://DonTrucho:FsRIylMvM2DrwjDz@cluster0.econnfj.mongodb.net/?appName=Cluster0') 
DATABASE_NAME = os.getenv('DATABASE_NAME', 'Db_Don_Trucho')
ca = certifi.where()

def dbConnection():
    """Conectar a MongoDB y retornar la base de datos."""
    try:
        # Configuración de timeout de conexión
        client = MongoClient(
            MONGO_URI, 
            tlsCAFile=ca, 
            serverSelectionTimeoutMS=5000  # Añadimos el timeout de 5 segundos
        )
        
        # Probar la conexión explícitamente
        client.admin.command('ping')
        
        db = client[DATABASE_NAME]
        print(f"Conexión a MongoDB Atlas Exitosa: {DATABASE_NAME}")
        
        return db
        
    # Manejo de errores específicos (tomado de la Opción 2)
    except ServerSelectionTimeoutError:
        print("ERROR DE CONEXIÓN: No se pudo conectar a MongoDB Atlas (Timeout).")
        return None
    except ConnectionFailure as e:
        print(f"ERROR DE CONEXIÓN (General): {e}")
        return None
    except Exception as e:
        print(f"ERROR DESCONOCIDO durante la conexión: {e}")
        return None
