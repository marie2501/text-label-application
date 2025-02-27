import {Component, OnInit, ViewEncapsulation} from '@angular/core';
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
  styleUrls: ['./run-eval.component.css'],
  encapsulation: ViewEncapsulation.None
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
      this.workflow_id = params['wid'];
    }).unsubscribe();
    this.username = this.getLoggedInUser();
    this.workflowService.updateCurrentWorkflow(true, this.workflow_id);
    this.runService.getRun(this.run_id).subscribe(respData => {
      this.run = respData;
      this.runLoaded = Promise.resolve(true);
    }, error => {
    });
  }


  executeRun() {
    this.runService.executeRun(this.run_id).subscribe(respData => {
      this.showSuccessMessage();
      this.executed = true;
      this.analysisModel_unlabeled = respData.summary;
      this.analysisModel_train = respData.summary_train;
      this.analysisLoaded = Promise.resolve(true);
    }, error => {
      this.showErrorMessage(error);
    });
  }

  private showErrorMessage(error: any) {
    this.errorMessage = [];
    this.errorMessage = [
      {severity: 'error', summary: 'Error', detail: error }];
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
