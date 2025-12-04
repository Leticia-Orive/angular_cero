import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { BehaviorSubject, Observable, from, throwError } from 'rxjs';
import { switchMap, catchError } from 'rxjs/operators';

export interface User {
  id: number;
  name: string;
  email: string;
  role: string;
}

export interface AuthResponse {
  message: string;
  user: User;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:5000/api/auth';
  private currentUserSubject: BehaviorSubject<User | null>;
  public currentUser: Observable<User | null>;

  constructor(private router: Router) {
    this.currentUserSubject = new BehaviorSubject<User | null>(null);
    this.currentUser = this.currentUserSubject.asObservable();
    this.checkCurrentUser();
  }

  public get currentUserValue(): User | null {
    return this.currentUserSubject.value;
  }

  checkCurrentUser(): void {
    from(
      fetch(`${this.apiUrl}/current-user`, {
        credentials: 'include'
      }).then(response => response.ok ? response.json() : null)
    ).subscribe({
      next: (user) => {
        if (user) {
          this.currentUserSubject.next(user);
        }
      },
      error: (error) => {
        console.error('Error checking current user:', error);
      }
    });
  }

  register(name: string, email: string, password: string, role: string = 'user'): Observable<AuthResponse> {
    return from(
      fetch(`${this.apiUrl}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ name, email, password, role })
      }).then(async (response) => {
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Error al registrarse');
        }
        this.currentUserSubject.next(data.user);
        return data;
      })
    ).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    );
  }

  login(email: string, password: string): Observable<AuthResponse> {
    return from(
      fetch(`${this.apiUrl}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({ email, password })
      }).then(async (response) => {
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.message || 'Error al iniciar sesión');
        }
        this.currentUserSubject.next(data.user);
        return data;
      })
    ).pipe(
      catchError((error) => {
        return throwError(() => error);
      })
    );
  }

  logout(): void {
    from(
      fetch(`${this.apiUrl}/logout`, {
        method: 'POST',
        credentials: 'include'
      })
    ).subscribe({
      next: () => {
        this.currentUserSubject.next(null);
        this.router.navigate(['/login']);
      },
      error: (error) => {
        console.error('Error al cerrar sesión:', error);
      }
    });
  }

  isAuthenticated(): boolean {
    return this.currentUserValue !== null;
  }

  isAdmin(): boolean {
    return this.currentUserValue?.role === 'admin';
  }
}
