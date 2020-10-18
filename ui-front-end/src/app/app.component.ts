import { Component} from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})

export class AppComponent {
  links = [
   // { title: 'Home', fragment: 'home' },
    { title: 'Trucks', fragment: 'load' },
    //{ title: 'Truck Management', fragment: 'truck' },
    { title: 'Profile', fragment: 'user' },

  ];
  
  constructor(public route: ActivatedRoute) {}

}
