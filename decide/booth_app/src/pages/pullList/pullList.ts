import { Component } from '@angular/core';
import { NavController, NavParams } from 'ionic-angular';

@Component({
  selector: 'page-pullList',
  templateUrl: 'pullList.html'
})
export class PullListPage {

  url: string;

  constructor() {
    this.url = "..\\..\\assets\\imgs\\Pet.png";
  }


}
