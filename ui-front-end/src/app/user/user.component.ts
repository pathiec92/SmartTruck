import { Component, OnInit } from '@angular/core';
import { AuthService } from './auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {
  title="Smart Truck"
  userName = "User Name "
  password = "Password"
  constructor(public authService:AuthService, private router:Router) { }

  ngOnInit(): void {
  }
  login(){
    console.log("login")
    this.router.navigate(['/home'])
    this.authService.login()

  }

  isLoggedIn():boolean{
    return this.authService.loggedIn
  }

  logout(){
    console.log("login")
    this.authService.logOut()
  }

}
