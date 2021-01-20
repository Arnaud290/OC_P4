"""main menu control module"""
from .controller import Controller
from .new_tournament_control import NewTournamentControl
from .manage_player_control import ManagePlayerControl
from .rounds_control import RoundsControl
from . import rapport_control
from ..views.view import View


class MainMenuControl(Controller):
    """main menu control class"""
    def __call__(self):
        self.control = None
        self.select = ''
        self.actual_tournaments_list = self.tournaments_list()
        self.view = View()
        self.main_menu()

    def main_menu(self):
        """Main menu méthod"""
        self.view.add_title_menu("CHESS MAIN MENU")
        if self.actual_tournaments_list:
            if self.actual_tournaments_list[-1].in_progress:
                self.view.add_menu_line("Continue Tournament")
                if self.actual_tournaments_list[-1].round_list:
                    self.control = RoundsControl()
                else:
                    self.control = NewTournamentControl()
            else:
                self.view.add_menu_line("New Tournament")
                self.control = NewTournamentControl()
        else:
            self.view.add_menu_line("New Tournament")
            self.control = NewTournamentControl()
        self.view.add_menu_line("Manage Players")
        self.view.add_menu_line("Rapports")
        self.view.add_menu_line("Quit")
        while True:
            self.select = self.view.choice_menu()
            if self.select not in ('1', '2', '3', '4'):
                continue
            else:
                break
        if self.select == '1':
            return self.control()
        if self.select == '2':
            self.control = ManagePlayerControl()
            return self.control()
        if self.select == '3':
            self.control = rapport_control.RapportControl()
            return self.control()
        if self.select == '4':
            return None
