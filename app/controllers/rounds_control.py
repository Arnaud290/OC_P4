"""match control module"""
from .controller import Controller


class RoundsControl(Controller):
    """Rounds control class"""
    def __call__(self):
        self.actual_tournaments_list = self.tournaments_list()
        self.tournament = self.actual_tournaments_list[-1]
        self.rounds_model_list = []
