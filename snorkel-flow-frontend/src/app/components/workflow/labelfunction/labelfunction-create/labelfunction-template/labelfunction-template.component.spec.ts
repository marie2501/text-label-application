import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelfunctionTemplateComponent } from './labelfunction-template.component';

describe('LabelfunctionTemplateComponent', () => {
  let component: LabelfunctionTemplateComponent;
  let fixture: ComponentFixture<LabelfunctionTemplateComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LabelfunctionTemplateComponent]
    });
    fixture = TestBed.createComponent(LabelfunctionTemplateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
