import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {Message, MessageService} from "primeng/api";
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-dawn';
import {ActivatedRoute, Router} from "@angular/router";
import {WorkflowService} from "../../../../services/workflow/workflow.service";


@Component({
  selector: 'app-workflow-file',
  templateUrl: './workflow-file.component.html',
  styleUrls: ['./workflow-file.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class WorkflowFileComponent implements OnInit {

  workflow_id: number = -1;
  workflow_created: boolean = false;
  errorMessage: Message[] = [];
  isCreator: boolean = false;

  constructor(private messageService: MessageService, private route: ActivatedRoute,
              private workflowService: WorkflowService, private router: Router) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['wid'];
    this.workflowService.isWorkflowCreator(this.workflow_id).subscribe(respData => {
      this.isCreator = respData.isCreator;
      if (this.isCreator == false) {
        this.router.navigate(['/workflow', this.workflow_id, 'dashboard'])
      }
    }, error => {
    });
    if (this.workflow_id != -1){
      this.workflow_created = true;
    }
  }

}
