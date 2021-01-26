"""Tournament control module"""
from . import main_menu_controller
from ..services.get_model_service import GetModelService
from .rounds_controller import RoundsController
from ..views.view import View
from ..services.test_service import TestService
from ..services.tournament_service import TournamentService


class TournamentController:
    """Tournament control class"""
    def __call__(self):
        self.control = None
        self.tournament_menu()

    def tournament_menu(self):
        """Method to manage the tournament menu"""
        self.actual_tournaments_list = GetModelService.get_model('TournamentModel')
        if self.actual_tournaments_list:
            if self.actual_tournaments_list[-1].in_progress:
                self.tournament = self.actual_tournaments_list[-1]
                if TournamentService.manage_tournament(self.tournament):
                    self.control = RoundsController()
                else:
                    self.control = main_menu_controller.MainMenuController()
                return self.control()
        View.add_title_menu("NEW TOURNAMENT")
        View.add_menu_line("Create new tournament")
        View.add_menu_line("Quit")
        choice = TestService.test_alpha(test_element=('1', '2'))
        if choice == '1':
            self.tournament = TournamentService.create_tournament()
            if TournamentService.manage_tournament(self.tournament):
                self.control = RoundsController()
            else:
                self.control = main_menu_controller.MainMenuController()
        if choice == '2':
            self.control = main_menu_controller.MainMenuController()
        return self.control()
