import {Injectable} from "@angular/core";
import {HttpClient, HttpErrorResponse} from '@angular/common/http';
import {throwError} from "rxjs";
import {catchError} from "rxjs/operators";
import {environmentProd} from "../../../environments/environment.prod";
import {environmentDev} from "../../../environments/environment";



// const fileURL = `${environmentProd.protocol}://${environmentProd.ip_adresse}/settings/file_upload`;
const fileURL = `${environmentDev.protocol}://${environmentDev.ip_adresse}:${environmentDev.port}/settings/file_upload`;



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

  getIsFileUploaded(workflow_id: number){
    return this.http.get<boolean>(`${fileURL}/${workflow_id}/`).pipe(catchError(this.handleError));
  }

  getCSVFile( run_id: number, type: string) {
    return this.http.get<any>(`${fileURL}/download/${run_id}/${type}/`, {
      responseType: 'text' as any
    }).pipe(catchError(this.handleError));
  }

  private handleError(error: HttpErrorResponse){
    if (error.error.non_field_errors != null){
      return throwError(() => new Error(error.error.non_field_errors));
    } else if (error.error != null){
      return throwError(() => new Error(error.error));
    }
    return throwError(() => new Error('An unknown error occurred'));
  }

}
