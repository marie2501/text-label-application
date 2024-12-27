import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ContributerComponent } from './contributer.component';

describe('ContributerComponent', () => {
  let component: ContributerComponent;
  let fixture: ComponentFixture<ContributerComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ContributerComponent]
    });
    fixture = TestBed.createComponent(ContributerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
