"""match model module"""
from.model import Model


class MatchModel(Model):
    """match model class"""
    def __init__(self, player1, player2):
        self.id = self.get_number()
        self.player1 = player1
        self.player2 = player2
        self.result = ''
        self.end = False
        self.id_round = ''
