import { DataManagement } from './../../app/services/dataManagemen';
import { Component } from '@angular/core';
import { NavController, NavParams, LoadingController, Loading } from 'ionic-angular';
import { Voting } from '../../app/app.data.models';
import { VotingPage } from '../votingClass/voting';
import { CookieService } from 'ngx-cookie-service';

@Component({
    selector: 'page-list',
    templateUrl: 'list.html'
})
export class ListPage {

    url: string = "..\\..\\assets\\imgs\\Pet.png";
    availableVotigns: Voting[] = [];
    loading: Loading;

    constructor(
        public navCtrl: NavController,
        public navParams: NavParams,
        public dm: DataManagement,
        public cookieService: CookieService,
        public loadingCtrl: LoadingController
    ) {
        this.loading = this.loadingCtrl.create({
            content: 'Loading your votings, please wait...',
        });
        this.getAvailableVotings();
    }

    getAvailableVotings() {
        this.loading.present();
        this.dm.getPollsIdUserLogged().then((data) => {
            console.log(data);
            data.voting.forEach(x => {
                console.log(x);
                this.dm.getPollWithId(x).then((response) => {
                    console.log(response[0]);
                    this.availableVotigns.push(response[0]);
                }).catch((error) => {
                    console.log("Error " + error);
                });
            });
            console.log(this.availableVotigns);
            this.loading.dismiss();
        }).catch((error) => {
            console.log(error);
            this.loading.dismiss();
        });
    }

    itemTapped(event, item) {
        console.log(item);
        this.navCtrl.push(VotingPage, {
            voting: item,
        });
    }

}
