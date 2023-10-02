import { Component } from '@angular/core';
import {NgForm} from "@angular/forms";
import {WorkflowModel} from "../../../models/workflow.model";
import {WorkflowService} from "../../../services/workflow/workflow.service";
import {Router} from "@angular/router";

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


  constructor(private workflowService: WorkflowService, private router: Router) {
  }

  onCreate(workflowForm: NgForm) {
    if (!workflowForm.valid) {
      return;
    }
    const title: string = workflowForm.value.title;
    const ratio: number = workflowForm.value.splittingRatio;
    let isPublic: boolean = false;
    if (workflowForm.value.isPublic == true) {
      isPublic = true;
    }
    const workflow: WorkflowModel = {is_public: isPublic, title: title, splitting_ratio_labeled_test: ratio};

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

  onLabeledFileUpload(fileUpload: HTMLInputElement) {
    if (fileUpload.files) {
      let conversation = 'False';
      let file = fileUpload.files[0];
      let formData = new FormData();
      formData.append('file', file);
      formData.append('workflow_id', '' + this.workflow_id);
      this.isLoading = true;
      this.workflowService.fileUpload(formData, this.workflow_id).subscribe(respData => {
        this.success = true;
      }, error => {
        this.isLoading = false;
        console.log(error);
      }, () => {
        this.isLoading = false;
      })
    }
  }

}
