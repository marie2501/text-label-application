import {Component, OnDestroy, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {RunService} from "../../../services/workflow/run.service";
import {RunModel} from "../../../models/run.model";
import {WorkflowService} from "../../../services/workflow/workflow.service";
import {MessageService} from "primeng/api";

@Component({
  selector: 'app-workflow-dashboard',
  templateUrl: './workflow-dashboard.component.html',
  styleUrls: ['./workflow-dashboard.component.css']
})
export class WorkflowDashboardComponent implements OnInit{

  workflow_id: number = 0;
  runs: RunModel[] = [];
  isCreator: boolean = false;

  constructor(private route: ActivatedRoute, private runService: RunService, private workflowService: WorkflowService) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
    this.workflowService.updateCurrentWorkflow(true, this.workflow_id);
    this.runService.listlabelfunctionRun(this.workflow_id).subscribe(respData => {
      this.runs = respData;
    }, error => {
      console.log(error);
    });
    this.workflowService.isWorkflowCreator(this.workflow_id).subscribe(respData => {
      this.isCreator = respData.isCreator;
    }, error => {
      console.log(error);
    })
  }
}
