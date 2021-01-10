"""player model module"""
from . import model


class PlayerModel(model.Model):
    """Player model class"""
    def __init__(self, first_name, last_name, birth_date, sex, rank):
    
    self.first_name = first_name
    self.last_name = last_name
    self.birth_date = birth_date
    self.sex = sex
    self.rank = rank