import {Component, OnInit} from '@angular/core';
import {ActivatedRoute, Route} from "@angular/router";

@Component({
  selector: 'app-workflow-dashboard',
  templateUrl: './workflow-dashboard.component.html',
  styleUrls: ['./workflow-dashboard.component.css']
})
export class WorkflowDashboardComponent implements OnInit{

  workflow_id: number = 0;

  constructor(private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
  }
}
