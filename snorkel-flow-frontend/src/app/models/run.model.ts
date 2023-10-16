import {LabelfunctionModel} from "./labelfunction.model";

export interface RunModel {
  id?: number;
  labelfunctions?: LabelfunctionModel[];
  splitting_ratio_labeled_test?: number;
  creation_date?: string;
  creator?: string;

}
