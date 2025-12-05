from app import app, db, Travel

def check_images():
    with app.app_context():
        travels = Travel.query.all()
        print(f"\nTotal de viajes: {len(travels)}")
        print("\n--- URLs de imágenes ---")
        for travel in travels:
            print(f"\nID: {travel.id}")
            print(f"Destino: {travel.destination}")
            print(f"Image URL: {travel.image_url}")
            print("-" * 50)

if __name__ == '__main__':
    check_images()
