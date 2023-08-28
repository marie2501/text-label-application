import {Component, OnInit} from '@angular/core';
import {MenuItem} from "primeng/api";

@Component({
  selector: 'app-labelfunction-create',
  templateUrl: './labelfunction-create.component.html',
  styleUrls: ['./labelfunction-create.component.css']
})
export class LabelfunctionCreateComponent implements OnInit{

  items: MenuItem[] = [];

  constructor() {
  }

  ngOnInit(): void {
    this.items = [
      {
        label: 'Type',
        routerLink: 'type'
      },
      {
        label: 'Template',
        routerLink: 'template'
      }
    ];
  }

}
