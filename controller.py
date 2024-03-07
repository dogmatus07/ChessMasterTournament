from datetime import datetime
from os import name
import random
import time
from enum import Enum, auto
from tinydb import TinyDB, Query
from rich.padding import PaddingDimensions

from db_manager import DatabaseManager
from models import Player, Tournament, Match, Round, RoundStatus, TournamentStatus
from view import View


class Controller:

    def __init__(self) -> None:
        self.view = View()
        self.current_tournament = None
        self.db_manager = DatabaseManager()
        self.menu_actions = {
            1: self.create_tournament,
            2: self.add_participants,
            3: self.launch_tournament,
            4: self.manage_rounds,
            5: self.manage_players,
            6: self.show_reports,
            7: self.exit_app
        }

    """
    MAIN LOOP
    """

    def main_loop(self):
        self.view.clear_screen()
        self.view.app_main_menu()
        try:
            main_menu_choice = self.view.ask_menu_choice()
            action = self.menu_actions.get(main_menu_choice)
            if action:
                action()
            else:
                self.view.display_error_message()
        except ValueError:
            self.view.display_error_message()

    def create_tournament(self):
        self.view.clear_screen()
        # create instance of tournament
        tournament_datas = self.view.get_tournament_infos()
        tournament = Tournament(name=tournament_datas[0],
                                location=tournament_datas[1],
                                start_date=tournament_datas[2],
                                end_date=tournament_datas[3],
                                description=tournament_datas[4])

        # serialize tournament

        tournament_serialized = tournament.serialize()

        # add to the database
        doc_id = self.db_manager.add_tournament(tournament_serialized)

        # update the tournament_id with the doc_id by TinyDB
        self.db_manager.update_tournament(doc_id, {'tournament_id': doc_id})

        # display success message and table of tournaments
        self.view.clear_screen()
        new_tournament = self.db_manager.list_tournaments()
        self.view.display_tournament_list(new_tournament)
        self.view.display_success_message()
        time.sleep(3)
        self.main_loop()

    def add_participants(self):
        self.view.clear_screen()
        tournaments = self.db_manager.list_tournaments()
        self.view.display_tournament_list(tournaments)

        # ask user to choose tournament
        tournament_choice = int(self.view.ask_tournament_id())

        # check if tournament exist
        tournament = self.db_manager.get_tournament(tournament_choice)
        if tournament:
            tournament['doc_id'] = tournament_choice
            self.add_players_to_tournament(tournament_choice)
            self.view.clear_screen()
            self.view.display_tournament_details(tournament)
            self.view.press_any_key_to_continue()
            self.back_to_main_menu()

        else:
            self.view.display_error_message()

    def launch_tournament(self):
        self.view.clear_screen()
        tournaments = self.db_manager.list_tournaments()
        self.view.display_tournament_list(tournaments)

        # ask user to choose tournament
        tournament_id = self.view.ask_tournament_id()

        # check if tournament exist and players are 8
        tournament = self.db_manager.get_tournament(tournament_id)
        if not tournament or len(tournament['players']) < 8:
            self.view.display_error_message()
            return

        # create all rounds for the tournament
        self.create_rounds(tournament_id)

        # launch rounds and matches
        tournament = self.db_manager.get_tournament(tournament_id)
        round_list = tournament['rounds']

        for round_number in round_list:
            if round_number == round_list[0]:
                self.prepare_and_start_first_round(tournament_id)
            else:
                if self.view.ask_start_next_round(tournament_id, round_number):
                    self.prepare_next_round(tournament_id, round_number)
                    self.db_manager.update_round(round_number, {'status': RoundStatus.FINISHED.name})
                else:
                    break

    def prepare_next_round(self, tournament_id, round_number):
        sorted_players = self.get_sorted_players_by_scores(tournament_id)
        self.view.display_tournament_stats(sorted_players)
        self.view.press_any_key_to_continue()
        pairings = self.generate_pairings(sorted_players, tournament_id, round_number)
        matches = self.save_round_matches(pairings, round_number, tournament_id)
        self.display_match_infos(round_number, matches)
        self.view.press_any_key_to_continue()
        self.ask_match_results(tournament_id, matches, round_number)

    def display_match_infos(self, round_id, matches):
        matches_infos_display = []
        for match in matches:
            player1 = self.db_manager.get_player(match['player1_id'])
            player2 = self.db_manager.get_player(match['player2_id'])
            match_infos = {
                'match_id': match['match_id'],
                'player1_chess_id': player1['chess_id'],
                'player1_name': f"{player1['first_name']} {player1['last_name']}",
                'player2_chess_id': player2['chess_id'],
                'player2_name': f"{player2['first_name']} {player2['last_name']}"
            }
            matches_infos_display.append(match_infos)
        self.view.display_matches(round_id, matches_infos_display)

    def get_sorted_players_by_scores(self, tournament_id):
        players_ids = self.db_manager.get_tournament_players(tournament_id)
        players = [self.db_manager.get_player(player_id) for player_id in players_ids]
        sorted_players = sorted(players, key=lambda x: (-x['score'], x['first_name'], x['last_name']))
        return sorted_players

    def generate_pairings(self, sorted_players, tournament_id, round_number):
        previous_matches = self.db_manager.list_all_matches(tournament_id)
        pairings = []
        used_players = set()

        for player in sorted_players:
            if player['player_id'] in used_players:
                continue # player already paired

            for opponent in sorted_players:
                if opponent['player_id'] in used_players or opponent['player_id'] == player['player_id']:
                    continue # bypass if player has already been used or equal the same player

                if not self.players_have_met(player['player_id'], opponent['player_id'], previous_matches):
                    pairings.append((player['player_id'], opponent['player_id']))
                    used_players.update([player['player_id'], opponent['player_id']])
                    break
        return pairings

    def save_round_matches(self, pairings, round_number, tournament_id):
        matches_infos = []
        for player1_id, player2_id in pairings:
            player1 = self.db_manager.get_player(player1_id)
            player2 = self.db_manager.get_player(player2_id)
            player1_name = f"{player1['first_name']} {player1['last_name']}"
            player2_name = f"{player2['first_name']} {player2['last_name']}"
            match_data = {
                'round_id': round_number,
                'player1_id': player1_id,
                'player2_id': player2_id,
                'player1_name': player1_name,
                'player2_name': player2_name,
                'winner': None
            }
            match_id = self.db_manager.add_match(match_data)
            match_data['match_id'] = match_id
            matches_infos.append(match_data)

        self.db_manager.update_round_matches(round_number, matches_infos, tournament_id)
        self.db_manager.update_round(round_number,
                                     {'status': RoundStatus.IN_PROGRESS.name})
        return matches_infos

    def prepare_and_start_first_round(self, tournament_id):
        player_ids = self.db_manager.get_tournament_players(tournament_id)
        print("Appariement des joueurs pour le ROUND 1")
        time.sleep(2)
        random.shuffle(player_ids)

        matches = []

        for i in range(0, len(player_ids), 2):
            player1_id = player_ids[i]
            player2_id = player_ids[i + 1]

            # get players infos
            player1 = self.db_manager.get_player(player1_id)
            player2 = self.db_manager.get_player(player2_id)

            # names
            player1_name = f"{player1['first_name']} {player1['last_name']}" if player1 else "Inconnu"
            player2_name = f"{player2['first_name']} {player2['last_name']}" if player2 else "Inconnu"

            # match creation
            match = Match(round_id=1, player1_id=player1_id, player2_id=player2_id)
            match_id = self.db_manager.add_match(
                match.serialize())
            match.match_id = match_id

            # update database
            self.db_manager.update_match(match_id, match.serialize())

            # match info to display
            match_info = {
                'match_id': match_id,
                'player1_id': player1_id,
                'player2_id': player2_id,
                'player1_name': player1_name,
                'player2_name': player2_name,
            }
            matches.append(match_info)

        # update tournament status
        self.db_manager.update_tournament(tournament_id,
                                          {'current_round': 1,
                                           'status': TournamentStatus.IN_PROGRESS.name
                                           })

        # update round status
        round_id = 1
        self.db_manager.update_round(round_id, {'matches': matches, 'status': RoundStatus.IN_PROGRESS.name})

        # display matches
        self.display_match_infos(round_id, matches)

        # ask scores for those matches
        self.view.press_any_key_to_continue()
        self.ask_match_results(tournament_id, matches, round_id)
        self.display_tournament_stats(tournament_id)

        # update round status after all matches are done
        self.db_manager.update_round(round_id, {'status': RoundStatus.FINISHED.name})
        self.view.press_any_key_to_continue()

    def ask_match_results(self, tournament_id, matches, round_id):
        for match in matches:
            winner_choice = self.view.ask_match_result(match, round_id)
            if winner_choice == 1:
                winner_id = match['player1_id']
            elif winner_choice == 2:
                winner_id = match['player2_id']
            else: # draw
                winner_id = None
            match['winner'] = winner_id
            self.update_player_scores(match['player1_id'], match['player2_id'], winner_id)
            self.db_manager.update_match_winner(match['match_id'], winner_id)

    def update_player_scores(self, player1_id, player2_id, winner):
        if winner == player1_id:
            self.db_manager.increment_player_score(player1_id, 1)
            self.db_manager.increment_player_score(player2_id, 0)
        elif winner == player2_id:
            self.db_manager.increment_player_score(player2_id, 1)
            self.db_manager.increment_player_score(player1_id, 0)
        else:
            self.db_manager.increment_player_score(player1_id, 0.5)
            self.db_manager.increment_player_score(player2_id, 0.5)

    def display_tournament_stats(self, tournament_id):
        player_ids = self.db_manager.get_tournament_players(tournament_id)
        players = [self.db_manager.get_player(player_id) for player_id in player_ids]

        # sort players by score
        sorted_players = sorted(players, key=lambda x: (-x['score'], x['first_name'] + " " + x['last_name']))

        # display_stats
        self.view.display_tournament_stats(sorted_players)

    def get_current_tournament(self):
        tournaments = self.db_manager.list_tournaments()
        for tournament in tournaments:
            if tournament['status'] == 'IN_PROGRESS':
                return tournament

    def get_current_round(self, tournament_id):
        rounds = self.db_manager.list_rounds(tournament_id)
        for round_item in rounds:
            if round_item['status'] == 'IN_PROGRESS':
                return round_item
        return None
    """
    def start_next_round(self, tournament_id):
        current_round = self.get_current_round(tournament_id)
        if current_round and current_round['status'] == 'PENDING':
            players = self.get_sorted_players(tournament_id)
            previous_matches = self.get_previous_matches(tournament_id)
            matches = []

            for i in range(0, len(players), 2):
                player1 = players[i]
                player2 = players[i+1]

                if not self.players_have_met(player1['player1_id'], player2['player2_id'], previous_matches):
                    matches_data = Match(
                        round_id=current_round['round_id'],
                        player1_id=player1['player1_id'],
                        player2_id=player2['player2_id']
                    )
                    matches.append(matches_data)
                else:
                    print("ces joueurs se sont déjà affrontés")

            # update database
            self.db_manager.update_round(current_round['round_id'], {'status': 'IN_PROGRESS', 'matches': matches})
        else:
            print("aucun round supplémentaire à démarrer")
    """
    """
    def get_sorted_players(self, tournament_id):
        players = self.db_manager.get_tournament_players(tournament_id)
        sorted_players = sorted(players, key=lambda x: (-x['score'], x['first_name'] + " " + x['last_name']))
        return sorted_players

    def get_previous_matches(self, tournament_id):
        rounds = self.db_manager.list_rounds(tournament_id)
        previous_matches = []
        for round_item in rounds:
            for match_id in round_item['matches']:
                match = self.db_manager.get_match(match_id)
                if match:
                    previous_matches.append(match)
        return previous_matches
    
    """

    def players_have_met(self, player1_id, player2_id, previous_matches):
        for match in previous_matches:
            # Assuming match structure contains player IDs as 'player1_id' and 'player2_id'
            players = [match['player1_id'], match['player2_id']]
            if player1_id in players and player2_id in players:
                return True
        return False

    def manage_rounds(self):
        self.view.clear_screen()
        self.back_to_main_menu()

    def create_rounds(self, tournament_id):
        # check if tournament exist
        tournament = self.db_manager.get_tournament(tournament_id)
        if not tournament:
            self.view.display_error_message()
            return

        # check if rounds exists and not >4
        rounds = self.db_manager.list_rounds(tournament_id)
        if len(rounds) > 4:
            print("Nombre de rounds maximum atteint")
            time.sleep(2)
            self.back_to_main_menu()

        # display round operation
        self.view.display_round_creation()
        time.sleep(1)
        # create 4 rounds
        rounds_created = []
        for i in range(1, 5):
            round_data = Round(tournament_id=tournament_id)
            round_serialized = round_data.serialize()
            round_id = self.db_manager.add_round(round_serialized)
            rounds_created.append(round_id)
        print(rounds_created)
        time.sleep(1)
        # update tournament to store its rounds
        self.db_manager.update_tournament(tournament_id, {'rounds': rounds_created})

        time.sleep(1)
        self.view.display_success_message()
        rounds_created = self.db_manager.list_rounds(tournament_id)
        self.view.display_list_of_rounds(rounds_created)

    """
    def start_rounds(self, tournament_id):
        # get all registered players for the tournament
        tournament = self.db_manager.get_tournament(tournament_id)
        player_ids = tournament.get('players', [])

        # random shuffle players for first round
        random.shuffle(player_ids)

        # get list of matches for this round
        matches = [(player_ids[i], player_ids[i + 1])
                   for i in range(0, len(player_ids), 2)]

        # create matches
        match_ids = []

        for player1_id, player2_id in matches:
            match = Match(round_id=1, player1_id=player1_id,
                          player2_id=player2_id).serialize()

            match_id = self.db_manager.add_match(match)
            match_ids.append(match_id)

        # update the first round with the matches

        round_data = {
            'tournament_id': tournament_id,
            'matche_ids': match_ids,
            'player_ids': player_ids,
            'status': RoundStatus.IN_PROGRESS
        }

        # update db
        self.db_manager.update_round(1, round_data)
        self.db_manager.update_tournament(tournament_id, {
            'current_round_id': 1,
            'status': TournamentStatus.IN_PROGRESS
        })
    """

    def manage_players(self):
        self.view.clear_screen()
        player_menu_actions = {
            1: self.register_player,
            2: self.list_players,
            3: self.delete_player,
            4: self.update_player,
            5: self.back_to_main_menu
        }

        while True:
            self.view.clear_screen()
            self.view.app_menu_players()
            player_menu_choice = int(self.view.ask_menu_choice())
            action = player_menu_actions.get(player_menu_choice)
            if action:
                action()
            else:
                self.view.display_error_message()

    def back_to_main_menu(self):
        self.view.clear_screen()
        self.main_loop()

    def show_reports(self):
        pass

    def exit_app(self):
        self.view.clear_screen()
        exit()

    """
    SELECT TOURNAMENT TO VIEW DETAILS
    """
    """
    self.view.clear_screen()
    tournaments = self.db_manager.list_tournaments()
    self.view.display_tournament_list(tournaments)
    user_choice = self.view.ask_tournament_id()
    self.view.clear_screen()
    self.current_tournament = self.db_manager.get_tournament(user_choice)
    self.view.display_tournament_details(self.current_tournament)
    """
    """
    UPDATE TOURNAMENT
    """
    """
    self.view.clear_screen()
    tournaments = self.db_manager.list_tournaments()
    self.view.display_tournament_list(tournaments)
    user_choice = self.view.ask_tournament_id()
    self.view.clear_screen()
    self.update_tournament(user_choice)
    """
    """
    DELETE TOURNAMENT
    """
    """
    self.view.clear_screen()
    tournament_list = self.db_manager.list_tournaments()
    self.view.display_tournament_list(tournament_list)
    tournament_id = self.view.ask_delete_tournament()
    self.delete_tournament(tournament_id)
    """
    """
    TOURNAMENT MANAGEMENT
    """

    def update_tournament(self, tournament_id):
        tournament_id = int(tournament_id)
        tournament = self.db_manager.get_tournament(tournament_id)

        if tournament:
            # display the actual values and ask for new ones
            self.view.display_tournament_details(tournament)
            updated_data = self.view.ask_tournament_infos_update()

            # update the tournament infos
            # tournament.update(updated_data)

            # save to database
            self.db_manager.update_tournament(tournament_id, updated_data)

            # display success message
            self.view.clear_screen()
            self.view.display_success_message()

            # show the list of tournament inside database after update
            updated_tournament = self.db_manager.list_tournaments()
            self.view.display_tournament_list(updated_tournament)

        else:
            self.view.display_error_message()

    def delete_tournament(self, tournament_id):
        self.view.clear_screen()
        tournament_id = int(tournament_id)
        tournament = self.db_manager.get_tournament(tournament_id)
        if not tournament:
            self.view.display_error_message()
            return

        # display the details of the tournament to delete
        self.view.display_tournament_details(tournament)

        # confirm deletion
        user_choice = self.view.ask_confirmation_deletion()

        if user_choice.lower() == "o":
            self.db_manager.delete_tournament(tournament_id)
            self.view.display_success_message()
        else:
            self.view.display_error_message()

        all_tournaments = self.db_manager.list_tournaments()
        self.view.display_tournament_list(all_tournaments)

    def list_tournaments(self):
        tournaments = self.db_manager.list_tournaments()
        self.view.display_tournament_list(tournaments)

    """
    ROUND MANAGEMENT
    """
    def end_round(self, round_id):
        self.db_manager.update_round(round_id, {'status': RoundStatus.FINISHED.name})

    """
    PLAYER MANAGEMENT
    """

    def register_player(self):
        self.view.clear_screen()
        while True:
            # get player infos
            player_infos = self.view.get_player_infos()

            # create instance of a player
            player = Player(*player_infos)

            # serialize player
            player_serialized = player.serialize()

            # add player to database
            doc_id = self.db_manager.add_player(player_serialized)

            # update the player_id with the doc_id by TinyDB
            self.db_manager.update_player(doc_id, {'player_id': doc_id})

            # display success message
            self.view.display_success_message()
            another_player_choice = self.view.ask_create_another_player()
            if another_player_choice != 1:
                break

        self.manage_players()

    def add_players_to_tournament(self, tournament_id):
        self.view.clear_screen()
        tournament = self.db_manager.get_tournament(tournament_id)
        if not tournament:
            self.view.display_error_message()
            return

        # self.view.display_tournament_details(tournament)

        # initialize list of registered players
        registered_players = set()

        while len(registered_players) < 8:
            all_players = self.db_manager.list_players()
            # filter out already registered players
            available_players = [
                player for player in all_players
                if player.doc_id not in registered_players
            ]
            self.view.display_player_list(available_players)

            try:
                player_id_int = int(self.view.ask_player_id())
                if player_id_int in registered_players:
                    self.view.display_error_message()
                    continue

                player_data = self.db_manager.get_player(player_id_int)
                if player_data:
                    self.register_player_to_tournament(tournament_id, player_id_int)
                    registered_players.add(player_id_int)
                    self.view.display_success_message()
                else:
                    self.view.display_error_message()
            except ValueError:
                self.view.display_error_message()

        self.db_manager.update_tournament(tournament_id,
                                          {'players': list(registered_players)})

    def register_player_to_tournament(self, tournament_id, player_id):
        # tournament infos
        tournament_data = self.db_manager.get_tournament(tournament_id)
        if not tournament_data:
            print("Tournoi non trouvé.")
            return

        # check and update players list
        players_list = tournament_data.get('players', [])

        if player_id not in players_list:
            players_list.append(player_id)

            # update tournament with new players list
            self.db_manager.tournament_table.update({'players': players_list},
                                                    doc_ids=[tournament_id])
            # update players with tournament_id
            self.db_manager.player_table.update({'tournament_id': tournament_id},
                                                doc_ids=[player_id])
        else:
            print("Le joueur est déjà inscrit dans le tournoi.")

    def update_player(self, player_id):
        pass

    def list_players(self):
        all_players = self.db_manager.list_players()
        self.view.clear_screen()
        self.view.display_player_list(all_players)
        self.view.press_any_key_to_continue()

    def delete_player(self, player_id):
        pass
