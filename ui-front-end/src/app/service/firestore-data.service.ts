import {Injectable} from '@angular/core'

import { AngularFirestore, AngularFirestoreCollection, AngularFirestoreDocument } from 'angularfire2/firestore';
import { Observable } from 'rxjs';
import { LoadEvents } from '../shared/LoadEvents';
import { Load, ActiveLoad, TruckAck, Truck, User } from '../shared/Load';
import { map, take, ignoreElements} from 'rxjs/operators';
import { INFO } from '../shared/util';
import { UUID } from 'angular2-uuid';
import { Command } from '../shared/Command';


@Injectable()
export class FirestoreDataService {
    loadEventCollection: AngularFirestoreCollection<LoadEvents>;
    loadEvents:Observable<LoadEvents[]>;
    loadEventDoc:AngularFirestoreDocument<LoadEvents>;

    loadCollection: AngularFirestoreCollection<Load>;
    loadDoc:AngularFirestoreDocument<Load>;

    activeLoadCollection: AngularFirestoreCollection<ActiveLoad>;
    activeLoads:Observable<ActiveLoad[]>;
    trucks:Observable<Truck[]>;
    users:Observable<User[]>;

    truckCommandSub:Observable<Command[]>;


    


    constructor(public firebase:AngularFirestore){
        // this.loadEventCollection = this.firebase.collection('LoadEvents',x=> x.orderBy('type', 'asc'))
        // this.loadEvents = this.loadEventCollection.snapshotChanges().pipe(
        //     map(actions => actions.map(a => {
        //         const data = a.payload.doc.data() as LoadEvents;
        //         data.id = a.payload.doc.id
        //         return data
        //       }))

        // )
        this.users = this.firebase.collection('Users').snapshotChanges().pipe(
            map(actions => actions.map(a => {
                const data = a.payload.doc.data() as User;
                data.id = a.payload.doc.id
                return data
              }))
        )
        this.trucks = this.firebase.collection('Truck').snapshotChanges().pipe(
            map(actions => actions.map(a => {
                const data = a.payload.doc.data() as Truck;
                data.truckId = a.payload.doc.id
                return data
              }))
        )
        this.activeLoadCollection = this.firebase.collection('ActiveLoad')
        this.activeLoads = this.activeLoadCollection.snapshotChanges().pipe(
            map(actions => actions.map(a => {
                const data = a.payload.doc.data() as ActiveLoad;
                data.loadId = a.payload.doc.id
                return data
              }))

        )
    }

    getActiveLoads(){
        return this.activeLoads
    }

    getTrucks(){
        return this.trucks
    }

    getUsers(){
        return this.users
    }

    subScribeTruckCommand(truckId:string){
        this.truckCommandSub = this.firebase.collection('Truck').doc(truckId).collection('command').snapshotChanges().pipe(
            map(actions => actions.map(a => {
                const data = a.payload.doc.data() as Command;
                data.truckId = a.payload.doc.id
                return data
              }))
        )
        return this.truckCommandSub
    }
    
    getLoadEvents(){
        return this.loadEvents
    }

    deleteActiveLoadsAndAddNew(loadId:string,truckId:string, sl:string){
        console.log(`loadId, truckId, sl = ${loadId}, ${truckId}, ${sl}`)
        this.activeLoadCollection = this.firebase.collection('ActiveLoad')
        var activeLoadSub = this.activeLoadCollection.valueChanges(take(1)).subscribe((al:ActiveLoad[]) => {
            activeLoadSub.unsubscribe()
               console.log(`subscribe for one ${al}`)
               this.deleteAL(al, al.length-1, loadId, truckId, sl)
            //   al.forEach(element => {
            //       console.log(`Deleting active load ${element.loadId}`)
                
            //   });
            });
    }

    subcribeToLoadEvents(loadId:string):Observable<LoadEvents[]>{
        this.loadEvents = this.firebase.doc(`LoadEvents/${loadId}`).collection(loadId, x=> x.orderBy('at', 'asc')).snapshotChanges().pipe(
            map(actions => actions.map(a => {
                const data = a.payload.doc.data() as LoadEvents;
                data.id = a.payload.doc.id
                return data
              }))
        )
        return this.loadEvents
    }

   

    startLoad(load:Load){
        console.log(`loadId, truckId, sl = ${load.id}, ${load.truckId}, ${load.sl}`)
        load.started = Date.now()
        this.loadDoc = this.firebase.doc(`Load/${load.id}`)
        this.loadDoc.set(Object.assign({},load))
        this.deleteActiveLoadsAndAddNew(load.id, load.truckId, load.sl)
    }

    publishLoadEvent(loadId:string, type:string, message:string){
        this.firebase.doc(`LoadEvents/${loadId}`).collection(loadId).doc(UUID.UUID()).set(Object.assign({},new LoadEvents(loadId, type, message, Date.now())))
    }

    stopLoad(loadId:string) {

        console.log(`Deleting the load ${loadId}`)
        this.loadDoc = this.firebase.doc(`Load/${loadId}`)
        this.loadDoc.update({ended:Date.now()})

        this.firebase.doc(`ActiveLoad/${loadId}`).delete()
        this.publishLoadEvent(loadId, INFO, "Load STOP request has been sent")
      }
      
    sendCommand(truckId:string, command: Command){
        console.log("Serving the command "+ command.command+", for truck "+truckId)
        this.firebase.doc(`Truck/${truckId}/command/0`).delete().then( (x)=> {
            console.info("Deleted the previous command")
            this.firebase.doc(`Truck/${truckId}/command/0`).set(Object.assign({},command)  )
        })
    }
      

      deleteAL(al:ActiveLoad[], n:number, loadId:string, truckId:string , sl:string){
        // if(n<=0) {
            this.firebase.doc(`ActiveLoad/${loadId}`).set(Object.assign({},new ActiveLoad(loadId,truckId, sl,Date.now())))
            this.publishLoadEvent(loadId, INFO, "Load start request has been sent")
        //     return
        // }
    //     this.firebase.doc(`ActiveLoad/${al[n].loadId}`).delete().then((res)=>{
    //         console.log(res)
    //         console.log(`Deleted active load ${al[n]}`)
    //         this.deleteAL(al, n-1,loadId)
    //     },(err)=>{
    //         console.log(err)
    //         console.log(`error while deleting active load ${al[n]}`)
    //         this.deleteAL(al, n-1,loadId)
    //     })
       }
}