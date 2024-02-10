import {Component, OnInit} from '@angular/core';
import {RunService} from "../../../../services/workflow/run.service";
import {LabelfunctionService} from "../../../../services/workflow/labelfunction.service";
import {ActivatedRoute, Router} from "@angular/router";
import {RunModel} from "../../../../models/run.model";
import {LabelfunctionModel} from "../../../../models/labelfunction.model";
import {AnalysisModel} from "../../../../models/analysis.model";
import {Message, MessageService} from "primeng/api";
import {WorkflowService} from "../../../../services/workflow/workflow.service";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-run-dashboard',
  templateUrl: './run-dashboard.component.html',
  styleUrls: ['./run-dashboard.component.css']
})
export class RunDashboardComponent implements OnInit{
  workflow_id: number = 0;
  run_id: number = 0;
  // @ts-ignore
  run: RunModel;
  runLoaded!: Promise<boolean>;
  labelfunctions: LabelfunctionModel[] = [];

  // @ts-ignore
  analysisModel_unlabeled: AnalysisModel;
  // @ts-ignore
  analysisModel_train: AnalysisModel;
  analysisLoaded!: Promise<boolean>;
  errorMessage: Message[] = [];

  username: string = '';



  constructor(private runService: RunService, private labelfunctionService: LabelfunctionService, private router: Router,
              private route: ActivatedRoute, private messageService: MessageService, private workflowService: WorkflowService) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
    this.run_id = this.route.snapshot.params['runID'];
    this.username = this.getLoggedInUser();
    this.workflowService.updateCurrentWorkflow(true, this.workflow_id);
    this.runService.getlabelfunctionRun(this.run_id).subscribe(respData => {
      this.run = respData;
      this.labelfunctions = this.run.labelfunctions!;
      this.runLoaded = Promise.resolve(true);
    }, error => {
      console.log(error);
    });
  }

  executeRun() {
    this.runService.executelabelfunctionRun(this.run_id).subscribe(respData => {
      this.showSuccessMessage();
    }, error => {
      this.showErrorMessage(error);
    });
  }

  getAnalysis() {
    this.runService.getAnalysisRun(this.run_id).subscribe(respData => {
      this.analysisModel_unlabeled = respData.summary;
      this.analysisModel_train = respData.summary_train
      this.analysisLoaded = Promise.resolve(true);
    }, error => {
      this.showErrorMessage(error);
    });
  }

  private showErrorMessage(error: any) {
    this.errorMessage = [];
    this.errorMessage = [
      {severity: 'error', summary: 'Error', detail: error.error }];
  }

  showSuccessMessage(){
    this.messageService.add({ key: 'bc', severity: 'success',
      summary: 'Success', detail: 'Run has been successfully executed' });
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
