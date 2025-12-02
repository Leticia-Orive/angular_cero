# Script para verificar y crear la base de datos MySQL

import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'angular_cero_db')

def check_and_create_database():
    try:
        # Conectar a MySQL sin especificar la base de datos
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD
        )
        
        cursor = connection.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute(f"SHOW DATABASES LIKE '{DB_NAME}'")
        result = cursor.fetchone()
        
        if result:
            print(f"✓ Base de datos '{DB_NAME}' ya existe")
        else:
            # Crear la base de datos
            cursor.execute(f"CREATE DATABASE {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✓ Base de datos '{DB_NAME}' creada exitosamente")
        
        cursor.close()
        connection.close()
        return True
        
    except pymysql.Error as e:
        print(f"✗ Error al conectar con MySQL: {e}")
        print("\nAsegúrate de que:")
        print("1. MySQL esté instalado y corriendo")
        print("2. Las credenciales en .env sean correctas")
        print("3. El usuario tenga permisos para crear bases de datos")
        return False

if __name__ == '__main__':
    print("Verificando conexión a MySQL...")
    print(f"Host: {DB_HOST}:{DB_PORT}")
    print(f"Usuario: {DB_USER}")
    print(f"Base de datos: {DB_NAME}\n")
    
    if check_and_create_database():
        print("\n✓ Todo listo. Puedes ejecutar: python app.py")
    else:
        print("\n✗ Hay problemas con la configuración de MySQL")
