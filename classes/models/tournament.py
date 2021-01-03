"""Tournament model module"""
import datetime
from ..models.settings import NB_PLAYERS, NB_ROUNDS
from ..models.player import Player


class Tournament:
    """Class for tournaments"""

    def __init__(self):
        self.name = ""
        self.location = ""
        self.date = datetime.date
        self.rounds = NB_ROUNDS
        self.players = []
        self.time_control = ""
        self.description = ""
        self.nb_days = 1
        self.date_start_tournament = datetime.date
        self.date_finish_tournament = datetime.date
        self.in_progress = True

    def new_tournament(self):
        """Instance method that defines new tournament"""
        self.name = input("Tournament name : ")
        self.location = input("Tournament location : ")
        self.time_contol()
        self.description = input("Tournament description : ")
        self.tournament_players()

    def time_contol(self):
        """Instance method that defines the type of time control"""
        time_position = input("Enter type of time (1 = bullet, 2 = blitz, 3 = rapid) : ")
        if time_position == 1:
            self.time_control = "bullet"
        elif time_position == 2:
            self.time_control = "blitz"
        elif time_position == 3:
            self.time_control = "rapid"

    def description(self, description):
        """Instance method that describes the tournament"""
        self.description = description

    def nb_days(self, nb_days):
        """Instance method that defines the number of days in the tournament"""
        self.nb_days = nb_days
        self.date_finish_tournament = datetime.timedelta(days=nb_days-1)

    def tournament_players(self):
        """Instance method that define list of players"""
        for i in range(NB_PLAYERS):
            player = Player(i)
            self.players.append(player)
            