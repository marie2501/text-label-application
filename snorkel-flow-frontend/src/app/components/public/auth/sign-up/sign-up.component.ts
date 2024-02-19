import {Component, ViewEncapsulation} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, NgForm, Validators} from "@angular/forms";
import {AuthService} from "../../../../services/auth/auth.service";
import {Router} from "@angular/router";
import {Message} from 'primeng/api';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class SignUpComponent {

  errorMessage: Message[] = [];
  invalidForm: boolean = false;

  constructor(private authService: AuthService, private router: Router, private builder: FormBuilder) {
  }

  signUpForm: FormGroup = this.builder.group({
    username: new FormControl('', [
      Validators.maxLength(50),
      Validators.minLength(4),
      Validators.pattern('^[A-Za-z0-9]+$')
    ]),
    password: new FormControl('', [
      Validators.maxLength(50),
      Validators.minLength(8),
      Validators.pattern('^[A-Za-z0-9!@#$%^&*()_+-=]+$')
    ]),
    email: new FormControl('', [
      Validators.maxLength(50),
      Validators.pattern('^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    ]),
  })


  onSignUp() {

    if(this.signUpForm.valid){
      const username = this.signUpForm.value.username;
      const password = this.signUpForm.value.password;
      const email = this.signUpForm.value.email;

      this.authService.signup(username,password,email).subscribe(respData => {},error => {
        this.errorMessage = [{severity: 'error', summary: 'Error', detail: error}]
      }, () => {
        this.router.navigate(['/dashboard']);
      });
    } else {
      this.invalidForm = true;
    }


  }

}
