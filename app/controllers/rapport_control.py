"""rapport control module"""
from .controller import Controller
from . import main_menu_control
from ..views.view import View
from ..models.player_model import PlayerModel
from ..models.tournament_model import TournamentModel
from ..models.round_model import RoundModel


class RapportControl(Controller):
    """Rapport control class"""
    def __call__(self):
        self.control = None
        self.select = ''
        self.actual_tournaments_list = self.tournaments_list()
        self.actual_rounds_list = self.rounds_list()
        self.actual_players_list = self.players_list()
        self.title_table = None
        self.table = []
        self.table_columns = []
        self.view = View()
        self.rapport_menu()

    def rapport_menu(self):
        """Main menu méthod"""
        while True:
            self.view.add_title_menu("RAPPORTS")
            self.view.add_menu_line("List of players")
            self.view.add_menu_line("List of tournament players")
            self.view.add_menu_line("List of tournaments")
            self.view.add_menu_line("list of rounds of a tournament")
            self.view.add_menu_line("list of matchs of a tournament")
            self.view.add_menu_line("Quit")
            while True:
                self.select = self.view.choice_menu()
                if self.select not in ('1', '2', '3', '4', '5', '6'):
                    continue
                else:
                    break
            if self.select == '1':
                players_list = PlayerModel.get_serialized()
                table_columns = ['id', 'first_name', 'last_name', 'birth_date', 'sex', 'rank']
                self.list_of_players(players_list, table_columns)
                continue
            if self.select == '2':
                self.list_of_tournament_players()
                continue
            if self.select == '3':
                self.list_of_tournaments()
                continue
            if self.select == '4':
                self.list_of_tournament_rounds()
                continue
            if self.select == '5':
                pass
            if self.select == '6':
                self.control = main_menu_control.MainMenuControl()
                return self.control()

    def list_of_players(self, players_list, table_columns):
        self.title_table = "Alphabetical order"
        self.table = players_list
        self.table_columns = table_columns
        self.table = sorted(self.table, key=lambda item: item.get('last_name'), reverse=False)
        while True:  
            self.view.add_title_menu("LIST OF PLAYERS")
            self.view.tab_view(self.title_table, self.table, self.table_columns)
            if self.title_table == "Alphabetical order":
                self.view.indication("Enter 1 for rank order")
            else:
                self.view.indication("Enter 1 for alphabetical order")
            self.view.indication("Enter 2 for quit")
            while True:
                choice = self.view.get_choice()
                if choice not in ('1', '2'):
                    continue
                else:
                    break
            if choice == '1':
                if self.title_table == "Alphabetical order":
                    self.title_table = "Rank order"
                    self.table.sort(key=lambda x: (x['tournament_points'], x['rank']), reverse=True)   
                else:
                    self.title_table = "Alphabetical order"
                    self.table = sorted(self.table, key=lambda item: item.get('last_name'), reverse=False)
            if choice == '2':
                break

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

    def list_of_tournament_players(self):
        tournament_players_list = []
        in_progress = True
        while in_progress:
            self.view.add_title_menu("LIST OF TOURNAMENT PLAYERS")
            self.table_list_of_tournaments()
            while True:
                choice = self.view.request("Enter id of tournament or Q for quit").upper()
                try:
                    choice = abs(int(choice))
                except ValueError:
                    if choice != 'Q':
                        continue
                    else:
                        in_progress = False
                        break
                else:
                    if choice not in range(len(self.table)):
                        continue
                    else:
                        tournament = TournamentModel.get_id_serialized(choice)
                        rounds_list = []
                        for rounds in tournament['round_list']:
                            rounds_list.append(RoundModel.get_id_serialized(rounds))
                        matchs_list = []
                        for rounds in rounds_list:
                            for matchs in rounds['matchs_list']:
                                matchs_list.append(matchs)
                        players_list = []
                        for players in tournament['player_list']:
                            players_list.append(PlayerModel.get_id_serialized(players))
                        for player in players_list:
                            tournament_points = 0
                            for matchs in matchs_list:
                                if matchs[0][0] == player['id']:
                                    tournament_points += matchs[0][1]
                                if matchs[1][0] == player['id']:
                                    tournament_points += matchs[1][1]
                            player['tournament_points'] = tournament_points
                        table_columns = ['id', 'first_name', 'last_name', 'rank' ,'tournament_points']   
                        self.list_of_players(players_list, table_columns)
                        break

    def list_of_tournaments(self):
         self.view.add_title_menu("LIST OF TOURNAMENTS")
         self.table_list_of_tournaments()
         while True:
            choice = self.view.request("Enter Q for quit").upper()
            if choice != 'Q':
                continue
            else:
                break
            pass
    
    def list_of_tournament_rounds(self):
        in_progress = True
        while in_progress:
            self.view.add_title_menu("LIST OF TOURNAMENT ROUNDS")
            self.table_list_of_tournaments()
            while True:
                choice = self.view.request("Enter id of tournament or Q for quit").upper()
                try:
                    choice = abs(int(choice))
                except ValueError:
                    if choice != 'Q':
                        continue
                    else:
                        in_progress = False
                        break
                else:
                    if choice not in range(len(self.table)):
                        continue
                    else:
                        tournament = TournamentModel.get_id_serialized(choice)
                        rounds_list = []
                        for rounds in tournament['round_list']:
                            rounds_list.append(RoundModel.get_id_serialized(rounds))
                        self.view.add_title_menu("LIST OF ROUNDS FOR TOURNAMENT {}".format(tournament['name']))
                        self.title_table = "Rounds"
                        self.table = rounds_list
                        self.table_columns = ['id', 'name', 'date_start', 'date_finish']
                        self.view.tab_view(self.title_table, self.table, self.table_columns)
                        while True:
                            choice = self.view.request("Enter Q for quit").upper()
                            if choice != 'Q':
                                continue
                            else:
                                break
                        break