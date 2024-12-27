import {Component, EventEmitter, Input, Output, ViewEncapsulation} from '@angular/core';
import {LabelfunctionModel} from "../../../../models/labelfunction.model";
import {LabelfunctionService} from "../../../../services/workflow/labelfunction.service";
import {Message, MessageService} from "primeng/api";
import {AnalysisModel} from "../../../../models/analysis.model";
import {RunService} from "../../../../services/workflow/run.service";

@Component({
  selector: 'app-labelfunction-list',
  templateUrl: './labelfunction-list.component.html',
  styleUrls: ['./labelfunction-list.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class LabelfunctionListComponent {

  @Input()
  workflow_id: number = 0;
  @Input()
  modifiable: boolean = false
  @Input()
  selectable: boolean = false;
  @Input()
  pointer: boolean = false;
  @Input()
  run_id: number = -1;

  @Output() selectEvent = new EventEmitter<LabelfunctionModel[]>();

  labelfunctions: LabelfunctionModel[] = [];

  selectedLabelfunction: LabelfunctionModel[] = [];
  errorMessage: Message[] = [];

  username: string = '';
  analysisModel_unlabeled!: AnalysisModel;
  analysisModel_train!: AnalysisModel;
  elementSelected: boolean = false;

  constructor(private labelfuntionService: LabelfunctionService, private messageService: MessageService,
              private runservice: RunService) {
  }

  ngOnInit(): void {
    this.labelfuntionService.getLabelfunctionsByWorkflowID(this.workflow_id).subscribe((respData) => {
      this.labelfunctions = respData;
    }, error => {
    });
    this.username = this.getLoggedInUser();
    if (this.run_id != -1){
      this.runservice.getRun(this.run_id).subscribe({
        next: value => {
          this.selectedLabelfunction = value.labelfunctions ?? [];
          if (!this.selectable){
            this.labelfunctions = this.selectedLabelfunction;
          }
        }
      });
    }
  }

  deleteButton(id: number) {
    this.labelfuntionService.deleteLabelfunctions(id).subscribe(
      {
        next: value  => {
          this.showMessage(value.message, 'success', 'Success');
          window.location.reload();
        },
        error: err => {
          this.showMessage(err, 'error', 'Error');
        }
      })
  }

  onRowSelect() {
    this.selectEvent.emit(this.selectedLabelfunction);
  }


  showMessage(message: string, severity: string, summary: string){
    this.messageService.add({ key: 'bc', severity: severity,
      summary: summary, detail: message });
  }

  getLoggedInUser(){
    const userData = JSON.parse(localStorage.getItem('userData') ?? '');
    if (userData) {
      return userData.username;
    }
    return '';
  }

  onSelectAnalysis(labelfunction: LabelfunctionModel) {
    this.analysisModel_train = labelfunction.summary_train!;
    this.analysisModel_unlabeled = labelfunction.summary_unlabeled!;
    this.elementSelected = true;
  }
}
