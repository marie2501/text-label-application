import {Component, ViewEncapsulation} from '@angular/core';

@Component({
  selector: 'app-run-tutorial',
  templateUrl: './run-tutorial.component.html',
  styleUrls: ['./run-tutorial.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class RunTutorialComponent {

  visible: boolean = false;

  showDialog() {
    this.visible = true;
  }

}
