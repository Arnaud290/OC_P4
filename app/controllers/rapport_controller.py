"""rapport control module"""
from . import main_menu_controller
from ..views.view import View
from ..models.player_model import PlayerModel
from ..models.tournament_model import TournamentModel
from ..models.round_model import RoundModel
from ..services.get_model_service import GetModelService
from ..services.test_service import TestService
from ..services.table_service import TableService
from ..services.match_service import MatchService
from ..services.tournament_service import TournamentService

class RapportController:
    """Rapport control class"""
    def __call__(self):
        self.control = None
        self.actual_tournaments_list = GetModelService.get_model('TournamentModel')
      
        self.title_table = None
        self.table = []
        self.table_columns = []
        self.tournament = None
        self.rapport_menu()

    def rapport_menu(self):
        """Main menu méthod"""
        while True:
            View.add_title_menu("RAPPORTS")
            TableService.table(
                                title="Tournaments",
                                columns=[
                                        'id',
                                        'name',
                                        'location',
                                        'date',
                                        'nb_players',
                                        'nb_rounds',
                                        'time_control',
                                        'description',
                                        ],  
                                table=GetModelService.get_serialized('TournamentModel')
            )
            View.add_menu_line("List of tournament players")
            View.add_menu_line("List of rounds of a tournament")
            View.add_menu_line("Quit")
            choice = TestService.test_alpha(test_element=('1', '2', '3'))
            if choice == '1':
                self.tournament = TournamentService.select_tournament()
                if self.tournament is None:
                    pass
                else:
                    TournamentService.table_of_tournament_players(self.tournament)
                continue
            if choice == '2':
                self.tournament = TournamentService.select_tournament()
                if self.tournament is None:
                    pass
                else:
                    TournamentService.table_of_tournament_rounds(self.tournament)
                continue
            if choice == '3':
                self.control = main_menu_controller.MainMenuController()
                return self.control()
