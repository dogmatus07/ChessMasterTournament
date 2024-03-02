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
        self.db_manager.add_tournament(tournament_serialized)

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
        if not tournament:
            self.view.display_error_message()
            return

        self.add_players_to_tournament(tournament_choice)

        self.view.clear_screen()
        self.view.display_tournament_details(tournaments)
        self.view.press_any_key_to_continue()

        """
        # start first round
        self.view.clear_screen()
        self.back_to_main_menu()
        """

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

        # prepare first round and matches
        self.prepare_and_start_first_round(tournament_id)

    def prepare_and_start_first_round(self, tournament_id):
        player_ids = self.db_manager.get_tournament_players(tournament_id)
        print(f"Player IDs: {player_ids}")
        time.sleep(10)

        random.shuffle(player_ids)

        matches = []

        for i in range(0, len(player_ids), 2):
            player1_id = player_ids[i]
            player2_id = player_ids[i + 1]

            # get players infos
            player1 = self.db_manager.get_player(player1_id)
            player2 = self.db_manager.get_player(player2_id)

            # names
            player1_name = player1['first_name'] if player1 else "Inconnu"
            player2_name = player2['first_name'] if player2 else "Inconnu"

            # match creation
            match = Match(round_id=1, player1_id=player1_id, player2_id=player2_id)
            match_id = self.db_manager.add_match(
                match.serialize())

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
                                          {'current_round': 1, 'status': TournamentStatus.IN_PROGRESS.name})

        # update round status
        round_id = 1
        self.db_manager.update_round(round_id, {'matches': matches, 'status': RoundStatus.IN_PROGRESS.name})

        # display matches
        self.view.display_all_first_round_matches(matches)

        # ask scores for those matches
        self.view.press_any_key_to_continue()

    def manage_rounds(self):
        self.view.clear_screen()
        self.back_to_main_menu()

    def create_rounds(self, tournament_id):
        print("create rounds initiated")
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
        time.sleep(3)
        # create 4 rounds
        rounds_created = []
        for i in range(1, 5):
            round_data = Round(round_id=i, tournament_id=tournament_id)
            round_created = self.db_manager.get_round(round_id=i)
            rounds_created.append(round_created)
            round_serialized = round_data.serialize()
            self.db_manager.add_round(round_serialized)

        # update tournament to store its rounds
        self.db_manager.update_tournament(tournament_id, {'rounds': rounds_created})

        time.sleep(2)
        self.view.display_success_message()
        rounds_created = self.db_manager.list_rounds(tournament_id)
        self.view.display_list_of_rounds(rounds_created)

    def create_matches(self, round_id):
        pass

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

    def resume_rounds(self):
        pass

    def check_tournament_players(self, tournament_id):
        players = self.db_manager.get_tournament_players(tournament_id)
        if len(players) != 8:
            self.view.display_not_suffisant_players()
            return False
        return True

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

    def create_round(self, tournament_id):
        pass

    def start_round(self, round_id):
        pass

    def end_round(self, round_id):
        pass

    def list_rounds(self, tournament_id):
        pass

    def generate_round_matches(self, tournament_id, round_id):
        pass

    """
    MATCH MANAGEMENT
    """

    def create_match(self, round_id, player1_id, player2_id):
        pass

    def list_matches(self, round_id):
        pass

    def set_match(self, match_id, winner_id):
        pass

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
            self.db_manager.add_player(player_serialized)

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

    def calculate_player_score(self, tournament_id):
        pass
