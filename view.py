import models
import datetime
from models import Player
from rich.console import Console
from rich.table import Table
from rich.progress import track
import time
import os
import re

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
        print("[4] Retour au menu principal")
        player_menu_choice = int(input("Quel est votre choix :"))
        return player_menu_choice

    def display_menu_tournament(self):
        console.print("MENU TOURNOI", style="bold blue")
        print("[1] Créer un tournoi")
        print("[2] Reprendre un tournoi")
        print("[3] Retour au menu principal")
        tournament_menu_choice = int(input("Quel est votre choix :"))
        return tournament_menu_choice

    def display_menu_report(self):
        console.print("MENU RAPPORT", style="bold blue")
        print("[1] Statistiques des joueurs")
        print("[2] Tous les tournois")
        print("[3] Tous les Rounds dans un tournoi")
        print("[4] Tous les matchs dans un tournoi")
        print("[5] Retour au menu principal")
        menu_report_choice = int(input("Quel est votre choix :"))
        return menu_report_choice

    def display_all_players(self):
        print("Affichage des joueurs créés")
        for player_id, player in Player.all_players.items():
            print(player)
        print("Joueurs créés dans la liste")

    def display_tournament(self, tournament):
        console.print("Tournoi créé avec succès", style="bold red")
        print(tournament)

    def display_player(self, player):
        console.print("Joueur créé avec succès", style="bold red")
        print(player)

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

    def validate_chess_id(self, chess_id):
        template = r'^[A-Za-z]{2}\d{5}$'
        if re.match(template, chess_id):
            return chess_id
        else:
            print("Format de Chess ID invalide. Il doit être composé de 2 lettres suivies de 5 chiffres. Ex. : AB12345")
            return False

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
            birthdate = self.validate_date(birthdate_input)

        print(f"Chess ID:")
        chess_id = None
        while chess_id is None:
            chess_id_input = input(":")
            chess_id = self.validate_chess_id(chess_id_input)

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

    """
    Managing Views
    """

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')