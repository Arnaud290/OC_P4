"""Round model module"""
from .model import Model


class RoundModel(Model):
    """Round model class"""
    def __init__(self, **attributs):
        self.match_nb = 0
        self.matchs_list = []
        self.start = False
        self.finish = False
        self.count = 0
        self.name = None
        self.date_start = None
        self.date_finish = None
        self.finish_matchs = []
        if attributs:
            for attr_name, attr_value in attributs.items():
                setattr(self, attr_name, attr_value)
