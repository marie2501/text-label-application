import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, Subject, tap, throwError} from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import {environmentProd} from "../../../environments/environment.prod";
import {environmentDev} from "../../../environments/environment";


const auhtURL = `${environmentProd.protocol}://${environmentProd.ip_adresse}/authentication`;

interface AuthRespData {
  token: string;
}

@Injectable({providedIn: "root"})
export class AuthService {

  isAuthenticated = new Subject<boolean>();

  constructor(private http: HttpClient) {
  }

  login(username: string, password: string) {
    return this.http.post<AuthRespData>(`${auhtURL}/login/`, {
      "username": username,
      "password": password
    }).pipe(catchError(this.handleError), tap(respData => {
      this.loginAuth(username, respData.token);
    }));
  }

  signup(username: string, password: string, email: string) {
    return this.http.post<AuthRespData>(`${auhtURL}/register/`, {
      "username": username,
      "password": password,
      "email": email
    }).pipe(catchError(this.handleError), tap(respData => {
      this.loginAuth(username, respData.token);
    }));
  }

  validateToken(){
    return this.http.get(`${auhtURL}/validate/`).pipe(tap(respData => {
      this.isAuthenticated.next(true)
    }));
  }

  logout() {
    return this.http.post(`${auhtURL}/logout/`, {}
    ).pipe(tap(respData => {
      this.isAuthenticated.next(false);
      localStorage.clear();
    }));
  }

  private loginAuth(username: string, token: string) {
    this.isAuthenticated.next(true)
    localStorage.setItem('userData', JSON.stringify({username: username, token: token}));
  }

  //todo passe error code später an
  private handleError(error: HttpErrorResponse) {
    return throwError(() => new Error('Login failed. Please try again.'));

  }
}
