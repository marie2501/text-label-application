import {Component, Input} from '@angular/core';
import {RunService} from "../../../../../services/workflow/run.service";
import {Message, MessageService} from "primeng/api";

@Component({
  selector: 'app-model-settings',
  templateUrl: './model-settings.component.html',
  styleUrls: ['./model-settings.component.css']
})
export class ModelSettingsComponent {

  constructor(private runservices: RunService, private messageService: MessageService) {
  }

  @Input()
  run_id: number = 0;

  selectedLabelModel: string = '';
  selectedClassifier: string = '';
  selectedFeaturize: string = '';

  range_x: number = 1;
  range_y: number = 1;
  errorMessage: Message[] = [];

  // todo implemnt function und backend + datenbank änderung -> zeige dies in run dashboard
  saveModel() {
    let data: {selectedModelClassifier: string, selectedModelLabel: string,
      selectedModelFeaturize: string, range_x: number, range_y: number} = {selectedModelClassifier: this.selectedClassifier,
      selectedModelLabel: this.selectedLabelModel,
      selectedModelFeaturize: this.selectedFeaturize, range_x: this.range_x, range_y: this.range_y}
    if(this.selectedClassifier != '' && this.selectedLabelModel != '' && this.selectedFeaturize != '' &&
      this.range_x >= 1 && this.range_y >= 1){
      if (this.selectedClassifier == 'Naive Bayes'){
        this.runservices.naiveBayesClassifier(this.run_id, data).subscribe(respData => {
          this.showSuccessMessage();
        }, error => {
          this.showErrorMessage(error);
        })
      }
    } else {
      console.log('error');
    }
  }

  onClose() {

  }


  onChangeLabelvote($event: string) {
    this.selectedLabelModel = $event;
  }

  onChangeClassifier($event: string) {
    this.selectedClassifier = $event;
    console.log(this.selectedClassifier)
  }

  onChangeFuturize($event: { selectedModel: string; range_x: number; range_y: number }) {
    this.range_x = $event.range_x;
    this.range_y = $event.range_y;
    this.selectedFeaturize = $event.selectedModel;
  }

  private showErrorMessage(error: any) {
    this.errorMessage = [];
    this.errorMessage = [
      {severity: 'error', summary: 'Error', detail: error.error }];
  }

  showSuccessMessage(){
    this.messageService.add({ key: 'bc', severity: 'success',
      summary: 'Success', detail: 'Classifier has been successfully trained' });
  }

}
