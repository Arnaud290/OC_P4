"""match control module"""
import time
import operator
from . import main_menu_controller
from ..views.view import View
from ..services.get_model_service import GetModelService
from ..models.player_model import PlayerModel
from . import manage_player_controller
from ..services.test_service import TestService
from ..services.table_service import TableService
from ..services.match_service import MatchService


class RoundsController:
    """Rounds control class"""
    def __call__(self):
        self.in_progress = True
        self.actual_tournaments_list = GetModelService.get_model('TournamentModel')
        self.tournament = self.actual_tournaments_list[-1]
        self.control = None
        self.rounds = None
        self.delete_tournament = False
        self.tab_r_matchs = []
        self.rounds_engine()

    def tournament_players_list(self):
        t_players = []
        for player in self.tournament.player_list:
            t_players.append(GetModelService.get_model('PlayerModel', player))
        return t_players

    def tournament_rounds_list(self):
        rounds = []
        for id_round in self.tournament.round_list:
            rounds.append(GetModelService.get_model('RoundModel', id_round))
        return rounds

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
            View.add_title_menu(title_menu)
            TableService.table(
                                title='Results',
                                columns=['first_name', 'last_name', 'tournament_points', 'rank'],
                                table=self.results(),
                                select_sort='tournament_points'
                                )
            t_players = self.tournament_players_list()
            for player in t_players:
                player.tournament_points = 0.0
                player.update('tournament_points', player.tournament_points)
            self.tournament.in_progress = False
            self.tournament.update('in_progress', self.tournament.in_progress)
            self.clear_players_points()
            View.pause()
            self.control = main_menu_controller.MainMenuController()
            return self.control()
        else:
            self.control = main_menu_controller.MainMenuController()
            return self.control()

    def results(self):
        t_players = self.tournament_players_list()
        tab_t_players = []
        for player in t_players:
                tab_t_players.append(GetModelService.get_serialized('PlayerModel', player.id))
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
        View.add_title_menu(title_menu)
        tab_t_players = []
        t_players = self.tournament_players_list()
        for player in t_players:
            tab_t_players.append(GetModelService.get_serialized('PlayerModel', player.id))
        TableService.table(
                            title="Tournament Players",
                            columns=['tournament_points', 'rank', 'first_name', 'last_name', 'id'],
                            table=tab_t_players
                        )
        TableService.table(
                            title="Round {}".format(self.rounds.count),
                            columns=['id', 'player1', 'score1', 'player2', 'score2'],
                            table=MatchService.match_list_tab(self.rounds.matchs_list)
                        )

    def rounds_menu(self):
        self.rounds_tab()
        if not self.rounds.start:
            View.add_menu_line("Start Round")
        else:
            View.add_menu_line("Finish Match ?")
        View.add_menu_line("Manage players tournament")
        View.add_menu_line("Quit")
        choice = TestService.test_alpha(test_element=('1', '2', '3'))
        if choice == '1':
            if not self.rounds.start:
                self.rounds.start = True
                self.rounds.update('start', self.rounds.start)
                self.rounds.date_start = time.strftime("%d/%m/%Y %H:%M:%S")
                self.rounds.update('date_start', self.rounds.date_start)
            else:   
                choice = TestService.test_num(
                                                title="Enter match number: ",
                                                modif_num = -1,
                                                test_range_element=len(self.rounds.matchs_list),
                                                test_not_element=self.rounds.finish_matchs
                                            )
                player_1 = MatchService.match_list_tab(self.rounds.matchs_list)[choice]['player1']
                player_2 = MatchService.match_list_tab(self.rounds.matchs_list)[choice]['player2']
                title = "Enter\n1: {} win\n2: {} win\n3: draw".format(player_1, player_2)
                result = TestService.test_alpha(
                                                title=title,
                                                test_element=('1', '2', '3')
                                            )
                self.match_management(choice, result)
        if choice == '2':
            t_players = self.tournament_players_list()
            self.control = manage_player_controller.ManagePlayerController()
            self.control.modify_player(t_players)
        if choice == '3':
            choice = TestService.test_alpha(
                                            title="quit by deleting the tournament? (Y or N)",
                                            test_element=('Y', 'N')
                                            )
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
        p_match = self.tournament_players_list()
        t_players_id = GetModelService.get_models_id(p_match)
        p_match.sort(key=operator.attrgetter('tournament_points', 'rank'), reverse=True)
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
            self.tournament.tab_results = self.results()
            self.tournament.update('results', self.tournament.tab_results)