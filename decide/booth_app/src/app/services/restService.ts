import { HttpClient, HttpRequest } from '@angular/common/http';
import { ConfigService } from './../../config/configService';
import { AbstractService } from './abstractService';
import { Injectable } from "@angular/core";
import { User, Voting, Option } from '../app.data.models';
import { CookieService } from 'ngx-cookie-service';

@Injectable()
export class RestService extends AbstractService {
    path: string;
   
    constructor(
        private config: ConfigService,
        http: HttpClient,
        private cookieService: CookieService
    ) {
        super(http);
        //Localhost:8080
        this.path = this.config.getConfig().restUrlPrefix;
    }

    //Methods
    public logout(): Promise<any> {
        return this.makeGetRequest(this.path + 'authentication/logout/', null).then((res) => {
            return Promise.resolve(res);
        }).catch((error) => {
            return Promise.reject(error);
        });
    }

    public login(username: string, pass: string): Promise<any> {
        let fd = new FormData();
        fd.append('username', username);
        fd.append('password', pass);

        return this.makePostRequest(this.path + 'rest-auth/login/', fd).then((res) => {
            console.log("Se ha logueado exitosamente");
            return Promise.resolve(res);
        }).catch((error) => {
            console.log("Error: " + error);
            return Promise.reject(error);
        })
    }

    public signUp(username: string, password: string, birthdate: string, gender: string): Promise<any> {
        let fd = new FormData();
        fd.append('username', username);
        fd.append('password1', password);
        fd.append('password2', password);
        fd.append('birthdate', birthdate);
        fd.append('gender', gender);


        return this.makePostRequest(this.path + 'authentication/signup/', fd).then((res) => {
            console.log("Se ha registrado correctamente");
            return Promise.resolve(res);
        }).catch((error) => {
            console.log("Error " + error);
            return Promise.reject(error);
        });
    }

    public getPollWithId(id: string): Promise<Voting> {
        let user = this.cookieService.get('username');
        let password = this.cookieService.get('password');
        return this.makeGetRequest2(this.path + 'voting/?format=json&id=' + id, null, user, password).then((res) => {
            return Promise.resolve(res);
        }).catch((error) => {
            console.log("Error " + error);
            return Promise.reject(error);
        });
    }

    public getPollsIdUserLogged(): Promise<any> {
        let user = new User;
        return this.getUserWithToken(this.cookieService.get('decide')).then((response) => {
            user = response;
            let password = this.cookieService.get('password');
            return this.makeGetRequest2(this.path + 'census/?voter_id=' + user.id, null, user.username, password).then((res) => {
                return Promise.resolve(res);
            }).catch((error) => {
                console.log("Error " + error);
                return Promise.reject(error);
            });
        }).catch((error) => {
            console.log("Error " + error);
        });
    }

    public getUserWithToken(token: string): Promise<User> {
        let fd = new FormData();
        fd.append('token', token);
        return this.makePostRequest(this.path + 'authentication/getuser/', fd).then((res) => {
            return Promise.resolve(res);
        }).catch((error) => {
            console.log("Error " + error);
            return Promise.reject(error);
        });
    }

    public vote(voting: Voting, option: Option): Promise<any> {
        return null;
    }
}