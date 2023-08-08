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

  labeledfileUpload(formData: FormData) {
    return this.http.post(`${fileURL}/`, formData);
  }

  unlabeledfileUpload(formData: FormData) {
    return this.http.post(`${fileURL}/`, formData);
  }


}
