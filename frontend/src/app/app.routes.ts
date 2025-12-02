import { Routes } from '@angular/router';
import { TravelListComponent } from './travel-list/travel-list.component';
import { TravelFormComponent } from './travel-form/travel-form.component';
import { TravelMapComponent } from './travel-map/travel-map.component';

export const routes: Routes = [
  { path: '', redirectTo: '/travels', pathMatch: 'full' },
  { path: 'travels', component: TravelListComponent },
  { path: 'travels/new', component: TravelFormComponent },
  { path: 'travels/edit/:id', component: TravelFormComponent },
  { path: 'travels/:id', component: TravelMapComponent },
  { path: '**', redirectTo: '/travels' }
];
