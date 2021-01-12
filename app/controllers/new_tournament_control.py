"""main menu control module"""
from . import controller
from . import main_menu_control
from ..models.tournament_model import TournamentModel
from ..views import menu_view, new_tournament_view
from ..config import settings


class NewTournamentControl(controller.Controller):
    """main menu control class"""
        
    def __call__(self):
        self.select = ''
        self.control = None
        self.menu = menu_view.MenuView()
        self.ask = new_tournament_view.NewTournamentView()
        self.new_tournament_menu()

    def new_tournament_menu(self):
        self.menu.add_title_menu("NEW TOURNAMENT")
        self.menu.add_menu_line("Create new tournament")
        self.menu.add_menu_line("Quit")
        self.select = self.menu.get_choice()
        self._choice()

    def _choice(self):
        if self.select not in ('1', '2'):
            self.control = NewTournamentControl()
            self.control()
        else:
            if self.select == '1':
                self.new_tournament()
            if self.select == '2':
                self.control = main_menu_control.MainMenuControl()
                self.control()

    def new_tournament(self):
        self.menu.add_title_menu("CREATE TOURNAMENT")
        tournament = TournamentModel()
        tournament.name = self.ask.request("Name :")
        tournament.location = self.ask.request("Location :")
        while True:
            tournament.nb_players = self.ask.request("Number players (default {}) : ".format(settings.NB_PLAYERS))
            if tournament.nb_players:
                try: 
                    tournament.nb_players = abs(int(tournament.nb_players))
                except ValueError:
                    continue
                else:
                    break
            else:
                tournament.nb_players = int(settings.NB_PLAYERS)
                break
        while True:
            tournament.nb_rounds = self.ask.request("Number rounds (default {}) : ".format(settings.NB_ROUNDS))
            if tournament.nb_rounds:
                try: 
                    tournament.nb_rounds = abs(int(tournament.nb_rounds))
                except ValueError:
                    continue
                else:
                    break
            else:
                tournament.nb_rounds = int(settings.NB_ROUNDS)
                break
        while True:
            tournament.time_control = self.ask.request("Time control (1 : 'bullet', 2: 'blitz' 3: 'coup rapide') : ")
            if tournament.time_control in ('1', '2', '3'):
                if tournament.time_control == '1':
                    tournament.time_control = 'bullet'
                    break
                if tournament.time_control == '2':
                    tournament.time_control = 'blitz'
                    break
                if tournament.time_control == '3':
                    tournament.time_control = 'coup rapide'
                    break
            else:
               continue
        tournament.description = self.ask.request("Description :")
        tournament.in_progress = True
        tournament.save()

