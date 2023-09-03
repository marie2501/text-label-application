import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {HomepageComponent} from "./components/public/homepage/homepage.component";
import {LoginComponent} from "./components/public/auth/login/login.component";
import {SignUpComponent} from "./components/public/auth/sign-up/sign-up.component";
import {UserDashboardComponent} from "./components/dashboard/user-dashboard/user-dashboard.component";
import {loginGuard, loginGuardHomepage} from "./services/auth/auth-guard.service";
import {WorkflowCreateComponent} from "./components/workflow/workflow-create/workflow-create.component";
import {WorkflowHomeComponent} from "./components/workflow/workflow-home/workflow-home.component";
import {WorkflowDashboardComponent} from "./components/workflow/workflow-dashboard/workflow-dashboard.component";
import {
  LabelfunctionCreateComponent
} from "./components/workflow/labelfunction/labelfunction-create/labelfunction-create.component";
import {
  LabelfunctionTypeComponent
} from "./components/workflow/labelfunction/labelfunction-create/labelfunction-type/labelfunction-type.component";
import {
  LabelfunctionTemplateComponent
} from "./components/workflow/labelfunction/labelfunction-create/labelfunction-template/labelfunction-template.component";
import {
  LabelfunctionCodeComponent
} from "./components/workflow/labelfunction/labelfunction-create/labelfunction-template/labelfunction-code/labelfunction-code.component";

const routes: Routes = [
  {path: '', component: HomepageComponent, canActivate: [loginGuardHomepage]},
  {path: 'login', component: LoginComponent, canActivate: [loginGuardHomepage]},
  {path: 'sign-up', component: SignUpComponent, canActivate: [loginGuardHomepage]},
  {path: 'dashboard', component: UserDashboardComponent, canActivate: [loginGuard]},
  {path: 'workflow', component: WorkflowHomeComponent,
    canActivate: [loginGuard], canActivateChild: [loginGuard],
    children: [
      {path: 'create', component: WorkflowCreateComponent},
      {path: ':id/dashboard', component: WorkflowDashboardComponent},
      {path: ':id/create-labelfunction', component: LabelfunctionCreateComponent, children:[
          {path: 'type', component: LabelfunctionTypeComponent},
          {path: 'template', component: LabelfunctionTemplateComponent, children: [
              {path: 'code', component: LabelfunctionCodeComponent}
            ]}
        ]},
      //todo generate component
      {path: ':id/update-labelfunction', component: LabelfunctionCreateComponent},
    ]},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
