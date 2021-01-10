"""match model module"""
from. import model


class MatchModel(model.Model):
    """match model class"""
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.result = ''
        self.end = False