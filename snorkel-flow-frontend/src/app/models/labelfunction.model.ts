import {AnalysisModel} from "./analysis.model";

export interface LabelfunctionModel {
  id?: number;
  name?: string;
  type?: string;
  code?: string;
  creator?: string;
  description?: string;
  summary_unlabeled?: AnalysisModel;
  summary_train?: AnalysisModel;

}
