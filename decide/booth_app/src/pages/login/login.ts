import { CookieService } from 'ngx-cookie-service';
import { NavController, NavParams, LoadingController, Loading } from 'ionic-angular';
import { Component, EventEmitter, Output } from '@angular/core';
import { DataManagement } from '../../app/services/dataManagemen'
import { HomePage } from '../home/home';
import { PullListPage } from '../pullList/pullList';

@Component({
    selector: 'page-login',
    templateUrl: 'login.html'
})

export class LoginPage {

    username: string = "";
    password: string = "";
    password2: string;
    birthdate: Date;
    gender: string;
    @Output()
    logged: EventEmitter<boolean> = new EventEmitter<boolean>();
    loading: Loading;

    status: string = 'login';

    error: string;

    constructor(
        public navCtrl: NavController,
        public navParams: NavParams,
        public dm: DataManagement,
        public loadingCtrl: LoadingController,
        private cookieService: CookieService,
    ) {
        this.loading = this.loadingCtrl.create({
            content: 'Logging in, please wait...',
        });
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
        this.loading.present();
        this.dm.login(this.username, this.password).then((data) => {
            this.cookieService.set('decide', data.key, this.getTimeToExpire());
            this.cookieService.set('username', this.username, this.getTimeToExpire());
            this.cookieService.set('password', this.password, this.getTimeToExpire());
            this.logged.emit(false);
            this.loading.dismiss();
        }).catch((error) => {
            this.error = error;
            this.loading.dismiss();
        });
    }

    public signUp() {
        this.dm.signUp(this.username, this.password, this.password2, this.birthdate, this.gender).then((data) => {
            console.log("Registrado correctamente");
            this.login();
        }).catch((error) => {
            console.log("Ha habido un error en el registro");
        });
    }

    private getTimeToExpire(): Date {
        let now = new Date();
        return new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours(), now.getMinutes() + 2);
        //return new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours(), now.getMinutes(), now.getSeconds() + 10);
    }

}