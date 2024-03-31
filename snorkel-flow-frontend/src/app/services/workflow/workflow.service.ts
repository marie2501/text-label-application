import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, Subject, tap, throwError} from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import {WorkflowModel} from "../../models/workflow.model";
import {environmentProd} from "../../../environments/environment.prod";
import {environmentDev} from "../../../environments/environment";

const workflowURL = `http://${environmentProd.ip_adresse}:${environmentProd.port}/settings/workflow`;



@Injectable({providedIn: "root"})
export class WorkflowService {

  currentWorkflow = new Subject<{isOnWorkflow: boolean, id: number}>();


  constructor(private http: HttpClient) {
  }

  updateCurrentWorkflow(isOnWorkflow: boolean, id: number){
    return this.currentWorkflow.next({isOnWorkflow: isOnWorkflow, id: id});
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

  getAllUsers(workflow_id: number){
    return this.http.get<{items: { label: string, value: string }[], label: string}[] >(`${workflowURL}/${workflow_id}/contributer/`).pipe(catchError(this.handleError));
  }

  isWorkflowCreator(workflow_id: number){
    return this.http.get<{ isCreator: boolean }>(`${workflowURL}/${workflow_id}/isCreator/`).pipe(catchError(this.handleError));
  }

  addContributer(workflow_id: number, username: string){
    return this.http.post(`${workflowURL}/${workflow_id}/contributer/`, {'username': username}).pipe(catchError(this.handleError));
  }

  deleteContributer(workflow_id: number, username: string){
    return this.http.delete(`${workflowURL}/${workflow_id}/contributer/`, {'body': {'username': username}}).pipe(catchError(this.handleError));
  }

  getInstalledPackages(){
    return this.http.get<string[]>(`${workflowURL}/package/`);
  }

  private handleError(error: HttpErrorResponse){
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
