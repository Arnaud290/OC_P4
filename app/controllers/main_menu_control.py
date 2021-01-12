"""main menu control module"""
from .controller import Controller
from . import new_tournament_control
from ..views import menu_view


class MainMenuControl(Controller):
    """main menu control class"""
        
    def __call__(self):
        self.select = ''
        self.actual_tournaments_list = self.tournaments_list()
        self.control = None
        self.menu = menu_view.MenuView()
        self.main_menu()

    def main_menu(self):   
        self.menu.add_title_menu("CHESS MAIN MENU")
        if self.actual_tournaments_list[-1].in_progress:
            self.menu.add_menu_line("Continue Tournament")
        else:
            self.menu.add_menu_line("New Tournament") 
        self.menu.add_menu_line("Rapports")
        self.menu.add_menu_line("Quit")
        self.select = self.menu.choice_menu()
        self._choice()

    def _choice(self):
        if self.select not in ('1', '2', '3'):
            self.control = MainMenuControl()
            self.control()
        else:
            if self.select == '1':
                if self.actual_tournaments_list[-1].in_progress:
                    pass
                else:
                    self.control = new_tournament_control.NewTournamentControl()
                    self.control()
            if self.select == '2':
                pass
            if self.select == '3':
                self.menu.quit()


