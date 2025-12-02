# Script para migrar la base de datos y agregar las nuevas columnas

from app import app, db
import pymysql

def migrate_database():
    with app.app_context():
        try:
            # Conectar a la base de datos
            connection = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                password='123456',
                database='angular_cero_db'
            )
            
            cursor = connection.cursor()
            
            print("Verificando y agregando columnas faltantes...")
            
            # Verificar si la columna 'country' existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'angular_cero_db' 
                AND TABLE_NAME = 'travels' 
                AND COLUMN_NAME = 'country'
            """)
            
            if cursor.fetchone()[0] == 0:
                print("Agregando columna 'country'...")
                cursor.execute("""
                    ALTER TABLE travels 
                    ADD COLUMN country VARCHAR(100) AFTER price
                """)
                print("✓ Columna 'country' agregada")
            else:
                print("✓ Columna 'country' ya existe")
            
            # Verificar si la columna 'duration' existe
            cursor.execute("""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.COLUMNS 
                WHERE TABLE_SCHEMA = 'angular_cero_db' 
                AND TABLE_NAME = 'travels' 
                AND COLUMN_NAME = 'duration'
            """)
            
            if cursor.fetchone()[0] == 0:
                print("Agregando columna 'duration'...")
                cursor.execute("""
                    ALTER TABLE travels 
                    ADD COLUMN duration INT AFTER country
                """)
                print("✓ Columna 'duration' agregada")
            else:
                print("✓ Columna 'duration' ya existe")
            
            connection.commit()
            print("\n✓ Migración completada exitosamente!")
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            print(f"Error durante la migración: {e}")
            raise

if __name__ == '__main__':
    print("Iniciando migración de base de datos...\n")
    migrate_database()
