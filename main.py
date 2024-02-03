from controller import Controller
import time

controller = Controller()

"""
Menu
"""
while True:  # boucle pour le menu principal
    controller.clear_screen()
    main_menu_choice = controller.view.display_main_menu()
    if main_menu_choice == 1:
        controller.clear_screen()
        while True:  # boucle pour le sous-menu tournoi (1)
            tournament_menu_choice = controller.view.display_menu_tournament()
            if tournament_menu_choice == 1:
                controller.clear_screen()
                tournament_infos = controller.view.get_tournament_infos()
                controller.view.display_progress_bar()
                controller.create_tournament(*tournament_infos)
                time.sleep(2)
                controller.clear_screen()

            elif tournament_menu_choice == 2:
                controller.clear_screen()
                controller.resume_tournament()

            elif tournament_menu_choice == 3:
                controller.clear_screen()
                controller.view.display_main_menu() # back to the main menu
            else:
                print("Choix non valide")
    if main_menu_choice == 2:
        while True: # boucle pour le sous-menu joueurs
            controller.clear_screen()
            player_menu_choice = controller.view.display_menu_players()
            if player_menu_choice == 1:
                pass

            elif player_menu_choice ==2:
                pass
    if main_menu_choice == 3:
        while True: # boucle pour le sous-menu rapports
            player_menu_choice = controller.view.display_menu_players()
            if player_menu_choice == 1:
                pass

            elif player_menu_choice ==2:
                pass
    if main_menu_choice == 4:
        break
