import { Injectable } from '@angular/core';

@Injectable()
export class ConfigService {

    constructor() {

    }

    public getConfig(): any {
        let urlPrefix = 'http://localhost:8000/';
        let urlApi = '';

        return {
            restUrlPrefix: urlPrefix + urlApi
        };
    }
}


