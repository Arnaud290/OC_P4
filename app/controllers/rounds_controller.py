"""Rounds control module"""
import time
from . import main_menu_controller
from ..views.view import View
from ..services.get_model_service import GetModelService
from ..services.test_service import TestService
from ..services.table_service import TableService
from ..services.match_service import MatchService
from ..services.tournament_service import TournamentService
from ..services.round_service import RoundService
from ..services.player_service import PlayerService


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

    def rounds_engine(self):
        """Round engine method"""
        while self.in_progress:
            for rounds in self.tournament.round_list:
                if rounds['finish']:
                    pass
                if self.in_progress:
                    self.rounds = rounds
                    while self.in_progress and not self.rounds['finish']:
                        if not self.rounds['start'] and not self.rounds['matchs_list']:
                            MatchService.create_matchs(self.tournament, self.rounds)
                            self.tournament.update('round_list', self.tournament.round_list)
                            self.rounds_menu()
                            continue
                        if self.rounds['matchs_list']:
                            self.rounds_menu()
                            continue
            break
        if self.in_progress:
            title_menu = "Tournament : {} is finish !".format(self.tournament.name)
            View.add_title_menu(title_menu)
            TableService.table(
                                title='Results',
                                columns=['number', 'first_name', 'last_name', 'tournament_points', 'rank'],
                                table=TournamentService.tournament_results_table(self.tournament),
                                select_sort='tournament_points'
                                )
            t_players = TournamentService.tournament_players_list(self.tournament)
            for player in t_players:
                player.tournament_points = 0.0
                player.update('tournament_points', player.tournament_points)
            self.tournament.in_progress = False
            self.tournament.update('in_progress', self.tournament.in_progress)
            TournamentService.clear_tournament_players_points(self.tournament)
            View.pause()
        self.control = main_menu_controller.MainMenuController()
        return self.control()

    def rounds_menu(self):
        """Management method of the round menu"""
        RoundService.round_table(self.tournament, self.rounds)
        if not self.rounds['start']:
            View.add_menu_line("Start Round")
        else:
            View.add_menu_line("Finish Match ?")
        View.add_menu_line("Manage players tournament")
        View.add_menu_line("Quit")
        choice = TestService.test_alpha(test_element=('1', '2', '3'))
        if choice == '1':
            if not self.rounds['start']:
                self.rounds['start'] = True
                self.rounds['date_start'] = time.strftime("%d/%m/%Y %H:%M:%S")
                self.tournament.update('round_list', self.tournament.round_list)
            else:
                choice = TestService.test_num(
                                                title="Enter match number: ",
                                                modif_num=-1,
                                                test_range_element=len(self.rounds['matchs_list']),
                                                test_not_element=self.rounds['finish_matchs'],
                                                test_loop=False
                                            )
                if choice is None:
                    pass
                else:
                    player_1 = MatchService.match_table(self.rounds['matchs_list'])[choice]['player1']
                    player_2 = MatchService.match_table(self.rounds['matchs_list'])[choice]['player2']
                    title = "Enter\n1: {} win\n2: {} win\n3: draw".format(player_1, player_2)
                    result_select = TestService.test_alpha(
                                                    title=title,
                                                    test_element=('1', '2', '3')
                                                )
                    MatchService.management_match(self.tournament, self.rounds, choice, result_select)
        if choice == '2':
            t_players = TournamentService.tournament_players_list(self.tournament)
            PlayerService.modify_player(t_players)
        if choice == '3':
            choice = TestService.test_alpha(
                                            title="quit by deleting the tournament? (Y or N)",
                                            test_element=('Y', 'N'),
                                            test_loop=False
                                            )
            if choice == 'Y':
                t_players = TournamentService.tournament_players_list(self.tournament)
                self.tournament.delete()
                TournamentService.clear_tournament_players_points(self.tournament)
                self.in_progress = False
                self.tournament = False
            if choice == 'N':
                self.in_progress = False
