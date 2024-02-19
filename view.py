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
        main_menu = Panel("MENU PRINCIPAL", title="CHESS TOURNAMENT MANAGER", subtitle="Bienvenue", width=panel_width,
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
        header_menu = Panel("Liste des joueurs disponibles pour participer au tournoi", title="MENU DÉMARRER TOURNOI")
        table = Table(title="", style="bold blue")
        help_menu = Panel("Vous êtes prêt(e) à démarrer le tournoi",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")
        # add columns
        table.add_column("Player ID", style="cyan")
        table.add_column("Nom & prénoms", style="blue")
        table.add_column("Date de naissance", style="yellow")
        table.add_column("Chess ID", style="magenta")
        table.add_column("Score", style="green")
        if players:
            for player in players:
                table.add_row(
                    str(player.player_id),
                    str(player.first_name) + " " + str(player.last_name),
                    str(player.birthdate),
                    str(player.chess_id),
                    str(player.score))
            console.print(table)
        else:
            print("Aucun joueur disponible")

        #  Display the results
        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

    @staticmethod
    def display_tournament(tournament):
        tournament_created_menu = Panel(
            "Informations du tournoi",
            title="TOURNOI CREÉ AVEC SUCCÊS",
            width=panel_width,
            style="bold green")

        help_menu_created = Panel("Vous pouvez maintenant créer des joueurs pour participer à ce tournoi",
                                  title="AIDE",
                                  border_style="green",
                                  width=panel_width,
                                  style="bold green")
        table = Table()

        # adding the columns
        table.add_column("ID Tournoi", style="cyan", no_wrap=True)
        table.add_column("Nom du Tournoi", style="magenta")
        table.add_column("Lieu", style="green")
        table.add_column("Début", style="yellow")
        table.add_column("Fin", style="yellow")
        table.add_column("Description", style="blue")

        # adding the rows
        table.add_row(
            str(tournament.tournament_id),
            tournament.name,
            tournament.location,
            tournament.start_date,
            tournament.end_date,
            tournament.description)
        console.print(tournament_created_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu_created, justify="center")

    @staticmethod
    def display_players(players):
        header_menu = Panel("Résultats", title="MENU CRÉATION DE JOUEURS", width=panel_width, style="bold blue")
        #  Adding the column
        table = Table(title=None)
        table.add_column("Player ID", style="cyan")
        table.add_column("Nom", style="blue")
        table.add_column("Genre", style="green")
        table.add_column("Date de naissance", style="yellow")
        table.add_column("Chess ID", style="magenta")
        table.add_column("Score", style="green")
        if players:
            for player in players:
                table.add_row(
                    str(player.player_id),
                    f"{player.first_name} {player.last_name}",
                    str(player.gender),
                    str(player.birthdate),
                    player.chess_id,
                    str(player.score)
                )
        else:
            print("Aucun joueur disponible")
        help_menu = Panel("Les joueurs ont été créés avec succès",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")
        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

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
            return ""

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
        ask_start_round_choice = int(input(":"))
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
        time.sleep(2)

    """
    Get informations from user
    """
    def get_player_infos(self):
        header_menu = Panel(
            "Veuillez fournir les informations du joueur",
            title="MENU CRÉATION JOUEURS",
            width=panel_width,
            style="bold blue")

        help_menu = Panel("Ces joueurs vont participer au tournoi",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        table = Table()
        table.add_column("Nom & prénoms du joueur", style="bold magenta")
        table.add_column("Genre")
        table.add_column("Date de naissance")
        table.add_column("Chess ID")

        table.add_row("Nom & prénoms", "H/F", "Format JJ/MM/AAAA", "Format AB12345")

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

        #  ask user for informations
        console.print(f"Nom du joueur :", style="bold blue")
        first_name = input(">> ")
        console.print(f"Prénom du joueur :", style="bold blue")
        last_name = input(">> ")
        console.print("Genre : ", style="bold blue")
        gender = ""
        while True:
            ask_genre = input("Choisir entre H ou F >> ")
            if ask_genre == "H" or ask_genre == "F":
                gender = ask_genre
                break
            else:
                print("Réponse invalide, veuillez saisir H pour Homme ou F pour Femme")
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
        return first_name, last_name, gender, birthdate.strftime("%d/%m/%Y"), chess_id

    def get_tournament_infos(self):
        header_menu = Panel(
            "Veuillez entrer les informations du tournoi",
            title="CRÉATION DU TOURNOI",
            width=panel_width,
            style="bold blue")

        help_menu = Panel("Veuillez fournir les informations demandées",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        table = Table()
        table.add_column("Champ", style="bold magenta")
        table.add_column("Description", justify="left")

        table.add_row("Nom", "Nom du tournoi")
        table.add_row("Lieu", "Lieu du tournoi")
        table.add_row("Date de début", "Format: DD/MM/YYYY")
        table.add_row("Date de fin", "Format: DD/MM/YYYY")
        table.add_row("Description", "Brève description du tournoi")

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

        # ask infos
        name = input("Nom du tournoi : ")
        location = input("Lieu : ")
        start_date = None
        while start_date is None:
            console.print("Saisissez la date au format JJ/MM/YYY :", style="bold blue")
            start_date_input = input(":")
            start_date = self.validate_date(start_date_input)
        end_date = None
        while end_date is None:
            console.print("Saisissez la date au format JJ/MM/YYY :", style="bold blue")
            end_date_input = input(":")
            end_date = self.validate_date(end_date_input)
        description = input("Description : ")
        return name, location, start_date.strftime("%d/%m/%Y"), end_date.strftime("%d/%m/%Y"), description

    @staticmethod
    def return_main_menu():
        print("[1] Retourner au menu principal")
        input(":")

    def display_matches(self, matches):
        # Afficher les matchs ici
        for match in matches:
            print(f"{match.player1} vs {match.player2}")

    def ask_match_result(self, match):
        header_menu = Panel(
            "Qui a gagné ?",
            title="RÉSULTAT DU MATCH",
            width=panel_width,
            style="bold blue")

        main_menu = Panel(f"\n1. Victoire de Player 1 : {match.player1.name}"
                          f"\n2. Victoire de Player 2 : {match.player2.name}"
                          "\n3. Match nul",
                          title="OPTIONS")

        help_menu = Panel(f"Veuillez entrer les résultats du match entre {match.player1.name} et {match.player2.name}",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(main_menu, justify="center")
        console.print(help_menu, justify="center")

        choice = input("Choix: ")
        if choice == '1':
            return match.player1
        elif choice == '2':
            return match.player2
        else:
            return None  # draw

    """
    Errors display message
    """
    def display_no_tournament(self):
        header_menu = Panel(
            "Vous devez d'abord créer un tournoi",
            title="ERREUR",
            width=panel_width,
            style="bold blue")

        main_menu = Panel("Il n'y a pas de tournoi actif")

        help_menu = Panel("Veuillez revenir au menu principal et créer un tournoi",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(main_menu, justify="center")
        console.print(help_menu, justify="center")

    def display_round_over(self):
        header_menu = Panel(
            "Les rounds sont tous terminés, le tournoi est achevé",
            title="TOURNOI TERMINÉ",
            width=panel_width,
            style="bold blue")

        main_menu = Panel("Tous les rounds sont terminés")

        help_menu = Panel("Veuillez revenir au menu principal et créer un nouveau tournoi",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(main_menu, justify="center")
        console.print(help_menu, justify="center")

    def display_no_pair_players(self):
        header_menu = Panel(
            "Le nombre de joueurs est impair",
            title="IMPOSSIBLE DE DÉMARRER LE TOURNOI",
            width=panel_width,
            style="bold blue")

        main_menu = Panel("Il faut que les joueurs soient en nombre pair pour pouvoir démarrer les rounds")

        help_menu = Panel("Veuillez revenir au menu principal > Gérer les joueurs et créer de nouveaux joueurs",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(main_menu, justify="center")
        console.print(help_menu, justify="center")
    def display_draw_message(self):
        console.print("Match nul entre {match.player1.name} et {match.player2.name}")

    def display_match(self, match, current_round, total_rounds):
        header_menu = Panel(
            "Liste des matches pour le round actuel",
            title=f"MATCHES EN COURS : ROUND {current_round} / {total_rounds}",
            width=panel_width,
            style="bold blue")

        help_menu = Panel("Détails des joueurs qui disputent les matches",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        table = Table()
        table.add_column("ID")
        table.add_column("Player 1")
        table.add_column("Player 2")
        table.add_row(str(match.match_id), match.player1.name, match.player2.name)

        # display menus
        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

    def show_all_tournaments(self):
        print("Tous les tournois")

    def display_current_round_number(self, current_round, total_rounds):
        header_menu = Panel(
            f"Le round {current_round} est actuellement en cours",
            title=f"ROUND {current_round} sur un total de {total_rounds}",
            width=panel_width,
            style="bold blue")

        help_menu = Panel("Rounds du tournoi lancé",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(help_menu, justify="center")
