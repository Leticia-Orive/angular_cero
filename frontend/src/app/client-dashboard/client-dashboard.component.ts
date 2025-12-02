import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { TravelService, Travel } from '../travel.service';

@Component({
  selector: 'app-client-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './client-dashboard.component.html',
  styleUrls: ['./client-dashboard.component.css']
})
export class ClientDashboardComponent implements OnInit {
  travels: Travel[] = [];
  filteredTravels: Travel[] = [];
  loading = false;
  error: string | null = null;
  searchTerm = '';
  selectedCountry = '';
  countries: string[] = [];
  maxPrice: number = 5000;
  currentMaxPrice: number = 5000;

  constructor(private travelService: TravelService) {}

  ngOnInit(): void {
    this.loadTravels();
  }

  loadTravels(): void {
    this.loading = true;
    this.error = null;

    this.travelService.getTravels().subscribe({
      next: (travels) => {
        this.travels = travels;
        this.filteredTravels = travels;
        this.countries = [...new Set(travels.map(t => t.country).filter(c => c))].sort() as string[];
        const prices = travels.map(t => t.price || 0);
        this.maxPrice = prices.length > 0 ? Math.max(...prices, 5000) : 5000;
        this.currentMaxPrice = this.maxPrice;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar viajes';
        console.error(err);
        this.loading = false;
      }
    });
  }

  filterTravels(): void {
    this.filteredTravels = this.travels.filter(travel => {
      const matchesSearch = travel.destination.toLowerCase().includes(this.searchTerm.toLowerCase()) ||
                           (travel.country && travel.country.toLowerCase().includes(this.searchTerm.toLowerCase())) ||
                           (travel.description && travel.description.toLowerCase().includes(this.searchTerm.toLowerCase()));

      const matchesCountry = !this.selectedCountry || travel.country === this.selectedCountry;
      const matchesPrice = (travel.price || 0) <= this.currentMaxPrice;      return matchesSearch && matchesCountry && matchesPrice;
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
    this.filteredTravels = this.travels;
  }
}
