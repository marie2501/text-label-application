import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {Observable, Subject, tap, throwError} from 'rxjs';
import { catchError, retry } from 'rxjs/operators';
import {WorkflowModel} from "../../models/workflow.model";

const workflowURL = 'http://localhost:8080/settings/workflow';
const fileURL = 'http://localhost:8080/settings/file_upload';



@Injectable({providedIn: "root"})
export class WorkflowService {


  constructor(private http: HttpClient) {
  }

  createWorkflow(workflow: WorkflowModel) {
    return this.http.post<{workflow_id: number}>(`${workflowURL}/`, workflow);
  }

  getWorkflows(){
    return this.http.get<WorkflowModel[]>(`${workflowURL}/`);
  }

  labeledfileUpload(formData: FormData, workflow_id: number) {
    return this.http.post(`${fileURL}/${workflow_id}/`, formData);
  }

  unlabeledfileUpload(formData: FormData) {
    return this.http.post(`${fileURL}/`, formData);
  }


}
