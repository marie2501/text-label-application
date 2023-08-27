import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, Subject, tap, throwError} from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import {WorkflowModel} from "../../models/workflow.model";
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
    return this.http.get<LabelfunctionModel[]>(`${labelfuntionURL}/${labelfunction_id}/labelfunction/`);
  }

  updateLabelfunctions(labelfunction_id: number, labelfunction: LabelfunctionModel){
    return this.http.patch<LabelfunctionModel[]>(`${labelfuntionURL}/${labelfunction_id}/labelfunction/`, labelfunction);
  }

  createlabelfunctionRun(formData: FormData, workflow_id: number) {
    return this.http.post(`${labelfuntionURL}/${workflow_id}/labelfunctionrun/`, formData);
  }

  getlabelfunctionRun(workflow_id: number) {
    return this.http.get(`${labelfuntionURL}/${workflow_id}/labelfunctionrun/`);
  }

  executelabelfunctionRun(workflow_id: number) {
    return this.http.get(`${labelfuntionURL}/${workflow_id}/labelfunctionrun/exec/`);
  }


}
