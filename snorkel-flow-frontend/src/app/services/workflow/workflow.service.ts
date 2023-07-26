import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, Subject, tap, throwError} from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import {WorkflowModel} from "../../models/workflow.model";

const workflowURL = 'http://localhost:8080/settings/workflow';



@Injectable({providedIn: "root"})
export class WorkflowService {


  constructor(private http: HttpClient) {
  }

  createWorkflow(workflow: WorkflowModel) {
    return this.http.post<{id: number}>(`${workflowURL}/create/`, workflow);
  }


}
