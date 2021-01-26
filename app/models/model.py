"""General model module"""
from tinydb import TinyDB, Query


class Model:
    """general model class"""
    db = TinyDB('app/database/db.json')

    def save(self):
        """Method of saving a model"""
        table = Model.db.table(self.__class__.__name__)
        table.insert(self.__dict__)

    def delete(self):
        """Method of deleting a model"""
        table = Model.db.table(self.__class__.__name__)
        query = Query()
        table.remove(query.id == self.id)

    def update(self, key, value):
        """Method for updating a
        model in the database"""
        table = Model.db.table(self.__class__.__name__)
        query = Query()
        table.update({key: value}, query.id == self.id)
