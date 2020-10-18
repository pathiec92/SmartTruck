import { Component, NgZone, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { interval, Subscription } from 'rxjs';
import { take } from 'rxjs/operators';
import { FirestoreDataService } from '../service/firestore-data.service';
import { Command } from '../shared/Command';
import { CMD_SENDING, CMD_SENT_FAIL, CMD_SENT_SUCCESS, ConnectProgress, INIT, INIT_CMD } from '../shared/util';

@Component({
  selector: 'app-command',
  templateUrl: './command.component.html',
  styleUrls: ['./command.component.css']
})
export class CommandComponent implements OnInit , OnDestroy{
  tripStatus : ConnectProgress = INIT_CMD
  truckId = ""
  sl = ""
  command=""
  arguments=""
  servingCmd = false
  cmdCounterSub: Subscription = null

  constructor(private zone:NgZone, private _data: FirestoreDataService,
    private route:ActivatedRoute) { }

  ngOnInit(): void {
    this.truckId = this.route.snapshot.params['truckId']
    this.sl = this.route.snapshot.params['sl']
    this.subscribeTruckCommand()

  }

  subscribeTruckCommand():void{
    this._data.subScribeTruckCommand(this.truckId).subscribe(
      (al:Command[]) => {
        console.log(`Command length = ${al.length}`)
        if(al.length>0 && al[0].ack !=null ){
          console.log(`Command ${al[0].command}, length = ${al.length}`)
          this.tripStatus = CMD_SENT_SUCCESS
          this.servingCmd = false
          if(this.cmdCounterSub != null){
            this.cmdCounterSub.unsubscribe()
          }
        }
      }
    )
  }

  send(): void{
    if(this.command.length>0 && this.arguments.length>0){
      console.log("Command = "+this.command)
      console.log("Arguments = "+this.arguments)
      this._data.sendCommand(this.truckId,new Command(this.truckId, this.command, this.arguments))
      this.command = ""
      this.arguments = ""
      this.servingCmd = true
      this.tripStatus = CMD_SENDING
      this.cmdCounterSub =  this.counter(()=>{
        this.tripStatus = CMD_SENT_FAIL
        this.servingCmd = false
        this.cmdCounterSub.unsubscribe()
        this.cmdCounterSub = null
      })
    } else{
      console.log("Command and arguments should not be empty")
    }
  }

  ngOnDestroy(){
    if(this.cmdCounterSub!=null){
      this.cmdCounterSub.unsubscribe()
    }
  }
  private counter(callback:()=>void): Subscription{
    // Create an Observable that will publish a value on an interval
    const secondsCounter = interval(1000).pipe(take(6));
    // Subscribe to begin publishing values
    return secondsCounter.subscribe(n =>{
        console.log(`It's been ${n} seconds since subscribing!,
         tripstatus = ${this.tripStatus.message}`)
         secondsCounter
         this.tripStatus.value = n * 20
        if(n == 5) {
           console.log(`Trinp started ${n} seconds since subscribing!,
            tripstatus = ${this.tripStatus.message}`)
            callback()
        }
        
      }
    );
  }

}
