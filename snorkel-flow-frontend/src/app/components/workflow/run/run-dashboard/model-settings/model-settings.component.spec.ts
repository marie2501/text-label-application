import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModelSettingsComponent } from './model-settings.component';

describe('ModelSettingsComponent', () => {
  let component: ModelSettingsComponent;
  let fixture: ComponentFixture<ModelSettingsComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModelSettingsComponent]
    });
    fixture = TestBed.createComponent(ModelSettingsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
