import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpErrorResponse } from '@angular/common/http';
import { Observable, PartialObserver, of, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { MessagesService, MessageType } from './Messages.service';

interface Token {
	token: string;
	expiry: string;
	// expiry: Date;
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
				'Authorization': 'Token ' + btoa(this.token.token)
			})
		};
	}

	private handleError(error: HttpErrorResponse) {
		console.error(`Error: <${error.name}>: ${error.message}`);
		if (error.error instanceof ErrorEvent) {
			// A client-side or network error occurred. Handle it accordingly.
			console.error('An error occurred:', error.error.message);
		} else {
			// The backend returned an unsuccessful response code.
			// The response body may contain clues as to what went wrong,
			console.error(
				`Backend returned code ${error.status}, ` +
				`body was: ${error.error}`);
		}
		// return an observable with a user-facing error message
		return throwError(
			'Something bad happened; please try again later.');
	}

	login(email: string, password: string) {
		console.log(`login ${email}`);
		const options = {
			headers: new HttpHeaders({
				'Content-Type': 'application/json',
				'Authorization': 'Basic ' + btoa(`${email}:${password}`)
			}),
			withCredentials: true
		};
		const that = this;
		// this.http.get<Token>('api/token', options).subscribe({
		this.http.get('api/token', options).pipe(
			catchError(this.handleError)
		).subscribe({
			next: x => console.log('token received: ' + x),
			error: err => console.error('error in token: ' + err),
			complete: () => console.log('token done')
		});

		// this.http.get<Token>('api/token', options).subscribe(token => {
		// 	console.log('token received!');
		// 	that.token = token;
		// }, error => {
		// 	console.log(`Error ${error.toString()} :-(`);
		// });
		// this.http.get<Token>('api/token', options).pipe(
		// 	tap(token => this.token = token),
		// 	// catchError(noop)
		// );
	}

	isConnected(): boolean {
		return this.token != null;
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
