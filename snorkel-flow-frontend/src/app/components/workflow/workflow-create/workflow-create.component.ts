import {Component, ViewEncapsulation} from '@angular/core';
import {NgForm} from "@angular/forms";
import {WorkflowModel} from "../../../models/workflow.model";
import {WorkflowService} from "../../../services/workflow/workflow.service";
import {Message, MessageService} from "primeng/api";

@Component({
  selector: 'app-workflow-create',
  templateUrl: './workflow-create.component.html',
  styleUrls: ['./workflow-create.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class WorkflowCreateComponent {

  workflow_id: number = 0;
  workflow_created: boolean = false;
  success: boolean = false;
  errorMessage: Message[] = [];


  constructor(private workflowService: WorkflowService, private messageService: MessageService) {
  }

  onCreate(workflowForm: NgForm) {
    if (!workflowForm.valid) {
      return;
    }
    const title: string = workflowForm.value.title;
    const description: string = workflowForm.value.description;
    let isPublic: boolean = false;
    // if (workflowForm.value.isPublic == true) {
    //   isPublic = true;
    // }
    const workflow: WorkflowModel = {is_public: isPublic, title: title, description: description};

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
    this.messageService.add({ severity: 'success',
      summary: 'Success', detail: 'Workflow has been successfully created' });
  }

}
