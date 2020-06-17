export class AuthService {
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

    login() {
        this.loggedIn = true
    }

    logOut(){
        this.loggedIn = false
    }
}