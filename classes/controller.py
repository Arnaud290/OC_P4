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
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def launch_menu():
        """Sequencer attribute"""
        Controller.cls()
        print(settings.TITLE)
        while True:
            Controller.cls()
            print(settings.MAIN_MENU)
            choice = (input("\n\n\nChoice : "))
            if choice not in ('0', '1', '2', '3'):
                continue
            if choice == '1':
                Controller.tournament()
            if choice == '2':
                Controller.manage_players()
            if choice == '3':
                Controller.cls()
                pass
            if choice == '0':
                Controller.cls()
                break

    @staticmethod
    def tournament():
        Controller.cls()
        tn = Tournament()
        tn.new_tournament()

    @staticmethod
    def manage_players():
        Controller.cls()
        print(settings.MANAGE_PLAYERS_MENU)
        choice = (input("\n\n\nChoice : "))
        if choice == '1':
            Controller.cls()
            player = Player()
            serialized_player = {
                                'last_name' : player.last_name,
                                'first_name' : player.first_name,
                                'date_of_birth' : player.date_of_birth,
                                'sex' : player.sex,
                                'rank' : player.rank
                                }
            SaveLoadingData.save_player(serialized_player)
        if choice == '2':
            Controller.cls()
            View.players_view()
            choice = int((input("\n\n\nENTER ID OF PLAYER : ")))
            serialized_players = SaveLoadingData.load_players()
            for key, value in serialized_players[choice].items():
                change_value = input("want to change {} ? Actual : {}".format(key, value))
                if change_value:
                    

        if choice == '0':
            pass

    

