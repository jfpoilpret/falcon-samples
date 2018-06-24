import { Component, OnInit } from '@angular/core';
import { BetService } from '../BetService.service';

@Component({
	selector: 'app-signin',
	templateUrl: './signin.component.html',
	styleUrls: ['./signin.component.css']
})
export class SigninComponent implements OnInit {

	constructor(private betService: BetService) { }

	ngOnInit() {
	}

	onSignIn(email: string, password: string) {
		this.betService.login(email, password);
	}
}
