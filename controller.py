from view import View
from models import Player
from models import Tournament
from models import Round
from datetime import datetime
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
            main_menu_choice = self.view.display_main_menu(is_tournament_active)
            if main_menu_choice == 1:  # Create Tournament
                self.view.clear_screen()
                tournament_infos = self.view.get_tournament_infos()
                self.create_tournament(*tournament_infos)
                time.sleep(2)
                self.view.clear_screen()
            elif main_menu_choice == 2:  # Launch Tournament
                self.launch_tournament()
            elif main_menu_choice == 3:  # Manage Players
                while True:
                    self.view.clear_screen()
                    player_menu_choice = self.view.display_menu_players()
                    if player_menu_choice == 1:  # Create player
                        while True:
                            self.view.clear_screen()
                            player_infos = self.view.get_player_infos()
                            self.create_player(*player_infos)
                            time.sleep(2)
                            another_player_choice = self.view.ask_create_another_player()
                            if another_player_choice != 1:
                                break

                    elif player_menu_choice == 2:  # Edit player
                        self.view.clear_screen()
                        self.edit_player()
                    elif player_menu_choice == 3:  # Display all players
                        self.view.clear_screen()
                        self.view.display_all_players(self.current_tournament.players)
                        time.sleep(2)
                    elif player_menu_choice == 4:  # Return to main menu
                        self.view.clear_screen()
                        break
                    else:
                        self.view.menu_error()
            elif main_menu_choice == 4:  # Reportings
                while True:
                    self.view.clear_screen()
                    menu_report_choice = self.view.display_menu_report()
                    if menu_report_choice == 1:  # Players Statistics
                        print("Statistiques des joueurs")
                    elif menu_report_choice == 2:  # Display all tournaments
                        self.show_all_tournaments()
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
                      birthdate,
                      chess_id,
                      score=0):
        player = Player(first_name, last_name, birthdate, chess_id, score=0)
        self.view.display_player(player)
        if self.current_tournament:
            self.current_tournament.add_player(player)
        return player

    def edit_player(self):
        print(f"Modification joueur")


    def update_score(self, points):
        """
        This will update the player's score :
        win : 1 point
        square : 0.5 point
        defeat : 0 point
        """
        pass

    def create_tournament(self, name, location, start_date, end_date, description):
        self.current_tournament = Tournament(name, location, start_date, end_date, description)
        self.view.display_tournament(self.current_tournament)
        return self.current_tournament

    def launch_tournament(self):
        while True:
            if self.current_tournament:
                self.view.display_all_players(self.current_tournament.players)
                # Ask confirmation to start the round
                ask_start_round_choice = self.view.ask_start_round()
                if ask_start_round_choice == 1:
                    # Start the first round
                    round_name = self.start_round()
                    self.view.menu_start_round(round_name)
                elif ask_start_round_choice == 2:
                    self.view.display_all_players(self.current_tournament.players)
                else:
                    break

    def start_round(self):
        round_name = None
        if self.current_tournament:
            new_round_number = len(self.current_tournament.rounds) + 1
            round_name = f"Round {new_round_number}"
            if new_round_number <= self.current_tournament.number_of_rounds:
                self.current_tournament.start_new_round(round_name)
            else:
                print("Nombre maximum de tours atteint")
        else:
            print("Aucun tournoi actif, veuillez en créer")
        return round_name

    def close_current_round(self):
        if self.current_tournament and self.current_tournament.rounds:
            current_round = self.current_tournament.rounds[-1]
            if not current_round.is_complete:
                current_round.close_round()
                print(f"Le {current_round.name} est maintenant terminé")
            else:
                print("Le dernier round est déjà terminé")
        else:
            print("Aucun tournoi actif et aucun round trouvé")

    def resume_tournament(self):
        self.view.display_resume_tournament()

    def choose_tournament_players(self):
        self.view.display_all_players()


    def show_all_tournaments(self):
        all_tournaments = Tournament.all_tournaments
        self.view.display_all_tournaments(all_tournaments)

