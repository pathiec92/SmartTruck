import {Injectable} from '@angular/core'

import { AngularFirestore, AngularFirestoreCollection, AngularFirestoreDocument } from 'angularfire2/firestore';
import { Observable } from 'rxjs';
import { LoadEvents } from '../shared/LoadEvents';
import { Load, ActiveLoad, TruckAck } from '../shared/Load';
import { map, take, ignoreElements} from 'rxjs/operators';
import { INFO } from '../shared/util';
import { UUID } from 'angular2-uuid';

@Injectable()
export class FirestoreDataService {
    loadEventCollection: AngularFirestoreCollection<LoadEvents>;
    loadEvents:Observable<LoadEvents[]>;
    loadEventDoc:AngularFirestoreDocument<LoadEvents>;

    loadCollection: AngularFirestoreCollection<Load>;
    loadDoc:AngularFirestoreDocument<Load>;

    activeLoadCollection: AngularFirestoreCollection<ActiveLoad>;
    activeLoads:Observable<ActiveLoad[]>;


    constructor(public firebase:AngularFirestore){
        // this.loadEventCollection = this.firebase.collection('LoadEvents',x=> x.orderBy('type', 'asc'))
        // this.loadEvents = this.loadEventCollection.snapshotChanges().pipe(
        //     map(actions => actions.map(a => {
        //         const data = a.payload.doc.data() as LoadEvents;
        //         data.id = a.payload.doc.id
        //         return data
        //       }))

        // )


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
    
    getLoadEvents(){
        return this.loadEvents
    }

    deleteActiveLoadsAndAddNew(loadId:string){
        this.activeLoadCollection = this.firebase.collection('ActiveLoad')
        var activeLoadSub = this.activeLoadCollection.valueChanges(take(1)).subscribe((al:ActiveLoad[]) => {
            activeLoadSub.unsubscribe()
               console.log(`subscribe for one ${al}`)
               this.deleteAL(al, al.length-1, loadId)
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
        load.started = Date.now()
        this.loadDoc = this.firebase.doc(`Load/${load.id}`)
        this.loadDoc.set(Object.assign({},load))
        this.deleteActiveLoadsAndAddNew(load.id)
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

      

      deleteAL(al:ActiveLoad[], n:number, loadId:string){
        if(n<0) {
            this.firebase.doc(`ActiveLoad/${loadId}`).set(Object.assign({},new ActiveLoad(loadId, Date.now())))
            this.publishLoadEvent(loadId, INFO, "Load start request has been sent")
            return
        }
        this.firebase.doc(`ActiveLoad/${al[n].loadId}`).delete().then((res)=>{
            console.log(res)
            console.log(`Deleted active load ${al[n]}`)
            this.deleteAL(al, n-1,loadId)
        },(err)=>{
            console.log(err)
            console.log(`error while deleting active load ${al[n]}`)
            this.deleteAL(al, n-1,loadId)
        })
      }
}