import {Component, OnInit} from '@angular/core';
import {LabelfunctionService} from "../../../services/workflow/labelfunction.service";
import {ActivatedRoute, Route} from "@angular/router";
import {LabelfunctionModel} from "../../../models/labelfunction.model";

@Component({
  selector: 'app-workflow-dashboard',
  templateUrl: './workflow-dashboard.component.html',
  styleUrls: ['./workflow-dashboard.component.css']
})
export class WorkflowDashboardComponent implements OnInit{

  workflow_id: number = 0;
  labelfunctions: LabelfunctionModel[] = [];

  constructor(private labelfuntionService: LabelfunctionService, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
    this.labelfuntionService.getLabelfunctions(this.workflow_id).subscribe((respData) => {
      this.labelfunctions = respData;
      console.log(respData);
    }, error => {
      console.log(error);
    })
  }

  deleteButton(id: number) {
    this.labelfuntionService.deleteLabelfunctions(id).subscribe(respData => {
      console.log(respData);
    })
    window.location.reload();
  }
}
