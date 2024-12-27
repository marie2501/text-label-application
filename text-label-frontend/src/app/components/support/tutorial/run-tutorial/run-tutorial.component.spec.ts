import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RunTutorialComponent } from './run-tutorial.component';

describe('RunTutorialComponent', () => {
  let component: RunTutorialComponent;
  let fixture: ComponentFixture<RunTutorialComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RunTutorialComponent]
    });
    fixture = TestBed.createComponent(RunTutorialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
