import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {FileService} from "../../services/workflow/file.service";

@Component({
  selector: 'app-file',
  templateUrl: './file.component.html',
  styleUrls: ['./file.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class FileComponent implements OnInit{

  workflow_id: number = 0;
  // file_names: {id: number, name: string}[] = [];
  // @ts-ignore
  file_names: {id: number, name: string} = {id: -1, name: ''};
  fileLoaded!: Promise<boolean>;


  constructor(private route: ActivatedRoute, private fileService: FileService) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
    this.fileService.getFileNamesByWorkflowId(this.workflow_id).subscribe(respData =>{
      if (respData != undefined){
        this.file_names = respData;
      }
      this.fileLoaded = Promise.resolve(true);
    }, error => {
      this.fileLoaded = Promise.resolve(true);
    });
  }
}
