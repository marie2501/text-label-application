import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {LabelfunctionModel} from "../../models/labelfunction.model";
import {catchError} from "rxjs/operators";
import {throwError} from "rxjs";

const labelfuntionURL = 'http://localhost:8080/settings/workflow';



@Injectable({providedIn: "root"})
export class LabelfunctionService {


  constructor(private http: HttpClient) {
  }

  compileLabelfunction(pythoncode: string, workflow_id: number){
    return this.http.post(`${labelfuntionURL}/labelfunction/${workflow_id}/compile/`, {pythoncode}).pipe(catchError(this.handleError));
  }

  testLabelfunction(pythoncode: string, name: string, workflow_id: number){
    return this.http.post<number>(`${labelfuntionURL}/${workflow_id}/labelfunction/test/`, {pythoncode, name}).pipe(catchError(this.handleError));
  }

  createLabelfunction(labelfunction: LabelfunctionModel, workflow_id: number) {
    return this.http.post<{workflow_id: number}>(`${labelfuntionURL}/${workflow_id}/labelfunction/`, labelfunction).pipe(catchError(this.handleError));
  }

  getLabelfunctions(workflow_id: number){
    return this.http.get<LabelfunctionModel[]>(`${labelfuntionURL}/${workflow_id}/labelfunction/`).pipe(catchError(this.handleError));
  }

  getLabelfunctionsByID(labelfunction_id: number){
    return this.http.get<LabelfunctionModel>(`${labelfuntionURL}/labelfunction/${labelfunction_id}/`).pipe(catchError(this.handleError));
  }

  deleteLabelfunctions(labelfunction_id: number){
    return this.http.delete(`${labelfuntionURL}/${labelfunction_id}/labelfunction/`).pipe(catchError(this.handleError));
  }

  getImports(workflow_id: number){
    return this.http.get<LabelfunctionModel>(`${labelfuntionURL}/${workflow_id}/labelfunction/import/`).pipe(catchError(this.handleError));
  }

  updateLabelfunctions(labelfunction_id: number, labelfunction: LabelfunctionModel){
    return this.http.patch(`${labelfuntionURL}/${labelfunction_id}/labelfunction/`, labelfunction).pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse){
    if (error.status == 403){
      return throwError(() => new Error('You do not have the authorization to change the label function.'));
    } else if (error.status == 404){
      return throwError(() => new Error('The label function does not exists.'));
    } else if (error.status == 400){
      return throwError(() => new Error(error.error));
    }
    return throwError(() => new Error('An unknown error occurred'));
  }

}
