import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelfunctionUpdateComponent } from './labelfunction-update.component';

describe('LabelfunctionUpdateComponent', () => {
  let component: LabelfunctionUpdateComponent;
  let fixture: ComponentFixture<LabelfunctionUpdateComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LabelfunctionUpdateComponent]
    });
    fixture = TestBed.createComponent(LabelfunctionUpdateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
