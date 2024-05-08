import {AfterViewInit, Component, ElementRef, OnInit, ViewChild, ViewEncapsulation} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, NgForm, Validators} from "@angular/forms";

import {Message, MessageService} from "primeng/api";
import * as ace from 'ace-builds';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-dawn';
import {WorkflowService} from "../../../../services/workflow/workflow.service";
import {WorkflowModel} from "../../../../models/workflow.model";
import {Router} from "@angular/router";

const THEME = 'ace/theme/dawn';
const LANGUAGE = 'ace/mode/python';
@Component({
  selector: 'app-workflow-settings',
  templateUrl: './workflow-settings.component.html',
  styleUrls: ['./workflow-settings.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class WorkflowSettingsComponent implements AfterViewInit {



  workflow_id: number = 0;
  workflow_created: boolean = false;
  success: boolean = false;
  errorMessage: Message[] = [];
  // @ts-ignore
  @ViewChild('editor') codeEditorRef: ElementRef;
  // @ts-ignore
  private labelEditor: ace.Ace.Editor;


  constructor(private workflowService: WorkflowService, private messageService: MessageService,
              private router: Router, private builder: FormBuilder) {
  }

  workflowSettingsForm: FormGroup = this.builder.group({
    title: new FormControl('', [
      Validators.required
    ]),
    description: new FormControl('', [
      Validators.required
    ]),
  })

  ngAfterViewInit(): void {

    const element = this.codeEditorRef.nativeElement;
    const editorOptions: Partial<ace.Ace.EditorOptions> = {
      highlightActiveLine: true,
      minLines: 4,
      maxLines: Infinity,
    };

    this.labelEditor = ace.edit(element, editorOptions);
    this.labelEditor.setTheme(THEME);
    this.labelEditor.getSession().setMode(LANGUAGE);
    this.labelEditor.setShowFoldWidgets(true);
    this.labelEditor.session.setValue('ABSTAIN = -1');

  }

  onCreate() {
    if (this.workflowSettingsForm.valid ){
      const title: string = this.workflowSettingsForm.value.title;
      const description: string = this.workflowSettingsForm.value.description;
      const code_label: string = this.labelEditor.getValue()
      const workflow: WorkflowModel = {title: title, description: description};

      this.workflowService.createWorkflow(workflow, code_label).subscribe({ next: respData => {
          this.workflow_created = true;
          this.workflow_id = respData.workflow_id;
          this.showSuccessMessage();
          this.router.navigate(['workflow/create', this.workflow_id, 'file'])
        }, error: error => {
          this.errorMessage = [];
          this.errorMessage = [
            { severity: 'error', summary: 'Error', detail: error }];
        }
      });
    }
  }

  showSuccessMessage(){
    this.messageService.add({ severity: 'success',
      summary: 'Success', detail: 'Workflow has been successfully created' });
  }


}
