import {Component, DoCheck, EventEmitter, Output, ViewEncapsulation} from '@angular/core';

@Component({
  selector: 'app-labelvote',
  templateUrl: './labelvote.component.html',
  styleUrls: ['./labelvote.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class LabelvoteComponent implements DoCheck {
  model: string[] = ['Majority Vote', 'Train Label Model'];
  tie_break: string[] = ['abstain', 'true-random'];
  selectedModel: string = '';
  selectedTie: string = '';

  n_epochs : number = 100;
  log_freq : number = 10;
  seed : number = 123;
  base_learning_rate : number = 0.01;
  l2: number = 0.0;

  @Output()
  changeEvent = new EventEmitter<{selectedModel: string , selectedTie: string, n_epochs : number, log_freq : number,
    seed : number, base_learning_rate : number, l2: number}>();


  ngDoCheck(): void {
    this.changeEvent.emit({selectedModel: this.selectedModel, selectedTie: this.selectedTie, l2: this.l2, seed: this.seed,
      base_learning_rate: this.base_learning_rate, log_freq: this.log_freq, n_epochs: this.n_epochs});
  }

}
