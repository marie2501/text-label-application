import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {throwError} from "rxjs";
import {catchError} from "rxjs/operators";



const fileURL = 'http://localhost:8080/settings/file_upload';



@Injectable({providedIn: "root"})
export class FileService {


  constructor(private http: HttpClient) {
  }

  fileUpload(formData: FormData, workflow_id: number) {
    return this.http.post(`${fileURL}/${workflow_id}/`, formData).pipe(catchError(this.handleError));
  }

  fileUpdate(formData: FormData, workflow_id: number) {
    return this.http.put(`${fileURL}/${workflow_id}/`, formData).pipe(catchError(this.handleError));
  }

  getFileNamesByWorkflowId(workflow_id: number){
    return this.http.get<{id: number, name: string}>(`${fileURL}/${workflow_id}/`).pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse){
    if (error.status == 403){
      return throwError(() => new Error('You do not have the authorization to change the dataset.'));
    } else if (error.status == 404){
      return throwError(() => new Error('The dataset or workflow does not exists.'));
    } else if (error.status == 400){
      if (error.error.non_field_errors){
        return throwError(() => new Error(error.error.non_field_errors));
      }
      return throwError(() => new Error(error.error));
    }
    return throwError(() => new Error('An unknown error occurred'));
  }

}
