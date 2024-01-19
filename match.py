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

