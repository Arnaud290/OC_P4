"""manage player control module"""
from . import main_menu_controller
from ..models.player_model import PlayerModel
from ..services.get_model_service import GetModelService
from ..views.view import View
from ..services.test_service import TestService
from ..services.table_service import TableService
from ..services.player_service import PlayerService


class ManagePlayerController:
    """Manage player control class"""
    def __call__(self):
        self.control = None
        self.tab_sort = "Id order"
        self.manage_player_menu()

    def manage_player_menu(self):
        """Manage player menu method"""
        while True:
            self.actual_players_list = GetModelService.get_model('PlayerModel')
            self.tab_players_list = GetModelService.get_serialized('PlayerModel')
            View.add_title_menu("MANAGE PLAYERS")
            TableService.table(
                                title=self.tab_sort,
                                columns=['id', 'first_name', 'last_name', 'birth_date', 'sex', 'rank'],
                                table = GetModelService.get_serialized('PlayerModel'),
                                select_sort=self.tab_sort
                            )
            TableService.table_sort_menu('player_table', self.tab_sort)
            View.add_menu_line("Create player")
            View.add_menu_line("modify player")
            View.add_menu_line("Quit")
            choice = TestService.test_alpha(test_element=('1', '2', '3', '4'))
            if choice == '1':
                self.tab_sort = TableService.table_sort_select('player_table', self.tab_sort)
            if choice == '2':
                PlayerService.create_player()
                continue
            if choice == '3':
                PlayerService.modify_player(self.actual_players_list)
                continue
            if choice == '4':
                break
        self.control = main_menu_controller.MainMenuController()
        return self.control()

    #def modify_player(self, players_model):
    #    """Manage player method"""
    #    players_id = GetModelService.get_models_id(players_model)
    #    player_id = TestService.test_num("Enter player id", test_element=players_id, test_loop=False)
    #    if player_id is None:
    #        pass
    #    else:
    #        player = GetModelService.get_model('PlayerModel', player_id)
    #        View.indication("Actual first name: {}".format(player.first_name))
    #        change = View.request("change first name or enter:").capitalize()
    #        if change:
    #            player.update('first_name', change)
    #        View.indication("Actual last name: {}".format(player.last_name))
    #        change = View.request("change last last name or enter:").capitalize()
    #        if change:
    #            player.update('last_name', change)
    #        View.indication("Actual birth date: {}".format(player.birth_date))
    #        change = View.request("change birth date (jj/mm//aaaa) or enter:")
    #        if change:
    #            player.update('birth_date', change)
    #        View.indication("Actual sex: {}".format(player.sex))
    #        change = TestService.test_alpha(
    #                                        title="Change sex (M or F) or enter: ",
    #                                        test_element=('M', 'F'),
    #                                        test_loop= False
    #                                        )
    #        if change:
    #            player.update('sex', change)
    #        View.indication("Actual rank: {}".format(player.rank))
    #        change = TestService.test_num("change rank or enter: ", test_loop= False)
    #        if change:
    #            player.update('rank', change)
