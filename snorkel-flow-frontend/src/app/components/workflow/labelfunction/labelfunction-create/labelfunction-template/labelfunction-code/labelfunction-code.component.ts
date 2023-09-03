import {Component, ViewChild, ElementRef, OnInit, AfterViewInit} from '@angular/core';
import * as ace from 'ace-builds';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-dawn';

const THEME = 'ace/theme/dawn';
const LANGUAGE = 'ace/mode/python';

@Component({
  selector: 'app-labelfunction-code',
  templateUrl: './labelfunction-code.component.html',
  styleUrls: ['./labelfunction-code.component.css']
})
export class LabelfunctionCodeComponent implements AfterViewInit{

  // @ts-ignore
  @ViewChild('editor') codeEditorRef: ElementRef;
  // @ts-ignore
  private codeEditor: ace.Ace.Editor;
  // @ts-ignore

  constructor() { }

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
    this.codeEditor.session.setValue("# Write your labelfunctions!");
  }

  savePythonCode() {
    const code = this.codeEditor.getValue();
    console.log(code);
  }

  compilePythonCode() {
    const code = this.codeEditor.getValue();
    console.log(code);
  }
}
