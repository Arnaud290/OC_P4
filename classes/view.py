"""View model module"""
from pandas import DataFrame
from .models.save_loading_data import SaveLoadingData


class View:
    """Class for players and tournaments views"""
    @staticmethod
    def players_view():
        print("LIST OF PLAYERS\n\n\n")
        players_list = SaveLoadingData.load_player()
        index = []
        for player in players_list:
            index.append('')
        tab_players = DataFrame(players_list, index=index)
        print(tab_players)
