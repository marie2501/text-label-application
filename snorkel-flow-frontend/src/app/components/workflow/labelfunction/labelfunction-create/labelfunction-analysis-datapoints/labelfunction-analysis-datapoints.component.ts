import {Component, Input, OnInit} from '@angular/core';
import {LabelfunctionService} from "../../../../../services/workflow/labelfunction.service";
import {DataframeModel} from "../../../../../models/dataframe.model";

@Component({
  selector: 'app-labelfunction-analysis-datapoints',
  templateUrl: './labelfunction-analysis-datapoints.component.html',
  styleUrls: ['./labelfunction-analysis-datapoints.component.css']
})
export class LabelfunctionAnalysisDatapointsComponent implements OnInit{

  @Input()
  df_combined : DataframeModel[] = [];
  visible: boolean = false;


  constructor(labelfunctionService: LabelfunctionService) {
  }

  ngOnInit(): void {
    console.log(this.df_combined)
  }

  showDialog() {
    this.visible = true;
  }

  getSplittingValue(value: string) {
    if (value == 'train'){
      return 'Train';
    }
    return 'Unlabeled';
  }

  getSplittingSeverty(value: string) {
    if (value == 'train'){
      return 'danger';
    }
    return 'primary';
  }
}
