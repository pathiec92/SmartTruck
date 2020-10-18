import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DispPastloadComponent } from './disp-pastload.component';

describe('DispPastloadComponent', () => {
  let component: DispPastloadComponent;
  let fixture: ComponentFixture<DispPastloadComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DispPastloadComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DispPastloadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
