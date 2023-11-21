import {Component, OnInit} from '@angular/core';
import {RunService} from "../../../../services/workflow/run.service";
import {LabelfunctionService} from "../../../../services/workflow/labelfunction.service";
import {ActivatedRoute} from "@angular/router";
import {RunModel} from "../../../../models/run.model";
import {LabelfunctionModel} from "../../../../models/labelfunction.model";
import {AnalysisModel} from "../../../../models/analysis.model";

@Component({
  selector: 'app-run-dashboard',
  templateUrl: './run-dashboard.component.html',
  styleUrls: ['./run-dashboard.component.css']
})
export class RunDashboardComponent implements OnInit{
  workflow_id: number = 0;
  run_id: number = 0;
  // @ts-ignore
  run: RunModel;
  runLoaded!: Promise<boolean>;
  labelfunctions: LabelfunctionModel[] = [];

  // @ts-ignore
   analysisModel: AnalysisModel;
   analysisLoaded!: Promise<boolean>;
  isLabelModelHidden: boolean = false;
  isFeatureHidden: boolean = false;
  isClassifierHidden: boolean = false;


  constructor(private runService: RunService, private labelfunctionService: LabelfunctionService, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.workflow_id = this.route.snapshot.params['id'];
    this.run_id = this.route.snapshot.params['runID'];
    this.runService.getlabelfunctionRun(this.run_id).subscribe(respData => {
      console.log(respData);
      this.run = respData;
      this.labelfunctions = this.run.labelfunctions!;
      this.runLoaded = Promise.resolve(true);
    }, error => {
      console.log(error);
    })
  }

  executeRun() {
    this.runService.executelabelfunctionRun(this.run_id).subscribe(respData => {
    }, error => {
      console.log(error);
    });
  }

  getAnalysis() {
    this.runService.getAnalysisRun(this.run_id).subscribe(respData => {
      this.analysisModel = respData;
      console.log(this.analysisModel)
      this.analysisLoaded = Promise.resolve(true);
    }, error => {
      console.log(error);
    });
  }

  openLabelModel() {
    this.isLabelModelHidden = true;
  }

  closeLabelModel($event: boolean) {
    this.isLabelModelHidden = $event;
  }

  openFeaturExraction() {
    this.isFeatureHidden = true;
  }

  closeFeature($event: boolean) {
    this.isFeatureHidden = $event;
  }

  openClassifier() {
    this.isClassifierHidden = true;
  }

  closeClassifier($event: boolean) {
    this.isClassifierHidden = $event;
  }

}
