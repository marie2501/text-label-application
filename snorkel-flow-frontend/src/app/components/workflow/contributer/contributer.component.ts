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
  contributer: {username: string}[] = [];
  possibleContributer: {username: string}[] = [];

  username: string = '';

  @Input()
  allowedToChange: boolean = true;

  visible: boolean = false;

  constructor(private workflowService: WorkflowService, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['wid'];
    this.workflowService.getContributers(this.workflow_id).subscribe(respData => {
      this.contributer = respData;
    });
    this.username = this.getLoggedInUser();
    console.log(this.username);
  }



  addButton(username_not_con: string | undefined) {
    if (username_not_con != undefined){
      this.workflowService.addContributer(this.workflow_id, username_not_con).subscribe(respData => {
        this.possibleContributer = this.possibleContributer.filter(user => user.username !== username_not_con)
        this.contributer.push({'username': username_not_con})
        const elementListe = document.getElementById('listbox');

      }, error => {
      })
    }
  }

  deleteButton(username_con: string | undefined) {
    if (username_con != undefined){
      this.workflowService.deleteContributer(this.workflow_id, username_con).subscribe(respData => {
        console.log(respData);
        this.contributer = this.contributer.filter(user => user.username !== username_con)
      }, error => {
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

  showDialog() {
    this.visible = true;
  }

  onChange(usernamefilter: Event) {
    let temp = <InputEvent>usernamefilter
    const username = temp.data
    if (username != undefined && username != ''){
      this.workflowService.filterPossibleContributer(this.workflow_id, username).subscribe(respData => {
        this.possibleContributer = respData;
      }, error => {
      });
    }
  }
}
