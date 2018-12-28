import { RestService } from './restService';
import { Injectable } from "@angular/core";

@Injectable()
export class DataManagement {

    constructor(
        private restService: RestService,
    ) {

    }

    //public login()

    public logout(): Promise<any> {
        return new Promise((resolve, reject) => {
            return this.restService.logout().then((data) => {
                resolve(data);
            }).catch((error) => {
                reject('error');
            });
        });
    }

    public login(username: string, pass: string): Promise<any> {
        return this.restService.login(username, pass).then((data) => {
            return Promise.resolve(data);
        }).catch((error) => {
            return Promise.reject('error');
        })
    }

    public signUp(username: string, password1: string, password2: string, birthdate: Date, gender: string): Promise<any> {
        return new Promise((resolve, reject) => {
            if (password1 === password2) {
                return this.restService.signUp(username, password1, birthdate, gender).then((data) => {
                    resolve(data);
                }).catch((error) => {
                    reject(error);
                });
            } else {
                return reject('Las contraseñas no coinciden');
            }
        });
    }

    public getPollsUserLogged(): Promise<any> {
        return this.restService.getPollsUserLogged().then((data) => {
            return Promise.resolve(data);
        }).catch((error) => {
            console.log(error);
            return Promise.reject(error);
        })
    }

}