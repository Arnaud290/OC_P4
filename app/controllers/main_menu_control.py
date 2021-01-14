"""main menu control module"""
from .controller import Controller
from .new_tournament_control import NewTournamentControl
from .rounds_control import RoundsControl
from ..views import menu_view


class MainMenuControl(Controller):
    """main menu control class"""

    def __call__(self):
        self.select = ''
        self.actual_tournaments_list = self.tournaments_list()
        self.menu = menu_view.MenuView()
        self.main_menu()

    def main_menu(self):
        """Main menu méthod"""
        self.menu.add_title_menu("CHESS MAIN MENU")
        if self.actual_tournaments_list:
            if self.actual_tournaments_list[-1].in_progress:
                self.menu.add_menu_line("Continue Tournament")
                if self.actual_tournaments_list[-1].round_list:
                    self.control = RoundsControl()
                else:
                   self.control = NewTournamentControl()
            else:
                self.menu.add_menu_line("New Tournament")
                self.control = NewTournamentControl()
        else:
            self.menu.add_menu_line("New Tournament")
            self.control = NewTournamentControl()
        self.menu.add_menu_line("Rapports")
        self.menu.add_menu_line("Quit")
        self.select = self.menu.choice_menu()
        if self.select not in ('1', '2', '3'):
            self.control = MainMenuControl()
            self.control()
        else:
            if self.select == '1':
                self.control()
            if self.select == '2':
                pass
            if self.select == '3':
                self.menu.quit()
