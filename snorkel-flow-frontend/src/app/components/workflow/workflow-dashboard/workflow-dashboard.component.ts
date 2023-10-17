import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {RunService} from "../../../services/workflow/run.service";
import {RunModel} from "../../../models/run.model";

@Component({
  selector: 'app-workflow-dashboard',
  templateUrl: './workflow-dashboard.component.html',
  styleUrls: ['./workflow-dashboard.component.css']
})
export class WorkflowDashboardComponent implements OnInit{

  workflow_id: number = 0;
  runs: RunModel[] = [];

  constructor(private route: ActivatedRoute, private runService: RunService) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
    this.runService.listlabelfunctionRun(this.workflow_id).subscribe(respData => {
      console.log(respData);
      this.runs = respData;
    }, error => {
      console.log(error);
    });
  }
}
