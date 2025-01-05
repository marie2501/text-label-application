import {Component, ViewEncapsulation} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, NgForm, Validators} from "@angular/forms";
import {AuthService} from "../../../../services/auth/auth.service";
import {Router} from "@angular/router";
import {ConfirmationService, Message} from 'primeng/api';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.css'],
  encapsulation: ViewEncapsulation.None,
  providers: [ConfirmationService]

})
export class SignUpComponent {

  errorMessage: Message[] = [];
  invalidForm: boolean = false;

  constructor(private authService: AuthService, private router: Router,
              private builder: FormBuilder, private confirmationService: ConfirmationService) {
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


  confirmSignUp($event: Event) {
    this.confirmationService.confirm({
      target: $event.target as EventTarget,
      message: '<div>\n' +
        '  <p>\n' +
        '    This application is a prototype developed for demonstration and testing purposes only. It will be available online for a limited period of time. The owner of this application assumes no liability for any potential data loss, service interruptions, or issues arising from its use.\n' +
        '  </p>\n' +
        '  <p>\n' +
        '    All user-uploaded data, including account details and files, will be deleted when the application is taken offline. Users are advised not to upload sensitive or critical data.\n' +
        '  </p>\n' +
        '  <p>By creating an account or using this application, you acknowledge that:</p>\n' +
        '  <ul>\n' +
        '    <li>You understand this is a temporary, experimental prototype.</li>\n' +
        '    <li>You agree to use it at your own risk.</li>\n' +
        '    <li>You accept that no guarantees of functionality, security, or availability are provided.</li>\n' +
        '  </ul>\n' +
        '  <p>\n' +
        '    If you do not agree to these terms, please refrain from using the application.\n' +
        '  </p>\n' +
        '</div>\n',
      header: 'Disclaimer: Prototype Application',
      icon: 'pi pi-exclamation-triangle',
      acceptIcon:"none",
      rejectIcon:"none",
      acceptButtonStyleClass: "p-button-text p-button-danger",
      rejectButtonStyleClass: "p-button-text p-button-info",
      accept: () => {
        this.onSignUp()
      },
      reject: () => {
      }
    });
  }
}
