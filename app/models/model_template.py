""" general model module"""
from tinydb import TinyDB, Query
from .player_model import PlayerModel
from .tournament_model import TournamentModel
from .round_model import RoundModel


class ModelTemplate:
    """general model class"""
    db = TinyDB('app/database/db.json')
    @classmethod
    def get_serialized(cls, class_model, id_model = None):
        """get all instances model"""
        table = cls.db.table(class_model)
        serialized_table = table.all()
        if not id_model:    
            return serialized_table
        else:
            return serialized_table[id_model]

    @classmethod
    def delete_all(cls, class_model):
        """delete all instances model"""
        table = cls.db.table(class_model)
        table.truncate()

    @classmethod
    def get_number(cls, class_model):
        """get numbers of instances model saved"""
        table = cls.db.table(class_model)
        number = len(table)
        return number

    @classmethod
    def get_model(cls, model, id_model=None):
        serialized_models = cls.get_serialized(model)
        class_model = eval(model)
        model_list = []
        if not id_model:
            for serialized_model in serialized_models:
                model_list.append(class_model(**serialized_model))
            return model_list
        else:
            serialized_model = cls.get_serialized(model, id_model)
            model_object = class_model(**serialized_model)   
            return model_object
