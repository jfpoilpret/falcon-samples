Feature: Place bets on matches and get score after matches play

	As a user,
	I want to place bets on future matches
	In order to get a good score

	Background: System is ready for tests
		Given system is ready
		And user "aaa" exists

	Scenario Outline: Place bets on unknown teams future matches is not allowed
		Given current date is "2018-06-01T00:00:00"
		When user "aaa" places bets
			| round | match                 | result |
			| 1     | Russia - Saudi Arabia | <bet>  |
		Then user "aaa" bets should match
			| round | match                 | result |
			| 1     | Russia - Saudi Arabia | <bet>  |
		Given current date is "2018-06-30T00:00:00"
		When admin sets match results
			| round | match                 | result   |
			| 1     | Russia - Saudi Arabia | <result> |
		Then user "aaa" score should be <score>

		Examples: Russia wins
			| bet | result | score |
			| 2-0 | 2-0    | 3     |
			| 3-1 | 2-0    | 2     |
			| 2-1 | 2-0    | 1     |
			| 1-1 | 2-0    | 0     |
			| 0-2 | 2-0    | 0     |

		Examples: Russia and Saudi Arabia draws
			| bet | result | score |
			| 2-2 | 2-2    | 3     |
			| 1-1 | 2-2    | 2     |
			| 0-0 | 2-2    | 2     |
			| 1-0 | 2-2    | 0     |
			| 1-2 | 2-2    | 0     |

		Examples: Saudi Arabia wins
			| bet | result | score |
			| 0-2 | 0-2    | 3     |
			| 2-4 | 0-2    | 2     |
			| 1-2 | 0-2    | 1     |
			| 2-2 | 0-2    | 0     |
			| 2-0 | 0-2    | 0     |
