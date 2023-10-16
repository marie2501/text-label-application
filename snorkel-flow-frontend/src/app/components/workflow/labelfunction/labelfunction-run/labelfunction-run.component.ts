import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {LabelfunctionModel} from "../../../../models/labelfunction.model";
import {RunModel} from "../../../../models/run.model";
import {RunService} from "../../../../services/workflow/run.service";

@Component({
  selector: 'app-labelfunction-run',
  templateUrl: './labelfunction-run.component.html',
  styleUrls: ['./labelfunction-run.component.css']
})
export class LabelfunctionRunComponent implements OnInit{
  workflow_id: number = 0;
  selectedLabelfunction: LabelfunctionModel[] = [];
  splitting_ratio_labeled_test: number = 50;
  created: boolean = false;

  constructor(private route: ActivatedRoute, private runservice: RunService) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
  }

  onSave() : void {
    console.log(this.selectedLabelfunction, this.splitting_ratio_labeled_test);

    let id_labelfunctions: (number|undefined)[] = this.selectedLabelfunction.map(item => item.id);
    let run: {labelfunctions: (number|undefined)[], splitting_ratio_labeled_test: number} =
      {splitting_ratio_labeled_test: this.splitting_ratio_labeled_test,
      labelfunctions: id_labelfunctions};
    this.runservice.createlabelfunctionRun(run, this.workflow_id).subscribe(respData => {
      this.created = true;
    }, error => {
      console.log(error);
    })
  }

  onSelectChange($event: LabelfunctionModel[]): void{
    this.selectedLabelfunction = $event;
  }
}
