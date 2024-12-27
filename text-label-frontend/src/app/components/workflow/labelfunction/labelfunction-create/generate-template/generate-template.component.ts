import {Component, EventEmitter, OnInit, Output, ViewEncapsulation} from '@angular/core';
import {MenuItem} from "primeng/api";

@Component({
  selector: 'app-generate-template',
  templateUrl: './generate-template.component.html',
  styleUrls: ['./generate-template.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class GenerateTemplateComponent implements OnInit {
  items: MenuItem[] = [];

  @Output()
  templateEvent = new EventEmitter<string>();

  ngOnInit(): void {
    this.items = [
      { icon: 'pi pi-plus',
        tooltipOptions: {
          tooltipLabel: 'Template: Sentiment Analysis'
        }, command: () => {
          this.implementTemplate('# Write your labelfunction!\n' +
            '# Please write one label function at a time.\n' +
            '# Note that x is the whole data point.\n' +
            '# x.text is the actual text to be annotated in string format.\n' +
            '# TextBlob may needs to be imported.\n' +
            '@labeling_function()\n' +
            'def change_name(x):\n' +
            '    sentiment = TextBlob(x.text).sentiment.polarity\n' +
            '    if sentiment > 0:\n' +
            '        return LABEL_1\n' +
            '    if sentiment < 0:\n' +
            '        return LABEL_2\n' +
            '    return ABSTAIN')
        }},
    { icon: 'pi pi-plus',
        tooltipOptions: {
          tooltipLabel: 'Template: Heuristic'
        }, command: () => {
          this.implementTemplate('# Write your labelfunction!\n' +
            '# Please write one label function at a time.\n' +
            '# Note that x is the whole data point.\n' +
            '# x.text is the actual text to be annotated in string format.\n' +
            '@labeling_function()\n' +
            'def change_name(x):\n' +
            '    if len(x.text) > 100:\n' +
            '        return LABEL_1\n' +
            '    return LABEL_2')
        }},
      { icon: 'pi pi-plus',
        tooltipOptions: {
          tooltipLabel: 'Template: Keywordfilter'
        }, command: () => {
          this.implementTemplate('# Write your labelfunction!\n' +
            '# Please write one label function at a time.\n' +
            '# Note that x is the whole data point.\n' +
            '# x.text is the actual text to be annotated in string format.\n' +
            '@labeling_function()\n' +
            'def change_name(x):\n' +
            '    if "keyword" in x.text:\n' +
            '        return LABEL_1\n' +
            '    return LABEL_2')
        }}]
  }

  implementTemplate(template: string){
    this.templateEvent.emit(template);
  }

}
