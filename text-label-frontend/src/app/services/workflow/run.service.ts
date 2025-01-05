import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {RunModel} from "../../models/run.model";
import {AnalysisModel} from "../../models/analysis.model";
import {map, Observable, of, Subject, throwError} from "rxjs";
import {catchError} from "rxjs/operators";
import {LabelfunctionModel} from "../../models/labelfunction.model";
import {environmentProd} from "../../../environments/environment.prod";
import {environmentDev} from "../../../environments/environment";

const runURL = `${environmentProd.protocol}://${environmentProd.ip_adresse}/settings/run`;
// const runURL = `${environmentDev.protocol}://${environmentDev.ip_adresse}:${environmentDev.port}/settings/run`;



@Injectable({providedIn: "root"})
export class RunService {


  constructor(private http: HttpClient) {
  }

  accessRun(run_id: number): Observable<boolean>{
    return this.http.get<boolean>(`${runURL}/${run_id}/runaccess/`).pipe(catchError(this.handleError));
  }

  createRun(run: {labelfunctions: (number|undefined)[]}, workflow_id: number) {
    return this.http.post(`${runURL}/${workflow_id}/create/`, run).pipe(catchError(this.handleError));
  }

  listRun(workflow_id: number) {
    return this.http.get<RunModel[]>(`${runURL}/${workflow_id}/create/`).pipe(catchError(this.handleError));
  }

  updateRun(run: {labelfunctions: (number|undefined)[]}, run_id: number) {
    return this.http.put(`${runURL}/${run_id}/`, run).pipe(catchError(this.handleError));
  }

  getRun(run_id: number) {
    return this.http.get<RunModel>(`${runURL}/${run_id}/`).pipe(catchError(this.handleError));
  }

  executeRun(run_id: number) {
    return this.http.get<{'summary': AnalysisModel, 'summary_train': AnalysisModel}>(`${runURL}/${run_id}/exec/`).pipe(catchError(this.handleError));
  }

  trainClassifier(run_id: number,
                  data: {selectedModelClassifier: string, selectedModelLabel: string,
                         selectedModelFeaturize: string, range_x: number, range_y: number}){
    return this.http.post<{score_train: number, score_test: number, df_combined: {columns: string[], index: string[], data: string[][]}}>(`${runURL}/${run_id}/trainclassifier/`, data).pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse){
    if (error.error.message != null){
      return throwError(() => new Error(error.error.message));
    } else if (error.status == 500){
      return throwError(() => new Error('An unknown error occurred. It may be possible that the label definition is wrong or the dataset has been changed.'));
    }else if (error.error != null){
      return throwError(() => new Error(error.error));
    }
    return throwError(() => new Error('An unknown error occurred'));
  }


}
