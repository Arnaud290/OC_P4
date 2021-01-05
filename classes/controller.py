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
        Controller.clear()
        tn = Tournament()
        tn.new_tournament()

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
                    View.players_view()
                    try:
                        choice = int((input("\n\n\nENTER ID OF PLAYER OR 0 FOR QUIT : ")))
                    except ValueError:
                        continue
                    else:
                        if not choice in range(0, nb_players):
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
            choice = (input("\n\n\nChoice : "))
            if choice not in ('0', '1'):
                continue
            if choice == '1':
                player = Player()
                serialized_player = {
                                    'id': player.id,
                                    'last_name': player.last_name,
                                    'first_name': player.first_name,
                                    'date_of_birth': player.date_of_birth,
                                    'sex': player.sex,
                                    'rank': player.rank
                                    }
                SaveLoadingData.save_player(serialized_player)
            if choice == '0':
                break
