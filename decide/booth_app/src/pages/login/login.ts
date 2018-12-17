import { NavController, NavParams } from 'ionic-angular';
import { Component } from '@angular/core';
import { DataManagement } from '../../app/services/dataManagemen'
import { HomePage } from '../home/home';

@Component({
    selector: 'page-login',
    templateUrl: 'login.html'
})

export class LoginPage {

    username: string;
    password: string;
    password2: string;
    error: string;

    constructor(
        public navCtrl: NavController,
        public navParams: NavParams,
        public dm: DataManagement
    ) {

    }

    public login() {
        this.dm.login(this.username, this.password).then((data) => {
            this.navCtrl.push(HomePage).then((data) => {
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