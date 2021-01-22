"""manage player control module"""
from .controller import Controller
from . import main_menu_controller
from ..models.player_model import PlayerModel
from ..views.view import View


class ManagePlayerController(Controller):
    """Manage player control class"""
    def __init__(self):
        self.view = View()

    def __call__(self):
        self.control = None
        self.tab_players_title = "Id order"
        self.tab_players_list = PlayerModel.get_serialized()
        self.tab_players_columns = ['id', 'first_name', 'last_name', 'birth_date', 'sex', 'rank']
        self.manage_player_menu()

    def manage_player_menu(self):
        """Manage player menu method"""
        select_sort = "Id order"
        while True:
            self.actual_players_list = self.players_list()
            self.tab_players_list = PlayerModel.get_serialized()
            self.view.add_title_menu("MANAGE PLAYERS")
            self.tab_players_list = self.tab_sort(PlayerModel.get_serialized(), select_sort)
            if self.tab_players_list:
                self.view.tab_view(self.tab_players_title, self.tab_players_list, self.tab_players_columns)
            if self.tab_players_title == "Id order":
                    self.view.add_menu_line("For alphabetical order")
            if self.tab_players_title == "Aphabetical order":  
                self.view.add_menu_line("For rank order")
            if self.tab_players_title == "Rank order":
                self.view.add_menu_line("For id order")    
            self.view.add_menu_line("Create player")
            self.view.add_menu_line("modify player")
            self.view.add_menu_line("Quit")
            choice = self.view.get_choice()
            if choice not in ('1', '2', '3', '4'):
                continue
            if choice == '1':
                if select_sort == "Id order":
                    self.tab_players_title = "Aphabetical order"
                    select_sort = "Aphabetical order"
                    continue
                if select_sort == "Aphabetical order":
                    self.tab_players_title = "Rank order"
                    select_sort = "Rank order"
                    continue
                if select_sort == "Rank order":
                    self.tab_players_title = "Id order"
                    select_sort = "Id order"
                    continue
            if choice  == '2':
                self.create_player()
                continue
            if choice  == '3':
                self.modify_player(self.actual_players_list)
                continue
            if choice  == '4':
                break
        self.control = main_menu_controller.MainMenuController()
        return self.control()

    def tab_sort(self, tab, select_sort):
        if select_sort == "Id order": 
            tab = sorted(tab, key=lambda x: x['id'], reverse=False)       
        if select_sort == "Aphabetical order":
            tab = sorted(tab, key=lambda item: item.get('last_name'), reverse=False)    
        if select_sort == "Rank order":
            tab = sorted(tab,key=lambda x: x['rank'], reverse=True)  
        return tab

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

    def modify_player(self, players_model):
        """Manage player method"""
        while True:
            id_player = self.view.request("Enter player id").upper()
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
                else:
                    break
            break
    
