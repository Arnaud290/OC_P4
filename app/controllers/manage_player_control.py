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
                controller = main_menu_control.MainMenuControl()
                controller()
                break

    def add_player(self):
        self.view_controller.display_players_table(self.player_list())
        player = player_model.PlayerModel()
        player.id = player_model.PlayerModel.get_number()
        player.first_name = self.view_controller.get_info_player("Enter first name or Q for quit: ").capitalize()
        if player.first_name == 'Q':
            self.player_control_menu()
        player.last_name = self.view_controller.get_info_player("Enter last name: ").capitalize()
        player.birth_date = self.view_controller.get_info_player("Enter birth date (jj/mm//aaaa): ")
        while True:
            player.sex = self.view_controller.get_info_player("Enter sex (M or F): ").upper()
            if player.sex in ('M', 'F'):
                break
            else: 
                continue  
        while True:     
            player.rank = self.view_controller.get_info_player("Enter rank: ")   
            try:
                player.rank = abs(int(player.rank)) 
                break
            except ValueError:
                print("\nEnter a number value !\n")
                continue
        player.save()
        controller = ManagePlayerControl()
        controller()

    def modify_player(self):
        self.menu.add_title_menu("MODIFY PLAYERS")   
        self.menu.add_menu_line('1', 'Add player')
        self.menu.add_menu_line('2', 'Modify existing players')
        self.menu.add_menu_line('q', 'Return to main menu')
        while True:


            self.view_controller.display_players_table(self.player_list())
        while True: 
            id_player = self.view_controller.get_info_player("Enter player id or 'Q' for quit: ").upper()
            if id_player == 'Q':
                break
            try:
                id_player = int(id_player)
            except ValueError:
                continue
            if id_player not in range(player_model.PlayerModel.get_number()):
                continue
            players = self.player_list()
            player = players[id_player]
            break
        value = self.view_controller.get_info_player("Change first name ? ({}): ".format(player.first_name))
        if value:
            player.update('first_name', value)
        value = self.view_controller.get_info_player("Change last name ? ({}): ".format(player.last_name))
        if value:
            player.update('last_name', value)
        value = self.view_controller.get_info_player("Change birth date ? ({}): ".format(player.birth_date))
        if value:
            player.update('birth_date', value)
        while True:    
            value = self.view_controller.get_info_player("Change sex ? ({}): ".format(player.sex))
            if value:
                if value in ('M', 'F'):
                    player.update('sex', value)
                    break
                else:
                    continue
            break
        while True:   
            value = self.view_controller.get_info_player("Change rank ? ({}): ".format(player.rank))
            if value:
                try:
                    value = abs(int(value))
                except ValueError:
                    continue
                else:
                    player.update('rank', value)
                    break
            break
        controller = ManagePlayerControl()
        controller()
