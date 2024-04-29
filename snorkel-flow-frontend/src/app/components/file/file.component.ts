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


  constructor(private route: ActivatedRoute, private fileService: FileService) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['wid'];
  }
}
