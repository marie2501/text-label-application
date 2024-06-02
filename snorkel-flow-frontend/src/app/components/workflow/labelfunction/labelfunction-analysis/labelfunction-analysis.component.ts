import {Component, Input} from '@angular/core';
import {AnalysisModel} from "../../../../models/analysis.model";

@Component({
  selector: 'app-labelfunction-analysis',
  templateUrl: './labelfunction-analysis.component.html',
  styleUrls: ['./labelfunction-analysis.component.css']
})
export class LabelfunctionAnalysisComponent {

  @Input()
  analysisModel_unlabeled : AnalysisModel = {index: ['Nothing to analyse'], Coverage: [0], Conflicts: [0], Polarity: [0], Overlaps: [0]};

  @Input()
  analysisModel_train : AnalysisModel = {index: ['Nothing to analyse'], Coverage: [0], Conflicts: [0], Polarity: [0], Overlaps: [0]};

}
