import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkflowTutorialComponent } from './workflow-tutorial.component';

describe('WorkflowTutorialComponent', () => {
  let component: WorkflowTutorialComponent;
  let fixture: ComponentFixture<WorkflowTutorialComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WorkflowTutorialComponent]
    });
    fixture = TestBed.createComponent(WorkflowTutorialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
