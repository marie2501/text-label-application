import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {RunService} from "../../../../services/workflow/run.service";
import {ActivatedRoute} from "@angular/router";
import {RunModel} from "../../../../models/run.model";
import {MenuItem, Message} from "primeng/api";
import {WorkflowService} from "../../../../services/workflow/workflow.service";

@Component({
  selector: 'app-run-dashboard',
  templateUrl: './run-dashboard.component.html',
  styleUrls: ['./run-dashboard.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class RunDashboardComponent implements OnInit{
  workflow_id: number = 0;
  run_id: number = 0;
  run!: RunModel;
  username: string = '';
  runSteps: MenuItem[] = [];
  runLoaded!: Promise<boolean>;



  constructor(private route: ActivatedRoute, private workflowService: WorkflowService, private runService: RunService,) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['wid'];
    this.run_id = this.route.snapshot.params['runID'];
    this.username = this.getLoggedInUser();
    this.workflowService.updateCurrentWorkflow(true, this.workflow_id);
    this.runService.getRun(this.run_id).subscribe(respData => {
      this.run = respData;
      this.runSteps = [
        { label: 'Information',
          routerLink: ['/workflow', this.workflow_id, 'run-dashboard', this.run_id, 'data']},
        { label: 'Evaluation',
          routerLink: ['/workflow', this.workflow_id, 'run-dashboard', this.run_id, 'eval']},
        { label: 'Model Training',
          routerLink: ['/workflow', this.workflow_id, 'run-dashboard', this.run_id, 'model'],
          disabled: this.username != this.run!.creator},
        { label: 'Download Dataset',
          routerLink: ['/workflow', this.workflow_id, 'run-dashboard', this.run_id, 'download'],
          disabled: this.username != this.run!.creator}];
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

}
