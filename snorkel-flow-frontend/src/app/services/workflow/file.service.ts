import {Injectable} from "@angular/core";
import {HttpClient} from '@angular/common/http';



const fileURL = 'http://localhost:8080/settings/file_upload';



@Injectable({providedIn: "root"})
export class FileService {


  constructor(private http: HttpClient) {
  }

  fileUpload(formData: FormData, workflow_id: number) {
    return this.http.post(`${fileURL}/${workflow_id}/`, formData);
  }

  getFileNamesByWorkflowId(workflow_id: number){
    return this.http.get<{id: number, name: string}[]>(`${fileURL}/${workflow_id}/`);
  }

}
