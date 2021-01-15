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
        serialized_players = models.player_model.PlayerModel.get_serialized()
        for serialized_player in serialized_players:
            player = models.player_model.PlayerModel(**serialized_player)
            player_list.append(player)
        return player_list

    @staticmethod
    def tournaments_list():
        """return list of objects tournaments"""
        tournaments_list = []
        serialized_tournaments = models.tournament_model.TournamentModel.get_serialized()
        for serialized_tournament in serialized_tournaments:
            tournament = models.tournament_model.TournamentModel(**serialized_tournament)
            tournaments_list.append(tournament)
        return tournaments_list

    @staticmethod
    def rounds_list():
        """return list of objects tournaments"""
        rounds_list = []
        serialized_rounds = models.round_model.RoundModel.get_serialized()
        for serialized_round in serialized_rounds:
            rounds = models.round_model.RoundModel(**serialized_round)
            rounds_list.append(rounds)
        return rounds_list

    @staticmethod
    def matchs_list():
        """return list of objects tournaments"""
        matchs_list = []
        serialized_matchs = models.match_model.MatchModel.get_serialized()
        for serialized_match in serialized_matchs:
            match = models.match_model.MatchModel(**serialized_match)
            matchs_list.append(match)
        return matchs_list
