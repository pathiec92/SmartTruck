export class Load {

    constructor(
        public id:string = "", public started:number ,
        public ended:number, public truckId:string) {

        }
}

export class ActiveLoad {
    constructor(
        public loadId:string = "",
        public truckId:string = "",
        public started:number = 1,
        public truckAck:TruckAck = null){
        }
}

export class TruckAck {
    constructor(
        public loadId:string = "",
        public truckNum:string = "",
        public ownerName:string = ""){

        }
}

export class Truck {
    constructor (
        public truckId:string = "",
        public owner:string="",
        public desc:string = ""
    ){}
}

