"""round model module"""
from.model import Model


class RoundModel(Model):
    """round model class"""
    round_count = 0
    def __init__(self, **attributs):
        RoundModel.round_count += 1
        self.id = self.get_number()
        self.matchs_list = []
        self.in_progress = False
        self.id_tourament = ''
        self.count = RoundModel.round_count
        if attributs:
            for attr_name, attr_value in attributs.items():
                setattr(self, attr_name, attr_value)
