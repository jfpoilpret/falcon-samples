/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { BetService } from './BetService.service';

describe('Service: BetService', () => {
	beforeEach(() => {
		TestBed.configureTestingModule({
			providers: [BetService]
		});
	});

	it('should ...', inject([BetService], (service: BetService) => {
		expect(service).toBeTruthy();
	}));
});
