import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelfunctionAnalysisDatapointsComponent } from './labelfunction-analysis-datapoints.component';

describe('LabelfunctionAnalysisDatapointsComponent', () => {
  let component: LabelfunctionAnalysisDatapointsComponent;
  let fixture: ComponentFixture<LabelfunctionAnalysisDatapointsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LabelfunctionAnalysisDatapointsComponent]
    });
    fixture = TestBed.createComponent(LabelfunctionAnalysisDatapointsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
