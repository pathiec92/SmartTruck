import { Component, OnInit, OnDestroy } from '@angular/core';
import { FirestoreDataService } from '../service/firestore-data.service';
import { Subscription } from 'rxjs';
import { Truck } from '../shared/Load';

interface Load {
  id:number;
  type: string;
  cloneType: string;
  truck: string;
}

// const LOADS:Load[] = [{
//   id:1,
//   truck:'KA03 HM43',
//   cloneType: 'success',
//   type: 'success'
// },
// {
//   id:2,
//   truck:'KA03 HM4343',
//   cloneType: 'info',
//   type: 'info'
// },
// {
//   id:3,
//   truck:'KA03 HM43',
//   cloneType: 'warning',
//   type: 'warning'
// },
// {
//   id:4,
//   truck:'KA03 HM43',
//   cloneType: 'danger',
//   type: 'danger'
// },
// ]


@Component({
  selector: 'app-loads',
  templateUrl: './loads.component.html',
  styleUrls: ['./loads.component.css']
})
export class LoadsComponent implements OnInit, OnDestroy {

  trucks:Truck[] = []
  truckArray: Truck[][] = [[]]
  activeLoadSub: Subscription = null
  numbers = [1,2,3]
  divSet = 6

  constructor(private _data: FirestoreDataService) { 
    
  }

  ngOnInit(): void {
    this.subscribeTrucks()
  }

  ngOnDestroy(){
    if(this.activeLoadSub!=null){
      this.activeLoadSub.unsubscribe()
    }
  }
  private arrayToMatrix = (array:Truck[], columns:number) => Array(Math.ceil(array.length / columns)).fill('').reduce((acc, cur, index) => {
    return [...acc, [...array].splice(index * columns, columns)]
  }, [])
  private subscribeTrucks(){
    if(this.activeLoadSub!=null){
      this.activeLoadSub.unsubscribe()
    }
    this.activeLoadSub = this._data.getTrucks().subscribe(
      (trucks:Truck[]) => {
       
        console.log(`active trucks length = ${trucks.length}`)
        this.trucks = trucks.filter((t,i, a)=> {
          return t.sl !== null &&  t.sl !== undefined && t.sl.length>0
        })
        var numSets = ((this.trucks.length - (this.trucks.length % this.divSet) )/ this.divSet ) +1
        console.log(`Number of sets = ${numSets}`)
        this.truckArray = this.arrayToMatrix(this.trucks, this.divSet)
      }
    )
  }

  onLoad(load:Load){
    // this.reset()
    // this.loads.forEach(l => {
    //   if(load.id != l.id) l.type = 'dark'
    // });
  }
  // reset(){
  //   console.log("reset")
  //   this.loads.forEach(element => {
  //     element.type = element.cloneType
  //   });
  // }

}
