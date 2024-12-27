import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelfunctionCodeComponent } from './labelfunction-code.component';

describe('LabelfunctionCodeComponent', () => {
  let component: LabelfunctionCodeComponent;
  let fixture: ComponentFixture<LabelfunctionCodeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LabelfunctionCodeComponent]
    });
    fixture = TestBed.createComponent(LabelfunctionCodeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
