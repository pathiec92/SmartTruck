import { Alert } from '../shared/util'
export class LoadEvents{
    constructor(public id:string,
    public type: string,
    public message: string,
    public at:number){}
}