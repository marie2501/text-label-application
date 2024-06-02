import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {LabelfunctionModel} from "../../models/labelfunction.model";
import {catchError} from "rxjs/operators";
import {throwError} from "rxjs";
import {environmentProd} from "../../../environments/environment.prod";
import {environmentDev} from "../../../environments/environment";
import {AnalysisModel} from "../../models/analysis.model";
import {DataframeModel} from "../../models/dataframe.model";

// const labelfuntionURL = `${environmentProd.protocol}://${environmentProd.ip_adresse}/settings/workflow`;
const labelfuntionURL = `${environmentDev.protocol}://${environmentDev.ip_adresse}:${environmentDev.port}/settings/workflow`;


@Injectable({providedIn: "root"})
export class LabelfunctionService {


  constructor(private http: HttpClient) {
  }

  testAndSaveLabelfunction(labelfunction: LabelfunctionModel, workflow_id: number){
    return this.http.post<{summary: AnalysisModel, summary_train: AnalysisModel, df_combined: DataframeModel[], lid: number}>(`${labelfuntionURL}/${workflow_id}/labelfunction/`, labelfunction).pipe(catchError(this.handleError));
  }

  testAndUpdateLabelfunctions(labelfunction_id: number, labelfunction: LabelfunctionModel, workflow_id: number){
    return this.http.patch<{summary: AnalysisModel, summary_train: AnalysisModel, df_combined: DataframeModel[], lid: number}>(`${labelfuntionURL}/labelfunction/${labelfunction_id}/modifiy/`, {labelfunction, workflow_id}).pipe(catchError(this.handleError));
  }



  getLabelfunctionsByWorkflowID(workflow_id: number){
    return this.http.get<LabelfunctionModel[]>(`${labelfuntionURL}/${workflow_id}/labelfunction/`).pipe(catchError(this.handleError));
  }

  getImportLabels(workflow_id: number, type: string){
    return this.http.get<LabelfunctionModel>(`${labelfuntionURL}/${workflow_id}/labelfunction/${type}/`).pipe(catchError(this.handleError));
  }

  updateImports(workflow_id: number, labelfunction: LabelfunctionModel){
    return this.http.patch(`${labelfuntionURL}/${workflow_id}/labelfunction/import/`, labelfunction).pipe(catchError(this.handleError));
  }

  getLabelfunctionsByID(labelfunction_id: number){
    return this.http.get<LabelfunctionModel>(`${labelfuntionURL}/labelfunction/${labelfunction_id}/modifiy/`).pipe(catchError(this.handleError));
  }

  deleteLabelfunctions(labelfunction_id: number){
    return this.http.delete(`${labelfuntionURL}/labelfunction/${labelfunction_id}/modifiy/`).pipe(catchError(this.handleError));
  }



  private handleError(error: HttpErrorResponse){
    console.log(error)
    if (error.error.non_field_errors != null) {
      return throwError(() => error.error.non_field_errors);
    } else if (error.status == 403){
      return throwError(() => new Error('You do not have the authorization to change the label function.'));
    } else if (error.status == 404){
      return throwError(() => new Error(error.error));
    } else if (error.status == 400){
      return throwError(() => new Error(error.error));
    }
    return throwError(() => new Error('An unknown error occurred'));
  }

}
