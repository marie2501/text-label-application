import {Component, ViewEncapsulation} from '@angular/core';

@Component({
  selector: 'app-workflow-tutorial',
  templateUrl: './workflow-tutorial.component.html',
  styleUrls: ['./workflow-tutorial.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class WorkflowTutorialComponent {
  visible: boolean = false;
  dashboardStatus: boolean = false;

  showDialog() {
    this.visible = true;
  }

  changeDashboardStatus() {
    this.dashboardStatus = !this.dashboardStatus;
  }
}
