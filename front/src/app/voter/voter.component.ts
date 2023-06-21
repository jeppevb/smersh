import { Component, EventEmitter, Input, Output } from '@angular/core';
import { Vote } from '../vote';

@Component({
  selector: 'smh-voter',
  templateUrl: './voter.component.html',
  styleUrls: ['./voter.component.sass']
})

export class VoterComponent {
  @Output() vote_emitter: EventEmitter<Vote> = new EventEmitter()
  a: string = ""
  b: string = ""

  voted: boolean = false

  set_a_b(a:string, b:string){
    this.a = a
    this.b = b
    this.voted = false
  }

  vote(voted_a: boolean){
    if (!this.voted){
      this.vote_emitter.emit({
        a: this.a,
        b: this.b, 
        a_win: voted_a
      })
      this.voted = true;
    }
  }
}
