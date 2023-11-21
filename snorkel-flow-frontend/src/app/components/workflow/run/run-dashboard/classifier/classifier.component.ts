import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {RunService} from "../../../../../services/workflow/run.service";

@Component({
  selector: 'app-classifier',
  templateUrl: './classifier.component.html',
  styleUrls: ['./classifier.component.css']
})
export class ClassifierComponent implements OnInit {

  model: string[] = ['Naive Bayes'];
  selectedModel: string = '';

  @Input()
  run_id: number = 0;
  @Output()
  closeEvent = new EventEmitter<boolean>();

  constructor(private runService: RunService) {
  }

  ngOnInit(): void {
  }

  trainClassifier() {
    if (this.selectedModel == 'Naive Bayes'){
      this.runService.naiveBayesClassifier(this.run_id).subscribe(respData => {
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
