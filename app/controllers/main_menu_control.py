"""main menu control module"""
from .controller import Controller
from .new_tournament_control import NewTournamentControl
from .manage_player_control import ManagePlayerControl
from .rounds_control import RoundsControl
from ..views.view import View


class MainMenuControl(Controller):
    """main menu control class"""

    def __call__(self):
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
        self.select = self.view.choice_menu()
        if self.select not in ('1', '2', '3', '4'):
            self.control = MainMenuControl()
            self.control()
        else:
            if self.select == '1':
                self.control()
            if self.select == '2':
                self.control = ManagePlayerControl()
                self.control()
            if self.select == '3':
                pass
            if self.select == '4':
                self.view.quit()
