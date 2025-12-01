# Proyecto Angular 21 + Python + MySQL

Este proyecto combina Angular 21 en el frontend, Python Flask en el backend y MySQL como base de datos.

## Estructura del Proyecto

```
angular_cero/
├── frontend/          # Aplicación Angular 21
└── backend/           # API REST con Flask y MySQL
```

## Requisitos Previos

### Frontend
- Node.js 18.19+ o 20.11+
- npm

### Backend
- Python 3.8+
- MySQL 8.0+

## Configuración

### 1. Base de Datos MySQL

Crear la base de datos en MySQL:

```sql
CREATE DATABASE angular_cero_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Backend (Python Flask)

```bash
cd backend

# Crear y activar entorno virtual
python -m venv venv
.\venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
copy .env.example .env
# Editar .env con tus credenciales de MySQL

# Ejecutar el servidor
python app.py
```

El backend estará disponible en: `http://localhost:5000`

### 3. Frontend (Angular 21)

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar servidor de desarrollo
npm start
```

El frontend estará disponible en: `http://localhost:4200`

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/users` - Obtener todos los usuarios
- `POST /api/users` - Crear un nuevo usuario
- `GET /api/users/:id` - Obtener un usuario específico
- `PUT /api/users/:id` - Actualizar un usuario
- `DELETE /api/users/:id` - Eliminar un usuario

## Scripts Útiles

### Frontend
- `npm start` - Iniciar servidor de desarrollo
- `npm run build` - Compilar para producción
- `npm test` - Ejecutar tests

### Backend
- `python app.py` - Iniciar servidor Flask

## Tecnologías

### Frontend
- Angular 21
- TypeScript
- Angular Router
- RxJS

### Backend
- Python 3.x
- Flask
- Flask-CORS
- Flask-SQLAlchemy
- PyMySQL
- python-dotenv

### Base de Datos
- MySQL 8.0+

## Notas de Desarrollo

- El backend crea automáticamente las tablas en la base de datos al iniciar
- CORS está habilitado para permitir las peticiones desde el frontend
- Las variables de entorno se cargan desde el archivo `.env`
