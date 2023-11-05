import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {LabelfunctionModel} from "../../../../models/labelfunction.model";
import {RunService} from "../../../../services/workflow/run.service";
import {FileService} from "../../../../services/workflow/file.service";

@Component({
  selector: 'app-labelfunction-run',
  templateUrl: './labelfunction-run.component.html',
  styleUrls: ['./labelfunction-run.component.css']
})
export class LabelfunctionRunComponent implements OnInit{
  workflow_id: number = 0;
  selectedLabelfunction: LabelfunctionModel[] = [];
  // splitting_ratio_labeled_test: number = 50;
  created: boolean = false;
  // file_names: {id: number, name: string}[] = []
  // file: {id: number, name: string} = {id: 0, name: ''};

  constructor(private route: ActivatedRoute, private runservice: RunService, private fileService: FileService) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
    // this.fileService.getFileNamesByWorkflowId(this.workflow_id).subscribe(respData => {
    //   this.file_names = respData;
    // })
  }

  onSave() : void {
    // console.log(this.selectedLabelfunction, this.splitting_ratio_labeled_test);

    let id_labelfunctions: (number|undefined)[] = this.selectedLabelfunction.map(item => item.id);

    let run: {labelfunctions: (number|undefined)[]} = {labelfunctions: id_labelfunctions};
    this.runservice.createlabelfunctionRun(run, this.workflow_id).subscribe(respData => {
      this.created = true;
    }, error => {
      console.log(error);
    })
  }

  onSelectChange($event: LabelfunctionModel[]): void{
    this.selectedLabelfunction = $event;
  }

  onRowSelect() {
    // console.log(this.file)
  }
}
