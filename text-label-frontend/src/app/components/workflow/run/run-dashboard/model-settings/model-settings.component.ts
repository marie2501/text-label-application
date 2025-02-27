import {Component, OnInit, ViewEncapsulation} from '@angular/core';
import {RunService} from "../../../../../services/workflow/run.service";
import {Message, MessageService} from "primeng/api";
import {ActivatedRoute} from "@angular/router";

@Component({
  selector: 'app-model-settings',
  templateUrl: './model-settings.component.html',
  styleUrls: ['./model-settings.component.css']
})
export class ModelSettingsComponent implements OnInit{

  run_id: number = 0;

  selectedLabelModel: string = '';
  selectedClassifier: string = '';
  selectedFeaturize: string = '';

  range_x: number = 1;
  range_y: number = 1;
  n_epochs : number = 100;
  log_freq : number = 10;
  seed : number = 123;
  base_learning_rate : number = 0.01;
  l2: number = 0.0;
  workflow_id: number = 0;
  df_combined: {columns: string[], index: string[], data: string[][]} = {columns: [], index : [], data: []};
  isClassified: boolean = false;
  filterAbstain: boolean = false;
  selectedTie: string = '';

  errorMessage: Message[] = [];
  classfierData: Message[] = [];
  classifierResult: { score_train: number, score_test: number } = {score_train: -1, score_test: -1};

  constructor(private runservices: RunService, private messageService: MessageService, private route: ActivatedRoute) {
  }

  ngOnInit(): void {
    this.route.parent?.params.subscribe((params) => {
      this.run_id = params['runID'];
      this.workflow_id = params['wid'];
    }).unsubscribe();
  }

  saveModel() {
    let data: {selectedModelClassifier: string, selectedModelLabel: string, selectedTie: string, filterAbstain: boolean,
      selectedModelFeaturize: string, range_x: number, range_y: number, n_epochs : number, log_freq : number,
      seed : number, base_learning_rate : number, l2: number} = {selectedModelClassifier: this.selectedClassifier, filterAbstain: this.filterAbstain,
      selectedModelLabel: this.selectedLabelModel, selectedTie: this.selectedTie, l2: this.l2, seed: this.seed, n_epochs: this.n_epochs,
      base_learning_rate: this.base_learning_rate, log_freq: this.log_freq,
      selectedModelFeaturize: this.selectedFeaturize, range_x: this.range_x, range_y: this.range_y}

    if(this.selectedClassifier != '' && this.selectedLabelModel != '' && this.selectedTie != '' && this.selectedFeaturize != '' &&
      (this.range_x && this.range_y) >= 1 && (this.l2 && this.seed && this.log_freq && this.seed && this.base_learning_rate) >= 0){
      this.runservices.trainClassifier(this.run_id, data).subscribe(respData => {
        this.classifierResult = respData;
        this.df_combined = respData.df_combined
        if(this.classifierResult.score_test != -1){
          this.classfierData = [];
          this.classfierData = [
            {severity: 'info', summary: 'Results', detail: `Trainings-Score: ${this.classifierResult.score_train}  und  Test-Score: ${this.classifierResult.score_test}` }];
          }
        this.showSuccessMessage();
        this.isClassified = true;
        }, error => {
          this.showErrorMessage(error);
        });
      } else {
      this.showErrorMessage('An error has occurred. Make a selection, range x and y must be greater than or equal to 1, all other values must be greater than or equal to 0');
    }
  }


  onChangeLabelvote($event: {selectedModel: string , selectedTie: string, n_epochs : number, log_freq : number,
    seed : number, base_learning_rate : number, l2: number}) {
    this.selectedLabelModel = $event.selectedModel;
    this.selectedTie = $event.selectedTie;
    this.l2 = $event.l2;
    this.seed = $event.seed;
    this.log_freq = $event.log_freq;
    this.base_learning_rate = $event.base_learning_rate;
    this.n_epochs = $event.n_epochs;
  }

  onChangeClassifier($event: { classifier: string, filterAbstain: boolean }) {
    this.selectedClassifier = $event.classifier;
    this.filterAbstain = $event.filterAbstain;
  }

  onChangeFeaturize($event: { selectedModel: string; range_x: number; range_y: number }) {
    this.range_x = $event.range_x;
    this.range_y = $event.range_y;
    this.selectedFeaturize = $event.selectedModel;
  }

  private showErrorMessage(error: any) {
    this.errorMessage = [];
    this.errorMessage = [
      {severity: 'error', summary: 'Error', detail: error }];
  }

  showSuccessMessage(){
    this.messageService.add({ key: 'bc', severity: 'success',
      summary: 'Success', detail: 'Classifier has been successfully trained' });
  }

}
