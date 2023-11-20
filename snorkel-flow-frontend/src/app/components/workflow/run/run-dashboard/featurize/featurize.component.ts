import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {RunService} from "../../../../../services/workflow/run.service";

@Component({
  selector: 'app-featurize',
  templateUrl: './featurize.component.html',
  styleUrls: ['./featurize.component.css']
})
export class FeaturizeComponent implements OnInit {
  model: string[] = ['Bag of words', 'TFIDF'];
  selectedModel: string = '';

  @Input()
  run_id: number = 0;

  @Input()
  workflow_id: number = 0;

  @Output()
  closeEvent = new EventEmitter<boolean>();
  range_x: number = 1;
  range_y: number = 1;



  constructor(private runservice: RunService) {
  }

  ngOnInit(): void {
  }

  saveModel() {
    let input = {range_x: this.range_x, range_y: this.range_y}
    if (this.selectedModel == 'Bag of words'){
      this.runservice.postBOW(this.run_id, this.workflow_id, input).subscribe(respData => {
        console.log(respData);
      }, error => {
        console.log(error);
      });
    } else if (this.selectedModel == 'TFIDF'){
      this.runservice.postTFIDF(this.run_id, this.workflow_id, input).subscribe(respData => {
        console.log(respData);
      }, error => {
        console.log(error);
      });
    }
  }

  onClose() {
    this.closeEvent.emit(false);
  }

}
