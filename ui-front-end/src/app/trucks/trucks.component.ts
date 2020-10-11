import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Command } from '../shared/Command';
import { FirestoreDataService } from '../service/firestore-data.service';

@Component({
  selector: 'app-trucks',
  templateUrl: './trucks.component.html',
  styleUrls: ['./trucks.component.css']
})
export class TrucksComponent implements OnInit {
  command=""
  arguments=""
  constructor(private router:Router, private _data: FirestoreDataService) { }

  ngOnInit(): void {
  }

  send(): void{
    if(this.command.length>0 && this.arguments.length>0){
      console.log("Command = "+this.command)
      console.log("Arguments = "+this.arguments)
      //this._data.sendCommand(new Command(this.command, this.arguments))
    } else{
      console.log("Command and arguments should not be empty")
    }
  }

}
