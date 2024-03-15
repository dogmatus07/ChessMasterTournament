from datetime import datetime
from enum import Enum, auto


class TournamentStatus(Enum):
    PENDING = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()


class Tournament:
    """
    This class represents a tournament.
    """

    def __init__(self,
                 name,
                 location,
                 start_date,
                 end_date,
                 description,
                 round_ids=None,
                 match_ids=None,
                 player_ids=None,
                 doc_id=None,
                 current_round_id=None,
                 status=TournamentStatus.PENDING):
        self.doc_id = doc_id
        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.round_ids = []  # will contain the list of rounds id
        self.match_ids = []  # will contain the list of matches id
        self.player_ids = []  # will contain the list of players id
        self.current_round_id = current_round_id
        self.status = status

    def __str__(self):
        return (f"Tournament ID : {self.doc_id}\n"
                f"Name : {self.name}\n"
                f"Location : {self.location}\n"
                f"Start Date : {self.start_date.strftime('%d/%m/%Y')}\n"
                f"End Date : {self.end_date.strftime('%d/%m/%Y')}\n"
                f"Description : {self.description}\n"
                f"Rounds : {self.round_ids}\n"
                f"Players : {self.player_ids}\n")

    def serialize(self):
        return {
            "name": self.name,
            "location": self.location,
            "start_date": self.start_date.strftime("%d/%m/%Y"),
            "end_date": self.end_date.strftime("%d/%m/%Y"),
            "description": self.description,
            "rounds": self.round_ids,
            "players": self.player_ids,
            "status": self.status.name
        }

    @classmethod
    def deserialize(cls, data):
        start_date = datetime.strptime(data['start_date'], "%d/%m/%Y")
        end_date = datetime.strptime(data['end_date'], "%d/%m/%Y")
        return cls(data["name"],
                   data["location"],
                   start_date,
                   end_date,
                   data["description"],
                   data.get('rounds', []),
                   data.get('players', []),
                   )


class RoundStatus(Enum):
    """
    This class represents the status of a round.
    """
    PENDING = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()


class Round:
    """
    This class represent a round
    """

    def __init__(self,
                 tournament_id,
                 match_ids=None,
                 player_ids=None,
                 matches=None,
                 start_date="To be defined",
                 end_date="To be defined",
                 status=RoundStatus.PENDING,
                 doc_id=None):
        self.doc_id = doc_id
        self.tournament_id = tournament_id
        self.matches = matches if matches is not None else []  # list of matches of current round
        self.match_ids = []  # will contain match ids for the round
        self.start_date = start_date
        self.end_date = end_date
        self.player_ids = []  # will contain player_ids who play for that round
        self.status = RoundStatus.PENDING  # initial state of the round

    def __str__(self):
        return (f"round_id : {self.doc_id}\n"
                f"tournament_id : {self.tournament_id}\n"
                f"match_ids : {self.match_ids}\n"
                f"player_ids : {self.player_ids}\n"
                f"matches : {self.matches}\n"
                f"start_date : {self.start_date}\n"
                f"end_date : {self.end_date}\n"
                f"status : {self.status.name}\n")

    def serialize(self):
        return {
            "tournament_id": self.tournament_id,
            "match_ids": self.match_ids,
            "player_ids": self.player_ids,
            "matches": self.matches,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "status": self.status.name
        }

    @classmethod
    def deserialize(cls, data):
        status = RoundStatus[data["status"]]
        return cls(tournament_id=data['tournament_id'],
                   match_ids=data.get('match_ids', []),
                   player_ids=data.get('player_ids', []),
                   matches=data.get('matches', []),
                   start_date=data.get('start_date, []'),
                   end_date=data.get('end_date', []),
                   status=status
                   )


class Match:
    """
    This class represent a match
    """

    def __init__(self,
                 round_id,
                 player1_id,
                 player2_id,
                 winner=None,
                 match_id=None,
                 score=None):
        self.match_id = match_id
        self.round_id = round_id
        self.player1_id = player1_id
        self.player2_id = player2_id
        self.winner = None
        self.score = None

    def __str__(self):
        return (f"round_id : {self.round_id}\n"
                f"match_id : {self.match_id}\n"
                f"player1_id : {self.player1_id}\n"
                f"player2_id : {self.player2_id}\n"
                f"winner : {'None' if self.winner is None else self.winner}\n")

    def serialize(self):
        return {
            "round_id": self.round_id,
            "match_id": self.match_id,
            "player1_id": self.player1_id,
            "player2_id": self.player2_id,
            "winner": self.winner
        }

    @classmethod
    def deserialize(cls, data):
        match_id = data.doc_id
        return cls(data['round_id'],
                   data['player1_id'],
                   data['player2_id'],
                   data['winner'],
                   match_id=match_id)


class Player:
    """
    This class represent a player
    """

    def __init__(self,
                 first_name,
                 last_name,
                 gender,
                 birthday,
                 chess_id,
                 tournament_id=None,
                 score=0,
                 doc_id=None,
                 ):
        self.doc_id = doc_id
        self.tournament_id = tournament_id
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birthday = birthday
        self.chess_id = chess_id
        self.score = score

    def __str__(self):
        return (f"player_id : {self.doc_id}\n"
                f"first_name : {self.first_name}\n"
                f"last_name : {self.last_name}\n"
                f"gender : {self.gender}\n"
                f"birthday : {self.birthday.strftime('%d/%m/%Y')}\n"
                f"chess_id : {self.chess_id}\n"
                f"score : {self.score}\n"
                )

    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "gender": self.gender,
            "birthday": self.birthday,
            "chess_id": self.chess_id,
            "score": self.score
        }

    @classmethod
    def deserialize(cls, data):
        player_id = data.doc_id
        return cls(data['first_name'],
                   data['last_name'],
                   data['gender'],
                   data['birthday'],
                   data['chess_id'],
                   data['score'],
                   doc_id=data.doc_id)
