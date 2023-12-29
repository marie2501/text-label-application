import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';

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
import { LabelfunctionCreateComponent } from './components/workflow/labelfunction/labelfunction-create/labelfunction-create.component';
import { LabelfunctionRunComponent } from './components/workflow/labelfunction/labelfunction-run/labelfunction-run.component';
import { LabelfunctionCodeComponent } from './components/workflow/labelfunction/labelfunction-create/labelfunction-code/labelfunction-code.component';
import { FileUploadComponent } from './components/file/file-upload/file-upload.component';
import { FileComponent } from './components/file/file.component';
import { LabelfunctionListComponent } from './components/workflow/labelfunction/labelfunction-list/labelfunction-list.component';
import { RunDashboardComponent } from './components/workflow/run/run-dashboard/run-dashboard.component';
import { LabelfunctionUpdateComponent } from './components/workflow/labelfunction/labelfunction-update/labelfunction-update.component';
import { LabelvoteComponent } from './components/workflow/run/run-dashboard/labelvote/labelvote.component';
import { FeaturizeComponent } from './components/workflow/run/run-dashboard/featurize/featurize.component';
import { ClassifierComponent } from './components/workflow/run/run-dashboard/classifier/classifier.component';
import { ModelSettingsComponent } from './components/workflow/run/run-dashboard/model-settings/model-settings.component';


import { MenuModule } from 'primeng/menu';
import { MenubarModule } from 'primeng/menubar';
import { CardModule } from 'primeng/card';
import { PasswordModule } from 'primeng/password';
import { ButtonModule } from 'primeng/button';
import { InputTextModule } from 'primeng/inputtext';
import { CheckboxModule } from 'primeng/checkbox';
import { DividerModule } from 'primeng/divider';
import { PanelModule } from 'primeng/panel';
import { InputNumberModule } from 'primeng/inputnumber';
import { TableModule } from 'primeng/table';
import { ScrollerModule } from 'primeng/scroller';
import { DropdownModule } from 'primeng/dropdown';
import { StepsModule } from 'primeng/steps';
import { MessagesModule } from 'primeng/messages';
import { TagModule } from 'primeng/tag';
import { TreeTableModule } from 'primeng/treetable';
import { ToastModule } from 'primeng/toast';
import {MessageService} from "primeng/api";




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
    WorkflowHomeComponent,
    LabelfunctionCreateComponent,
    LabelfunctionRunComponent,
    LabelfunctionCodeComponent,
    FileUploadComponent,
    FileComponent,
    LabelfunctionListComponent,
    RunDashboardComponent,
    LabelfunctionUpdateComponent,
    LabelvoteComponent,
    FeaturizeComponent,
    ClassifierComponent,
    ModelSettingsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    CommonModule,
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
    DividerModule,
    PanelModule,
    InputNumberModule,
    TableModule,
    ScrollerModule,
    DropdownModule,
    StepsModule,
    MessagesModule,
    TreeTableModule,
    TagModule,
    ToastModule
  ],
  providers: [{ provide: HTTP_INTERCEPTORS, useClass: AuthInterceptorService, multi: true }, MessageService],
  bootstrap: [AppComponent]
})
export class AppModule { }
