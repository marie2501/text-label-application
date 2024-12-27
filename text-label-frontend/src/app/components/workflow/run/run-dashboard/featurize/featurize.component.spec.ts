import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FeaturizeComponent } from './featurize.component';

describe('FeaturizeComponent', () => {
  let component: FeaturizeComponent;
  let fixture: ComponentFixture<FeaturizeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [FeaturizeComponent]
    });
    fixture = TestBed.createComponent(FeaturizeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
