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

class RapportController:
    """Rapport control class"""
    def __call__(self):
        self.control = None
        self.actual_tournaments_list = GetModelService.get_model('TournamentModel')
        self.actual_rounds_list = GetModelService.get_model('RoundModel')
        self.title_table = None
        self.table = []
        self.table_columns = []
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
                tournament = self.select_tournament()
                self.list_of_tournament_players(tournament)
                continue
            if choice == '2':
                tournament = self.select_tournament()
                self.list_of_tournament_rounds(tournament)
                continue
            if choice == '3':
                self.control = main_menu_controller.MainMenuController()
                return self.control()

    def select_tournament(self):
        choice = TestService.test_num(
                                    title="Enter id of tournament",
                                    test_range_element=len(self.actual_tournaments_list)
                                    )
        tournament = GetModelService.get_model('TournamentModel', choice)
        return tournament

    def list_of_tournament_players(self, tournament):
        table_sort = "Alphabetical order"
        while True:
            View.add_title_menu("PLAYERS LIST OF TOURNAMENT {}".format(tournament.name))
            TableService.table(
                                title=table_sort,
                                columns=['first_name', 'last_name', 'tournament_points', 'rank'],
                                table=tournament.results,
                                select_sort=table_sort
                            )
            TableService.table_sort_menu('tournament_player_table', table_sort)
            View.add_menu_line("For quit")
            choice = TestService.test_alpha(test_element=('1', '2'))
            if choice == '1':
                table_sort = TableService.table_sort_select('tournament_player_table', table_sort)
            if choice == '2':
                break
    
    def list_of_tournament_rounds(self, tournament):
        rounds_models_list = []
        tab_list = []
        for rounds in self.actual_rounds_list:
            if rounds.id in tournament.round_list:
                rounds_models_list.append(rounds)
                tab_list.append(GetModelService.get_serialized('RoundModel', rounds.id))
        match_tab_title = None
        match_tab_list = []
        while True:
            View.add_title_menu("ROUNDS LIST OF TOURNAMENT {}".format(tournament.name))
            TableService.table( 
                                title="Rounds list",
                                columns=['name', 'date_start', 'date_finish'],
                                table=tab_list,
                                select_sort='Round_name'
                            )
            
            
            TableService.table(
                                title=match_tab_title,
                                columns=['id', 'player1', 'score1', 'player2', 'score2'],
                                table=match_tab_list
                            )
            match_tab_list = []
            View.add_menu_line("For show matchs")
            View.add_menu_line("For quit")
            choice = TestService.test_alpha(test_element=('1', '2'))
            if choice == '1':
                choice = TestService.test_num(
                                            title="Enter round number",
                                            modif_num=-1,
                                            test_range_element=len(tournament.round_list)
                                            )     
                match_tab_title = rounds_models_list[choice].name
                match_tab_list = MatchService.match_list_tab(rounds_models_list[choice - 1].matchs_list)
            if choice == '2':
                break
