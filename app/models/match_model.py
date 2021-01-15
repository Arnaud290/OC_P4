"""match model module"""
from .model import Model


class MatchModel(Model):
    """match model class"""
    def __init__(self, **attributs):
        self.id = self.get_number()
        self.player1_id = None
        self.player2_id = None
        self.player1_name = ''
        self.player2_name = ''
        self.result = ''
        self.finish = False
        self.id_round = ''
        if attributs:
            for attr_name, attr_value in attributs.items():
                setattr(self, attr_name, attr_value)
