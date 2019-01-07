import { Component } from '@angular/core';
import { NavController, LoadingController, Loading, NavParams } from 'ionic-angular';
import { Voting } from '../../app/app.data.models';

@Component({
  selector: 'page-voting',
  templateUrl: 'voting.html'
})
export class VotingPage {

  loading: Loading;
  voting: Voting;

  constructor(
    public navCtrl: NavController,
    public NavParams: NavParams,
    private loadingCtrl: LoadingController,
  ) {
    this.loading = this.loadingCtrl.create({
      content: 'Signing out, please wait...',
    });
    this.voting = this.NavParams.get('voting');
  }
}