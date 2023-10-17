import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RunDashboardComponent } from './run-dashboard.component';

describe('RunDashboardComponent', () => {
  let component: RunDashboardComponent;
  let fixture: ComponentFixture<RunDashboardComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RunDashboardComponent]
    });
    fixture = TestBed.createComponent(RunDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
