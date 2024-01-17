class Player:
    """
    This class represent a Player
    """

    def __init__(self, first_name, last_name, birthdate, chess_id, score=0):
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
        return f"Player : {self.first_name} {self.last_name}, Birth Date : {self.birthdate}, Chess ID : {self.chess_id}, Score : {self.score}"

    def to_json(self):
        """
        Add the player data to json
        """
        pass