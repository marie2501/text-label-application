import {Component, ViewChild, ElementRef, OnInit, AfterViewInit, Input} from '@angular/core';
import * as ace from 'ace-builds';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-dawn';
import {LabelfunctionService} from "../../../../../services/workflow/labelfunction.service";
import {ActivatedRoute} from "@angular/router";
import {LabelfunctionModel} from "../../../../../models/labelfunction.model";
import {Message, MessageService} from "primeng/api";

const THEME = 'ace/theme/dawn';
const LANGUAGE = 'ace/mode/python';

@Component({
  selector: 'app-labelfunction-code',
  templateUrl: './labelfunction-code.component.html',
  styleUrls: ['./labelfunction-code.component.css']
})
export class LabelfunctionCodeComponent implements AfterViewInit, OnInit{

  // Editor für den Python Code
  // @ts-ignore
  @ViewChild('editor') codeEditorRef: ElementRef;
  // @ts-ignore
  private codeEditor: ace.Ace.Editor;

  // Editor für import statements
  // @ts-ignore
  @ViewChild('imports') importEditorRef: ElementRef;

  // differenziere ob wir eine Funktion updaten oder erstellen
  // bei erstellen bleibt lid = -1
  @Input()
  lid : number = -1;

  // @ts-ignore
  private importEditor: ace.Ace.Editor;

  // @ts-ignore
  workflow_id: number = 0;
  functionName: string = '';

  isCompiled: boolean = false;
  isTested: boolean = false;
  // todo name of labelfunction in form field
  // @ts-ignore
  importLabelfunction : LabelfunctionModel;

  test_coverage: number = 0;
  errorMessage: Message[] = [];

  constructor(private labelfunctionService: LabelfunctionService, private route: ActivatedRoute, private messageService: MessageService) { }

  ngOnInit(): void {
    if (this.lid == 0){
      this.lid = this.route.snapshot.params['lid'];
    }
    this.workflow_id = this.route.snapshot.params['wid'];
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
        }
      });
    } else {
      this.codeEditor.session.setValue("# Write your labelfunction!\n# Please write one label function at a time.");
    }

    this.codeEditor.on('change', () => {
      this.isTested = false;
      this.isCompiled = false;
    });
    // import Editor
    const elementImport = this.importEditorRef.nativeElement;
    const importOptions: Partial<ace.Ace.EditorOptions> = {
      highlightActiveLine: true,
      minLines: 5,
      maxLines: Infinity,
    };

    this.labelfunctionService.getImports(this.workflow_id).subscribe(respData => {
      this.importLabelfunction = respData;
      this.importEditor.session.setValue(this.getImport());
    })

    this.importEditor = ace.edit(elementImport, importOptions);
    this.importEditor.setTheme(THEME);
    this.importEditor.getSession().setMode(LANGUAGE);
    this.importEditor.setShowFoldWidgets(true);
    this.importEditor.on('change', () => {
      this.isTested = false;
      this.isCompiled = false;
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

  savePythonCode() {
    const code = this.codeEditor.getValue();

    if (this.lid != -1){
      const labelfunctionModel: LabelfunctionModel = {code: code, name: this.functionName}
      this.labelfunctionService.updateLabelfunctions(this.lid, labelfunctionModel).subscribe(respData => {
        this.showSuccessMessage('Labelfunction has been saved');
      }, error => {
        this.showErrorMessage(error);
      });

    } else {
      const labelfunctionModel: LabelfunctionModel = {code: code, type: 'python_code', name: this.functionName}
      this.labelfunctionService.createLabelfunction(labelfunctionModel ,this.workflow_id).subscribe(respData => {
        this.showSuccessMessage('Labelfunction has been saved');
      }, error => {
        this.showErrorMessage(error);
      });
    }
  }

  compilePythonCode() {
    const code: string = this.codeEditor.getValue();
    console.log(code);
    this.labelfunctionService.compileLabelfunction(code).subscribe(respData => {
      this.isCompiled = true;
      this.showSuccessMessage('Python code runs trough');
    }, error => {
      this.showErrorMessage(error);
    });
  }

  testPythonCode() {
    const code: string = this.codeEditor.getValue();
    console.log(code);
    this.labelfunctionService.testLabelfunction(code, this.functionName, this.workflow_id).subscribe(respData => {
      this.test_coverage = respData;
      this.isTested = true;
      this.showSuccessMessage('Python code runs on the dataset');
    }, error => {
      this.showErrorMessage(error);
    });
  }

  saveImport() {
    const code: string = this.importEditor.getValue();
    let name: string = 'imports';
    if (this.importLabelfunction?.id == undefined){
      const labelfunctionModel: LabelfunctionModel = {code: code, type: 'import', name: name}
      this.labelfunctionService.createLabelfunction(labelfunctionModel ,this.workflow_id).subscribe(respData => {
        this.showSuccessMessage('Imports have been saved');
      }, error => {
        this.showErrorMessage(error);
      });
    } else {
      const labelfunctionModel: LabelfunctionModel = {code: code, type: 'import', name: name}
      this.labelfunctionService.updateLabelfunctions(this.importLabelfunction.id, labelfunctionModel).subscribe(respData => {
        this.showSuccessMessage('Imports have been saved');
      }, error => {
        this.showErrorMessage(error);
      });
    }
  }


  showSuccessMessage(successMessage: string){
    this.messageService.add({ key: 'bc', severity: 'success',
      summary: 'Success', detail: successMessage });
  }

  private showErrorMessage(error: any) {
    this.errorMessage = [];
    this.errorMessage = [
      {severity: 'error', summary: 'Error', detail: error.error.non_field_errors }];
  }

}
