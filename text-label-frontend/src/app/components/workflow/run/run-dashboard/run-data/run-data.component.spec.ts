import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RunDataComponent } from './run-data.component';

describe('RunDataComponent', () => {
  let component: RunDataComponent;
  let fixture: ComponentFixture<RunDataComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RunDataComponent]
    });
    fixture = TestBed.createComponent(RunDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
