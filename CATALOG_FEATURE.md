# Catálogo de Viajes - Nueva Funcionalidad

## 🎯 Descripción

He creado un nuevo componente de **Catálogo de Viajes** que te permite:
- Ver todos los viajes disponibles
- Filtrar viajes por destino, país y precio
- Agregar viajes a "Mis Viajes" con un solo clic
- Ver un resumen de tus viajes en la barra lateral
- Gestionar tus viajes reservados

## 🚀 Características Principales

### 1. Catálogo de Viajes (`/catalog`)
- **Vista de tarjetas** con imágenes, descripciones y precios
- **Filtros avanzados**: búsqueda por texto, país y rango de precio
- **Indicador visual** de viajes ya agregados a "Mis Viajes"
- **Botón de agregar/eliminar** dinámico según el estado del viaje
- **Contador de resultados** filtrados

### 2. Sidebar de "Mis Viajes"
- Lista compacta de viajes agregados
- Contador de viajes totales
- Botón rápido para eliminar viajes
- Enlace directo a la vista completa de "Mis Viajes"

### 3. Backend API Actualizado

#### Nuevos Endpoints:

**GET `/api/my-travels?user_id=1`**
- Obtiene todos los viajes del usuario
- Devuelve información completa del viaje y del usuario

**POST `/api/my-travels`**
```json
{
  "user_id": 1,
  "travel_id": 5,
  "status": "booked",
  "notes": "Viaje de aniversario"
}
```
- Agrega un viaje a "Mis Viajes"
- Previene duplicados (devuelve error 409 si ya existe)

**DELETE `/api/my-travels/{id}`**
- Elimina un viaje de "Mis Viajes"

**PUT `/api/my-travels/{id}`**
- Actualiza el estado o notas de un viaje reservado

### 4. Modelo de Datos

#### Tabla `user_travels`
- `id`: ID único
- `user_id`: ID del usuario (FK a users)
- `travel_id`: ID del viaje (FK a travels)
- `booking_date`: Fecha de reserva (automática)
- `status`: Estado del viaje (booked, completed, cancelled)
- `notes`: Notas personales del usuario

## 📋 Navegación Actualizada

La barra de navegación ahora incluye:
- 🌍 **Catálogo** - Ver y agregar viajes disponibles
- ✈️ **Mis Viajes** - Gestionar tus viajes reservados
- 👤 **Cliente** - Vista de cliente original
- ⚙️ **Admin** - Panel de administración

## 🎨 Diseño

- **Layout de 2 columnas**: Filtros/Mis Viajes a la izquierda, catálogo a la derecha
- **Diseño responsive**: Se adapta a diferentes tamaños de pantalla
- **Animaciones suaves**: Mensajes de éxito/error con animaciones
- **Badges visuales**: Indicadores de estado en las tarjetas

## 💡 Uso

1. **Ver viajes disponibles**: Navega a `/catalog`
2. **Filtrar viajes**: Usa los filtros de la barra lateral
3. **Agregar a Mis Viajes**: Haz clic en "+ Agregar a Mis Viajes"
4. **Ver confirmación**: Aparece un mensaje de éxito y el viaje se agrega a la sidebar
5. **Gestionar viajes**: Elimina viajes con el botón "✕" o desde `/travels`

## 🔧 Archivos Creados/Modificados

### Frontend:
- `travel-catalog/travel-catalog.component.ts`
- `travel-catalog/travel-catalog.component.html`
- `travel-catalog/travel-catalog.component.css`
- `app.routes.ts` (actualizado)
- `app.html` (navegación actualizada)

### Backend:
- `app.py` (nuevos modelos y rutas)
- `create_user_travels_table.py` (script de migración)

## 🗄️ Base de Datos

La tabla `user_travels` fue creada con constraints de integridad:
- Foreign keys a `users` y `travels`
- Índice único para evitar duplicados (user_id, travel_id)
- Cascade delete para mantener integridad referencial

## 📱 Responsive

El diseño se adapta a:
- **Desktop**: Layout de 2 columnas
- **Tablet**: Filtros en fila horizontal
- **Mobile**: Layout de 1 columna, filtros apilados

¡Disfruta explorando y agregando viajes a tu lista! 🌍✈️
