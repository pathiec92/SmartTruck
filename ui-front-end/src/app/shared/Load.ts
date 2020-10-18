export class Load {

    constructor(
        public id:string = "", public started:number ,
        public ended:number, public truckId:string, public sl:string) {

        }
}

export class LoadUi {

    constructor(
        public id:string = "", public started:string ,
        public ended:string, public truckId:string, public sl:string) {

        }
}

export class ActiveLoad {
    constructor(
        public loadId:string = "",
        public truckId:string = "",
        public sl:string = "",
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
        public desc:string = "",
        public sl:string = ""
    ){}
}

export class User {
    constructor (
        public id:string = "",
        public userId:string = "",
        public password:string=""
    ){}
}

export class Device {
    constructor (
        public id:string = "",
        public sl:string = "",
        public at:number=0
    ){}
}





