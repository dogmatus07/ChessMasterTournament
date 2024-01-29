from view import View
from models import Player


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
        return player

