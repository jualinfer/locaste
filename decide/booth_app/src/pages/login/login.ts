import { NavController, NavParams } from 'ionic-angular';
import { Component } from '@angular/core';
import { DataManagement } from '../../app/services/dataManagemen'
import { HomePage } from '../home/home';
import { PullListPage } from '../pullList/pullList';

@Component({
    selector: 'page-login',
    templateUrl: 'login.html'
})

export class LoginPage {

    username: string;
    password: string;
    error: string;

    constructor(
        public navCtrl: NavController,
        public navParams: NavParams,
        public dm: DataManagement
    ) {

    }

    private changeStatus(status: string) {
        switch (status) {
            case 'login':
                this.status = 'login';
                break;
            case 'signUp':
                this.status = 'signUp';
                break;
        }
    }

    public login() {
        this.dm.login(this.username, this.password).then((data) => {
            this.navCtrl.push(PullListPage).then((data) => {
                console.log(data);
            }).catch((error) => {
                console.log(error);
            })
        }).catch((error) => {
            this.error = error;
        });
    }


}