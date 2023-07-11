import { Component } from '@angular/core';
import {NgForm} from "@angular/forms";
import {AuthService} from "../../../../services/auth/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  constructor(private authService: AuthService, private router: Router) {
  }
  onLogin(loginForm: NgForm) {

    if(loginForm.valid){
      const username = loginForm.value.username;
      const password = loginForm.value.password;

      this.authService.login(username, password).subscribe(respData => {
        console.log(respData)
      }, error => {},
        () => {
          this.router.navigate(['/dashboard']);
        })

    }
  }

}
