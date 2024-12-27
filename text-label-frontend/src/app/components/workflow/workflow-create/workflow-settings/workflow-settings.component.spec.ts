import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkflowSettingsComponent } from './workflow-settings.component';

describe('WorkflowSettingsComponent', () => {
  let component: WorkflowSettingsComponent;
  let fixture: ComponentFixture<WorkflowSettingsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WorkflowSettingsComponent]
    });
    fixture = TestBed.createComponent(WorkflowSettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
