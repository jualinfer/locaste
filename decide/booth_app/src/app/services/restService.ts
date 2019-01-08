import { HttpClient } from '@angular/common/http';
import { ConfigService } from './../../config/configService';
import { AbstractService } from './abstractService';
import { Injectable } from "@angular/core";
import { User, Voting, Option } from '../app.data.models';
import { CookieService } from 'ngx-cookie-service';
import { ElGamal } from './../../theme/crypto/elgamal';
import { BigInt } from './../../theme/crypto/BigInt';
import { jsbn } from './../../theme/crypto/jsbn';
import { jsbn2 } from './../../theme/crypto/jsbn2';
import { sjcl } from './../../theme/crypto/sjcl';

@Injectable()
export class RestService extends AbstractService {
    path: string;
    ElGamal = 256;
    bigpk = {
        p: BigInt.fromJSONObject("82643657556894946728015596219769215539034924986637827091199915061922676560027"),
        g: BigInt.fromJSONObject("29754636446977317234968558514570282907227658437381086964370531713408561309461"),
        y: BigInt.fromJSONObject("60347897324258881463769870948422257740897067249236479963281276201752547048248"),
    };
    cypher: any;
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
        return this.makeGetRequest(this.path + 'voting/?format=json&id=' + id, null).then((res) => {
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
            return this.makeGetRequest(this.path + 'census/?voter_id=' + user.id, null).then((res) => {
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
        let fd = new FormData();
        let user = new User;
        let v = this.cypher;
        let data = {
            vote: { a: v.alpha.toString(), b: v.beta.toString() },
            voting: voting.id,
            voter: user.id,
            token: this.cookieService.get('decide')
        };
        return this.getUserWithToken(this.cookieService.get('decide')).then((response) => {
            user = response;
            fd.append('voting', voting.id);
            fd.append('voter', user.id);
            fd.append('vote', String(data.vote));
            fd.append('token', data.token);
            return this.makePostRequest(this.path + 'store/', fd).then((res) => {
                return Promise.resolve(res);
            }).catch((error) => {
                console.log("Error " + error);
                return Promise.reject(error);
            });
        }).catch((error) => {
            console.log("Error " + error);
        });
    }





    public decideEncrypt() {
        let msg = document.querySelector("input[name=question]:checked");
        let bigmsg = BigInt.fromJSONObject(msg);
        console.log(bigmsg);
        this.cypher = ElGamal.encrypt(this.bigpk, bigmsg);
    }


}