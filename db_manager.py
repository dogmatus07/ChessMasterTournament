from tinydb import TinyDB, Query


class DatabaseManager:

    def __init__(self, path="data/tournaments/db.json"):
        self.db = TinyDB(path)
        self.tournament_table = self.db.table("tournament")
        self.round_table = self.db.table("round")
        self.match_table = self.db.table("match")
        self.player_table = self.db.table("player")

    """
    Add Methods
    """

    def add_tournament(self, tournament):
        tournament_id = self.tournament_table.insert(tournament)
        return tournament_id

    def add_round(self, round_data):
        round_id = self.round_table.insert(round_data)
        return round_id

    def add_match(self, match):
        match_id = self.match_table.insert(match)
        return match_id

    def add_player(self, player_data):
        player_id = self.player_table.insert(player_data)
        return player_id

    """
    Get Methods
    """

    def get_tournament(self, tournament_id):
        tournament_id = int(tournament_id)
        tournament = self.tournament_table.get(doc_id=tournament_id)
        return tournament

    def get_round(self, round_id):
        round = self.round_table.get(doc_id=round_id)
        return round

    def get_match(self, match_id):
        match = self.match_table.get(doc_id=match_id)
        return match

    def get_player(self, player_id):
        player = self.player_table.get(doc_id=player_id)
        return player

    """
    Update Methods
    """

    def update_tournament(self, tournament_id, tournament):
        self.tournament_table.update(tournament, doc_ids=[tournament_id])

    def update_round(self, round_id, round):
        self.round_table.update(round, doc_ids=[round_id])

    def update_match(self, match_id, match):
        self.match_table.update(match, doc_ids=[match_id])

    def update_player(self, player_id, player):
        self.player_table.update(player, doc_ids=[player_id])

    def increment_player_score(self, player_id, increment):
        player = self.get_player(player_id)
        if player is not None:
            new_score = player['score'] + increment
            self.update_player(player_id, {'score': new_score})

    def update_match_winner(self, match_id, winner_id):
        self.match_table.update({'winner': winner_id}, doc_ids=[match_id])

        # update matches in round table
        udpated_match = self.match_table.get(doc_id=match_id)
        round_id = udpated_match['round_id']

        round_item = self.round_table.get(doc_id=round_id)
        updated_matches = []

        for match in round_item['matches']:
            if match['match_id'] == match_id:
                match['winner'] = winner_id
            updated_matches.append(match)

        # save to database
        self.round_table.update({'matches': updated_matches}, doc_ids=[round_id])

    def update_round_matches(self, round_id, matches, tournament_id):
        self.round_table.update(
            {'matches': matches},
            doc_ids=[round_id]
        )
        self.tournament_table.update(
            {'current_round': round_id},
            doc_ids=[tournament_id]
        )

    """
    Delete Methods
    """

    def delete_tournament(self, tournament_id):
        self.tournament_table.remove(doc_ids=[tournament_id])

    def delete_round(self, round_id):
        self.round_table.remove(doc_ids=[round_id])

    def delete_match(self, match_id):
        self.match_table.remove(doc_ids=[match_id])

    def delete_player(self, player_id):
        self.player_table.remove(doc_ids=[player_id])

    """
    List & Display methods
    """

    def list_tournaments(self):
        return self.tournament_table.all()

    def list_rounds(self, tournament_id):
        query = Query()
        rounds = self.round_table.search(query.tournament_id == tournament_id)
        return rounds

    def list_matches(self, round_id):
        query = Query()
        matches = self.match_table.search(query.round_id == round_id)
        return matches

    def list_all_matches(self, tournament_id):
        all_matches = self.match_table.search(
            Query().tournament_id == tournament_id)
        return all_matches

    def list_players(self):
        return self.player_table.all()

    def get_tournament_players(self, tournament_id):
        tournament = self.tournament_table.get(doc_id=tournament_id)
        if tournament:
            player_ids = tournament.get('players', [])
            return player_ids
        return []

    def get_player_chess_id(self, player_id):
        player = self.player_table.get(doc_id=player_id)
        if player:
            return player['chess_id']
        return "N/A"
