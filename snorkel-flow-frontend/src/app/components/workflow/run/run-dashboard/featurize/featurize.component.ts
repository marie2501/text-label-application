import {Component, DoCheck, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges} from '@angular/core';
import {RunService} from "../../../../../services/workflow/run.service";

@Component({
  selector: 'app-featurize',
  templateUrl: './featurize.component.html',
  styleUrls: ['./featurize.component.css']
})
export class FeaturizeComponent implements OnInit, DoCheck {
  model: string[] = ['Bag of words', 'TFIDF'];
  selectedModel: string = '';


  @Output()
  changeEvent = new EventEmitter<{selectedModel: string, range_x: number, range_y: number}>();
  range_x: number = 1;
  range_y: number = 1;



  constructor(private runservice: RunService) {
  }

  ngOnInit(): void {
  }

  ngDoCheck(): void {
    this.changeEvent.emit({selectedModel: this.selectedModel, range_x: this.range_x, range_y: this.range_y});
  }

}
