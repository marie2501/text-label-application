import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {HomepageComponent} from "./components/public/homepage/homepage.component";
import {LoginComponent} from "./components/public/auth/login/login.component";
import {SignUpComponent} from "./components/public/auth/sign-up/sign-up.component";
import {UserDashboardComponent} from "./components/dashboard/user-dashboard/user-dashboard.component";
import {loginGuard, loginGuardHomepage} from "./services/auth/auth-guard.service";

const routes: Routes = [
  {path: '', component: HomepageComponent, canActivate: [loginGuardHomepage]},
  {path: 'login', component: LoginComponent, canActivate: [loginGuardHomepage]},
  {path: 'sign-up', component: SignUpComponent, canActivate: [loginGuardHomepage]},
  {path: 'dashboard', component: UserDashboardComponent, canActivate: [loginGuard]},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
