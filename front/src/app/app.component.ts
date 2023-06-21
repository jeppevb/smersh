import { Component, Input } from '@angular/core';
import { Vote } from './vote';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent {
  title = 'front';
  smersh: string = ""
  username: string = ""

  send_vote(vote: Vote){

  }
}
