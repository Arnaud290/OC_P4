"""base controller module"""
from .. import models


class Controller:
    """General controller class"""

    def __init__(self):
        pass

    @staticmethod
    def players_list():
        """return list of objects players""" 
        player_list = []
        serialized_players = models.player_model.PlayerModel.get()
        for serialized_player in serialized_players:
            player = models.player_model.PlayerModel(**serialized_player)
            player_list.append(player)
        return player_list

    @staticmethod
    def tournaments_list():
        """return list of objects tournaments""" 
        tournaments_list = []
        serialized_tournaments = models.tournament_model.TournamentModel.get()
        for serialized_tournament in serialized_tournaments:
            tournament = models.tournament_model.TournamentModel(**serialized_tournament)
            tournaments_list.append(tournament)
        return tournaments_list