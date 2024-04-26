import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {RunModel} from "../../../../../models/run.model";
import {LabelfunctionModel} from "../../../../../models/labelfunction.model";
import {Message, MessageService} from "primeng/api";
import {RunService} from "../../../../../services/workflow/run.service";
import {LabelfunctionService} from "../../../../../services/workflow/labelfunction.service";
import {ActivatedRoute, Router} from "@angular/router";
import {WorkflowService} from "../../../../../services/workflow/workflow.service";

@Component({
  selector: 'app-run-data',
  templateUrl: './run-data.component.html',
  styleUrls: ['./run-data.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class RunDataComponent implements OnInit{

  runLoaded!: Promise<boolean>;

  workflow_id: number = 0;
  run_id: number = 0;
  run!: RunModel;
  labelfunctions: LabelfunctionModel[] = [];
  errorMessage: Message[] = [];
  username: string = '';

  constructor(private runService: RunService, private labelfunctionService: LabelfunctionService, private router: Router,
              private route: ActivatedRoute, private messageService: MessageService, private workflowService: WorkflowService) {
  }

  ngOnInit(): void {
    this.route.parent?.params.subscribe((params) => {
      this.run_id = params['runID'];
      this.workflow_id = params['id'];
    }).unsubscribe();
    this.username = this.getLoggedInUser();
    this.workflowService.updateCurrentWorkflow(true, this.workflow_id);
    this.runService.getRun(this.run_id).subscribe(respData => {
      this.run = respData;
      this.labelfunctions = this.run.labelfunctions!;
      this.runLoaded = Promise.resolve(true);
    }, error => {
    });
  }

  getLoggedInUser(){
    const userData = JSON.parse(localStorage.getItem('userData') ?? '');
    if (userData) {
      return userData.username;
    }
    return '';
  }

  updateLabelfunktion() {
    this.router.navigate(['/workflow', this.workflow_id , 'labelfunction-run'], {queryParams: {run_id: this.run_id}});
  }

}
