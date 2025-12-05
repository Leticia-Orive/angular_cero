import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TravelService, Travel } from '../travel.service';
import { HttpClient } from '@angular/common/http';

export interface UserTravel {
  id?: number;
  user_id: number;
  travel_id: number;
  booking_date?: string;
  status: string;
  notes?: string;
  travel?: Travel;
}

@Component({
  selector: 'app-travel-catalog',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './travel-catalog.component.html',
  styleUrls: ['./travel-catalog.component.css']
})
export class TravelCatalogComponent implements OnInit {
  availableTravels: Travel[] = [];
  myTravels: UserTravel[] = [];
  filteredTravels: Travel[] = [];
  loading = false;
  error: string | null = null;
  successMessage: string | null = null;
  searchTerm = '';
  selectedCountry = '';
  countries: string[] = [];
  maxPrice: number = 5000;
  currentMaxPrice: number = 5000;
  userId = 1; // Por defecto, usuario con ID 1

  private apiUrl = 'http://localhost:5000/api';

  constructor(
    private travelService: TravelService,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;
    this.error = null;
    console.log('🔄 Iniciando carga de viajes...');

    // Cargar viajes disponibles
    this.travelService.getTravels().subscribe({
      next: (travels) => {
        console.log('✅ Viajes recibidos:', travels.length, travels);
        this.availableTravels = travels;
        this.filteredTravels = travels;
        this.countries = [...new Set(travels.map(t => t.country).filter(c => c))].sort() as string[];
        const prices = travels.map(t => t.price || 0);
        this.maxPrice = prices.length > 0 ? Math.max(...prices, 5000) : 5000;
        this.currentMaxPrice = this.maxPrice;

        // Cargar mis viajes después de tener los viajes disponibles
        this.loadMyTravels();
      },
      error: (err) => {
        console.error('❌ Error al cargar viajes:', err);
        this.error = 'Error al cargar viajes disponibles. Verifica que el backend esté corriendo.';
        this.loading = false;
      }
    });
  }

  loadMyTravels(): void {
    console.log('🔄 Cargando mis viajes...');
    this.http.get<UserTravel[]>(`${this.apiUrl}/my-travels?user_id=${this.userId}`).subscribe({
      next: (myTravels) => {
        console.log('✅ Mis viajes recibidos:', myTravels.length);
        this.myTravels = myTravels;
        this.loading = false;
        console.log('📊 Estado final - Loading:', this.loading, 'Viajes disponibles:', this.availableTravels.length, 'Viajes filtrados:', this.filteredTravels.length);
      },
      error: (err) => {
        console.error('⚠️ Error al cargar mis viajes:', err);
        this.loading = false;
      }
    });
  }

  filterTravels(): void {
    this.filteredTravels = this.availableTravels.filter(travel => {
      const matchesSearch = travel.destination.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
                           (travel.country && travel.country.toLowerCase().includes(this.searchTerm.toLowerCase())) ||
                           (travel.description && travel.description.toLowerCase().includes(this.searchTerm.toLowerCase()));

      const matchesCountry = !this.selectedCountry || travel.country === this.selectedCountry;
      const matchesPrice = (travel.price || 0) <= this.currentMaxPrice;

      return matchesSearch && matchesCountry && matchesPrice;
    });
  }

  onSearchChange(event: Event): void {
    this.searchTerm = (event.target as HTMLInputElement).value;
    this.filterTravels();
  }

  onCountryChange(event: Event): void {
    this.selectedCountry = (event.target as HTMLSelectElement).value;
    this.filterTravels();
  }

  onPriceChange(event: Event): void {
    this.currentMaxPrice = Number((event.target as HTMLInputElement).value);
    this.filterTravels();
  }

  resetFilters(): void {
    this.searchTerm = '';
    this.selectedCountry = '';
    this.currentMaxPrice = this.maxPrice;
    this.filteredTravels = this.availableTravels;
  }

  isInMyTravels(travelId: number | undefined): boolean {
    if (!travelId) return false;
    return this.myTravels.some(ut => ut.travel_id === travelId);
  }

  addToMyTravels(travel: Travel): void {
    if (!travel.id) return;

    this.error = null;
    this.successMessage = null;

    const data = {
      user_id: this.userId,
      travel_id: travel.id,
      status: 'booked'
    };

    this.http.post<UserTravel>(`${this.apiUrl}/my-travels`, data).subscribe({
      next: (userTravel) => {
        this.myTravels.push(userTravel);
        this.successMessage = `¡${travel.destination} agregado a tus viajes!`;
        setTimeout(() => this.successMessage = null, 3000);
      },
      error: (err) => {
        if (err.status === 409) {
          this.error = 'Este viaje ya está en tu lista';
        } else {
          this.error = 'Error al agregar el viaje';
        }
        setTimeout(() => this.error = null, 3000);
        console.error(err);
      }
    });
  }

  removeFromMyTravels(userTravelId: number | undefined): void {
    if (!userTravelId) return;

    this.http.delete(`${this.apiUrl}/my-travels/${userTravelId}`).subscribe({
      next: () => {
        this.myTravels = this.myTravels.filter(ut => ut.id !== userTravelId);
        this.successMessage = '¡Viaje eliminado de tu lista!';
        setTimeout(() => this.successMessage = null, 3000);
      },
      error: (err) => {
        this.error = 'Error al eliminar el viaje';
        setTimeout(() => this.error = null, 3000);
        console.error(err);
      }
    });
  }

  getUserTravelId(travelId: number | undefined): number | undefined {
    if (!travelId) return undefined;
    return this.myTravels.find(ut => ut.travel_id === travelId)?.id;
  }
}
