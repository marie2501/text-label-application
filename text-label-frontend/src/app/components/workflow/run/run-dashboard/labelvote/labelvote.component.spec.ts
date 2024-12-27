import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LabelvoteComponent } from './labelvote.component';

describe('LabelvoteComponent', () => {
  let component: LabelvoteComponent;
  let fixture: ComponentFixture<LabelvoteComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [LabelvoteComponent]
    });
    fixture = TestBed.createComponent(LabelvoteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
