import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http'

@Injectable()
export class AbstractService {

    constructor(
        private http: HttpClient
    ) {

    }

    private getHeaders(): Promise<HttpHeaders> {
        return new Promise((resolve) => {
            let headers = new HttpHeaders().set("Accept", "application/json");
            resolve(headers);
        })
    }

    protected makeGetRequest(path: string, paramsRequest: any): Promise<any> {
        if (!paramsRequest)
            paramsRequest = {};

        return this.getHeaders().then((result) => {
            return new Promise((resolve, reject) => {
                this.http.get(path, { headers: result, params: paramsRequest }).subscribe(response => {
                    resolve(response);
                }, error => {
                    if (error.status == 200) {
                        resolve(null);
                    } else {
                        console.log(error);
                        reject(error);
                    }
                });
            });
        });
    }

    protected makePostRequest(path: string, data: any): Promise<any> {
        return this.getHeaders().then((result) => {
            return this.http.post(path, data, { headers: result })
                .toPromise()
                .then((result: HttpResponse<any>) => {
                    return Promise.resolve(result);
                }).catch((err) => {
                    return Promise.reject(err);
                });
        });
    }


}
