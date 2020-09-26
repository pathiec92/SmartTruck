import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { NgbModule } from '@ng-bootstrap/ng-bootstrap';
import { environment } from '../environments/environment';
import { AngularFireModule } from 'angularfire2';
import { AngularFirestoreModule } from 'angularfire2/firestore';
import { FirestoreDataService } from './service/firestore-data.service';
import { HomeComponent } from './home/home.component';
import { UserComponent } from './user/user.component';
import { AuthGaurd } from './user/auth.gaurd.service';
import { AuthService } from './user/auth.service';
import { AppRoutingModule } from './app.routing.module';
import { TruckComponent } from './trucks/truck/truck.component';
import { LoadComponent } from './loads/load/load.component';
import { TrucksComponent } from './trucks/trucks.component';
import { LoadsComponent } from './loads/loads.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    UserComponent,
    TruckComponent,
    LoadComponent,
    TrucksComponent,
    LoadsComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    ReactiveFormsModule,
    NgbModule,
    AngularFireModule.initializeApp(environment.firebase),
    AngularFirestoreModule,
    FormsModule,
    AppRoutingModule
  ],
  providers: [FirestoreDataService, AuthGaurd,AuthService],
  bootstrap: [AppComponent]
})
export class AppModule { }
