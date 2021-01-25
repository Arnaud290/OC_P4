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
        
    def main_menu(self):
        """Main menu method"""
        View.add_title_menu("CHESS MAIN MENU")
        if self.actual_tournaments_list:
            if self.actual_tournaments_list[-1].in_progress:
                View.add_menu_line("Continue Tournament")
                if self.actual_tournaments_list[-1].round_list:
                    self.control = RoundsController()
                else:
                    self.control = NewTournamentController()
            else:
                View.add_menu_line("New Tournament")
                self.control = NewTournamentController()        
        else:
            View.add_menu_line("New Tournament")
            self.control = NewTournamentController()
        View.add_menu_line("Manage Players")
        View.add_menu_line("Rapports")
        View.add_menu_line("Quit")
        choice = TestService.test_alpha(test_element=('1', '2', '3', '4'))
        if choice == '1':
            return self.control()
        if choice == '2':
            self.control = ManagePlayerController()
        if choice == '3':
            self.control = rapport_controller.RapportController()
        if choice == '4':
            return None
        return self.control()