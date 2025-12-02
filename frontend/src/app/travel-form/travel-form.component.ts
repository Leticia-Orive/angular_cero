import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';
import { TravelService, Travel } from '../travel.service';

@Component({
  selector: 'app-travel-form',
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './travel-form.component.html',
  styleUrl: './travel-form.component.css'
})
export class TravelFormComponent implements OnInit {
  travelForm: FormGroup;
  isEditMode = false;
  travelId: number | null = null;
  loading = false;
  error: string | null = null;

  constructor(
    private fb: FormBuilder,
    private travelService: TravelService,
    private router: Router,
    private route: ActivatedRoute
  ) {
    this.travelForm = this.fb.group({
      destination: ['', Validators.required],
      description: ['', Validators.required],
      start_date: ['', Validators.required],
      end_date: ['', Validators.required],
      latitude: ['', [Validators.required, Validators.min(-90), Validators.max(90)]],
      longitude: ['', [Validators.required, Validators.min(-180), Validators.max(180)]],
      image_url: [''],
      price: ['']
    });
  }

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      if (params['id']) {
        this.isEditMode = true;
        this.travelId = +params['id'];
        this.loadTravel(this.travelId);
      }
    });
  }

  loadTravel(id: number): void {
    this.loading = true;
    this.travelService.getTravel(id).subscribe({
      next: (travel) => {
        this.travelForm.patchValue({
          destination: travel.destination,
          description: travel.description,
          start_date: travel.start_date,
          end_date: travel.end_date,
          latitude: travel.latitude,
          longitude: travel.longitude,
          image_url: travel.image_url,
          price: travel.price
        });
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar el viaje';
        this.loading = false;
        console.error(err);
      }
    });
  }

  onSubmit(): void {
    if (this.travelForm.valid) {
      this.loading = true;
      this.error = null;

      const travelData: Travel = this.travelForm.value;

      const request = this.isEditMode && this.travelId
        ? this.travelService.updateTravel(this.travelId, travelData)
        : this.travelService.createTravel(travelData);

      request.subscribe({
        next: () => {
          this.router.navigate(['/travels']);
        },
        error: (err) => {
          this.error = 'Error al guardar el viaje';
          this.loading = false;
          console.error(err);
        }
      });
    }
  }

  useCurrentLocation(): void {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          this.travelForm.patchValue({
            latitude: position.coords.latitude.toFixed(6),
            longitude: position.coords.longitude.toFixed(6)
          });
        },
        (error) => {
          console.error('Error getting location', error);
          alert('No se pudo obtener la ubicación actual');
        }
      );
    } else {
      alert('Geolocalización no soportada por tu navegador');
    }
  }

  cancel(): void {
    this.router.navigate(['/travels']);
  }
}
