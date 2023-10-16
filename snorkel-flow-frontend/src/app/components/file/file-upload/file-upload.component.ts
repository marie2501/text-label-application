import {Component, Input, OnInit} from '@angular/core';
import {FileService} from "../../../services/workflow/file.service";

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.component.html',
  styleUrls: ['./file-upload.component.css']
})
export class FileUploadComponent implements OnInit{

  @Input()
  workflow_id: number = 0;
  success: boolean = false;
  isLoading: boolean = false;

  constructor(private fileService: FileService) {
  }

  onFileUpload(fileUpload: HTMLInputElement) {
    if (fileUpload.files) {
      let conversation = 'False';
      let file = fileUpload.files[0];
      let formData = new FormData();
      formData.append('file', file);
      formData.append('workflow_id', '' + this.workflow_id);
      this.isLoading = true;
      this.fileService.fileUpload(formData, this.workflow_id).subscribe(respData => {
        this.success = true;
      }, error => {
        this.isLoading = false;
        console.log(error);
      }, () => {
        this.isLoading = false;
      })
    }
  }

  ngOnInit(): void {
    console.log(this.workflow_id)
  }

}
