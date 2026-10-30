import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_player_search_returns_correct_player(self):
        name = "Semenko"
        player = self.stats.search(name)
        self.assertEqual(player.name, name)
    
    def test_missing_player_name_returns_none(self):
        name = "Simenko"
        player = self.stats.search(name)
        self.assertEqual(player, None)

    def test_get_list_of_team_players(self):
        team_name = "EDM"
        self.assertEqual(self.stats.team(team_name)[0].team, team_name)

    def test_top_players_are_in_right_order(self):
        top_list = self.stats.top(2)
        print(top_list)
        self.assertEqual(
            list(map(lambda player: player.points, top_list)),
            [124, 99, 98]
        )
