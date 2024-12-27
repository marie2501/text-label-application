import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelfunctionTutorialComponent } from './labelfunction-tutorial.component';

describe('LabelfunctionTutorialComponent', () => {
  let component: LabelfunctionTutorialComponent;
  let fixture: ComponentFixture<LabelfunctionTutorialComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LabelfunctionTutorialComponent]
    });
    fixture = TestBed.createComponent(LabelfunctionTutorialComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
