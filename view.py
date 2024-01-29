import models
import datetime

class View:
    def __init__(self) -> None:
        pass

    def get_menu_choice(self):
        print("1 : Créer un nouveau joueur")
        print("2 : quitter")
        choice = int(input("Quel est votre choix :"))
        return choice

    def validate_birthdate(self, birthdate_str):
        try:
            birthdate = datetime.datetime.strptime(birthdate_str, "%d/%m/%Y")
            return birthdate
        except ValueError:
            print("Format de date incorrect. Veuillez utiliser JJ/MM/AAAA")

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
