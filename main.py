from controller import Controller

controller = Controller()

first_action = controller.view.get_menu_choice()

if first_action == 1:
    player_infos = controller.view.get_player_infos()
    player = controller.create_player(*player_infos)
    print(f"Joueur créé : {player}")
