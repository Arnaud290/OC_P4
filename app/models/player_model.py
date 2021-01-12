"""player model module"""
from .model import Model


class PlayerModel(Model):
    """Player model class"""
    def __init__(self, **attributs):
    
        self.id = ''
        self.first_name = ''
        self.last_name = ''
        self.birth_date = ''
        self.sex = ''
        self.rank = ''
        self.tournament_points = ''
        self.tournament_list = ''
        if attributs:
            for attr_name, attr_value in attributs.items():
                setattr(self, attr_name, attr_value)
