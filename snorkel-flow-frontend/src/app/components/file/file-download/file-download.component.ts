import {Component, OnInit} from '@angular/core';
import {saveAs} from "file-saver";
import {FileService} from "../../../services/workflow/file.service";
import {ActivatedRoute, Route} from "@angular/router";
import {MessageService} from "primeng/api";

@Component({
  selector: 'app-file-download',
  templateUrl: './file-download.component.html',
  styleUrls: ['./file-download.component.css']
})
export class FileDownloadComponent implements OnInit {

  isLoading: boolean = false;

  run_id: number = 0;
  workflow_id: number = 0;

  constructor(private fileService: FileService, private route: ActivatedRoute, private messageService: MessageService) {}

  ngOnInit(): void {
    this.route.parent?.params.subscribe((params) => {
      this.run_id = params['runID'];
      this.workflow_id = params['wid'];
    }).unsubscribe();
  }

  onDownload(type: string) {
    this.fileService.getCSVFile(this.run_id, type).subscribe(respData => {
      const data: Blob = new Blob([respData], {
        type: (type == 'model' ? "application/octet-stream" : "text/csv; charset=utf-8")
      });
      let filename = 'labeled_data_run_id_' + this.run_id + '_' + type + (type == 'model' ? ".pickle" : ".csv");
      saveAs(data, filename);
    }, error => {
      this.showMessage(error, 'error', 'Error')
    });
  }

  showMessage(message: string, severity: string, summary: string){
    this.messageService.add({ key: 'bc', severity: severity,
      summary: summary, detail: message });
  }

}
