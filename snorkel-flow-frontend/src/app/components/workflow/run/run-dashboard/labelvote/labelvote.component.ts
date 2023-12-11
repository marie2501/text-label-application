import {Component, DoCheck, EventEmitter, Input, OnChanges, OnInit, Output, SimpleChanges} from '@angular/core';
import {RunService} from "../../../../../services/workflow/run.service";

@Component({
  selector: 'app-labelvote',
  templateUrl: './labelvote.component.html',
  styleUrls: ['./labelvote.component.css']
})
export class LabelvoteComponent implements OnInit, DoCheck {
  model: string[] = ['Majority Vote', 'Train Label Model'];
  selectedModel: string = '';

  @Output()
  changeEvent = new EventEmitter<string>();



  constructor(private runservice: RunService) {
  }

  ngOnInit(): void {
  }


  ngDoCheck(): void {
    this.changeEvent.emit(this.selectedModel);
  }

}
