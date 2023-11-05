import {Injectable} from "@angular/core";
import {HttpClient} from '@angular/common/http';
import {RunModel} from "../../models/run.model";
import {AnalysisModel} from "../../models/analysis.model";

const labelfuntionURL = 'http://localhost:8080/settings/workflow';



@Injectable({providedIn: "root"})
export class RunService {


  constructor(private http: HttpClient) {
  }


  createlabelfunctionRun(run: {labelfunctions: (number|undefined)[]}, workflow_id: number) {
    return this.http.post(`${labelfuntionURL}/${workflow_id}/run/`, run);
  }

  getlabelfunctionRun(run_id: number) {
    return this.http.get<RunModel>(`${labelfuntionURL}/${run_id}/run/`);
  }

  listlabelfunctionRun(workflow_id: number) {
    return this.http.get<RunModel[]>(`${labelfuntionURL}/${workflow_id}/run/list/`);
  }

  executelabelfunctionRun(run_id: number) {
    return this.http.get(`${labelfuntionURL}/${run_id}/run/exec/`);
  }

  getAnalysisRun(run_id: number) {
    return this.http.get<AnalysisModel>(`${labelfuntionURL}/${run_id}/run/analysis/`);
  }


}
