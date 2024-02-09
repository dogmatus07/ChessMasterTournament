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
    def display_main_menu(self, is_tournament_active):
        console.print("MENU PRINCIPAL", style="bold blue")
        print("[1] Créer un tournoi")
        if is_tournament_active:
            print("[2] Démarrer un tournoi")
            print("[3] Gérer les joueurs")
        else:
            print("[2] Démarrer un tournoi (créez d'abord un tournoi)")
            print("[3] Gérer les joueurs (créez d'abord un tournoi)")
        print("[4] Rapport et Statistiques")
        print("[5] Quitter")
        main_menu_choice = int(input("Veuillez choisir un menu :"))
        return main_menu_choice

    @staticmethod
    def display_menu_players():
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
        print("[2] Lancer un tournoi")
        print("[3] Reprendre un tournoi")
        print("[4] Retour au menu principal")
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

    def display_menu_participants(self):
        pass

    def display_all_players(self, players):
        print("Joueurs disponibles pour participer au tournoi :")
        if players:
            for player in players:
                print(f"Player ID: {player.player_id}"
                      f"Nom : {player.first_name} {player.last_name}"
                      f"Date de naissance : {player.birthdate}"
                      f"Chess ID : {player.chess_id}"
                      f"Score : {player.score}"
                      )
        else:
            print("Aucun joueur disponible")

    def display_all_tournaments(self, all_tournaments):
        print("Liste des tournois :")
        for tournament_id, tournament in all_tournaments.items():
            print(f"Tournoi {tournament_id}: {tournament.name}"
                  f"Lieu: {tournament.location}"
                  f"Début: {tournament.start_date}"
                  f"Fin: {tournament.end_date}"
                  f"Description: {tournament.description}")

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
        console.print(f"Nom du joueur:", style="bold blue")
        first_name = input(":")
        console.print(f"Prénom du joueur:", style="bold blue")
        last_name = input(":")
        birthdate = None
        while birthdate is None:
            console.print("Saisissez la date de naissance au format JJ/MM/YYY :", style="bold blue")
            birthdate_input = input(":")
            birthdate = self.validate_date(birthdate_input)

        console.print(f"Chess ID:", style="bold blue")
        chess_id = None
        while chess_id is None:
            chess_id_input = input(":")
            chess_id = self.validate_chess_id(chess_id_input)

        return first_name, last_name, birthdate.strftime("%d/%m/%Y"), chess_id

    def get_tournament_infos(self):
        console.print("CRÉATION DU TOURNOI", style="bold blue")
        console.print("Nom du tournoi", style="bold blue")
        name = input(":")
        console.print("Lieu", style="bold blue")
        location = input(":")
        console.print("Date de début", style="bold blue")
        start_date = input(":")
        console.print("Date de fin", style="bold blue")
        end_date = input(":")
        console.print("Description", style="bold blue")
        description = input(":")
        return name, location, start_date, end_date, description

    """
    Managing Views
    """

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def ask_start_round(self):
        print("Commencer le round ?")
        print("[1] Oui")
        print("[2] Non")
        ask_start_round_choice = input(":")
        return ask_start_round_choice

    def ask_create_another_player(self):
        print("Voulez-vous créer un autre joueur ?")
        print("[1] Oui")
        print("[2] Non")
        another_player_choice = int(input(":"))
        return another_player_choice

    """
    Error handling
    """

    def menu_error(self):
        print("Choix non valide, veuillez réessayer")

    def menu_start_round(self, round_name):
        print(f"Démarrage du tour : {round_name} sur un total de 4 Rounds")
        time.sleep(10)