import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RunAnalysisDatapointsComponent } from './run-analysis-datapoints.component';

describe('RunAnalysisDatapointsComponent', () => {
  let component: RunAnalysisDatapointsComponent;
  let fixture: ComponentFixture<RunAnalysisDatapointsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RunAnalysisDatapointsComponent]
    });
    fixture = TestBed.createComponent(RunAnalysisDatapointsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
