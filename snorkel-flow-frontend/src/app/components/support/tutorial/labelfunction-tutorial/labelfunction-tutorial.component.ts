import {Component, ViewEncapsulation} from '@angular/core';

@Component({
  selector: 'app-labelfunction-tutorial',
  templateUrl: './labelfunction-tutorial.component.html',
  styleUrls: ['./labelfunction-tutorial.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class LabelfunctionTutorialComponent {
  visible: boolean = false;

  showDialog() {
    this.visible = true;
  }
}
