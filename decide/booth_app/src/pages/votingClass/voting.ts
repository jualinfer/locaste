import { CookieService } from 'ngx-cookie-service';
import { Component } from '@angular/core';
import { NavController, LoadingController, Loading } from 'ionic-angular';
import { DataManagement } from '../../app/services/dataManagemen';
import { Voting } from '../../app/app.data.models';

@Component({
  selector: 'page-voting',
  templateUrl: 'voting.html'
})
export class VotingPage {

  showLoginPage: boolean = true;
  loading: Loading;
  voting: Voting = new Voting;

  constructor(
    public navCtrl: NavController,
    private dm: DataManagement,
    private cookieService: CookieService,
    private loadingCtrl: LoadingController,
    voting: Voting,
  ) {
    this.loading = this.loadingCtrl.create({
      content: 'Signing out, please wait...',
    });
    this.voting = voting;
    this.checkIfLogged();
  }

  private checkIfLogged() {
    if (this.cookieService.get('decide')) {
      this.showLoginPage = false;
    }
  }

}
