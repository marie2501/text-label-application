import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {HomepageComponent} from "./components/public/homepage/homepage.component";
import {LoginComponent} from "./components/public/auth/login/login.component";
import {SignUpComponent} from "./components/public/auth/sign-up/sign-up.component";
import {UserDashboardComponent} from "./components/dashboard/user-dashboard/user-dashboard.component";
import {loginGuard, loginGuardHomepage, runAccessGuard, workflowAccessGuard} from "./services/auth/auth-guard.service";
import {WorkflowCreateComponent} from "./components/workflow/workflow-create/workflow-create.component";
import {WorkflowHomeComponent} from "./components/workflow/workflow-home/workflow-home.component";
import {WorkflowDashboardComponent} from "./components/workflow/workflow-dashboard/workflow-dashboard.component";
import {LabelfunctionCreateComponent} from "./components/workflow/labelfunction/labelfunction-create/labelfunction-create.component";
import {FileComponent} from "./components/file/file.component";
import {LabelfunctionRunComponent} from "./components/workflow/labelfunction/labelfunction-run/labelfunction-run.component";
import {RunDashboardComponent} from "./components/workflow/run/run-dashboard/run-dashboard.component";
import {
  LabelfunctionUpdateComponent
} from "./components/workflow/labelfunction/labelfunction-update/labelfunction-update.component";
import {LabelvoteComponent} from "./components/workflow/run/run-dashboard/labelvote/labelvote.component";
import {FeaturizeComponent} from "./components/workflow/run/run-dashboard/featurize/featurize.component";
import {ClassifierComponent} from "./components/workflow/run/run-dashboard/classifier/classifier.component";
import {ModelSettingsComponent} from "./components/workflow/run/run-dashboard/model-settings/model-settings.component";
import {ContributerComponent} from "./components/workflow/contributer/contributer.component";
import {RunDataComponent} from "./components/workflow/run/run-dashboard/run-data/run-data.component";
import {RunEvalComponent} from "./components/workflow/run/run-dashboard/run-eval/run-eval.component";
import {FileDownloadComponent} from "./components/file/file-download/file-download.component";
import {ForbiddenComponent} from "./components/errors/forbidden/forbidden.component";

const routes: Routes = [
  {path: '', component: HomepageComponent, canActivate: [loginGuardHomepage]},
  {path: 'login', component: LoginComponent, canActivate: [loginGuardHomepage]},
  {path: 'sign-up', component: SignUpComponent, canActivate: [loginGuardHomepage]},
  {path: 'dashboard', component: UserDashboardComponent, canActivate: [loginGuard]},
  {path: 'workflow', component: WorkflowHomeComponent,
    canActivate: [loginGuard], canActivateChild: [loginGuard],
    children: [
      {path: 'create', component: WorkflowCreateComponent},
      {path: ':wid/file', component: FileComponent, canActivate: [workflowAccessGuard]},
      {path: ':wid/dashboard', component: WorkflowDashboardComponent, canActivate: [workflowAccessGuard]},
      {path: ':wid/create-labelfunction', component: LabelfunctionCreateComponent, canActivate: [workflowAccessGuard]},
      {path: ':wid/:lid/update-labelfunction', component: LabelfunctionUpdateComponent, canActivate: [workflowAccessGuard]},
      {path: ':wid/labelfunction-run', component: LabelfunctionRunComponent, canActivate: [workflowAccessGuard]},
      {path: ':wid/run-dashboard/:runID', component: RunDashboardComponent,
        canActivate: [runAccessGuard], canActivateChild: [runAccessGuard], children: [
          {path: 'data', component: RunDataComponent},
          {path: 'eval', component: RunEvalComponent},
          {path: 'model', component: ModelSettingsComponent},
          {path: 'download', component: FileDownloadComponent},
        ]},
    ]},
  {path: 'forbidden', component: ForbiddenComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
