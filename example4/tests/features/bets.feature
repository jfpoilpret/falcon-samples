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
		When match results are
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

	Scenario: Handle perfect teams ranking
		Given current date is "2018-06-30T00:00:00"
		When match results are
			| round | match                 | result |
			| 1     | Russia - Saudi Arabia | 3-0    |
			| 1     | Egypt - Uruguay       | 1-2    |
		Then teams in "Group A" should match
			| rank | team         | Pld | W | D | L | GF | GA | GD | Pts |
			| 1    | Russia       | 1   | 1 | 0 | 0 | 3  | 0  | 3  | 3   |
			| 2    | Uruguay      | 1   | 1 | 0 | 0 | 2  | 1  | 1  | 3   |
			| 3    | Egypt        | 1   | 0 | 0 | 1 | 1  | 2  | -1 | 0   |
			| 4    | Saudi Arabia | 1   | 0 | 0 | 1 | 0  | 3  | -3 | 0   |
		When match results are
			| round | match                  | result |
			| 2     | Russia - Egypt         | 2-1    |
			| 2     | Uruguay - Saudi Arabia | 2-0    |
		Then teams in "Group A" should match
			| rank | team         | Pld | W | D | L | GF | GA | GD | Pts |
			| 1    | Russia       | 2   | 2 | 0 | 0 | 5  | 1  | 4  | 6   |
			| 2    | Uruguay      | 2   | 2 | 0 | 0 | 4  | 1  | 3  | 6   |
			| 3    | Egypt        | 2   | 0 | 0 | 2 | 2  | 4  | -2 | 0   |
			| 4    | Saudi Arabia | 2   | 0 | 0 | 2 | 0  | 5  | -5 | 0   |
		When match results are
			| round | match                | result |
			| 3     | Uruguay - Russia     | 3-2    |
			| 3     | Saudi Arabia - Egypt | 1-2    |
		Then teams in "Group A" should match
			| rank | team         | Pld | W | D | L | GF | GA | GD | Pts |
			| 1    | Uruguay      | 3   | 3 | 0 | 0 | 7  | 3  | 4  | 9   |
			| 2    | Russia       | 3   | 2 | 0 | 1 | 7  | 4  | 3  | 6   |
			| 3    | Egypt        | 3   | 1 | 0 | 2 | 4  | 5  | -1 | 3   |
			| 4    | Saudi Arabia | 3   | 0 | 0 | 3 | 1  | 7  | -6 | 0   |
		And matches in "Round of 16" should match
			| matchnumber | match                       |
			| 49          | Uruguay - Runner-up Group B |
			| 51          | Winner Group B - Russia     |

	Scenario: Handle teams ranking with duplicate rank 1
		Given current date is "2018-06-30T00:00:00"
		When match results are
			| round | match                 | result |
			| 1     | Russia - Saudi Arabia | 2-1    |
			| 1     | Egypt - Uruguay       | 1-2    |
		Then teams in "Group A" should match
			| rank | team         | Pld | W | D | L | GF | GA | GD | Pts |
			| 1    | Russia       | 1   | 1 | 0 | 0 | 2  | 1  | 1  | 3   |
			| 1    | Uruguay      | 1   | 1 | 0 | 0 | 2  | 1  | 1  | 3   |
			| 2    | Egypt        | 1   | 0 | 0 | 1 | 1  | 2  | -1 | 0   |
			| 2    | Saudi Arabia | 1   | 0 | 0 | 1 | 1  | 2  | -1 | 0   |
		When match results are
			| round | match                  | result |
			| 2     | Russia - Egypt         | 2-1    |
			| 2     | Uruguay - Saudi Arabia | 2-1    |
		Then teams in "Group A" should match
			| rank | team         | Pld | W | D | L | GF | GA | GD | Pts |
			| 1    | Russia       | 2   | 2 | 0 | 0 | 4  | 2  | 2  | 6   |
			| 1    | Uruguay      | 2   | 2 | 0 | 0 | 4  | 2  | 2  | 6   |
			| 2    | Egypt        | 2   | 0 | 0 | 2 | 2  | 4  | -2 | 0   |
			| 2    | Saudi Arabia | 2   | 0 | 0 | 2 | 2  | 4  | -2 | 0   |
		When match results are
			| round | match                | result |
			| 3     | Uruguay - Russia     | 2-2    |
			| 3     | Saudi Arabia - Egypt | 0-1    |
		Then teams in "Group A" should match
			| rank | team         | Pld | W | D | L | GF | GA | GD | Pts |
			| 1    | Uruguay      | 3   | 2 | 1 | 0 | 6  | 4  | 2  | 7   |
			| 1    | Russia       | 3   | 2 | 1 | 0 | 6  | 4  | 2  | 7   |
			| 2    | Egypt        | 3   | 1 | 0 | 2 | 3  | 4  | -1 | 3   |
			| 3    | Saudi Arabia | 3   | 0 | 0 | 3 | 2  | 5  | -3 | 0   |
		And matches in "Round of 16" should match
			| matchnumber | match                              |
			| 49          | Winner Group A - Runner-up Group B |
			| 51          | Winner Group B - Runner-up Group A |

	@debug
	Scenario: Handle teams ranking with duplicate rank 1
		Given current date is "2018-06-30T00:00:00"
		When match results are
			| round | match                 | result |
			| 1     | Russia - Saudi Arabia | 2-1    |
			| 1     | Egypt - Uruguay       | 1-2    |
		Then teams in "Group A" should match
			| rank | team         | Pld | W | D | L | GF | GA | GD | Pts |
			| 1    | Russia       | 1   | 1 | 0 | 0 | 2  | 1  | 1  | 3   |
			| 1    | Uruguay      | 1   | 1 | 0 | 0 | 2  | 1  | 1  | 3   |
			| 2    | Egypt        | 1   | 0 | 0 | 1 | 1  | 2  | -1 | 0   |
			| 2    | Saudi Arabia | 1   | 0 | 0 | 1 | 1  | 2  | -1 | 0   |
		When match results are
			| round | match                  | result |
			| 2     | Russia - Egypt         | 2-2    |
			| 2     | Uruguay - Saudi Arabia | 2-1    |
		Then teams in "Group A" should match
			| rank | team         | Pld | W | D | L | GF | GA | GD | Pts |
			| 1    | Uruguay      | 2   | 2 | 0 | 0 | 4  | 2  | 2  | 6   |
			| 2    | Russia       | 2   | 1 | 1 | 0 | 4  | 3  | 1  | 4   |
			| 3    | Egypt        | 2   | 0 | 1 | 1 | 3  | 4  | -1 | 1   |
			| 4    | Saudi Arabia | 2   | 0 | 0 | 2 | 2  | 4  | -2 | 0   |
		When match results are
			| round | match                | result |
			| 3     | Uruguay - Russia     | 1-0    |
			| 3     | Saudi Arabia - Egypt | 0-1    |
		Then teams in "Group A" should match
			| rank | team         | Pld | W | D | L | GF | GA | GD | Pts |
			| 1    | Uruguay      | 3   | 3 | 0 | 0 | 5  | 2  | 3  | 9   |
			| 2    | Russia       | 3   | 1 | 1 | 1 | 4  | 4  | 0  | 4   |
			| 2    | Egypt        | 3   | 1 | 1 | 1 | 4  | 4  | 0  | 4   |
			| 3    | Saudi Arabia | 3   | 0 | 0 | 3 | 2  | 5  | -3 | 0   |
		And matches in "Round of 16" should match
			| matchnumber | match                              |
			| 49          | Uruguay - Runner-up Group B        |
			| 51          | Winner Group B - Runner-up Group A |

	# #TODO review later
	Scenario: Handle bets throughout the whole competition
		Given current date is "2018-06-01T00:00:00"
		And user "aaa" places bets
			| round | match                   | result |
			| 1     | Russia - Saudi Arabia   | 3-0    |
			| 1     | Egypt - Uruguay         | 1-2    |
			| 1     | Morocco - Iran          | 2-1    |
			| 1     | Portugal - Spain        | 1-1    |
			| 1     | France - Australia      | 2-1    |
			| 1     | Argentina - Iceland     | 2-1    |
			| 1     | Peru - Denmark          | 0-1    |
			| 1     | Croatia - Nigeria       | 2-0    |
			| 1     | Costa Rica - Serbia     | 0-2    |
			| 1     | Germany - Mexico        | 3-1    |
			| 1     | Brazil - Switzerland    | 3-0    |
			| 1     | Sweden - Korea Republic | 2-1    |
			| 1     | Belgium - Panama        | 3-1    |
			| 1     | Tunisia - England       | 1-3    |
			| 1     | Colombia - Japan        | 0-2    |
			| 1     | Poland - Senegal        | 1-1    |
		When current date is "2018-06-30T00:00:00"
		And match results are
			#TODO other results to put here
			| round | match                   | result |
			| 1     | Russia - Saudi Arabia   | 3-0    |
			| 1     | Egypt - Uruguay         | 1-2    |
			| 1     | Morocco - Iran          | 2-1    |
			| 1     | Portugal - Spain        | 1-1    |
			| 1     | France - Australia      | 2-1    |
			| 1     | Argentina - Iceland     | 2-1    |
			| 1     | Peru - Denmark          | 0-1    |
			| 1     | Croatia - Nigeria       | 2-0    |
			| 1     | Costa Rica - Serbia     | 0-2    |
			| 1     | Germany - Mexico        | 3-1    |
			| 1     | Brazil - Switzerland    | 3-0    |
			| 1     | Sweden - Korea Republic | 2-1    |
			| 1     | Belgium - Panama        | 3-1    |
			| 1     | Tunisia - England       | 1-3    |
			| 1     | Colombia - Japan        | 0-2    |
			| 1     | Poland - Senegal        | 1-1    |
		#TODO add step to check teams score in 1 or 2 groups
		Then user "aaa" score should be 48
#TODO Add round 2 then round 3
#TODO Add step to set matches for round of 16
#TODO Add quarter finals, semi finals and 2 finals
#TODO Check that teams automatically set by system once results have been set
