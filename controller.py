import random
import uuid
from view import View
from models import Player
from models import Tournament
from models import Match
from faker import Faker
import time

fake = Faker()


class Controller:
    def __init__(self) -> None:
        self.view = View()
        self.current_tournament = None

    def main_loop(self):
        while True:
            self.view.clear_screen()
            is_tournament_active = self.current_tournament is not None
            self.view.app_main_menu(is_tournament_active)
            main_menu_choice = self.view.ask_user_choice()
            if main_menu_choice == 1:  # Create Tournament
                self.view.clear_screen()
                tournament_infos = self.view.get_tournament_infos()
                self.create_tournament(*tournament_infos)
                self.view.clear_screen()
                self.view.display_tournament(self.current_tournament)
                self.view.return_main_menu()
                self.view.clear_screen()
            elif main_menu_choice == 2:  # Launch Tournament
                self.start_tournament_round()
            elif main_menu_choice == 3:  # Manage Players
                while True:
                    self.view.clear_screen()
                    self.view.app_menu_players()
                    player_menu_choice = self.view.ask_user_choice()
                    if player_menu_choice == 1:  # Create player
                        while True:
                            self.view.clear_screen()
                            player_infos = self.view.get_player_infos()
                            self.view.clear_screen()
                            self.create_player(*player_infos)
                            another_player_choice = self.view.ask_create_another_player()
                            if another_player_choice != 1:
                                break

                    elif player_menu_choice == 2:  # Edit player
                        self.view.clear_screen()
                        self.edit_player()
                    elif player_menu_choice == 3:  # Display all players
                        self.view.clear_screen()
                        self.view.display_players(self.current_tournament.players)
                        time.sleep(2)
                    elif player_menu_choice == 4:  # Return to main menu
                        self.view.clear_screen()
                        break
                    else:
                        self.view.menu_error()
                        time.sleep(3)
                        self.view.ask_user_choice()
            elif main_menu_choice == 4:  # Reportings
                while True:
                    self.view.clear_screen()
                    menu_report_choice = self.view.display_menu_report()
                    if menu_report_choice == 1:  # Players Statistics
                        print("Statistiques des joueurs")
                    elif menu_report_choice == 2:  # Display all tournaments
                        self.view.show_all_tournaments()
                        time.sleep(2)
                    elif menu_report_choice == 3:  # Display all rounds
                        print("Liste des rounds")
                    elif menu_report_choice == 4:  # Display all matches
                        print("Liste des matchs")
                    elif menu_report_choice == 5:
                        break
            elif main_menu_choice == 5:  # Quit the app
                self.view.clear_screen()
                break

    def create_player(self,
                      first_name,
                      last_name,
                      gender,
                      birthdate,
                      chess_id,
                      score=0):

        #  Create instance of player
        player = Player(first_name, last_name, gender, birthdate, chess_id, score=0)

        #  check if there's an active tournament and add the player to the list of players
        if self.current_tournament:
            self.current_tournament.players.append(player)
            self.view.display_players(self.current_tournament.players)
        return player

    def edit_player(self):
        print(f"Modification joueur")

    def create_tournament(self, name, location, start_date, end_date, description):
        self.current_tournament = Tournament(name, location, start_date, end_date, description)
        return self.current_tournament

    def pair_players(self):
        if self.current_tournament.current_round_number == 1:
            random.shuffle(self.current_tournament.players)
            matches = [
                Match(uuid.uuid4(),
                      self.current_tournament.players[i],
                      self.current_tournament.players[i + 1])
                for i in range(0, len(self.current_tournament.players), 2)]
            return matches

    def start_tournament_round(self):
        if not self.current_tournament:
            self.view.display_no_tournament()
            time.sleep(7)
            return

        while self.current_tournament.current_round_number <= self.current_tournament.number_of_rounds:
            if self.current_tournament.current_round_number > self.current_tournament.number_of_rounds:
                self.view.display_round_over()
                time.sleep(7)

            if len(self.current_tournament.players) % 2 != 0:
                self.view.display_no_pair_players()
                time.sleep(7)
                return

            matches = self.pair_players()
            for match in matches:
                self.view.display_match(
                    match,
                    self.current_tournament.current_round_number,
                    self.current_tournament.number_of_rounds)  # display match
                result = self.view.ask_match_result(match)  # ask match result
                match.set_result(result)  # update result and score

            self.current_tournament.current_round_number += 1
