"""main menu control module"""
from .new_tournament_controller import NewTournamentController
from .manage_player_controller import ManagePlayerController
from .rounds_controller import RoundsController
from . import rapport_controller
from ..views.view import View
from ..models.model_template import ModelTemplate


class MainMenuController:
    """main menu control class"""
    def __call__(self):
        self.control = None
        self.select = ''
        self.actual_tournaments_list = ModelTemplate.get_model("TournamentModel")
        self.view = View()
        self.main_menu()

    def main_menu(self):
        """Main menu méthod"""
        self.view.add_title_menu("CHESS MAIN MENU")
        if self.actual_tournaments_list:
            if self.actual_tournaments_list[-1].in_progress:
                self.view.add_menu_line("Continue Tournament")
                if self.actual_tournaments_list[-1].round_list:
                    self.control = RoundsController()
                else:
                    self.control = NewTournamentController()
            else:
                self.view.add_menu_line("New Tournament")
                self.control = NewTournamentController()
        else:
            self.view.add_menu_line("New Tournament")
            self.control = NewTournamentController()
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
            self.control = ManagePlayerController()
            return self.control()
        if self.select == '3':
            self.control = rapport_controller.RapportController()
            return self.control()
        if self.select == '4':
            return None
