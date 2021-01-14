"""round model module"""
from.model import Model


class RoundModel(Model):
    """round model class"""
    def __init__(self,):
        self.id = self.get_number()
        self.matchs_list = []
        self.end = False
        self.id_tourament = ''
