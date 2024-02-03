class Tournament:
    """
    This class represent a tournament
    """
    def __init__(
            self,
            name, location,
            start_date, end_date,
            current_round_id, rounds,
            players, description,
            round_number=4):

        self.name = name
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.round_number = round_number
        self.current_round_id = current_round_id
        self.rounds = rounds
        self.players = players
        self.description = description

    def add_player(self):
        pass

    def remove_player(self):
        pass

    def start_round(self):
        pass

    def __str__(self):
        return (
            f"Tournament: {self.name}",
            f"Location: {self.location}",
            f"Start Date: {self.start_date}",
            f"End Date: {self.end_date}",
            f"Round: {self.rounds}",
            f"Current Round ID: {self.current_round_id}",
            f"Players: {self.players}",
        )


class Player:
    """
    This class represent a Player
    """
    player_count = 0 #will be used for a unique player_id
    def __init__(self, first_name, last_name, birthdate, chess_id, score=0):
        Player.player_count += 1  # everytime a player is created
        self.player_id = Player.player_count
        self.first_name = first_name
        self.last_name = last_name
        self.birthdate = birthdate
        self.score = score
        self.chess_id = chess_id  # Two letters followed by five digits

    def update_score(self, points):
        """
        This will update the player's score :
        win : 1 point
        square : 0.5 point
        defeat : 0 point
        """
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

    def to_json(self):
        """
        Add the player data to json
        """
        pass


class Round:
    """
    This class represent a round
    """
    def __init__(self, current_round_id, matches, is_complete, round_number=4):
        self.round_number = round_number
        self.matches = matches
        self.is_complete = is_complete
        self.current_round_id = current_round_id

    def add_match(self, match):
        """
        Add a match to the list of matches for the round
        :param match:
        :return:
        """
        pass

    def finalize_round(self):
        """
        Change the value of is_complete to True when a round is complete
        :return:
        """
        pass

    def get_round_results(self):
        """
        Get the results of all matches of this round
        :return:
        """
        pass

    def to_json(self):
        """
        Add the round data to Json
        :return:
        """
        pass

    def __str__(self):
        return f"Round Number: {self.round_number}, Matches: {self.matches}, Status: {self.is_complete}"


class Match:
    """
    This class represent a Match
    """

    def __init__(self, match_id, player1, player2, match_result):
        self.match_id = match_id
        self.player1 = player1
        self.player2 = player2
        self.match_result = match_result

    def set_result(self):
        """
        Method for setting the result of a match
        :return:
        """
        pass

    def get_winner(self):
        """
        Method to get who is the winner of the match
        :return:
        """
        pass

    def to_json(self):
        """
        Add the match data to Json
        :return:
        """

    def __str__(self):
        return (
            f"Match ID : {self.match_id}, "
            f"Player 1: {self.player1}, "
            f"Player2: {self.player2}, "
            f"Match Results: {self.match_result}",
        )