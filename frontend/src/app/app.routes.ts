import { Routes } from '@angular/router';
import { TravelListComponent } from './travel-list/travel-list.component';
import { TravelFormComponent } from './travel-form/travel-form.component';
import { TravelMapComponent } from './travel-map/travel-map.component';
import { AdminDashboardComponent } from './admin-dashboard/admin-dashboard.component';
import { ClientDashboardComponent } from './client-dashboard/client-dashboard.component';

export const routes: Routes = [
  { path: '', redirectTo: '/client', pathMatch: 'full' },
  { path: 'client', component: ClientDashboardComponent },
  { path: 'admin', component: AdminDashboardComponent },
  { path: 'travels', component: TravelListComponent },
  { path: 'travels/new', component: TravelFormComponent },
  { path: 'travels/edit/:id', component: TravelFormComponent },
  { path: 'travels/:id', component: TravelMapComponent },
  { path: '**', redirectTo: '/client' }
];
