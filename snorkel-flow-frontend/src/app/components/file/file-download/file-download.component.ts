import {Component, OnInit} from '@angular/core';
import {saveAs} from "file-saver";
import {FileService} from "../../../services/workflow/file.service";
import {ActivatedRoute, Route} from "@angular/router";

@Component({
  selector: 'app-file-download',
  templateUrl: './file-download.component.html',
  styleUrls: ['./file-download.component.css']
})
export class FileDownloadComponent implements OnInit {

  isLoading: boolean = false;

  run_id = 0;

  constructor(private fileService: FileService, private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.run_id = this.route.snapshot.parent?.params['runID']
  }

  onDownload() {
    this.fileService.getCSVFile(this.run_id).subscribe(respData => {
      const data: Blob = new Blob([respData], {
        type: "text/csv; charset=utf-8"
      });
      let filename = 'run' + this.run_id + '.csv';
      saveAs(data, filename);
    }, error => {
    });
  }



}
