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

	Scenario: Handle bets throughout the whole competition
		Given current date is "2018-06-14T00:00:00"
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
		When current date is "2018-06-19T18:00:00+03:00"
		And match results are
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
		Then user "aaa" score should be 48
		Given user "aaa" places bets
			| round | match                   | result |
			| 2     | Russia - Egypt          | 3-0    |
			| 2     | Uruguay - Saudi Arabia  | 1-2    |
			| 2     | Portugal - Morocco      | 2-1    |
			| 2     | Iran - Spain            | 1-1    |
			| 2     | France - Peru           | 2-1    |
			| 2     | Denmark - Australia     | 2-1    |
			| 2     | Argentina - Croatia     | 0-1    |
			| 2     | Nigeria - Iceland       | 2-0    |
			| 2     | Brazil - Costa Rica     | 0-2    |
			| 2     | Serbia - Switzerland    | 3-1    |
			| 2     | Germany - Sweden        | 3-0    |
			| 2     | Korea Republic - Mexico | 2-1    |
			| 2     | Belgium - Tunisia       | 3-1    |
			| 2     | England - Panama        | 1-3    |
			| 2     | Poland - Colombia       | 0-2    |
			| 2     | Japan - Senegal         | 1-1    |
		When current date is "2018-06-25T00:00:00"
		And match results are
			| round | match                   | result |
			| 2     | Russia - Egypt          | 3-0    |
			| 2     | Uruguay - Saudi Arabia  | 1-2    |
			| 2     | Portugal - Morocco      | 2-1    |
			| 2     | Iran - Spain            | 1-1    |
			| 2     | France - Peru           | 2-1    |
			| 2     | Denmark - Australia     | 2-1    |
			| 2     | Argentina - Croatia     | 0-1    |
			| 2     | Nigeria - Iceland       | 2-0    |
			| 2     | Brazil - Costa Rica     | 0-2    |
			| 2     | Serbia - Switzerland    | 3-1    |
			| 2     | Germany - Sweden        | 3-0    |
			| 2     | Korea Republic - Mexico | 2-1    |
			| 2     | Belgium - Tunisia       | 3-1    |
			| 2     | England - Panama        | 1-3    |
			| 2     | Poland - Colombia       | 0-2    |
			| 2     | Japan - Senegal         | 1-1    |
		Then user "aaa" score should be 96
		Given user "aaa" places bets
			| round | match                    | result |
			| 3     | Uruguay - Russia         | 3-2    |
			| 3     | Saudi Arabia - Egypt     | 1-1    |
			| 3     | Iran - Portugal          | 2-0    |
			| 3     | Spain - Morocco          | 1-4    |
			| 3     | Denmark - France         | 2-0    |
			| 3     | Australia - Peru         | 2-2    |
			| 3     | Nigeria - Argentina      | 4-1    |
			| 3     | Iceland - Croatia        | 2-5    |
			| 3     | Serbia - Brazil          | 2-2    |
			| 3     | Switzerland - Costa Rica | 3-4    |
			| 3     | Korea Republic - Germany | 3-2    |
			| 3     | Mexico - Sweden          | 2-2    |
			| 3     | England - Belgium        | 3-3    |
			| 3     | Panama - Tunisia         | 1-5    |
			| 3     | Japan - Poland           | 3-2    |
			| 3     | Senegal - Colombia       | 4-3    |
		When current date is "2018-06-29T00:00:00"
		And match results are
			| round | match                    | result |
			| 3     | Uruguay - Russia         | 3-2    |
			| 3     | Saudi Arabia - Egypt     | 1-1    |
			| 3     | Iran - Portugal          | 2-0    |
			| 3     | Spain - Morocco          | 1-4    |
			| 3     | Denmark - France         | 2-0    |
			| 3     | Australia - Peru         | 2-2    |
			| 3     | Nigeria - Argentina      | 4-1    |
			| 3     | Iceland - Croatia        | 2-5    |
			| 3     | Serbia - Brazil          | 2-2    |
			| 3     | Switzerland - Costa Rica | 3-4    |
			| 3     | Korea Republic - Germany | 3-2    |
			| 3     | Mexico - Sweden          | 2-2    |
			| 3     | England - Belgium        | 3-3    |
			| 3     | Panama - Tunisia         | 1-5    |
			| 3     | Japan - Poland           | 3-2    |
			| 3     | Senegal - Colombia       | 4-3    |
		Then user "aaa" score should be 144
		And matches in "Round of 16" should match
			| matchnumber | match                   |
			| 49          | Russia - Iran           |
			| 50          | Denmark - Nigeria       |
			| 51          | Morocco - Uruguay       |
			| 52          | Croatia - France        |
			| 53          | Serbia - Korea Republic |
			| 54          | Belgium - Senegal       |
			| 55          | Germany - Costa Rica    |
			| 56          | Japan - England         |
		Given user "aaa" places bets
			| round       | match                   | result |
			| Round of 16 | Russia - Iran           | 3-0    |
			| Round of 16 | Denmark - Nigeria       | 2-1    |
			| Round of 16 | Morocco - Uruguay       | 1-2    |
			| Round of 16 | Croatia - France        | 2-3    |
			| Round of 16 | Serbia - Korea Republic | 2-0    |
			| Round of 16 | Belgium - Senegal       | 3-2    |
			| Round of 16 | Germany - Costa Rica    | 3-0    |
			| Round of 16 | Japan - England         | 2-3    |
		When current date is "2018-07-04T00:00:00"
		And match results are
			| round       | match                   | result |
			| Round of 16 | Russia - Iran           | 3-0    |
			| Round of 16 | Denmark - Nigeria       | 2-1    |
			| Round of 16 | Morocco - Uruguay       | 1-2    |
			| Round of 16 | Croatia - France        | 2-3    |
			| Round of 16 | Serbia - Korea Republic | 2-0    |
			| Round of 16 | Belgium - Senegal       | 3-2    |
			| Round of 16 | Germany - Costa Rica    | 3-0    |
			| Round of 16 | Japan - England         | 2-3    |
		Then user "aaa" score should be 168
		And matches in "Quarter Finals" should match
			| matchnumber | match             |
			| 57          | Russia - Denmark  |
			| 58          | Serbia - Belgium  |
			| 59          | Uruguay - France  |
			| 60          | Germany - England |
		Given user "aaa" places bets
			| round          | match             | result |
			| Quarter Finals | Russia - Denmark  | 2-1    |
			| Quarter Finals | Serbia - Belgium  | 1-2    |
			| Quarter Finals | Uruguay - France  | 1-2    |
			| Quarter Finals | Germany - England | 3-2    |
		When current date is "2018-07-08T00:00:00"
		And match results are
			| round          | match             | result |
			| Quarter Finals | Russia - Denmark  | 2-1    |
			| Quarter Finals | Serbia - Belgium  | 1-2    |
			| Quarter Finals | Uruguay - France  | 1-2    |
			| Quarter Finals | Germany - England | 3-2    |
		Then user "aaa" score should be 180
		And matches in "Semi Finals" should match
			| matchnumber | match            |
			| 61          | Russia - Belgium |
			| 62          | France - Germany |
		Given user "aaa" places bets
			| round       | match            | result |
			| Semi Finals | Russia - Belgium | 6-5    |
			| Semi Finals | France - Germany | 7-6    |
		When current date is "2018-07-12T00:00:00"
		And match results are
			| round       | match            | result |
			| Semi Finals | Russia - Belgium | 6-5    |
			| Semi Finals | France - Germany | 7-6    |
		Then user "aaa" score should be 186
		And matches in "Finals" should match
			| matchnumber | match             |
			| 63          | Belgium - Germany |
			| 64          | Russia - France   |
		Given user "aaa" places bets
			| round  | match             | result |
			| Finals | Belgium - Germany | 1-3    |
			| Finals | Russia - France   | 1-3    |
		When current date is "2018-07-16T00:00:00"
		And match results are
			| round  | match             | result |
			| Finals | Belgium - Germany | 1-3    |
			| Finals | Russia - France   | 1-3    |
		Then user "aaa" score should be 192
