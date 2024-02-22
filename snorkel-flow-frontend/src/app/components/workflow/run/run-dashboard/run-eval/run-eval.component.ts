import {Component, OnInit} from '@angular/core';
import {RunModel} from "../../../../../models/run.model";
import {AnalysisModel} from "../../../../../models/analysis.model";
import {Message, MessageService} from "primeng/api";
import {RunService} from "../../../../../services/workflow/run.service";
import {LabelfunctionService} from "../../../../../services/workflow/labelfunction.service";
import {ActivatedRoute, Router} from "@angular/router";
import {WorkflowService} from "../../../../../services/workflow/workflow.service";

@Component({
  selector: 'app-run-eval',
  templateUrl: './run-eval.component.html',
  styleUrls: ['./run-eval.component.css']
})
export class RunEvalComponent implements OnInit{

  workflow_id: number = 0;
  run_id: number = 0;
  run!: RunModel;
  runLoaded!: Promise<boolean>;

  analysisModel_unlabeled!: AnalysisModel;
  analysisModel_train!: AnalysisModel;
  analysisLoaded!: Promise<boolean>;
  errorMessage: Message[] = [];

  username: string = '';
  executed: boolean = false;





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
    this.runService.getlabelfunctionRun(this.run_id).subscribe(respData => {
      this.run = respData;
      this.runLoaded = Promise.resolve(true);
    }, error => {
    });
  }


  executeRun() {
    this.runService.executelabelfunctionRun(this.run_id).subscribe(respData => {
      this.showSuccessMessage();
      this.executed = true;
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

}
