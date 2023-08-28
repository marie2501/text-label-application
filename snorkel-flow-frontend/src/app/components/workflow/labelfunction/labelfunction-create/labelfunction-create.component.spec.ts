import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelfunctionCreateComponent } from './labelfunction-create.component';

describe('LabelfunctionCreateComponent', () => {
  let component: LabelfunctionCreateComponent;
  let fixture: ComponentFixture<LabelfunctionCreateComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LabelfunctionCreateComponent]
    });
    fixture = TestBed.createComponent(LabelfunctionCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
