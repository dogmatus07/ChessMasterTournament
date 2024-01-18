class Round:
    """
    This class represent a round
    """
    def __init__(self,current_round_id, matches, is_complete, round_number=4):
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
