import { Component } from '@angular/core';
import {NgForm} from "@angular/forms";
import {AuthService} from "../../../../services/auth/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css']
})
export class SignUpComponent {

  constructor(private authService: AuthService, private router: Router) {
  }


  onSignUp(signUpForm: NgForm) {

    if(signUpForm.valid){
      const username = signUpForm.value.username;
      const password = signUpForm.value.password;
      const email = signUpForm.value.email;

      this.authService.signup(username,password,email).subscribe(respData => {},error => {}, () => {
        this.router.navigate(['/dashboard']);
      });
    }


  }

}
