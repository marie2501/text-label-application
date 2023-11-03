import { Component } from '@angular/core';
import {NgForm} from "@angular/forms";
import {WorkflowModel} from "../../../models/workflow.model";
import {WorkflowService} from "../../../services/workflow/workflow.service";
import {Router} from "@angular/router";
import {FileService} from "../../../services/workflow/file.service";

@Component({
  selector: 'app-workflow-create',
  templateUrl: './workflow-create.component.html',
  styleUrls: ['./workflow-create.component.css']
})
export class WorkflowCreateComponent {

  workflow_id: number = 0;
  workflow_created: boolean = false;
  success: boolean = false;
  isLoading: boolean = false;


  constructor(private workflowService: WorkflowService, private router: Router, private fileService: FileService) {
  }

  onCreate(workflowForm: NgForm) {
    if (!workflowForm.valid) {
      return;
    }
    const title: string = workflowForm.value.title;
    let isPublic: boolean = false;
    if (workflowForm.value.isPublic == true) {
      isPublic = true;
    }
    const workflow: WorkflowModel = {is_public: isPublic, title: title};

    this.workflowService.createWorkflow(workflow).subscribe(respData => {
      this.workflow_created = true;
      this.workflow_id = respData.workflow_id;
    }, error => {
      console.log(error);
      },
      () => {
        console.log('success');
      })
  }

}
