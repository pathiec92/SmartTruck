import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PastLoadComponent } from './past-load.component';

describe('PastLoadComponent', () => {
  let component: PastLoadComponent;
  let fixture: ComponentFixture<PastLoadComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PastLoadComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PastLoadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
