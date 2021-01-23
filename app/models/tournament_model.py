"""tournament model module"""
import time
from .model import Model
from . import model_template

class TournamentModel(Model):
    """Tournament model class"""
    def __init__(self, **attributs):
        self.id = model_template.ModelTemplate.get_number('TournamentModel')
        self.name = None
        self.location = None
        self.date = time.strftime("%d/%m/%Y")
        self.nb_players = None
        self.nb_rounds = None
        self.round_list = []
        self.player_list = []
        self.time_control = None
        self.description = None
        self.in_progress = False
        self.tab_results = []
        if attributs:
            for attr_name, attr_value in attributs.items():
                setattr(self, attr_name, attr_value)
