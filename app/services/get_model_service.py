"""Model recovery service"""
from tinydb import TinyDB


class GetModelService:
    """Get model service class"""
    db = TinyDB('app/database/db.json')

    @classmethod
    def get_serialized(cls, class_model, id_model=None):
        """get the serialized model (s)"""
        table = cls.db.table(class_model)
        serialized_table = table.all()
        if id_model is None:
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
        """get instance with instance id or
        all instances with class model name"""
        serialized_models = cls.get_serialized(model)
        class_model = eval(model)
        model_list = []
        if id_model is None:
            for serialized_model in serialized_models:
                model_list.append(class_model(**serialized_model))
            return model_list
        else:
            serialized_model = cls.get_serialized(model, id_model)
            model_object = class_model(**serialized_model)
            return model_object

    @classmethod
    def get_models_id(cls, list_models):
        """get all id from list of instances model"""
        models_id = []
        for model in list_models:
            models_id.append(model.id)
        return models_id
