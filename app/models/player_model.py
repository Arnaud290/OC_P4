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
        self.tournament_points = None
        self.tournament_list = None
        if attributs:
            for attr_name, attr_value in attributs.items():
                setattr(self, attr_name, attr_value)
