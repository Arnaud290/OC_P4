"""round model module"""
from.model import Model


class RoundModel(Model):
    """round model class"""
    def __init__(self, **attributs):
        self.id = self.get_number()
        self.matchs_list = []
        self.end = False
        self.id_tourament = ''
        if attributs:
            for attr_name, attr_value in attributs.items():
                setattr(self, attr_name, attr_value)
