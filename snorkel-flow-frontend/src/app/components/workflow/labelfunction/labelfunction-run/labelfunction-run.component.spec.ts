import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelfunctionRunComponent } from './labelfunction-run.component';

describe('LabelfunctionRunComponent', () => {
  let component: LabelfunctionRunComponent;
  let fixture: ComponentFixture<LabelfunctionRunComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LabelfunctionRunComponent]
    });
    fixture = TestBed.createComponent(LabelfunctionRunComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
