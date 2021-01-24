"""main menu control module"""
from . import main_menu_controller
from ..services.get_model_service import GetModelService
from ..models.tournament_model import TournamentModel
from ..models.player_model import PlayerModel
from ..models.round_model import RoundModel
from .rounds_controller import RoundsController
from ..views.view import View
from ..config import settings
from .manage_player_controller import ManagePlayerController
from ..services.test_service import TestService


class NewTournamentController:
    """main menu control class"""
    def __call__(self):
        self.control = None
        self.actual_tournaments_list = GetModelService.get_model('TournamentModel')
        if self.actual_tournaments_list:
            if self.actual_tournaments_list[-1].in_progress:
                self.tournament = self.actual_tournaments_list[-1]
                self.manage_players_tournament()
            else:
                self.tournament = TournamentModel()
                self.new_tournament_menu()
        else:
            self.tournament = TournamentModel()
            self.new_tournament_menu()

    def new_tournament_menu(self):
        """New tournament menu method"""
        View.add_title_menu("NEW TOURNAMENT")
        View.add_menu_line("Create new tournament")
        View.add_menu_line("Quit")
        choice = TestService.test_alpha(test_element=('1', '2'))
        if choice == '1':
            self.new_tournament()
        if choice == '2':
            self.control = main_menu_controller.MainMenuController()
            return self.control()

    def new_tournament(self):
        """create new tournament method"""
        View.add_title_menu("CREATE TOURNAMENT")
        self.tournament.name = View.request("Name :")
        self.tournament.location = View.request("Location :")
        choice = TestService.test_num(
                                title=("Number players (default {}) : ".format(settings.NB_PLAYERS)),
                                test_loop=False,
                                even_test=True,
                                positif_num=True
                                )
        if choice is not None:
            self.tournament.nb_players = choice
        else:
            self.tournament.nb_players = settings.NB_PLAYERS
        choice = TestService.test_num(
                                    title=("Number rounds (default {}) : ".format(settings.NB_ROUNDS)),
                                    test_loop=False,
                                    test_range_element=self.tournament.nb_players,
                                    positif_num=True
                                    )
        if choice is not None:
            self.tournament.nb_rounds = choice
        else:
            self.tournament.nb_rounds = settings.NB_ROUNDS
        print()
        choice = TestService.test_alpha(title="Time control (1: 'bullet', 2: 'blitz' 3: 'coup rapide') : ",
                                        test_element=('1', '2', '3')
                                    )
        if choice == '1':
            self.tournament.time_control = 'bullet' 
        if choice == '2':
            self.tournament.time_control = 'blitz'
        if choice == '3':
            self.tournament.time_control = 'coup rapide'
        self.tournament.description = View.request("Description :")
        self.tournament.save()
        self.manage_players_tournament()
    def manage_players_tournament(self):
        """create, add or delete players for tournament method"""
        id_players_tournament_list = self.tournament.player_list
        while True:
            id_all_players = []
            players_model = GetModelService.get_model('PlayerModel')
            for player in players_model:
                id_all_players.append(player.id)
            tab_players_list = []
            tab_tournament_players = []
            tab_players_list = GetModelService.get_serialized('PlayerModel')
            for player_id in self.tournament.player_list:
                tab_tournament_players.append(GetModelService.get_serialized('PlayerModel', player_id))
                tab_players_list.remove(GetModelService.get_serialized('PlayerModel', player_id))
            View.add_title_menu("TOURNAMENT PLAYERS")
            elements_columns = ['id', 'first_name', 'last_name', 'rank']
            View.tab_view("List of players to add", tab_players_list, elements_columns)
            View.tab_view("List of players in tournament", tab_tournament_players, elements_columns)
            View.add_menu_line("Create Player")
            View.add_menu_line("Modify player")
            View.add_menu_line("Select player for tournament")
            View.add_menu_line("Delete tournament player")
            View.add_menu_line("Start Tournament")
            View.add_menu_line("Quit")
            choice = TestService.test_alpha(test_element=('1', '2', '3', '4', '5', '6'))
            if choice == '1':
                self.control = ManagePlayerController()
                self.control.create_player()
            if choice == '2':
                self.control = ManagePlayerController()
                self.control.modify_player(players_model)
            if choice == '3':
                id_player = TestService.test_num(
                                                    title="Enter player id to add: ",
                                                    test_element=id_all_players,
                                                    test_not_element=self.tournament.player_list
                                                ) 
                id_players_tournament_list.append(id_player)
                self.tournament.player_list = id_players_tournament_list
                self.tournament.update('player_list', id_players_tournament_list)
            if choice == '4':
                id_player = TestService.test_num(
                                                    title="Enter player id to delete",
                                                    test_element=self.tournament.player_list,
                                                )
                id_players_tournament_list.remove(id_player)
                self.tournament.player_list = id_players_tournament_list
                self.tournament.update('player_list', id_players_tournament_list)
            if choice == '5':
                if len(self.tournament.player_list) != self.tournament.nb_players:
                    View.indication("Players number must be {}".format(self.tournament.nb_players))
                    View.pause()
                    continue
                choice = TestService.test_alpha(
                                                title="Start tournament ? (Y or N)",
                                                test_element=('Y', 'N')
                                            )
                if choice == 'Y':
                    rounds_nb = 1
                    for nb_rounds in range(self.tournament.nb_rounds):
                        round_game = RoundModel()
                        round_game.id_tourament = self.tournament.id
                        round_game.count = rounds_nb
                        round_game.name = 'Round ' + str(rounds_nb)
                        self.tournament.round_list.append(round_game.id)
                        round_game.save()
                        rounds_nb += 1
                    self.tournament.in_progress = True
                    self.tournament.update('in_progress', self.tournament.in_progress)
                    self.tournament.update('round_list', self.tournament.round_list)
                    self.control = RoundsController()
                    return self.control()
                if choice == 'N':
                    continue
            if choice == '6':
                choice = TestService.test_alpha(
                                                    title="quit by deleting the tournament? (Y or N)",
                                                    test_element=('Y', 'N')
                                                    ) 
            if choice == 'Y':
                self.tournament.delete()
                self.control = main_menu_controller.MainMenuController()
                return self.control()
            if choice == 'N':
                self.tournament.in_progress = True
                self.tournament.update('in_progress', self.tournament.in_progress)
                self.control = main_menu_controller.MainMenuController()
                return self.control()
