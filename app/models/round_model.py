"""round model module"""
from. import model


class MatchModel(model.Model):
    """round model class"""
    def __init__(self, player1, player2):
        self.id = self.get_number()
        self.matchs_list = []
        self.end = False
        self.id_tourament = ''