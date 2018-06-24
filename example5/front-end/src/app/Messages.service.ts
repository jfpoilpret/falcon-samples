import { Injectable } from '@angular/core';

export enum MessageType {
	Success = 'success',
	Info = 'info',
	Warning = 'warning',
	Danger = 'danger'
}

export interface Message {
	id: number;
	message: string;
	type: MessageType;
}

@Injectable({
	providedIn: 'root'
})
export class MessagesService {
	private nextId: number;
	messages: Message[];

	constructor() {
		this.nextId = 1;
		this.messages = [];
	}

	private add(message: string, type: MessageType) {
		this.messages.push({
			id: this.nextId++,
			message,
			type
		});
	}

	addSuccess(message: string) {
		this.add(message, MessageType.Success);
	}
	addInfo(message: string) {
		this.add(message, MessageType.Info);
	}
	addWarning(message: string) {
		this.add(message, MessageType.Warning);
	}
	addDanger(message: string) {
		this.add(message, MessageType.Danger);
	}

	clearMessage(id: number) {
		const index: number = this.messages.findIndex(message => message.id === id);
		if (index >= 0) {
			this.messages.splice(index, 1);
		}
	}

	clear() {
		this.messages = [];
	}
}
