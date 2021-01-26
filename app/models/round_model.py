"""Round model module"""
from .model import Model
from .. import services


class RoundModel(Model):
    """Round model class"""
    def __init__(self, **attributs):
        self.id = services.get_model_service.GetModelService.get_number('RoundModel')
        self.match_nb = 0
        self.matchs_list = []
        self.start = False
        self.finish = False
        self.id_tourament = ''
        self.count = 0
        self.name = None
        self.date_start = None
        self.date_finish = None
        self.finish_matchs = []
        if attributs:
            for attr_name, attr_value in attributs.items():
                setattr(self, attr_name, attr_value)
