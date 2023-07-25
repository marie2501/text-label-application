import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkflowCreateComponent } from './workflow-create.component';

describe('WorkflowCreateComponent', () => {
  let component: WorkflowCreateComponent;
  let fixture: ComponentFixture<WorkflowCreateComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WorkflowCreateComponent]
    });
    fixture = TestBed.createComponent(WorkflowCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
