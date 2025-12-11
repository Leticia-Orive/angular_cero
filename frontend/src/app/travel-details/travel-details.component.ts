import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { TravelService, Travel } from '../travel.service';

@Component({
  selector: 'app-travel-details',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './travel-details.component.html',
  styleUrls: ['./travel-details.component.css']
})
export class TravelDetailsComponent implements OnInit {
  travel: Travel | null = null;
  loading = false;
  error: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private travelService: TravelService
  ) {}

  ngOnInit(): void {
    const id = this.route.snapshot.paramMap.get('id');
    if (id) {
      this.loadTravelDetails(+id);
    } else {
      this.error = 'ID de viaje no válido';
    }
  }

  loadTravelDetails(id: number): void {
    this.loading = true;
    this.error = null;

    this.travelService.getTravelById(id).subscribe({
      next: (travel) => {
        this.travel = travel;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar los detalles del viaje';
        this.loading = false;
        console.error(err);
      }
    });
  }

  goBack(): void {
    this.router.navigate(['/catalog']);
  }

  addToMyTravels(): void {
    if (this.travel) {
      // Lógica para agregar a mis viajes
      console.log('Agregar viaje:', this.travel.id);
    }
  }
}
