import uuid
from datetime import datetime
class Tournament:
    """
    This class represent a tournament
    """
    tournament_count = 0
    all_tournaments = {}

    def __init__(self, name, location, start_date, end_date, description, number_of_rounds=4):

        Tournament.tournament_count += 1
        self.tournament_id = uuid.uuid4()
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.number_of_rounds = number_of_rounds
        self.current_round_number = 1
        self.players = []  # players list
        self.rounds = []  # rounds list
        self.all_tournaments[self.tournament_count] = self

    def add_player(self, player):
        self.players.append(player)

    def start_new_round(self, round_name):
        if len(self.rounds) < self.number_of_rounds:
            current_round_id = len(self.rounds) + 1
            new_round = Round(
                name=round_name,
                current_round_id=current_round_id,
                matches=[],
                start_date=datetime.now(),
                end_date=None,
                is_complete=False)
            self.rounds.append(new_round)
            print(f"Nouveau tour démarré : {round_name}")
        else:
            print(f"Nombre maximum de tours atteint")

    def __str__(self):
        return (
            f"ID Tournoi : {self.tournament_id} "
            f"Nom : {self.name} "
            f"Lieu : {self.location} "
            f"Date de Début : {self.start_date} "
            f"Date de fin : {self.end_date} "
            f"Description : {self.description} "
        )


class Player:
    """
    This class represent a Player
    """
    player_count = 0  # will be used for a unique player_id
    all_players = {}

    def __init__(
            self,
            first_name,
            last_name,
            gender,
            birthdate,
            chess_id,
            score=0):
        Player.player_count += 1  # everytime a player is created
        self.player_id = Player.player_count
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birthdate = birthdate
        self.score = score
        self.chess_id = chess_id  # Two letters followed by five digits
        self.match_won = []
        self.match_lost = []

        Player.all_players[self.player_id] = self

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    def update_score(self, points: float):
        self.score += points
        return self.score


    def __str__(self):
        return (
            f"Identifiant : {self.player_id}, "
            f"Nom & Prénoms : {self.first_name} {self.last_name}, "
            f"Date de naissance : {self.birthdate}, "
            f"Chess ID : {self.chess_id}, "
            f"Score : {self.score}"
        )

class Round:
    """
    This class represent a round
    """
    def __init__(self, name, current_round_id, matches, start_date, end_date, is_complete, round_number=4):
        self.name = name
        self.current_round_id = current_round_id
        self.matches = matches if matches is not None else []
        self.start_date = start_date
        self.end_date = end_date
        self.is_complete = is_complete
        self.round_number = round_number

    def close_round(self):
        self.end_date = datetime.now()
        self.is_complete = True

    def __str__(self):
        return f"Round Number: {self.round_number}, Matches: {self.matches}, Status: {self.is_complete}"


class Match:
    """
    This class represent a Match
    """

    def __init__(self, match_id, player1, player2):
        self.match_id = match_id
        self.player1 = player1
        self.player2 = player2
        self.winner = None
        self.loser = None
        self.result = None

    def set_result(self, winner=None):
        if winner is None:
            self.result = 'draw'
            self.player1.score += 0.5
            self.player2.score += 0.5
        elif winner == self.player1:
            self.result = 'player1'
            self.player1.score += 1
        else:
            self.result = 'player2'
            self.player2.score += 1




    def __str__(self):
        return (
            f"Match ID : {self.match_id}, "
            f"Player 1: {self.player1}, "
            f"Player2: {self.player2}, "
            f"Match Results: {self.match_result}",
        )
