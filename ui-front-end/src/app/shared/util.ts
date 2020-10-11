
export interface Alert {
    type: string;
    message: string;
  }
  
  export const INFO = 'info'
  export const SUCCESS = 'success'
  export  const WARN = 'warning'
  export const DANG = 'danger'
  
  export  const INIT : ConnectProgress = {
      type: INFO,
      message: 'No Load in progress',
      value:0
    }
  
    export  const CONNECTING : ConnectProgress = {
      type: WARN,
      message: 'Connecting to truck...',
      value:10
    }
  
    export const CONNECTED : ConnectProgress = {
      type: SUCCESS,
      message: 'Connection Successful',
      value:100
    }
  
    export  const LOAD_STARTED : ConnectProgress = {
      type: SUCCESS,
      message: 'Load Started',
      value:100
    }
  
    export  const LOAD_ENDED : ConnectProgress = {
      type: SUCCESS,
      message: 'Load ENDED',
      value:100
    }
  
    export const CONNECTING_FAILED : ConnectProgress = {
      type: DANG,
      message: 'Opps!, Connection failed',
      value:100
    }

    export  const WAITING : ConnectProgress = {
      type: WARN,
      message: 'Connected! Waiting for truck response...',
      value:10
    }

    export  const CMD_SENDING : ConnectProgress = {
      type: WARN,
      message: 'Sending the Command',
      value:100
    }
  
    export  const CMD_SENT_SUCCESS : ConnectProgress = {
      type: SUCCESS,
      message: 'Command executed successfully',
      value:100
    }

    export  const CMD_SENT_FAIL : ConnectProgress = {
      type: DANG,
      message: 'Command sent failed',
      value:100
    }


  
  
    export const ALERTS :Alert[] = [{
      type: 'success',
      message: 'This is an success alert',
    }, {
      type: 'info',
      message: 'This is an info alert',
    }, {
      type: 'warning',
      message: 'This is a warning alert',
    }, {
      type: 'danger',
      message: 'This is a danger alert',
    }, {
      type: 'primary',
      message: 'This is a primary alert',
    }, {
      type: 'secondary',
      message: 'This is a secondary alert',
    }, {
      type: 'light',
      message: 'This is a light alert',
    }, {
      type: 'dark',
      message: 'This is a dark alert',
    }]
  
  
  
  export interface ConnectProgress extends Alert {  
    value:number
  }