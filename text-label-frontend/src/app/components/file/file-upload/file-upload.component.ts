import {Component, Input, OnInit} from '@angular/core';
import {FileService} from "../../../services/workflow/file.service";
import {Message, MessageService} from "primeng/api";
import {WorkflowService} from "../../../services/workflow/workflow.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent implements OnInit {

  @Input()
  workflow_id: number = 0;
  success: boolean = false;
  isLoading: boolean = false;
  isUploaded: boolean = true;

  type: string = 'Change the dataset';
  errorMessage: Message[] = [];

  constructor(private fileService: FileService, private messageService: MessageService,
              private workflowService: WorkflowService, private router: Router) {
  }

  ngOnInit(): void {

    this.fileService.getIsFileUploaded(this.workflow_id).subscribe(respData => {
      this.isUploaded = respData;
      if (!this.isUploaded){
        this.type = 'Upload a dataset';
      }
    });

    this.workflowService.updateCurrentWorkflow(true, this.workflow_id);
  }

  onFileUpload(fileUpload: HTMLInputElement) {
    if (fileUpload.files) {
      let file = fileUpload.files[0];
      let formData = new FormData();
      formData.append('file', file);
      formData.append('workflow_id', '' + this.workflow_id);
      this.isLoading = true;
      if (!this.isUploaded){
        this.fileService.fileUpload(formData, this.workflow_id).subscribe(respData => {
          this.success = true;
          this.isLoading = false;
          this.showSuccessMessage();
          this.router.navigate(['workflow', this.workflow_id,'dashboard'])

        }, error => {
          this.isLoading = false;
          this.showErrorMessage(error);
        }, () => {
        });
      } else {
        this.fileService.fileUpdate(formData, this.workflow_id).subscribe(respData => {
          this.success = true;
          this.isLoading = false;
          this.showSuccessMessage();
          this.router.navigate(['workflow', this.workflow_id,'dashboard'])
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
      {severity: 'error', summary: 'Error', detail: error }];
  }

  showSuccessMessage(){
    this.messageService.add({ key: 'bc', severity: 'success',
      summary: 'Success', detail: 'Dataset has been successfully uploaded' });
  }

}
