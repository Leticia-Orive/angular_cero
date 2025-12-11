import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Accommodation {
  name: string;
  type: string;
  description: string;
}

export interface Restaurant {
  name: string;
  cuisine: string;
  description: string;
}

export interface Travel {
  id?: number;
  destination: string;
  description: string;
  start_date: string;
  end_date: string;
  latitude: number;
  longitude: number;
  image_url?: string;
  price?: number;
  country?: string;
  duration?: number;
  attractions?: string[];
  accommodations?: Accommodation[];
  restaurants?: Restaurant[];
  tips?: string[];
  created_at?: string;
}

@Injectable({
  providedIn: 'root'
})
export class TravelService {
  private apiUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) { }

  getTravels(): Observable<Travel[]> {
    return this.http.get<Travel[]>(`${this.apiUrl}/travels`);
  }

  getTravel(id: number): Observable<Travel> {
    return this.http.get<Travel>(`${this.apiUrl}/travels/${id}`);
  }

  getTravelById(id: number): Observable<Travel> {
    return this.http.get<Travel>(`${this.apiUrl}/travels/${id}`);
  }

  createTravel(travel: Travel): Observable<Travel> {
    return this.http.post<Travel>(`${this.apiUrl}/travels`, travel);
  }

  updateTravel(id: number, travel: Travel): Observable<Travel> {
    return this.http.put<Travel>(`${this.apiUrl}/travels/${id}`, travel);
  }

  deleteTravel(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/travels/${id}`);
  }
}
