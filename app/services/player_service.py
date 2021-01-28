"""Player service module"""
from ..models.player_model import PlayerModel
from .get_model_service import GetModelService
from ..views.view import View
from .test_service import TestService


class PlayerService:
    """Class of player service"""

    @classmethod
    def create_player(cls):
        """Create player method"""
        player = PlayerModel()
        player.id = GetModelService.get_number('PlayerModel')
        player.number = player.id + 1
        player.first_name = View.request("Enter first name:").capitalize()
        if not player.first_name:
            player.delete()
            pass
        else:
            player.last_name = TestService.test_alpha(title="Enter last name:", test_loop=True)
            player.last_name.capitalize()
            player.birth_date = View.request("Enter birth date (jj/mm//aaaa):")
            player.sex = TestService.test_alpha(title="Enter sex (M or F): ", test_element=('M', 'F'))
            player.rank = TestService.test_num(title="Enter rank: ")
            player.save()

    @classmethod
    def modify_player(cls, players_model_list):
        """Manage player method"""
        #players_id = GetModelService.get_models_id(players_model_list)
        player_id = TestService.test_num(
                                            title="Enter player number",
                                            test_range_element=len(players_model_list),
                                            modif_num=-1,
                                            test_loop=False
                                        )
        if player_id is None:
            pass
        else:
            player = GetModelService.get_model('PlayerModel', player_id)
            View.indication("Actual first name: {}".format(player.first_name))
            change = View.request("change first name or enter:").capitalize()
            if change:
                player.update('first_name', change)
            View.indication("Actual last name: {}".format(player.last_name))
            change = View.request("change last last name or enter:").capitalize()
            if change:
                player.update('last_name', change)
            View.indication("Actual birth date: {}".format(player.birth_date))
            change = View.request("change birth date (jj/mm//aaaa) or enter:")
            if change:
                player.update('birth_date', change)
            View.indication("Actual sex: {}".format(player.sex))
            change = TestService.test_alpha(
                                            title="Change sex (M or F) or enter: ",
                                            test_element=('M', 'F'),
                                            test_loop=False
                                            )
            if change:
                player.update('sex', change)
            View.indication("Actual rank: {}".format(player.rank))
            change = TestService.test_num("change rank or enter: ", test_loop=False)
            if change:
                player.update('rank', change)
