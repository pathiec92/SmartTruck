import { Routes, RouterModule } from "@angular/router";
import { HomeComponent } from './home/home.component';
import { AuthGaurd } from './user/auth.gaurd.service';
import { AppComponent } from './app.component';
import { UserComponent } from './user/user.component';
import { NgModule } from '@angular/core';
import { LoadsComponent } from './loads/loads.component';
import { TrucksComponent } from './trucks/trucks.component';
import { LoadComponent } from './loads/load/load.component';
import { PastLoadComponent } from './past-load/past-load.component';
import { DispPastloadComponent } from './disp-pastload/disp-pastload.component';
import { CommandComponent } from './command/command.component';

// canActivate:[AuthGaurd]
const appRoutes: Routes = [
    {path:'', redirectTo:'/load', pathMatch:'full'},
    {path:'home', component:HomeComponent},
    {
        path:'load', component:LoadsComponent, canActivate:[AuthGaurd],
        children: [
            {
                path:':truckId/:sl', component:LoadComponent,
                // children: [ {
                //     path:':sl', component:LoadComponent
                // }
                // ]
            },
            {path: ':truckId/:sl/:past', component:PastLoadComponent},
            {path: ':truckId/:sl/:past/:command', component:CommandComponent},
            {path: ':truckId/:sl/:past/:loadId', component:DispPastloadComponent}

        ]
    },
    {path:'truck', component:TrucksComponent, canActivate:[AuthGaurd]},
    {path:'user', component:UserComponent},
]

@NgModule({
    imports:[
        RouterModule.forRoot(appRoutes)
    ],
    exports:[RouterModule]
})
export class AppRoutingModule{

}