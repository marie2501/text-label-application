import {Component, OnInit} from '@angular/core';
import {WorkflowService} from "../../../services/workflow/workflow.service";
import {WorkflowModel} from "../../../models/workflow.model";


@Component({
  selector: 'app-user-dashboard',
  templateUrl: './user-dashboard.component.html',
  styleUrls: ['./user-dashboard.component.css']
})
export class UserDashboardComponent implements OnInit{

  workflows: WorkflowModel[] = [];
  workflowLoaded!: Promise<boolean>;

  constructor(private workflowService: WorkflowService) {
  }

  ngOnInit(): void {
    this.workflowService.updateCurrentWorkflow(false,0);
    this.workflowService.getWorkflows().subscribe((respData) => {
      this.workflows = respData;
      this.workflowLoaded = Promise.resolve(true);
    })
  }

}
