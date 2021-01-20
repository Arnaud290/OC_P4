"""player model module"""
from .model import Model


class PlayerModel(Model):
    """Player model class"""
    def __init__(self, **attributs):
        self.id = None
        self.first_name = None
        self.last_name = None
        self.birth_date = None
        self.sex = None
        self.rank = None
        self.tournament_points = 0.0
        self.tournament_list = None
        self.no_vs = []
        self.vs = []
        if attributs:
            for attr_name, attr_value in attributs.items():
                setattr(self, attr_name, attr_value)
