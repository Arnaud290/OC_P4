"""rapport control module"""
from . import main_menu_controller
from ..views.view import View
from ..models.player_model import PlayerModel
from ..models.tournament_model import TournamentModel
from ..models.round_model import RoundModel
from ..services.get_model_service import GetModelService
from ..services.test_service import TestService


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
            self.table_list_of_tournaments()
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

    def table_list_of_tournaments(self):
        self.title_table = "Tournaments"
        self.table = GetModelService.get_serialized('TournamentModel')
        self.table_columns = [
                                'id',
                                'name',
                                'location',
                                'date',
                                'nb_players',
                                'nb_rounds',
                                'time_control',
                                'description',
                            ]  
        return View.tab_view(self.title_table, self.table, self.table_columns)

    def list_of_tournament_players(self, tournament):
        tab_list = tournament.tab_results
        title_table = "Alphabetical order"
        tab_list = sorted(tab_list, key=lambda item: item.get('last_name'), reverse=False) 
        tab_columns = ['first_name', 'last_name', 'tournament_points', 'rank']
        while True:
            View.add_title_menu("PLAYERS LIST OF TOURNAMENT {}".format(tournament.name))
            View.tab_view(title_table, tab_list, tab_columns)
            if title_table == "Alphabetical order":
                View.add_menu_line("For tournament points order")
            if title_table == "Tournament points order":  
                View.add_menu_line("For rank order")
            if title_table == "Rank order":
                View.add_menu_line("For alphabetical order")    
            View.add_menu_line("For quit")
            choice = TestService.test_alpha(test_element=('1', '2'))
            if choice == '1':
                if title_table == "Alphabetical order":
                    title_table = "Tournament points order"
                    tab_list.sort(key=lambda x: (x['tournament_points'], x['rank']), reverse=True) 
                    continue 
                if title_table ==  "Tournament points order":
                    title_table = "Rank order"
                    tab_list.sort(key=lambda x: (x['rank'], x['tournament_points']), reverse=True) 
                    continue
                if title_table == "Rank order":
                    title_table = "Alphabetical order"
                    tab_list = sorted(tab_list, key=lambda item: item.get('last_name'), reverse=False) 
                    continue
            if choice == '2':
                break
    
    def list_of_tournament_rounds(self, tournament):
        rounds_models_list = []
        tab_list = []
        for rounds in self.actual_rounds_list:
            if rounds.id in tournament.round_list:
                rounds_models_list.append(rounds)
                tab_list.append(GetModelService.get_serialized('RoundModel', rounds.id))
        rounds_tab_title = "Rounds list"
        rounds_tab_list = sorted(tab_list, key=lambda item: item.get('name'), reverse=False) 
        rounds_tab_columns = ['name', 'date_start', 'date_finish']
        match_tab_title = None
        match_tab_list = []
        match_tab_columns = ['match number', 'player1', 'score1', 'player2', 'score2']
        while True:
            View.add_title_menu("ROUNDS LIST OF TOURNAMENT {}".format(tournament.name))
            View.tab_view(rounds_tab_title, rounds_tab_list, rounds_tab_columns)
            if match_tab_list:
                View.tab_view(match_tab_title, match_tab_list, match_tab_columns )
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
                match_nb = 1
                for matchs in rounds_models_list[choice - 1].matchs_list:
                    player1 = GetModelService.get_serialized('PlayerModel', matchs[0][0])
                    player2 = GetModelService.get_serialized('PlayerModel', matchs[1][0])
                    match_tab_list.append(
                                    {
                                        'match number': match_nb,
                                        'player1': player1['first_name'] + ' ' + player1['last_name'],
                                        'score1': matchs[0][1],
                                        'player2': player2['first_name'] + ' ' + player2['last_name'],
                                        'score2': matchs[1][1]
                                    }
                                    )
                    match_nb += 1
            if choice == '2':
                break
