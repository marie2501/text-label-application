import { Component } from '@angular/core';
import {NgForm} from "@angular/forms";
import {WorkflowModel} from "../../../models/workflow.model";
import {WorkflowService} from "../../../services/workflow/workflow.service";
import {Router} from "@angular/router";
import {FileService} from "../../../services/workflow/file.service";
import {Message, MessageService} from "primeng/api";

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
  errorMessage: Message[] = [];


  constructor(private workflowService: WorkflowService, private messageService: MessageService) {
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
      this.showSuccessMessage();
    }, error => {
        this.errorMessage = [];
        this.errorMessage = [
            { severity: 'error', summary: 'Error', detail: error.error.non_field_errors }];
        },
      () => {
      })
  }

  showSuccessMessage(){
    this.messageService.add({ key: 'bc', severity: 'success',
      summary: 'Success', detail: 'Workflow has been successfully created' });
  }

}
