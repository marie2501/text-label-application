import {Component, OnInit} from '@angular/core';

@Component({
  selector: 'app-labelfunction-type',
  templateUrl: './labelfunction-type.component.html',
  styleUrls: ['./labelfunction-type.component.css']
})
export class LabelfunctionTypeComponent implements OnInit{

  types: string[] = [];
  type: string = '';

  constructor() {
  }

  ngOnInit(): void {
    this.types = ['python_code', 'keywords'];
  }

}
