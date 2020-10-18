import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-disp-pastload',
  templateUrl: './disp-pastload.component.html',
  styleUrls: ['./disp-pastload.component.css']
})
export class DispPastloadComponent implements OnInit {

  content:string = "This will be the content"
  constructor() { }

  ngOnInit(): void {
  }

}
