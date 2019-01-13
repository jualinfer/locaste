import { RestService } from './restService';
import { Injectable } from "@angular/core";
import { Voting, Option } from '../app.data.models';

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
                let birthdateString: string = String(birthdate) + "T00:00";
                console.log(birthdateString);
                return this.restService.signUp(username, password1, birthdateString, gender).then((data) => {
                    resolve(data);
                }).catch((error) => {
                    reject(error);
                });
            } else {
                return reject('Las contraseñas no coinciden');
            }
        });
    }

    public getPollsIdUserLogged(): Promise<any> {
        return this.restService.getPollsIdUserLogged().then((data) => {
            return Promise.resolve(data);
        }).catch((error) => {
            console.log(error);
            return Promise.reject(error);
        });
    }

    public getPollWithId(id: string): Promise<any> {
        return this.restService.getPollWithId(id).then((data) => {
            return Promise.resolve(data);
        }).catch((error) => {
            console.log(error);
            return Promise.reject(error);
        });
    }

    public vote(voting: Voting, option: Option): Promise<any> {
        return this.restService.vote(voting, option).then((data) => {
            return Promise.resolve(data);
        }).catch((error) => {
            console.log(error);
            return Promise.reject(error);
        });
    }

}