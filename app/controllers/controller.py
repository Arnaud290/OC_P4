"""base controller module"""
from .. import models


class Controller:
    """General controller class"""

    @staticmethod
    def player_list():
        """return list of objects players""" 
        player_list = []
        serialized_players = models.player_model.PlayerModel.get()
        for serialized_player in serialized_players:
            player = models.player_model.PlayerModel(**serialized_player)
            player_list.append(player)
        return player_list
