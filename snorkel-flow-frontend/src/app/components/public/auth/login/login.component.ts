import { Component } from '@angular/core';
import {NgForm} from "@angular/forms";
import {AuthService} from "../../../../services/auth/auth.service";
import {Router} from "@angular/router";
import { Message } from 'primeng/api';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  errorMessage: Message[] = [];
  invalidForm: boolean = false;

  constructor(private authService: AuthService, private router: Router) {
  }
  onLogin(loginForm: NgForm) {
    if(loginForm.valid){
      const username = loginForm.value.username;
      const password = loginForm.value.password;

      this.authService.login(username, password).subscribe(respData => {
        console.log(respData)
      }, error => {
        this.errorMessage = [{severity: 'error', summary: 'Error', detail: error}]
        },
        () => {
          this.router.navigate(['/dashboard']);
        })

    } else {
      this.invalidForm = true;
    }
  }

}
