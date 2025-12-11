from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

def add_details_columns():
    """Agregar columnas de detalles a la tabla travels"""
    try:
        with app.app_context():
            # Verificar si las columnas ya existen
            with db.engine.connect() as conn:
                # Intentar agregar cada columna individualmente
                columns = ['attractions', 'accommodations', 'restaurants', 'tips']
                
                for column in columns:
                    try:
                        conn.execute(text(f"ALTER TABLE travels ADD COLUMN {column} TEXT"))
                        conn.commit()
                        print(f"✓ Columna {column} agregada")
                    except Exception as e:
                        if 'Duplicate column name' in str(e):
                            print(f"  Columna {column} ya existe")
                        else:
                            print(f"  Error con columna {column}: {e}")
            
            print("\n✓ Proceso de migración completado")
            
            # Actualizar algunos viajes con datos de ejemplo
            import json
            
            print("\nAgregando datos de ejemplo...")
            
            sample_data = {
                'attractions': json.dumps([
                    'Torre Eiffel',
                    'Museo del Louvre',
                    'Arco del Triunfo',
                    'Catedral de Notre-Dame',
                    'Basílica del Sagrado Corazón'
                ]),
                'accommodations': json.dumps([
                    {
                        'name': 'Hotel Le Marais',
                        'type': 'Hotel 4 estrellas',
                        'description': 'Hotel boutique en el corazón del Marais, con elegantes habitaciones y desayuno incluido.'
                    },
                    {
                        'name': 'Apartamentos Montmartre',
                        'type': 'Apartamento',
                        'description': 'Acogedores apartamentos cerca de Montmartre, perfectos para familias.'
                    }
                ]),
                'restaurants': json.dumps([
                    {
                        'name': 'Le Comptoir du Relais',
                        'cuisine': 'Cocina Francesa',
                        'description': 'Bistró parisino clásico con excelente cocina tradicional francesa.'
                    },
                    {
                        'name': 'L\'As du Fallafel',
                        'cuisine': 'Comida Mediterránea',
                        'description': 'El mejor falafel de París, ubicado en el barrio judío.'
                    }
                ]),
                'tips': json.dumps([
                    'Compra el Paris Museum Pass para ahorrar en entradas',
                    'Usa el metro, es la forma más rápida de moverse',
                    'Visita los monumentos temprano para evitar multitudes',
                    'Prueba los croissants en cualquier boulangerie local'
                ])
            }
            
            with db.engine.connect() as conn:
                conn.execute(text("""
                    UPDATE travels 
                    SET attractions = :attractions,
                        accommodations = :accommodations,
                        restaurants = :restaurants,
                        tips = :tips
                    WHERE id = 1
                """), sample_data)
                conn.commit()
            
            print("✓ Datos de ejemplo agregados al primer viaje")
            
    except Exception as e:
        print(f"Error al agregar columnas: {e}")

if __name__ == '__main__':
    add_details_columns()
    print("\n¡Migración completada!")
