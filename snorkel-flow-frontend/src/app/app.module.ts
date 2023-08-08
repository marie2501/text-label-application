import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomepageComponent } from './components/public/homepage/homepage.component';
import { NavbarComponent } from './components/public/navbar/navbar.component';
import { LoginComponent } from './components/public/auth/login/login.component';
import { SignUpComponent } from './components/public/auth/sign-up/sign-up.component';
import { UserDashboardComponent } from './components/dashboard/user-dashboard/user-dashboard.component';
import {AuthInterceptorService} from "./services/auth/auth-interceptor.service";
import { WorkflowDashboardComponent } from './components/workflow/workflow-dashboard/workflow-dashboard.component';
import { WorkflowCreateComponent } from './components/workflow/workflow-create/workflow-create.component';
import { WorkflowHomeComponent } from './components/workflow/workflow-home/workflow-home.component';

import { MenuModule } from 'primeng/menu';
import { MenubarModule } from 'primeng/menubar';
import { CardModule } from 'primeng/card';
import { PasswordModule } from 'primeng/password';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { CheckboxModule } from 'primeng/checkbox';
import { DividerModule } from 'primeng/divider';




@NgModule({
  declarations: [
    AppComponent,
    HomepageComponent,
    NavbarComponent,
    LoginComponent,
    SignUpComponent,
    UserDashboardComponent,
    WorkflowDashboardComponent,
    WorkflowCreateComponent,
    WorkflowHomeComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    BrowserAnimationsModule,
    HttpClientModule,
    AppRoutingModule,
    MenuModule,
    MenubarModule,
    CardModule,
    PasswordModule,
    ButtonModule,
    InputTextModule,
    CheckboxModule,
    DividerModule
  ],
  providers: [{ provide: HTTP_INTERCEPTORS, useClass: AuthInterceptorService, multi: true }],
  bootstrap: [AppComponent]
})
export class AppModule { }
