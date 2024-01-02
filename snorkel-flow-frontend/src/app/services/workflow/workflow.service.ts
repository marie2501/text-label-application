import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, Subject, tap, throwError} from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import {WorkflowModel} from "../../models/workflow.model";

const workflowURL = 'http://localhost:8080/settings/workflow';



@Injectable({providedIn: "root"})
export class WorkflowService {

  currentWorkflow = new Subject<{isOnWorkflow: boolean, id: number}>();


  constructor(private http: HttpClient) {
  }

  updateCurrentWorkflow(isOnWorkflow: boolean, id: number){
    return this.currentWorkflow.next({isOnWorkflow: isOnWorkflow, id: id});
  }

  createWorkflow(workflow: WorkflowModel) {
    return this.http.post<{workflow_id: number}>(`${workflowURL}/`, workflow);
  }

  getWorkflows(){
    return this.http.get<WorkflowModel[]>(`${workflowURL}/`);
  }

  getWorkflowById(workflow_id: number){
    return this.http.get<WorkflowModel>(`${workflowURL}/${workflow_id}/`);
  }

  getAllUsers(workflow_id: number){
    return this.http.get<{items: { label: string, value: string }[], label: string}[] >(`${workflowURL}/${workflow_id}/contributer/`);
  }

  isWorkflowCreator(workflow_id: number){
    return this.http.get<{ isCreator: boolean }>(`${workflowURL}/${workflow_id}/isCreator/`);
  }

  addContributer(workflow_id: number, username: string){
    return this.http.post(`${workflowURL}/${workflow_id}/contributer/`, {'username': username});
  }

  deleteContributer(workflow_id: number, username: string){
    return this.http.delete(`${workflowURL}/${workflow_id}/contributer/`, {'body': {'username': username}});
  }


}
