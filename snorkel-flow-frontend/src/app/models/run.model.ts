import {LabelfunctionModel} from "./labelfunction.model";

export interface RunModel {
  id?: number;
  labelfunctions?: LabelfunctionModel[];
  creation_date?: string;
  creator?: string;

}
