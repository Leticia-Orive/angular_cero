# Script para agregar viajes de ejemplo a la base de datos

from app import app, db, Travel
from datetime import datetime, timedelta

def seed_travels():
    with app.app_context():
        # Eliminar viajes existentes (opcional)
        print("Limpiando viajes existentes...")
        Travel.query.delete()
        
        # Lista de viajes de ejemplo
        sample_travels = [
            {
                'destination': 'París, Francia',
                'description': 'Ciudad del amor y la luz. Visita a la Torre Eiffel, Louvre y Campos Elíseos.',
                'start_date': datetime.now() + timedelta(days=30),
                'end_date': datetime.now() + timedelta(days=37),
                'latitude': 48.8566,
                'longitude': 2.3522,
                'image_url': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?auto=format&fit=crop&w=800&q=80',
                'price': 1500.00,
                'country': 'Francia',
                'duration': 7
            },
            {
                'destination': 'Tokio, Japón',
                'description': 'Mezcla perfecta de tradición y modernidad. Templos antiguos y tecnología futurista.',
                'start_date': datetime.now() + timedelta(days=60),
                'end_date': datetime.now() + timedelta(days=70),
                'latitude': 35.6762,
                'longitude': 139.6503,
                'image_url': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?auto=format&fit=crop&w=800&q=80',
                'price': 2200.00,
                'country': 'Japón',
                'duration': 10
            },
            {
                'destination': 'Nueva York, EE.UU.',
                'description': 'La ciudad que nunca duerme. Times Square, Central Park y la Estatua de la Libertad.',
                'start_date': datetime.now() + timedelta(days=15),
                'end_date': datetime.now() + timedelta(days=22),
                'latitude': 40.7128,
                'longitude': -74.0060,
                'image_url': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?auto=format&fit=crop&w=800&q=80',
                'price': 1800.00,
                'country': 'Estados Unidos',
                'duration': 7
            },
            {
                'destination': 'Roma, Italia',
                'description': 'Historia viva en cada esquina. Coliseo, Vaticano y auténtica comida italiana.',
                'start_date': datetime.now() + timedelta(days=45),
                'end_date': datetime.now() + timedelta(days=52),
                'latitude': 41.9028,
                'longitude': 12.4964,
                'image_url': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?auto=format&fit=crop&w=800&q=80',
                'price': 1400.00,
                'country': 'Italia',
                'duration': 7
            },
            {
                'destination': 'Barcelona, España',
                'description': 'Arte de Gaudí, playas mediterráneas y tapas deliciosas. La Sagrada Familia es imperdible.',
                'start_date': datetime.now() + timedelta(days=90),
                'end_date': datetime.now() + timedelta(days=97),
                'latitude': 41.3851,
                'longitude': 2.1734,
                'image_url': 'https://images.unsplash.com/photo-1583422409516-2895a77efded?auto=format&fit=crop&w=800&q=80',
                'price': 1200.00,
                'country': 'España',
                'duration': 7
            },
            {
                'destination': 'Bali, Indonesia',
                'description': 'Paraíso tropical con templos místicos, playas de ensueño y cultura fascinante.',
                'start_date': datetime.now() + timedelta(days=120),
                'end_date': datetime.now() + timedelta(days=134),
                'latitude': -8.3405,
                'longitude': 115.0920,
                'image_url': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?auto=format&fit=crop&w=800&q=80',
                'price': 1600.00,
                'country': 'Indonesia',
                'duration': 14
            },
            {
                'destination': 'Machu Picchu, Perú',
                'description': 'Antigua ciudad inca en las montañas. Una de las maravillas del mundo moderno.',
                'start_date': datetime.now() + timedelta(days=75),
                'end_date': datetime.now() + timedelta(days=82),
                'latitude': -13.1631,
                'longitude': -72.5450,
                'image_url': 'https://images.unsplash.com/photo-1587595431973-160d0d94add1?auto=format&fit=crop&w=800&q=80',
                'price': 1300.00,
                'country': 'Perú',
                'duration': 7
            },
            {
                'destination': 'Dubái, EAU',
                'description': 'Lujo y modernidad en el desierto. Burj Khalifa, playas y compras de clase mundial.',
                'start_date': datetime.now() + timedelta(days=100),
                'end_date': datetime.now() + timedelta(days=107),
                'latitude': 25.2048,
                'longitude': 55.2708,
                'image_url': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?auto=format&fit=crop&w=800&q=80',
                'price': 2000.00,
                'country': 'Emiratos Árabes Unidos',
                'duration': 7
            },
            {
                'destination': 'Santorini, Grecia',
                'description': 'Casas blancas con cúpulas azules sobre acantilados. Atardeceres inolvidables.',
                'start_date': datetime.now() + timedelta(days=50),
                'end_date': datetime.now() + timedelta(days=57),
                'latitude': 36.3932,
                'longitude': 25.4615,
                'image_url': 'https://images.unsplash.com/photo-1613395877344-13d4a8e0d49e?auto=format&fit=crop&w=800&q=80',
                'price': 1700.00,
                'country': 'Grecia',
                'duration': 7
            },
            {
                'destination': 'Islandia',
                'description': 'Tierra de hielo y fuego. Auroras boreales, géiseres y paisajes de otro planeta.',
                'start_date': datetime.now() + timedelta(days=150),
                'end_date': datetime.now() + timedelta(days=160),
                'latitude': 64.9631,
                'longitude': -19.0208,
                'image_url': 'https://images.unsplash.com/photo-1504829857797-ddff29c27927?auto=format&fit=crop&w=800&q=80',
                'price': 2500.00,
                'country': 'Islandia',
                'duration': 10
            },
            {
                'destination': 'Cancún, México',
                'description': 'Playas caribeñas de arena blanca, ruinas mayas y vida nocturna vibrante.',
                'start_date': datetime.now() + timedelta(days=20),
                'end_date': datetime.now() + timedelta(days=27),
                'latitude': 21.1619,
                'longitude': -86.8515,
                'image_url': 'https://images.unsplash.com/photo-1568402102990-bc541580b59f?auto=format&fit=crop&w=800&q=80',
                'price': 1100.00,
                'country': 'México',
                'duration': 7
            },
            {
                'destination': 'Londres, Reino Unido',
                'description': 'Historia, realeza y cultura. Big Ben, Buckingham Palace y los mejores museos.',
                'start_date': datetime.now() + timedelta(days=40),
                'end_date': datetime.now() + timedelta(days=47),
                'latitude': 51.5074,
                'longitude': -0.1278,
                'image_url': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?auto=format&fit=crop&w=800&q=80',
                'price': 1600.00,
                'country': 'Reino Unido',
                'duration': 7
            },
            {
                'destination': 'Ámsterdam, Países Bajos',
                'description': 'Canales pintorescos, museos de arte y bicicletas por todas partes.',
                'start_date': datetime.now() + timedelta(days=80),
                'end_date': datetime.now() + timedelta(days=85),
                'latitude': 52.3676,
                'longitude': 4.9041,
                'image_url': 'https://images.unsplash.com/photo-1534351590666-13e3e96b5017?auto=format&fit=crop&w=800&q=80',
                'price': 1300.00,
                'country': 'Países Bajos',
                'duration': 5
            },
            {
                'destination': 'Praga, República Checa',
                'description': 'Ciudad de cuento de hadas con arquitectura medieval y cerveza excepcional.',
                'start_date': datetime.now() + timedelta(days=110),
                'end_date': datetime.now() + timedelta(days=115),
                'latitude': 50.0755,
                'longitude': 14.4378,
                'image_url': 'https://images.unsplash.com/photo-1541849546-216549ae216d?auto=format&fit=crop&w=800&q=80',
                'price': 900.00,
                'country': 'República Checa',
                'duration': 5
            },
            {
                'destination': 'Sídney, Australia',
                'description': 'Ópera icónica, playas espectaculares y vida marina única. Gran Barrera de Coral.',
                'start_date': datetime.now() + timedelta(days=180),
                'end_date': datetime.now() + timedelta(days=195),
                'latitude': -33.8688,
                'longitude': 151.2093,
                'image_url': 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?auto=format&fit=crop&w=800&q=80',
                'price': 2800.00,
                'country': 'Australia',
                'duration': 15
            }
        ]
        
        print(f"Agregando {len(sample_travels)} viajes de ejemplo...")
        
        for travel_data in sample_travels:
            travel = Travel(**travel_data)
            db.session.add(travel)
        
        db.session.commit()
        print(f"✓ {len(sample_travels)} viajes agregados exitosamente!")
        
        # Mostrar los viajes agregados
        travels = Travel.query.all()
        print(f"\nTotal de viajes en la base de datos: {len(travels)}")
        print("\nViajes agregados:")
        for travel in travels:
            print(f"  - {travel.destination} ({travel.start_date.strftime('%d/%m/%Y')} - {travel.end_date.strftime('%d/%m/%Y')})")

if __name__ == '__main__':
    print("Iniciando población de viajes...\n")
    seed_travels()
    print("\n✓ Proceso completado!")
