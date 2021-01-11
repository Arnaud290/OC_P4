"""manage player control module"""
from . import controller
from ..views import manage_player_view
from ..views import menu_view
from . import main_menu_control
from ..models import player_model


class ManagePlayerControl(controller.Controller):
    """Manage player control class"""
 
    def __call__(self):
        self.menu = menu_view.MenuView()
        self.new_player = {}
        self.view_controller = manage_player_view.ManagePlayerView()
        self.player_control_menu()

    def player_control_menu(self):
        self.menu.add_title_menu("CHESS MANAGE PLAYERS")   
        self.menu.add_menu_line('1', 'Add player')
        self.menu.add_menu_line('2', 'Modify existing players')
        self.menu.add_menu_line('q', 'Return to main menu')
        while True:
            choice = self.menu.display_menu()
            choice.lower()
            if choice not in ('1', '2', 'q'):
                continue
            if choice == '1':
                self.add_player()
            if choice == '2':
                self.modify_player()
            if choice == 'q' or 'Q':
                return True

    def add_player(self):
        self.view_controller.display_players_table(self.player_list())
        self.new_player = self.view_controller.add_player()
        player_id = player_model.PlayerModel.get_number()
        player = player_model.PlayerModel(id = player_id, **self.new_player)
        player.save()
        self.player_control_menu()

    def modify_player(self):
        self.view_controller.display_players_table(self.player_list())
        while True: 
            id_player = self.view_controller.get_id_modify_player()
            if id_player == 'q':
                self.player_control_menu()
                break
            try:
                id_player = int(id_player)
            except ValueError:
                continue
            else:
                if id_player not in range(player_model.PlayerModel.get_number()):
                    continue
                players_list = self.player_list()
                modified_player = self.view_controller.modify_player(players_list[id_player])
            for key, value in modified_player.items():
                players_list[id_player].update(key, value)
            self.player_list()
            break
        self.player_control_menu()
