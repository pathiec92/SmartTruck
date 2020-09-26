import { Alert } from '../shared/util'
import { getLocaleDateFormat } from '@angular/common'
export class LoadEvents{
    constructor(public id:string,
    public type: string,
    public message: string,
    public at:number){}
    
    public getColor(){
        // switch(this.type){
        //     case 'info':
        //         return "gray"
        //     case 'danger':
        //         return "red"
        // }
        return "blue"
    }
}