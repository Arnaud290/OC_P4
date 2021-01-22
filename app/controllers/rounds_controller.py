"""match control module"""
import time
import operator
from .controller import Controller
from . import main_menu_controller
from ..views.view import View
from ..models.player_model import PlayerModel
from . import manage_player_controller


class RoundsController(Controller):
    """Rounds control class"""
    def __call__(self):
        self.select = ''
        self.in_progress = True
        self.actual_tournaments_list = self.tournaments_list()
        self.tournament = self.actual_tournaments_list[-1]
        self.view = View()
        self.control = None
        self.rounds = None
        self.delete_tournament = False
        self.rounds_engine()

    def tournament_players_list(self):
        all_players_list = self.players_list()
        t_players = []
        for player in all_players_list:
            if player.id in self.tournament.player_list:
                t_players.append(player)
        return t_players

    def tournament_rounds_list(self):
        rounds_model_list = self.rounds_list()
        t_rounds = []
        for round_model in rounds_model_list:
            if round_model.id in self.tournament.round_list:
                t_rounds.append(round_model)
        return t_rounds

    def rounds_engine(self):
        """Round menu method"""
        t_rounds = self.tournament_rounds_list()
        while t_rounds and self.tournament:
            self.rounds = t_rounds.pop(0)
            while not self.rounds.finish and self.in_progress:
                if not self.rounds.start and not self.rounds.matchs_list:
                    self.create_rounds_matchs()
                    self.rounds_menu()
                    continue
                if not self.rounds.start and self.rounds.matchs_list and not self.rounds.finish:
                    self.rounds_menu()
                    continue
                if self.rounds.start and not self.rounds.finish:
                    self.rounds_menu()
                    continue
        if not self.tournament and not self.in_progress:
            self.control = main_menu_controller.MainMenuController()
            return self.control()
        if not t_rounds and self.in_progress:
            title_menu = "Tournament : {} is finish !".format(self.tournament.name)
            self.view.add_title_menu(title_menu)
            t_players = self.tournament_players_list()
            elements_columns = ['first_name', 'last_name', 'tournament_points', 'rank']
            self.view.tab_view("Tournament Players", self.tournament.tab_results , elements_columns)
            for player in t_players:
                player.tournament_points = 0.0
                player.update('tournament_points', player.tournament_points)
            self.tournament.in_progress = False
            self.tournament.update('in_progress', self.tournament.in_progress)
            self.clear_players_points()
            self.view.pause()
            self.control = main_menu_controller.MainMenuController()
            return self.control()
        else:
            self.control = main_menu_controller.MainMenuController()
            return self.control()

    def tab_results(self):
        t_players = self.tournament_players_list()
        tab_t_players = []
        for player in t_players:
                tab_t_players.append(PlayerModel.get_id_serialized(player.id))
                tab_t_players.sort(key=lambda x: (x['tournament_points'], x['rank']), reverse=True)
        return tab_t_players
           


    def clear_players_points(self):
        t_players = self.tournament_players_list()
        for player in t_players:
            player.tournament_points = 0.0
            player.update('tournament_points', player.tournament_points)
            player.vs = []
            player.no_vs = []
            player.update('vs', player.vs)
            player.update('no_vs', player.no_vs)

    def rounds_tab(self):
        title_menu = "Tournament : {}".format(self.tournament.name)
        self.view.add_title_menu(title_menu)
        tab_t_players = []
        t_players = self.tournament_players_list()
        for player in t_players:
            tab_t_players.append(PlayerModel.get_id_serialized(player.id))
        elements_columns = ['tournament_points', 'rank', 'first_name', 'last_name', 'id']
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

    def rounds_menu(self):
        self.rounds_tab()
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
        if self.select == '2':
            t_players = self.tournament_players_list()
            self.control = manage_player_controller.ManagePlayerController()
            self.control.modify_player(t_players)
        if self.select == '3':
            while True:
                choice = self.view.request("quit by deleting the tournament? (Y or N)").upper()
                if choice not in ('Y', 'N'):
                    continue
                else:
                    break
            if choice == 'Y':
                t_players = self.tournament_players_list()
                t_rounds = self.tournament_rounds_list()
                for rounds in t_rounds:
                    rounds.delete()
                self.tournament.delete()
                self.clear_players_points()
                self.in_progress = False
                self.tournament = False
            if choice == 'N':
                self.in_progress = False

    def create_rounds_matchs(self):
        """create matchs round method"""
        t_players_id = []
        p_match = self.tournament_players_list()
        p_match.sort(key=operator.attrgetter('tournament_points', 'rank'), reverse=True)
        for player in p_match:
            t_players_id.append(player.id)
        for player in p_match:
            player.no_vs = []
            for id_player in t_players_id:
                if player.id != id_player and id_player not in player.vs:
                    player.no_vs.append(id_player)
            player.update('no_vs', player.no_vs)
        if self.rounds.count == 1:
            while p_match:
                middle = int(len(p_match)/2)
                player_1 = p_match[0]
                player_2 = p_match[middle]
                player_1.vs.append(player_2.id)
                player_1.update('vs', player_1.vs)
                player_2.vs.append(player_1.id)
                player_2.update('vs', player_2.vs)
                match = ([player_1.id, 0], [player_2.id, 0])
                self.rounds.matchs_list.append(match)
                del p_match[middle]
                del p_match[0]
            self.rounds.update('matchs_list', self.rounds.matchs_list)
        else:
            pos_player = 0
            while True:
                p_match.sort(key=operator.attrgetter('tournament_points', 'rank'), reverse=True)
                player_1 = p_match[pos_player]
                del p_match[pos_player]
                for player_model in p_match:
                    try:
                        if player_model.id == player_1.no_vs[pos_player]:
                            player_2 = player_model
                            p_match.remove(player_model)
                            break
                    except IndexError:
                        if player_model.id == player_1.no_vs[-1]:
                            player_2 = player_model
                            p_match.remove(player_model)
                            break
                player_1.vs.append(player_2.id)
                player_1.update('vs', player_1.vs)
                player_2.vs.append(player_1.id)
                player_2.update('vs', player_2.vs)
                match = ([player_1.id, 0], [player_2.id, 0])
                self.rounds.matchs_list.append(match)
                while p_match:
                    player_1 = p_match[0]
                    del p_match[0]
                    for player_model in p_match:
                        if player_model.id in player_1.no_vs:
                            player_2 = player_model
                            p_match.remove(player_model)
                            break
                    player_1.vs.append(player_2.id)
                    player_1.update('vs', player_1.vs)
                    player_2.vs.append(player_1.id)
                    player_2.update('vs', player_2.vs)
                    match = ([player_1.id, 0], [player_2.id, 0])
                    self.rounds.matchs_list.append(match)
                if len(self.rounds.matchs_list) > int(self.tournament.nb_players/2):
                    p_match = self.tournament_players_list()
                    for player in p_match:
                        while len(player.vs) >= self.rounds.count:
                            del player.vs[-1]
                            player.update('vs', player.vs)
                    self.rounds.matchs_list = []
                    self.rounds.update('matchs_list', self.rounds.matchs_list)
                    pos_player += 1
                    continue
                else:
                    self.rounds.update('matchs_list', self.rounds.matchs_list)
                    break

    def match_management(self, match_nb, result):
        """match management method"""
        t_players = self.tournament_players_list()
        if result == '1':
            self.rounds.matchs_list[match_nb][0][1] += 1
            for player in t_players:
                if player.id == self.rounds.matchs_list[match_nb][0][0]:
                    player.tournament_points += 1
                    player.update('tournament_points', player.tournament_points)
        if result == '2':
            self.rounds.matchs_list[match_nb][1][1] += 1
            for player in t_players:
                if player.id == self.rounds.matchs_list[match_nb][1][0]:
                    player.tournament_points += 1
                    player.update('tournament_points', player.tournament_points)
        if result == '3':
            self.rounds.matchs_list[match_nb][0][1] += 0.5
            self.rounds.matchs_list[match_nb][1][1] += 0.5
            for player in t_players:
                if player.id == self.rounds.matchs_list[match_nb][0][0]:
                    player.tournament_points += 0.5
                    player.update('tournament_points', player.tournament_points)
            for player in t_players:
                if player.id == self.rounds.matchs_list[match_nb][1][0]:
                    player.tournament_points += 0.5
                    player.update('tournament_points', player.tournament_points)
        self.rounds.update('matchs_list', self.rounds.matchs_list)
        self.rounds.finish_matchs.append(match_nb)
        self.rounds.update('finish_matchs', self.rounds.finish_matchs)
        if len(self.rounds.finish_matchs) == int(self.tournament.nb_players/2):
            self.rounds.start = False
            self.rounds.update('start', self.rounds.start)
            self.rounds.finish = True
            self.rounds.update('finish', self.rounds.finish)
            self.rounds.date_finish = time.strftime("%d/%m/%Y %H:%M:%S")
            self.rounds.update('date_finish', self.rounds.date_finish)
            self.tournament.tab_results = self.tab_results()
            self.tournament.update('tab_results', self.tournament.tab_results)
