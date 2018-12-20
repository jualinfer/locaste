import { CookieService } from 'ngx-cookie-service';
import { Component } from '@angular/core';
import { NavController } from 'ionic-angular';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  url: string = "..\\..\\assets\\imgs\\Pet.png";
  showLoginPage: boolean = true;

  constructor(
    public navCtrl: NavController,
    private cookieService: CookieService,
  ) {
    this.checkIfLogged();
  }

  private checkIfLogged() {
    if(this.cookieService.get('decide')) {
      this.showLoginPage = false;
    }
  }

  public hiddeLogin($event?: boolean) {
    this.showLoginPage = $event;
  }

}
