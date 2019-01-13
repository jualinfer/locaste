import { Component } from "@angular/core";
import {
  NavController,
  LoadingController,
  Loading,
  NavParams
} from "ionic-angular";
import { Voting, Option, Question } from "../../app/app.data.models";
import { DataManagement } from "../../app/services/dataManagemen";
import { stringify } from "@angular/core/src/util";

@Component({
  selector: "page-voting",
  templateUrl: "voting.html"
})
export class VotingPage {
  url: string = "..\\..\\assets\\imgs\\Pet.png";
  loading: Loading;
  voting: Voting;
  questions: Question[];
  options: Option[];
  start_date: string;
  end_date: string;
  booleanStart: boolean;
  booleanEnd: boolean;

  constructor(
    public navCtrl: NavController,
    public NavParams: NavParams,
    public dm: DataManagement,
    private loadingCtrl: LoadingController
  ) {
    this.loading = this.loadingCtrl.create({
      content: "Signing out, please wait..."
    });
    this.voting = this.NavParams.get("voting");
    let startString: string =
      String(this.voting.start_date).substring(0, 10) +
      " " +
      String(this.voting.start_date).substring(11, 16);
    this.start_date = startString;
    if (this.voting.start_date === null) {
      this.booleanStart = false;
    } else {
      this.booleanStart = true;
    }
    let endString: string =
      String(this.voting.end_date).substring(0, 10) +
      " " +
      String(this.voting.end_date).substring(11, 16);
    this.end_date = endString;
    if (this.voting.end_date === null) {
      this.booleanEnd = false;
    } else {
      this.booleanEnd = true;
    }
    this.questions = this.voting.question;
    console.log(this.voting);
    console.log(this.options);
  }

  public vote(voting: Voting, option: Option) {
    console.log(voting);
    console.log(option);
    this.dm
      .vote(voting, option)
      .then(data => {
        console.log("Ha votado correctamente");
      })
      .catch(error => {
        console.log("Ha habido un error en la votación");
      });
  }
}
