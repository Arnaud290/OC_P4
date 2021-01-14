"""main menu control module"""
from . import controller
from . import main_menu_control
from ..models.tournament_model import TournamentModel
from ..models.player_model import PlayerModel
from ..views import menu_view, new_tournament_view
from ..config import settings


class NewTournamentControl(controller.Controller):
    """main menu control class"""
    def __call__(self):
        self.select = ''
        self.control = None
        self.actual_tournaments_list = self.tournaments_list()
        self.menu = menu_view.MenuView()
        self.tournament_view = new_tournament_view.NewTournamentView()
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
        self.menu.add_title_menu("NEW TOURNAMENT")
        self.menu.add_menu_line("Create new tournament")
        self.menu.add_menu_line("Quit")
        self.select = self.menu.get_choice()
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
        self.menu.add_title_menu("CREATE TOURNAMENT")
        self.tournament.name = self.tournament_view.request("Name :")
        self.tournament.location = self.tournament_view.request("Location :")
        while True:
            choice = self.tournament_view.request("Number players (default {}) : ".format(settings.NB_PLAYERS))
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
            choice = self.tournament_view.request("Number rounds (default {}) : ".format(settings.NB_ROUNDS))
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
            choice = self.tournament_view.request("Time control (1 : 'bullet', 2: 'blitz' 3: 'coup rapide') : ")
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
        self.tournament.description = self.tournament_view.request("Description :")
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
            self.menu.add_title_menu("TOURNAMENT PLAYERS")
            self.tournament_view.tab_view("List of players to add", tab_players_list)
            self.tournament_view.tab_view("List of players in tournament", tab_tournament_players)
            self.menu.add_menu_line("Create Player")
            self.menu.add_menu_line("modify player")
            self.menu.add_menu_line("Select player for tournament")
            self.menu.add_menu_line("delete tournament player")
            self.menu.add_menu_line("Start Tournament")
            self.menu.add_menu_line("Quit")
            choice = self.menu.get_choice()
            if choice not in ('1', '2', '3', '4', '5', '6'):
                continue
            if choice == '1':
                player = PlayerModel()
                player.id = PlayerModel.get_number()
                player.first_name = self.tournament_view.request("Enter first name:").capitalize()
                player.last_name = self.tournament_view.request("Enter last name:").capitalize()
                player.birth_date = self.tournament_view.request("Enter birth date (jj/mm//aaaa):")
                while True:
                    player.sex = self.tournament_view.request("Enter sex (M or F): ").upper()
                    if player.sex in ('M', 'F'):
                        break
                    else:
                        continue
                while True:
                    player.rank = self.tournament_view.request("Enter rank:")
                    try:
                        player.rank = abs(int(player.rank))
                        break
                    except ValueError:
                        continue
                player.save()
                continue
            if choice == '2':
                while True:
                    id_player = self.tournament_view.request("Enter player id or Q for quit:").upper()
                    if id_player == 'Q':
                        break
                    try:
                        id_player = abs(int(id_player))
                    except ValueError:
                        continue
                    if id_player not in range(len(players_model)):
                        continue
                    for players in players_model:
                        if players.id == id_player:
                            player = players
                    self.tournament_view.indication("Actual first name: {}".format(player.first_name))
                    change = self.tournament_view.request("change first name or enter:").capitalize()
                    if change:
                        player.update('first_name', change)
                    self.tournament_view.indication("Actual last name: {}".format(player.last_name))
                    change = self.tournament_view.request("change last last name or enter:").capitalize()
                    if change:
                        player.update('last_name', change)
                    self.tournament_view.indication("Actual birth date: {}".format(player.birth_date))
                    change = self.tournament_view.request("change birth date (jj/mm//aaaa) or enter:")
                    if change:
                        player.update('birth_date', change)
                    self.tournament_view.indication("Actual sex: {}".format(player.sex))
                    while True:
                        change = self.tournament_view.request("change sex (M or F) or enter: ").upper()
                        if change:
                            if player.sex in ('M', 'F'):
                                player.update('sex', change)
                                break
                            else:
                                continue
                        else:
                            break
                    self.tournament_view.indication("Actual rank: {}".format(player.rank))
                    while True:
                        change = self.tournament_view.request("change rank or enter:")
                        if change:
                            try:
                                change = abs(int(change))
                            except ValueError:
                                continue
                            else:
                                player.update('rank', change)
                                break
                        break
                    break
            if choice == '3':
                while True:
                    id_player = self.tournament_view.request("Enter player id to add or Q for quit:").upper()
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
                    id_player = self.tournament_view.request("Enter player id to delete or Q for quit:").upper()
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
                        self.tournament_view.indication("Players number must be {}".format(self.tournament.nb_players))
                        self.tournament_view.pause()
                        break
                    choice = self.tournament_view.request("Start tournament ? (Y or N)").upper()
                    if choice not in ('Y', 'N'):
                        continue
                    if choice == 'Y':
                        self.tournament.in_progress = True
                        self.tournament.save()
                        pass
                    if choice == 'N':
                        break
            if choice == '6':
                choice = self.tournament_view.request("quit by deleting the tournament? (Y or N)").upper()
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
