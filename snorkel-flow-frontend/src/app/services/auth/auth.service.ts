import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, Subject, tap, throwError} from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import {environmentProd} from "../../../environments/environment.prod";
import {environmentDev} from "../../../environments/environment";


// const auhtURL = `${environmentProd.protocol}://${environmentProd.ip_adresse}/authentication`;
const auhtURL = `${environmentDev.protocol}://${environmentDev.ip_adresse}:${environmentDev.port}/authentication`;

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

  private handleError(error: HttpErrorResponse) {
    console.log(error.error);
    if (error.error.user != null){
      const userError : string = error.error.user[0]
      return throwError(() => new Error(userError));
    }
    if (error.error.email != null){
      const emailError : string = 'email:' + error.error.email[0]
      return throwError(() => new Error(emailError));
    }
    if (error.error.username != null){
      const usernameError : string = 'username: ' + error.error.username[0]
      return throwError(() => new Error(usernameError));
    }
    return throwError(() => new Error('Login failed. Please try again.'));

  }
}
