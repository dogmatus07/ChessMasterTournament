import random
import time
from datetime import datetime

from db_manager import DatabaseManager
from models import (
    Player, Tournament, Match,
    Round, RoundStatus, TournamentStatus
)
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
                self.view.clear_screen()
                self.view.display_error_message()
                self.view.press_any_key_to_continue()
                self.back_to_main_menu()

        except ValueError:
            self.view.clear_screen()
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
        self.view.press_any_key_to_continue()
        self.back_to_main_menu()

    def add_participants(self):
        self.view.clear_screen()
        tournaments = self.db_manager.list_tournaments()
        self.view.display_tournament_list(tournaments)

        # ask user to choose tournament
        tournament_choice = int(self.view.ask_id())

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
        tournament_id = self.view.ask_id()

        # check if tournament exist and players are 8
        tournament = self.db_manager.get_tournament(tournament_id)
        if not tournament or len(tournament['players']) < 8:
            self.view.clear_screen()
            self.view.display_error_message()
            self.view.press_any_key_to_continue()
            self.back_to_main_menu()
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
                start_date = self.round_start_date(round_number)
                end_date = self.round_end_date(round_number)
                self.db_manager.update_round(round_number, {'start_date': start_date})
                self.prepare_next_round(tournament_id, round_number)
                self.round_end_date(round_number)
                self.db_manager.update_round(
                    round_number,
                    {'status': RoundStatus.FINISHED.name, 'end_date': end_date})

        # if all rounds are finished, update tournament status
        all_rounds_finished = all(
            self.db_manager.get_round(round_id)['status'] == RoundStatus.FINISHED.name for round_id in round_list)
        if all_rounds_finished:
            self.db_manager.update_tournament(tournament_id, {'status': TournamentStatus.FINISHED.name})
            self.view.message_tournament_finished()
            self.view.press_any_key_to_continue()
            self.back_to_main_menu()

    def prepare_next_round(self, tournament_id, round_number):
        sorted_players = self.get_sorted_players_by_scores(tournament_id)
        pairings = self.generate_pairings(
            sorted_players,
            tournament_id,
            round_number
        )
        matches = self.save_round_matches(
            pairings,
            round_number,
            tournament_id
        )
        self.display_match_infos(round_number, matches)
        self.view.press_any_key_to_continue()
        self.ask_match_results(tournament_id, matches, round_number)

    def display_match_infos(self, round_id, matches):
        matches_infos_display = []
        for match in matches:
            player1 = self.db_manager.get_player(match['player1_id'])
            player2 = self.db_manager.get_player(match['player2_id'])
            player1_fname = f"{player1['first_name']} {player1['last_name']}"
            player2_fname = f"{player2['first_name']} {player2['last_name']}"
            match_infos = {
                'match_id': match['match_id'],
                'player1_chess_id': player1['chess_id'],
                'player1_name': player1_fname,
                'player2_chess_id': player2['chess_id'],
                'player2_name': player2_fname
            }
            matches_infos_display.append(match_infos)
        self.view.display_matches(round_id, matches_infos_display)

    def get_sorted_players_by_scores(
            self,
            tournament_id):
        players_ids = self.db_manager.get_tournament_players(tournament_id)

        players = []
        for player_id in players_ids:
            player = self.db_manager.get_player(player_id)
            players.append(player)

        sorted_players = sorted(
            players,
            key=lambda x: (-x['score'], x['first_name'], x['last_name']))
        return sorted_players

    def generate_pairings(self, sorted_players, tournament_id, round_number):
        previous_matches = self.db_manager.list_all_matches(tournament_id)
        pairings = []
        used_players = set()

        for player in sorted_players:
            if player['player_id'] in used_players:
                continue  # player already paired

            for opponent in sorted_players:
                if opponent['player_id'] in used_players or \
                        opponent['player_id'] == player['player_id']:
                    continue

                if not self.players_have_met(
                        player['player_id'],
                        opponent['player_id'],
                        previous_matches):
                    pairings.append(
                        (player['player_id'], opponent['player_id'])
                    )
                    used_players.update(
                        [player['player_id'],
                         opponent['player_id']])
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

        self.db_manager.update_round_matches(
            round_number,
            matches_infos,
            tournament_id)

        self.db_manager.update_round(round_number,
                                     {'status': RoundStatus.IN_PROGRESS.name})
        return matches_infos

    def prepare_and_start_first_round(self, tournament_id):
        player_ids = self.db_manager.get_tournament_players(tournament_id)
        self.view.message_player_pairing()
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
            player1_name = (f"{player1['first_name']} {player1['last_name']}"
                            if player1 else "Inconnu")
            player2_name = (f"{player2['first_name']} {player2['last_name']}"
                            if player2 else "Inconnu")

            # match creation
            match = Match(
                round_id=1,
                player1_id=player1_id,
                player2_id=player2_id,
                winner=None)
            match_id = self.db_manager.add_match(
                match.serialize())
            match.match_id = match_id

            # update database
            self.db_manager.update_match(match_id, match.serialize())

            # match info to display
            self.round_start_date(round_id=1)
            match_info = {
                'match_id': match_id,
                'player1_id': player1_id,
                'player2_id': player2_id,
                'player1_name': player1_name,
                'player2_name': player2_name,
                'winner': None
            }
            matches.append(match_info)

        # update tournament status
        self.db_manager.update_tournament(
            tournament_id,
            {'current_round': 1, 'status': TournamentStatus.IN_PROGRESS.name}
            )

        # update round status
        round_id = 1
        self.round_start_date(round_id)
        self.db_manager.update_round(
            round_id,
            {'matches': matches, 'status': RoundStatus.IN_PROGRESS.name})

        # display matches
        self.display_match_infos(round_id, matches)

        # ask scores for those matches
        self.view.press_any_key_to_continue()
        self.ask_match_results(tournament_id, matches, round_id)
        self.display_tournament_stats(tournament_id)

        # update round status after all matches are done
        self.round_end_date(round_id)
        self.db_manager.update_round(
            round_id,
            {'status': RoundStatus.FINISHED.name}
            )
        self.view.press_any_key_to_continue()

    def ask_match_results(self, tournament_id, matches, round_id):
        winner_id = None
        for match in matches:
            winner_choice = self.view.ask_match_result(match, round_id)
            if winner_choice == 1:
                winner_id = match['player1_id']
            elif winner_choice == 2:
                winner_id = match['player2_id']
            elif winner_choice == 3:
                winner_id = None
            else:
                self.back_to_main_menu()

            match['winner'] = winner_id

            self.update_player_scores(
                match['player1_id'],
                match['player2_id'],
                winner_id)

            self.db_manager.update_match_winner(
                match['match_id'],
                winner_id
                )

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

        players = []
        for player_id in player_ids:
            player = self.db_manager.get_player(player_id)
            players.append(player)

        # sort players by score
        sorted_players = sorted(
            players,
            key=lambda x: (
                -x['score'],
                x['first_name'] + " " + x['last_name'])
                )

        # display_stats
        self.view.display_tournament_stats(sorted_players)

    def get_current_tournament(self):
        tournaments = self.db_manager.list_tournaments()
        for tournament in tournaments:
            if tournament['status'] == 'IN_PROGRESS':
                return tournament

    def players_have_met(self, player1_id, player2_id, previous_matches):
        for match in previous_matches:
            players = [match['player1_id'], match['player2_id']]
            if player1_id in players and player2_id in players:
                return True
        return False

    def manage_rounds(self):
        self.view.clear_screen()
        manage_round_actions = {
            1: self.display_rounds_status,
            2: self.resume_round,
            3: self.back_to_main_menu
        }

        while True:
            self.view.clear_screen()
            self.view.app_menu_rounds()
            round_menu_choice = int(self.view.ask_menu_choice())
            action = manage_round_actions.get(round_menu_choice)
            if action:
                action()
            else:
                self.view.clear_screen()
                self.view.display_error_message()
                self.view.press_any_key_to_continue()
                self.manage_rounds()
                break

    def display_rounds_status(self):
        self.view.clear_screen()
        tournaments = self.db_manager.list_tournaments()
        self.view.display_tournament_list(tournaments)

        # ask user to choose tournament
        tournament_id = self.view.ask_id()
        all_rounds = self.db_manager.list_rounds(tournament_id)
        self.view.show_rounds_status(all_rounds)
        self.view.press_any_key_to_continue()
        return all_rounds

    def choose_round_to_resume(self):
        self.view.clear_screen()
        tournaments = self.db_manager.list_tournaments()
        self.view.display_tournament_list(tournaments)

        # ask user to choose tournament
        tournament_id = self.view.ask_id()
        all_rounds = self.db_manager.list_rounds(tournament_id)
        self.view.show_rounds_status(all_rounds)
        return all_rounds

    def resume_round(self):
        self.view.clear_screen()
        # get current tournament
        current_tournament = self.get_current_tournament()
        if current_tournament:
            tournament_id = current_tournament['tournament_id']
            all_rounds = self.db_manager.list_rounds(tournament_id)

            if all(round_item['status'] == "FINISHED" for round_item in all_rounds):
                self.view.message_tournament_finished()
                self.view.press_any_key_to_continue()
                self.back_to_main_menu()
            else:
                self.continue_round()
        else:
            self.view.message_no_active_tournament()
            self.view.press_any_key_to_continue()
            self.back_to_main_menu()

    def continue_round(self):
        # display rounds
        self.choose_round_to_resume()  # display all rounds and status
        round_id = self.view.ask_id()  # choose round id to resume

        selected_round = self.db_manager.get_round(round_id)

        if selected_round:
            if selected_round == 1:
                if selected_round['status'] == "PENDING":
                    self.view.message_start_round()
                    time.sleep(1)
                    self.prepare_and_start_first_round(tournament_id=selected_round['tournamend_id'])

            if selected_round['status'] == "PENDING":
                self.view.message_start_round()
                time.sleep(1)
                self.prepare_next_round(tournament_id=selected_round['tournament_id'], round_number=round_id)
            elif selected_round['status'] == "IN_PROGRESS":
                self.view.clear_screen()
                self.view.message_resume_round()
                time.sleep(1)
                self.resume_round_matches(tournament_id=selected_round['tournament_id'], round_id=round_id)
            else:
                self.view.message_round_finished()
                self.view.press_any_key_to_continue()
        else:
            self.view.display_error_message()
            self.view.press_any_key_to_continue()

    def resume_round_matches(self, tournament_id, round_id):
        round_info = self.db_manager.get_round(round_id)
        if not round_info:
            self.view.message_round_not_found()
            return

        matches = self.db_manager.list_matches(round_id)
        unfinished_matches = [match for match in matches if match['winner'] is None]

        if not unfinished_matches:
            self.view.message_all_matches_done()
            self.db_manager.update_round(round_id, {'status': RoundStatus.FINISHED.name})
            self.check_and_prepare_next_round(tournament_id, round_id)
            return

        all_unfinished_matches = []
        for match in unfinished_matches:
            player1 = self.db_manager.get_player(match['player1_id'])
            player2 = self.db_manager.get_player(match['player2_id'])
            match['player1_chess_id'] = player1['chess_id']
            match['player2_chess_id'] = player2['chess_id']
            match['player1_name'] = f"{player1.get('first_name', 'inconnu')} {player1.get('last_name', 'inconnu')}"
            match['player2_name'] = f"{player2.get('first_name', 'inconnu')} {player2.get('last_name', 'inconnu')}"
            match['match_id'] = match.doc_id
            all_unfinished_matches.append(match)

        # display all unfinished matches
        self.view.display_matches(round_id, all_unfinished_matches)

        # ask matches results
        for match in all_unfinished_matches:
            self.ask_match_results(tournament_id, [match], round_id)

        matches = self.db_manager.list_matches(round_id)
        if all(match['winner'] is not None for match in matches):
            self.db_manager.update_round(round_id, {'status': RoundStatus.FINISHED.name})
            self.view.message_round_finished()
            self.check_and_prepare_next_round(tournament_id, round_id)
        else:
            self.view.message_matches_left()

    def check_and_prepare_next_round(self, tournament_id, current_round_id):
        # get tournament infos status
        tournament_info = self.db_manager.get_tournament(tournament_id)
        if not tournament_info:
            self.view.message_tournament_not_found()
            return

        rounds = tournament_info['rounds']
        total_rounds = len(rounds)
        current_round_index = rounds.index(current_round_id)

        if current_round_index < total_rounds - 1:
            next_round_id = rounds[current_round_index + 1]
            self.view.message_prepare_next_round(next_round_id)
            self.prepare_next_round(tournament_id, next_round_id)
        else:
            self.db_manager.update_tournament(tournament_id, {'status': TournamentStatus.FINISHED.name})
            self.view.message_tournament_finished()

    def create_rounds(self, tournament_id):
        # check if tournament exist
        tournament = self.db_manager.get_tournament(tournament_id)
        if not tournament:
            self.view.display_error_message()
            return

        # check if rounds exists and not >4
        rounds = self.db_manager.list_rounds(tournament_id)
        if len(rounds) > 4:
            self.view.message_max_round_number()
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

        # update tournament to store its rounds
        self.db_manager.update_tournament(
            tournament_id,
            {'rounds': rounds_created}
        )

        time.sleep(1)
        self.view.display_success_message()
        rounds_created = self.db_manager.list_rounds(tournament_id)
        self.view.display_list_of_rounds(rounds_created)

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
                self.view.clear_screen()
                self.view.display_error_message()
                self.view.press_any_key_to_continue()
                self.manage_players()
                break

    def back_to_main_menu(self):
        self.view.clear_screen()
        self.main_loop()

    def show_reports(self):
        # to be defined -> Views : app_menu_reports and methods
        self.view.clear_screen()
        reports_menu_action = {
            1: self.players_reporting,
            2: self.tournaments_reporting,
            3: self.participants_reporting,
            4: self.rounds_matches_reporting,
            5: self.back_to_main_menu
        }

        while True:
            self.view.clear_screen()
            self.view.app_menu_reports()
            reports_menu_choice = int(self.view.ask_menu_choice())
            action = reports_menu_action.get(reports_menu_choice)
            if action:
                action()
            else:
                self.view.clear_screen()
                self.view.display_error_message()
                break

    def players_reporting(self):
        # get all players in database
        all_players = self.db_manager.list_players()

        # sort alphabeticaly
        sorted_all_players = sorted(
            all_players,
            key=lambda x: (x['first_name'], x['last_name'])
        )

        # display all players
        self.view.display_player_list(sorted_all_players)
        self.view.press_any_key_to_continue()
        self.show_reports()

    def tournaments_reporting(self):
        # get all tournaments
        all_tournaments = self.db_manager.list_tournaments()

        # show tournaments
        self.view.display_tournament_list(all_tournaments)
        self.view.press_any_key_to_continue()
        self.show_reports()

    def participants_reporting(self):
        # get all players
        players = self.db_manager.list_players()

        # ask tournament id from user
        tournaments = self.db_manager.list_tournaments()
        self.view.display_tournament_list(tournaments)
        tournament_id = self.view.ask_id()

        if tournament_id:
            participants = []
            for player in players:
                player_tournament_id = player.get('tournament_id')
                if player_tournament_id == tournament_id:
                    participants.append(player)

            # sort by score to determine champion
            sorted_participants = sorted(
                participants,
                key=lambda x: (
                    -x['score'],
                    x['first_name'],
                    x['last_name'])
            )

            # If there are participants, display them
            if sorted_participants:
                self.view.show_participants_list(sorted_participants)
                self.view.press_any_key_to_continue()
            else:
                self.view.display_message("Ce tournoi n'a pas encore de participants.")
        else:
            self.view.display_message("il n'y a pas de tournoi actif en cours.")

    def rounds_matches_reporting(self):
        # get tournament_id
        tournaments = self.db_manager.list_tournaments()
        self.view.display_tournament_list(tournaments)
        tournament_id = self.view.ask_id()

        # get all rounds
        rounds = self.db_manager.list_rounds(tournament_id)
        self.view.show_rounds_matches(rounds)
        self.view.press_any_key_to_continue()
        self.show_reports()

    def exit_app(self):
        self.view.clear_screen()
        exit()

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

    def update_player(self):
        all_players = self.db_manager.list_players()
        if not all_players:
            self.view.display_message("Aucun joueur à afficher.")
            return

        self.view.display_player_list(all_players)
        player_id = self.view.ask_id()

        player = self.db_manager.get_player(player_id)
        if player:
            self.view.show_player_data(player)
            updated_data = self.view.ask_player_infos_update()

            # update new player data inside database
            self.db_manager.update_player(player_id, updated_data)

            # show new player data
            updated_player = self.db_manager.get_player(player_id)
            self.view.show_player_data(updated_player)

            self.view.display_message("Informations du joueur mises à jour avec succès.")
        else:
            self.view.display_message("Joueur non trouvé.")

        self.view.press_any_key_to_continue()

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

    def round_start_date(self, round_id):
        # get current round
        current_round = self.db_manager.get_round(round_id)
        start_date = None
        if current_round is not None:
            string_start_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            start_date = string_start_date
            self.db_manager.update_round(round_id, {'start_date': start_date})
        else:
            self.view.message_round_not_found()

        return start_date

    def round_end_date(self, round_id):
        # get current round
        end_date = None
        current_round = self.db_manager.get_round(round_id)
        if current_round is not None:
            string_end_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            end_date = string_end_date
            self.db_manager.update_round(round_id, {'end_date': end_date})
        else:
            self.view.message_round_not_found()

        return end_date

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
            self.view.clear_screen()
            players = self.db_manager.list_players()
            self.view.display_player_list(players)
            self.view.display_success_message()
            another_player_choice = self.view.ask_create_another_player()
            self.view.clear_screen()
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
                    self.register_player_to_tournament(
                        tournament_id,
                        player_id_int
                    )
                    registered_players.add(player_id_int)
                    self.view.display_success_message()
                else:
                    self.view.display_error_message()
            except ValueError:
                self.view.display_error_message()

        self.db_manager.update_tournament(
            tournament_id,
            {'players': list(registered_players)}
        )

    def register_player_to_tournament(self, tournament_id, player_id):
        # tournament infos
        tournament_data = self.db_manager.get_tournament(tournament_id)
        if not tournament_data:
            self.view.message_tournament_not_found()
            return

        # check and update players list
        players_list = tournament_data.get('players', [])

        if player_id not in players_list:
            players_list.append(player_id)

            # update tournament with new players list
            self.db_manager.tournament_table.update(
                {'players': players_list},
                doc_ids=[tournament_id])
            # update players with tournament_id
            self.db_manager.player_table.update(
                {'tournament_id': tournament_id},
                doc_ids=[player_id])
        else:
            self.view.message_player_already_in_list()

    def list_players(self):
        all_players = self.db_manager.list_players()
        self.view.clear_screen()
        self.view.display_player_list(all_players)
        self.view.press_any_key_to_continue()

    def delete_player(self):
        players = self.db_manager.list_players()

        self.view.display_player_list(players)
        player_to_delete = self.view.ask_id()
        # check if player exist and show details about the player to delete

        player_to_delete_id = self.db_manager.get_player(player_to_delete)
        if not player_to_delete_id:
            self.view.display_message("Joueur non trouvé")
            self.view.press_any_key_to_continue()
            return

        self.view.show_player_data(player_to_delete_id)

        while True:
            user_input = self.view.ask_confirmation_deletion()
            if user_input.lower() == "o":
                self.db_manager.delete_player(player_to_delete)
                self.view.display_message("Joueur supprimé avec succès, base de données mise à jour")
                self.view.press_any_key_to_continue()
                break
            elif user_input.lower() == "n":
                self.view.display_message("Opération annulée, aucun élément supprimé, retour au menu principal")
                break
            else:
                self.view.display_message("Valeur incorrecte, veuillez choisir entre o et n")

        self.view.press_any_key_to_continue()
        self.back_to_main_menu()
