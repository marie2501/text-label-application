import {Component, Input} from '@angular/core';
import {LabelfunctionModel} from "../../../../models/labelfunction.model";
import {LabelfunctionService} from "../../../../services/workflow/labelfunction.service";
import { Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-labelfunction-list',
  templateUrl: './labelfunction-list.component.html',
  styleUrls: ['./labelfunction-list.component.css']
})
export class LabelfunctionListComponent {

  @Input()
  workflow_id: number = 0;
  @Input()
  modifiable: boolean = false
  @Input()
  selectable: boolean = false;

  @Output() selectEvent = new EventEmitter<LabelfunctionModel[]>();

  labelfunctions: LabelfunctionModel[] = [];

  selectedLabelfunction: LabelfunctionModel[] = [];

  constructor(private labelfuntionService: LabelfunctionService) {
  }

  ngOnInit(): void {
    this.labelfuntionService.getLabelfunctions(this.workflow_id).subscribe((respData) => {
      this.labelfunctions = respData;
      console.log(respData);
    }, error => {
      console.log(error);
    });
  }

  deleteButton(id: number) {
    this.labelfuntionService.deleteLabelfunctions(id).subscribe(respData => {
      console.log(respData);
    })
    window.location.reload();
  }

  onRowSelect() {
    this.selectEvent.emit(this.selectedLabelfunction);
  }
}
