"""main menu control module"""
from .new_tournament_controller import NewTournamentController
from .manage_player_controller import ManagePlayerController
from .rounds_controller import RoundsController
from . import rapport_controller
from ..views.view import View
from ..services.get_model_service import GetModelService
from ..services.test_service import TestService


class MainMenuController:
    """main menu control class"""
    def __call__(self):
        self.control = None
        self.actual_tournaments_list = GetModelService.get_model("TournamentModel")
        self.main_menu()

    def menu_display(self):
        View.add_menu_line("Manage Players")
        View.add_menu_line("Rapports")
        View.add_menu_line("Quit")

    def main_menu(self):
        """Main menu méthod"""
        View.add_title_menu("CHESS MAIN MENU")
        if self.actual_tournaments_list:
            if self.actual_tournaments_list[-1].in_progress:
                View.add_menu_line("Continue Tournament")
                self.menu_display()
                if self.actual_tournaments_list[-1].round_list:
                    self.control = RoundsController()
                else:
                    self.control = NewTournamentController()
            else:
                View.add_menu_line("New Tournament")
                self.control = NewTournamentController()
                self.menu_display()
        else:
            self.control = NewTournamentController()

        choice = TestService.test_alpha(test_element=('1', '2', '3', '4'))
        if choice == '1':
            return self.control()
        if choice == '2':
            self.control = ManagePlayerController()
            return self.control()
        if choice == '3':
            self.control = rapport_controller.RapportController()
            return self.control()
        if choice == '4':
            return None
