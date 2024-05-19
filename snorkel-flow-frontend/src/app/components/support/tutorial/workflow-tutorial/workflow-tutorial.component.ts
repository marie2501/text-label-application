import { Component } from '@angular/core';

@Component({
  selector: 'app-workflow-tutorial',
  templateUrl: './workflow-tutorial.component.html',
  styleUrls: ['./workflow-tutorial.component.css']
})
export class WorkflowTutorialComponent {
  visible: boolean = false;

  showDialog() {
    this.visible = true;
  }
}
