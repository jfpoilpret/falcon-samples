Feature: Place bets on matches and get score after matches play

	As a user,
	I want to place bets on future matches
	In order to get a good score

	Background: System is ready for tests
		Given system is ready
		And user "aaa" exists

	Scenario: Place bets on unknown teams future matches is not allowed
		Given current date is "2018-06-01"
		When user "aaa" places bets
			| round | match                 | result |
			| 1     | Russia - Saudi Arabia | 2-0    |
		Then user "aaa" bets should match
			| round | match                 | result |
			| 1     | Russia - Saudi Arabia | 2-0    |
		Given current date is "2018-06-30"
		When admin sets match results
			| round | match                 | result |
			| 1     | Russia - Saudi Arabia | 2-0    |
		Then user "aaa" score should be 3

		