"""Tournament model module"""
import datetime


class Tournament:
    """Class for tournaments"""

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.date = datetime.today()
        self.tours = []
        self.players = []
        self.time_control = ""
        self.description = ""
        self.nb_days = 1
        self.date_start_tournament = datetime.today()
        self.date_finish_tournament = datetime.today()
        self.in_progress = True

    def time_contol(self, time_position):
        """Instance method that defines the type of time control"""
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
