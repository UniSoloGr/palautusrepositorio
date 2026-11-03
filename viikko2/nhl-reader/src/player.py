import requests

class Player:
    def __init__(self, player_data):
        self.name = player_data['name']
        self.nationality = player_data['nationality']
        self.assists = player_data['assists']
        self.goals = player_data['goals']
        self.team = player_data['team']
        self.games = player_data['games']
        self.id = player_data['id']
    
    def __str__(self):
        return f"{self.name:20} {self.team:15} {self.goals:2} + {self.assists:2} = {self.goals + self.assists}"

class PlayerReader:
    def __init__(self, url):
        self.response = requests.get(url).json()

class PlayerStats:
    def __init__(self, reader):
        self.reader = reader
        self.players = []
        for player_dict in self.reader:
            player = Player(player_dict)
            self.players.append(player)


    def top_scorers_by_nationality(nationality):
        players = filter(lambda x: x.nationality == nationality, self.players).sort(
            key = lambda x: x.goals + x.assists, reverse=True
        )
        return players
        