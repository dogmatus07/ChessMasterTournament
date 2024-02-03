from controller import Controller
import time

controller = Controller()

"""
Menu
"""
while True:  # boucle pour le menu principal
    controller.view.clear_screen()
    main_menu_choice = controller.view.display_main_menu()
    if main_menu_choice == 1:
        controller.view.clear_screen()
        while True:  # boucle pour le sous-menu tournoi (1)
            tournament_menu_choice = controller.view.display_menu_tournament()
            if tournament_menu_choice == 1:
                controller.view.clear_screen()
                tournament_infos = controller.view.get_tournament_infos()
                controller.view.display_progress_bar()
                controller.create_tournament(*tournament_infos)
                time.sleep(2)
                controller.view.clear_screen()

            elif tournament_menu_choice == 2:
                controller.view.clear_screen()
                controller.resume_tournament()

            elif tournament_menu_choice == 3:
                controller.view.clear_screen()
                break
            else:
                print("Choix non valide")
    if main_menu_choice == 2:
        while True: # boucle pour le sous-menu joueurs
            controller.view.clear_screen()
            player_menu_choice = controller.view.display_menu_players()
            if player_menu_choice == 1:
                controller.view.clear_screen()
                player_infos = controller.view.get_player_infos()
                controller.view.display_progress_bar()
                controller.create_player(*player_infos)
                time.sleep(2)
                controller.view.clear_screen()

            elif player_menu_choice == 2:
                controller.view.clear_screen()
                pass

            elif player_menu_choice == 3:
                controller.view.clear_screen()
                pass

            elif player_menu_choice == 4:
                controller.view.clear_screen()
                break
    if main_menu_choice == 3:
        while True: # boucle pour le sous-menu rapports
            controller.view.clear_screen()
            menu_report_choice = controller.view.display_menu_report()
            if menu_report_choice == 1:
                controller.view.clear_screen()
                pass

            elif menu_report_choice == 2:
                controller.view.clear_screen()
                pass

            elif menu_report_choice == 3:
                controller.view.clear_screen()
                pass

            elif menu_report_choice == 4:
                controller.view.clear_screen()
                pass

            elif menu_report_choice == 5:
                controller.view.clear_screen()
                break
    if main_menu_choice == 4:
        controller.view.clear_screen()
        break
