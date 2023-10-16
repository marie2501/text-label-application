import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelfunctionListComponent } from './labelfunction-list.component';

describe('LabelfunctionListComponent', () => {
  let component: LabelfunctionListComponent;
  let fixture: ComponentFixture<LabelfunctionListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LabelfunctionListComponent]
    });
    fixture = TestBed.createComponent(LabelfunctionListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
