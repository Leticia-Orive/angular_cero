# Script para crear la tabla user_travels

import pymysql

def create_user_travels_table():
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
        
        print("Verificando y creando tabla user_travels...")
        
        # Verificar si la tabla ya existe
        cursor.execute("""
            SELECT COUNT(*) 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'angular_cero_db' 
            AND TABLE_NAME = 'user_travels'
        """)
        
        if cursor.fetchone()[0] == 0:
            print("Creando tabla user_travels...")
            cursor.execute("""
                CREATE TABLE user_travels (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    travel_id INT NOT NULL,
                    booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(50) DEFAULT 'booked',
                    notes TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (travel_id) REFERENCES travels(id) ON DELETE CASCADE,
                    UNIQUE KEY unique_user_travel (user_id, travel_id)
                )
            """)
            print("✓ Tabla 'user_travels' creada exitosamente")
        else:
            print("✓ Tabla 'user_travels' ya existe")
        
        connection.commit()
        print("\n✓ Proceso completado!")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"Error durante la creación de la tabla: {e}")
        raise

if __name__ == '__main__':
    print("Iniciando creación de tabla user_travels...\n")
    create_user_travels_table()
