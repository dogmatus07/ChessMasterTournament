import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track
import time
import os
import re

console = Console()
panel_width = 60

class View:
    def __init__(self) -> None:
        pass

    """
    Handling Menus Display
    """

    @staticmethod
    def app_main_menu(is_tournament_active):
        main_menu = Panel("MENU PRINCIPAL", title="CHESS MASTER APP", subtitle="Bienvenue", width=panel_width,
                          style="bold blue")
        # test if there's a tournament object active
        if is_tournament_active:
            options_menu = Panel(
                "\n1. Créer un tournoi"
                "\n2. Démarrer un tournoi"
                "\n3. Gérer les joueurs"
                "\n4. Rapport et Statistiques"
                "\n5. Quitter",
                border_style="blue",
                width=panel_width)
        else:
            options_menu = Panel(
                "\n1. Créer un tournoi"
                "\n2. Démarrer un tournoi (Créez d'abord un tournoi)"
                "\n3. Gérer les joueurs (Créez d'abord un tournoi)"
                "\n4. Rapport et Statistiques"
                "\n5. Quitter",
                border_style="blue",
                width=panel_width)

        # showing the rest of the menu
        help_menu = Panel("Logiciel de gestion de tournoi d'échecs",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        # display menus
        console.print(main_menu, justify="center")
        console.print(options_menu, justify="center")
        console.print(help_menu, justify="center")

    @staticmethod
    def app_menu_players():
        menu_players = Panel("Gérer les joueurs", title="MENU JOUEURS", width=panel_width, style="bold blue")
        players_options_menu = Panel(
            "\n1. Créer des joueurs"
            "\n2. Modifier un joueur"
            "\n3. Afficher la liste des joueurs"
            "\n4. Retour au menu principal",
            width=panel_width)
        help_menu = Panel("Ajoutez, modifiez ou affichez des joueurs",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")
        # display menus
        console.print(menu_players, justify="center")
        console.print(players_options_menu, justify="center")
        console.print(help_menu, justify="center")

    @staticmethod
    def display_menu_tournament():
        console.print("MENU TOURNOI", style="bold blue")
        print("[1] Créer un tournoi")
        print("[2] Lancer un tournoi")
        print("[3] Reprendre un tournoi")
        print("[4] Retour au menu principal")
        tournament_menu_choice = int(input("Quel est votre choix :"))
        return tournament_menu_choice

    @staticmethod
    def display_menu_report():
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

    @staticmethod
    def display_all_players(players):
        table = Table(title="Joueurs disponibles pour participer au tournoi", style="bold blue")
        # print("Joueurs disponibles pour participer au tournoi :")

        # add columns
        table.add_column("Player ID", style="cyan")
        table.add_column("Nom", style="blue")
        table.add_column("Date de naissance", style="yellow")
        table.add_column("Chess ID", style="magenta")
        table.add_column("Score", style="green")
        if players:
            for player in players:
                table.add_row(
                    str(player.player_id),
                    str(player.first_name) + str(player.last_name),
                    str(player.birthdate),
                    str(player.chess_id),
                    str(player.score))
            console.print(table)
        else:
            print("Aucun joueur disponible")

    @staticmethod
    def display_all_tournaments(all_tournaments):
        table = Table(title="Liste des joueurs disponibles pour le tournoi")

        # adding the columns
        table.add_column("ID Tournoi", style="cyan", no_wrap=True)
        table.add_column("Nom du Tournoi", style="magenta")
        table.add_column("Lieu", style="green")
        table.add_column("Début", style="yellow")
        table.add_column("Fin", style="yellow")
        table.add_column("Description", style="blue")

        for tournament_id, tournament in all_tournaments.items():
            table.add_row(
                tournament_id,
                tournament.name,
                tournament.location,
                tournament.start_date,
                tournament.end_date,
                tournament.description)
        console.print(table)

        """
        print(f"Tournoi {tournament_id}: {tournament.name}"
              f"Lieu: {tournament.location}"
              f"Début: {tournament.start_date}"
              f"Fin: {tournament.end_date}"
              f"Description: {tournament.description}")
        """
    @staticmethod
    def display_tournament(tournament):
        console.print("Tournoi créé avec succès", style="bold red")
        print(tournament)

    @staticmethod
    def display_player(player):
        console.print("Joueur créé avec succès", style="bold red")
        print(player)

    @staticmethod
    def display_resume_tournament():
        console.print("Reprendre un tournoi", style="bold blue")

    @staticmethod
    def display_progress_bar():
        for i in track(range(100)):
            time.sleep(0.025)

    """
    Validate datas
    """

    @staticmethod
    def validate_date(date):
        try:
            date = datetime.datetime.strptime(date, "%d/%m/%Y")
            return date
        except ValueError:
            print("Format de date incorrect. Veuillez utiliser JJ/MM/AAAA")

    @staticmethod
    def validate_chess_id(chess_id):
        template = r'^[A-Za-z]{2}\d{5}$'
        if re.match(template, chess_id):
            return chess_id
        else:
            print("Format de Chess ID invalide. Il doit être composé de 2 lettres suivies de 5 chiffres. Ex. : AB12345")
            return False

    """
    Managing Views
    """

    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def ask_start_round():
        print("Commencer le round ?")
        print("[1] Oui")
        print("[2] Non")
        ask_start_round_choice = input(":")
        return ask_start_round_choice

    @staticmethod
    def ask_create_another_player():
        print("Voulez-vous créer un autre joueur ?")
        print("[1] Oui")
        print("[2] Non")
        another_player_choice = int(input(":"))
        return another_player_choice

    @staticmethod
    def ask_user_choice():
        user_input = input("Quel est votre choix ? : ")
        user_choice = Panel(user_input, title="Votre choix ", style="bold blue", width=panel_width)
        console.print(user_choice, justify="center")
        return int(user_input)
    """
    Error handling
    """

    @staticmethod
    def menu_error():
        print("Choix non valide, veuillez réessayer")

    @staticmethod
    def menu_start_round(round_name):
        print(f"Démarrage du tour : {round_name} sur un total de 4 Rounds")
        time.sleep(10)

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

    @staticmethod
    def get_tournament_infos():
        tournament_menu_infos = Panel(
            "Veuillez entrer les informations du tournoi",
            title="CRÉATION DU TOURNOI",
            width=panel_width,
            style="bold blue")
        console.print(tournament_menu_infos, justify="center")

        table = Table()
        table.add_column("Champ", style="bold magenta")
        table.add_column("Description", justify="left")

        table.add_row("Nom", "Nom du tournoi")
        table.add_row("Lieu", "Lieu du tournoi")
        table.add_row("Date de début", "Format: DD/MM/YYYY")
        table.add_row("Date de fin", "Format: DD/MM/YYYY")
        table.add_row("Description", "Brève description du tournoi")

        console.print(table, justify="center")

        name = input("Nom du tournoi : ")
        location = input("Lieu : ")
        start_date = input("Date de début (DD/MM/YYYY) : ")
        end_date = input("Date de fin (DD/MM/YYYY) : ")
        description = input("Description : ")

        # display the datas entered
        View.clear_screen()
        tournament_created_menu = Panel(
            "Informations du tournoi",
            title="TOURNOI CREÉ AVEC SUCCÊS",
            width=panel_width,
            style="bold green")

        console.print(tournament_created_menu, justify="center")

        table = Table()
        table.add_column("Champ", style="bold magenta")
        table.add_column("Description", justify="left")
        table.add_row("Nom", name)
        table.add_row("Lieu", location)
        table.add_row("Date de début", start_date)
        table.add_row("Date de fin", end_date)
        table.add_row("Description", description)

        console.print(table, justify="center")
        return name, location, start_date, end_date, description