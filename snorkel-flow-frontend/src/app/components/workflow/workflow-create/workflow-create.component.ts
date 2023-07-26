import { Component } from '@angular/core';
import {NgForm} from "@angular/forms";
import {WorkflowModel} from "../../../models/workflow.model";
import {WorkflowService} from "../../../services/workflow/workflow.service";

@Component({
  selector: 'app-workflow-create',
  templateUrl: './workflow-create.component.html',
  styleUrls: ['./workflow-create.component.css']
})
export class WorkflowCreateComponent {

  workflow_id: number = 0;
  workflow_created: boolean = false;

  constructor(private workflowService: WorkflowService ,) {
  }

  onCreate(workflowForm: NgForm) {
    if (!workflowForm.valid) {
      return;
    }
    const title: string = workflowForm.value.title;
    let isPublic: boolean = false;
    if (workflowForm.value.is_public == true) {
      isPublic = true;
    }
    const workflow: WorkflowModel = {is_public: isPublic, title: title};

    this.workflowService.createWorkflow(workflow).subscribe(respData => {
      this.workflow_created = true;
      this.workflow_id = respData.id;
    }, error => {
      console.log(error);
      },
      () => {
        console.log('success');
      })



  }
}
