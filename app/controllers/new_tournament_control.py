"""main menu control module"""
from .controller import Controller
from . import main_menu_control
from ..models.tournament_model import TournamentModel
from ..models.player_model import PlayerModel
from ..models.round_model import RoundModel
from .rounds_control import RoundsControl
from ..views.view import View
from ..config import settings
from .manage_player_control import ManagePlayerControl


class NewTournamentControl(Controller):
    """main menu control class"""
    def __call__(self):
        self.select = ''
        self.control = None
        self.actual_tournaments_list = self.tournaments_list()
        self.view = View()
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
        self.view.add_title_menu("NEW TOURNAMENT")
        self.view.add_menu_line("Create new tournament")
        self.view.add_menu_line("Quit")
        self.select = self.view.get_choice()
        if self.select not in ('1', '2'):
            self.control = NewTournamentControl()
            self.control()
        else:
            if self.select == '1':
                self.new_tournament()
            if self.select == '2':
                self.control = main_menu_control.MainMenuControl()
                self.control()

    def new_tournament(self):
        """create new tournament method"""
        self.view.add_title_menu("CREATE TOURNAMENT")
        self.tournament.name = self.view.request("Name :")
        self.tournament.location = self.view.request("Location :")
        while True:
            choice = self.view.request("Number players (default {}) : ".format(settings.NB_PLAYERS))
            if choice:
                try:
                    self.tournament.nb_players = abs(int(choice))
                except ValueError:
                    continue
                else:
                    break
            else:
                self.tournament.nb_players = int(settings.NB_PLAYERS)
                break
        while True:
            choice = self.view.request("Number rounds (default {}) : ".format(settings.NB_ROUNDS))
            if choice:
                try:
                    self.tournament.nb_rounds = abs(int(choice))
                except ValueError:
                    continue
                else:
                    break
            else:
                self.tournament.nb_rounds = int(settings.NB_ROUNDS)
                break
        while True:
            choice = self.view.request("Time control (1 : 'bullet', 2: 'blitz' 3: 'coup rapide') : ")
            if choice in ('1', '2', '3'):
                if choice == '1':
                    self.tournament.time_control = 'bullet'
                    break
                if choice == '2':
                    self.tournament.time_control = 'blitz'
                    break
                if choice == '3':
                    self.tournament.time_control = 'coup rapide'
                    break
            else:
                continue
        self.tournament.description = self.view.request("Description :")
        self.manage_players_tournament()

    def manage_players_tournament(self):
        """create, add or delete players for tournament method"""
        id_players_tournament_list = self.tournament.player_list
        while True:
            id_all_players = []
            players_model = self.players_list()
            for player in players_model:
                id_all_players.append(player.id)
            tab_players_list = []
            tab_tournament_players = []
            tab_players_list = PlayerModel.get_serialized()
            for player_id in self.tournament.player_list:
                tab_tournament_players.append(PlayerModel.get_id_serialized(player_id))
                tab_players_list.remove(PlayerModel.get_id_serialized(player_id))
            self.view.add_title_menu("TOURNAMENT PLAYERS")
            elements_columns = ['id', 'first_name', 'last_name', 'rank']
            self.view.tab_view("List of players to add", tab_players_list, elements_columns)
            self.view.tab_view("List of players in tournament", tab_tournament_players, elements_columns)
            self.view.add_menu_line("Create Player")
            self.view.add_menu_line("Modify player")
            self.view.add_menu_line("Select player for tournament")
            self.view.add_menu_line("Delete tournament player")
            self.view.add_menu_line("Start Tournament")
            self.view.add_menu_line("Quit")
            choice = self.view.get_choice()
            if choice not in ('1', '2', '3', '4', '5', '6'):
                continue
            if choice == '1':
                self.control = ManagePlayerControl()
                self.control.create_player()
            if choice == '2':
                self.control = ManagePlayerControl()
                self.control.modify_player(players_model)
            if choice == '3':
                while True:
                    id_player = self.view.request("Enter player id to add or Q for quit:").upper()
                    if id_player == 'Q':
                        break
                    try:
                        id_player = abs(int(id_player))
                    except ValueError:
                        continue
                    if id_player in id_all_players and id_player not in self.tournament.player_list:
                        id_players_tournament_list.append(id_player)
                        self.tournament.player_list = id_players_tournament_list
                        self.tournament.update('player_list', id_players_tournament_list)
                        break
                    else:
                        continue
            if choice == '4':
                while True:
                    id_player = self.view.request("Enter player id to delete or Q for quit:").upper()
                    if id_player == 'Q':
                        break
                    try:
                        id_player = abs(int(id_player))
                    except ValueError:
                        continue
                    if id_player in self.tournament.player_list:
                        id_players_tournament_list.remove(id_player)
                        self.tournament.player_list = id_players_tournament_list
                        self.tournament.update('player_list', id_players_tournament_list)
                        break
                    else:
                        continue
            if choice == '5':
                while True:
                    if len(self.tournament.player_list) != self.tournament.nb_players:
                        self.view.indication("Players number must be {}".format(self.tournament.nb_players))
                        self.view.pause()
                        break
                    choice = self.view.request("Start tournament ? (Y or N)").upper()
                    if choice not in ('Y', 'N'):
                        continue
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
                        self.tournament.save()
                        self.control = RoundsControl()
                        break
                    if choice == 'N':
                        self.control = ManagePlayerControl()
                        break
                self.control()
            if choice == '6':
                choice = self.view.request("quit by deleting the tournament? (Y or N)").upper()
                if choice not in ('Y', 'N'):
                    pass
                if choice == 'Y':
                    self.tournament.delete()
                    break
                if choice == 'N':
                    self.tournament.in_progress = True
                    self.tournament.save()
                    break
        self.control = main_menu_control.MainMenuControl()
        self.control()
