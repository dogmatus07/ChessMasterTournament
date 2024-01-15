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
        return f"Player : {self.fname} {self.lname}, Birth Date : {self.birthdate}, Chess ID : {self.chess_id}, Score : {self.score}"

    def to_json(self):
        """
        Add the player data to json
        :return:
        """
        pass