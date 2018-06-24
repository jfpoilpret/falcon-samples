import { Component, OnInit } from '@angular/core';
import { BetService } from '../BetService.service';

@Component({
	selector: 'app-menu',
	templateUrl: './menu.component.html',
	styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {

	constructor(public betService: BetService) { }

	ngOnInit() {
	}

}
