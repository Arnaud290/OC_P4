"""match model module"""
from .model import Model


class MatchModel(Model):
    """match model class"""
    def __init__(self, **attributs):
        self.match_nb = None
        self.id = self.get_number()
        self.p1_id = None
        self.p2_id = None
        self.result = ''
        self.finish = False
        self.id_round = ''
        if attributs:
            for attr_name, attr_value in attributs.items():
                setattr(self, attr_name, attr_value)
