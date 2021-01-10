"""tournament model module"""
from . import model
import time


class TournamentModel(model.Model):
    """Tournament model class"""
    def __init__(self, name, location, nb_players, nb_rounds, time_control, description):
        self.name = ""
        self.location = ""
        self.date = time.strftime("%d/%m/%Y")
        self.nb_players = nb_players
        self.nb_rounds = nb_rounds
        self.round_list = []
        self.player_list = []
        self.time_control = time_control
        self.description = description
        self.in_progress = False

