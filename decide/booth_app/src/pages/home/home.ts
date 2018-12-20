import { CookieService } from 'ngx-cookie-service';
import { Component } from '@angular/core';
import { NavController, LoadingController, Loading } from 'ionic-angular';
import { DataManagement } from '../../app/services/dataManagemen';

@Component({
  selector: 'page-home',
  templateUrl: 'home.html'
})
export class HomePage {

  url: string = "..\\..\\assets\\imgs\\Pet.png";
  showLoginPage: boolean = true;
  loading: Loading;

  constructor(
    public navCtrl: NavController,
    private dm: DataManagement,
    private cookieService: CookieService,
    private loadingCtrl: LoadingController
  ) {
    this.loading = this.loadingCtrl.create({
      content: 'Signing out, please wait...',
    });
    this.checkIfLogged();
  }

  private checkIfLogged() {
    if (this.cookieService.get('decide')) {
      this.showLoginPage = false;
    }
  }

  public hiddeLogin($event?: boolean) {
    this.showLoginPage = $event;
  }

  public logout() {
    this.loading.present()
    this.dm.logout().then((data) => {
      this.cookieService.delete('decide');
      this.loading.dismiss();
      location.reload();

      console.log("You've been logged out")
    });
  }

}
