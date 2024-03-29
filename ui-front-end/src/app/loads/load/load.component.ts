import { Component, OnInit, NgZone, OnDestroy } from '@angular/core';
import { interval, Subscription } from 'rxjs';
import { take } from 'rxjs/operators';
import { ConnectProgress, Alert, INIT, CONNECTING, 
  LOAD_ENDED,LOAD_STARTED,
  CONNECTING_FAILED, CONNECTED,ALERTS, INFO, WAITING, CMD_SENDING, CMD_SENT_FAIL, CMD_SENT_SUCCESS} from '../../shared/util'

import { FirestoreDataService } from '../../service/firestore-data.service';
import { LoadEvents } from '../../shared/LoadEvents';
import { Load, ActiveLoad, TruckAck, Device} from '../../shared/Load';
import { UUID } from 'angular2-uuid';
import { ActivatedRoute, Params } from '@angular/router';
import { Command } from 'src/app/shared/Command';



@Component({
  selector: 'app-load',
  templateUrl: './load.component.html',
  styleUrls: ['./load.component.css']
})

export class LoadComponent implements OnInit, OnDestroy{
  isLoading = false
  isStarted = false

  enableStart = false
  enableStop = false
  model = 2
  tripStatus : ConnectProgress = INIT
  tripEvents :LoadEvents[] = []
  activeLoad = new ActiveLoad()
  load:Load = new Load(UUID.UUID(), null,null,  "","")
  loadEventSub: Subscription = null
  startCounterSub: Subscription = null
  stopCounterSub: Subscription = null
  activeLoadSub: Subscription = null
  truckId:string=""
  sl:string = ""
  past:string="past"
  cmd:string="command"
  lastReportedAt:string=""
  lastReportedAt1:string=""


  constructor(private zone:NgZone, private _data: FirestoreDataService,
    private route:ActivatedRoute) {
    this.model = 2;
  }

  ngOnInit() {
    this.truckId = this.route.snapshot.params['truckId']
    this.sl = this.route.snapshot.params['sl']
    this.route.params.subscribe(
      (param:Params) => {
        this.truckId = param['truckId']
        this.sl = param['sl']
        console.log(`new truckId selected ${this.truckId}, ${this.sl}`)
        this.subscribeToActiveLoad()
      }
    )
    this._data.lastReportedAt(this.sl).subscribe(
      (al:Device) => {
        //console.log(`Devices length = ${al.length}`)
        if(al != undefined) 
        this.lastReportedAt = this.convertTime(al.at)
        this.lastReportedAt1 = al.dt
        //al.forEach(x=> this.lastReportedAt = this.convertTime(x.at))
        
        // if(this.pastLoadSub!=null){
        //   this.pastLoadSub.unsubscribe()
        // }
      }
    )
  }

  private convertTime(epoch:number){
    var nd = new Date(0)
    nd.setUTCMilliseconds(epoch)
    return nd.toLocaleString();
  }
  
  

