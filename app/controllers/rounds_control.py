"""match control module"""
import time
from .controller import Controller
from . import main_menu_control
from ..views.view import View
from ..models.player_model import PlayerModel
from . import manage_player_control

class RoundsControl(Controller):
    """Rounds control class"""
    def __call__(self):
        self.select = ''
        self.in_progress = True
        self.all_players_list = self.players_list()
        self.actual_tournaments_list = self.tournaments_list()
        self.tournament = self.actual_tournaments_list[-1]
        self.t_players = []
        self.view = View()
        self.control = None
        self.rounds_engine()
            
    def rounds_engine(self):
        """Round menu method"""
        if not self.in_progress:
            self.control = main_menu_control.MainMenuControl()
            self.control()
        else:
            self.t_rounds = []
            self.rounds_model_list = self.rounds_list()
            for round_model in self.rounds_model_list:
                if round_model.id in self.tournament.round_list:
                   self.t_rounds.append(round_model) 
                for rounds in self.t_rounds:
                    if rounds.finish == False:
                        self.rounds = round_model
                        break
                if not self.rounds.start and not self.rounds.matchs_list:
                    self.create_rounds_matchs()
                    self.rounds_menu()
                if self.rounds.start and self.rounds.matchs_list:
                    self.rounds_menu()
                    break 
            for rounds in self.t_rounds:
                if rounds.finish:
                    self.in_progress = False
                else:
                    self.in_progress = True

    def rounds_menu(self):
        title_menu = "Tournament : {}".format(self.tournament.name)
        self.view.add_title_menu(title_menu)
        self.t_players = []
        for player in self.all_players_list:
            if player.id in self.tournament.player_list:
                self.t_players.append(player)
        tab_t_players = []
        for player in self.t_players:
            tab_t_players.append(PlayerModel.get_id_serialized(player.id))
        elements_columns = ['id', 'first_name', 'last_name','tournament_points', 'rank']
        self.view.tab_view("Tournament Players", tab_t_players, elements_columns)     
        tab_r_matchs = []
        match_nb = 1
        for matchs in self.rounds.matchs_list:
            player1 = PlayerModel.get_id_serialized(matchs[0][0])
            player2 = PlayerModel.get_id_serialized(matchs[1][0])
            tab_r_matchs.append(
                                {
                                    'match number': match_nb,
                                    'player1': player1['first_name'] + ' ' + player1['last_name'],
                                    'score1': matchs[0][1], 
                                    'player2': player2['first_name'] + ' ' + player2['last_name'],
                                    'score2': matchs[1][1]
                                }
                                )
            match_nb += 1
        elements_columns = ['match number', 'player1', 'score1', 'player2', 'score2']
        self.view.tab_view("Round {}".format(self.rounds.count), tab_r_matchs, elements_columns)
        if not self.rounds.start:
            self.view.add_menu_line("Start Round")
        else:    
            self.view.add_menu_line("Finish Match ?")
        self.view.add_menu_line("Manage players tournament")
        self.view.add_menu_line("Quit")
        self.select = self.view.get_choice()
        if self.select not in ('1', '2', '3'):
            pass
        if self.select == '1':
            if not self.rounds.start:
                self.rounds.start = True
                self.rounds.update('start', self.rounds.start)
                self.rounds.date_start = time.strftime("%d/%m/%Y %H:%M:%S")
                self.rounds.update('date_start', self.rounds.date_start)
                self.rounds_engine()
            else:
                while True:
                    choice = self.view.request("Enter match number or Q for quit: ").upper()
                    if choice == 'Q':
                        break
                    try:
                        choice = int(choice) - 1
                    except ValueError:
                        continue
                    if choice not in range(len(self.rounds.matchs_list)) or choice in self.rounds.finish_matchs:
                        continue
                    else:
                        while True:
                            result = self.view.request("Enter 1 : player1_win, 2 : player2_win, 3 : draw")
                            if result not in ('1', '2', '3'):
                                continue
                            else:
                                self.match_management(choice, result)
                                break
                        break
                self.rounds_engine()
        if self.select == '2':
            self.control = manage_player_control.ManagePlayerControl()
            self.control.modify_player(self.t_players)
            self.rounds_engine()
        if self.select == '3':
            while True:
                choice = self.view.request("quit by deleting the tournament? (Y or N)").upper()
                if choice not in ('Y', 'N'):
                    continue
                if choice == 'Y':
                    self.tournament.delete()
                    for rounds in self.t_rounds:
                        rounds.delete()
                    self.in_progress = False
                    break
                if choice == 'N':
                    self.in_progress = False
                    break  
            self.rounds_engine()

    def create_rounds_matchs(self):
        """create matchs round method"""
        players_for_match = self.t_players
        if self.rounds.count == 1:
            players_for_match.sort(key=lambda x: x.rank, reverse=True)
            while players_for_match:
                middle = int(len(players_for_match)/2)
                match = ([players_for_match[0].id, 0], [players_for_match[middle].id, 0])
                self.rounds.matchs_list.append(match)
                self.rounds.update('matchs_list', self.rounds.matchs_list)
                players_for_match[0].vs.append(players_for_match[middle].id)
                players_for_match[0].update('vs', players_for_match[0].vs)
                players_for_match[middle].vs.append(players_for_match[0].id)
                players_for_match[middle].update('vs', players_for_match[middle].vs)
                del players_for_match[0]
                try:
                    del players_for_match[middle - 1]
                except IndexError:
                     del players_for_match[0]
        else:
            players_for_match.sort(key=lambda x: x.tournament_points, reverse=True)
            while players_for_match:
                player = 1
            while players_for_match[0].id in players_for_match[player].vs:
                player += 1
            match = ([players_for_match[0].id, 0], [players_for_match[player].id, 0])
            self.rounds.matchs_list.append(match)
            self.rounds.update('matchs_list', self.rounds.matchs_list)
            players_for_match[0].vs.append(players_for_match[player].id)
            players_for_match[0].update('vs', players_for_match[0].vs)
            players_for_match[player].vs.append(players_for_match[0].id)
            players_for_match[player].update('vs', players_for_match[player].vs)
            del players_for_match[0]
            del players_for_match[player]
       
    def match_management(self, match_nb, result):
        """match management method"""
        if result == '1':
            self.rounds.matchs_list[match_nb][0][1] += 1
            for player in self.t_players:
                if player.id == self.rounds.matchs_list[match_nb][0][0]:
                    player.tournament_points += 1
                    player.update('tournament_points', player.tournament_points)
        if result == '2':
            self.rounds.matchs_list[match_nb][1][1] += 1
            for player in self.t_players:
                if player.id == self.rounds.matchs_list[match_nb][1][0]:
                    player.tournament_points += 1
                    player.update('tournament_points', player.tournament_points)
        if result == '3':
            self.rounds.matchs_list[match_nb][0][1] += 0.5
            self.rounds.matchs_list[match_nb][1][1] += 0.5
            for player in self.t_players:
                if player.id == self.rounds.matchs_list[match_nb][0][0]:
                    player.tournament_points += 0.5
                    player.update('tournament_points', player.tournament_points)
            for player in self.t_players:
                if player.id == self.rounds.matchs_list[match_nb][1][0]:
                    player.tournament_points += 0.5
                    player.update('tournament_points', player.tournament_points)
        self.rounds.update('matchs_list', self.rounds.matchs_list)
        self.rounds.finish_matchs.append(match_nb)
        self.rounds.update('match_nb', self.rounds.finish_matchs)
        if  len(self.rounds.finish_matchs) == len(self.rounds.matchs_list):
             self.rounds.start == False
             self.rounds.update('start', self.rounds.start)
             self.rounds.finish == True
             self.rounds.update('finish', self.rounds.finish)
