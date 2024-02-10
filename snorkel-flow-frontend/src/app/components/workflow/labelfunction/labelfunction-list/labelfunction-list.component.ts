import {Component, Input} from '@angular/core';
import {LabelfunctionModel} from "../../../../models/labelfunction.model";
import {LabelfunctionService} from "../../../../services/workflow/labelfunction.service";
import { Output, EventEmitter } from '@angular/core';
import {Message, MessageService} from "primeng/api";

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
  errorMessage: Message[] = [];

  username: string = '';

  constructor(private labelfuntionService: LabelfunctionService, private messageService: MessageService) {
  }

  ngOnInit(): void {
    this.labelfuntionService.getLabelfunctions(this.workflow_id).subscribe((respData) => {
      this.labelfunctions = respData;
    }, error => {
      console.log(error);
    });
    this.username = this.getLoggedInUser();
  }

  deleteButton(id: number) {
    this.labelfuntionService.deleteLabelfunctions(id).subscribe(respData => {
      this.showSuccessMessage();
    })
    window.location.reload();
  }

  onRowSelect() {
    this.selectEvent.emit(this.selectedLabelfunction);
  }



  showSuccessMessage(){
    this.messageService.add({ key: 'bc', severity: 'success',
      summary: 'Success', detail: 'Labelfunction has been deleted' });
  }

  getLoggedInUser(){
    const userData = JSON.parse(localStorage.getItem('userData') ?? '');
    if (userData) {
      return userData.username;
    }
    return '';
  }

}
