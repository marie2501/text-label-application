import {Component, OnDestroy, OnInit} from '@angular/core';
import {MenuItem, PrimeIcons} from 'primeng/api';
import {Subscription} from "rxjs";
import {AuthService} from "../../../services/auth/auth.service";
import {Router} from "@angular/router";
import {WorkflowService} from "../../../services/workflow/workflow.service";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit, OnDestroy{
  menuItems: MenuItem[] = [];
  isUserLoggedIn: boolean = false;
  authSubscribtion: Subscription = new Subscription();

  workflow: {isOnWorkflow: boolean, id: number} = {isOnWorkflow: false, id: 0};
  workflowSubscribtion: Subscription = new Subscription();

  constructor(private authService: AuthService, private router: Router, private workflowService: WorkflowService) {
  }

  ngOnInit(): void {
    this.authSubscribtion = this.authService.isAuthenticated.subscribe((isAuthenticated:boolean) => {
      this.isUserLoggedIn = isAuthenticated;
      this.reloadNavbarOnChange();
    });
    this.workflowSubscribtion = this.workflowService.currentWorkflow.subscribe((workflow :{isOnWorkflow: boolean, id: number} ) => {
      this.workflow = workflow;
      this.reloadNavbarOnChange();
    });

    this.validateOnInit();
    this.reloadNavbarOnChange();
  }


  reloadNavbarOnChange(){
    this.menuItems = [];
    this.menuItems = [
      { label: 'Home', icon: PrimeIcons.HOME , routerLink: [''],
        disabled: this.isUserLoggedIn, visible: !this.isUserLoggedIn },

      { label: 'Dashboard', icon: PrimeIcons.HOME , routerLink: ['/dashboard'],
        disabled: !this.isUserLoggedIn, visible: this.isUserLoggedIn },

      { label: 'Workflow-Dashboard', routerLink: ['/workflow', this.workflow.id ,'dashboard'],
        disabled: !this.workflow.isOnWorkflow, visible: this.workflow.isOnWorkflow },

      { label: 'Login', routerLink: ['/login'], style: {position: 'relative', left: '75em'},
        disabled: this.isUserLoggedIn, visible: !this.isUserLoggedIn},

      { label: 'Sign up', routerLink: ['/sign-up'], style: {position: 'relative', left: '75em'},
        disabled: this.isUserLoggedIn, visible: !this.isUserLoggedIn},

      { label: 'Logout', style: {position: 'relative', left: this.positionLeft()},
        disabled: !this.isUserLoggedIn, visible: this.isUserLoggedIn,
        command: (event) => {
          this.onLogout()
        }}
    ];
  }

  positionLeft(){
    if (this.workflow.isOnWorkflow){
      return '65rem'
    }
    return '75rem'
  }


  validateOnInit() {
    if (localStorage.getItem('userData')) {
      this.authService.validateToken().subscribe();
    }
  }

  ngOnDestroy(): void {
    this.authSubscribtion.unsubscribe();
    this.workflowSubscribtion.unsubscribe();
  }


  private onLogout() {
    this.authService.logout().subscribe({
      complete: () => {
        this.router.navigate(['/'])
      }
    });
  }
}
