import { Component, OnInit } from '@angular/core';
import { MessagesService } from '../Messages.service';

@Component({
	selector: 'app-messages',
	templateUrl: './messages.component.html',
	styleUrls: ['./messages.component.css']
})
export class MessagesComponent implements OnInit {

	constructor(public messagesService: MessagesService) { }

	ngOnInit() {
		// TODO for tests only remvoe afterwards
		this.messagesService.addInfo('Hello');
		this.messagesService.addWarning('This is a warning');
	}

	closeMessage(id: number) {
		this.messagesService.clearMessage(id);
	}

}
