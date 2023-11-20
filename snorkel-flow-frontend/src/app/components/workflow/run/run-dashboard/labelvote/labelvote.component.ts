import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {RunService} from "../../../../../services/workflow/run.service";

@Component({
  selector: 'app-labelvote',
  templateUrl: './labelvote.component.html',
  styleUrls: ['./labelvote.component.css']
})
export class LabelvoteComponent implements OnInit{
  model: string[] = ['Majority Vote', 'Train Label Model'];
  selectedModel: string = '';

  @Input()
  run_id: number = 0;
  @Output()
  closeEvent = new EventEmitter<boolean>();



  constructor(private runservice: RunService) {
  }

  ngOnInit(): void {
  }

  saveModel() {
    if (this.selectedModel == 'Majority Vote'){
      this.runservice.postMajorityModel(this.run_id).subscribe(respData => {
        console.log(respData);
      }, error => {
        console.log(error);
      });
    } else if (this.selectedModel == 'Train Label Model'){
      this.runservice.postLabelModel(this.run_id).subscribe(respData => {
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
