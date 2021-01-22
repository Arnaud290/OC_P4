"""rapport control module"""
from .controller import Controller
from . import main_menu_controller
from ..views.view import View
from ..models.player_model import PlayerModel
from ..models.tournament_model import TournamentModel
from ..models.round_model import RoundModel


class RapportController(Controller):
    """Rapport control class"""
    def __call__(self):
        self.control = None
        self.select = ''
        self.actual_tournaments_list = self.tournaments_list()
        self.actual_rounds_list = self.rounds_list()
        self.title_table = None
        self.table = []
        self.table_columns = []
        self.view = View()
        self.rapport_menu()

    def rapport_menu(self):
        """Main menu méthod"""
        while True:
            self.view.add_title_menu("RAPPORTS")
            self.table_list_of_tournaments()
            self.view.add_menu_line("List of tournament players")
            self.view.add_menu_line("List of rounds of a tournament")
            self.view.add_menu_line("Quit")
            while True:
                self.select = self.view.choice_menu()
                if self.select not in ('1', '2', '3'):
                    continue
                else:
                    break
            if self.select == '1':
                tournament = self.select_tournament()
                self.list_of_tournament_players(tournament)
                continue
            if self.select == '2':
                tournament = self.select_tournament()
                self.list_of_tournament_rounds(tournament)
                continue
            if self.select == '3':
                self.control = main_menu_controller.MainMenuController()
                return self.control()

    def select_tournament(self):
        while True:
            choice = self.view.request("Enter id of tournament").upper()
            try:
                choice = abs(int(choice))
            except ValueError:
               continue
            else:
                if choice not in range(len(self.actual_tournaments_list)):
                    continue
                else:
                    for tournament_model in self.actual_tournaments_list:
                        if tournament_model.id == choice:
                            tournament = tournament_model
                    return tournament

    def table_list_of_tournaments(self):
        self.title_table = "Tournaments"
        self.table = TournamentModel.get_serialized()
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
        return self.view.tab_view(self.title_table, self.table, self.table_columns)

    def list_of_tournament_players(self, tournament):
        tab_list = tournament.tab_results
        title_table = "Alphabetical order"
        tab_list = sorted(tab_list, key=lambda item: item.get('last_name'), reverse=False) 
        tab_columns = ['first_name', 'last_name', 'tournament_points', 'rank']
        while True:
            self.view.add_title_menu("PLAYERS LIST OF TOURNAMENT {}".format(tournament.name))
            self.view.tab_view(title_table, tab_list,  tab_columns)
            if title_table == "Alphabetical order":
                self.view.add_menu_line("For tournament points order")
            if title_table == "Tournament points order":  
                self.view.add_menu_line("For rank order")
            if title_table == "Rank order":
                self.view.add_menu_line("For alphabetical order")    
            self.view.add_menu_line("For quit")
            choice = self.view.get_choice()
            if choice not in ('1', '2'):
                continue
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
                tab_list.append(RoundModel.get_id_serialized(rounds.id))
        rounds_tab_title = "Rounds list"
        rounds_tab_list = sorted(tab_list, key=lambda item: item.get('name'), reverse=False) 
        rounds_tab_columns = ['name', 'date_start', 'date_finish']
        match_tab_title = None
        match_tab_list = []
        match_tab_columns = ['match number', 'player1', 'score1', 'player2', 'score2']
        while True:
            self.view.add_title_menu("ROUNDS LIST OF TOURNAMENT {}".format(tournament.name))
            self.view.tab_view(rounds_tab_title, rounds_tab_list, rounds_tab_columns)
            if match_tab_list:
                self.view.tab_view(match_tab_title, match_tab_list, match_tab_columns )
                match_tab_list = []
            self.view.add_menu_line("For show matchs")
            self.view.add_menu_line("For quit")
            choice = self.view.get_choice()
            if choice not in ('1', '2'):
                continue
            if choice == '1':
                choice = self.view.request("Enter round number")
                try:
                    choice = abs(int(choice))
                except ValueError:
                    continue
                else:
                    if choice not in range(1, len(tournament.round_list) + 1):
                        continue
                    else:
                        match_tab_title = rounds_models_list[choice - 1].name
                        match_nb = 1
                        for matchs in rounds_models_list[choice - 1].matchs_list:
                            player1 = PlayerModel.get_id_serialized(matchs[0][0])
                            player2 = PlayerModel.get_id_serialized(matchs[1][0])
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
