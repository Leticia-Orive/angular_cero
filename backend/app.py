from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración de la base de datos MySQL
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de ejemplo
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Modelo de Viajes (Catálogo de viajes disponibles)
class Travel(db.Model):
    __tablename__ = 'travels'
    
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500))
    price = db.Column(db.Float)
    country = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Modelo de Viajes del Usuario (Mis Viajes)
class UserTravel(db.Model):
    __tablename__ = 'user_travels'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    travel_id = db.Column(db.Integer, db.ForeignKey('travels.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(50), default='booked')  # booked, completed, cancelled
    notes = db.Column(db.Text)
    
    # Relaciones
    user = db.relationship('User', backref='user_travels')
    travel = db.relationship('Travel', backref='user_travels')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'travel_id': self.travel_id,
            'booking_date': self.booking_date.isoformat() if self.booking_date else None,
            'status': self.status,
            'notes': self.notes,
            'travel': self.travel.to_dict() if self.travel else None,
            'user': {'id': self.user.id, 'name': self.user.name, 'email': self.user.email} if self.user else None
        }
    
    def to_dict(self):
        return {
            'id': self.id,
            'destination': self.destination,
            'description': self.description,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_url': self.image_url,
            'price': self.price,
            'country': self.country,
            'duration': self.duration,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Rutas
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Backend is running'}), 200

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(
            name=data.get('name'),
            email=data.get('email')
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
            
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ========== RUTAS DE VIAJES ==========

@app.route('/api/travels', methods=['GET'])
def get_travels():
    try:
        travels = Travel.query.order_by(Travel.start_date.desc()).all()
        return jsonify([travel.to_dict() for travel in travels]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/travels', methods=['POST'])
def create_travel():
    try:
        data = request.get_json()
        from datetime import datetime
        
        new_travel = Travel(
            destination=data.get('destination'),
            description=data.get('description'),
            start_date=datetime.fromisoformat(data.get('start_date')),
            end_date=datetime.fromisoformat(data.get('end_date')),
            latitude=float(data.get('latitude')),
            longitude=float(data.get('longitude')),
            image_url=data.get('image_url'),
            price=float(data.get('price')) if data.get('price') else None
        )
        db.session.add(new_travel)
        db.session.commit()
        return jsonify(new_travel.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/travels/<int:travel_id>', methods=['GET'])
def get_travel(travel_id):
    try:
        travel = Travel.query.get_or_404(travel_id)
        return jsonify(travel.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 404

@app.route('/api/travels/<int:travel_id>', methods=['PUT'])
def update_travel(travel_id):
    try:
        travel = Travel.query.get_or_404(travel_id)
        data = request.get_json()
        from datetime import datetime
        
        if 'destination' in data:
            travel.destination = data['destination']
        if 'description' in data:
            travel.description = data['description']
        if 'start_date' in data:
            travel.start_date = datetime.fromisoformat(data['start_date'])
        if 'end_date' in data:
            travel.end_date = datetime.fromisoformat(data['end_date'])
        if 'latitude' in data:
            travel.latitude = float(data['latitude'])
        if 'longitude' in data:
            travel.longitude = float(data['longitude'])
        if 'image_url' in data:
            travel.image_url = data['image_url']
        if 'price' in data:
            travel.price = float(data['price']) if data['price'] else None
            
        db.session.commit()
        return jsonify(travel.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/travels/<int:travel_id>', methods=['DELETE'])
def delete_travel(travel_id):
    try:
        travel = Travel.query.get_or_404(travel_id)
        db.session.delete(travel)
        db.session.commit()
        return jsonify({'message': 'Travel deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# ========== RUTAS DE MIS VIAJES (USER TRAVELS) ==========

@app.route('/api/my-travels', methods=['GET'])
def get_my_travels():
    """Obtener todos los viajes del usuario (por defecto user_id=1)"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        user_travels = UserTravel.query.filter_by(user_id=user_id).order_by(UserTravel.booking_date.desc()).all()
        return jsonify([ut.to_dict() for ut in user_travels]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/my-travels', methods=['POST'])
def add_to_my_travels():
    """Agregar un viaje a 'Mis Viajes'"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 1)
        travel_id = data.get('travel_id')
        
        # Verificar si ya existe
        existing = UserTravel.query.filter_by(user_id=user_id, travel_id=travel_id).first()
        if existing:
            return jsonify({'error': 'Este viaje ya está en tus viajes', 'user_travel': existing.to_dict()}), 409
        
        new_user_travel = UserTravel(
            user_id=user_id,
            travel_id=travel_id,
            status=data.get('status', 'booked'),
            notes=data.get('notes', '')
        )
        db.session.add(new_user_travel)
        db.session.commit()
        return jsonify(new_user_travel.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/my-travels/<int:user_travel_id>', methods=['DELETE'])
def remove_from_my_travels(user_travel_id):
    """Eliminar un viaje de 'Mis Viajes'"""
    try:
        user_travel = UserTravel.query.get_or_404(user_travel_id)
        db.session.delete(user_travel)
        db.session.commit()
        return jsonify({'message': 'Travel removed from your travels'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/api/my-travels/<int:user_travel_id>', methods=['PUT'])
def update_my_travel(user_travel_id):
    """Actualizar el estado o notas de un viaje en 'Mis Viajes'"""
    try:
        user_travel = UserTravel.query.get_or_404(user_travel_id)
        data = request.get_json()
        
        if 'status' in data:
            user_travel.status = data['status']
        if 'notes' in data:
            user_travel.notes = data['notes']
            
        db.session.commit()
        return jsonify(user_travel.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
