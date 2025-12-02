import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { TravelService, Travel } from '../travel.service';

@Component({
  selector: 'app-travel-list',
  imports: [CommonModule, RouterLink],
  templateUrl: './travel-list.component.html',
  styleUrl: './travel-list.component.css'
})
export class TravelListComponent implements OnInit {
  travels: Travel[] = [];
  loading = false;
  error: string | null = null;

  constructor(private travelService: TravelService) {}

  ngOnInit(): void {
    this.loadTravels();
  }

  loadTravels(): void {
    this.loading = true;
    this.error = null;
    this.travelService.getTravels().subscribe({
      next: (data) => {
        this.travels = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar los viajes';
        this.loading = false;
        console.error(err);
      }
    });
  }

  deleteTravel(id: number): void {
    if (confirm('¿Estás seguro de eliminar este viaje?')) {
      this.travelService.deleteTravel(id).subscribe({
        next: () => {
          this.loadTravels();
        },
        error: (err) => {
          this.error = 'Error al eliminar el viaje';
          console.error(err);
        }
      });
    }
  }

  getImageUrl(travel: Travel): string {
    return travel.image_url || 'https://via.placeholder.com/300x200?text=' + encodeURIComponent(travel.destination);
  }
}
