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
import { LabelfunctionListComponent } from './components/workflow/labelfunction/labelfunction-list/labelfunction-list.component';
import { RunDashboardComponent } from './components/workflow/run/run-dashboard/run-dashboard.component';
import { LabelfunctionUpdateComponent } from './components/workflow/labelfunction/labelfunction-update/labelfunction-update.component';
import { LabelvoteComponent } from './components/workflow/run/run-dashboard/labelvote/labelvote.component';
import { FeaturizeComponent } from './components/workflow/run/run-dashboard/featurize/featurize.component';
import { ClassifierComponent } from './components/workflow/run/run-dashboard/classifier/classifier.component';
import { ModelSettingsComponent } from './components/workflow/run/run-dashboard/model-settings/model-settings.component';
import { ContributerComponent } from './components/workflow/contributer/contributer.component';
import { RunDataComponent } from './components/workflow/run/run-dashboard/run-data/run-data.component';
import { RunEvalComponent } from './components/workflow/run/run-dashboard/run-eval/run-eval.component';
import { FileDownloadComponent } from './components/file/file-download/file-download.component';
import { ForbiddenComponent } from './components/errors/forbidden/forbidden.component';
import { WorkflowSettingsComponent } from './components/workflow/workflow-create/workflow-settings/workflow-settings.component';
import { WorkflowFileComponent } from './components/workflow/workflow-create/workflow-file/workflow-file.component';
import { WorkflowTutorialComponent } from './components/support/tutorial/workflow-tutorial/workflow-tutorial.component';
import { LabelfunctionTutorialComponent } from './components/support/tutorial/labelfunction-tutorial/labelfunction-tutorial.component';
import { RunTutorialComponent } from './components/support/tutorial/run-tutorial/run-tutorial.component';
import { GenerateTemplateComponent } from './components/workflow/labelfunction/labelfunction-create/generate-template/generate-template.component';


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
import { ListboxModule } from 'primeng/listbox';
import { InputTextareaModule } from 'primeng/inputtextarea';
import { SidebarModule } from 'primeng/sidebar';
import { DialogModule } from 'primeng/dialog';
import { TooltipModule } from 'primeng/tooltip';
import { EditorModule } from 'primeng/editor';
import { RippleModule } from 'primeng/ripple';
import { SpeedDialModule } from 'primeng/speeddial';
import { TabViewModule } from 'primeng/tabview';
import { LabelfunctionAnalysisDatapointsComponent } from './components/workflow/labelfunction/labelfunction-create/labelfunction-analysis-datapoints/labelfunction-analysis-datapoints.component';
import { LabelfunctionAnalysisComponent } from './components/workflow/labelfunction/labelfunction-analysis/labelfunction-analysis.component';
import { RunAnalysisDatapointsComponent } from './components/workflow/run/run-dashboard/run-analysis-datapoints/run-analysis-datapoints.component';



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
    LabelfunctionListComponent,
    RunDashboardComponent,
    LabelfunctionUpdateComponent,
    LabelvoteComponent,
    FeaturizeComponent,
    ClassifierComponent,
    ModelSettingsComponent,
    ContributerComponent,
    RunDataComponent,
    RunEvalComponent,
    FileDownloadComponent,
    ForbiddenComponent,
    WorkflowSettingsComponent,
    WorkflowFileComponent,
    WorkflowTutorialComponent,
    LabelfunctionTutorialComponent,
    RunTutorialComponent,
    GenerateTemplateComponent,
    LabelfunctionAnalysisDatapointsComponent,
    LabelfunctionAnalysisComponent,
    RunAnalysisDatapointsComponent
  ],
  imports: [
    BrowserModule,
    ReactiveFormsModule,
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
    ToastModule,
    ListboxModule,
    InputTextareaModule,
    SidebarModule,
    DialogModule,
    TooltipModule,
    EditorModule,
    RippleModule,
    SpeedDialModule,
    TabViewModule
  ],
  providers: [{ provide: HTTP_INTERCEPTORS, useClass: AuthInterceptorService, multi: true }, MessageService],
  bootstrap: [AppComponent]
})
export class AppModule { }
