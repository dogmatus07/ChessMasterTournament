import os
import re
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

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

    def app_menu_rounds(self):
        menu_rounds = Panel("Gérer les rounds",
                             title="MENU ROUNDS",
                             width=panel_width,
                             style="bold blue")

        rounds_options_menu = Panel(
            "\n1. Liste et état des rounds"
            "\n2. Reprendre le tournoi"
            "\n3. Retour au menu principal",
            width=panel_width)

        help_menu = Panel("Etat des rounds et reprise du tournoi",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")
        # display menus
        console.print(menu_rounds, justify="center")
        console.print(rounds_options_menu, justify="center")
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

    def app_menu_reports(self):
        menu_rounds = Panel("Gérer les rounds",
                            title="MENU ROUNDS",
                            width=panel_width,
                            style="bold blue")

        round_menu_options = Panel(
            "\n1. Joueurs"
            "\n2. Tournois"
            "\n3. Participants"
            "\n4. Rounds et matches"
            "\n5. Retour au menu principal",
            width=panel_width)

        help_menu = Panel("Rapports et statistiques, choisissez les données à afficher",
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
        self.clear_screen()
        if rounds_created is None:
            print("Aucun round trouvé ou liste vide")
            return
        header_menu = Panel("Rounds créés avec succès",
                            title="CHESS TOURNAMENT MANAGER ",
                            width=panel_width,
                            style="bold green")
        table = Table()
        table.add_column("Round ID", style="bold magenta")
        table.add_column("Status", style="bold magenta")
        table.add_column("Start date", style="bold yellow")
        table.add_column("End date", style="bold yellow")
        for i in rounds_created:
            table.add_row(str(i.doc_id), i["status"], i['start_date'], i['end_date'])

        help_menu = Panel(
            "Liste des rounds et leurs status actuellement",
            title="AIDE",
            style="bold green",
            width=panel_width)

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

    def show_rounds_status(self, rounds_created):
        self.clear_screen()
        if rounds_created is None:
            print("Aucun round trouvé ou liste vide")
            return
        header_menu = Panel("Status des rounds",
                            title="CHESS TOURNAMENT MANAGER ",
                            width=panel_width,
                            style="bold green")
        table = Table()
        table.add_column("Round ID", style="bold magenta")
        table.add_column("Start date", style="bold yellow")
        table.add_column("End date", style="bold yellow")
        table.add_column("Status", style="bold green")
        table.add_column("Matches", style="bold green")
        for i in rounds_created:
            table.add_row(
                str(i.doc_id),
                i["start_date"],
                i['end_date'],
                i["status"],
                str(len(i['matches']))
            )

        help_menu = Panel(
            "Liste des rounds et leurs status actuellement",
            title="AIDE",
            style="bold green",
            width=panel_width)

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

    def display_menu_report(self):
        console.print("MENU RAPPORT", style="bold blue")
        print("[1] Classement des joueurs")
        print("[2] Résultats des matches")
        print("[3] Statistiques tournoi")
        print("[4] Retour au menu principal")
        menu_report_choice = int(input("Quel est votre choix :"))
        return menu_report_choice

    def show_player_data(self, player):
        header_menu = Panel("Informations Joueur",
                            title="CHESS TOURNAMENT MANAGER ",
                            width=panel_width,
                            style="bold green")

        table = Table()

        table.add_column("Labels", style="bold magenta")
        table.add_column("Description", justify="left")

        table.add_row("Chess ID", player['chess_id'])
        table.add_row("Nom", player['first_name'])
        table.add_row("Prénom", player['last_name'])
        table.add_row("Date de naissance", player['birthday'])
        table.add_row("Genre", player['gender'])
        table.add_row("Score", str(player['score']))

        help_menu = Panel("A propos du joueur et ses informations",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

    """
    SHOW REPORTS
    """

    def display_matches(self, round_id, matches):
        self.clear_screen()
        header_menu = Panel(f"Liste des matchs du Round {round_id}",
                            title="MENU DÉMARRER TOURNOI",
                            width=panel_width)

        table = Table(title="", style="bold blue")
        help_menu = Panel("Vous êtes prêt(e) à démarrer le tournoi",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")
        # add columns
        table.add_column("Match ID", style="cyan")
        table.add_column("Chess ID P1", style="blue")
        table.add_column("Joueur 1", style="blue")
        table.add_column("VS")
        table.add_column("Chess ID P2", style="yellow")
        table.add_column("Joueur 2", style="yellow")

        if matches:
            for match in matches:
                table.add_row(
                    str(match['match_id']),
                    str(match['player1_chess_id']),
                    str(match['player1_name']),
                    str("VS"),
                    str(match['player2_chess_id']),
                    str(match['player2_name'])
                )

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
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

    def ask_start_next_round(self, tournament_id, round_id):
        self.clear_screen()
        header_menu = Panel(f"Prêt pour le ROUND {round_id}",
                            title="MENU DÉMARRER UN ROUND",
                            width=panel_width,
                            style="bold blue")

        option_menu = Panel(
            f"\n1. Commencer le Round {round_id}"
            "\n2. Retour au menu principal",
            width=panel_width,
            style="bold blue")

        help_menu = Panel(
            f"Tournoi {tournament_id} en cours."
            f"Démarrez le round {round_id} maintenant",
            title="AIDE",
            border_style="green",
            width=panel_width,
            style="bold green"
        )

        console.print(header_menu, justify="center")
        console.print(option_menu, justify="center")
        console.print(help_menu, justify="center")

        user_choice = int(input("Quel est votre choix :"))
        return user_choice

    def ask_match_result(self, match, round_id):
        self.clear_screen()
        header_menu = Panel(
            f"Résultat du match en cours",
            subtitle=f"Match numéro {match['match_id']} du TOURNOI / ROUND [{round_id} / 4]",
            title=f"{match['player1_name']} VS {match['player2_name']}",
            width=panel_width,
            style="bold blue"
        )
        option_menu = Panel(
            f"\n1. Victoire du joueur 1 : {match['player1_name']}"
            f"\n2. Victoire du joueur 2 : {match['player2_name']}"
            "\n3. Match Nul"
            "\n4. Retour au menu principal",
            width=panel_width,
        )

        help_menu = Panel("Renseignez les résultats du match",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(option_menu, justify="center")
        console.print(help_menu, justify="center")

        choice = int(input("Choisissez une option (1, 2, ou 3) : "))
        return choice

    def display_message_round_finished(self, round_number):
        print(f"Round {round_number} terminé !")

    def display_tournament_stats(self, players):
        header_menu = Panel(
            "Classement et Statistiques",
            title="CHESS TOURNAMENT MANAGER",
            style="bold blue",
            width=panel_width
        )
        table = Table(width=panel_width)
        table.add_column("Position", style="bold magenta")
        table.add_column("Chess ID", style="bold magenta")
        table.add_column("Nom", style="bold magenta")
        table.add_column("Score", style="bold magenta")
        for index, player in enumerate(players, start=1):
            table.add_row(str(index),
                          f"{player['chess_id']}",
                          f"{player['first_name']} {player['last_name']}",
                          str(player['score'])
                          )

        help_menu = Panel("Scores actuels des joueurs dans le tournoi",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

    def get_player_infos(self):
        header_menu = Panel("Création de joueurs",
                            title="CHESS TOURNAMENT MANAGER",
                            width=panel_width,
                            style="bold blue")

        help_menu = Panel("Veuillez fournir les informations du joueur",
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
                print(
                    "Réponse invalide,"
                    "veuillez saisir H pour Homme ou F pour Femme"
                )
        birthdate = None
        while birthdate is None:
            console.print(
                "Saisissez la date de naissance au format JJ/MM/YYY :",
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
        header_menu = Panel("Création d'un tournoi",
                            title="CHESS TOURNAMENT MANAGER ",
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

        # ask information about the tournament
        name = input("Nom du tournoi : ")
        location = input("Lieu du tournoi : ")
        start_date = None
        while start_date is None:
            console.print(
                "Date de début au format DD/MM/YYY :",
                style="bold blue")
            start_date_input = input(":")
            start_date = self.validate_date(start_date_input)
        end_date = None
        while end_date is None:
            console.print(
                "Date de fin au format DD/MM/YYY :",
                style="bold blue")
            end_date_input = input(":")
            end_date = self.validate_date(end_date_input)
        description = input("Description du tournoi : ")
        return name, location, start_date, end_date, description

    def ask_id(self):
        console.print("Veuillez renseigner un ID ", style="bold blue")
        user_choice = input(":")
        return int(user_choice)

    def ask_player_id(self):
        console.print("Veuillez choisir l'ID du joueur à inscrire au tournoi",
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
            "Opération effectuée avec succès. "
            "Base de données mise à jour",
            title="SUCCÈS",
            border_style="green",
            width=panel_width,
            style="bold green")

        console.print(help_menu, justify="center")

    def display_error_message(self):
        help_menu = Panel(
            "Erreur, veuillez réessayer ou revenir au menu principal en appuyant sur entrée",
            title="ERREUR",
            border_style="red",
            width=panel_width,
            style="bold red")

        console.print(help_menu, justify="center")

    def display_message(self, message):
        print(message)

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
        header_menu = Panel("Tournois disponibles en ce moment",
                            title="MENU TOURNOI ",
                            width=panel_width,
                            style="bold green")

        table = Table(width=panel_width)
        table.add_column("ID", style="bold magenta")
        table.add_column("Nom", style="bold magenta")
        table.add_column("Lieu", style="bold magenta")
        table.add_column("Date début", style="bold magenta")
        table.add_column("Date fin", style="bold magenta")
        table.add_column("Description", style="bold magenta")
        table.add_column("Status", style="bold blue")
        for tournament in tournaments:
            table.add_row(str(tournament.doc_id), tournament["name"],
                          tournament["location"], tournament["start_date"],
                          tournament["end_date"], tournament["description"],
                          tournament["status"]
                          )

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
            f"Détails à propos du tournoi suivant : {tournament['description']}",
            title="MENU TOURNOI",
            width=panel_width,
            style="bold green")

        table = Table()
        table.add_column("Libellé", style="bold magenta")
        table.add_column("Description", style="bold magenta")
        table.add_row("ID", str(tournament['doc_id']))
        table.add_row("Nom", tournament["name"])
        table.add_row("Lieu", tournament["location"])
        table.add_row("Date début", tournament["start_date"])
        table.add_row("Date fin", tournament["end_date"])
        table.add_row("Description", tournament["description"])
        table.add_row("Status", tournament['status'])

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
            print(
                "Format incorrect."
                "Veuillez fournir une date au format DD/MM/AAAA")

    @staticmethod
    def validate_chess_id(chess_id):
        template = r'^[A-Za-z]{2}\d{5}$'
        if re.match(template, chess_id):
            return chess_id
        else:
            print(
                "Format de Chess ID invalide.\n"
                "Il doit être composé de 2 lettres suivies de 5 chiffres."
                "Ex. : AB12345"
            )
            return None

    def show_participants_list(self, players):
        self.clear_screen()
        header_menu = Panel("Liste et détails des participants",
                            title="CHESS TOURNAMENT MANAGER",
                            subtitle="Menu Rapports & Statistiques",
                            width=panel_width,
                            style="bold green")

        table = Table(width=panel_width)
        table.add_column("ID", style="bold magenta")
        table.add_column("Nom & prénoms", style="bold magenta")
        table.add_column("Genre", style="bold magenta")
        table.add_column("Date de naissance", style="bold magenta")
        table.add_column("Chess ID", style="bold magenta")
        table.add_column("Score", style="bold green")
        for player in players:
            table.add_row(
                str(player.doc_id),
                player["first_name"] + " " + player["last_name"],
                player["gender"],
                datetime.strptime(player["birthday"],
                                  "%d/%m/%Y").strftime("%d/%m/%Y"),
                player["chess_id"],
                str(player['score'])
            )

        help_menu = Panel("Informations à propos des participants",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

    def show_rounds_matches(self, players):
        self.clear_screen()
        header_menu = Panel("Liste des rounds et matches",
                            title="CHESS TOURNAMENT MANAGER",
                            subtitle="Menu Rapports & Statistiques",
                            width=panel_width,
                            style="bold green")

        table = Table(width=panel_width)
        table.add_column("ID", style="bold magenta")
        table.add_column("Nom & prénoms", style="bold magenta")
        table.add_column("Genre", style="bold magenta")
        table.add_column("Date de naissance", style="bold magenta")
        table.add_column("Chess ID", style="bold magenta")
        table.add_column("Score", style="bold green")
        for player in players:
            table.add_row(
                str(player.doc_id),
                player["first_name"] + " " + player["last_name"],
                player["gender"],
                datetime.strptime(player["birthday"],
                                  "%d/%m/%Y").strftime("%d/%m/%Y"),
                player["chess_id"],
                str(player['score'])
            )

        help_menu = Panel("Informations à propos des tours et des matches du tournoi",
                          title="AIDE",
                          border_style="green",
                          width=panel_width,
                          style="bold green")

        console.print(header_menu, justify="center")
        console.print(table, justify="center")
        console.print(help_menu, justify="center")

    def display_player_list(self, players):
        self.clear_screen()
        header_menu = Panel("Joueurs disponibles",
                            title="MENU JOUEURS",
                            width=panel_width,
                            style="bold green")

        table = Table(title="Liste des joueurs", width=panel_width)
        table.add_column("ID", style="bold magenta")
        table.add_column("Nom & prénoms", style="bold magenta")
        table.add_column("Genre", style="bold magenta")
        table.add_column("Date de naissance", style="bold magenta")
        table.add_column("Chess ID", style="bold magenta")
        for player in players:
            table.add_row(
                str(player.doc_id),
                player["first_name"] + " " + player["last_name"],
                player["gender"],
                datetime.strptime(player["birthday"],
                                  "%d/%m/%Y").strftime("%d/%m/%Y"),
                player["chess_id"])
        console.print(header_menu, justify="center")
        console.print(table, justify="center")

    def message_round_not_found(self):
        self.clear_screen()
        alert_message = Panel("Round non trouvé",
                          title="MESSAGE",
                          border_style="red",
                          width=panel_width,
                          style="bold red")

        console.print(alert_message, justify="center")

    def message_all_matches_done(self):
        self.clear_screen()
        alert_message = Panel("Tous les matches de ce round sont terminés",
                              title="MESSAGE",
                              border_style="cyan",
                              width=panel_width,
                              style="bold cyan")

        console.print(alert_message, justify="center")
        self.press_any_key_to_continue()
    def message_round_finished(self):
        self.clear_screen()
        alert_message = Panel("ROUND terminé avec succès",
                              title="MESSAGE",
                              border_style="green",
                              width=panel_width,
                              style="bold green")

        console.print(alert_message, justify="center")
        self.press_any_key_to_continue()
    def message_matches_left(self):
        self.clear_screen()
        alert_message = Panel("Il reste des matches non terminés",
                              title="MESSAGE",
                              border_style="red",
                              width=panel_width,
                              style="bold red")

        console.print(alert_message, justify="center")
        self.press_any_key_to_continue()
    def message_max_round_number(self):
        self.clear_screen()
        alert_message = Panel("Nombre de rounds maximum atteint",
                              title="MESSAGE",
                              border_style="red",
                              width=panel_width,
                              style="bold red")

        console.print(alert_message, justify="center")
        self.press_any_key_to_continue()

    def message_tournament_not_found(self):
        self.clear_screen()
        alert_message = Panel("Tournoi non trouvé",
                              title="MESSAGE",
                              border_style="red",
                              width=panel_width,
                              style="bold red")

        console.print(alert_message, justify="center")
        self.press_any_key_to_continue()

    def message_player_already_in_list(self):
        self.clear_screen()
        alert_message = Panel("Le joueur est déjà inscrit dans le tournoi.",
                              title="MESSAGE",
                              border_style="red",
                              width=panel_width,
                              style="bold red")

        console.print(alert_message, justify="center")
        self.press_any_key_to_continue()

    def message_player_pairing(self):
        self.clear_screen()
        alert_message = Panel("Appariement des joueurs pour le round...",
                              title="MESSAGE",
                              border_style="green",
                              width=panel_width,
                              style="bold green")

        console.print(alert_message, justify="center")

    def message_start_round(self):
        alert_message = Panel("Démarrer le round...",
                              title="MESSAGE",
                              border_style="green",
                              width=panel_width,
                              style="bold green")

        console.print(alert_message, justify="center")

    def message_resume_round(self):
        alert_message = Panel("Préparation du ROUND à reprendre...",
                              title="MESSAGE",
                              border_style="green",
                              width=panel_width,
                              style="bold green")

        console.print(alert_message, justify="center")

    def message_prepare_next_round(self, next_round_id):
        alert_message = Panel(f"Préparation du round {next_round_id}",
                              title="MESSAGE",
                              border_style="green",
                              width=panel_width,
                              style="bold green")

        console.print(alert_message, justify="center")

    def message_tournament_finished(self):
        self.clear_screen()
        alert_message = Panel("Le tournoi est terminé.",
                              title="MESSAGE",
                              border_style="green",
                              width=panel_width,
                              style="bold green")

        console.print(alert_message, justify="center")

    def message_no_active_tournament(self):
        alert_message = Panel("Aucun tournoi ACTIF à reprendre.",
                              subtitle="Tous les rounds sont terminés",
                              title="MESSAGE",
                              border_style="green",
                              width=panel_width,
                              style="bold green")

        console.print(alert_message, justify="center")

