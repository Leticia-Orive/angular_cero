import { Component, OnInit, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { TravelService, Travel } from '../travel.service';
import * as L from 'leaflet';

@Component({
  selector: 'app-travel-map',
  imports: [CommonModule],
  templateUrl: './travel-map.component.html',
  styleUrl: './travel-map.component.css'
})
export class TravelMapComponent implements OnInit, AfterViewInit {
  travel: Travel | null = null;
  loading = false;
  error: string | null = null;
  private map: L.Map | null = null;
  private marker: L.Marker | null = null;

  constructor(
    private travelService: TravelService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      if (params['id']) {
        this.loadTravel(+params['id']);
      }
    });
  }

  ngAfterViewInit(): void {
    this.initMap();
  }

  loadTravel(id: number): void {
    this.loading = true;
    this.travelService.getTravel(id).subscribe({
      next: (travel) => {
        this.travel = travel;
        this.loading = false;
        this.updateMap();
      },
      error: (err) => {
        this.error = 'Error al cargar el viaje';
        this.loading = false;
        console.error(err);
      }
    });
  }

  initMap(): void {
    // Configurar el icono por defecto de Leaflet
    const iconRetinaUrl = 'assets/marker-icon-2x.png';
    const iconUrl = 'assets/marker-icon.png';
    const shadowUrl = 'assets/marker-shadow.png';

    const iconDefault = L.icon({
      iconRetinaUrl,
      iconUrl,
      shadowUrl,
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      tooltipAnchor: [16, -28],
      shadowSize: [41, 41]
    });

    L.Marker.prototype.options.icon = iconDefault;

    // Inicializar el mapa con una vista por defecto
    this.map = L.map('map').setView([0, 0], 2);

    // Agregar capa de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors',
      maxZoom: 19
    }).addTo(this.map);
  }

  updateMap(): void {
    if (this.map && this.travel) {
      // Remover marcador anterior si existe
      if (this.marker) {
        this.marker.remove();
      }

      // Centrar el mapa en las coordenadas del viaje
      const coordinates: L.LatLngExpression = [this.travel.latitude, this.travel.longitude];
      this.map.setView(coordinates, 13);

      // Agregar marcador
      this.marker = L.marker(coordinates).addTo(this.map);

      // Agregar popup con información
      const popupContent = `
        <div class="map-popup">
          <h3>${this.travel.destination}</h3>
          <p>${this.travel.description}</p>
          ${this.travel.price ? `<p><strong>Precio:</strong> $${this.travel.price}</p>` : ''}
        </div>
      `;

      this.marker.bindPopup(popupContent).openPopup();
    }
  }

  goBack(): void {
    this.router.navigate(['/travels']);
  }

  editTravel(): void {
    if (this.travel?.id) {
      this.router.navigate(['/travels/edit', this.travel.id]);
    }
  }

  getImageUrl(): string {
    return this.travel?.image_url || 'https://via.placeholder.com/400x200?text=' + encodeURIComponent(this.travel?.destination || 'Viaje');
  }
}
