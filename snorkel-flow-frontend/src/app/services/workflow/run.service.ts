import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {RunModel} from "../../models/run.model";
import {AnalysisModel} from "../../models/analysis.model";
import {map, Observable, of, Subject, throwError} from "rxjs";
import {catchError} from "rxjs/operators";
import {LabelfunctionModel} from "../../models/labelfunction.model";
import {environmentProd} from "../../../environments/environment.prod";
import {environmentDev} from "../../../environments/environment";

// const runURL = `${environmentProd.protocol}://${environmentProd.ip_adresse}/settings/workflow`;
const runURL = `${environmentDev.protocol}://${environmentDev.ip_adresse}:${environmentDev.port}/settings/workflow`;



@Injectable({providedIn: "root"})
export class RunService {


  constructor(private http: HttpClient) {
  }

  accessRun(run_id: number): Observable<boolean>{
    return this.http.get<boolean>(`${runURL}/${run_id}/runaccess/`).pipe(catchError(this.handleError));
  }

  createRun(run: {labelfunctions: (number|undefined)[]}, workflow_id: number) {
    return this.http.post(`${runURL}/${workflow_id}/create/run/`, run).pipe(catchError(this.handleError));
  }

  listRun(workflow_id: number) {
    return this.http.get<RunModel[]>(`${runURL}/${workflow_id}/create/run/`).pipe(catchError(this.handleError));
  }

  updateRun(run: {labelfunctions: (number|undefined)[]}, run_id: number) {
    return this.http.put(`${runURL}/${run_id}/run/`, run).pipe(catchError(this.handleError));
  }

  getRun(run_id: number) {
    return this.http.get<RunModel>(`${runURL}/${run_id}/run/`).pipe(catchError(this.handleError));
  }

  executeRun(run_id: number) {
    return this.http.get<{'summary': AnalysisModel, 'summary_train': AnalysisModel}>(`${runURL}/${run_id}/run/exec/`).pipe(catchError(this.handleError));
  }

  getAnalysisRun(run_id: number) {
    return this.http.get<{'summary': AnalysisModel, 'summary_train': AnalysisModel}>(`${runURL}/${run_id}/run/analysis/`).pipe(catchError(this.handleError));
  }

  trainClassifier(run_id: number,
                  data: {selectedModelClassifier: string, selectedModelLabel: string,
                         selectedModelFeaturize: string, range_x: number, range_y: number}){
    return this.http.post<{score_train: number, score_test: number}>(`${runURL}/run/${run_id}/trainclassifier/`, data).pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse){
    console.log(error)
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
