import {Component, Input, OnInit, ViewEncapsulation} from '@angular/core';
import {WorkflowService} from "../../../services/workflow/workflow.service";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-contributer',
  templateUrl: './contributer.component.html',
  styleUrls: ['./contributer.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class ContributerComponent implements OnInit{

  workflow_id: number = 0;
  users: {items: { label: string, value: string }[], label: string}[] = [];

  username: string = '';

  @Input()
  allowedToChange: boolean = true;

  constructor(private workflowService: WorkflowService, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
    this.workflowService.getAllUsers(this.workflow_id).subscribe(respData => {
      this.users = respData;
      console.log(respData)
    });
    this.username = this.getLoggedInUser();
    console.log(this.username);
  }

  addButton(username_not_con: string | undefined) {
    if (username_not_con != undefined){
      this.workflowService.addContributer(this.workflow_id, username_not_con).subscribe(respData => {
        console.log(respData);
      }, error => {
        console.log(error);
      })
    }
  }

  deleteButton(username_con: string | undefined) {
    if (username_con != undefined){
      this.workflowService.deleteContributer(this.workflow_id, username_con).subscribe(respData => {
        console.log(respData);
      }, error => {
        console.log(error);
      })
    }
  }

  getLoggedInUser(){
    const userData = JSON.parse(localStorage.getItem('userData') ?? '');
    if (userData) {
     return userData.username;
    }
    return '';
  }

}
