export class Command {

    constructor(public truckId:string ,
        public command:string , public args:string, public ack:string='') {

        }
}