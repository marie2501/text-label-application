import {Component, Input, OnInit} from '@angular/core';
import {FileService} from "../../../services/workflow/file.service";
import {Message, MessageService} from "primeng/api";
import {WorkflowService} from "../../../services/workflow/workflow.service";

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent implements OnInit {

  @Input()
  workflow_id: number = 0;

  @Input()
  update: boolean = false;

  @Input()
  file_id: number = -1;

  success: boolean = false;
  isLoading: boolean = false;

  type: string = 'Upload';
  errorMessage: Message[] = [];

  constructor(private fileService: FileService, private messageService: MessageService, private workflowService: WorkflowService) {
  }

  ngOnInit(): void {
    if (this.file_id != -1){
      this.type = 'Change Dataset'
    }
    this.workflowService.updateCurrentWorkflow(true, this.workflow_id);
  }

  onFileUpload(fileUpload: HTMLInputElement) {
    if (fileUpload.files) {
      let file = fileUpload.files[0];
      let formData = new FormData();
      formData.append('file', file);
      formData.append('workflow_id', '' + this.workflow_id);
      this.isLoading = true;
      if (this.file_id == -1){
        this.fileService.fileUpload(formData, this.workflow_id).subscribe(respData => {
          this.success = true;
          this.isLoading = false;
          this.showSuccessMessage();
        }, error => {
          this.isLoading = false;
          this.showErrorMessage(error);
        }, () => {
        });
      } else {
        formData.append('id', this.file_id.toString());
        this.fileService.fileUpdate(formData, this.workflow_id).subscribe(respData => {
          this.success = true;
          this.isLoading = false;
          this.showSuccessMessage();
        }, error => {
          this.isLoading = false;
          this.showErrorMessage(error);
        }, () => {

        });
      }
    }
  }

  private showErrorMessage(error: any) {
    this.errorMessage = [];
    this.errorMessage = [
      {severity: 'error', summary: 'Error', detail: error.error.non_field_errors }];
  }

  showSuccessMessage(){
    this.messageService.add({ key: 'bc', severity: 'success',
      summary: 'Success', detail: 'Dataset has been successfully uploaded' });
  }

}
