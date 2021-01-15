"""manage player control module"""
from .controller import Controller
from . import main_menu_control
from ..models.player_model import PlayerModel
from ..views.view import View


class ManagePlayerControl(Controller):
    """Manage player control class"""
    
    def __init__(self):
        self.view = View()

    def __call__(self):
        self.select = ''
        self.control = None
        self.actual_tournaments_list = self.tournaments_list()
        self.manage_player_menu()

    def manage_player_menu(self):
        """Manage player menu method"""
        while True:
            tab_players_list = PlayerModel.get_serialized()
            self.view.add_title_menu("MANAGE PLAYERS")
            elements_columns = ['id', 'first_name', 'last_name', 'birth_date' ,'sex', 'rank']
            self.view.tab_view("Actual players", tab_players_list, elements_columns)
            self.view.add_menu_line("Create player")
            self.view.add_menu_line("modify player")
            self.view.add_menu_line("Quit")
            self.select = self.view.get_choice()
            if self.select not in ('1', '2', '3'):
                self.control = ManagePlayerControl()
                self.control()
            else:
                if self.select == '1':
                    self.create_player()

                if self.select == '2':
                    self.modify_player()

                if self.select == '3':
                    break
        self.control = main_menu_control.MainMenuControl()
        self.control()

    def create_player(self):
        """Create player method"""
        player = PlayerModel()
        player.id = PlayerModel.get_number()
        player.first_name = self.view.request("Enter first name:").capitalize()
        player.last_name = self.view.request("Enter last name:").capitalize()
        player.birth_date = self.view.request("Enter birth date (jj/mm//aaaa):")
        while True:
            player.sex = self.view.request("Enter sex (M or F): ").upper()
            if player.sex in ('M', 'F'):
                break
            else:
                continue
        while True:
            player.rank = self.view.request("Enter rank:")
            try:
                player.rank = abs(int(player.rank))
                break
            except ValueError:
                continue
        player.save()
            
    def modify_player(self):
        """Manage player method"""
        players_model = self.players_list()
        while True:
            id_player = self.view.request("Enter player id or Q for quit:").upper()
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
            self.view.indication("Actual first name: {}".format(player.first_name))
            change = self.view.request("change first name or enter:").capitalize()
            if change:
                player.update('first_name', change)
            self.view.indication("Actual last name: {}".format(player.last_name))
            change = self.view.request("change last last name or enter:").capitalize()
            if change:
                player.update('last_name', change)
            self.view.indication("Actual birth date: {}".format(player.birth_date))
            change = self.view.request("change birth date (jj/mm//aaaa) or enter:")
            if change:
                player.update('birth_date', change)
            self.view.indication("Actual sex: {}".format(player.sex))
            while True:
                change = self.view.request("change sex (M or F) or enter: ").upper()
                if change:
                    if player.sex in ('M', 'F'):
                        player.update('sex', change)
                        break
                    else:
                        continue
                else:
                    break
            self.view.indication("Actual rank: {}".format(player.rank))
            while True:
                change = self.view.request("change rank or enter:")
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
