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
