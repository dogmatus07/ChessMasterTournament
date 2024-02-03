from view import View
from models import Player
from models import Tournament
import os

class Controller:
    def __init__(self) -> None:
        self.view = View()

    def create_player(self,
                      first_name,
                      last_name,
                      birthdate,
                      chess_id,
                      score=0):
        player = Player(first_name, last_name, birthdate, chess_id, score=0)
        self.view.display_player(player)
        return player

    def create_tournament(self, name, location, start_date, end_date, description):
        tournament = Tournament(name, location, start_date, end_date, description)
        self.view.display_tournament(tournament)
        return tournament

    def resume_tournament(self):
        self.view.display_resume_tournament()

