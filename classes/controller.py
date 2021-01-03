"""module containing the commands"""
import os
from .models import settings
from .models.tournament import Tournament


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
            print(settings.MENU)
            choice = (input("\n\n\nChoice : "))
            if choice not in ('0', '1', '2', '3'):
                continue
            if choice == '1':
                Controller.cls()
                tn = Tournament()
                tn.new_tournament()
            if choice == '2':
                pass
            if choice == '3':
                pass
            if choice == '0':
                break
