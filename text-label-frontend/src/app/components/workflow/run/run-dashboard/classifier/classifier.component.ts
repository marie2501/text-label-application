import {Component, DoCheck, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges} from '@angular/core';
import {RunService} from "../../../../../services/workflow/run.service";

@Component({
  selector: 'app-classifier',
  templateUrl: './classifier.component.html',
  styleUrls: ['./classifier.component.css']
})
export class ClassifierComponent implements DoCheck {

  model: string[] = ['Naive Bayes', 'Decision Tree', 'Random Forest', 'KNeighbors', 'Logistic Regression'];
  selectedModel: string = '';

  @Output()
  changeEvent = new EventEmitter<{ classifier: string, filterAbstain: boolean }>();
  filterAbstain: boolean = false;


  ngDoCheck(): void {
    this.changeEvent.emit({classifier: this.selectedModel, filterAbstain: this.filterAbstain});
  }
}
