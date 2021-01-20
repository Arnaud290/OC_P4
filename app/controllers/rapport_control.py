"""rapport control module"""
from .controller import Controller
from . import main_menu_control
from ..views.view import View


class RapportControl(Controller):
    """Rapport control class"""
    def __call__(self):
        self.control = None
        self.select = ''
        self.actual_tournaments_list = self.tournaments_list()
        self.actual_rounds_list = self.rounds_list()
        self.actual_players_list = self.players_list()
        self.title_table = None
        self.table = None
        self.table_columns = None
        self.view = View()
        self.rapport_menu()

    def rapport_menu(self):
        """Main menu méthod"""
        while True:
            self.view.add_title_menu("RAPPORTS")
            if self.table:
                self.view.tab_view(self.title_table, self.table, self.table_columns)
            self.view.add_menu_line("List of players")
            self.view.add_menu_line("Quit")
            while True:
                self.select = self.view.choice_menu()
                if self.select not in ('1', '2'):
                    continue
                else:
                    break
            if self.select == '1':
                pass
            if self.select == '2':
                self.control = main_menu_control.MainMenuControl()
                return self.control()
    






        
   