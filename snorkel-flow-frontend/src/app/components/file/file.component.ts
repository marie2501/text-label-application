import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {FileService} from "../../services/workflow/file.service";

@Component({
  selector: 'app-file',
  templateUrl: './file.component.html',
  styleUrls: ['./file.component.css']
})
export class FileComponent implements OnInit{

  workflow_id: number = 0;
  file_names: {id: number, name: string}[] = [];

  constructor(private route: ActivatedRoute, private fileService: FileService) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
    this.fileService.getFileNamesByWorkflowId(this.workflow_id).subscribe(respData =>{
      this.file_names = respData;
      console.log(respData);
    }, error => {
      console.log(error);
    });
  }
}
