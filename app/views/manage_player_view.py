"""manage player view"""
from . import view
from ..controllers import manage_player_control


class ManagePlayerView(view.View):
    """Manage player view class"""
    def __call__(self):
        self.add_player_attributs = {}

    def display_players_table(self, player_list):
        """display record players table"""
        self.clear()
        print("Players List :\n\n")
        for player in player_list:
            print("id : {}, name : {} {}, rank : {}".format(
                                                        player.id,
                                                        player.first_name,
                                                        player.last_name,
                                                        player.rank
                                                        ))
            
    def get_info_player(self, key):
        player_add = input("\n{}".format(key))
        return player_add

            
   