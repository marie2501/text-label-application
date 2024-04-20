import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {RunModel} from "../../models/run.model";
import {AnalysisModel} from "../../models/analysis.model";
import {Subject, throwError} from "rxjs";
import {catchError} from "rxjs/operators";
import {LabelfunctionModel} from "../../models/labelfunction.model";
import {environmentProd} from "../../../environments/environment.prod";
import {environmentDev} from "../../../environments/environment";

// const labelfuntionURL = `${environmentProd.protocol}://${environmentProd.ip_adresse}/settings/workflow`;
const labelfuntionURL = `${environmentDev.protocol}://${environmentDev.ip_adresse}:${environmentDev.port}/settings/workflow`;



@Injectable({providedIn: "root"})
export class RunService {


  constructor(private http: HttpClient) {
  }


  createlabelfunctionRun(run: {labelfunctions: (number|undefined)[]}, workflow_id: number) {
    return this.http.post(`${labelfuntionURL}/${workflow_id}/run/`, run).pipe(catchError(this.handleError));
  }

  updatelabelfunctionRun(run: {labelfunctions: (number|undefined)[]}, run_id: number) {
    return this.http.put(`${labelfuntionURL}/${run_id}/run/`, run).pipe(catchError(this.handleError));
  }

  getlabelfunctionRun(run_id: number) {
    return this.http.get<RunModel>(`${labelfuntionURL}/${run_id}/run/`).pipe(catchError(this.handleError));
  }

  listlabelfunctionRun(workflow_id: number) {
    return this.http.get<RunModel[]>(`${labelfuntionURL}/${workflow_id}/run/list/`).pipe(catchError(this.handleError));
  }

  executelabelfunctionRun(run_id: number) {
    return this.http.get(`${labelfuntionURL}/${run_id}/run/exec/`).pipe(catchError(this.handleError));
  }

  getAnalysisRun(run_id: number) {
    return this.http.get<{'summary': AnalysisModel, 'summary_train': AnalysisModel}>(`${labelfuntionURL}/${run_id}/run/analysis/`).pipe(catchError(this.handleError));
  }

  // getLabelModel(run_id: number){
  //   return this.http.get<{ type: string }>(`${labelfuntionURL}/${run_id}/run/labelmodel/`);
  // }

  naiveBayesClassifier(run_id: number,
                       data: {selectedModelClassifier: string, selectedModelLabel: string,
                         selectedModelFeaturize: string, range_x: number, range_y: number}){
    return this.http.post<{score_train: number, score_test: number}>(`${labelfuntionURL}/run/${run_id}/naivebayes/`, data).pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse){
    if (error.status == 403){
      return throwError(() => new Error('You do not have authorization to access this resource'));
    } else if (error.status == 404){
      return throwError(() => new Error('The requested resource does not exists.'));
    } else if (error.status == 400){
      return throwError(() => new Error(error.error));
    }
    return throwError(() => new Error('An unknown error occurred'));
  }


}
