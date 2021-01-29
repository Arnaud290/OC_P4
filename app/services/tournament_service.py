"""Service module for tournaments"""
from .get_model_service import GetModelService
from ..models.tournament_model import TournamentModel
from ..views.view import View
from .test_service import TestService
from .table_service import TableService
from .player_service import PlayerService
from . import match_service
from ..config import settings
from . import round_service


class TournamentService:
    @classmethod
    def tournament_players_list(cls, tournament):
        """method that returns the list of
        models of players in a tournament"""
        t_players = []
        for player in tournament.player_list:
            t_players.append(GetModelService.get_model('PlayerModel', player))
        return t_players

    @classmethod
    def tournament_results_table(cls, tournament):
        """Table creation method for tournament results"""
        t_players = cls.tournament_players_list(tournament)
        tab_t_players = []
        for player in t_players:
            tab_t_players.append(GetModelService.get_serialized('PlayerModel', player.id))
            tab_t_players.sort(key=lambda x: (x['tournament_points'], x['rank']), reverse=True)
        return tab_t_players

    @classmethod
    def clear_tournament_players_points(cls, tournament):
        """Method of erasing player
        points after a tournament"""
        t_players = cls.tournament_players_list(tournament)
        for player in t_players:
            player.tournament_points = 0.0
            player.update('tournament_points', player.tournament_points)
            player.vs = []
            player.no_vs = []
            player.update('vs', player.vs)
            player.update('no_vs', player.no_vs)

    @classmethod
    def create_tournament(cls):
        """method to create a tournament"""
        tournament = TournamentModel()
        View.add_title_menu("CREATE TOURNAMENT")
        tournament.name = TestService.test_alpha(title="Name :", test_loop=True)
        tournament.location = TestService.test_alpha(title="Location :", test_loop=True)
        choice = TestService.test_num(
                                title=("Number players (default {}) : ".format(settings.NB_PLAYERS)),
                                test_loop=False,
                                even_test=True,
                                positif_num=True
                                )
        if choice is not None:
            tournament.nb_players = choice
        else:
            tournament.nb_players = settings.NB_PLAYERS
        choice = TestService.test_num(
                                    title=("Number rounds (default {}) : ".format(settings.NB_ROUNDS)),
                                    test_loop=False,
                                    test_range_element=tournament.nb_players,
                                    positif_num=True
                                    )
        if choice is not None:
            tournament.nb_rounds = choice
        else:
            tournament.nb_rounds = settings.NB_ROUNDS
        choice = TestService.test_alpha(
                                        title="Time control (1: 'bullet', 2: 'blitz' 3: 'coup rapide') : ",
                                        test_element=('1', '2', '3')
                                    )
        if choice == '1':
            tournament.time_control = 'bullet'
        if choice == '2':
            tournament.time_control = 'blitz'
        if choice == '3':
            tournament.time_control = 'coup rapide'
        tournament.description = View.request("Description :")
        tournament.in_progress = True
        tournament.save()
        return tournament

    @classmethod
    def manage_tournament(cls, tournament):
        """method to manage a tournament before departure"""
        id_players_tournament_list = tournament.player_list
        while True:
            id_all_players = GetModelService.get_models_id(GetModelService.get_model('PlayerModel'))
            tab_players_list = []
            tab_tournament_players = []
            tab_players_list = GetModelService.get_serialized('PlayerModel')
            for player_id in tournament.player_list:
                tab_tournament_players.append(GetModelService.get_serialized('PlayerModel', player_id))
                tab_players_list.remove(GetModelService.get_serialized('PlayerModel', player_id))
            View.add_title_menu("TOURNAMENT PLAYERS")
            TableService.table(
                                title="List of players to add",
                                columns=['number', 'first_name', 'last_name', 'rank'],
                                table=tab_players_list
                                )
            TableService.table(
                                title="List of players in tournament",
                                columns=['number', 'first_name', 'last_name', 'rank'],
                                table=tab_tournament_players
                                )
            View.add_menu_line("Create Player")
            View.add_menu_line("Modify player")
            View.add_menu_line("Select player for tournament")
            View.add_menu_line("Delete tournament player")
            View.add_menu_line("Start Tournament")
            View.add_menu_line("Quit")
            choice = TestService.test_alpha(test_element=('1', '2', '3', '4', '5', '6'))
            if choice == '1':
                PlayerService.create_player()
                continue
            if choice == '2':
                PlayerService.modify_player(GetModelService.get_model('PlayerModel'))
                continue
            if choice == '3':
                id_player = TestService.test_num(
                                                    title="Enter player number to add: ",
                                                    test_element=id_all_players,
                                                    test_not_element=tournament.player_list,
                                                    modif_num=-1,
                                                    test_loop=False
                                                )
                if id_player is None:
                    continue
                else:
                    id_players_tournament_list.append(id_player)
                    tournament.player_list = id_players_tournament_list
                    tournament.update('player_list', id_players_tournament_list)
                    continue
            if choice == '4':
                id_player = TestService.test_num(
                                                    title="Enter player number to delete",
                                                    test_element=tournament.player_list,
                                                    modif_num=-1,
                                                    test_loop=False
                                                )
                if id_player is None:
                    continue
                else:
                    id_players_tournament_list.remove(id_player)
                    tournament.player_list = id_players_tournament_list
                    tournament.update('player_list', id_players_tournament_list)
                    continue
            if choice == '5':
                if len(tournament.player_list) != tournament.nb_players:
                    View.indication("Players number must be {}".format(tournament.nb_players))
                    View.pause()
                    continue
                choice = TestService.test_alpha(
                                                title="Start tournament ? (Y or N)",
                                                test_element=('Y', 'N'),
                                                test_loop=False
                                            )
                if choice is None:
                    continue
                else:
                    if choice == 'Y':
                        round_service.RoundService.create_rounds(tournament)
                        return True
                    if choice == 'N':
                        continue
            if choice == '6':
                choice = TestService.test_alpha(
                                                    title="quit by deleting the tournament? (Y or N)",
                                                    test_element=('Y', 'N'),
                                                    test_loop=False
                                                )
            if choice is None:
                continue
            else:
                if choice == 'Y':
                    tournament.delete()
                if choice == 'N':
                    tournament.in_progress = True
                    tournament.update('in_progress', tournament.in_progress)
                return False

    @classmethod
    def select_tournament(cls):
        """Method to select the model
        of a tournament with its id"""
        tournament_list = GetModelService.get_model('TournamentModel')
        choice = TestService.test_num(
                                    title="Enter number of tournament",
                                    test_range_element=len(tournament_list),
                                    test_loop=False,
                                    modif_num=-1
                                    )
        if choice is None:
            pass
        else:
            tournament = GetModelService.get_model('TournamentModel', choice)
            return tournament

    @classmethod
    def table_of_tournament_players(cls, tournament):
        """Method to create a table
        of players in a tournament"""
        table_sort = "Alphabetical order"
        while True:
            View.add_title_menu("PLAYERS LIST OF TOURNAMENT {}".format(tournament.name))
            TableService.table(
                                title=table_sort,
                                columns=['number', 'first_name', 'last_name', 'tournament_points', 'rank'],
                                table=tournament.results,
                                select_sort=table_sort
                            )
            TableService.table_sort_menu('tournament_player_table', table_sort)
            View.add_menu_line("Quit")
            choice = TestService.test_alpha(test_element=('1', '2'))
            if choice == '1':
                table_sort = TableService.table_sort_select('tournament_player_table', table_sort)
            if choice == '2':
                break

    @classmethod
    def table_of_tournament_rounds(cls, tournament):
        """Method to create a table
        of rounds of a tournament"""
        match_tab_title = None
        match_tab_list = []
        while True:
            View.add_title_menu("ROUNDS LIST OF TOURNAMENT {}".format(tournament.name))
            TableService.table(
                                title="Rounds list",
                                columns=['name', 'date_start', 'date_finish'],
                                table=tournament.round_list,
                                select_sort='Round_name'
                            )
            TableService.table(
                                title=match_tab_title,
                                columns=['number', 'player1', 'score1', 'player2', 'score2'],
                                table=match_tab_list
                            )
            match_tab_list = []
            View.add_menu_line("Display matchs")
            View.add_menu_line("Quit")
            choice = TestService.test_alpha(test_element=('1', '2'))
            if choice == '1':
                choice = TestService.test_num(
                                            title="Enter round number",
                                            modif_num=-1,
                                            test_range_element=len(tournament.round_list),
                                            test_loop=False
                                            )
                if choice is None:
                    continue
                match_tab_title = tournament.round_list[choice]['name']
                match_tab_list = match_service.MatchService.match_table(tournament.round_list[choice]['matchs_list'])
            if choice == '2':
                break
