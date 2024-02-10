import {Component, OnDestroy, OnInit} from '@angular/core';
import {ActivatedRoute, Router} from "@angular/router";
import {LabelfunctionModel} from "../../../../models/labelfunction.model";
import {RunService} from "../../../../services/workflow/run.service";
import {FileService} from "../../../../services/workflow/file.service";
import {Message, MessageService} from "primeng/api";
import {WorkflowService} from "../../../../services/workflow/workflow.service";
import {Subscription} from "rxjs";

@Component({
  selector: 'app-labelfunction-run',
  templateUrl: './labelfunction-run.component.html',
  styleUrls: ['./labelfunction-run.component.css']
})
export class LabelfunctionRunComponent implements OnInit{
  workflow_id: number = 0;
  selectedLabelfunction: LabelfunctionModel[] = [];
  created: boolean = false;
  errorMessage: Message[] = [];
  run_id: number = -1;



  constructor(private route: ActivatedRoute, private runservice: RunService, private fileService: FileService,
              private messageService: MessageService, private workflowService: WorkflowService,
              private router: Router) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
    this.run_id = this.route.snapshot.queryParams['run_id'] ?? -1;
    this.workflowService.updateCurrentWorkflow(true, this.workflow_id);

  }

  onSave() : void {

    let id_labelfunctions: (number|undefined)[] = this.selectedLabelfunction.map(item => item.id);

    let run: {labelfunctions: (number|undefined)[]} = {labelfunctions: id_labelfunctions};
    if (this.run_id != -1){
      this.runservice.updatelabelfunctionRun(run, this.run_id).subscribe(respData => {
        this.created = true;
        this.showSuccessMessage();
      }, error => {
        this.showErrorMessage(error);
      });
      this.router.navigate(['/workflow', this.workflow_id , 'run-dashboard', this.run_id])
    } else {
      this.runservice.createlabelfunctionRun(run, this.workflow_id).subscribe(respData => {
        this.created = true;
        this.showSuccessMessage();
      }, error => {
        this.showErrorMessage(error);
      });
      this.router.navigate(['/workflow', this.workflow_id , 'dashboard'])
    }

  }

  onSelectChange($event: LabelfunctionModel[]): void{
    this.selectedLabelfunction = $event;
  }

  private showErrorMessage(error: any) {
    this.errorMessage = [];
    this.errorMessage = [
      {severity: 'error', summary: 'Error', detail: error.error.non_field_errors }];
  }

  showSuccessMessage(){
    this.messageService.add({ key: 'bc', severity: 'success',
      summary: 'Success', detail: 'Run has been successfully created' });
  }
}
