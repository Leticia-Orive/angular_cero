import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { UserService, User } from '../user.service';
import { TravelService, Travel } from '../travel.service';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.css']
})
export class AdminDashboardComponent implements OnInit {
  users: User[] = [];
  travels: Travel[] = [];
  loading = false;
  error: string | null = null;

  constructor(
    private userService: UserService,
    private travelService: TravelService
  ) {}

  ngOnInit(): void {
    this.loadData();
  }

  loadData(): void {
    this.loading = true;
    this.error = null;

    this.userService.getUsers().subscribe({
      next: (users) => {
        this.users = users;
      },
      error: (err) => {
        this.error = 'Error al cargar usuarios';
        console.error(err);
      }
    });

    this.travelService.getTravels().subscribe({
      next: (travels) => {
        this.travels = travels;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar viajes';
        console.error(err);
        this.loading = false;
      }
    });
  }

  deleteUser(id: number): void {
    if (confirm('¿Estás seguro de eliminar este usuario?')) {
      this.userService.deleteUser(id).subscribe({
        next: () => {
          this.users = this.users.filter(u => u.id !== id);
        },
        error: (err) => {
          this.error = 'Error al eliminar usuario';
          console.error(err);
        }
      });
    }
  }

  deleteTravel(id: number): void {
    if (confirm('¿Estás seguro de eliminar este viaje?')) {
      this.travelService.deleteTravel(id).subscribe({
        next: () => {
          this.travels = this.travels.filter(t => t.id !== id);
        },
        error: (err) => {
          this.error = 'Error al eliminar viaje';
          console.error(err);
        }
      });
    }
  }
}
