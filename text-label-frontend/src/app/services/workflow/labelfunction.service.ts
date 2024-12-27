import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {LabelfunctionModel} from "../../models/labelfunction.model";
import {catchError} from "rxjs/operators";
import {throwError} from "rxjs";
import {environmentProd} from "../../../environments/environment.prod";
import {environmentDev} from "../../../environments/environment";
import {AnalysisModel} from "../../models/analysis.model";
import {DataframeModel} from "../../models/dataframe.model";

// const labelfuntionURL = `${environmentProd.protocol}://${environmentProd.ip_adresse}/settings/labelfunction`;
const labelfuntionURL = `${environmentDev.protocol}://${environmentDev.ip_adresse}:${environmentDev.port}/settings/labelfunction`;


@Injectable({providedIn: "root"})
export class LabelfunctionService {


  constructor(private http: HttpClient) {
  }

  testAndSaveLabelfunction(labelfunction: LabelfunctionModel, workflow_id: number){
    return this.http.post<{summary: AnalysisModel, summary_train: AnalysisModel, df_combined: DataframeModel[], lid: number}>(`${labelfuntionURL}/workflow/${workflow_id}/`, labelfunction).pipe(catchError(this.handleError));
  }

  testAndUpdateLabelfunctions(labelfunction_id: number, labelfunction: LabelfunctionModel, workflow_id: number){
    return this.http.patch<{summary: AnalysisModel, summary_train: AnalysisModel, df_combined: DataframeModel[], lid: number}>(`${labelfuntionURL}/${labelfunction_id}/modifiy/`, {labelfunction, workflow_id}).pipe(catchError(this.handleError));
  }



  getLabelfunctionsByWorkflowID(workflow_id: number){
    return this.http.get<LabelfunctionModel[]>(`${labelfuntionURL}/workflow/${workflow_id}/`).pipe(catchError(this.handleError));
  }

  getImportLabels(workflow_id: number, type: string){
    return this.http.get<LabelfunctionModel>(`${labelfuntionURL}/workflow/${workflow_id}/${type}/`).pipe(catchError(this.handleError));
  }

  updateImports(workflow_id: number, labelfunction: LabelfunctionModel){
    return this.http.patch(`${labelfuntionURL}/workflow/${workflow_id}/import/`, labelfunction).pipe(catchError(this.handleError));
  }

  getLabelfunctionsByID(labelfunction_id: number){
    return this.http.get<LabelfunctionModel>(`${labelfuntionURL}/${labelfunction_id}/modifiy/`).pipe(catchError(this.handleError));
  }

  deleteLabelfunctions(labelfunction_id: number){
    return this.http.delete<{message: string}>(`${labelfuntionURL}/${labelfunction_id}/modifiy/`).pipe(catchError(this.handleError));
  }



  private handleError(error: HttpErrorResponse){
    if (error.error.non_field_errors != null) {
      return throwError(() => error.error.non_field_errors);
    } else if (error.error.message != null){
      return throwError(() => new Error(error.error.message));
    } else if (error.error.code != null){
      const code: string = 'import: ' + error.error.code[0]
      return throwError(() => new Error(code));
    } else if (error.error != null){
      return throwError(() => new Error(error.error));
    }
    return throwError(() => new Error('An unknown error occurred'));
  }

}
