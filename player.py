class Player:
    """
    This class represent a Player
    """

    def __init__(self, fname, lname, birthdate, chess_id, score=0):
        self.fname = fname
        self.lname = lname
        self.birthdate = birthdate
        self.score = score
        self.chess_id = chess_id  # Two letters followed by five digits

    """
    Methods for Player
    """

    def update_score(self, points):
        """
        This will update the player's score :
        win : 1 point
        square : 0.5 point
        defeat : 0 point
        """
        self.score += points

    def to_json(self):
        """
        Add the player data to json
        :return:
        """
        pass