import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { MessagesService, MessageType } from './Messages.service';

interface Token {
	token: string;
	expiry: Date;
}

enum UserState {
	pending = 'pending',
	approved = 'approved',
	suspended = 'suspended'
}

export interface User {
	id: number;
	email: string;
	status: UserState;
	admin: boolean;
	fullname: string;
	score: number;
	creation: Date;
	connection?: Date;
}

export interface Team {
	id: number;
	name: string;
	group: string;
	rank?: number;
	played: number;
	won: number;
	drawn: number;
	lost: number;
	goals_for: number;
	goals_against: number;
	goals_diff: number;
	points: number;
}

export interface Venue {
	id: number;
	name: string;
}

export interface Match {
	id: number;
	matchnumber: number;
	round: string;
	matchtime: Date;
	group: string;
	venue: Venue;
	team1: Team;
	team2: Team;
	result?: string;
	winner?: Team;
	goals1?: number;
	goals2?: number;
}

// TODO check if other fields (better/better_id, winner...) are needed
export interface Bet {
	id: number;
	bettime?: Date;
	match: Match;
	result?: string;
}

// TODO catch error for login => need MessageServcie that will show something as an alert
// TODO catch error for all calls
// TODO use Http interceptor fro auto handling of authentication, and possibly errors too?
@Injectable({
	providedIn: 'root'
})
export class BetService {
	private token: Token;

	constructor(private http: HttpClient, private messagesService: MessagesService) { }

	private headers() {
		return {
			headers: new HttpHeaders({
				'Content-Type': 'application/json',
				'Authorization': 'Token: ' + btoa(this.token.token)
			})
		};
	}

	login(email: string, password: string) {
		const options = {
			headers: new HttpHeaders({
				'Content-Type': 'application/json',
				'Authorization': 'Basic:' + btoa(`${email}:${password}`)
			})};
		this.http.get<Token>('token', options).pipe(
			tap(token => this.token = token),
			// catchError(noop)
		);
	}

	getProfile(): Observable<User> {
		return this.http.get<User>('/profile', this.headers());
	}

	getBets(): Observable<Bet[]> {
		return this.http.get<Bet[]>('/bet', this.headers());
	}

	getMatches() {
	}

	getTeams() {
	}

	getUsers() {
	}

}
