from player import PlayerStats


class StubReader:
    response = [
        {"name": "Alex", "nationality": "FIN", "assists": 4, "goals": 6,
         "team": "AAA", "games": 10, "id": 1},
        {"name": "Blake", "nationality": "CAN", "assists": 7, "goals": 5,
         "team": "AAA", "games": 10, "id": 2},
        {"name": "Casey", "nationality": "FIN", "assists": 2, "goals": 8,
         "team": "BBB", "games": 10, "id": 3},
    ]


class EmptyReader:
    response = []


def test_top_scorers_by_nationality_are_sorted_by_points():
    stats = PlayerStats(StubReader())

    players = stats.top_scorers_by_nationality("FIN")

    assert [player.name for player in players] == ["Alex", "Casey"]


def test_top_scorers_by_nationality_returns_empty_list_when_no_players_match():
    stats = PlayerStats(StubReader())

    assert stats.top_scorers_by_nationality("SWE") == []


def test_top_scorers_by_team_returns_only_matching_players_in_point_order():
    stats = PlayerStats(StubReader())

    players = stats.top_scorers_by_team("AAA")

    assert [player.name for player in players] == ["Blake", "Alex"]


def test_top_scorers_by_team_returns_empty_list_when_no_players_match():
    stats = PlayerStats(StubReader())

    assert stats.top_scorers_by_team("CCC") == []


def test_list_of_nationalities_returns_sorted_unique_values():
    stats = PlayerStats(StubReader())

    assert stats.list_of_nationalities() == ["CAN", "FIN"]


def test_list_of_nationalities_returns_empty_list_when_there_are_no_players():
    stats = PlayerStats(EmptyReader())

    assert stats.list_of_nationalities() == []


def test_top_goal_scorers_limits_results_and_sorts_by_goals():
    stats = PlayerStats(StubReader())

    players = stats.top_goal_scorers(2)

    assert [player.name for player in players] == ["Casey", "Alex"]


def test_top_goal_scorers_returns_empty_list_when_how_many_is_zero():
    stats = PlayerStats(StubReader())

    assert stats.top_goal_scorers(0) == []


def test_top_goal_scorers_returns_all_players_when_how_many_exceeds_player_count():
    stats = PlayerStats(StubReader())

    players = stats.top_goal_scorers(10)

    assert [player.name for player in players] == ["Casey", "Alex", "Blake"]
