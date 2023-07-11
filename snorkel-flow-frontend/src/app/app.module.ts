import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomepageComponent } from './components/public/homepage/homepage.component';
import { NavbarComponent } from './components/public/navbar/navbar.component';
import { LoginComponent } from './components/public/auth/login/login.component';
import { SignUpComponent } from './components/public/auth/sign-up/sign-up.component';
import { UserDashboardComponent } from './components/dashboard/user-dashboard/user-dashboard.component';

import { MenuModule } from 'primeng/menu';
import { MenubarModule } from 'primeng/menubar';
import { CardModule } from 'primeng/card';
import { PasswordModule } from 'primeng/password';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import {AuthInterceptorService} from "./services/auth/auth-interceptor.service";



@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    NavbarComponent,
    LoginComponent,
    SignUpComponent,
    UserDashboardComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule,
    AppRoutingModule,
    MenuModule,
    MenubarModule,
    CardModule,
    PasswordModule,
    ButtonModule,
    InputTextModule
  ],
  providers: [{ provide: HTTP_INTERCEPTORS, useClass: AuthInterceptorService, multi: true }],
  bootstrap: [AppComponent]
})
export class AppModule { }
