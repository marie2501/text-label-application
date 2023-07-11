import {Component, OnDestroy, OnInit} from '@angular/core';
import {MenuItem, PrimeIcons} from 'primeng/api';
import {Subscription} from "rxjs";
import {AuthService} from "../../../services/auth/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit, OnDestroy{
  menuItems: MenuItem[] = [];
  isUserLoggedIn: boolean = false;
  authSubscribtion: Subscription = new Subscription();

  constructor(private authService: AuthService, private router: Router) {
  }

  ngOnInit(): void {
    this.authSubscribtion = this.authService.isAuthenticated.subscribe((isAuthenticated:boolean) => {
      this.isUserLoggedIn = isAuthenticated;
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

      { label: 'Login', routerLink: ['/login'], style: {position: 'relative', left: '75em'},
        disabled: this.isUserLoggedIn, visible: !this.isUserLoggedIn},

      { label: 'Sign up', routerLink: ['/sign-up'], style: {position: 'relative', left: '75em'},
        disabled: this.isUserLoggedIn, visible: !this.isUserLoggedIn},

      { label: 'Logout', style: {position: 'relative', left: '75rem'},
        disabled: !this.isUserLoggedIn, visible: this.isUserLoggedIn,
        command: (event) => {
          this.onLogout()
        }}
    ];
  }


  validateOnInit() {
    if (localStorage.getItem('userData')) {
      this.authService.validateToken().subscribe();
    }
  }

  ngOnDestroy(): void {
    this.authSubscribtion.unsubscribe();
  }


  private onLogout() {
    this.authService.logout().subscribe({
      complete: () => {
        this.router.navigate(['/'])
      }
    });
  }
}
