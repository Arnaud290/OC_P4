"""round model module"""
from.model import Model


class MatchModel(Model):
    """round model class"""
    def __init__(self, player1, player2):
        self.id = self.get_number()
        self.matchs_list = []
        self.end = False
        self.id_tourament = ''
