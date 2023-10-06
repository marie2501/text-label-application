import {Component, ViewChild, ElementRef, OnInit, AfterViewInit} from '@angular/core';
import * as ace from 'ace-builds';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-dawn';
import {LabelfunctionService} from "../../../../../services/workflow/labelfunction.service";
import {ActivatedRoute} from "@angular/router";
import {LabelfunctionModel} from "../../../../../models/labelfunction.model";

const THEME = 'ace/theme/dawn';
const LANGUAGE = 'ace/mode/python';

@Component({
  selector: 'app-labelfunction-code',
  templateUrl: './labelfunction-code.component.html',
  styleUrls: ['./labelfunction-code.component.css']
})
export class LabelfunctionCodeComponent implements AfterViewInit, OnInit{

  // @ts-ignore
  @ViewChild('editor') codeEditorRef: ElementRef;
  // @ts-ignore
  private codeEditor: ace.Ace.Editor;
  // @ts-ignore
  workflow_id: number = 0;
  functionName: string = '';

  isCompiled: boolean = false;
  isTested: boolean = false;
  // todo name of labelfunction in form field

  constructor(private labelfunctionService: LabelfunctionService, private route: ActivatedRoute) { }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
  }

  ngAfterViewInit(): void {
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
    this.codeEditor.session.setValue("# Write your labelfunction!\n# Please write one label function at a time.");
    this.codeEditor.on('change', () => {
      this.isTested = false;
      this.isCompiled = false;
    })
  }

  savePythonCode() {
    const code = this.codeEditor.getValue();
    console.log(code);
    const labelfunctionModel: LabelfunctionModel = {code: code, type: 'python_code', name: this.functionName}
    this.labelfunctionService.createLabelfunction(labelfunctionModel ,this.workflow_id).subscribe(respData => {
      console.log(respData);
    }, error => {
      console.log(error);
    });
  }

  compilePythonCode() {
    const code: string = this.codeEditor.getValue();
    console.log(code);
    this.labelfunctionService.compileLabelfunction(code).subscribe(respData => {
      console.log(respData);
      this.isCompiled = true;
    }, error => {
      console.log(error);
    });
  }

  testPythonCode() {
    const code: string = this.codeEditor.getValue();
    console.log(code);
    let name: string = 'labelfunction_link';
    this.labelfunctionService.testLabelfunction(code, this.functionName).subscribe(respData => {
      console.log(respData);
      this.isTested = true;
    }, error => {
      console.log(error);
    });
  }

}
