import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router, CanActivateChild } from "@angular/router";
import { AuthService } from "./auth.service";
import { Injectable } from "@angular/core";


@Injectable()
export class AuthGaurd implements CanActivate, CanActivateChild {
    
    constructor(private authService:AuthService,
        private router:Router){}

    canActivate(route:ActivatedRouteSnapshot,
        state:RouterStateSnapshot):Promise<boolean> {
            return this.authService.isAuthenticated().then(
                (authenticated:boolean) => {
                    if(authenticated) {
                        return true
                    } else {
                        this.router.navigate(['/user'])
                    }
                }
            )
        }
    canActivateChild(route:ActivatedRouteSnapshot,
        state:RouterStateSnapshot):Promise<boolean> {
            return this.canActivate(route,state)
        }

}