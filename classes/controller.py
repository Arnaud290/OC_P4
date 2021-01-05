"""module containing the commands"""
import os
from .models import settings
from .models.tournament import Tournament
from .models.player import Player
from .models.save_loading_data import SaveLoadingData
from .view import View


class Controller:
    """User command control class"""
    def __init__(self):
        Controller.launch_menu()

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def launch_menu():
        """Sequencer attribute"""
        Controller.clear()
        print(settings.TITLE)
        while True:
            Controller.clear()
            print(settings.MAIN_MENU)
            choice = (input("\n\n\nChoice : "))
            if choice not in ('0', '1', '2', '3'):
                continue
            if choice == '1':
                Controller.tournament()
            if choice == '2':
                Controller.manage_players()
            if choice == '3':
                Controller.clear()
                pass
            if choice == '0':
                Controller.clear()
                break

    @staticmethod
    def tournament():
        while True:
            Controller.clear()
            print(settings.NEW_TOURNAMENT_MENU)
            choice = (input("\n\n\nChoice : "))
            if choice not in ('0', '1',):
                continue
            if choice == '1':
                tournament = Tournament()
                tournament.new_tournament()
                while True:
                    Controller.clear()
                    print(settings.START_TOURNAMENT_MENU)
                    choice = (input("\n\n\nChoice : "))
                    if choice not in ('0', '1',):
                        continue
                    if choice == '1':
                        tournament.start_tournament()
                        Controller.clear()
                        SaveLoadingData.save_tournament(tournament.serialized_tournament())
                        print("TOURNAMENT {} IN PROGRESS".format(tournament.name))
                        
                        


                        input("\n\nPRESS ENTER TO CONTINUE...")
                    if choice == '0':
                        break
            if choice == '0':
                break

    @staticmethod
    def manage_players():
        while True:
            Controller.clear()
            print(settings.MANAGE_PLAYERS_MENU)
            choice = (input("\n\n\nChoice : "))
            if choice not in ('0', '1', '2'):
                continue
            if choice == '1':
                Controller.new_player()
            if choice == '2':
                nb_players = SaveLoadingData.nb_players() + 1
                while True:
                    Controller.clear()
                    list_players = SaveLoadingData.load_player()
                    print(View.tab_view(list_players))
                    try:
                        choice = int((input("\n\n\nENTER ID OF PLAYER OR 0 FOR QUIT : ")))
                    except ValueError:
                        continue
                    else:
                        if choice not in range(0, nb_players):
                            continue
                        if choice == 0:
                            break
                        if choice in range(1, nb_players):
                            Controller.clear()
                            serialized_players = SaveLoadingData.load_player()
                            for key, value in serialized_players[choice - 1].items():
                                if key != 'id':
                                    change_value = input("want to change {} ? Actual ({}) : ".format(key, value))
                                    if change_value:
                                        serialized_players[choice - 1][key] = change_value
                            SaveLoadingData.save_player(serialized_players)
            if choice == '0':
                break

    @staticmethod
    def new_player():
        while True:
            Controller.clear()
            print(settings.NEW_PLAYER_MENU)
            print("\nLIST OF PLAYERS\n")
            list_players = SaveLoadingData.load_player()
            print(View.tab_view(list_players))
            choice = (input("\n\n\nChoice : "))
            if choice not in ('0', '1'):
                continue
            if choice == '1':
                player = Player()
                player.new_player()
                
                SaveLoadingData.save_player(serialized_player)
            if choice == '0':
                break
