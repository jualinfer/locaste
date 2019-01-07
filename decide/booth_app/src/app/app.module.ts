import { Voting } from './app.data.models';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { DataManagement } from './services/dataManagemen';
import { LoginPage } from './../pages/login/login';
import { ConfigService } from './../config/configService';
import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';
import { IonicApp, IonicErrorHandler, IonicModule } from 'ionic-angular';
import { CookieService } from 'ngx-cookie-service';

import { MyApp } from './app.component';
import { HomePage } from '../pages/home/home';
import { ListPage } from '../pages/list/list';
import { PullListPage } from '../pages/pullList/pullList';
import { VotingPage } from '../pages/votingClass/voting';

import { StatusBar } from '@ionic-native/status-bar';
import { SplashScreen } from '@ionic-native/splash-screen';
import { RestService } from './services/restService';


@NgModule({
  declarations: [
    MyApp,
    HomePage,
    ListPage,
    LoginPage,
    PullListPage,
    VotingPage,
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    IonicModule.forRoot(MyApp),
  ],
  bootstrap: [IonicApp],
  entryComponents: [
    MyApp,
    HomePage,
    ListPage,
    LoginPage,
    PullListPage,
    VotingPage,
  ],
  providers: [
    LoginPage,
    HttpClient,
    RestService,
    DataManagement,
    ConfigService,
    StatusBar,
    SplashScreen,
    CookieService,
    Voting,
    { provide: ErrorHandler, useClass: IonicErrorHandler }
  ]
})
export class AppModule { }