  private subscribeToActiveLoad(){
    this.tripEvents=[]
    if(this.activeLoadSub!=null){
      this.activeLoadSub.unsubscribe()
    }
    if(this.loadEventSub!=null){
      this.loadEventSub.unsubscribe()
    }
    this.activeLoadSub = this._data.getActiveLoads().subscribe(
      (al:ActiveLoad[]) => {
        console.log(`active loads ${al}, length = ${al.length}`)
        var isActiveLoadAvail = false
        for(let aload of al){
          console.log(`active truckId ${aload.truckId}, selected truckId ${this.truckId}`)
          if(aload.truckId === this.truckId){
            isActiveLoadAvail = true
            this.activeLoad = aload
            console.log("Active Load = "+this.activeLoad)
  
            //this.isStarted = this.activeLoad.loadId != null && this.activeLoad.loadId != ""
            //check if we got ack from truck
            this.isStarted = this.activeLoad!= null && this.activeLoad.truckAck != null
            //waiting for truck ack
            this.isLoading = this.activeLoad!= null && this.activeLoad.truckAck == null
            if(this.isLoading) {
              this.startCounterSub =  this.counter(()=>{if(this.isLoading)this.tripStatus = CONNECTING_FAILED})
            }
            this.updateButtonStatus()  
            this.updateProgress()
            //this._data.publishLoadEvent(this.activeLoad.loadId, INFO,"Load Started Request Accepted")
            if(this.loadEventSub!=null){
              this.loadEventSub.unsubscribe()
            }
            this.loadEventSub = this._data.subcribeToLoadEvents(this.activeLoad.loadId).subscribe(
              (loadEvents:LoadEvents[]) => {
                this.tripEvents = loadEvents.reverse()
                console.log(this.tripEvents)
              }
            )
          }
        }
        if(!isActiveLoadAvail) {
          //thre are no curret active loads
          console.log('thre are no curret active loads')
          this.noCurrentActiveLoads();
        }
      }
    )

  }

  private noCurrentActiveLoads() {
    this.isStarted = false;
    this.isLoading = false;
    this.updateButtonStatus();
    this.updateProgress();
  }

  startTrip(){
   this.tripStatus = CONNECTING
   this.isLoading = true
   this.updateButtonStatus()
   this.load = new Load(UUID.UUID(),  null,null, this.truckId, this.sl)
   this._data.startLoad(this.load)
   this.startCounterSub =  this.counter(()=>{
      // this.isStarted = true
      // this.isLoading = false
      if(this.isLoading) this.tripStatus = CONNECTING_FAILED
      // this.updateButtonStatus()
    })
  }
  public getColor(load:LoadEvents){
    switch(load.type){
      case 'info':
        return "gray"
      case 'danger':
        return "red"
      case 'warning':
        return 'orange'
    }
    return "blue"
  }

  deleteAllActiveLoads(){

  }

  private updateButtonStatus(){
    this.updateStop()
    this.updateStart()

  }

  stopTrip(){
    this.tripEvents=[]
    this.tripStatus = CONNECTING
    this.isLoading = true
    this.updateButtonStatus()
    this._data.stopLoad(this.activeLoad.loadId)
    this.stopCounterSub = this.counter(()=>{
      this.tripStatus = CONNECTING_FAILED
      // this.isStarted = false
      // this.isLoading = false
      // this.tripStatus = LOAD_ENDED
      // this.updateButtonStatus()
    })
  }

  updateProgress() {
    console.log("updateProgress")
    if(this.isLoading){
      this.tripStatus = WAITING
    }
    if(this.enableStop){
      this.tripStatus = LOAD_STARTED
      if(this.startCounterSub != null){
        console.log("unsub startCounterSub")
        this.startCounterSub.unsubscribe()
        this.startCounterSub = null
      }
    }
    if(this.enableStart){
      this.tripStatus = LOAD_ENDED
      if(this.stopCounterSub != null){
        console.log("unsub stopCounterSub")
        this.stopCounterSub.unsubscribe()
        this.stopCounterSub = null
      }
    }
  }

  updateStart() {
    this.enableStart = !(this.isLoading || this.isStarted)
    console.log(`enableStart = ${this.enableStart}`)
  }


  updateStop() {
    this.enableStop= !this.isLoading && this.isStarted
    console.log(`enableStop = ${this.enableStop}`)
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

  ngOnDestroy(){
    
    if(this.loadEventSub!=null){
      this.loadEventSub.unsubscribe()
    }
    if(this.startCounterSub!=null){
      this.startCounterSub.unsubscribe()
    }
    
    if(this.stopCounterSub!=null){
      this.stopCounterSub.unsubscribe()
    }
    if(this.activeLoadSub!=null){
      this.activeLoadSub.unsubscribe()
    }
    if(this.activeLoadSub!=null){
      this.activeLoadSub.unsubscribe()
    }
    }
}

