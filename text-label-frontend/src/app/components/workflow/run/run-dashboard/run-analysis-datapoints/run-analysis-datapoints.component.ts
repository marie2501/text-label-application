import {Component, Input, OnInit} from '@angular/core';
import {DataframeModel} from "../../../../../models/dataframe.model";
import {LabelfunctionService} from "../../../../../services/workflow/labelfunction.service";

@Component({
  selector: 'app-run-analysis-datapoints',
  templateUrl: './run-analysis-datapoints.component.html',
  styleUrls: ['./run-analysis-datapoints.component.css']
})
export class RunAnalysisDatapointsComponent implements OnInit{

  @Input()
  df_combined : {columns: string[], index: string[], data: string[][]} = {columns: [], index: [], data: []};
  visible: boolean = false;


  constructor(labelfunctionService: LabelfunctionService) {
  }

  ngOnInit(): void {
  }

  showDialog() {
    this.visible = true;
  }

}
