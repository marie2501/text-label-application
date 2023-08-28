import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {LabelfunctionModel} from "../../models/labelfunction.model";

const labelfuntionURL = 'http://localhost:8080/settings/workflow';



@Injectable({providedIn: "root"})
export class LabelfunctionService {


  constructor(private http: HttpClient) {
  }

  createLabelfunction(labelfunction: LabelfunctionModel, workflow_id: number) {
    return this.http.post<{workflow_id: number}>(`${labelfuntionURL}/${workflow_id}/labelfunction/`, labelfunction);
  }

  getLabelfunctions(workflow_id: number){
    return this.http.get<LabelfunctionModel[]>(`${labelfuntionURL}/${workflow_id}/labelfunction/`);
  }

  deleteLabelfunctions(labelfunction_id: number){
    return this.http.delete(`${labelfuntionURL}/${labelfunction_id}/labelfunction/`);
  }

  updateLabelfunctions(labelfunction_id: number, labelfunction: LabelfunctionModel){
    return this.http.patch(`${labelfuntionURL}/${labelfunction_id}/labelfunction/`, labelfunction);
  }

  createlabelfunctionRun(formData: FormData, workflow_id: number) {
    return this.http.post(`${labelfuntionURL}/${workflow_id}/labelfunctionrun/`, formData);
  }

  getlabelfunctionRun(labelfunctionrun_id: number) {
    return this.http.get<LabelfunctionModel[]>(`${labelfuntionURL}/${labelfunctionrun_id}/labelfunctionrun/`);
  }

  executelabelfunctionRun(labelfunctionrun_id: number) {
    return this.http.get(`${labelfuntionURL}/${labelfunctionrun_id}/labelfunctionrun/exec/`);
  }


}
