import {Component, DoCheck, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges} from '@angular/core';
import {RunService} from "../../../../../services/workflow/run.service";

@Component({
  selector: 'app-classifier',
  templateUrl: './classifier.component.html',
  styleUrls: ['./classifier.component.css']
})
export class ClassifierComponent implements OnInit, DoCheck {

  model: string[] = ['Naive Bayes'];
  selectedModel: string = '';

  @Output()
  changeEvent = new EventEmitter<string>();

  constructor(private runService: RunService) {
  }

  ngOnInit(): void {
  }

  ngDoCheck(): void {
    this.changeEvent.emit(this.selectedModel);
  }
}
