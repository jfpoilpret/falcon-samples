import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { noop } from 'rxjs';

interface Token {
	token: string;
	expiry: Date;
}

// FIXME is that the right to define enums in typescript?
enum UserState {
	pending,
	approved,
	suspended
}

export interface User {
	id: number;
	email: string;
	admin: boolean;
	fullname: string;
	score: number;
	creation: Date;
	conection?: Date;
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

@Injectable({
	providedIn: 'root'
})
export class BetService {
	private token: Token;

	constructor(private http: HttpClient) { }

	private headers() {
		return {
			headers: new HttpHeaders({
				'Content-Type': 'application/json',
				'Authorization': this.token.token
			})
		};
	}

	signIn(email: string, password: string) {
		const options = {
			headers: new HttpHeaders({
				'Content-Type': 'application/json',
				'Authorization': email
			})};
		this.http.get<Token>('token', options).pipe(
			tap(token => this.token = token),
			// catchError(noop)
		);
	}

	getBets() {
	}

	getMatches() {
	}

	getTeams() {
	}

	getUsers() {
	}

}
