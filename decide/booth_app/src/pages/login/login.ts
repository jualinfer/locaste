import { NavController, NavParams } from 'ionic-angular';
import { Component } from '@angular/core';
import { DataManagement } from '../../app/services/dataManagemen'
import { PullListPage } from '../pullList/pullList';

@Component({
    selector: 'page-login',
    templateUrl: 'login.html'
})

export class LoginPage {

    username: string;
    password: string;
    password2: string;

    status: string = 'login';

    error: string;

    constructor(
        public navCtrl: NavController,
        public navParams: NavParams,
        public dm: DataManagement
    ) {

    }

    public changeStatus(status: string) {
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
            this.navCtrl.setRoot(PullListPage).then((data) => {
                console.log(data);
            }).catch((error) => {
                console.log(error);
            })
        }).catch((error) => {
            this.error = error;
        });
    }

    public signUp() {
        this.dm.signUp(this.username, this.password, this.password2).then((data) => {
            console.log("Registrado correctamente");
        }).catch((error) => {
            console.log("Ha habido un error en el registro");
        });
    }

}