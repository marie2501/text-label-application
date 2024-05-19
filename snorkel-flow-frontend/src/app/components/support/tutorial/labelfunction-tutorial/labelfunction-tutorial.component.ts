import { Component } from '@angular/core';

@Component({
  selector: 'app-labelfunction-tutorial',
  templateUrl: './labelfunction-tutorial.component.html',
  styleUrls: ['./labelfunction-tutorial.component.css']
})
export class LabelfunctionTutorialComponent {
  visible: boolean = false;

  showDialog() {
    this.visible = true;
  }
}
