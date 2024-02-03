import models
import datetime
from models import Player
from rich.console import Console
from rich.table import Table
from rich.progress import track
import time
console = Console()
class View:
    def __init__(self) -> None:
        pass

    """
    Handling Menus Display
    """
    def display_main_menu(self):
        console.print("MENU PRINCIPAL", style="bold blue")
        print("[1] Tournoi")
        print("[2] Joueurs")
        print("[3] Rapport")
        print("[4] Quitter")
        main_menu_choice = int(input("Veuillez choisir un menu :"))
        return main_menu_choice

    def display_menu_players(self):
        print("Menu Joueurs")
        print("[1] Créer des joueurs")
        print("[2] Modifier un joueur")
        print("[3] Afficher la liste des joueurs")
        print("[4] Retour")
        player_menu_choice = int(input("Quel est votre choix :"))
        return player_menu_choice

    def display_menu_tournament(self):
        console.print("MENU TOURNOI", style="bold blue")
        print("[1] Créer un tournoi")
        print("[2] Reprendre un tournoi")
        print("[3] Retour")
        tournament_menu_choice = int(input("Quel est votre choix :"))
        return tournament_menu_choice

    def display_all_players(self):
        print("Affichage des joueurs créés")
        for player_id, player in Player.all_players.items():
            print(player)
        print("Joueurs créés dans la liste")

    def display_tournament(self, tournament):
        console.print("Tournoi créé avec succès", style="bold red")
        print(tournament)

    def display_resume_tournament(self):
        console.print("Reprendre un tournoi", style="bold blue")

    def display_progress_bar(self):
        for i in track(range(100)):
            time.sleep(0.025)


    """
    Validate datas
    """
    def validate_date(self, date):
        try:
            date = datetime.datetime.strptime(date, "%d/%m/%Y")
            return date
        except ValueError:
            print("Format de date incorrect. Veuillez utiliser JJ/MM/AAAA")

    """
    Get informations from user
    """
    def get_player_infos(self):
        print(f"Nom du joueur:")
        first_name = input(":")
        print(f"Prénom du joueur:")
        last_name = input(":")
        birthdate = None
        while birthdate is None:
            print("Saisissez la date de naissance au format JJ/MM/YYY :")
            birthdate_input = input(":")
            birthdate = self.validate_birthdate(birthdate_input)

        print(f"Chess ID:")
        chess_id = input(":")
        return first_name, last_name, birthdate.strftime("%d/%m/%Y"), chess_id

    def get_tournament_infos(self):
        console.print("CRÉATION DU TOURNOI", style="bold blue")
        print("Nom du tournoi")
        name = input(":")
        print("Lieu")
        location = input(":")
        print("Date de début")
        start_date = input(":")
        print("Date de fin")
        end_date = input(":")
        print("Description")
        description = input(":")
        return name, location, start_date, end_date, description
