import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkflowFileComponent } from './workflow-file.component';

describe('WorkflowFileComponent', () => {
  let component: WorkflowFileComponent;
  let fixture: ComponentFixture<WorkflowFileComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WorkflowFileComponent]
    });
    fixture = TestBed.createComponent(WorkflowFileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
