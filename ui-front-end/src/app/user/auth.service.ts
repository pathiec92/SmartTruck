import { FirestoreDataService } from '../service/firestore-data.service';
import { Injectable } from "@angular/core";
import { User } from '../shared/Load';
import { Subscription } from 'rxjs';

@Injectable()
export class AuthService {
    users:User[] = []
    activeUserSub: Subscription = null
    constructor(private _data: FirestoreDataService) { 
        this.subscribeTrucks()
    }
    //todo: need to turn false after testing
    loggedIn = false;
    
    isAuthenticated() {
        const promise = new Promise(
            (resolve, reject)=> {
                setTimeout( () => {
                    resolve(this.loggedIn)
                },20)
            }
        )
        return promise
    }

    login(userId:string, pass:string) {
        console.log(`user ${userId}, pass ${pass}`)
        if(this.users !== null && this.users !== undefined){
            //this.users.map((v,i,a)=>console.log(`1 user ${v.userId}, pass ${v.password}`))
            var loggedInUser = this.users.filter((v,i,a) =>{ 
                //console.log(`2 user: ${v.userId}, pass: ${v.password} user: ${userId}, pass: ${pass}, res ${v.id.trim() === userId.trim() && v.password === pass}, res id ${v.id === userId},  res pass ${v.password === pass}`)
                return v.userId.trim() === userId.trim() && v.password.trim() === pass.trim()
            }) 
            // console.log(`loggedInUser ${loggedInUser}`)
            this.loggedIn = loggedInUser !==null && loggedInUser !== undefined && loggedInUser.length>0
        } else{
            this.loggedIn = false
        }
        console.log(`loggedIn ${this.loggedIn}`)
        
    }

    logOut(){
        this.loggedIn = false
    }
    private subscribeTrucks(){
        if(this.activeUserSub!=null){
          this.activeUserSub.unsubscribe()
        }
        this.activeUserSub = this._data.getUsers().subscribe(
          (users:User[]) => {
            console.log(`active users ${users}, length = ${users.length}`)
            this.users = users
          }
        )
      }
}