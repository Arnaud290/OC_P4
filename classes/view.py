"""View model module"""
from .models.save_loading_data import SaveLoadingData

class View:
    """Class for players and tournaments views"""
    @staticmethod
    def players_view():
        print("LIST OF PLAYERS\n\n\n")
        players_list = SaveLoadingData.load_players()
        for player in players_list:
            print("id : {}".format(players_list.index(player)))
            print("name : {}".format(player['first_name'] + ' ' + player['last_name']))
            print("\n")


