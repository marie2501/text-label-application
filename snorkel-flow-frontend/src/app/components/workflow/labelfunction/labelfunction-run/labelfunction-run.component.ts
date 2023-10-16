import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from "@angular/router";
import {LabelfunctionModel} from "../../../../models/labelfunction.model";

@Component({
  selector: 'app-labelfunction-run',
  templateUrl: './labelfunction-run.component.html',
  styleUrls: ['./labelfunction-run.component.css']
})
export class LabelfunctionRunComponent implements OnInit{
  workflow_id: number = 0;
  selectedLabelfunction: LabelfunctionModel[] = [];

  constructor(private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
  }

  onSave() {
    console.log(this.selectedLabelfunction);
  }


  onSelectChange($event: LabelfunctionModel[]) {
    this.selectedLabelfunction = $event;
  }
}
