import { Component, NgZone, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute, Params } from '@angular/router';
import { Subscription } from 'rxjs';
import { FirestoreDataService } from '../service/firestore-data.service';
import { Device, Load, LoadUi } from '../shared/Load';
import { LoadEvents } from '../shared/LoadEvents';

@Component({
  selector: 'app-past-load',
  templateUrl: './past-load.component.html',
  styleUrls: ['./past-load.component.css']
})
export class PastLoadComponent implements OnInit, OnDestroy {
  private setting = {
    element: {
      dynamicDownload: null as HTMLElement
    }
  }
  truckId:string=""
  sl:string = ""
  tripLogs = "This is trip logs"
  url= null
  pastLoadSub: Subscription = null
  reportLoadSub: Subscription = null

  pastLoads:LoadUi[] = []
  constructor(private zone:NgZone, private _data: FirestoreDataService,
    private route:ActivatedRoute) {
      
  }

  ngOnInit() {
    this.truckId = this.route.snapshot.params['truckId']
    this.sl = this.route.snapshot.params['sl']
    this.route.params.subscribe(
      (param:Params) => {
        this.truckId = param['truckId']
        this.sl = param['sl']
        console.log(`new truckId selected ${this.truckId}, ${this.sl}`)
      }
    )
    this.subscribeToPastLoad(this.truckId)
    
     
  }

  openReport(loadId:string, startTime:string) {
    this.reportLoadSub = this._data.subcribeToLoadEvents(loadId).subscribe(
      (al:LoadEvents[]) => {
        console.log(`report loads length = ${al.length}`)
        this.dyanmicDownloadByHtmlTag({
          fileName: startTime,
          text: al.map(x=>`${this.convertTime(x.at)}: [${x.type}]-${x.message}`).join("\n")
        })
         if(this.reportLoadSub!=null){
          this.reportLoadSub.unsubscribe()
        }
      }
    )
  }

  private dyanmicDownloadByHtmlTag(arg: {
    fileName: string,
    text: string
  }) {
    if (!this.setting.element.dynamicDownload) {
      this.setting.element.dynamicDownload = document.createElement('a');
    }
    const element = this.setting.element.dynamicDownload;
    const fileType = arg.fileName.indexOf('.json') > -1 ? 'text/json' : 'text/plain';
    element.setAttribute('href', `data:${fileType};charset=utf-8,${encodeURIComponent(arg.text)}`);
    element.setAttribute('download', arg.fileName);

    var event = new MouseEvent("click");
    element.dispatchEvent(event);
  }

  private convertTime(epoch:number){
    // var offset:number = 5.3
    // var d = new Date(epoch);
    // var utc = d.getTime() + (d.getTimezoneOffset() * 60000);  //This converts to UTC 00:00
    // var nd = new Date(utc + (3600000*offset));
    var nd = new Date(0)
    nd.setUTCMilliseconds(epoch)
    return nd.toLocaleString();
  }
  private subscribeToPastLoad(truckId:string){
    console.log("subscribing for past loads")
    this.pastLoads=[]
    this.pastLoadSub = this._data.getPastLoads().subscribe(
      (al:Load[]) => {
        console.log(`past loads length = ${al.length}, truckId = ${truckId}`)
        
        this.pastLoads = al.filter(x=> {
          console.log(`serv tid = ${x.truckId}`)
          return x.truckId == truckId}).sort((a,b)=> a.started - b.started).map(l=> {
          return new LoadUi(l.id, this.convertTime(l.started),this.convertTime(l.ended),l.truckId, l.sl)
        })
        console.log(`after past loads length = ${this.pastLoads.length}`)
        // if(this.pastLoadSub!=null){
        //   this.pastLoadSub.unsubscribe()
        // }
      }
    )
  }
  ngOnDestroy(){
    if(this.pastLoadSub!=null){
      this.pastLoadSub.unsubscribe()
    }
  }

}
