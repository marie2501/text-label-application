import {Component, OnInit} from '@angular/core';
import {MenuItem, PrimeIcons} from 'primeng/api';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit{
  menuItems: MenuItem[] = [];
  isUserLoggedIn: boolean = false;

  ngOnInit(): void {
    this.menuItems = [
      { label: 'Home', icon: PrimeIcons.HOME , routerLink: [''] },
      { label: 'Login', routerLink: ['/login'], style: {position: 'relative', left: '75rem'},
        disabled: this.isUserLoggedIn, visible: !this.isUserLoggedIn},
      { label: 'Sign up', routerLink: ['/sign-up'], style: {position: 'relative', left: '75rem'},
        disabled: this.isUserLoggedIn, visible: !this.isUserLoggedIn},
      { label: 'Logout', style: {position: 'relative', left: '70rem'},
        disabled: !this.isUserLoggedIn, visible: this.isUserLoggedIn }
    ];
  }



}
