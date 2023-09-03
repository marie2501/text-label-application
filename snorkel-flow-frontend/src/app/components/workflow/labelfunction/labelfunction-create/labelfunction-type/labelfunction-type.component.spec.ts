import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelfunctionTypeComponent } from './labelfunction-type.component';

describe('LabelfunctionTypeComponent', () => {
  let component: LabelfunctionTypeComponent;
  let fixture: ComponentFixture<LabelfunctionTypeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LabelfunctionTypeComponent]
    });
    fixture = TestBed.createComponent(LabelfunctionTypeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
