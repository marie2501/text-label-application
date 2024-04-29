import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {map, Observable, of, Subject, tap, throwError} from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import {WorkflowModel} from "../../models/workflow.model";
import {environmentProd} from "../../../environments/environment.prod";
import {environmentDev} from "../../../environments/environment";

// const workflowURL = `${environmentProd.protocol}://${environmentProd.ip_adresse}/settings/workflow`;
const workflowURL = `${environmentDev.protocol}://${environmentDev.ip_adresse}:${environmentDev.port}/settings/workflow`;



@Injectable({providedIn: "root"})
export class WorkflowService {

  currentWorkflow = new Subject<{isOnWorkflow: boolean, id: number}>();


  constructor(private http: HttpClient) {
  }

  updateCurrentWorkflow(isOnWorkflow: boolean, id: number){
    return this.currentWorkflow.next({isOnWorkflow: isOnWorkflow, id: id});
  }


  accessWorkflow(workflow_id: number): Observable<boolean>{
    return this.http.get<boolean>(`${workflowURL}/${workflow_id}/access/`).pipe(catchError(this.handleError));
  }

  createWorkflow(workflow: WorkflowModel) {
    return this.http.post<{workflow_id: number}>(`${workflowURL}/`, workflow).pipe(catchError(this.handleError));
  }

  getWorkflows(){
    return this.http.get<WorkflowModel[]>(`${workflowURL}/`).pipe(catchError(this.handleError));
  }

  getWorkflowById(workflow_id: number){
    return this.http.get<WorkflowModel>(`${workflowURL}/${workflow_id}/`).pipe(catchError(this.handleError));
  }

  isWorkflowCreator(workflow_id: number){
    return this.http.get<{ isCreator: boolean }>(`${workflowURL}/${workflow_id}/isCreator/`).pipe(catchError(this.handleError));
  }

  getContributers(workflow_id: number){
    return this.http.get<{ username: string }[]>(`${workflowURL}/${workflow_id}/contributer/`).pipe(catchError(this.handleError));
  }

  filterPossibleContributer(workflow_id: number, username_start: string){
    return this.http.get<{ username: string }[]>(`${workflowURL}/${workflow_id}/contributer/modify/`).pipe(catchError(this.handleError));
  }

  addContributer(workflow_id: number, username: string){
    return this.http.post(`${workflowURL}/${workflow_id}/contributer/modify/`, {'username': username}).pipe(catchError(this.handleError));
  }

  deleteContributer(workflow_id: number, username: string){
    return this.http.delete(`${workflowURL}/${workflow_id}/contributer/modify/`, {'body': {'username': username}}).pipe(catchError(this.handleError));
  }

  //todo auslagern in eigenen info/hilf service
  getInstalledPackages(){
    return this.http.get<string[]>(`${workflowURL}/package/`);
  }

  private handleError(error: HttpErrorResponse){
    console.log(error)
    if(error.error.description != null) {
      return throwError(() => new Error('Description can not be blank'));
    } else if (error.error.title != null)  {
      return throwError(() => new Error('Title can not be blank'));
    } else if (error.error.non_field_errors != null) {
      return throwError(() => error.error.non_field_errors);
    } else if (error.status == 403){
      return throwError(() => new Error('You do not have authorization to access this resource'));
    } else if (error.status == 404){
      return throwError(() => new Error('The requested resource does not exists.'));
    } else if (error.status == 400){
      return throwError(() => new Error(error.error));
    }
    return throwError(() => new Error('An unknown error occurred'));
  }
}
