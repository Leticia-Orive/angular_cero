# Script para actualizar la tabla users con autenticación

import pymysql

def update_users_table():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            database='angular_cero_db'
        )
        
        cursor = connection.cursor()
        
        print("Actualizando tabla users para autenticación...")
        
        # Verificar si la columna password ya existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'angular_cero_db' 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'password'
        """)
        
        if cursor.fetchone()[0] == 0:
            print("Agregando columna 'password'...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN password VARCHAR(255) NOT NULL DEFAULT ''
            """)
            print("✓ Columna 'password' agregada")
        else:
            print("✓ Columna 'password' ya existe")
        
        # Verificar si la columna role ya existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_SCHEMA = 'angular_cero_db' 
            AND TABLE_NAME = 'users' 
            AND COLUMN_NAME = 'role'
        """)
        
        if cursor.fetchone()[0] == 0:
            print("Agregando columna 'role'...")
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN role VARCHAR(20) DEFAULT 'user'
            """)
            print("✓ Columna 'role' agregada")
        else:
            print("✓ Columna 'role' ya existe")
        
        connection.commit()
        print("\n✓ Migración completada exitosamente!")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error durante la migración: {e}")
        raise

if __name__ == '__main__':
    print("Iniciando actualización de tabla users...\n")
    update_users_table()
