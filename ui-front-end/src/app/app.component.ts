import { Component, OnInit, NgZone } from '@angular/core';
import { interval, Subscription } from 'rxjs';
import { take } from 'rxjs/operators';
import { ConnectProgress, Alert, INIT, CONNECTING, 
  LOAD_ENDED,LOAD_STARTED,
  CONNECTING_FAILED, CONNECTED,ALERTS, INFO, WAITING} from './shared/util'
``
import { FirestoreDataService } from './service/firestore-data.service';
import { LoadEvents } from './shared/LoadEvents';
import { Load, ActiveLoad, TruckAck} from './shared/Load';
import { UUID } from 'angular2-uuid';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styles: [`
    ngb-progressbar {
      margin-top: 5rem;
    }
  `]
})

export class AppComponent implements OnInit{
  isLoading = false
  isStarted = false

  enableStart = false
  enableStop = false
  model = 2
  tripStatus : ConnectProgress = INIT
  tripEvents :LoadEvents[] = []
  activeLoad = new ActiveLoad()
  load:Load = new Load(UUID.UUID(), null,null,  "")
  loadEventSub: Subscription = null
  startCounterSub: Subscription = null
  stopCounterSub: Subscription = null


  constructor(private zone:NgZone, private _data: FirestoreDataService) {
    this.model = 2;
  }
  startTrip(){
   this.tripStatus = CONNECTING
   this.isLoading = true
   this.updateButtonStatus()
   this.load = new Load(UUID.UUID(),  null,null,  "")
   this._data.startLoad(this.load)
   this.startCounterSub =  this.counter(()=>{
      // this.isStarted = true
      // this.isLoading = false
      this.tripStatus = CONNECTING_FAILED
      // this.updateButtonStatus()
    })
  }

  deleteAllActiveLoads(){

  }

  private updateButtonStatus(){
    this.updateStop()
    this.updateStart()

  }

  stopTrip(){
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

  ngOnInit() {
    // this._data.getLoadEvents().subscribe(
    //   (loadEvents:LoadEvents[]) => {
    //     this.tripEvents = loadEvents
    //     console.log(this.tripEvents)
    //   }
    // )

    this._data.getActiveLoads().subscribe(
      (al:ActiveLoad[]) => {
        console.log(`active loads ${al}, length = ${al.length}`)
        if(al.length>0) {
          this.activeLoad = al[0]
          console.log("Active Load = "+this.activeLoad)

          //this.isStarted = this.activeLoad.loadId != null && this.activeLoad.loadId != ""
          //check if we got ack from truck
          this.isStarted = this.activeLoad!= null && this.activeLoad.truckAck != null
          //waiting for truck ack
          this.isLoading = this.activeLoad!= null && this.activeLoad.truckAck == null
          this.updateButtonStatus()  
          this.updateProgress()
          //this._data.publishLoadEvent(this.activeLoad.loadId, INFO,"Load Started Request Accepted")
          if(this.loadEventSub!=null){
            this.loadEventSub.unsubscribe()
          }
          this.loadEventSub = this._data.subcribeToLoadEvents(this.activeLoad.loadId).subscribe(
            (loadEvents:LoadEvents[]) => {
              this.tripEvents = loadEvents
              console.log(this.tripEvents)
            }
          )
        } else {
          //thre are no curret active loads
          this.isStarted = false
          this.isLoading = false
          this.updateButtonStatus()
          this.updateProgress()
        }
      }
    )
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
}


