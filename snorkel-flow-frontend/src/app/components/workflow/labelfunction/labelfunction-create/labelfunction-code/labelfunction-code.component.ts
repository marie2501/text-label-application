import {Component, ViewChild, ElementRef, OnInit, AfterViewInit, Input, ViewEncapsulation} from '@angular/core';
import * as ace from 'ace-builds';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-dawn';
import {LabelfunctionService} from "../../../../../services/workflow/labelfunction.service";
import {ActivatedRoute} from "@angular/router";
import {LabelfunctionModel} from "../../../../../models/labelfunction.model";
import {Message, MessageService} from "primeng/api";
import {WorkflowService} from "../../../../../services/workflow/workflow.service";
import {AnalysisModel} from "../../../../../models/analysis.model";
import {DataframeModel} from "../../../../../models/dataframe.model";

const THEME = 'ace/theme/dawn';
const LANGUAGE = 'ace/mode/python';

@Component({
  selector: 'app-labelfunction-code',
  templateUrl: './labelfunction-code.component.html',
  styleUrls: ['./labelfunction-code.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class LabelfunctionCodeComponent implements AfterViewInit, OnInit{

  // @ts-ignore
  @ViewChild('editor') codeEditorRef: ElementRef;
  // @ts-ignore
  private codeEditor: ace.Ace.Editor;

  // @ts-ignore
  @ViewChild('imports') importEditorRef: ElementRef;
  // @ts-ignore
  private importEditor: ace.Ace.Editor;

  // differenziere ob wir eine Funktion updaten oder erstellen
  // bei erstellen bleibt lid = -1

  @Input()
  lid : number = -1;

  // @ts-ignore
  workflow_id: number = 0;
  functionName: string = '';

  isTested: boolean = false;
  isSaved: boolean = true;
  importLabelfunction!: LabelfunctionModel;

  analysisModel_unlabeled!: AnalysisModel;
  analysisModel_train!: AnalysisModel;
  errorMessage: Message[] = [];
  sidebarVisible: boolean = false;
  workflowDescription: string = '';
  labelfunctionDescription: string = '';
  annotationschema: string = '';
  packages: string[] = [];

  df_combined: DataframeModel[] = [];

  constructor(private labelfunctionService: LabelfunctionService, private route: ActivatedRoute,
              private messageService: MessageService, private workflowService: WorkflowService) { }

  ngOnInit(): void {
    if (this.lid == 0){
      this.lid = this.route.snapshot.params['lid'];
    }
    this.workflow_id = this.route.snapshot.params['wid'];
    this.workflowService.updateCurrentWorkflow(true, this.workflow_id);
    this.workflowService.getWorkflowById(this.workflow_id).subscribe(respData => {
      this.workflowDescription = respData.description ?? 'No description was specified by the workflow owner';
    });
    this.workflowService.getInstalledPackages().subscribe(respData => {
      this.packages = respData;
    });
    this.labelfunctionService.getImportLabels(this.workflow_id, 'labels').subscribe(respData => {
      this.annotationschema = respData.code ?? 'No annotation schema was specified by the workflow owner';
    })
  }

  ngAfterViewInit(): void {
    // code Editor
    const element = this.codeEditorRef.nativeElement;
    const editorOptions: Partial<ace.Ace.EditorOptions> = {
      highlightActiveLine: true,
      minLines: 10,
      maxLines: Infinity,
    };

    this.codeEditor = ace.edit(element, editorOptions);
    this.codeEditor.setTheme(THEME);
    this.codeEditor.getSession().setMode(LANGUAGE);
    this.codeEditor.setShowFoldWidgets(true);

    if (this.lid != -1){
      this.labelfunctionService.getLabelfunctionsByID(this.lid).subscribe(respData => {
        if ((respData.code != null) && (respData.name != null)) {
          this.codeEditor.session.setValue(respData.code);
          this.functionName = respData.name;
          this.labelfunctionDescription = respData.description ?? '';
        }
      });
    } else {
      this.codeEditor.session.setValue("# Write your labelfunction!\n" +
        "# Please write one label function at a time.\n" +
        "# Note that x is the whole data point.\n" +
        "# x.text is the actual text to be annotated in string format.\n");
    }

    this.codeEditor.on('change', () => {
      this.getfunctionName();
    });
    // import Editor
    const elementImport = this.importEditorRef.nativeElement;
    const importOptions: Partial<ace.Ace.EditorOptions> = {
      highlightActiveLine: true,
      minLines: 5,
      maxLines: Infinity,
    };

    this.labelfunctionService.getImportLabels(this.workflow_id, 'import').subscribe(respData => {
      this.importLabelfunction = respData;
      this.importEditor.session.setValue(this.getImport());
    })

    this.importEditor = ace.edit(elementImport, importOptions);
    this.importEditor.setTheme(THEME);
    this.importEditor.getSession().setMode(LANGUAGE);
    this.importEditor.setShowFoldWidgets(true);
    this.importEditor.on('change', () => {
      this.isSaved = false;
    });
  }

  getImport(): string {
  if (this.importLabelfunction?.code == undefined){
    return "# Please write here all import statements";
    } else {
     let str: string = this.importLabelfunction.code
    return str;
    }
  }


  isUpdate(){
      if (this.lid == -1){
        return 'Save';
      }
      return 'Update';
  }

  getDescription(){
    if (this.labelfunctionDescription.length > 0){
      return this.labelfunctionDescription;
    }
    return 'No description was given.';
  }

  testAndSaveLabelfunction() {
    const code: string = this.codeEditor.getValue();
    if (this.isOnlyOneLabelfunction()) {


      if (this.lid != -1) {
        const labelfunctionModel: LabelfunctionModel = {
          code: code,
          name: this.functionName,
          description: this.getDescription()
        }

        this.labelfunctionService.testAndUpdateLabelfunctions(this.lid, labelfunctionModel, this.workflow_id).subscribe({
          next: value => {
            this.analysisModel_unlabeled = value.summary;
            this.analysisModel_train = value.summary_train;
            this.df_combined = value.df_combined;
            this.lid = value.lid;
            this.isTested = true;
            this.showSuccessMessage('The label function has been successfully tested and updated');
          },
          error: error => {
            this.showErrorMessage(error);
          }
        });
      } else {
        const labelfunctionModel: LabelfunctionModel = {code: code, type: 'python_code', name: this.functionName}

        this.labelfunctionService.testAndSaveLabelfunction(labelfunctionModel, this.workflow_id).subscribe({
          next: value => {
            this.analysisModel_unlabeled = value.summary;
            this.analysisModel_train = value.summary_train;
            this.df_combined = value.df_combined;
            this.lid = value.lid;
            this.isTested = true;
            this.showSuccessMessage('The label function has been successfully tested and saved');
          },
          error: error => {
            this.showErrorMessage(error);
          }
        });
      }
    } else {
      this.showErrorMessage("Write exactly one labelfunction!");
    }
  }

  saveImport() {
    const code: string = this.importEditor.getValue();
    let name: string = 'imports';
    const labelfunctionModel: LabelfunctionModel = {code: code, type: 'import', name: name}
    this.labelfunctionService.updateImports(this.workflow_id, labelfunctionModel).subscribe({
      next: value => {
        this.isSaved = true;
        this.showSuccessMessage('Imports have been saved');
      },
      error: error => {
        this.showErrorMessage(error);
      }
    });
  }

  showSuccessMessage(successMessage: string){
    this.messageService.add({ key: 'bc', severity: 'success',
      summary: 'Success', detail: successMessage });
  }

  private showErrorMessage(error: any) {
    this.errorMessage = [];
    this.errorMessage = [
      {severity: 'error', summary: 'Error', detail: error, closable: true }];
  }

  private getfunctionName(){
    const code: string = this.codeEditor.getValue();
    const i = code.indexOf('@labeling_function()');
    const j = code.indexOf(':');
    if (i < j){
      const substring = code.substring(i+22, j);
      const k = substring.indexOf('(');
      this.functionName = substring.substring(4, k).toString().trim();
    }
  }

  private isOnlyOneLabelfunction(){
    const code: string = this.codeEditor.getValue();
    const substring = '@labeling_function()';
    console.log(code.split(substring))
    if (code.split(substring).length - 1 == 1){
      return true;
    }
    return false;
  }

  implementTemplate($event: string) {
    this.codeEditor.session.setValue($event);
  }
}
