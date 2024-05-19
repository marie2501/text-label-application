import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GenerateTemplateComponent } from './generate-template.component';

describe('GenerateTemplateComponent', () => {
  let component: GenerateTemplateComponent;
  let fixture: ComponentFixture<GenerateTemplateComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [GenerateTemplateComponent]
    });
    fixture = TestBed.createComponent(GenerateTemplateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
