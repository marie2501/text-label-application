import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {RunService} from "../../../services/workflow/run.service";
import {RunModel} from "../../../models/run.model";
import {WorkflowService} from "../../../services/workflow/workflow.service";
import {FileService} from "../../../services/workflow/file.service";

@Component({
  selector: 'app-workflow-dashboard',
  templateUrl: './workflow-dashboard.component.html',
  styleUrls: ['./workflow-dashboard.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class WorkflowDashboardComponent implements OnInit{

  workflow_id: number = 0;
  runs: RunModel[] = [];
  isCreator: boolean = false;
  isUploaded: boolean = true;

  buttonDataset: string = 'Edit the dataset';

  constructor(private route: ActivatedRoute, private runService: RunService, private workflowService: WorkflowService, private fileService: FileService) {
  }


  // todo info box welches Vormat das dataset haben soll
  // am besten ein ordern wo ich alle infoboxen sammel

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
    this.workflowService.updateCurrentWorkflow(true, this.workflow_id);
    this.runService.listRun(this.workflow_id).subscribe(respData => {
      this.runs = respData;
    }, error => {
    });
    this.workflowService.isWorkflowCreator(this.workflow_id).subscribe(respData => {
      this.isCreator = respData.isCreator;
    }, error => {
    }, () => {
      if (this.isCreator){
        this.fileService.getIsFileUploaded(this.workflow_id).subscribe(respData => {
          this.isUploaded = respData;
          if (!this.isUploaded){
            this.buttonDataset = 'Upload a dataset';
          }
        });
      }
    });
  }

  updateDataset() {

  }
}
