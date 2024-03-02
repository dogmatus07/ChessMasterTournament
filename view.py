import os
import re
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from db_manager import DatabaseManager

console = Console()
panel_width = 80


class View:

    def __init__(self) -> None:
        pass

    """
    MENUS
    """

    def app_main_menu(self):
        main_menu = Panel("MENU PRINCIPAL",
                          title="CHESS TOURNAMENT MANAGER",
                          subtitle="Bienvenue",
                          width=panel_width,
                          style="bold blue")

        options_menu = Panel(
            "\n1. Créer un tournoi"
            "\n2. Ajouter des participants"
            "\n3. Démarrer le tournoi"
            "\n4. Gérer les rounds"
            "\n5. Gérer les joueurs"
            "\n6. Rapport et Statistiques"
            "\n7. Quitter",
            border_style="blue",
            width=panel_width)

        help_menu = Panel("Logiciel de gestion de tournoi d'échecs",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        # display menus
        console.print(main_menu, justify="center")
        console.print(options_menu, justify="center")
        console.print(help_menu, justify="center")

    def app_menu_players(self):
        menu_players = Panel("Gérer les joueurs",
                             title="MENU JOUEURS",
                             width=panel_width,
                             style="bold blue")

        players_options_menu = Panel(
            "\n1. Créer des joueurs"
            "\n2. Liste des joueurs"
            "\n3. Supprimer un joueur"
            "\n4. Mettre à jour un joueur"
            "\n5. Retour au menu principal",
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

    def app_round_menu(self):
        menu_rounds = Panel("Gérer les rounds",
                            title="MENU ROUNDS",
                            width=panel_width,
                            style="bold blue")

        round_menu_options = Panel(
            "\n1. Créer rounds"
            "\n2. Démarrer un round"
            "\n3. Reprendre un round"
            "\n4. Retour au menu principal",
            width=panel_width)

        help_menu = Panel("Ajoutez, démarrez ou reprenez des rounds",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")
        # display menus
        console.print(menu_rounds, justify="center")
        console.print(round_menu_options, justify="center")
        console.print(help_menu, justify="center")

    def display_round_creation(self):
        print("Création des rounds 1 à 4 en cours...")

    def display_list_of_rounds(self, rounds_created):
        if rounds_created is None:
            print("Aucun round trouvé ou liste vide")
            return
        header_menu = Panel("Rounds disponibles pour ce tournoi",
                            title="MENU TOURNOI ",
                            width=panel_width,
                            style="bold green")
        table = Table()
        table.add_column("Round ID", style="bold magenta")
        table.add_column("Status", style="bold magenta")
        for i in rounds_created:
            table.add_row(str(i.doc_id), i["status"])

            help_menu = Panel(
                "Etape suivante : démarrer le premier round",
                title="AIDE",
                style="bold green",
                width=panel_width)

            console.print(header_menu, justify="center")
            console.print(help_menu, justify="center")

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
        print("[1] Classement des joueurs")
        print("[2] Résultats des matches")
        print("[3] Statistiques tournoi")
        print("[4] Retour au menu principal")
        menu_report_choice = int(input("Quel est votre choix :"))
        return menu_report_choice

    """
    SHOW REPORTS
    """

    @staticmethod
    def display_all_players(players):
        header_menu = Panel(
            "Liste des joueurs disponibles pour participer au tournoi",
            title="MENU DÉMARRER TOURNOI")

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
                table.add_row(str(player.player_id),
                              str(player.first_name) + " " + str(player.last_name),
                              str(player.birthdate), str(player.chess_id),
                              str(player.score))
            console.print(table)
        else:
            print("Aucun joueur disponible")

        #  Display the results
        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

    def display_all_first_round_matches(self, matches):
        header_menu = Panel("Liste des matchs du premier round",
                            title="MENU DÉMARRER TOURNOI")

        table = Table(title="", style="bold blue")
        help_menu = Panel("Vous êtes prêt(e) à démarrer le tournoi",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")
        # add columns
        table.add_column("Match ID", style="cyan")
        table.add_column("Joueur 1", style="blue")
        table.add_column("Joueur 2", style="yellow")
        table.add_column("Score", style="magenta")

        if matches:
            for match in matches:
                table.add_row(
                    str(match['match_id']),
                    str(match['player1_name']),
                    str(match['player2_name']),
                    str(match.get('score', 'N/A')),
                )

        console.print(table, justify="center")
        console.print(header_menu, justify="center")
        console.print(help_menu, justify="center")

    """
    GET INFORMATIONS FROM USER
    """

    def ask_create_another_player(self):
        print("Voulez-vous créer un autre joueur ?")
        print("[1] Oui")
        print("[2] Non")
        another_player_choice = int(input(":"))
        return another_player_choice

    def ask_menu_choice(self):
        user_input = input("Quel est votre choix ? : ")

        user_choice = Panel(user_input,
                            title="Votre choix ",
                            style="bold blue",
                            width=panel_width)

        console.print(user_choice, justify="center")
        return int(user_input)

    def ask_start_first_round(self):
        header_menu = Panel("Commencer le Round 1",
                            title="MENU DÉMARRER UN TOURNOI",
                            width=panel_width,
                            style="bold blue")

        option_menu = Panel(
            "\n1. Commencer le Round 1"
            "\n2. Retour au menu principal",
            width=panel_width,
            style="bold blue")

        help_menu = Panel("Démarrage du premier round",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(option_menu, justify="center")
        console.print(help_menu, justify="center")

        user_choice = int(input("Quel est votre choix :"))
        return user_choice

    def get_player_infos(self):
        header_menu = Panel("Veuillez fournir les informations du joueur",
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

        table.add_row("Nom & prénoms", "H/F", "Format JJ/MM/AAAA",
                      "Format AB12345")

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

        #  ask user for informations
        console.print("Nom du joueur :", style="bold blue")
        first_name = input(">> ")
        console.print("Prénom du joueur :", style="bold blue")
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
            console.print("Saisissez la date de naissance au format JJ/MM/YYY :",
                          style="bold blue")
            birthdate_input = input(":")
            birthdate = self.validate_date(birthdate_input)

        console.print("Chess ID:", style="bold blue")
        chess_id = None
        while chess_id is None:
            chess_id_input = input(":")
            chess_id = self.validate_chess_id(chess_id_input)
        return first_name, last_name, gender, birthdate.strftime(
            "%d/%m/%Y"), chess_id

    def get_tournament_infos(self):
        header_menu = Panel("Informations du tournoi",
                            title="CRÉATION D'UN TOURNOI ",
                            width=panel_width,
                            style="bold green")

        table = Table()

        table.add_column("Labels", style="bold magenta")
        table.add_column("Description", justify="left")

        table.add_row("Nom", "Nom du tournoi")
        table.add_row("Lieu", "Lieu où se déroule le tournoi")
        table.add_row("Date de début", "Format: DD/MM/YYYY")
        table.add_row("Date de fin", "Format: DD/MM/YYYY")
        table.add_row("Description", "Description du tournoi")

        help_menu = Panel("Veuillez fournir les informations du tournoi",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

        # ask informations about the tournament
        name = input("Nom du tournoi : ")
        location = input("Lieu du tournoi : ")
        start_date = None
        while start_date is None:
            console.print("Date de début au format DD/MM/YYY :", style="bold blue")
            start_date_input = input(":")
            start_date = self.validate_date(start_date_input)
        end_date = None
        while end_date is None:
            console.print("Date de fin au format DD/MM/YYY :", style="bold blue")
            end_date_input = input(":")
            end_date = self.validate_date(end_date_input)
        description = input("Description du tournoi : ")
        return name, location, start_date, end_date, description

    def ask_tournament_id(self):
        console.print("Veuillez renseigner l'ID du tournoi", style="bold blue")
        user_choice = input(":")
        return int(user_choice)

    def ask_player_id(self):
        console.print("Veuillez choisir le joueur à inscrire au tournoi",
                      style="bold blue")
        user_choice = input(":")
        return user_choice

    def ask_tournament_infos_update(self):
        updated_data = {}
        name = input("Nouveau nom du tournoi : ")
        if name.strip():
            updated_data["name"] = name

        location = input("Nouveau lieu du tournoi : ")
        if location.strip():
            updated_data["location"] = location

        start_date = input("Nouvelle date de début du tournoi : ")
        if start_date.strip():
            updated_data["start_date"] = start_date

        end_date = input("Nouvelle date de fin du tournoi : ")
        if end_date.strip():
            updated_data['end_date'] = end_date

        description = input("Nouvelle description du tournoi : ")
        if description.strip():
            updated_data["description"] = description

        return updated_data

    def ask_delete_tournament(self):
        user_input = input("Saisissez l'ID du tournoi à supprimer : ")
        user_choice = Panel(user_input,
                            title="Votre choix ",
                            style="bold blue",
                            width=panel_width)

        console.print(user_choice, justify="center")
        return user_input

    def ask_confirmation_deletion(self):
        help_menu = Panel("Voulez-vous vraiment supprimer cet élément ?",
                          title="ACTION REQUISE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(help_menu, justify="center")
        user_input = input("o/n : ")
        return user_input

    """
    USER EXPERIENCE  
    """

    @staticmethod
    def clear_screen():
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def return_main_menu(self):
        print("[1] Retourner au menu principal ?")
        input(":")

    def press_any_key_to_continue(self):
        input("Appuyez sur entrée pour continuer...")

    """
    DISPLAY MESSAGES
    """

    def display_success_message(self):
        help_menu = Panel(
            "Opération effectuée avec succès et mise à jour de la base de données",
            title="SUCCÈS",
            border_style="green",
            width=panel_width,
            style="bold green")

        console.print(help_menu, justify="center")

    def display_error_message(self):
        help_menu = Panel(
            "Erreur, veuillez réessayer ou revenir au menu principal ",
            title="ERREUR",
            border_style="red",
            width=panel_width,
            style="bold red")

    def display_not_suffisant_players(self):
        help_menu = Panel(
            "Nombre de joueurs insuffisant, créez des joueurs pour commencer ",
            title="ERREUR",
            border_style="red",
            width=panel_width,
            style="bold red")

        console.print(help_menu, justify="center")

    def display_initialize_rounds_success(self):
        help_menu = Panel("Round initialisé avec succès",
                          title="SUCCESS",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(help_menu, justify="center")

    def display_tournament_list(self, tournaments):

        header_menu = Panel("Tournois disponibles",
                            title="MENU TOURNOI ",
                            width=panel_width,
                            style="bold green")

        table = Table(title="Liste des tournois")
        table.add_column("ID", style="bold magenta")
        table.add_column("Nom", style="bold magenta")
        table.add_column("Lieu", style="bold magenta")
        table.add_column("Date début", style="bold magenta")
        table.add_column("Date fin", style="bold magenta")
        table.add_column("Description", style="bold magenta")
        for tournament in tournaments:
            table.add_row(str(tournament.doc_id), tournament["name"],
                          tournament["location"], tournament["start_date"],
                          tournament["end_date"], tournament["description"])

        help_menu = Panel("Tournois actuellement dans la base de données",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

    def display_tournament_details(self, tournament):
        header_menu = Panel(
            f"Détails à propos du tournoi suivant : ",
            title="MENU TOURNOI",
            width=panel_width,
            style="bold green")

        table = Table(title=f"Détails du tournoi : {tournament['name']}")
        table.add_column("Libellé", style="bold magenta")
        table.add_column("Description", style="bold magenta")
        table.add_row("ID", str(tournament.doc_id))
        table.add_row("Nom", tournament["name"])
        table.add_row("Lieu", tournament["location"])
        table.add_row("Date début", tournament["start_date"])
        table.add_row("Date fin", tournament["end_date"])
        table.add_row("Description", tournament["description"])

        help_menu = Panel("Informations à propos d'un tournoi",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

    """
    VALIDATE DATAS
    """

    @staticmethod
    def validate_date(date):
        try:
            date = datetime.strptime(date, "%d/%m/%Y")
            return date
        except ValueError:
            print("Format incorrect. Veuillez fournir une date au format DD/MM/AAAA")

    @staticmethod
    def validate_chess_id(chess_id):
        template = r'^[A-Za-z]{2}\d{5}$'
        if re.match(template, chess_id):
            return chess_id
        else:
            print(
                "Format de Chess ID invalide.\n"
                "Il doit être composé de 2 lettres suivies de 5 chiffres. Ex. : AB12345"
            )
            return None

    def display_player_list(self, players):
        header_menu = Panel("Joueurs disponibles",
                            title="MENU JOUEURS",
                            width=panel_width,
                            style="bold green")

        table = Table(title="Liste des joueurs")
        table.add_column("ID", style="bold magenta")
        table.add_column("Nom & prénoms", style="bold magenta")
        table.add_column("Genre", style="bold magenta")
        table.add_column("Date de naissance", style="bold magenta")
        table.add_column("Chess ID", style="bold magenta")
        for player in players:
            table.add_row(
                str(player.doc_id), player["first_name"] + " " + player["last_name"],
                player["gender"],
                datetime.strptime(player["birthday"],
                                  "%d/%m/%Y").strftime("%d/%m/%Y"),
                player["chess_id"])
        console.print(header_menu, justify="center")
        console.print(table, justify="center")
