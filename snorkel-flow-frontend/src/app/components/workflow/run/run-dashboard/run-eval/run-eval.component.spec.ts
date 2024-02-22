import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RunEvalComponent } from './run-eval.component';

describe('RunEvalComponent', () => {
  let component: RunEvalComponent;
  let fixture: ComponentFixture<RunEvalComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RunEvalComponent]
    });
    fixture = TestBed.createComponent(RunEvalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
