import {Injectable} from "@angular/core";
import {HttpEvent, HttpHandler, HttpInterceptor, HttpRequest} from "@angular/common/http";
import {Observable} from "rxjs";

@Injectable()
export class AuthInterceptorService implements HttpInterceptor {

  constructor() {

  }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    if (localStorage.length > 0) {
      const userData = JSON.parse(localStorage.getItem('userData') ?? '');
      if (userData) {
        req = req.clone({
          setHeaders: {
            Authorization: 'Token ' + userData.token,
          }
        })
      }
    }
    return next.handle(req);
  }
}
