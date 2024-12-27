import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelfunctionAnalysisComponent } from './labelfunction-analysis.component';

describe('LabelfunctionAnalysisComponent', () => {
  let component: LabelfunctionAnalysisComponent;
  let fixture: ComponentFixture<LabelfunctionAnalysisComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LabelfunctionAnalysisComponent]
    });
    fixture = TestBed.createComponent(LabelfunctionAnalysisComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
